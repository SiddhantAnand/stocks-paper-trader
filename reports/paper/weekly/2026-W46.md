# Weekly paper-trading review - 2026-W46 (week of 2026-11-09)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 0.8 | risk x1.0 | shadow: {'policy': 'h1', 'hold': 1, 'tp': 4.0, 'sl': 3.0, 'thr': 0.4, 'slots': 2, 'started': '2026-10-16', 'evidence': {'oos': '2025-11..2026-10', 'trades': 252, 'avg_net': 0.6, 'win': 51.6, 'pf': 1.46, 'total': 101.5, 'wk8_median': 7.8, 'wk8_worst': -9.1, 'maxdd': -14.3}, 'name': 'score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0%'}

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 7 | 57.1 | 0.5 | 1217 | 20 | 65.0 | 0.88 | 1.82 | 104,991 |
| lookalike | 7 | 28.6 | -0.9 | -2045 | 20 | 40.0 | -0.38 | 0.77 | 97,290 |
| shadow | 6 | 33.3 | -0.15 | 648 | 21 | 33.3 | -0.57 | 0.68 | 96,120 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 20 main trades of ~80 needed for a confident verdict.

## Trades closed this week
| book      | sym        | entry_date   | exit_date   |   entry_px |   exit_px | reason     |   ret_net |      pnl |   pred |   analog_avg |   cfg_ver | lesson                                                                                                         |
|:----------|:-----------|:-------------|:------------|-----------:|----------:|:-----------|----------:|---------:|-------:|-------------:|----------:|:---------------------------------------------------------------------------------------------------------------|
| main      | HFCL       | 2026-11-05   | 2026-11-09  |     219.61 |    213    | gap_stop   |     -3.36 |  -575.53 |  1.259 |       -0.866 |         1 | gapped below stop overnight (overnight risk); historical analogs were negative                                 |
| lookalike | STLTECH    | 2026-11-05   | 2026-11-09  |     757.75 |    688    | gap_stop   |     -9.55 | -3113.29 | -0.745 |      nan     |         1 | gapped below stop overnight (overnight risk)                                                                   |
| lookalike | AEROFLEX   | 2026-11-06   | 2026-11-09  |     483.3  |    502.95 | gap_target |      3.72 |  1221.18 | -0.153 |      nan     |         1 | worked: gap_target; entered on -10.6% day, close-in-range 0.34, pred -0.15                                     |
| shadow    | HFCL       | 2026-11-05   | 2026-11-09  |     219.61 |    213    | gap_stop   |     -3.36 |  -796.89 |  1.259 |       -0.866 |         1 | gapped below stop overnight (overnight risk); historical analogs were negative                                 |
| main      | KISSHT     | 2026-11-06   | 2026-11-09  |     346.9  |    360.78 | target     |      3.65 |  1253.92 |  1.722 |        0.035 |         1 | worked: target; entered on +4.9% day, close-in-range 1.00, pred +1.72                                          |
| shadow    | KISSHT     | 2026-11-06   | 2026-11-09  |     346.9  |    360.78 | target     |      3.65 |  1735.22 |  1.722 |        0.035 |         1 | worked: target; entered on +4.9% day, close-in-range 1.00, pred +1.72                                          |
| main      | KMEW       | 2026-11-06   | 2026-11-09  |     649    |    665    | time       |      2.12 |   356.94 |  1.112 |       -1.512 |         1 | worked: time; entered on -79.4% day, close-in-range 0.98, pred +1.11                                           |
| lookalike | ACE        | 2026-11-06   | 2026-11-09  |    1167.05 |   1166.75 | time       |     -0.38 |  -122.77 | -0.244 |      nan     |         1 | no follow-through, small time-exit loss (costs)                                                                |
| lookalike | TDPOWERSYS | 2026-11-11   | 2026-11-12  |     606.95 |    631.23 | target     |      3.65 |  1174.25 |  0.831 |      nan     |         1 | worked: target; entered on +6.2% day, close-in-range 0.78, pred +0.83                                          |
| main      | SETL       | 2026-11-11   | 2026-11-12  |     331.5  |    344.76 | target     |      3.65 |   629.19 |  1.342 |       -0.829 |         1 | worked: target; entered on -3.8% day, close-in-range 0.07, pred +1.34                                          |
| shadow    | SETL       | 2026-11-11   | 2026-11-12  |     331.5  |    344.76 | target     |      3.65 |   871.18 |  1.342 |       -0.829 |         1 | worked: target; entered on -3.8% day, close-in-range 0.07, pred +1.34                                          |
| main      | RAIN       | 2026-11-11   | 2026-11-12  |     167.8  |    167.02 | time       |     -0.81 |  -142.2  |  0.934 |       -0.352 |         1 | no follow-through, small time-exit loss (costs); up-day but closed off highs; historical analogs were negative |
| main      | MPHASIS    | 2026-11-11   | 2026-11-12  |    2380.8  |   2409.9  | time       |      0.87 |   145.37 |  0.865 |       -0.518 |         1 | worked: time; entered on -3.0% day, close-in-range 0.07, pred +0.86                                            |
| lookalike | BIRLACABLE | 2026-11-11   | 2026-11-12  |     329.8  |    321    | time       |     -3.02 |  -975.52 |  0.449 |      nan     |         1 | no obvious flag - normal variance                                                                              |
| lookalike | GALLANTT   | 2026-11-11   | 2026-11-12  |     526.5  |    527.7  | time       |     -0.12 |   -39.21 |  0.375 |      nan     |         1 | no follow-through, small time-exit loss (costs)                                                                |
| shadow    | RAIN       | 2026-11-11   | 2026-11-12  |     167.8  |    167.02 | time       |     -0.81 |  -195.52 |  0.934 |       -0.352 |         1 | no follow-through, small time-exit loss (costs); up-day but closed off highs; historical analogs were negative |
| main      | SHARDACROP | 2026-11-12   | 2026-11-13  |     745.5  |    728.5  | time       |     -2.63 |  -451.01 |  0.91  |       -0.755 |         1 | historical analogs were negative                                                                               |
| lookalike | KIRLPNU    | 2026-11-12   | 2026-11-13  |     661.05 |    659.5  | time       |     -0.58 |  -189.32 |  0.482 |      nan     |         1 | no follow-through, small time-exit loss (costs)                                                                |
| shadow    | SHARDACROP | 2026-11-12   | 2026-11-13  |     745.5  |    728.5  | time       |     -2.63 |  -627.5  |  0.91  |       -0.755 |         1 | historical analogs were negative                                                                               |
| shadow    | KTKBANK    | 2026-11-12   | 2026-11-13  |     366.25 |    362.4  | time       |     -1.4  |  -338.7  |  0.758 |       -1.284 |         1 | historical analogs were negative                                                                               |

