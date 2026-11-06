# Weekly paper-trading review - 2026-W45 (week of 2026-11-02)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 0.8 | risk x1.0 | shadow: {'policy': 'h1', 'hold': 1, 'tp': 4.0, 'sl': 3.0, 'thr': 0.4, 'slots': 2, 'started': '2026-10-16', 'evidence': {'oos': '2025-11..2026-10', 'trades': 252, 'avg_net': 0.6, 'win': 51.6, 'pf': 1.46, 'total': 101.5, 'wk8_median': 7.8, 'wk8_worst': -9.1, 'maxdd': -14.3}, 'name': 'score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0%'}

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 5 | 80.0 | 0.52 | 1054 | 13 | 69.2 | 1.08 | 1.96 | 103,027 |
| lookalike | 5 | 20.0 | -2.11 | -3606 | 13 | 46.2 | -0.11 | 0.93 | 97,685 |
| shadow | 5 | 40.0 | -0.48 | -711 | 15 | 33.3 | -0.73 | 0.61 | 94,300 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 13 main trades of ~80 needed for a confident verdict.

## Trades closed this week
| book      | sym        | entry_date   | exit_date   |   entry_px |   exit_px | reason   |   ret_net |      pnl |   pred |   analog_avg |   cfg_ver | lesson                                                                |
|:----------|:-----------|:-------------|:------------|-----------:|----------:|:---------|----------:|---------:|-------:|-------------:|----------:|:----------------------------------------------------------------------|
| main      | INTELLECT  | 2026-11-02   | 2026-11-03  |     531.8  |    553.07 | target   |      3.65 |  1242.16 |  0.801 |        1.644 |         1 | worked: target; entered on +5.4% day, close-in-range 0.71, pred +0.80 |
| lookalike | PNCINFRA   | 2026-11-02   | 2026-11-03  |     129.86 |    125.96 | stop     |     -3.35 | -1149.59 |  0.038 |      nan     |         1 | hit stop intraday                                                     |
| main      | DYNAMATECH | 2026-11-02   | 2026-11-03  |   11977    |  12203    | time     |      1.54 |   184.08 |  1.057 |       -1.169 |         1 | worked: time; entered on +3.2% day, close-in-range 0.99, pred +1.06   |
| lookalike | JAMNAAUTO  | 2026-11-02   | 2026-11-03  |     125.41 |    123.01 | time     |     -2.26 |  -775.03 |  0.106 |      nan     |         1 | no obvious flag - normal variance                                     |
| shadow    | DYNAMATECH | 2026-11-02   | 2026-11-03  |   11977    |  12203    | time     |      1.54 |   368.16 |  1.057 |       -1.169 |         1 | worked: time; entered on +3.2% day, close-in-range 0.99, pred +1.06   |
| main      | E2E        | 2026-11-02   | 2026-11-04  |     499.5  |    484.51 | stop     |     -3.35 |  -569.1  |  1.713 |       -1.663 |         1 | hit stop intraday; historical analogs were negative                   |
| lookalike | STLTECH    | 2026-11-02   | 2026-11-04  |     783.3  |    738.3  | gap_stop |     -6.09 | -2052.89 | -2.451 |      nan     |         1 | gapped below stop overnight (overnight risk)                          |
| shadow    | E2E        | 2026-11-02   | 2026-11-04  |     499.5  |    484.51 | stop     |     -3.35 |  -803.44 |  1.713 |       -1.663 |         1 | hit stop intraday; historical analogs were negative                   |
| shadow    | KIRLPNU    | 2026-11-04   | 2026-11-05  |     574.2  |    570.85 | time     |     -0.93 |  -444.86 |  0.553 |        0.35  |         1 | no follow-through, small time-exit loss (costs)                       |
| shadow    | SUMICHEM   | 2026-11-04   | 2026-11-05  |     328.1  |    329.15 | time     |     -0.03 |   -14.26 |  0.449 |        0.01  |         1 | no follow-through, small time-exit loss (costs)                       |
| main      | MOTILALOFS | 2026-11-05   | 2026-11-06  |    1094.9  |   1103    | time     |      0.39 |   132.3  |  1.185 |        0.357 |         1 | worked: time; entered on +8.1% day, close-in-range 0.98, pred +1.19   |
| main      | MBAPL      | 2026-11-05   | 2026-11-06  |     194    |    195.41 | time     |      0.38 |    64.33 |  0.87  |       -0.28  |         1 | worked: time; entered on +3.6% day, close-in-range 1.00, pred +0.87   |
| lookalike | 360ONE     | 2026-11-05   | 2026-11-06  |    1143    |   1138    | time     |     -0.79 |  -252.01 |  0.415 |      nan     |         1 | no follow-through, small time-exit loss (costs)                       |
| lookalike | SHYAMMETL  | 2026-11-05   | 2026-11-06  |    1274.8  |   1304.2  | time     |      1.96 |   623.45 |  0.423 |      nan     |         1 | worked: time; entered on +3.5% day, close-in-range 0.83, pred +0.42   |
| shadow    | MOTILALOFS | 2026-11-05   | 2026-11-06  |    1094.9  |   1103    | time     |      0.39 |   183.52 |  1.185 |        0.357 |         1 | worked: time; entered on +8.1% day, close-in-range 0.98, pred +1.19   |

## Loss reasons this week (main)
| lesson                           |   count |
|:---------------------------------|--------:|
| hit stop intraday                |       1 |
| historical analogs were negative |       1 |

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |   labelled |   corr |   above_thr |   above_thr_avg |   below_thr_avg |
|:-----------|-------------:|------:|------------:|-----------:|-------:|------------:|----------------:|----------------:|
| 2026-11-02 |        54716 |   0.8 |           1 |       1860 |  0.11  |          11 |            1.34 |           -0.78 |
| 2026-11-03 |        54952 |   0.8 |           1 |       2077 |  0.153 |          13 |            0.82 |           -0.73 |
| 2026-11-04 |        55055 |   0.8 |           1 |       2169 |  0.169 |          13 |            0.82 |           -0.7  |
| 2026-11-05 |        55281 |   0.8 |           1 |       2392 |  0.188 |          13 |            0.82 |           -0.58 |
| 2026-11-06 |        55497 |   0.8 |           1 |       2601 |  0.158 |          16 |            0.45 |           -0.63 |

## Equity this week
| date       |   lookalike |   main |   shadow |
|:-----------|------------:|-------:|---------:|
| 2026-11-02 |    103042   | 102520 |  95938.8 |
| 2026-11-03 |     99999.5 | 103982 |  96318.5 |
| 2026-11-04 |     98963.6 | 103578 |  95747.9 |
| 2026-11-05 |     98784.8 | 103768 |  95523.1 |
| 2026-11-06 |     97684.9 | 103027 |  94300.2 |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
