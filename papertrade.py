"""Daily paper trader with nightly learning. Run every few minutes by launchd; acts by IST time.

Phases (trading days only):
  premarket  >= 08:30  holiday check, age open positions
  monitor    09:15-15:30  stop/target exits from live 1-minute bars
  entry      15:15-15:28  time exits, score today's 3%+ movers with the model, buy at ~close
  eod        >= 16:00  update history, label predictions, retrain model, adapt threshold, write report
Cloud (GitHub Actions): `job` runs after the close (any hour, GitHub cron is often hours late) and processes
every closed session not yet done: stops/targets from that day's 1-minute bars, buy at the close, learn.
Usage: .venv/bin/python papertrade.py [tick|loop|job entry|job eod|report|status] [--force PHASE]
"""
import argparse
import datetime as dt
import json
import os
import time
import traceback
from zoneinfo import ZoneInfo

import joblib
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from sklearn.neighbors import NearestNeighbors

import model as M
import reporting as R
import research

IST = ZoneInfo("Asia/Kolkata")
PAPER = os.path.join(M.DATA, "paper")
REPORTS = os.environ.get("STOCKS_REPORTS", os.path.join(M.ROOT, "reports", "paper"))
STATE = os.path.join(PAPER, "state.json")
CFG = os.path.join(M.DATA, "model_config.json")
SHADOW = os.path.join(M.DATA, "shadow_config.json")  # challenger settings found by the weekly self-tuning
SHADOW_MODEL = os.path.join(M.DATA, "model_shadow.joblib")  # only when the challenger uses another hold policy
PROMOTE_TRADES = 20
RUN_BUDGET = dt.timedelta(hours=5, minutes=30)  # GitHub kills a job at 6h; hand over to a fresh run before that
CONTINUE = os.path.join(PAPER, "continue.flag")
OUTBOX = os.path.join(PAPER, "outbox.json")
START_CAPITAL = 100000.0
END_DATE = "2026-12-02"  # 8 weeks of sessions
BOOKS = ("main", "lookalike")


DAY = None  # trading session being processed (dt.date); set by job() so late or catch-up runs book the right day


def now():
    return dt.datetime.now(IST)


def today():
    return DAY or now().date()


def ds():
    return today().strftime("%Y-%m-%d")


def stamp():
    return f"{now():%H:%M}" if today() == now().date() else "close"


def target(cfg):
    return "y_" + cfg.get("policy", "h1")


def note(st, what):
    st.setdefault("incidents", []).append({"date": ds(), "what": what})


def log(msg):
    os.makedirs(PAPER, exist_ok=True)
    line = f"{now():%Y-%m-%d %H:%M:%S} {msg}"
    with open(os.path.join(PAPER, "log.txt"), "a") as f:
        f.write(line + "\n")
    print(line)


def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, default=str)
    os.replace(tmp, path)


def new_state():
    return {"start": ds(), "end": END_DATE, "done": {}, "finished": False,
            "books": {b: {"cash": START_CAPITAL, "positions": []} for b in BOOKS}}


def append_csv(name, rows):
    if not rows:
        return
    path = os.path.join(PAPER, name)
    pd.DataFrame(rows).to_csv(path, mode="a", header=not os.path.exists(path), index=False)


def read_csv(name):
    path = os.path.join(PAPER, name)
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()


# ---------- calendar ----------
def holidays():
    path = os.path.join(PAPER, "holidays.json")
    cached = load_json(path, None)
    if cached and cached.get("year") == now().year:
        return set(cached["dates"])
    try:
        r = requests.get("https://www.nseindia.com/api/holiday-master?type=trading", headers=M.UA, timeout=15)
        dates = [dt.datetime.strptime(h["tradingDate"], "%d-%b-%Y").strftime("%Y-%m-%d") for h in r.json()["CM"]]
        save_json(path, {"year": now().year, "dates": dates})
        return set(dates)
    except Exception as e:
        log(f"holiday fetch failed ({e}); using weekday rule")
        return set(cached["dates"]) if cached else set()


def is_trading_day(d):
    return d.weekday() < 5 and d.strftime("%Y-%m-%d") not in holidays()


# ---------- prices ----------
def intraday(syms):
    df = yf.download([s + ".NS" for s in syms], start=today(), end=today() + dt.timedelta(days=1), interval="1m",
                     group_by="ticker", auto_adjust=False, progress=False, threads=True)
    out = {}
    for s in syms:
        t = s + ".NS"
        if t in df.columns.get_level_values(0):
            d = df[t].dropna(subset=["Close"])
            d = d[d.index.tz_convert(IST).date == today()]
            if len(d):
                out[s] = d
    missing = [s for s in syms if s not in out]
    if missing:  # no 1-minute bars: fall back to the day's daily bar (same rule as the research backtest)
        for k, v in M._download([s + ".NS" for s in missing], "1mo").items():
            v = v[v.index.date == today()]
            if len(v):
                out[k[:-3]] = v
    return out


def equity(book, last):
    return book["cash"] + sum(p["qty"] * last.get(p["sym"], p["entry_px"]) for p in book["positions"])


