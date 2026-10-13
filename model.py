"""Shared data, feature and label engine for research.py and papertrade.py (same code path = no train/live skew)."""
import io
import os
import pickle
import time

import numpy as np
import pandas as pd
import requests
import yfinance as yf

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("STOCKS_DATA", os.path.join(ROOT, "data"))
os.makedirs(os.path.join(ROOT, ".cache", "yfinance"), exist_ok=True)
yf.set_tz_cache_location(os.path.join(ROOT, ".cache", "yfinance"))  # default cache failed under launchd (sqlite)
HIST = os.path.join(DATA, "hist.pkl")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}

# Delivery round trip on ~Rs 33k orders: STT 0.1%x2, stamp 0.015%, exch+SEBI+GST ~0.01%, DP ~Rs16 (~0.05%),
# plus ~0.07% slippage on small/mid caps.
COST = 0.35
MIN_MOVE = 3.0       # candidate events: |day change| >= 3%
MIN_TV_CR = 5.0      # 20d median traded value, Rs crore
MIN_PRICE = 20.0

FEATS = ["r1", "gap", "oc", "clv", "r2", "r5", "r20", "d_sma20", "d_sma50", "trend", "rsi", "atr", "vr",
         "pos20", "d_hi52", "tv_log", "band", "is_be", "streak", "n_r1", "n_d50", "vix", "vix_ch5", "dow"]

# (max hold days, target %, stop %); research picks one, live uses data/model_config.json
POLICIES = {
    "h1": (1, 4.0, 3.0),
    "h2": (2, 5.0, 4.0),
    "h3": (3, 6.0, 4.0),
}


def load_meta():
    sec = pd.read_csv(os.path.join(DATA, "sec_list.csv"), dtype=str)
    sec = sec.drop_duplicates("Symbol").set_index("Symbol")
    band = pd.to_numeric(sec["Band"].str.strip(), errors="coerce").fillna(20.0)  # "No Band" (F&O) ~ wide
    tm = pd.read_csv(os.path.join(DATA, "ind_niftytotalmarket_list.csv"), dtype=str)
    b5 = sec[(band == 5) & sec.Series.isin(["EQ", "BE"])].index
    gsm = sec[sec["Remarks"].fillna("").str.contains("GSM|ASM")].index
    syms = sorted((set(tm.Symbol) | set(b5)) - set(gsm))
    return syms, band, sec["Series"], tm.set_index("Symbol")["Industry"]


def refresh_reference_files():
    import requests
    for name, url in [("sec_list.csv", "https://archives.nseindia.com/content/equities/sec_list.csv"),
                      ("ind_niftytotalmarket_list.csv",
                       "https://archives.nseindia.com/content/indices/ind_niftytotalmarket_list.csv")]:
        try:
            r = requests.get(url, headers=UA, timeout=20)
            if r.ok and len(r.content) > 10000:
                with open(os.path.join(DATA, name), "wb") as f:
                    f.write(r.content)
        except Exception as e:
            print("reference refresh failed", name, e)


def _download(tickers, period, interval="1d"):
    out = {}
    for i in range(0, len(tickers), 100):
        chunk = tickers[i:i + 100]
        for attempt in range(3):
            try:
                df = yf.download(chunk, period=period, interval=interval, group_by="ticker",
                                 auto_adjust=False, progress=False, threads=True)
                break
            except Exception as e:
                print("download retry", e)
                time.sleep(5 * (attempt + 1))
        else:
            continue
        for t in chunk:
            if t in df.columns.get_level_values(0):
                d = df[t].dropna(how="all")
                if "Volume" in d:
                    d = d[(d["Volume"] > 0) | t.startswith("^")]
                if len(d):
                    out[t] = d[["Open", "High", "Low", "Close", "Volume"]].copy()
    return out


