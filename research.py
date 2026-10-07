"""Walk-forward research: does the learning model beat simple rules out-of-sample? Saves the live model + config.

Usage: .venv/bin/python research.py [--download]
"""
import argparse
import json
import os

import numpy as np
import pandas as pd

from model import DATA, FEATS, POLICIES, build_events, fit, load_history, load_meta, save_model, update_history

EVENTS = os.path.join(DATA, "events.pkl")


def walk_forward(ev, target, min_train_days=120):
    ev = ev.dropna(subset=[target]).sort_values("date")
    out = []
    for m in ev.date.dt.to_period("M").unique():
        test = ev[ev.date.dt.to_period("M") == m]
        train = ev[ev.date < test.date.min() - pd.Timedelta(days=7)]  # embargo: labels look up to ~6 days ahead
        if train.date.nunique() < min_train_days:
            continue
        t = test.copy()
        t["pred"] = fit(train, target).predict(t[FEATS])
        out.append(t)
    return pd.concat(out) if out else pd.DataFrame()


def simulate(cands, cal, y, hd, slots=3):
    """Rs 1L, up to `slots` positions; each entry gets equity/slots; capital locked until the label's exit bar."""
    idx = {d: i for i, d in enumerate(cal)}
    cash, open_, trades, curve = 1e5, [], [], []
    by_day = {d: g for d, g in cands.groupby("date")}
    for i, d in enumerate(cal):
        for p in [p for p in open_ if p["exit_i"] <= i]:
            cash += p["amt"] * (1 + p["ret"] / 100)
            trades.append(p["ret"])
            open_.remove(p)
        eq = cash + sum(p["amt"] for p in open_)
        g = by_day.get(d)
        if g is not None:
            for _, r in g.sort_values("score", ascending=False).iterrows():
                if len(open_) >= slots or cash < 1000:
                    break
                amt = min(cash, eq / slots)
                cash -= amt
                open_.append(dict(amt=amt, ret=r[y], exit_i=i + int(r[hd])))
        curve.append(cash + sum(p["amt"] for p in open_))
    c, t = pd.Series(curve, index=cal), pd.Series(trades, dtype=float)
    w = pd.Series([(c.iloc[k + 40] / c.iloc[k] - 1) * 100 for k in range(len(c) - 40)]) if len(c) > 45 else pd.Series([np.nan])
    pf = t[t > 0].sum() / -t[t < 0].sum() if (t < 0).any() else np.nan
    return dict(trades=len(t), per_wk=round(len(t) / (len(cal) / 5), 1), win=round((t > 0).mean() * 100, 1),
                avg=round(t.mean(), 2), pf=round(pf, 2), total=round((c.iloc[-1] / 1e5 - 1) * 100, 1),
                wk8_med=round(w.median(), 1), wk8_worst=round(w.min(), 1), wk8_best=round(w.max(), 1),
                wk8_pos=round((w > 0).mean() * 100), maxdd=round(((c / c.cummax()) - 1).min() * 100, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()
    syms, band, series, _ = load_meta()
    hist = update_history(syms) if a.download else load_history()
    if a.download or a.rebuild or not os.path.exists(EVENTS):
        ev = build_events(hist, syms, band, series)
        ev.to_pickle(EVENTS)
    ev = pd.read_pickle(EVENTS)
    print(f"stocks {len([s for s in syms if s in hist])}, events {len(ev)}, "
          f"{ev.date.min():%Y-%m-%d} .. {ev.date.max():%Y-%m-%d}, up {int((ev.r1 > 0).sum())} / down {int((ev.r1 < 0).sum())}")

    cal_all = list(hist["^NSEI"].index)
    rows, best = [], None
    for name in POLICIES:
        y, hd = "y_" + name, "hd_" + name
        oos = walk_forward(ev, y)
        cal = [d for d in cal_all if oos.date.min() <= d <= oos.date.max()]
        base = oos.copy()
        print(f"\n== {name} {POLICIES[name]}  OOS {oos.date.min():%Y-%m-%d}..{oos.date.max():%Y-%m-%d}  "
              f"events {len(oos)}  avg all {oos[y].mean():+.2f}%  up-days {oos[oos.r1 > 0][y].mean():+.2f}%  "
              f"down-days {oos[oos.r1 < 0][y].mean():+.2f}%  corr(pred,y) {oos.pred.corr(oos[y]):.3f}")
        q = pd.qcut(oos.pred, 5, labels=False, duplicates="drop")
        print("   avg return by prediction quintile (0=worst):", oos.groupby(q)[y].mean().round(2).to_dict())
        variants = {
            "rule_momentum": base[(base.r1 >= 4.5) & (base.clv >= 0.9) & (base.trend == 1) & (base.d_sma20 > 0)
                                  & (base.rsi < 78) & (base.vr >= 1.5)].assign(score=lambda x: x.r1),
            "rule_dip": base[(base.r1 <= -4.5)].assign(score=lambda x: -x.r1),
        }
        for thr in (0.0, 0.3, 0.6, 1.0):
            variants[f"model>{thr}"] = base[base.pred > thr].assign(score=lambda x: x.pred)
        for k, cands in variants.items():
            r = dict(policy=name, select=k, **simulate(cands, cal, y, hd))
            rows.append(r)
            if k.startswith("model") and r["trades"] >= 150 and (best is None or r["pf"] > best["pf"]):
                best = r | {"thr": float(k.split(">")[1])}
    res = pd.DataFrame(rows)
    print("\n", res.to_string(index=False))
    res.to_csv(os.path.join("reports", "research_results.csv"), index=False)

    if best:
        name = best["policy"]
        y = "y_" + name
        model = fit(ev, y)
        save_model(model, ev)
        H, tp, sl = POLICIES[name]
        old = json.load(open(os.path.join(DATA, "model_config.json"))) if os.path.exists(
            os.path.join(DATA, "model_config.json")) else {}
        cfg = dict(policy=name, hold=H, tp=tp, sl=sl, thr=best["thr"], slots=3, trained_on=len(ev.dropna(subset=[y])),
                   trained_to=f"{ev.date.max():%Y-%m-%d}", research=best, version=old.get("version", 0) + 1,
                   changelog=old.get("changelog", []) + [{"version": old.get("version", 0) + 1,
                                                          "date": f"{pd.Timestamp.now():%Y-%m-%d}",
                                                          "change": f"research.py selected {name} thr {best['thr']}",
                                                          "evidence": str(best)}])
        with open(os.path.join(DATA, "model_config.json"), "w") as f:
            json.dump(cfg, f, indent=1, default=str)
        print("\nselected:", json.dumps(cfg, default=str))


if __name__ == "__main__":
    main()