# ---------- trading ----------
def close_position(st, book_name, p, px, reason):
    book = st["books"][book_name]
    gross = (px / p["entry_px"] - 1) * 100
    net = gross - M.COST
    pnl = p["qty"] * (px - p["entry_px"]) - p["qty"] * p["entry_px"] * M.COST / 100
    lesson = lesson_for(p, px, reason, net)
    book["cash"] += p["qty"] * px - p["qty"] * p["entry_px"] * M.COST / 100
    book["positions"].remove(p)
    row = {k: v for k, v in p.items() if k not in ("feat", "fund")}
    row.update(book=book_name, exit_date=ds(), exit_time=stamp(), exit_px=round(px, 2),
               reason=reason, ret_net=round(net, 2), pnl=round(pnl, 2), lesson=lesson)
    row.update({"f_" + k: v for k, v in p["feat"].items()})
    row.update({"fund_" + k: v for k, v in (p.get("fund") or {}).items()})
    append_csv("trades.csv", [row])
    log(f"[{book_name}] SELL {p['sym']} {p['qty']} @ {px:.2f} ({reason}) net {net:+.2f}% pnl {pnl:+.0f} | {lesson}")


def lesson_for(p, px, reason, net):
    f = p["feat"]
    if net > 0:
        return f"worked: {reason}; entered on {f['r1']:+.1f}% day, close-in-range {f['clv']:.2f}, pred {p['pred']:+.2f}"
    tags = []
    if reason == "gap_stop":
        tags.append("gapped below stop overnight (overnight risk)")
    if reason == "stop":
        tags.append("hit stop intraday")
    if reason == "time" and net > -1:
        tags.append("no follow-through, small time-exit loss (costs)")
    if f["r1"] > 0 and f["clv"] < 0.7:
        tags.append("up-day but closed off highs")
    if f["n_r1"] < -0.5:
        tags.append("weak market day at entry")
    if p.get("analog_avg") is not None and p["analog_avg"] <= 0:
        tags.append("historical analogs were negative")
    if f["rsi"] > 75:
        tags.append("overbought RSI")
    return "; ".join(tags) or "no obvious flag - normal variance"


def ensure_data(syms, band, series):
    if not os.path.exists(M.HIST):
        log("no cached price history - downloading 2 years (first cloud run)")
        M.update_history(syms)
    ev_path = os.path.join(M.DATA, "events.pkl")
    if not os.path.exists(ev_path):
        M.build_events(M.load_history(), syms, band, series).to_pickle(ev_path)


def shadow_cfg(st):
    c = load_json(SHADOW, None)
    if c and "shadow" not in st["books"]:
        st["books"]["shadow"] = {"cash": START_CAPITAL, "positions": []}
        log(f"shadow book started: {c.get('name')} {c}")
    return c


def phase_premarket(st):
    M.refresh_reference_files()
    for b in st["books"]:
        for p in st["books"][b]["positions"]:
            if p["entry_date"] != ds():
                p["sessions"] = p.get("sessions", 0) + 1
    log("premarket: trading day, positions aged " +
        ", ".join(f"{p['sym']}({p['sessions']})" for b in st["books"] for p in st["books"][b]["positions"]))


def phase_monitor(st):
    pos = [(b, p) for b in st["books"] for p in list(st["books"][b]["positions"])]
    live = [(b, p) for b, p in pos if p["sessions"] >= p["min_hold"]]
    if not live:
        return
    bars = intraday(sorted({p["sym"] for _, p in live}))
    for b, p in live:
        d = bars.get(p["sym"])
        if d is None:
            continue
        lc_px = p["prev_close"] * (1 - (p["band"] - 0.3) / 100)
        if d["Close"].iloc[-1] <= lc_px and d["High"].max() - d["Low"].min() <= d["Close"].iloc[-1] * 0.002:
            continue  # locked at lower circuit: no buyers
        o = d["Open"].iloc[0]
        if o <= p["stop"]:
            close_position(st, b, p, o, "gap_stop")
            continue
        if o >= p["target"]:
            close_position(st, b, p, o, "gap_target")
            continue
        for _, r in d.iterrows():
            if r["Low"] <= p["stop"]:
                close_position(st, b, p, p["stop"], "stop")
                break
            if r["High"] >= p["target"]:
                close_position(st, b, p, p["target"], "target")
                break


