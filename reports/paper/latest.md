# Daily paper-trading report - Mon, 09 Nov 2026
> Practice trading with Rs 1,00,000 of virtual money. No real money is used. Run: 2026-10-07 to 2026-12-02.

## Today in one line
**Bought 0 stock(s), sold 3 for +Rs 1,035.**

## Scoreboard (main strategy)
| Measure | Value |
|---|---|
| Portfolio value | **Rs 1,04,810** |
| Today's change | +Rs 1,783 (▲ +1.73%) |
| Total profit / loss since 2026-10-07 | **+Rs 4,810** (▲ +4.81%) |
| Trades completed | 16 (11 wins, 5 losses) |
| Win rate | 69% (expected about 55.6%) |
| Average result per trade | ▲ +1.03% (expected about ▲ +0.85%) |
| Profit factor | 1.91 (expected about 1.73) |
| Stocks held now | 0 of 3 slots |
| Cash available | Rs 1,04,810 |
| Evidence so far | 16 of ~80 trades needed for a reliable verdict |

## What happened today
### Sold
| Book | Stock | Bought at | Sold at | Result | Profit / loss | Why it was sold |
|---|---|---|---|---|---|---|
| main | **HFCL** | 219.61 | 213.00 | ▼ -3.36% | -Rs 576 | Opened below the stop-loss - sold at the open |
| lookalike | **STLTECH** | 757.75 | 688.00 | ▼ -9.55% | -Rs 3,113 | Opened below the stop-loss - sold at the open |
| lookalike | **AEROFLEX** | 483.30 | 502.95 | ▲ +3.72% | +Rs 1,221 | Opened above the profit target - sold at the open |
| shadow | **HFCL** | 219.61 | 213.00 | ▼ -3.36% | -Rs 797 | Opened below the stop-loss - sold at the open |
| main | **KISSHT** | 346.90 | 360.78 | ▲ +3.65% | +Rs 1,254 | Hit the profit target |
| shadow | **KISSHT** | 346.90 | 360.78 | ▲ +3.65% | +Rs 1,735 | Hit the profit target |
| main | **KMEW** | 649.00 | 665.00 | ▲ +2.12% | +Rs 357 | Holding period ended - sold at about 3:15 pm |
| lookalike | **ACE** | 1,167.05 | 1,166.75 | ▼ -0.38% | -Rs 123 | Holding period ended - sold at about 3:15 pm |

## Today's market check
| Measure | Value |
|---|---|
| Nifty 50 | 25,045 (▲ +0.06%) |
| Market fear (India VIX) | 17.4 - nervous (below 15 calm, 15-20 nervous, above 20 fearful) |
| Stocks scanned | 1,051 |
| Moved 3% or more today | 126 |
| Scored above the bar (0.8) | 0 |

## Top candidates the model looked at
| Stock | Today's move | Model score | Decision |
|---|---|---|---|
| SYNGENE | ▲ +4.64% | -0.09 | Skipped - score below the bar |
| LAURUSLABS | ▲ +4.44% | -0.09 | Skipped - score below the bar |
| IGIL | ▲ +5.14% | -0.14 | Skipped - score below the bar |
| SGMART | ▲ +4.91% | -0.19 | Skipped - score below the bar |
| WELSPUNLIV | ▲ +4.76% | -0.20 | Skipped - score below the bar |
| UNIONBANK | ▲ +5.08% | -0.20 | Skipped - score below the bar |
| GROWW | ▲ +3.34% | -0.21 | Skipped - score below the bar |
| BANKBARODA | ▲ +3.79% | -0.22 | Skipped - score below the bar |

## How the model is learning
- Retrained tonight on **55,632** past setups, including every setup that finished today. Recent data counts more.
- The bar to buy is **0.8** and position size is **100%**. Both tighten automatically after a losing streak and relax after a winning one.
- Prediction check: of 2728 past predictions, stocks above the bar averaged ▲ +0.68% next day vs ▼ -0.55% for the rest.

## Experiments running alongside
| Book | Value | Total profit / loss | Trades | What it tests |
|---|---|---|---|---|
| lookalike | Rs 97,320 | -Rs 2,680 | 16 | Experiment: buys the most similar-looking stock to each main pick, to test whether 'similar stocks' also work. |
| shadow | Rs 96,411 | -Rs 3,589 | 17 | Practice account: settings found by the weekly self-tuning. They replace the main settings automatically if they make more money over 20 trades. |

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