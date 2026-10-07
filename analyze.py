"""HFCL-style swing scanner: profile HFCL's +/-5% circuit swings and find NSE stocks that behave alike.

Usage: .venv/bin/python analyze.py [--refresh] [--ref HFCL]
"""
import argparse
import os
import pickle
import time

import numpy as np
import pandas as pd
import yfinance as yf

DATA = "data"
CACHE = os.path.join(DATA, "prices.pkl")
OUT = "reports"
BIG = 4.5            # a "5% day" (allows for bands that print 4.95-5.0)
WIN = 120            # profile window, trading days (~6 months)
MIN_TV_CR = 5.0      # min median daily traded value, Rs crore
COST = 0.25          # round-trip cost %, brokerage + STT + slippage


def load_universe():
    sec = pd.read_csv(os.path.join(DATA, "sec_list.csv"), dtype=str)
    sec["Band"] = sec["Band"].str.strip()
    tm = pd.read_csv(os.path.join(DATA, "ind_niftytotalmarket_list.csv"), dtype=str)
    band5 = sec[(sec.Band == "5") & sec.Series.isin(["EQ", "BE"])]
    syms = sorted(set(tm.Symbol) | set(band5.Symbol))
    meta = sec.drop_duplicates("Symbol").set_index("Symbol")[["Series", "Band", "Remarks", "Security Name"]]
    ind = tm.set_index("Symbol")["Industry"]
    return syms, meta, ind


def download(syms, refresh):
    if os.path.exists(CACHE) and not refresh:
        with open(CACHE, "rb") as f:
            return pickle.load(f)
    frames = {}
    tickers = [s + ".NS" for s in syms]
    for i in range(0, len(tickers), 100):
        chunk = tickers[i:i + 100]
        for attempt in range(3):
            try:
                df = yf.download(chunk, period="1y", interval="1d", group_by="ticker",
                                 auto_adjust=True, progress=False, threads=True)
                break
            except Exception as e:  # rate limit bursts
                print("retry", i, e)
                time.sleep(5 * (attempt + 1))
        for t in chunk:
            if t in df.columns.get_level_values(0):
                d = df[t].dropna(how="all")
                d = d[d["Volume"] > 0]  # drop holiday/stub rows Yahoo emits with 0 volume
                if len(d) >= 60:
                    frames[t[:-3]] = d
        print(f"downloaded {min(i + 100, len(tickers))}/{len(tickers)}, usable {len(frames)}")
    with open(CACHE, "wb") as f:
        pickle.dump(frames, f)
    return frames


def rsi(close, n=14):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def atr_pct(d, n=14):
    pc = d["Close"].shift()
    tr = pd.concat([d["High"] - d["Low"], (d["High"] - pc).abs(), (d["Low"] - pc).abs()], axis=1).max(axis=1)
    return (tr.rolling(n).mean() / d["Close"] * 100).iloc[-1]


def flip_rate(r, lookahead=3):
    """Share of big-move days followed within `lookahead` days by a big move the other way."""
    idx = np.where(r.abs() >= BIG)[0]
    if len(idx) == 0:
        return np.nan
    flips = 0
    for i in idx:
        nxt = r.iloc[i + 1:i + 1 + lookahead]
        flips += bool(((np.sign(nxt) == -np.sign(r.iloc[i])) & (nxt.abs() >= BIG)).any())
    return flips / len(idx)


def backtest(d, rule, tp=5.0, sl=5.0, hold=7):
    """Entry next-day open after a signal day; exit at tp/sl (checked on high/low) or after `hold` days."""
    c, o, h, l = d["Close"], d["Open"], d["High"], d["Low"]
    r = c.pct_change() * 100
    r2 = c.pct_change(2) * 100
    if rule == "dip":
        sig = (r <= -BIG) | (r2 <= -8)
    else:  # momentum: buy after a big up day
        sig = r >= BIG
    trades, i, n = [], 1, len(d)
    while i < n - 1:
        if sig.iloc[i]:
            e = o.iloc[i + 1]
            ret = None
            for j in range(i + 1, min(i + 1 + hold, n)):
                if l.iloc[j] <= e * (1 - sl / 100):
                    ret = -sl
                    break
                if h.iloc[j] >= e * (1 + tp / 100):
                    ret = tp
                    break
            if ret is None:
                j = min(i + hold, n - 1)
                ret = (c.iloc[j] / e - 1) * 100
            trades.append(ret - COST)
            i = j + 1
        else:
            i += 1
    if not trades:
        return dict(n=0, win=np.nan, avg=np.nan)
    t = np.array(trades)
    return dict(n=len(t), win=(t > 0).mean() * 100, avg=t.mean())


