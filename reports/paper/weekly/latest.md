# Weekly paper-trading review - 2026-W41 (week of 2026-10-05)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 1.0 | risk x1.0

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 0 | - | - | - | 0 | - | - | - | 100,000 |
| lookalike | 0 | - | - | - | 0 | - | - | - | 100,000 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 0 main trades of ~80 needed for a confident verdict.

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |
|:-----------|-------------:|------:|------------:|
| 2026-10-07 |        53074 |     1 |           1 |
| 2026-10-08 |        52517 |     1 |           1 |
| 2026-10-09 |        52678 |     1 |           1 |

## Equity this week
| date       |   lookalike |   main |
|:-----------|------------:|-------:|
| 2026-10-07 |      100000 | 100000 |
| 2026-10-08 |      100000 | 100000 |
| 2026-10-09 |      100000 | 100000 |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
