# Daily paper-trading report - Fri, 23 Oct 2026
> Practice trading with Rs 1,00,000 of virtual money. No real money is used. Run: 2026-10-07 to 2026-12-02.

## Today in one line
**No new trades today.** 295 stocks moved 3% or more, and 0 scored above the model's bar of 1.0.

## Scoreboard (main strategy)
| Measure | Value |
|---|---|
| Portfolio value | **Rs 1,00,360** |
| Today's change | Rs 0 (+0.00%) |
| Total profit / loss since 2026-10-07 | **+Rs 360** (▲ +0.36%) |
| Trades completed | 3 (2 wins, 1 losses) |
| Win rate | 67% (expected about 55.6%) |
| Average result per trade | ▼ -0.42% (expected about ▲ +0.85%) |
| Profit factor | 0.85 (expected about 1.73) |
| Stocks held now | 0 of 3 slots |
| Cash available | Rs 1,00,360 |
| Evidence so far | 3 of ~80 trades needed for a reliable verdict |

## What happened today
Nothing was bought or sold today.

## Stocks we're holding
| Book | Stock | Bought on | Buy price | Latest | Change | Sell if it reaches | Sell if it falls to |
|---|---|---|---|---|---|---|---|
| shadow | **DIACABS** | 2026-10-22 | 325.00 | 315.05 | ▼ -3.06% | 338.00 (profit target) | 315.25 (stop-loss) |
| shadow | **KABRAEXTRU** | 2026-10-22 | 707.95 | 678.85 | ▼ -4.11% | 736.27 (profit target) | 686.71 (stop-loss) |

_Anything not sold by target or stop-loss is sold at about 3:15 pm on the next trading day (2 days for T2T stocks)._

## Today's market check
| Measure | Value |
|---|---|
| Nifty 50 | 22,600 (▼ -0.39%) |
| Market fear (India VIX) | 16.8 - nervous (below 15 calm, 15-20 nervous, above 20 fearful) |
| Stocks scanned | 1,016 |
| Moved 3% or more today | 295 |
| Scored above the bar (1.0) | 0 |

## Top candidates the model looked at
| Stock | Today's move | Model score | Decision |
|---|---|---|---|
| CAPILLARY | ▲ +5.34% | +0.16 | Skipped - score below the bar |
| CUPID | ▼ -4.14% | -0.44 | Skipped - score below the bar |
| SGMART | ▲ +4.14% | -0.78 | Skipped - score below the bar |
| EXIDEIND | ▼ -3.30% | -0.91 | Skipped - score below the bar |
| TITAGARH | ▼ -4.46% | -0.97 | Skipped - score below the bar |
| DIACABS | ▼ -3.02% | -1.00 | Skipped - score below the bar |
| FINCABLES | ▼ -4.16% | -1.01 | Skipped - score below the bar |
| AEGISLOG | ▼ -4.42% | -1.01 | Skipped - score below the bar |

## How the model is learning
- Retrained tonight on **53,664** past setups, including every setup that finished today. Recent data counts more.
- The bar to buy is **1.0** and position size is **100%**. Both tighten automatically after a losing streak and relax after a winning one.
- Prediction check: of 866 past predictions, stocks above the bar averaged ▼ -0.37% next day vs ▼ -1.52% for the rest.

## Experiments running alongside
| Book | Value | Total profit / loss | Trades | What it tests |
|---|---|---|---|---|
| lookalike | Rs 97,759 | -Rs 2,241 | 3 | Experiment: buys the most similar-looking stock to each main pick, to test whether 'similar stocks' also work. |
| shadow | Rs 94,936 | -Rs 5,064 | 2 | Practice account: settings found by the weekly self-tuning. They replace the main settings automatically if they make more money over 20 trades. |

## How this works
1. **3:15 pm every trading day:** the system scans about 1,100 NSE stocks and keeps those that moved 3% or more today and trade at least Rs 5 crore a day.
2. **Scoring:** a machine-learning model, trained on about 2 years of similar situations, gives each stock a score = expected next-day return after costs.
3. **Buying:** up to 3 stocks scoring above the bar are bought (about Rs 33,333 each). Half size if similar past setups lost money.
4. **Selling (next trading day):** at **+4.0%** profit target, **-3.0%** stop-loss, or at about 3:15 pm - whichever comes first. T2T stocks are held 2 days.
5. **Every evening:** prices are updated, the model retrains, yesterday's predictions are checked, and this report is sent.
6. **Costs:** 0.35% per round trip (taxes, charges, slippage) is deducted from every trade.

### What the model looks at
| Factor | In plain words |
|---|---|
| Today's move | How much the stock rose or fell today (only stocks moving 3% or more are considered). |
| Opening gap | Did it open much higher or lower than yesterday's close? |
| Close position in the day's range | Closing near the day's high shows buyers in control; near the low shows sellers. |
| Recent momentum | Price change over the last 2, 5 and 20 trading days. |
| Distance from 20-day and 50-day averages | How stretched the price is above or below its usual level. |
| Trend | Is the short-term average above the longer-term average (uptrend)? |
| RSI (strength index, 0-100) | Above 70 = overheated, below 30 = oversold. |
| Volatility (ATR) | How much the stock normally moves in a day. |
| Volume surge | Today's trading volume compared with its 20-day average. |
| Position in 20-day range | 0 = at the 20-day low, 1 = at the 20-day high. |
| Distance from 52-week high | How far below its one-year peak the stock is. |
| Liquidity | Average daily traded value - only stocks trading at least Rs 5 crore a day are used. |
| Price band and T2T status | NSE's daily limit (2/5/10/20%) and whether delivery-only (T2T) rules apply. |
| Up/down streak | How many days in a row the stock has moved in the same direction. |
| Market mood | Nifty 50's move today and its distance from its 50-day average. |
| Fear index (India VIX) | Market fear level and how fast it changed over 5 days. |
| Day of the week | Some weekdays behave differently. |

_Also recorded for every buy (not used for picking): P/E ratio, price-to-book, market value, debt-to-equity and return on equity._

### Words used in this report
| Term | Meaning |
|---|---|
| Paper trade | A practice trade with virtual money - no real money is used. |
| Model score | The model's estimate of the next-day return in %, after costs. Higher is better. |
| The bar (threshold) | The minimum model score needed to buy. Raised automatically after a losing streak. |
| Profit target / stop-loss | Automatic sell levels: take profit at +target%, cut the loss at -stop%. |
| Win rate | Share of completed trades that made money. |
| Profit factor | Total gains divided by total losses. Above 1 = profitable; 1.5+ is good. |
| Similar past setups | The 30 most similar situations in history. If they lost money on average, we buy half size. |

_Settings version 1. Paper trades only - not investment advice. Prices assume the ~3:15 pm level; real fills can differ._