# LEARN — Project 3, explained for a beginner 🎓

*No finance or coding background needed. Read top to bottom.*

## What this project does (in 4 sentences)
This project studies the US stock market using more than 150 years of **real** historical data.
It answers four simple questions: how has the market grown, how risky is it, is it expensive
right now, and do different investments (stocks vs gold) protect each other. It uses basic
statistics to show that **how expensive the market is today** has historically told us
**what returns to expect over the next ten years**. The result is a clear, evidence-based view
an everyday investor could actually use.

## The story of the analysis (why each step, not just what)

1. **Get real data → why:** opinions are cheap; this project is built on actual numbers
   (prices, inflation, valuations) going back to 1871, so the conclusions are grounded in
   evidence, not vibes.
2. **Clean the data → why:** the raw files had a trap — recent months stored `0` where the real
   value simply wasn't reported yet. If we'd believed those zeros, every average would be wrong.
   So we marked them as "missing" instead. We also turned a *daily* fear-index into *monthly*
   numbers so everything lined up on the same calendar.
3. **Explore (EDA) → why:** before any fancy maths, we just *look*. Plotting the market over
   time (after removing inflation) instantly reveals that the real growth rate is modest, and
   plotting the "fear gauge" shows a spike at every crisis. Looking first tells you where to dig.
4. **Analyse deeper → why:** we measured the **worst losses** the market has ever put investors
   through (drawdowns), then ran a real **statistical test**: does today's price level predict
   the next decade's return? It does — and we can show it isn't luck. We also checked whether
   gold and stocks move together (they don't — that's useful).
5. **Conclude → why:** numbers only matter if they change a decision. We turned the findings into
   three concrete actions: expect lower returns, diversify, and automate discipline.

## Glossary (plain-English, one line each)
- **Real (inflation-adjusted):** the value after removing the effect of rising prices — "true"
  buying power, in today's dollars.
- **Return:** the percentage gain or loss over a period.
- **Volatility:** how much returns bounce around — a common way to measure risk.
- **Drawdown:** how far an investment is below its previous highest point (the pain an investor
  feels).
- **CAPE / PE10:** a valuation ratio — price compared with 10 years of average earnings. High =
  expensive.
- **VIX:** the "fear gauge" — a market index that rises when investors expect big swings.
- **Correlation:** a number from −1 to +1 saying whether two things move together (+1), oppositely
  (−1), or unrelated (0).
- **Regression (OLS):** drawing the best straight line through a cloud of points to summarise a
  relationship and measure its strength.
- **R²:** of all the ups and downs, what fraction the line explains (0 = nothing, 1 = everything).
- **p-value:** the chance the pattern is just luck — small (e.g. < 0.05) means "probably real".
- **Window function (SQL):** a database calculation that compares a row with *other* rows — here,
  this year's price vs last year's.

## How to run this yourself (exact steps)
1. Open a terminal in the project folder:
   ```bash
   cd project-3-finance
   ```
2. (First time only) install the tools:
   ```bash
   pip install pandas numpy matplotlib seaborn statsmodels jupyter
   ```
3. (Optional) refresh the real data:
   ```bash
   python data/download_data.py
   ```
4. Open the notebook:
   ```bash
   python -m jupyter notebook analysis.ipynb
   ```
   A browser tab opens. Click **Kernel → Restart & Run All**. Read top to bottom — every chart
   and number regenerates in front of you.

## Questions an interviewer might ask (with suggested answers)
- **"Walk me through this project."** → "I used 150 years of real market data to answer four
  investor questions — trend, risk, valuation, and diversification. The headline finding is a
  statistically significant relationship between how expensive the market is and its next-decade
  returns, which I turned into a concrete, caveated recommendation."
- **"The brief wanted yfinance — why didn't you use it?"** → "The sandbox blocked Yahoo and FRED,
  so I pivoted to GitHub-mirrored versions of the *same* real sources (Shiller, CBOE, LBMA) and
  documented the pivot. I always keep a labelled synthetic fallback so the pipeline never stalls."
- **"How did you handle data quality?"** → "The biggest issue was recent months storing `0` as a
  placeholder for unreported values; I converted those to missing so they couldn't poison the
  averages, and I verified the remaining missing-value pattern matched expectations."
- **"Your model predicts a negative real return — do you believe that?"** → "Not literally. It's a
  simple linear fit extrapolating past the historical CAPE range, so I report it as 'well below
  average' and flagged an out-of-sample backtest as the next step. The *direction* and
  *significance* are robust; the precise point estimate isn't."
- **"What would you do differently with more time?"** → "Add a total-return series including
  dividends, backtest the forecast out-of-sample, and test whether the valuation signal holds
  internationally."

## Talking points (say these out loud)
"My flagship project analyses 150 years of real US market data to answer what an investor actually
cares about: trend, risk, and valuation. The standout result is a statistically significant link
between today's valuation and the next ten years of returns — when the market is expensive, future
returns have historically been lower. I handled real-world data messiness like placeholder zeros
and mismatched frequencies, validated the work by running the notebook end-to-end, and turned it
into a clear recommendation: expect modest returns, diversify, and stay disciplined."
