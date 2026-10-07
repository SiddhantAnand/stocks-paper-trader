# Paper trading report - 2026-10-07

Model: buy at ~15:20 on 3%+ movers scored > threshold, sell next session (target +4.0% / stop -3.0%), Rs 100,000 per book, max 3 positions, costs 0.35% round trip. Run 2026-10-07 -> 2026-12-02.

## Books
| book | equity | P&L | return | open | trades | win% | avg net % | profit factor |
|---|---|---|---|---|---|---|---|---|
| main | 100,000 | +0 | +0.00% | 0 | 0 | - | - | - |
| lookalike | 100,000 | -0 | -0.00% | 0 | 0 | - | - | - |

Research expectation (out-of-sample 2025-26): avg 0.85% / trade, win 55.6%, profit factor 1.73, 8-week median 6.1%.

## Learning log
| date       |   train_rows |   thr |   risk_mult |
|:-----------|-------------:|------:|------------:|
| 2026-10-07 |        53074 |     1 |           1 |

## Equity curve
| date       |   lookalike |   main |
|:-----------|------------:|-------:|
| 2026-10-07 |      100000 | 100000 |

_Paper trades only. Fills assume the ~15:20 price; real fills can differ._