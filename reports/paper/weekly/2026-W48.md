# Weekly paper-trading review - 2026-W48 (week of 2026-11-23)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 1.2 | risk x0.5 | shadow: {'policy': 'h1', 'hold': 1, 'tp': 4.0, 'sl': 3.0, 'thr': 0.4, 'slots': 2, 'started': '2026-10-16', 'evidence': {'oos': '2025-11..2026-10', 'trades': 252, 'avg_net': 0.6, 'win': 51.6, 'pf': 1.46, 'total': 101.5, 'wk8_median': 7.8, 'wk8_worst': -9.1, 'maxdd': -14.3}, 'name': 'score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0%'}

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 7 | 14.3 | -1.74 | -3286 | 28 | 53.6 | 0.29 | 1.21 | 102,171 |
| lookalike | 7 | 42.9 | -2.3 | -5181 | 28 | 42.9 | -0.72 | 0.66 | 93,280 |
| shadow | 6 | 16.7 | -1.65 | -3144 | 32 | 31.2 | -0.61 | 0.64 | 93,837 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 28 main trades of ~80 needed for a confident verdict.

## Trades closed this week
| book      | sym        | entry_date   | exit_date   |   entry_px |   exit_px | reason     |   ret_net |      pnl |   pred |   analog_avg |   cfg_ver | lesson                                                                    |
|:----------|:-----------|:-------------|:------------|-----------:|----------:|:-----------|----------:|---------:|-------:|-------------:|----------:|:--------------------------------------------------------------------------|
| main      | EBGNG      | 2026-11-20   | 2026-11-23  |     470.1  |    488.9  | target     |      3.65 |  1269.44 |  1.651 |        0.259 |         1 | worked: target; entered on -8.8% day, close-in-range 0.01, pred +1.65     |
| shadow    | EBGNG      | 2026-11-20   | 2026-11-23  |     470.1  |    488.9  | target     |      3.65 |  1766.93 |  1.651 |        0.259 |         1 | worked: target; entered on -8.8% day, close-in-range 0.01, pred +1.65     |
| lookalike | AVALON     | 2026-11-20   | 2026-11-23  |    1727    |   1675.19 | stop       |     -3.35 | -1099.24 | -0.073 |      nan     |         1 | hit stop intraday                                                         |
| main      | TBZ        | 2026-11-20   | 2026-11-25  |     547    |    530.59 | stop       |     -3.35 |  -586.38 |  0.87  |       -0.977 |         1 | hit stop intraday; historical analogs were negative                       |
| lookalike | HFCL       | 2026-11-20   | 2026-11-25  |     184.72 |    169.67 | gap_stop   |     -8.5  | -2778.28 | -1.146 |      nan     |         1 | gapped below stop overnight (overnight risk)                              |
| shadow    | TBZ        | 2026-11-20   | 2026-11-25  |     547    |    530.59 | stop       |     -3.35 |  -806.28 |  0.87  |       -0.977 |         1 | hit stop intraday; historical analogs were negative                       |
| main      | SKYGOLD    | 2026-11-23   | 2026-11-25  |     818.25 |    793.7  | stop       |     -3.35 | -1178.8  |  1.318 |        0.956 |         1 | hit stop intraday; weak market day at entry                               |
| shadow    | SKYGOLD    | 2026-11-23   | 2026-11-25  |     818.25 |    793.7  | stop       |     -3.35 | -1644.83 |  1.318 |        0.956 |         1 | hit stop intraday; weak market day at entry                               |
| lookalike | KAYNES     | 2026-11-23   | 2026-11-25  |    2809    |   2724.73 | stop       |     -3.35 | -1035.12 |  0.904 |      nan     |         1 | hit stop intraday; weak market day at entry                               |
| main      | INOXWIND   | 2026-11-23   | 2026-11-25  |      53.61 |     52.56 | time       |     -2.31 |  -409.66 |  1.143 |       -0.309 |         1 | weak market day at entry; historical analogs were negative                |
| lookalike | PFOCUS     | 2026-11-23   | 2026-11-25  |     235.45 |    238.8  | time       |      1.07 |   346.05 |  0.936 |      nan     |         1 | worked: time; entered on -6.8% day, close-in-range 0.07, pred +0.94       |
| lookalike | SGMART     | 2026-11-25   | 2026-11-26  |     829.45 |    745    | gap_stop   |    -10.53 | -3232.06 | -1.728 |      nan     |         1 | gapped below stop overnight (overnight risk)                              |
| lookalike | ATLANTAELE | 2026-11-25   | 2026-11-26  |    1387.2  |   1460    | gap_target |      4.9  |  1494.79 |  0.323 |      nan     |         1 | worked: gap_target; entered on -3.3% day, close-in-range 0.04, pred +0.32 |
| lookalike | BLUESTONE  | 2026-11-25   | 2026-11-26  |     640.95 |    666.59 | target     |      3.65 |  1123.04 |  0.577 |      nan     |         1 | worked: target; entered on -3.6% day, close-in-range 0.01, pred +0.58     |
| main      | UTLSOLAR   | 2026-11-25   | 2026-11-26  |     276.45 |    268.16 | stop       |     -3.35 | -1166.45 |  1.603 |        0.066 |         1 | hit stop intraday                                                         |
| shadow    | UTLSOLAR   | 2026-11-25   | 2026-11-26  |     276.45 |    268.16 | stop       |     -3.35 | -1610.82 |  1.603 |        0.066 |         1 | hit stop intraday                                                         |
| main      | IONEXCHANG | 2026-11-25   | 2026-11-26  |     271.55 |    263.4  | stop       |     -3.35 | -1164.85 |  0.868 |        0.053 |         1 | hit stop intraday                                                         |
| main      | APLAPOLLO  | 2026-11-25   | 2026-11-26  |    1475    |   1478    | time       |     -0.15 |   -49.74 |  1.863 |        0.165 |         1 | no follow-through, small time-exit loss (costs)                           |
| shadow    | APLAPOLLO  | 2026-11-25   | 2026-11-26  |    1475    |   1478    | time       |     -0.15 |   -69.2  |  1.863 |        0.165 |         1 | no follow-through, small time-exit loss (costs)                           |
| shadow    | SPECTRUM   | 2026-11-26   | 2026-11-27  |    3878.6  |   3762.24 | stop       |     -3.35 |  -779.61 |  0.604 |       -1.455 |         1 | hit stop intraday; historical analogs were negative                       |