def fill_gaps(hist, syms, lookback=25):
    """Yahoo sometimes drops a whole session for most stocks (e.g. 12 Oct 2026). Features skip any stock with a
    missing session, so fill recent gaps from NSE's official bhavcopy (unadjusted, same as our Yahoo bars)."""
    have = [s for s in syms if s in hist]
    for t in hist["^NSEI"].index[-lookback:]:
        missing = [s for s in have if t not in hist[s].index]
        if len(missing) < 0.2 * len(have):
            continue
        url = f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{t:%d%m%Y}.csv"
        try:
            r = requests.get(url, headers=UA, timeout=30)
            r.raise_for_status()
            b = pd.read_csv(io.StringIO(r.text), skipinitialspace=True)
        except Exception as e:
            print(f"bhavcopy fill failed for {t.date()}: {e}")
            continue
        b.columns = b.columns.str.strip()
        b = b[b.SERIES.str.strip().isin(["EQ", "BE"])].drop_duplicates("SYMBOL").set_index("SYMBOL")
        n = 0
        for s in missing:
            if s in b.index:
                x = b.loc[s]
                row = pd.DataFrame({"Open": [x.OPEN_PRICE], "High": [x.HIGH_PRICE], "Low": [x.LOW_PRICE],
                                    "Close": [x.CLOSE_PRICE], "Volume": [x.TTL_TRD_QNTY]},
                                   index=pd.DatetimeIndex([t], name=hist[s].index.name), dtype=float)
                hist[s] = pd.concat([hist[s], row]).sort_index()
                n += 1
        print(f"filled {n} of {len(missing)} missing bars for {t.date()} from NSE bhavcopy")
    return hist


def update_history(syms, period="2y"):
    tick = [s + ".NS" for s in syms] + ["^NSEI", "^INDIAVIX"]
    raw = _download(tick, period)
    hist = fill_gaps({k[:-3] if k.endswith(".NS") else k: v for k, v in raw.items()}, syms)
    with open(HIST, "wb") as f:
        pickle.dump(hist, f)
    return hist


def load_history():
    with open(HIST, "rb") as f:
        return pickle.load(f)


def market_frame(hist):
    n = hist["^NSEI"]["Close"]
    v = hist["^INDIAVIX"]["Close"].reindex(n.index).ffill()
    return pd.DataFrame({
        "n_r1": n.pct_change() * 100,
        "n_d50": (n / n.rolling(50).mean() - 1) * 100,
        "vix": v,
        "vix_ch5": (v / v.shift(5) - 1) * 100,
    })


def _rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def stock_features(d, band, series, mkt, cal_prev):
    c, o, h, l, v = d["Close"], d["Open"], d["High"], d["Low"], d["Volume"]
    pc = c.shift()
    r1 = (c / pc - 1) * 100
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    sma20, sma50 = c.rolling(20).mean(), c.rolling(50).mean()
    sign = np.sign(r1)
    streak = sign.groupby((sign != sign.shift()).cumsum()).cumcount() + 1
    f = pd.DataFrame({
        "r1": r1,
        "gap": (o / pc - 1) * 100,
        "oc": (c / o - 1) * 100,
        "clv": ((c - l) / (h - l).replace(0, np.nan)).fillna(0.5),
        "r2": (c / c.shift(2) - 1) * 100,
        "r5": (c / c.shift(5) - 1) * 100,
        "r20": (c / c.shift(20) - 1) * 100,
        "d_sma20": (c / sma20 - 1) * 100,
        "d_sma50": (c / sma50 - 1) * 100,
        "trend": (sma20 > sma50).astype(float),
        "rsi": _rsi(c),
        "atr": tr.rolling(14).mean() / c * 100,
        "vr": v / v.rolling(20).mean().shift(),
        "pos20": (c - l.rolling(20).min()) / (h.rolling(20).max() - l.rolling(20).min()).replace(0, np.nan),
        "d_hi52": (c / h.rolling(250, min_periods=60).max() - 1) * 100,
        "tv_cr": (c * v).rolling(20).median() / 1e7,
        "band": band,
        "is_be": float(series == "BE"),
        "streak": streak * sign,
        "dow": d.index.dayofweek,
    }, index=d.index)
    f["tv_log"] = np.log10(f["tv_cr"].clip(lower=0.01))
    f = f.join(mkt, how="left")
    prev_bar = pd.Series(d.index, index=d.index).shift()
    f["valid"] = [cal_prev.get(t) == p for t, p in zip(d.index, prev_bar)]  # no missing session in between
    f["uc_locked"] = (c >= pc * (1 + (band - 0.3) / 100)) & (c >= h * 0.999)
    f["close"] = c
    return f


