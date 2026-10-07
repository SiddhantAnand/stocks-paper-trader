"""Plain-language report + shared HTML styling for the daily report, email and dashboard website."""
import datetime as dt

import markdown
import pandas as pd

REASONS = {
    "target": "Hit the profit target",
    "gap_target": "Opened above the profit target - sold at the open",
    "stop": "Hit the stop-loss (limits the loss)",
    "gap_stop": "Opened below the stop-loss - sold at the open",
    "time": "Holding period ended - sold at about 3:15 pm",
    "void": "Cancelled - excluded from results",
}

BOOK_INFO = {
    "main": "The real strategy: the model's top picks.",
    "lookalike": "Experiment: buys the most similar-looking stock to each main pick, to test whether 'similar stocks' "
                 "also work.",
    "shadow": "Experiment: same model with different settings proposed in a weekly review; adopted only if it beats main.",
}

FACTORS = [
    ("Today's move", "How much the stock rose or fell today (only stocks moving 3% or more are considered)."),
    ("Opening gap", "Did it open much higher or lower than yesterday's close?"),
    ("Close position in the day's range", "Closing near the day's high shows buyers in control; near the low shows sellers."),
    ("Recent momentum", "Price change over the last 2, 5 and 20 trading days."),
    ("Distance from 20-day and 50-day averages", "How stretched the price is above or below its usual level."),
    ("Trend", "Is the short-term average above the longer-term average (uptrend)?"),
    ("RSI (strength index, 0-100)", "Above 70 = overheated, below 30 = oversold."),
    ("Volatility (ATR)", "How much the stock normally moves in a day."),
    ("Volume surge", "Today's trading volume compared with its 20-day average."),
    ("Position in 20-day range", "0 = at the 20-day low, 1 = at the 20-day high."),
    ("Distance from 52-week high", "How far below its one-year peak the stock is."),
    ("Liquidity", "Average daily traded value - only stocks trading at least Rs 5 crore a day are used."),
    ("Price band and T2T status", "NSE's daily limit (2/5/10/20%) and whether delivery-only (T2T) rules apply."),
    ("Up/down streak", "How many days in a row the stock has moved in the same direction."),
    ("Market mood", "Nifty 50's move today and its distance from its 50-day average."),
    ("Fear index (India VIX)", "Market fear level and how fast it changed over 5 days."),
    ("Day of the week", "Some weekdays behave differently."),
]

GLOSSARY = [
    ("Paper trade", "A practice trade with virtual money - no real money is used."),
    ("Model score", "The model's estimate of the next-day return in %, after costs. Higher is better."),
    ("The bar (threshold)", "The minimum model score needed to buy. Raised automatically after a losing streak."),
    ("Profit target / stop-loss", "Automatic sell levels: take profit at +target%, cut the loss at -stop%."),
    ("Win rate", "Share of completed trades that made money."),
    ("Profit factor", "Total gains divided by total losses. Above 1 = profitable; 1.5+ is good."),
    ("Similar past setups", "The 30 most similar situations in history. If they lost money on average, we buy half size."),
]

CSS = """
body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1f2937;background:#f5f7fb;margin:0}
.wrap{max-width:880px;margin:0 auto;padding:20px}
.card{background:#fff;border-radius:12px;padding:18px 22px;margin:14px 0;box-shadow:0 1px 3px rgba(0,0,0,.08);
overflow-x:auto}
h1{font-size:24px;margin:6px 0 2px;color:#0f172a} h2{font-size:18px;margin:22px 0 8px;color:#0f172a;
border-bottom:2px solid #e5e7eb;padding-bottom:4px} h3{font-size:15px;margin:14px 0 6px;color:#334155}
blockquote{margin:8px 0;padding:8px 14px;background:#eef2ff;border-left:4px solid #6366f1;color:#3730a3;border-radius:6px}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:14px}
th{background:#f1f5f9;text-align:left;font-weight:600;color:#334155}
td,th{border:1px solid #e2e8f0;padding:7px 9px;vertical-align:top} tr:nth-child(even) td{background:#fafbfc}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin:12px 0}
.kpi{flex:1 1 150px;background:#fff;border-radius:12px;padding:14px 16px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.kpi .l{font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:.04em}
.kpi .v{font-size:22px;font-weight:700;margin-top:4px}
.up{color:#047857}.down{color:#b91c1c}.muted{color:#64748b;font-size:13px}
a{color:#4f46e5} nav a{margin-right:14px} em{color:#64748b}
"""