def phase_entry(st):
    cfg = load_json(CFG, {})
    syms, band, series, industry = M.load_meta()
    ensure_data(syms, band, series)
    hist = M.load_history()

    # time exits first (frees slots), at live price
    due = [(b, p) for b in st["books"] for p in list(st["books"][b]["positions"])
           if p["sessions"] >= max(p["hold"], p["min_hold"])]
    if due:
        bars = intraday(sorted({p["sym"] for _, p in due}))
        for b, p in due:
            d = bars.get(p["sym"])
            if d is not None:
                close_position(st, b, p, float(d["Close"].iloc[-1]), "time")

    # today's live daily bar for the whole universe, appended to history -> identical feature code as training
    tick = [s + ".NS" for s in syms] + ["^NSEI", "^INDIAVIX"]
    bars = M._download(tick, "1mo")
    h2 = {s: v[v.index.date < today()] for s, v in hist.items()}
    for k, v in bars.items():
        s = k[:-3] if k.endswith(".NS") else k
        v = v[v.index.date == today()]
        if s in h2 and len(v):
            h2[s] = pd.concat([h2[s], v])
    if "^NSEI" not in h2 or h2["^NSEI"].index[-1].date() != today():
        raise RuntimeError(f"no daily bars for {ds()} on Yahoo yet")
    h2 = M.fill_gaps(h2, syms)
    syms = [s for s in syms if s in h2 and h2[s].index[-1].date() == today()]
    cands = M.build_events(h2, syms, band, series, with_labels=False, only_last=True)
    cands = cands[cands.date.dt.date == today()] if len(cands) else cands
    if cands.empty:
        log("entry: no 3%+ movers passed filters")
        return
    mdl = joblib.load(os.path.join(M.DATA, "model.joblib"))
    if not M.canary_ok(mdl):
        log("entry ABORTED: model canary mismatch (wrong or corrupted model file); no trades today")
        return
    cands["pred"] = mdl.predict(cands[M.FEATS])
    thr = st.get("thr", cfg.get("thr", 1.0))
    append_csv("predictions.csv", cands[["date", "sym", "pred", "r1", "close"] + M.FEATS].assign(thr=thr).to_dict("records"))

    # guard: re-score each candidate from a fresh float copy; any mismatch means the scoring is unreliable today
    check = mdl.predict(cands[M.FEATS].astype(float).round(6).to_numpy())
    bad = np.abs(check - cands["pred"].to_numpy()) > 0.05
    if bad.any():
        log(f"entry ABORTED: prediction self-check failed for {list(cands.sym[bad])[:10]}; no trades today")
        return

    ev = pd.read_pickle(os.path.join(M.DATA, "events.pkl")).dropna(subset=["y_h1"])
    mu, sd = ev[M.FEATS].mean(), ev[M.FEATS].std().replace(0, 1)
    z = lambda df: ((df[M.FEATS] - mu) / sd).fillna(0).to_numpy()
    past = ev[ev.date < pd.Timestamp(today()) - pd.Timedelta(days=7)]
    nn_past = NearestNeighbors(n_neighbors=30).fit(z(past))

    def analog_avg(r):
        return past.iloc[nn_past.kneighbors(z(r.to_frame().T))[1][0]]["y_h1"].mean()

    picks = cands[cands.pred > thr].sort_values("pred", ascending=False)
    main = st["books"]["main"]
    held = {p["sym"] for b in BOOKS for p in st["books"][b]["positions"]}
    risk_mult = st.get("risk_mult", 1.0)
    chosen = []
    for _, r in picks.iterrows():
        if len(main["positions"]) >= cfg.get("slots", 3):
            break
        if r.sym in held:
            continue
        an = analog_avg(r)
        size = (1.0 if an > 0 else 0.5) * risk_mult
        if open_position(st, "main", r, cfg, band, series, hist, size, an, industry):
            chosen.append(r.sym)
            held.add(r.sym)

    # shadow book: challenger settings from the weekly self-tuning; runs independently of main
    scfg = shadow_cfg(st)
    if scfg:
        sc, sb = {**cfg, **scfg}, st["books"]["shadow"]
        sheld = {p["sym"] for p in sb["positions"]}
        sc_c = cands
        if sc.get("policy") != cfg.get("policy") and os.path.exists(SHADOW_MODEL):
            sc_c = cands.assign(pred=joblib.load(SHADOW_MODEL).predict(cands[M.FEATS]))
        for _, r in sc_c[sc_c.pred > sc["thr"]].sort_values("pred", ascending=False).iterrows():
            if len(sb["positions"]) >= sc.get("slots", 3):
                break
            if r.sym not in sheld:
                an = analog_avg(r)
                if open_position(st, "shadow", r, sc, band, series, hist, 1.0 if an > 0 else 0.5, an, industry,
                                 note=f"shadow: {sc.get('name', '')}"):
                    sheld.add(r.sym)

    # look-alike book: closest same-day fingerprint to each main pick (tests the "similar stocks" idea)
    pool = cands[~cands.sym.isin(held)]
    if chosen and len(pool):
        nn_day = NearestNeighbors(n_neighbors=1).fit(z(pool))
        for s in chosen:
            row = cands[cands.sym == s]
            dist, ix = nn_day.kneighbors(z(row))
            r = pool.iloc[ix[0][0]]
            if r.sym in held or len(st["books"]["lookalike"]["positions"]) >= cfg.get("slots", 3):
                continue
            if open_position(st, "lookalike", r, cfg, band, series, hist, 1.0, np.nan, industry,
                             note=f"lookalike of {s} (distance {dist[0][0]:.2f})"):
                held.add(r.sym)
    log(f"entry: {len(cands)} movers scored, {len(picks)} above thr {thr:.2f}, bought {chosen}")


def fundamentals(sym):
    try:
        i = yf.Ticker(sym + ".NS").info
        pe, px = i.get("trailingPE"), i.get("currentPrice") or 0
        if pe and (i.get("trailingEps") == 1.0 or abs(pe - px) < 0.01 * max(px, 1)):
            pe = None  # Yahoo placeholder EPS=1 makes P/E equal the price
        return {"pe": pe, "pb": i.get("priceToBook"), "mcap_cr": round((i.get("marketCap") or 0) / 1e7),
                "de": i.get("debtToEquity"), "roe": i.get("returnOnEquity"), "sector": i.get("sector")}
    except Exception:
        return {}


