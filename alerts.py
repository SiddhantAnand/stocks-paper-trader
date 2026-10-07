"""Dip alerts for the swing watchlist: macOS notification when a stock has its 5% down day or enters its buy zone.

Watchlist + levels come from reports/trade_plans.csv (written by analyze.py); "Avoid" names are skipped.
Usage: .venv/bin/python alerts.py [--force] [--test]
"""
import argparse
import datetime as dt
import json
import os
import subprocess
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

ROOT = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.join(ROOT, "reports", "trade_plans.csv")
STATE = os.path.join(ROOT, "data", "alert_state.json")
LOG = os.path.join(ROOT, "data", "alerts.log")
IST = ZoneInfo("Asia/Kolkata")
DAY_DIP = -4.5
TWO_DAY_DIP = -8.0


def notify(title, msg):
    # argv keeps symbol/price text out of the AppleScript source
    subprocess.run(["osascript", "-e", "on run argv", "-e",
                    'display notification (item 1 of argv) with title (item 2 of argv) sound name "Glass"',
                    "-e", "end run", msg, title], check=False)


def log(line):
    stamp = dt.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a") as f:
        f.write(f"{stamp} {line}\n")
    print(stamp, line)


def market_open(now):
    return now.weekday() < 5 and dt.time(9, 15) <= now.time() <= dt.time(15, 35)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="run outside market hours")
    ap.add_argument("--test", action="store_true", help="send a sample notification and exit")
    a = ap.parse_args()

    if a.test:
        notify("Dip alert test", "STLTECH -5.0% at 955.00 | buy zone <= 955, stop 760, target 1051")
        return
    now = dt.datetime.now(IST)
    if not (a.force or market_open(now)):
        return

    plans = pd.read_csv(PLANS)
    plans = plans[~plans.verdict.str.startswith("Avoid")].set_index("sym")
    px = yf.download([s + ".NS" for s in plans.index], period="7d", interval="1d",
                     group_by="ticker", auto_adjust=False, progress=False, threads=True)

    today = now.date().isoformat()
    state = {}
    if os.path.exists(STATE):
        with open(STATE) as f:
            state = json.load(f)
    fired = state.get(today, {})

    for sym, p in plans.iterrows():
        d = px[sym + ".NS"]["Close"].dropna()
        if len(d) < 3:
            continue
        if not a.force and d.index[-1].date() != now.date():
            continue  # no bar for today yet (holiday / pre-open)
        last = d.iloc[-1]
        chg1 = (last / d.iloc[-2] - 1) * 100
        chg2 = (last / d.iloc[-3] - 1) * 100

        hits = []
        if chg1 <= DAY_DIP:
            hits.append(("day", f"{chg1:+.1f}% today"))
        if chg2 <= TWO_DAY_DIP:
            hits.append(("2day", f"{chg2:+.1f}% in 2 days"))
        if last <= p.entry:
            hits.append(("zone", "in buy zone"))
        new = [h for h in hits if h[0] not in fired.get(sym, [])]
        if not new:
            continue

        warn = " | BELOW STOP - don't catch it" if last <= p.stop else ""
        msg = (f"{sym} {last:.2f} ({', '.join(h[1] for h in hits)}) | "
               f"buy <= {p.entry:.0f}, stop {p.stop:.0f}, target {p.target:.0f}{warn}")
        notify(f"Dip alert: {sym}", msg)
        log(msg)
        fired[sym] = fired.get(sym, []) + [h[0] for h in new]

    with open(STATE, "w") as f:
        json.dump({today: fired}, f)


if __name__ == "__main__":
    main()
