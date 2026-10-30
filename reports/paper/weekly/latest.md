# Weekly paper-trading review - 2026-W44 (week of 2026-10-26)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 0.8 | risk x1.0 | shadow: {'policy': 'h1', 'hold': 1, 'tp': 4.0, 'sl': 3.0, 'thr': 0.4, 'slots': 2, 'started': '2026-10-16', 'evidence': {'oos': '2025-11..2026-10', 'trades': 252, 'avg_net': 0.6, 'win': 51.6, 'pf': 1.46, 'total': 101.5, 'wk8_median': 7.8, 'wk8_worst': -9.1, 'maxdd': -14.3}, 'name': 'score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0%'}

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 5 | 60.0 | 2.53 | 2361 | 8 | 62.5 | 1.43 | 2.01 | 102,721 |
| lookalike | 5 | 100.0 | 3.19 | 5182 | 8 | 62.5 | 1.14 | 2.35 | 102,941 |
| shadow | 8 | 37.5 | -0.24 | -478 | 10 | 30.0 | -0.86 | 0.64 | 96,183 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 8 main trades of ~80 needed for a confident verdict.

## Trades closed this week
| book      | sym        | entry_date   | exit_date   |   entry_px |   exit_px | reason     |   ret_net |      pnl |   pred |   analog_avg |   cfg_ver | lesson                                                                                                   |
|:----------|:-----------|:-------------|:------------|-----------:|----------:|:-----------|----------:|---------:|-------:|-------------:|----------:|:---------------------------------------------------------------------------------------------------------|
| shadow    | DIACABS    | 2026-10-22   | 2026-10-26  |     325    |    312    | gap_stop   |     -4.35 | -1046.18 |  0.769 |       -4.74  |         1 | gapped below stop overnight (overnight risk); weak market day at entry; historical analogs were negative |
| shadow    | KABRAEXTRU | 2026-10-22   | 2026-10-26  |     707.95 |    671.65 | gap_stop   |     -5.48 | -1318.45 |  0.478 |       -2.352 |         1 | gapped below stop overnight (overnight risk); weak market day at entry; historical analogs were negative |
| lookalike | J&KBANK    | 2026-10-26   | 2026-10-27  |     117.17 |    121.86 | target     |      3.65 |  1189.81 |  1.024 |      nan     |         1 | worked: target; entered on +3.6% day, close-in-range 0.96, pred +1.02                                    |
| lookalike | PWL        | 2026-10-26   | 2026-10-27  |     124.62 |    129.6  | target     |      3.65 |  1185.94 |  1.015 |      nan     |         1 | worked: target; entered on +3.9% day, close-in-range 0.93, pred +1.01                                    |
| main      | SWIGGY     | 2026-10-26   | 2026-10-27  |     185.75 |    190    | time       |      1.94 |   323.99 |  1.252 |       -0.381 |         1 | worked: time; entered on +5.5% day, close-in-range 0.67, pred +1.25                                      |
| main      | RAIN       | 2026-10-26   | 2026-10-27  |     205.68 |    202.35 | time       |     -1.97 |  -656.08 |  1.182 |        0.113 |         1 | no obvious flag - normal variance                                                                        |
| shadow    | SWIGGY     | 2026-10-26   | 2026-10-27  |     185.75 |    190    | time       |      1.94 |   453.58 |  1.252 |       -0.381 |         1 | worked: time; entered on +5.5% day, close-in-range 0.67, pred +1.25                                      |
| main      | KABRAEXTRU | 2026-10-26   | 2026-10-28  |     705    |    777    | gap_target |      9.86 |  1599.25 |  1.92  |       -1.841 |         1 | worked: gap_target; entered on +3.9% day, close-in-range 1.00, pred +1.92                                |
| shadow    | KABRAEXTRU | 2026-10-26   | 2026-10-28  |     705    |    777    | gap_target |      9.86 |  2294.57 |  1.92  |       -1.841 |         1 | worked: gap_target; entered on +3.9% day, close-in-range 1.00, pred +1.92                                |
| shadow    | SURYAROSNI | 2026-10-27   | 2026-10-28  |     216    |    209.52 | stop       |     -3.35 |  -788.72 |  0.526 |       -0.741 |         1 | hit stop intraday; historical analogs were negative                                                      |
| lookalike | SWANDEF    | 2026-10-26   | 2026-10-28  |    2576.4  |   2670    | time       |      3.28 |  1014.99 | -3.354 |      nan     |         1 | worked: time; entered on -5.0% day, close-in-range 0.00, pred -3.35                                      |
| lookalike | SKYGOLD    | 2026-10-28   | 2026-10-29  |     855.65 |    903    | gap_target |      5.18 |  1729.85 | -0.367 |      nan     |         1 | worked: gap_target; entered on -8.5% day, close-in-range 0.54, pred -0.37                                |
| main      | AEQUS      | 2026-10-28   | 2026-10-29  |     211.75 |    220.22 | target     |      3.65 |  1228.89 |  1.023 |        0.183 |         1 | worked: target; entered on -3.4% day, close-in-range 0.33, pred +1.02                                    |
| shadow    | AEQUS      | 2026-10-28   | 2026-10-29  |     211.75 |    220.22 | target     |      3.65 |  1754.45 |  1.023 |        0.183 |         1 | worked: target; entered on -3.4% day, close-in-range 0.33, pred +1.02                                    |
| main      | TIPSMUSIC  | 2026-10-28   | 2026-10-29  |     795    |    791.35 | time       |     -0.81 |  -135.08 |  1.346 |       -0.587 |         1 | no follow-through, small time-exit loss (costs); historical analogs were negative                        |
| lookalike | OMNI       | 2026-10-28   | 2026-10-29  |     712.8  |    716.6  | time       |      0.18 |    61.34 |  0.678 |      nan     |         1 | worked: time; entered on +4.5% day, close-in-range 0.95, pred +0.68                                      |
| shadow    | TIPSMUSIC  | 2026-10-28   | 2026-10-29  |     795    |    791.35 | time       |     -0.81 |  -192.98 |  1.346 |       -0.587 |         1 | no follow-through, small time-exit loss (costs); historical analogs were negative                        |
| shadow    | MSTCLTD    | 2026-10-29   | 2026-10-30  |     574    |    556.78 | stop       |     -3.35 | -1634.47 |  0.409 |        0.434 |         1 | hit stop intraday                                                                                        |

