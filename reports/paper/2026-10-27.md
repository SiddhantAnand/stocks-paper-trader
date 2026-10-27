# Daily paper-trading report - Tue, 27 Oct 2026
> Practice trading with Rs 1,00,000 of virtual money. No real money is used. Run: 2026-10-07 to 2026-12-02.

## Today in one line
**Bought 0 stock(s), sold 2 for -Rs 332.**

## Scoreboard (main strategy)
| Measure | Value |
|---|---|
| Portfolio value | **Rs 1,00,859** |
| Today's change | +Rs 428 (▲ +0.43%) |
| Total profit / loss since 2026-10-07 | **+Rs 859** (▲ +0.86%) |
| Trades completed | 5 (3 wins, 2 losses) |
| Win rate | 60% (expected about 55.6%) |
| Average result per trade | ▼ -0.26% (expected about ▲ +0.85%) |
| Profit factor | 0.88 (expected about 1.73) |
| Stocks held now | 1 of 3 slots |
| Cash available | Rs 83,813 |
| Evidence so far | 5 of ~80 trades needed for a reliable verdict |

## What happened today
### Sold
| Book | Stock | Bought at | Sold at | Result | Profit / loss | Why it was sold |
|---|---|---|---|---|---|---|
| lookalike | **J&KBANK** | 117.17 | 121.86 | ▲ +3.65% | +Rs 1,190 | Hit the profit target |
| lookalike | **PWL** | 124.62 | 129.60 | ▲ +3.65% | +Rs 1,186 | Hit the profit target |
| main | **SWIGGY** | 185.75 | 190.00 | ▲ +1.94% | +Rs 324 | Holding period ended - sold at about 3:15 pm |
| main | **RAIN** | 205.68 | 202.35 | ▼ -1.97% | -Rs 656 | Holding period ended - sold at about 3:15 pm |
| shadow | **SWIGGY** | 185.75 | 190.00 | ▲ +1.94% | +Rs 454 | Holding period ended - sold at about 3:15 pm |

### Bought
| Book | Stock | Price | Amount | Why |
|---|---|---|---|---|
| shadow | **SURYAROSNI** | 216.00 | Rs 23,544 | moved +8.2% today and closed near the day's high; volume 1.0x normal; downtrend; RSI 54; model score +0.53 (bar 1.0); similar past setups averaged -0.74%; bought at reduced size; shadow: score bar 0.4, up to 2 stocks, hold 1 day(s), target +4.0%, stop-loss -3.0% |

## Stocks we're holding
| Book | Stock | Bought on | Buy price | Latest | Change | Sell if it reaches | Sell if it falls to |
|---|---|---|---|---|---|---|---|
| main | **KABRAEXTRU** | 2026-10-26 | 705.00 | 741.15 | ▲ +5.13% | 733.20 (profit target) | 683.85 (stop-loss) |
| lookalike | **SWANDEF** | 2026-10-26 | 2,576.40 | 2,651.70 | ▲ +2.92% | 2,679.46 (profit target) | 2,499.11 (stop-loss) |
| shadow | **KABRAEXTRU** | 2026-10-26 | 705.00 | 741.15 | ▲ +5.13% | 733.20 (profit target) | 683.85 (stop-loss) |
| shadow | **SURYAROSNI** | 2026-10-27 | 216.00 | 213.47 | ▼ -1.17% | 224.64 (profit target) | 209.52 (stop-loss) |

_Anything not sold by target or stop-loss is sold at about 3:15 pm on the next trading day (2 days for T2T stocks)._

## Today's market check
| Measure | Value |
|---|---|
| Nifty 50 | 22,750 (▼ -0.02%) |
| Market fear (India VIX) | 16.4 - nervous (below 15 calm, 15-20 nervous, above 20 fearful) |
| Stocks scanned | 1,019 |
| Moved 3% or more today | 164 |
| Scored above the bar (1.0) | 0 |

## Top candidates the model looked at
| Stock | Today's move | Model score | Decision |
|---|---|---|---|
| SURYAROSNI | ▲ +8.17% | +0.53 | Skipped - score below the bar |
| SBFC | ▲ +7.43% | +0.51 | Skipped - score below the bar |
| ENTERO | ▲ +7.09% | +0.49 | Skipped - score below the bar |
| SUDEEPPHRM | ▲ +4.17% | +0.45 | Skipped - score below the bar |
| SARDAEN | ▲ +3.12% | +0.43 | Skipped - score below the bar |
| URBANCO | ▲ +5.90% | +0.43 | Skipped - score below the bar |
| CEMPRO | ▲ +6.47% | +0.42 | Skipped - score below the bar |
| BLACKBUCK | ▲ +4.78% | +0.40 | Skipped - score below the bar |

## How the model is learning
- Retrained tonight on **54,059** past setups, including every setup that finished today. Recent data counts more.
- The bar to buy is **1.0** and position size is **100%**. Both tighten automatically after a losing streak and relax after a winning one.
- Prediction check: of 1265 past predictions, stocks above the bar averaged ▲ +0.25% next day vs ▼ -1.08% for the rest.

## Experiments running alongside
| Book | Value | Total profit / loss | Trades | What it tests |
|---|---|---|---|---|
| lookalike | Rs 1,01,039 | +Rs 1,039 | 5 | Experiment: buys the most similar-looking stock to each main pick, to test whether 'similar stocks' also work. |
| shadow | Rs 95,668 | -Rs 4,332 | 5 | Practice account: settings found by the weekly self-tuning. They replace the main settings automatically if they make more money over 20 trades. |

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