---
description: "Weekly AI review of the paper-trading run: pull results from GitHub, diagnose losses, test any proposed change out-of-sample or as a shadow book, then commit and push only evidence-backed changes."
agent: "agent"
argument-hint: "Optional: week to review, e.g. 2026-W42 (default: latest)"
---
Act as a disciplined quant reviewer for this paper-trading project. Follow these steps in order.

1. **Sync**: run `git pull` in the workspace root. Confirm the latest weekly report exists in [reports/paper/weekly/](../../reports/paper/weekly/) (use `latest.md` unless the user named a week).

2. **Read the evidence**:
   - The weekly report, [data/paper/trades.csv](../../data/paper/trades.csv), [data/paper/equity.csv](../../data/paper/equity.csv), [data/paper/predictions.csv](../../data/paper/predictions.csv), the `learning` list in [data/paper/state.json](../../data/paper/state.json), and [data/paper/log.txt](../../data/paper/log.txt) (look for `FAILED` and late or missed runs).
   - The live settings and changelog in [data/model_config.json](../../data/model_config.json), and [data/shadow_config.json](../../data/shadow_config.json) if it exists.

3. **Diagnose**:
   - Compare live results with the research expectation in the config (avg net per trade, win %, profit factor). Report how many main trades exist vs the ~80 needed for a confident verdict.
   - For each losing trade, look up news or results for that stock around the entry date, and decide whether the loss was predictable or normal variance.
   - Check for data problems: missing bars, odd prices, wrong P/E, and runs that started late.
   - Compare the main, lookalike and shadow books.

4. **Decide** (the rules below are mandatory):
   - With fewer than ~20 main trades since the last change, do **not** change live settings. Only fix bugs and data problems.
   - A change that can be backtested (threshold, target, stop, hold, features, filters on price data) must beat the current settings in `research.py`'s walk-forward test, on profit factor and avg net per trade with at least 150 trades. Run it, show the comparison table, and only then edit `data/model_config.json`: bump `version` and add a `changelog` entry that states the evidence.
   - A change that cannot be backtested honestly (news or event filters, discretionary rules) must first run as a shadow book: write `data/shadow_config.json` (keys: `name`, plus any of `thr`, `tp`, `sl`, `hold`, `slots`) or add code that applies only to the `shadow` book. Promote it to main only after it beats main over at least 20 shadow trades.
   - Never change settings mid-week, connect to a broker, or place real orders.

5. **Verify**: run `.venv/bin/python -m py_compile papertrade.py model.py research.py notify.py`. For code changes, run a sandbox test with `STOCKS_DATA` and `STOCKS_REPORTS` pointing at a temporary copy of `data/`, e.g. `papertrade.py tick --force entry` and `--force eod`.

6. **Report back** with:
   - a short verdict (on track, behind expectation, or broken)
   - the evidence table
   - the losing-trade diagnosis
   - each proposed change with its test result
   - what you changed and what you deliberately left alone

7. **Ship**: show the user the `git diff`. Commit with a message like `weekly review 2026-W42: <change>` and `git push` only after the user confirms. GitHub Actions uses the new settings from the next scheduled run.