## Loss reasons this week (main)
| lesson                                          |   count |
|:------------------------------------------------|--------:|
| no obvious flag - normal variance               |       1 |
| no follow-through, small time-exit loss (costs) |       1 |
| historical analogs were negative                |       1 |

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |   labelled |   corr |   above_thr |   above_thr_avg |   below_thr_avg |
|:-----------|-------------:|------:|------------:|-----------:|-------:|------------:|----------------:|----------------:|
| 2026-10-26 |        53942 |   1   |           1 |       1141 |  0.031 |           3 |           -0.37 |           -1.31 |
| 2026-10-27 |        54059 |   1   |           1 |       1265 |  0.097 |           8 |            0.25 |           -1.08 |
| 2026-10-28 |        54245 |   1   |           1 |       1425 |  0.118 |           9 |            1.3  |           -1    |
| 2026-10-29 |        54358 |   0.9 |           1 |       1527 |  0.131 |          11 |            1.34 |           -0.97 |
| 2026-10-30 |        54471 |   0.8 |           1 |       1633 |  0.135 |          11 |            1.34 |           -1.05 |

## Equity this week
| date       |   lookalike |   main |   shadow |
|:-----------|------------:|-------:|---------:|
| 2026-10-26 |     99218.5 | 100431 |  94326.4 |
| 2026-10-27 |    101038   | 100859 |  95667.5 |
| 2026-10-28 |    101556   | 101635 |  96268.6 |
| 2026-10-29 |    102941   | 102721 |  97643.4 |
| 2026-10-30 |    102941   | 102721 |  96183.2 |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
