# Weekly paper-trading review - 2026-W47 (week of 2026-11-16)

Config version 1 | hold 1 | target +4.0% | stop -3.0% | threshold now 0.8 | risk x1.0 | shadow: {'policy': 'h1', 'hold': 1, 'tp': 4.0, 'sl': 3.0, 'thr': 0.4, 'slots': 2, 'started': '2026-10-16', 'evidence': {'oos': '2025-11..2026-10', 'trades': 252, 'avg_net': 0.6, 'win': 51.6, 'pf': 1.46, 'total': 101.5, 'wk8_median': 7.8, 'wk8_worst': -9.1, 'maxdd': -14.3}, 'name': 'score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0%'}

## This week vs whole run
| book | week trades | week win% | week avg % | week P&L | total trades | total win% | total avg % | PF | equity |
|---|---|---|---|---|---|---|---|---|---|
| main | 1 | 100.0 | 2.69 | 466 | 21 | 66.7 | 0.96 | 1.94 | 105,556 |
| lookalike | 1 | 100.0 | 3.65 | 1171 | 21 | 42.9 | -0.19 | 0.88 | 99,066 |
| shadow | 5 | 40.0 | 0.47 | 861 | 26 | 34.6 | -0.37 | 0.76 | 97,117 |

Research expectation: avg 0.85% / trade, win 55.6%, PF 1.73. Evidence: 21 main trades of ~80 needed for a confident verdict.

## Trades closed this week
| book      | sym        | entry_date   | exit_date   |   entry_px |   exit_px | reason   |   ret_net |      pnl |   pred |   analog_avg |   cfg_ver | lesson                                                                                                      |
|:----------|:-----------|:-------------|:------------|-----------:|----------:|:---------|----------:|---------:|-------:|-------------:|----------:|:------------------------------------------------------------------------------------------------------------|
| shadow    | ASHAPURMIN | 2026-11-16   | 2026-11-17  |     402.7  |    418.81 | target   |      3.65 |  1749.37 |  0.696 |        0.074 |         1 | worked: target; entered on -3.0% day, close-in-range 0.04, pred +0.70                                       |
| shadow    | SHILCTECH  | 2026-11-16   | 2026-11-17  |    3430    |   3406.1  | time     |     -1.05 |  -251.33 |  0.762 |       -0.751 |         1 | historical analogs were negative                                                                            |
| shadow    | EBGNG      | 2026-11-17   | 2026-11-18  |     526.95 |    516.2  | time     |     -2.39 | -1158.68 |  0.748 |        0.342 |         1 | no obvious flag - normal variance                                                                           |
| lookalike | STLTECH    | 2026-11-17   | 2026-11-19  |     641.5  |    667.16 | target   |      3.65 |  1170.74 | -1.257 |      nan     |         1 | worked: target; entered on -5.0% day, close-in-range 0.00, pred -1.26                                       |
| main      | HFCL       | 2026-11-17   | 2026-11-19  |     188.4  |    194.13 | time     |      2.69 |   466.5  |  1.168 |       -0.113 |         1 | worked: time; entered on -3.5% day, close-in-range 0.33, pred +1.17                                         |
| shadow    | HFCL       | 2026-11-17   | 2026-11-19  |     188.4  |    194.13 | time     |      2.69 |   654.11 |  1.168 |       -0.113 |         1 | worked: time; entered on -3.5% day, close-in-range 0.33, pred +1.17                                         |
| shadow    | ICIL       | 2026-11-18   | 2026-11-19  |     578.8  |    577.6  | time     |     -0.56 |  -132.26 |  0.701 |       -0.067 |         1 | no follow-through, small time-exit loss (costs); weak market day at entry; historical analogs were negative |

## Learning log this week
| date       |   train_rows |   thr |   risk_mult |   labelled |   corr |   above_thr |   above_thr_avg |   below_thr_avg |
|:-----------|-------------:|------:|------------:|-----------:|-------:|------------:|----------------:|----------------:|
| 2026-11-16 |        56097 |   0.8 |           1 |       3124 |  0.126 |          22 |            0.76 |           -0.5  |
| 2026-11-17 |        56067 |   0.8 |           1 |       3240 |  0.124 |          22 |            0.76 |           -0.5  |
| 2026-11-18 |        56062 |   0.8 |           1 |       3315 |  0.123 |          22 |            0.76 |           -0.52 |
| 2026-11-19 |        55977 |   0.8 |           1 |       3397 |  0.121 |          23 |            0.88 |           -0.51 |
| 2026-11-20 |        55999 |   0.8 |           1 |       3486 |  0.122 |          23 |            0.88 |           -0.51 |

## Equity this week
| date       |   lookalike |   main |   shadow |
|:-----------|------------:|-------:|---------:|
| 2026-11-16 |     97290.3 | 104991 |  96158.2 |
| 2026-11-17 |     97290.3 | 104972 |  97632.4 |
| 2026-11-18 |     98872.8 | 105828 |  97541.1 |
| 2026-11-19 |     98461.1 | 105458 |  96981.3 |
| 2026-11-20 |     99066.3 | 105556 |  97117   |

## Review checklist (/weekly-review)
- Data problems: missing bars, odd prices, failed runs in data/paper/log.txt
- News or results around each losing trade (was it predictable?)
- Live results vs research expectation; do not change settings on fewer than ~20 trades
- Any change must pass research.py walk-forward, or run as a shadow book first