## Loss reasons this week (main)
| lesson                                          |   count |
|:------------------------------------------------|--------:|
| hit stop intraday                               |       4 |
| historical analogs were negative                |       2 |
| weak market day at entry                        |       2 |
| no follow-through, small time-exit loss (costs) |       1 |

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |   labelled |   corr |   above_thr |   above_thr_avg |   below_thr_avg |
|:-----------|-------------:|------:|------------:|-----------:|-------:|------------:|----------------:|----------------:|
| 2026-11-23 |        55940 |   0.8 |         1   |       3556 |  0.124 |          24 |            1    |           -0.53 |
| 2026-11-25 |        55945 |   0.8 |         1   |       3646 |  0.121 |          46 |            0.18 |           -0.53 |
| 2026-11-26 |        55951 |   1   |         0.5 |       3744 |  0.125 |          50 |            0.03 |           -0.52 |
| 2026-11-27 |        55758 |   1.2 |         0.5 |       3844 |  0.123 |          50 |            0.03 |           -0.51 |

## Equity this week
| date       |   lookalike |   main |   shadow |
|:-----------|------------:|-------:|---------:|
| 2026-11-23 |     96443   | 106421 |  98287.8 |
| 2026-11-25 |     93990.7 | 104678 |  96311.7 |
| 2026-11-26 |     93280.3 | 102171 |  94617.1 |
| 2026-11-27 |     93280.3 | 102171 |  93837.5 |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
