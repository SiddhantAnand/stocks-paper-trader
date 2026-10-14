# Daily paper-trading report - Wed, 14 Oct 2026
> Practice trading with Rs 1,00,000 of virtual money. No real money is used. Run: 2026-10-07 to 2026-12-02.

## Today in one line
**Bought 1 stock(s), sold 2 for +Rs 1,784.**

## Scoreboard (main strategy)
| Measure | Value |
|---|---|
| Portfolio value | **Rs 1,01,760** |
| Today's change | +Rs 273 (▲ +0.27%) |
| Total profit / loss since 2026-10-07 | **+Rs 1,760** (▲ +1.76%) |
| Trades completed | 2 (2 wins, 0 losses) |
| Win rate | 100% (expected about 55.6%) |
| Average result per trade | ▲ +3.65% (expected about ▲ +0.85%) |
| Profit factor | - (expected about 1.73) |
| Stocks held now | 1 of 3 slots |
| Cash available | Rs 85,116 |
| Evidence so far | 2 of ~80 trades needed for a reliable verdict |

## What happened today
### Sold
| Book | Stock | Bought at | Sold at | Result | Profit / loss | Why it was sold |
|---|---|---|---|---|---|---|
| main | **SIGMAADV** | 961.70 | 1,000.17 | ▲ +3.65% | +Rs 1,194 | Hit the profit target |
| lookalike | **BODALCHEM** | 177.77 | 172.44 | ▼ -3.35% | -Rs 1,113 | Hit the stop-loss (limits the loss) |
| main | **E2E** | 735.55 | 764.97 | ▲ +3.65% | +Rs 591 | Hit the profit target |
| lookalike | **SWANDEF** | 2,931.10 | 2,939.00 | ▼ -0.08% | -Rs 26 | Holding period ended - sold at about 3:15 pm |

### Bought
| Book | Stock | Price | Amount | Why |
|---|---|---|---|---|
| main | **STLTECH** | 926.00 | Rs 16,668 | moved -3.9% today and closed mid-range; volume 0.7x normal; uptrend; RSI 56; model score +1.08 (bar 1.0); similar past setups averaged -0.37%; bought at reduced size |
| lookalike | **AHCL** | 29.04 | Rs 32,931 | moved -5.0% today and closed near the day's low; volume 0.2x normal; uptrend; RSI 57; model score -3.61 (bar 1.0); lookalike of STLTECH (distance 7.67) |

## Stocks we're holding
| Book | Stock | Bought on | Buy price | Latest | Change | Sell if it reaches | Sell if it falls to |
|---|---|---|---|---|---|---|---|
| main | **STLTECH** | 2026-10-14 | 926.00 | 924.65 | ▼ -0.15% | 963.04 (profit target) | 898.22 (stop-loss) |
| lookalike | **AHCL** | 2026-10-14 | 29.04 | 29.04 | +0.00% | 30.20 (profit target) | 28.17 (stop-loss) |

_Anything not sold by target or stop-loss is sold at about 3:15 pm on the next trading day (2 days for T2T stocks)._

## Today's market check
| Measure | Value |
|---|---|
| Nifty 50 | 22,623 (▼ -0.44%) |
| Market fear (India VIX) | 14.7 - calm (below 15 calm, 15-20 nervous, above 20 fearful) |
| Stocks scanned | 1,022 |
| Moved 3% or more today | 83 |
| Scored above the bar (1.0) | 1 |

## Top candidates the model looked at
| Stock | Today's move | Model score | Decision |
|---|---|---|---|
| STLTECH | ▼ -3.89% | +1.08 | **Bought** |
| LTTS | ▲ +5.74% | +0.24 | Skipped - score below the bar |
| UTLSOLAR | ▲ +3.99% | +0.14 | Skipped - score below the bar |
| ABDL | ▲ +3.64% | +0.09 | Skipped - score below the bar |
| CSBBANK | ▲ +3.64% | +0.05 | Skipped - score below the bar |
| MFSL | ▼ -3.20% | -0.02 | Skipped - score below the bar |
| CRAFTSMAN | ▲ +3.08% | -0.02 | Skipped - score below the bar |
| JWL | ▼ -3.22% | -0.04 | Skipped - score below the bar |

## How the model is learning
- Retrained tonight on **52,922** past setups, including every setup that finished today. Recent data counts more.
- The bar to buy is **1.0** and position size is **100%**. Both tighten automatically after a losing streak and relax after a winning one.
- Prediction check: of 179 past predictions, stocks above the bar averaged ▲ +3.65% next day vs ▼ -0.30% for the rest.

## Experiments running alongside
| Book | Value | Total profit / loss | Trades | What it tests |
|---|---|---|---|---|
| lookalike | Rs 98,861 | -Rs 1,139 | 2 | Experiment: buys the most similar-looking stock to each main pick, to test whether 'similar stocks' also work. |

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