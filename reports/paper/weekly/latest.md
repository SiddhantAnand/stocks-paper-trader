# Weekly paper-trading review - 2026-W43 (week of 2026-10-19)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 1.0 | risk x1.0 | shadow: {'policy': 'h1', 'hold': 1, 'tp': 4.0, 'sl': 3.0, 'thr': 0.4, 'slots': 2, 'started': '2026-10-16', 'evidence': {'oos': '2025-11..2026-10', 'trades': 252, 'avg_net': 0.6, 'win': 51.6, 'pf': 1.46, 'total': 101.5, 'wk8_median': 7.8, 'wk8_worst': -9.1, 'maxdd': -14.3}, 'name': 'score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0%'}

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 0 | - | - | - | 3 | 66.7 | -0.42 | 0.85 | 100,360 |
| lookalike | 0 | - | - | - | 3 | 0.0 | -2.26 | 0.0 | 97,759 |
| shadow | 2 | 0.0 | -3.35 | -3339 | 2 | 0.0 | -3.35 | 0.0 | 94,936 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 3 main trades of ~80 needed for a confident verdict.

## Trades closed this week
| book   | sym     | entry_date   | exit_date   |   entry_px |   exit_px | reason   |   ret_net |      pnl |   pred |   analog_avg |   cfg_ver | lesson                                      |
|:-------|:--------|:-------------|:------------|-----------:|----------:|:---------|----------:|---------:|-------:|-------------:|----------:|:--------------------------------------------|
| shadow | PRAJIND | 2026-10-19   | 2026-10-21  |     275.6  |    267.33 | stop     |     -3.35 | -1671.46 |  0.946 |        0.157 |         1 | hit stop intraday; weak market day at entry |
| shadow | APTUS   | 2026-10-19   | 2026-10-21  |     212.77 |    206.39 | stop     |     -3.35 | -1667.18 |  0.9   |        0.516 |         1 | hit stop intraday; weak market day at entry |

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |   labelled |   corr |   above_thr |   above_thr_avg |   below_thr_avg |
|:-----------|-------------:|------:|------------:|-----------:|-------:|------------:|----------------:|----------------:|
| 2026-10-19 |        53203 |     1 |           1 |        448 |  0.189 |           3 |           -0.37 |           -0.73 |
| 2026-10-21 |        53319 |     1 |           1 |        567 |  0.039 |           3 |           -0.37 |           -1.12 |
| 2026-10-22 |        53569 |     1 |           1 |        782 |  0.118 |           3 |           -0.37 |           -1.32 |
| 2026-10-23 |        53664 |     1 |           1 |        866 |  0.156 |           3 |           -0.37 |           -1.52 |

## Equity this week
| date       |   lookalike |   main |   shadow |
|:-----------|------------:|-------:|---------:|
| 2026-10-19 |     97759.1 | 100360 | 100058   |
| 2026-10-21 |     97759.1 | 100360 |  96661.4 |
| 2026-10-22 |     97759.1 | 100360 |  96603.3 |
| 2026-10-23 |     97759.1 | 100360 |  94935.6 |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