def inr(x, sign=False):
    x = round(float(x))
    s = "-" if x < 0 else ("+" if sign and x > 0 else "")
    t = str(int(round(abs(x))))
    if len(t) > 3:
        head, tail = t[:-3], t[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        t = ",".join(([head] if head else []) + parts) + "," + tail
    return f"{s}Rs {t}"


def pct(x):
    if x is None or pd.isna(x):
        return "-"
    x = round(float(x), 2)
    return f"{'▲' if x > 0 else '▼' if x < 0 else ''} {x:+.2f}%".strip()


def why_bought(p, thr):
    f = p["feat"]
    close = "near the day's high" if f["clv"] >= 0.8 else "near the day's low" if f["clv"] <= 0.2 else "mid-range"
    bits = [f"moved {f['r1']:+.1f}% today and closed {close}",
            f"volume {f['vr']:.1f}x normal",
            "uptrend" if f["trend"] else "downtrend",
            f"RSI {f['rsi']:.0f}",
            f"model score {p['pred']:+.2f} (bar {thr})"]
    if p.get("analog_avg") is not None:
        bits.append(f"similar past setups averaged {p['analog_avg']:+.2f}%")
    if p.get("size_mult", 1) < 1:
        bits.append("bought at reduced size")
    if p.get("note"):
        bits.append(p["note"])
    return "; ".join(bits)


def daily_md(st, cfg, trades, equity_df, last, ctx, start_capital, cost):
    """ctx: day, nifty_close, nifty_chg, vix, universe, movers, above_bar, top (DataFrame), train_rows, acc"""
    day = ctx["day"]
    d = dt.datetime.strptime(day, "%Y-%m-%d")
    thr = st.get("thr", cfg.get("thr"))
    main = st["books"]["main"]
    pos_val = sum(p["qty"] * last.get(p["sym"], p["entry_px"]) for p in main["positions"])
    eq_now = main["cash"] + pos_val
    e_main = equity_df[equity_df.book == "main"] if len(equity_df) else equity_df
    prev = float(e_main.equity.iloc[-2]) if len(e_main) >= 2 else start_capital
    tr = trades[trades.reason != "void"] if len(trades) else trades
    tm = tr[tr.book == "main"] if len(tr) else tr
    sold = tr[tr.exit_date == day] if len(tr) else tr
    bought = [(b, p) for b in st["books"] for p in st["books"][b]["positions"] if p["entry_date"] == day]
    bought_main = [p for b, p in bought if b == "main"]
    wins = int((tm.ret_net > 0).sum()) if len(tm) else 0
    losses = len(tm) - wins
    pf = (tm[tm.ret_net > 0].ret_net.sum() / -tm[tm.ret_net <= 0].ret_net.sum()
          if len(tm) and (tm.ret_net <= 0).any() and tm[tm.ret_net <= 0].ret_net.sum() < 0 else None)
    r = cfg.get("research", {})

    if bought_main or (len(sold) and (sold.book == "main").any()):
        s_main = sold[sold.book == "main"] if len(sold) else sold
        one = (f"**Bought {len(bought_main)} stock(s), sold {len(s_main)}"
               + (f" for {inr(s_main.pnl.sum(), True)}" if len(s_main) else "") + ".**")
    elif ctx.get("movers"):
        one = (f"**No new trades today.** {ctx['movers']} stocks moved 3% or more, and "
               f"{ctx.get('above_bar', 0)} scored above the model's bar of {thr}"
               + (" but there was no free slot." if ctx.get("above_bar") else "."))
    else:
        one = "**No trades today.** No stock passed the filters."

    md = [f"# Daily paper-trading report - {d:%a, %d %b %Y}",
          f"> Practice trading with {inr(start_capital)} of virtual money. No real money is used. "
          f"Run: {st['start']} to {st['end']}.", "",
          "## Today in one line", one, ""]
    notes = [i["what"] for i in st.get("incidents", []) if i.get("date") == day]
    if notes:
        md += ["> **Notice:** " + " ".join(notes), ""]
    md += ["## Scoreboard (main strategy)",
          "| Measure | Value |", "|---|---|",
          f"| Portfolio value | **{inr(eq_now)}** |",
          f"| Today's change | {inr(eq_now - prev, True)} ({pct((eq_now / prev - 1) * 100)}) |",
          f"| Total profit / loss since {st['start']} | **{inr(eq_now - start_capital, True)}** "
          f"({pct((eq_now / start_capital - 1) * 100)}) |",
          f"| Trades completed | {len(tm)} ({wins} wins, {losses} losses) |",
          f"| Win rate | {f'{wins / len(tm) * 100:.0f}%' if len(tm) else '-'} "
          f"(expected about {r.get('win', '-')}%) |",
          f"| Average result per trade | {pct(tm.ret_net.mean()) if len(tm) else '-'} "
          f"(expected about {pct(r.get('avg_net'))}) |",
          f"| Profit factor | {f'{pf:.2f}' if pf else '-'} (expected about {r.get('pf', '-')}) |",
          f"| Stocks held now | {len(main['positions'])} of {cfg.get('slots', 3)} slots |",
          f"| Cash available | {inr(main['cash'])} |",
          f"| Evidence so far | {len(tm)} of ~80 trades needed for a reliable verdict |", ""]

    md += ["## What happened today"]
    if len(sold):
        md += ["### Sold", "| Book | Stock | Bought at | Sold at | Result | Profit / loss | Why it was sold |",
               "|---|---|---|---|---|---|---|"]
        for _, t in sold.iterrows():
            md.append(f"| {t.book} | **{t.sym}** | {t.entry_px:,.2f} | {t.exit_px:,.2f} | {pct(t.ret_net)} | "
                      f"{inr(t.pnl, True)} | {REASONS.get(t.reason, t.reason)} |")
        md.append("")
    if bought:
        md += ["### Bought", "| Book | Stock | Price | Amount | Why |", "|---|---|---|---|---|"]
        for b, p in bought:
            md.append(f"| {b} | **{p['sym']}** | {p['entry_px']:,.2f} | {inr(p['qty'] * p['entry_px'])} | "
                      f"{why_bought(p, thr)} |")
        md.append("")
    if not len(sold) and not bought:
        md += ["Nothing was bought or sold today.", ""]

    holding = [(b, p) for b in st["books"] for p in st["books"][b]["positions"]]
    if holding:
        md += ["## Stocks we're holding",
               "| Book | Stock | Bought on | Buy price | Latest | Change | Sell if it reaches | Sell if it falls to |",
               "|---|---|---|---|---|---|---|---|"]
        for b, p in holding:
            lp = last.get(p["sym"], p["entry_px"])
            md.append(f"| {b} | **{p['sym']}** | {p['entry_date']} | {p['entry_px']:,.2f} | {lp:,.2f} | "
                      f"{pct((lp / p['entry_px'] - 1) * 100)} | {p['target']:,.2f} (profit target) | "
                      f"{p['stop']:,.2f} (stop-loss) |")
        md += ["", "_Anything not sold by target or stop-loss is sold at about 3:15 pm on the next trading day "
                   "(2 days for T2T stocks)._", ""]

    vix = ctx.get("vix")
    mood = "calm" if vix and vix < 15 else "nervous" if vix and vix < 20 else "fearful" if vix else "-"
    md += ["## Today's market check", "| Measure | Value |", "|---|---|",
           f"| Nifty 50 | {ctx.get('nifty_close', 0):,.0f} ({pct(ctx.get('nifty_chg'))}) |",
           f"| Market fear (India VIX) | {vix:.1f} - {mood} (below 15 calm, 15-20 nervous, above 20 fearful) |"
           if vix else "| Market fear (India VIX) | - |",
           f"| Stocks scanned | {ctx.get('universe', '-'):,} |" if ctx.get("universe") else "| Stocks scanned | - |",
           f"| Moved 3% or more today | {ctx.get('movers', 0)} |",
           f"| Scored above the bar ({thr}) | {ctx.get('above_bar', 0)} |", ""]

    top = ctx.get("top")
    if top is not None and len(top):
        md += ["## Top candidates the model looked at", "| Stock | Today's move | Model score | Decision |",
               "|---|---|---|---|"]
        for _, c in top.iterrows():
            md.append(f"| {c.sym} | {pct(c.r1)} | {c.pred:+.2f} | {c.decision} |")
        md.append("")

    acc = ctx.get("acc") or {}
    md += ["## How the model is learning",
           f"- Retrained tonight on **{ctx.get('train_rows', 0):,}** past setups, including every setup that "
           f"finished today. Recent data counts more.",
           f"- The bar to buy is **{thr}** and position size is **{st.get('risk_mult', 1.0) * 100:.0f}%**. "
           f"Both tighten automatically after a losing streak and relax after a winning one."]
    if acc.get("labelled"):
        md.append(f"- Prediction check: of {acc['labelled']} past predictions, stocks above the bar averaged "
                  f"{pct(acc.get('above_thr_avg'))} next day vs {pct(acc.get('below_thr_avg'))} for the rest.")
    md.append("")

    if len(st["books"]) > 1:
        md += ["## Experiments running alongside", "| Book | Value | Total profit / loss | Trades | What it tests |",
               "|---|---|---|---|---|"]
        for b, bk in st["books"].items():
            if b == "main":
                continue
            e = bk["cash"] + sum(p["qty"] * last.get(p["sym"], p["entry_px"]) for p in bk["positions"])
            n = int((tr.book == b).sum()) if len(tr) else 0
            md.append(f"| {b} | {inr(e)} | {inr(e - start_capital, True)} | {n} | {BOOK_INFO.get(b, '')} |")
        md.append("")

    md += ["## How this works",
           f"1. **3:15 pm every trading day:** the system scans about 1,100 NSE stocks and keeps those that moved "
           f"3% or more today and trade at least Rs 5 crore a day.",
           f"2. **Scoring:** a machine-learning model, trained on about 2 years of similar situations, gives each "
           f"stock a score = expected next-day return after costs.",
           f"3. **Buying:** up to {cfg.get('slots', 3)} stocks scoring above the bar are bought (about "
           f"{inr(start_capital / cfg.get('slots', 3))} each). Half size if similar past setups lost money.",
           f"4. **Selling (next trading day):** at **+{cfg.get('tp')}%** profit target, **-{cfg.get('sl')}%** "
           f"stop-loss, or at about 3:15 pm - whichever comes first. T2T stocks are held 2 days.",
           f"5. **Every evening:** prices are updated, the model retrains, yesterday's predictions are checked, "
           f"and this report is sent.",
           f"6. **Costs:** {cost}% per round trip (taxes, charges, slippage) is deducted from every trade.", "",
           "### What the model looks at", "| Factor | In plain words |", "|---|---|"]
    md += [f"| {a} | {b} |" for a, b in FACTORS]
    md += ["", "_Also recorded for every buy (not used for picking): P/E ratio, price-to-book, market value, "
               "debt-to-equity and return on equity._", "",
           "### Words used in this report", "| Term | Meaning |", "|---|---|"]
    md += [f"| {a} | {b} |" for a, b in GLOSSARY]
    md += ["", f"_Settings version {cfg.get('version', 1)}. Paper trades only - not investment advice. "
               f"Prices assume the ~3:15 pm level; real fills can differ._"]
    return "\n".join(md)


def to_html(md_text):
    return markdown.markdown(md_text, extensions=["tables"])


def page(title, body, nav="", extra_head=""):
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' "
            f"content='width=device-width,initial-scale=1'><meta name='robots' content='noindex,nofollow'>"
            f"<title>{title}</title><style>{CSS}</style>{extra_head}</head><body><div class='wrap'>"
            f"{nav}{body}</div></body></html>")


def email_html(md_text, link, site_url=None):
    links = f"<a href='{link}'>View on GitHub</a>" + (f" &nbsp;|&nbsp; <a href='{site_url}'>Open dashboard</a>"
                                                       if site_url else "")
    return page("Paper trading report", f"<p class='muted'>{links}</p><div class='card'>{to_html(md_text)}</div>")
