"""Build the static dashboard website (site/) from paper-trading data. Published to GitHub Pages by the workflow."""
import glob
import html
import json
import os
import shutil

import pandas as pd

import reporting as R

ROOT = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(os.environ.get("STOCKS_DATA", os.path.join(ROOT, "data")), "paper")
REPORTS = os.environ.get("STOCKS_REPORTS", os.path.join(ROOT, "reports", "paper"))
OUT = os.environ.get("STOCKS_SITE", os.path.join(ROOT, "site"))
START = 100000.0
COLORS = {"main": "#4f46e5", "lookalike": "#f59e0b", "shadow": "#10b981"}


def read(name):
    p = os.path.join(PAPER, name)
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


def svg_chart(eq):
    if eq.empty:
        return "<p class='muted'>The chart appears after the first trading day.</p>"
    piv = eq.pivot_table(index="date", columns="book", values="equity").sort_index()
    w, h, pad = 820, 260, 44
    lo, hi = min(piv.min().min(), START), max(piv.max().max(), START)
    span = max(hi - lo, START * 0.01)
    lo, hi = lo - span * 0.1, hi + span * 0.1
    n = len(piv)
    xs = lambda i: pad + (w - 2 * pad) * (i / max(n - 1, 1))
    ys = lambda v: h - pad + (h - 2 * pad) * -((v - lo) / (hi - lo))
    parts = [f"<svg viewBox='0 0 {w} {h}' width='100%' role='img' aria-label='Portfolio value over time'>",
             f"<line x1='{pad}' x2='{w - pad}' y1='{ys(START):.1f}' y2='{ys(START):.1f}' stroke='#94a3b8' "
             f"stroke-dasharray='4 4'/><text x='{w - pad}' y='{ys(START) - 6:.1f}' text-anchor='end' font-size='11' "
             f"fill='#64748b'>Starting value {R.inr(START)}</text>"]
    for v in (lo + (hi - lo) * k / 4 for k in range(5)):
        parts.append(f"<text x='4' y='{ys(v) + 4:.1f}' font-size='10' fill='#94a3b8'>{v / 1000:.1f}k</text>")
    for b in piv.columns:
        s = piv[b].dropna()
        pts = " ".join(f"{xs(piv.index.get_loc(d)):.1f},{ys(v):.1f}" for d, v in s.items())
        c = COLORS.get(b, "#64748b")
        parts.append(f"<polyline fill='none' stroke='{c}' stroke-width='{3 if b == 'main' else 2}' points='{pts}'/>")
        for d, v in s.items():
            parts.append(f"<circle cx='{xs(piv.index.get_loc(d)):.1f}' cy='{ys(v):.1f}' r='3' fill='{c}'>"
                         f"<title>{b} {d}: {R.inr(v)}</title></circle>")
    parts.append(f"<text x='{pad}' y='{h - 10}' font-size='11' fill='#64748b'>{piv.index[0]}</text>"
                 f"<text x='{w - pad}' y='{h - 10}' font-size='11' fill='#64748b' text-anchor='end'>{piv.index[-1]}</text>")
    parts.append("</svg><p class='muted'>" + " &nbsp; ".join(
        f"<span style='color:{COLORS.get(b, '#64748b')}'>&#9632;</span> {b}" for b in piv.columns) + "</p>")
    return "".join(parts)


def kpis(st, eq, tr):
    main = eq[eq.book == "main"].sort_values("date") if len(eq) else eq
    val = float(main.equity.iloc[-1]) if len(main) else START
    prev = float(main.equity.iloc[-2]) if len(main) >= 2 else START
    tm = tr[(tr.book == "main") & (tr.reason != "void")] if len(tr) else tr
    win = f"{(tm.ret_net > 0).mean() * 100:.0f}%" if len(tm) else "-"
    avg = R.pct(tm.ret_net.mean()) if len(tm) else "-"
    cls = lambda x: "up" if x > 0 else "down" if x < 0 else ""
    cards = [("Portfolio value", R.inr(val), ""),
             ("Total profit / loss", f"{R.inr(val - START, True)}", cls(val - START)),
             ("Last day", R.pct((val / prev - 1) * 100), cls(val - prev)),
             ("Trades completed", f"{len(tm)} <span class='muted'>/ ~80 needed</span>", ""),
             ("Win rate", win, ""), ("Average per trade", avg, cls(tm.ret_net.mean()) if len(tm) else "")]
    return "<div class='kpis'>" + "".join(
        f"<div class='kpi'><div class='l'>{l}</div><div class='v {c}'>{v}</div></div>" for l, v, c in cards) + "</div>"