## Loss reasons this week (main)
| lesson                                          |   count |
|:------------------------------------------------|--------:|
| historical analogs were negative                |       3 |
| gapped below stop overnight (overnight risk)    |       1 |
| no follow-through, small time-exit loss (costs) |       1 |
| up-day but closed off highs                     |       1 |

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |   labelled |   corr |   above_thr |   above_thr_avg |   below_thr_avg |
|:-----------|-------------:|------:|------------:|-----------:|-------:|------------:|----------------:|----------------:|
| 2026-11-09 |        55632 |   0.8 |           1 |       2728 |  0.159 |          18 |            0.68 |           -0.55 |
| 2026-11-11 |        55761 |   0.8 |           1 |       2849 |  0.137 |          18 |            0.68 |           -0.49 |
| 2026-11-12 |        55906 |   0.8 |           1 |       2977 |  0.137 |          21 |            0.89 |           -0.46 |
| 2026-11-13 |        56022 |   0.8 |           1 |       3065 |  0.128 |          22 |            0.76 |           -0.47 |

## Equity this week
| date       |   lookalike |   main |   shadow |
|:-----------|------------:|-------:|---------:|
| 2026-11-09 |     97320.1 | 104810 |  96410.6 |
| 2026-11-11 |     96881.3 | 104864 |  96396.6 |
| 2026-11-12 |     97469.9 | 105368 |  96967.4 |
| 2026-11-13 |     97290.3 | 104991 |  96120.1 |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
