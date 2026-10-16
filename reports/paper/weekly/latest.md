# Weekly paper-trading review - 2026-W42 (week of 2026-10-12)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 1.0 | risk x1.0 | shadow: {'policy': 'h1', 'hold': 1, 'tp': 4.0, 'sl': 3.0, 'thr': 0.4, 'slots': 2, 'started': '2026-10-16', 'evidence': {'oos': '2025-11..2026-10', 'trades': 252, 'avg_net': 0.6, 'win': 51.6, 'pf': 1.46, 'total': 101.5, 'wk8_median': 7.8, 'wk8_worst': -9.1, 'maxdd': -14.3}, 'name': 'score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0%'}

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 3 | 66.7 | -0.42 | 360 | 3 | 66.7 | -0.42 | 0.85 | 100,360 |
| lookalike | 3 | 0.0 | -2.26 | -2241 | 3 | 0.0 | -2.26 | 0.0 | 97,759 |
| shadow | 0 | - | - | - | 0 | - | - | - | 100,000 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 3 main trades of ~80 needed for a confident verdict.

## Trades closed this week
| book      | sym       | entry_date   | exit_date   |   entry_px |   exit_px | reason   |   ret_net |      pnl |   pred |   analog_avg |   cfg_ver | lesson                                                                         |
|:----------|:----------|:-------------|:------------|-----------:|----------:|:---------|----------:|---------:|-------:|-------------:|----------:|:-------------------------------------------------------------------------------|
| main      | SIGMAADV  | 2026-10-12   | 2026-10-14  |     961.7  |   1000.17 | target   |      3.65 |  1193.54 |  1.794 |        0.435 |         1 | worked: target; entered on -4.7% day, close-in-range 0.09, pred +1.79          |
| lookalike | BODALCHEM | 2026-10-12   | 2026-10-14  |     177.77 |    172.44 | stop     |     -3.35 | -1113.06 |  0.005 |      nan     |         1 | hit stop intraday; weak market day at entry                                    |
| main      | E2E       | 2026-10-12   | 2026-10-14  |     735.55 |    764.97 | target   |      3.65 |   590.6  |  1.377 |       -0.92  |         1 | worked: target; entered on +4.4% day, close-in-range 0.92, pred +1.38          |
| lookalike | SWANDEF   | 2026-10-12   | 2026-10-14  |    2931.1  |   2939    | time     |     -0.08 |   -25.95 |  0.128 |      nan     |         1 | no follow-through, small time-exit loss (costs); weak market day at entry      |
| lookalike | AHCL      | 2026-10-14   | 2026-10-15  |      29.04 |     28.17 | stop     |     -3.35 | -1101.84 | -3.614 |      nan     |         1 | hit stop intraday                                                              |
| main      | STLTECH   | 2026-10-14   | 2026-10-16  |     926    |    850.1  | gap_stop |     -8.55 | -1424.54 |  1.083 |       -0.367 |         1 | gapped below stop overnight (overnight risk); historical analogs were negative |

## Loss reasons this week (main)
| lesson                                       |   count |
|:---------------------------------------------|--------:|
| gapped below stop overnight (overnight risk) |       1 |
| historical analogs were negative             |       1 |

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |   labelled |    corr |   above_thr |   above_thr_avg |   below_thr_avg |
|:-----------|-------------:|------:|------------:|-----------:|--------:|------------:|----------------:|----------------:|
| 2026-10-12 |        52741 |     1 |           1 |        nan | nan     |         nan |          nan    |          nan    |
| 2026-10-13 |        52830 |     1 |           1 |         87 |   0.006 |           0 |          nan    |           -0.87 |
| 2026-10-14 |        52922 |     1 |           1 |        179 |   0.182 |           2 |            3.65 |           -0.3  |
| 2026-10-15 |        53006 |     1 |           1 |        258 |   0.276 |           2 |            3.65 |           -0.79 |
| 2026-10-16 |        53143 |     1 |           1 |        384 |   0.169 |           3 |           -0.37 |           -0.59 |

## Equity this week
| date       |   lookalike |   main |   shadow |
|:-----------|------------:|-------:|---------:|
| 2026-10-12 |    100000   | 100000 |      nan |
| 2026-10-13 |    100154   | 101487 |      nan |
| 2026-10-14 |     98861   | 101760 |      nan |
| 2026-10-15 |     97759.1 | 100928 |      nan |
| 2026-10-16 |     97759.1 | 100360 |   100000 |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