def trade_table(tr):
    t = tr[tr.reason != "void"] if len(tr) else tr
    if t.empty:
        return "<p class='muted'>No completed trades yet.</p>"
    rows = "".join(
        f"<tr><td>{r.exit_date}</td><td>{r.book}</td><td><b>{html.escape(str(r.sym))}</b></td><td>{r.entry_px:,.2f}</td>"
        f"<td>{r.exit_px:,.2f}</td><td class='{'up' if r.ret_net > 0 else 'down'}'>{R.pct(r.ret_net)}</td>"
        f"<td>{R.inr(r.pnl, True)}</td><td>{R.REASONS.get(r.reason, r.reason)}</td></tr>"
        for r in t.sort_values("exit_date", ascending=False).itertuples())
    return ("<table><tr><th>Sold on</th><th>Book</th><th>Stock</th><th>Bought at</th><th>Sold at</th><th>Result</th>"
            f"<th>Profit / loss</th><th>Why sold</th></tr>{rows}</table>")


def nav(prefix=""):
    return (f"<nav class='muted'><a href='{prefix}index.html'>Dashboard</a><a href='{prefix}reports.html'>"
            f"All reports</a><a href='{prefix}how.html'>How it works</a></nav>")


def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "r"))
    st = json.load(open(os.path.join(PAPER, "state.json"))) if os.path.exists(os.path.join(PAPER, "state.json")) else {}
    eq, tr = read("equity.csv"), read("trades.csv")
    latest_md = open(os.path.join(REPORTS, "latest.md")).read() if os.path.exists(os.path.join(REPORTS, "latest.md")) else ""
    upto = latest_md.split("## How this works")[0]
    how = "## How this works" + latest_md.split("## How this works")[1] if "## How this works" in latest_md else ""

    body = (f"<h1>Paper-trading dashboard</h1><p class='muted'>Virtual {R.inr(START)}, no real money. "
            f"Run {st.get('start', '-')} to {st.get('end', '-')}. Updated every trading day after 4 pm IST.</p>"
            f"{kpis(st, eq, tr)}<div class='card'><h2>Portfolio value over time</h2>{svg_chart(eq)}</div>"
            f"<div class='card'>{R.to_html(upto)}</div>"
            f"<div class='card'><h2>All completed trades</h2>{trade_table(tr)}</div>")
    open(os.path.join(OUT, "index.html"), "w").write(R.page("Paper-trading dashboard", body, nav()))
    open(os.path.join(OUT, "how.html"), "w").write(
        R.page("How it works", f"<div class='card'>{R.to_html(how or 'Available after the first report.')}</div>", nav()))

    items = []
    for kind, pattern in (("Weekly", os.path.join(REPORTS, "weekly", "20*.md")), ("Daily", os.path.join(REPORTS, "20*.md"))):
        for p in sorted(glob.glob(pattern), reverse=True):
            name = os.path.basename(p)[:-3]
            out = f"{kind.lower()}-{name}.html"
            open(os.path.join(OUT, "r", out), "w").write(
                R.page(f"{kind} report {name}", f"<div class='card'>{R.to_html(open(p).read())}</div>", nav("../")))
            items.append(f"<li>{kind} - <a href='r/{out}'>{name}</a></li>")
    open(os.path.join(OUT, "reports.html"), "w").write(
        R.page("All reports", f"<div class='card'><h1>All reports</h1><ul>{''.join(items) or '<li>None yet</li>'}</ul></div>",
               nav()))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"site built: {len(items)} report page(s) -> {OUT}")


if __name__ == "__main__":
    build()