def label(o, h, l, c, i, H, tp, sl, min_hold, band):
    """(net % return, bars held) buying at close of bar i. None if not enough future data."""
    e = c[i]
    stop, tgt = e * (1 - sl / 100), e * (1 + tp / 100)
    for d in range(1, H + 4):
        j = i + d
        if j >= len(c):
            return None
        if (h[j] - l[j] <= c[j] * 0.002) and c[j] <= c[j - 1] * (1 - (band - 0.3) / 100):
            continue  # locked at lower circuit: no buyers, cannot exit
        if d < min_hold:
            continue
        if o[j] <= stop:
            x = o[j]
        elif l[j] <= stop:
            x = stop
        elif o[j] >= tgt:
            x = o[j]
        elif h[j] >= tgt:
            x = tgt
        elif d >= H:
            x = c[j]
        else:
            continue
        return (x / e - 1) * 100 - COST, d
    return None


def build_events(hist, syms, band, series, with_labels=True, only_last=False):
    mkt = market_frame(hist)
    cal = list(hist["^NSEI"].index)
    cal_prev = dict(zip(cal[1:], cal[:-1]))
    rows = []
    for s in syms:
        d = hist.get(s)
        if d is None or len(d) < 60:
            continue
        b, se = float(band.get(s, 20.0)), series.get(s, "EQ")
        f = stock_features(d, b, se, mkt, cal_prev)
        f["sym"] = s
        f["date"] = f.index
        f["pos"] = np.arange(len(f))
        if only_last:
            f = f.iloc[-1:]
        ev = f[(f.r1.abs() >= MIN_MOVE) & f.valid & (f.tv_cr >= MIN_TV_CR) & (f.close >= MIN_PRICE) & ~f.uc_locked]
        if ev.empty:
            continue
        ev = ev.copy()
        if with_labels:
            o, h, l, c = (d[k].to_numpy() for k in ["Open", "High", "Low", "Close"])
            mh = 2 if se == "BE" else 1  # T2T: no BTST, earliest sell is T+2
            for name, (H, tp, sl) in POLICIES.items():
                res = [label(o, h, l, c, int(i), H, tp, sl, mh, b) for i in ev.pos]
                ev["y_" + name] = [r[0] if r else np.nan for r in res]
                ev["hd_" + name] = [r[1] if r else np.nan for r in res]
        rows.append(ev)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def make_model():
    from sklearn.ensemble import HistGradientBoostingRegressor
    return HistGradientBoostingRegressor(max_iter=250, learning_rate=0.04, max_leaf_nodes=15,
                                         min_samples_leaf=200, l2_regularization=1.0, random_state=0)


def fit(df, target):
    d = df.dropna(subset=[target])
    w = np.exp((d.date - d.date.max()).dt.days / 180.0)  # recent data weighted more (half-life ~4 months)
    m = make_model()
    m.fit(d[FEATS], d[target].clip(-10, 10), sample_weight=w)
    return m


CANARY = os.path.join(DATA, "model_canary.json")


def save_model(m, df):
    import joblib
    import json
    joblib.dump(m, os.path.join(DATA, "model.joblib"))
    x = df[FEATS].dropna().tail(5)
    with open(CANARY, "w") as f:
        json.dump({"x": x.to_numpy().tolist(), "y": m.predict(x).tolist()}, f)


def canary_ok(m):
    import json
    if not os.path.exists(CANARY):
        return True
    with open(CANARY) as f:
        c = json.load(f)
    got = m.predict(pd.DataFrame(c["x"], columns=FEATS))
    return bool(np.allclose(got, c["y"], atol=1e-6))