def open_position(st, book_name, r, cfg, band, series, hist, size, analog_avg, industry, note=""):
    book = st["books"][book_name]
    last = {p["sym"]: p["entry_px"] for p in book["positions"]}
    eq = equity(book, last)
    px = float(r.close)
    amt = min(book["cash"], eq / cfg.get("slots", 3) * size)
    qty = int(amt // px)
    if qty < 1:
        return False
    b = float(band.get(r.sym, 20.0))
    p = dict(sym=r.sym, entry_date=ds(), entry_time=stamp(), entry_px=round(px, 2), qty=qty,
             stop=round(px * (1 - cfg["sl"] / 100), 2), target=round(px * (1 + cfg["tp"] / 100), 2),
             hold=cfg["hold"], min_hold=2 if series.get(r.sym) == "BE" else 1, sessions=0, band=b,
             series=series.get(r.sym, "EQ"), industry=industry.get(r.sym, ""), prev_close=px,
             pred=round(float(r.pred), 3), analog_avg=None if pd.isna(analog_avg) else round(float(analog_avg), 3),
             size_mult=size, note=note, cfg_ver=cfg.get("version", 1),
             feat={k: round(float(r[k]), 3) for k in M.FEATS}, fund=fundamentals(r.sym))
    book["cash"] -= qty * px
    book["positions"].append(p)
    log(f"[{book_name}] BUY {r.sym} {qty} @ {px:.2f} (Rs {qty * px:,.0f}) pred {r.pred:+.2f} day {r.r1:+.1f}% "
        f"size x{size} {note} | PE {p['fund'].get('pe')} mcap {p['fund'].get('mcap_cr')}Cr")
    return True


def phase_eod(st):
    syms, band, series, _ = M.load_meta()
    ensure_data(syms, band, series)
    hist = M.load_history()
    fresh = M._download([s + ".NS" for s in syms] + ["^NSEI", "^INDIAVIX"], "1mo")
    for k, v in fresh.items():
        s = k[:-3] if k.endswith(".NS") else k
        old = hist.get(s)
        hist[s] = v if old is None else pd.concat([old, v])[lambda x: ~x.index.duplicated(keep="last")].sort_index()
        hist[s] = hist[s].iloc[-520:]
    hist = M.fill_gaps(hist, syms)
    pd.to_pickle(hist, M.HIST)
    # learn and mark to market only with data up to the session being processed (no peeking on catch-up runs)
    hist = {s: v[v.index.date <= today()] for s, v in hist.items()}

    # learning step 1: rebuild labelled events (adds every newly completed setup, incl. our live trades) and refit
    ev = M.build_events(hist, syms, band, series)
    ev.to_pickle(os.path.join(M.DATA, "events.pkl"))
    cfg = load_json(CFG, {})
    mdl = M.fit(ev, target(cfg))
    M.save_model(mdl, ev)
    st["model_through"] = ds()
    scfg = load_json(SHADOW, None)
    if scfg and scfg.get("policy") != cfg.get("policy"):
        joblib.dump(M.fit(ev, target(scfg)), SHADOW_MODEL)

    # learning step 2: score yesterday's predictions against what actually happened
    pr = read_csv("predictions.csv")
    acc = {}
    if len(pr):
        pr["date"] = pd.to_datetime(pr["date"])
        lab = pr.merge(ev[["sym", "date", "y_h1"]], on=["sym", "date"], how="left").dropna(subset=["y_h1"])
        if len(lab):
            hi = lab[lab.pred > lab.thr]
            acc = dict(labelled=len(lab), corr=round(lab.pred.corr(lab.y_h1), 3) if len(lab) > 5 else None,
                       above_thr=len(hi), above_thr_avg=round(hi.y_h1.mean(), 2) if len(hi) else None,
                       below_thr_avg=round(lab[lab.pred <= lab.thr].y_h1.mean(), 2))

    # learning step 3: adapt threshold / size from live paper results (risk governor)
    tr = read_csv("trades.csv")
    thr, risk = st.get("thr", cfg.get("thr", 1.0)), st.get("risk_mult", 1.0)
    base = cfg.get("thr", 1.0)
    m = tr[tr.book == "main"] if len(tr) else tr
    if len(m) >= 8:
        recent = m.ret_net.tail(10).mean()
        if recent < -0.3:
            thr, risk = min(thr + 0.2, base + 0.8), 0.5
        elif recent > 0.5:
            thr, risk = max(thr - 0.1, base - 0.2), 1.0
        else:
            risk = 1.0 if recent > 0 else 0.75
    st["thr"], st["risk_mult"] = round(thr, 2), risk
    evolve(st, ev, hist, weekly=week_ends_today(st))
    risk = st["risk_mult"]

    # mark to market
    last = {p["sym"]: float(hist[p["sym"]]["Close"].iloc[-1]) for b in st["books"]
            for p in st["books"][b]["positions"] if p["sym"] in hist}
    rows = [dict(date=ds(), book=b, equity=round(equity(st["books"][b], last), 2),
                 cash=round(st["books"][b]["cash"], 2), open=len(st["books"][b]["positions"])) for b in st["books"]]
    append_csv("equity.csv", rows)
    st.setdefault("learning", []).append(dict(date=ds(), train_rows=int(ev.y_h1.notna().sum()),
                                              thr=st["thr"], risk_mult=risk, **acc))
    headline = write_report(st, last, report_ctx(st, hist, len(syms), int(ev.y_h1.notna().sum()), acc))
    queue_mail(os.path.join(REPORTS, f"{ds()}.md"), f"[Paper trade] Daily {today():%d %b}: {headline}")
    if week_ends_today(st):
        path = write_weekly(st, last)
        queue_mail(path, f"[Paper trade] Weekly review {os.path.basename(path)[:-3]}: {headline}")
    log(f"eod: model retrained on {int(ev.y_h1.notna().sum())} setups; thr {st['thr']} risk x{risk}; accuracy {acc}")


def queue_mail(path, subject):
    box = load_json(OUTBOX, [])
    box.append({"path": os.path.relpath(path, M.ROOT), "subject": subject})
    save_json(OUTBOX, box)


def settings_text(c):
    return (f"score bar {c['thr']}, up to {c['slots']} stocks, hold {c['hold']} day(s), "
            f"target +{c['tp']}%, stop-loss -{c['sl']}%")


def evolve(st, ev, hist, weekly):
    """Self-tuning. Weekly: search settings on the last 12 months of unseen data; a clear winner trades in the
    shadow book. Daily: once the shadow has PROMOTE_TRADES closed trades and made more money than main over the
    same period, its settings replace main automatically (versioned in model_config.json)."""
    cfg, scfg = load_json(CFG, {}), load_json(SHADOW, None)
    if scfg:
        tr = read_csv("trades.csv")
        t = tr[tr.exit_date >= scfg["started"]] if len(tr) else tr
        s = t[t.book == "shadow"] if len(t) else t
        m = t[t.book == "main"] if len(t) else t
        s_pnl, m_pnl = (float(x.pnl.sum()) if len(x) else 0.0 for x in (s, m))
        if len(s) >= PROMOTE_TRADES and s_pnl > m_pnl and s.ret_net.mean() > 0:
            v = cfg.get("version", 1) + 1
            old = settings_text(cfg)
            cfg.update({k: scfg[k] for k in ("policy", "hold", "tp", "sl", "thr", "slots")}, version=v,
                       research=scfg["evidence"], trained_to=ds())
            cfg.setdefault("changelog", []).append(dict(
                version=v, date=ds(), change=f"auto-promoted challenger: {settings_text(cfg)} (was {old})",
                evidence=f"live since {scfg['started']}: challenger {len(s)} trades Rs {s_pnl:+,.0f} vs main "
                         f"{len(m)} trades Rs {m_pnl:+,.0f}; backtest {scfg['evidence']}"))
            save_json(CFG, cfg)
            M.save_model(M.fit(ev, target(cfg)), ev)
            st["thr"], st["risk_mult"] = cfg["thr"], 1.0
            for f in (SHADOW, SHADOW_MODEL):
                if os.path.exists(f):
                    os.remove(f)
            note(st, f"Settings upgraded automatically (version {v}). The practice settings made Rs {s_pnl:+,.0f} "
                     f"over {len(s)} trades versus Rs {m_pnl:+,.0f} for the main settings, so the main strategy now "
                     f"uses: {settings_text(cfg)}.")
            log(f"evolve: promoted challenger to main v{v}: {settings_text(cfg)}")
        elif len(s) >= 2 * PROMOTE_TRADES:
            for f in (SHADOW, SHADOW_MODEL):
                if os.path.exists(f):
                    os.remove(f)
            note(st, f"The practice settings ({settings_text(scfg)}) did not beat the main strategy over {len(s)} "
                     f"trades (Rs {s_pnl:+,.0f} vs Rs {m_pnl:+,.0f}), so they were dropped.")
            log("evolve: challenger retired")
        return
    if not weekly or st["books"].get("shadow", {}).get("positions"):
        return
    cur, best, res = research.tune(ev, list(hist["^NSEI"].index), cfg)
    res.sort_values("total", ascending=False).to_csv(os.path.join(PAPER, "tuning_latest.csv"), index=False)
    same = best is not None and (best["policy"], best["thr"], best["slots"]) == \
        (cfg.get("policy"), cfg.get("thr"), cfg.get("slots"))
    log(f"evolve: weekly search current={cur and {k: cur[k] for k in ('trades', 'total', 'pf', 'maxdd')}} "
        f"best={best and {k: best[k] for k in ('policy', 'thr', 'slots', 'trades', 'total', 'pf', 'maxdd')}}")
    if best is None or same or (cur is not None and best["total"] < cur["total"] + 5):
        return
    H, tp, sl = M.POLICIES[best["policy"]]
    ch = dict(policy=best["policy"], hold=H, tp=tp, sl=sl, thr=float(best["thr"]), slots=int(best["slots"]),
              started=ds(), evidence=dict(oos=best["oos"], trades=best["trades"], avg_net=best["avg"],
                                          win=best["win"], pf=best["pf"], total=best["total"],
                                          wk8_median=best["wk8_med"], wk8_worst=best["wk8_worst"],
                                          maxdd=best["maxdd"]))
    ch["name"] = settings_text(ch)
    save_json(SHADOW, ch)
    if ch["policy"] != cfg.get("policy"):
        joblib.dump(M.fit(ev, target(ch)), SHADOW_MODEL)
    st["books"]["shadow"] = {"cash": START_CAPITAL, "positions": []}
    note(st, f"Weekly self-tuning found settings that earned {best['total']:+.1f}% over the last 12 months of "
             f"unseen data, versus {cur['total'] if cur else '?'}% for the current ones: {ch['name']}. They now "
             f"trade in a separate practice account and replace the main settings automatically if they make "
             f"more money over the next {PROMOTE_TRADES} trades.")
    log(f"evolve: new challenger {ch}")


def week_ends_today(st):
    n = today()
    if f"{n:%Y-%m-%d}" >= st["end"]:
        return True
    x = n + dt.timedelta(days=1)
    while not is_trading_day(x):
        x += dt.timedelta(days=1)
    return x.isocalendar()[1] != n.isocalendar()[1]


# ---------- reporting ----------
def stats(df):
    if df is None or df.empty:
        return dict(trades=0)
    w, l = df[df.ret_net > 0], df[df.ret_net <= 0]
    return dict(trades=len(df), win=round(len(w) / len(df) * 100, 1), avg=round(df.ret_net.mean(), 2),
                pf=round(w.ret_net.sum() / -l.ret_net.sum(), 2) if len(l) and l.ret_net.sum() < 0 else None,
                pnl=round(df.pnl.sum()))


def report_ctx(st, hist=None, universe=None, train_rows=None, acc=None):
    day = ds()
    ctx = {"day": day, "universe": universe, "train_rows": train_rows or 0, "acc": acc or {}}
    if hist is not None and "^NSEI" in hist:
        n = hist["^NSEI"]["Close"]
        ctx.update(nifty_close=float(n.iloc[-1]), nifty_chg=float((n.iloc[-1] / n.iloc[-2] - 1) * 100),
                   vix=float(hist["^INDIAVIX"]["Close"].iloc[-1]) if "^INDIAVIX" in hist else None)
    pr = read_csv("predictions.csv")
    if len(pr):
        pr = pr[pr.date.astype(str).str.startswith(day)]
    if len(pr):
        thr = st.get("thr", 1.0)
        bought = {b: {p["sym"] for p in st["books"][b]["positions"] if p["entry_date"] == day} for b in st["books"]}
        held = {p["sym"] for b in st["books"] for p in st["books"][b]["positions"] if p["entry_date"] != day}

        def decision(r):
            if r.sym in bought.get("main", ()):
                return "**Bought**"
            if r.sym in bought.get("lookalike", ()):
                return "Bought in look-alike experiment"
            if r.pred <= r.thr:
                return "Skipped - score below the bar"
            if r.sym in held:
                return "Skipped - already holding"
            return "Skipped - all slots full"
        top = pr.sort_values("pred", ascending=False).head(8).copy()
        top["decision"] = top.apply(decision, axis=1)
        ctx.update(movers=len(pr), above_bar=int((pr.pred > pr.thr).sum()), top=top)
    return ctx


def write_report(st, last, ctx=None):
    os.makedirs(REPORTS, exist_ok=True)
    tr, eq = read_csv("trades.csv"), read_csv("equity.csv")
    day = ds()
    cfg = load_json(CFG, {})
    text = R.daily_md(st, cfg, tr, eq, last, ctx or report_ctx(st), START_CAPITAL, M.COST)
    for name in (f"{day}.md", "latest.md"):
        with open(os.path.join(REPORTS, name), "w") as f:
            f.write(text)
    main = st["books"]["main"]
    e = main["cash"] + sum(p["qty"] * last.get(p["sym"], p["entry_px"]) for p in main["positions"])
    return f"{R.inr(e)} ({R.pct((e / START_CAPITAL - 1) * 100)} total)"


def write_weekly(st, last):
    n = today()
    y, w, _ = n.isocalendar()
    wk_start = (n - dt.timedelta(days=n.weekday())).strftime("%Y-%m-%d")
    tr, eq = read_csv("trades.csv"), read_csv("equity.csv")
    cfg = load_json(CFG, {})
    r = cfg.get("research", {})
    wk = tr[tr.exit_date >= wk_start] if len(tr) else tr
    md = [f"# Weekly paper-trading review - {y}-W{w:02d} (week of {wk_start})", "",
          f"Config version {cfg.get('version', 1)} | hold {cfg.get('hold')} | target +{cfg.get('tp')}% | "
          f"stop -{cfg.get('sl')}% | threshold now {st.get('thr', cfg.get('thr'))} | risk x{st.get('risk_mult', 1.0)}"
          + (f" | shadow: {load_json(SHADOW, {})}" if os.path.exists(SHADOW) else ""), "",
          "## This week vs whole run",
          "| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for b in st["books"]:
        ws = stats(wk[wk.book == b] if len(wk) else None)
        cs = stats(tr[tr.book == b] if len(tr) else None)
        md.append(f"| {b} | {ws['trades']} | {ws.get('win', '-')} | {ws.get('avg', '-')} | {ws.get('pnl', '-')} | "
                  f"{cs['trades']} | {cs.get('win', '-')} | {cs.get('avg', '-')} | {cs.get('pf', '-')} | "
                  f"{equity(st['books'][b], last):,.0f} |")
    n_main = int((tr.book == "main").sum()) if len(tr) else 0
    md += ["", f"Research expectation: avg {r.get('avg_net')}% / trade, win {r.get('win')}%, PF {r.get('pf')}. "
               f"Evidence: {n_main} main trades of ~80 needed for a confident verdict.", ""]
    cols = [c for c in ("book", "sym", "entry_date", "exit_date", "entry_px", "exit_px", "reason", "ret_net", "pnl",
                        "pred", "analog_avg", "cfg_ver", "lesson") if c in tr.columns]
    if len(wk):
        md += ["## Trades closed this week", wk[cols].to_markdown(index=False), ""]
        losers = wk[(wk.book == "main") & (wk.ret_net <= 0)]
        if len(losers):
            tags = losers.lesson.str.split("; ").explode().value_counts()
            md += ["## Loss reasons this week (main)", tags.to_frame("count").to_markdown(), ""]
    learn = [x for x in st.get("learning", []) if x["date"] >= wk_start]
    if learn:
        md += ["## Learning log this week", pd.DataFrame(learn).to_markdown(index=False), ""]
    if len(eq):
        md += ["## Equity this week", eq[eq.date >= wk_start].pivot_table(index="date", columns="book",
                                                                         values="equity").to_markdown(), ""]
    md += ["## Review checklist (/weekly-review)",
           "- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt",
           "- News or results around each losing trade (was it predictable?)",
           "- Live results vs research expectation; do not change settings on fewer than ~20 trades",
           "- Any change must pass research.py walk-forward, or run as a shadow book first", ""]
    out = os.path.join(REPORTS, "weekly")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"{y}-W{w:02d}.md")
    for p in (path, os.path.join(out, "latest.md")):
        with open(p, "w") as f:
            f.write("\n".join(md))
    return path


# ---------- driver ----------
def tick(force=None):
    st = load_json(STATE, None) or new_state()
    n = now()
    day = f"{n:%Y-%m-%d}"
    if st.get("finished"):
        return
    if not force and not is_trading_day(n):
        return
    done = st["done"].setdefault(day, [])
    t = n.time()
    plan = [("premarket", dt.time(8, 30), dt.time(23, 59), phase_premarket),
            ("monitor", dt.time(9, 15), dt.time(15, 30), phase_monitor),
            ("entry", dt.time(15, 15), dt.time(15, 28), phase_entry),
            ("eod", dt.time(16, 0), dt.time(23, 59), phase_eod)]
    for name, t0, t1, fn in plan:
        once = name != "monitor"
        due = (force == name) or (not force and t0 <= t <= t1 and not (once and name in done))
        if name != "premarket" and "premarket" not in done and not force:
            due = False
        if not due:
            continue
        try:
            fn(st)
            if once:
                done.append(name)
        except Exception:
            log(f"{name} FAILED:\n{traceback.format_exc()}")
        save_json(STATE, st)
    if day >= st["end"] and "eod" in done:
        st["finished"] = True
        log("run finished")
    st["done"] = {k: v for k, v in st["done"].items() if k >= (n - dt.timedelta(days=10)).strftime("%Y-%m-%d")}
    save_json(STATE, st)


def pending_sessions(st):
    """Closed trading days after the last completed eod, oldest first. Looks back at most a week because
    Yahoo keeps 1-minute bars (used for stop/target checks) for only ~7 days."""
    n = now()
    last_close = n.date() if n.time() >= dt.time(15, 35) else n.date() - dt.timedelta(days=1)
    since = max([k for k, v in st["done"].items() if "eod" in v], default="")
    days = [last_close - dt.timedelta(days=k) for k in range(7)]
    keep = lambda s: since < s and st["start"] <= s <= st["end"]
    return sorted(d for d in days if is_trading_day(d) and keep(d.strftime("%Y-%m-%d")))


def run_phase(st, name, fn):
    done = st["done"].setdefault(ds(), [])
    if name != "monitor" and name in done:
        return True
    try:
        fn(st)
        if name != "monitor":
            done.append(name)
        ok = True
    except Exception:
        log(f"{ds()} {name} FAILED:\n{traceback.format_exc()}")
        ok = False
    save_json(STATE, st)
    return ok


def catch_up(st):
    """Process every closed session not yet done, at the closing price (same as the research backtest), so a
    run that GitHub starts hours late still books the day."""
    global DAY
    days = pending_sessions(st)
    if not days:
        return
    log(f"catch-up: processing {[f'{d}' for d in days]}")
    since = max([k for k, v in st["done"].items() if "eod" in v], default="")
    if since and st.get("model_through") != since:
        # catch-up after a state rewind: the saved model may have seen later data -> retrain up to `since` only
        syms, band, series, _ = M.load_meta()
        ensure_data(syms, band, series)
        h = M.fill_gaps({s: v[v.index.strftime("%Y-%m-%d") <= since] for s, v in M.load_history().items()}, syms)
        ev = M.build_events(h, syms, band, series)
        ev.to_pickle(os.path.join(M.DATA, "events.pkl"))
        M.save_model(M.fit(ev, target(load_json(CFG, {}))), ev)
        st["model_through"] = since
        log(f"catch-up: model retrained on data up to {since} first")
    for d in days:
        DAY = d
        run_phase(st, "premarket", phase_premarket)
        run_phase(st, "monitor", phase_monitor)
        entered = run_phase(st, "entry", phase_entry)
        fresh = now() < dt.datetime.combine(d, dt.time(15, 30), IST) + dt.timedelta(hours=14)
        if not entered and fresh:
            log(f"{ds()}: entry incomplete (data not ready?) - will retry")
            break
        if not run_phase(st, "eod", phase_eod):
            break
        if ds() >= st["end"]:
            st["finished"] = True
            log("run finished")
            break
    DAY = None


def next_session(st):
    d = now().date()
    for _ in range(10):
        s = d.strftime("%Y-%m-%d")
        if s > st["end"]:
            return None
        still_open = d > now().date() or now().time() < dt.time(15, 35)
        if still_open and is_trading_day(d) and "eod" not in st["done"].get(s, []):
            return d
        d += dt.timedelta(days=1)
    return None


def at(d, h, m):
    return dt.datetime.combine(d, dt.time(h, m), IST)


def live_session(st, d, stop_at):
    """Trade one session live: stop/target checks every 5 min, buy at the live price from 15:15, wrap up after
    the close. Returns True if this run must hand over to a fresh run (time budget used up)."""
    global DAY
    DAY = d
    log(f"live: session {ds()}, this run hands over at {stop_at:%d %b %H:%M} if still busy")
    while True:
        n = now()
        if n >= stop_at:
            return True
        if n < at(d, 9, 10):
            time.sleep(min(600, (min(at(d, 9, 10), stop_at) - n).total_seconds()))
            continue
        run_phase(st, "premarket", phase_premarket)
        if n >= at(d, 15, 35):
            DAY = None
            catch_up(st)
            if "eod" in st["done"].get(d.strftime("%Y-%m-%d"), []) or now() > at(d, 16, 30):
                return False
            DAY = d
            time.sleep(600)
            continue
        if n >= at(d, 9, 15):
            run_phase(st, "monitor", phase_monitor)
        if at(d, 15, 15) <= n <= at(d, 15, 28) and not run_phase(st, "entry", phase_entry):
            time.sleep(60)
            continue
        nxt = min(t for t in (n + dt.timedelta(minutes=5), at(d, 15, 15), at(d, 15, 35), stop_at) if t > n)
        time.sleep(max(1, (nxt - now()).total_seconds()))


def job(kind=None):
    """One cloud run: first books any missed closed session (at the close price), then trades the current or
    next session live if it opens within 6h. When the time budget is used up it writes CONTINUE and the
    workflow starts a fresh run that carries on."""
    global DAY
    t0 = now()
    if os.path.exists(CONTINUE):
        os.remove(CONTINUE)
    st = load_json(STATE, None) or new_state()
    if st.get("finished"):
        log("job: run already finished")
        return
    catch_up(st)
    d = None if st.get("finished") else next_session(st)
    if d is None or at(d, 9, 10) - now() > dt.timedelta(hours=6):
        print(f"job: next session {d} is not close yet - a later scheduled run will start it")
    else:
        stop_at = t0 + RUN_BUDGET
        if at(d, 14, 40) < stop_at < at(d, 15, 50) and t0 < at(d, 14, 40):
            stop_at = at(d, 14, 40)  # never hand over during the 15:15 entry or the close
        if live_session(st, d, stop_at):
            open(CONTINUE, "w").close()
            log("live: time budget used, handing over to a fresh run")
    DAY = None
    cut = (now() - dt.timedelta(days=10)).strftime("%Y-%m-%d")
    st["done"] = {k: v for k, v in st["done"].items() if k >= cut}
    save_json(STATE, st)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="tick", choices=["tick", "loop", "job", "report", "status"])
    ap.add_argument("kind", nargs="?", choices=["entry", "eod"])
    ap.add_argument("--force", choices=["premarket", "monitor", "entry", "eod"])
    a = ap.parse_args()
    os.makedirs(PAPER, exist_ok=True)
    if a.cmd == "tick":
        tick(a.force)
    elif a.cmd == "job":
        job(a.kind or "eod")
    elif a.cmd == "loop":  # for hosts without launchd/cron
        while True:
            try:
                tick()
            except Exception:
                log(f"tick crashed:\n{traceback.format_exc()}")
            time.sleep(180)
    elif a.cmd == "report":
        st = load_json(STATE, new_state())
        write_report(st, {})
        print(open(os.path.join(REPORTS, "latest.md")).read())
    else:
        st = load_json(STATE, new_state())
        print(json.dumps({b: {"cash": round(st["books"][b]["cash"]), "positions": [p["sym"] for p in st["books"][b]["positions"]]}
                          for b in st["books"]}, indent=1), "\ndone:", st["done"], "\nthr:", st.get("thr"), "risk:", st.get("risk_mult"))


if __name__ == "__main__":
    main()