def profile(sym, d, band, ref_ret=None):
    d = d.iloc[-WIN:]
    c = d["Close"]
    r = c.pct_change().dropna() * 100
    tv = (d["Close"] * d["Volume"]).median() / 1e7
    b = float(band) if band not in (None, "No Band") and pd.notna(band) else None
    uc = lc = 0
    if b:
        full = d.loc[r.index]
        uc = int(((r >= b - 0.15) & (full["Close"] >= full["High"] * 0.998)).sum())
        lc = int(((r <= -(b - 0.15)) & (full["Close"] <= full["Low"] * 1.002)).sum())
    corr = r.corr(ref_ret) if ref_ret is not None else np.nan
    return dict(
        sym=sym, band=band, close=c.iloc[-1], tv_cr=tv,
        vol20=r.iloc[-20:].std(), vol120=r.std(),
        big_up=(r >= BIG).mean() * 100, big_dn=(r <= -BIG).mean() * 100,
        big_60=int((r.iloc[-60:].abs() >= BIG).sum()),
        uc=uc, lc=lc, flip=flip_rate(r), ac1=r.autocorr(1), atr=atr_pct(d),
        range60=(d["High"].iloc[-60:].max() / d["Low"].iloc[-60:].min() - 1) * 100,
        ret_3m=(c.iloc[-1] / c.iloc[-63] - 1) * 100 if len(c) > 63 else np.nan,
        corr=corr,
    )


def levels(d):
    c = d["Close"]
    last = c.iloc[-1]
    hi20, lo20 = d["High"].iloc[-20:].max(), d["Low"].iloc[-20:].min()
    return dict(
        last=last, rsi=rsi(c).iloc[-1], sma20=c.rolling(20).mean().iloc[-1],
        sma50=c.rolling(50).mean().iloc[-1], sma200=c.rolling(200).mean().iloc[-1] if len(c) >= 200 else np.nan,
        hi20=hi20, lo20=lo20, pos20=(last - lo20) / (hi20 - lo20) * 100 if hi20 > lo20 else np.nan,
        hi52=d["High"].max(), lo52=d["Low"].min(), atr=atr_pct(d),
        vol_ratio=d["Volume"].iloc[-5:].mean() / d["Volume"].iloc[-50:].mean(),
    )


def verdict(lv, bt_dip, bt_mom):
    """Rule-based stance from trend, range position, RSI and which swing rule has worked on this stock."""
    up_trend = lv["last"] > lv["sma50"] and (np.isnan(lv["sma200"]) or lv["last"] > lv["sma200"])
    dip_ok = bt_dip["n"] >= 4 and bt_dip["avg"] > 0
    mom_ok = bt_mom["n"] >= 4 and bt_mom["avg"] > 0
    if lv["rsi"] >= 75 and lv["pos20"] >= 90:
        return "Overbought - book profit / wait for a 5% dip"
    if dip_ok and lv["pos20"] <= 35 and lv["rsi"] <= 45:
        if lv["last"] < lv["sma50"]:
            return "Counter-trend dip (below SMA50) - small size only"
        return "BUY zone (near 20d support, dip rule profitable)"
    if mom_ok and up_trend and lv["pos20"] >= 80 and lv["vol_ratio"] >= 1.3:
        return "Momentum BUY (breakout on volume)"
    if dip_ok:
        return "Watchlist - buy on next 5% down day"
    return "Avoid / no edge"


def fmt(df, cols, floatfmt=2):
    out = df[cols].copy()
    for c in out.select_dtypes("number").columns:
        out[c] = out[c].round(floatfmt)
    return out.to_markdown(index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--ref", default="HFCL")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    syms, meta, ind = load_universe()
    print(f"universe: {len(syms)} symbols")
    px = download(syms, a.refresh)
    ref = px[a.ref]
    ref_ret = ref["Close"].pct_change().iloc[-WIN:] * 100

    rows = []
    for s, d in px.items():
        band = meta["Band"].get(s)
        p = profile(s, d, band, ref_ret)
        p["series"] = meta["Series"].get(s)
        p["remarks"] = meta["Remarks"].get(s)
        p["industry"] = ind.get(s, "")
        rows.append(p)
    df = pd.DataFrame(rows).set_index("sym")

    # similarity on the swing fingerprint (z-scored, liquid names only)
    feats = ["vol20", "vol120", "big_up", "big_dn", "flip", "atr", "range60", "ac1"]
    weights = np.array([1.5, 1.0, 1.5, 1.5, 1.5, 1.0, 1.0, 0.5])
    liq = df[(df.tv_cr >= MIN_TV_CR) | (df.index == a.ref)].dropna(subset=feats).copy()
    z = (liq[feats] - liq[feats].mean()) / liq[feats].std()
    liq["distance"] = np.sqrt((((z - z.loc[a.ref]) ** 2) * weights).sum(axis=1))
    liq["similarity"] = (100 * np.exp(-liq["distance"] / 3)).round(1)
    ranked = liq.drop(a.ref).sort_values("distance")
    top = ranked.head(a.top).copy()

    plans = []
    for s in [a.ref] + list(top.index):
        d = px[s]
        lv = levels(d)
        bd, bm = backtest(d, "dip"), backtest(d, "mom")
        atr_ = lv["atr"]
        plans.append(dict(
            sym=s, last=lv["last"], rsi=lv["rsi"], pos20=lv["pos20"], lo20=lv["lo20"], hi20=lv["hi20"],
            sma50=lv["sma50"], sma200=lv["sma200"], vol_ratio=lv["vol_ratio"],
            dip_n=bd["n"], dip_win=bd["win"], dip_avg=bd["avg"],
            mom_n=bm["n"], mom_win=bm["win"], mom_avg=bm["avg"],
            entry=max(lv["lo20"], lv["last"] * (1 - atr_ / 100)),
            stop=lv["lo20"] * 0.97, target=lv["hi20"],
            verdict=verdict(lv, bd, bm),
        ))
    plan = pd.DataFrame(plans)
    df.to_csv(os.path.join(OUT, "all_profiles.csv"))
    ranked.to_csv(os.path.join(OUT, "similarity_ranked.csv"))
    plan.to_csv(os.path.join(OUT, "trade_plans.csv"), index=False)

    # 5%-band peers that are actually swinging (the closest structural analogues)
    band5 = df[(df.band == "5") & (df.tv_cr >= MIN_TV_CR) & (df.index != a.ref)]
    band5 = band5.sort_values(["big_60", "uc"], ascending=False).head(15)

    r = ref["Close"].pct_change() * 100
    last30 = pd.DataFrame({
        "date": ref.index[-30:].strftime("%Y-%m-%d"),
        "close": ref["Close"].iloc[-30:].round(2).values,
        "chg_%": r.iloc[-30:].round(2).values,
        "volume_lakh": (ref["Volume"].iloc[-30:] / 1e5).round(1).values,
    })
    rp, rl = df.loc[a.ref], levels(ref)

    md = [f"# {a.ref} swing-pattern analysis and look-alike scan",
          f"_Data: Yahoo Finance daily, 1y, as of {ref.index[-1]:%Y-%m-%d} (last bar may be intraday). "
          f"Universe {len(px)} NSE stocks; liquid (median traded value >= Rs {MIN_TV_CR:.0f} Cr/day): {len(liq)}._",
          "", f"## 1. {a.ref} profile (last {WIN} sessions)",
          f"- NSE series **{rp.series}**, price band **{rp.band}%**, surveillance remark: {rp.remarks}",
          f"- Last close **{rl['last']:.2f}**, RSI14 **{rl['rsi']:.1f}**, 20d range {rl['lo20']:.2f} - {rl['hi20']:.2f} "
          f"(position {rl['pos20']:.0f}%), 52w {rl['lo52']:.2f} - {rl['hi52']:.2f}",
          f"- SMA20 {rl['sma20']:.2f} | SMA50 {rl['sma50']:.2f} | SMA200 {rl['sma200']:.2f}",
          f"- Daily volatility: 20d **{rp.vol20:.2f}%**, {WIN}d {rp.vol120:.2f}%, ATR14 {rp.atr:.2f}%",
          f"- Days >= +{BIG}%: **{rp.big_up:.1f}%** of sessions; days <= -{BIG}%: **{rp.big_dn:.1f}%**; "
          f"big days in last 60: **{rp.big_60}**",
          f"- Upper-circuit closes: **{rp.uc}**, lower-circuit closes: **{rp.lc}**",
          f"- Flip rate (big move reversed by an opposite big move within 3 days): **{rp.flip * 100:.0f}%**; "
          f"lag-1 autocorrelation {rp.ac1:+.2f}",
          f"- 60d high/low range {rp.range60:.1f}%, 3M return {rp.ret_3m:+.1f}%",
          "", "### Last 30 sessions", last30.to_markdown(index=False),
          "", "## 2. Most similar stocks (swing fingerprint)",
          "Features: 20d/120d volatility, frequency of +/-5% days, flip rate, ATR, 60d range, autocorrelation. "
          "`corr` = daily-return correlation with the reference (sector co-movement).", "",
          fmt(top.reset_index(), ["sym", "industry", "band", "series", "similarity", "close", "tv_cr", "vol20",
                                  "big_up", "big_dn", "big_60", "uc", "lc", "flip", "atr", "corr", "ret_3m"]),
          "", "## 3. Other liquid 5%-band stocks swinging the most (structural peers)", "",
          fmt(band5.reset_index(), ["sym", "industry", "series", "remarks", "close", "tv_cr", "big_60", "uc", "lc",
                                    "flip", "vol20", "ret_3m"]),
          "", "## 4. Backtest + current trade setup",
          f"Rules on 1y data, entry next-day open, +5% target / -5% stop / 7-day max hold, {COST}% cost per trade. "
          "**dip** = buy after a <= -4.5% day (or -8% in 2 days). **mom** = buy after a >= +4.5% day.", "",
          fmt(plan, ["sym", "last", "rsi", "pos20", "lo20", "hi20", "dip_n", "dip_win", "dip_avg",
                     "mom_n", "mom_win", "mom_avg", "entry", "stop", "target", "verdict"]),
          "", "_Not investment advice. Backtests are small-sample and in-sample; circuit-locked days may not "
              "be fillable at the modelled price._"]
    path = os.path.join(OUT, f"{a.ref}_report.md")
    with open(path, "w") as f:
        f.write("\n".join(md))
    print("\n".join(md))
    print("\nwrote", path)


if __name__ == "__main__":
    main()
