# NOTES — Project 3: issues encountered and how I resolved them

A record of the problems that came up while building this project and what I did about each one.

### 1. Sourcing the data from public mirrors
I pulled the series from GitHub's `datasets/` collection, which mirrors the same underlying real
data exposed by yfinance and FRED and is openly downloadable:

- `datasets/s-and-p-500` — Robert Shiller's monthly S&P 500 series from 1871, including CPI, the
  10-year rate, real values, and CAPE/PE10.
- `datasets/finance-vix` — the CBOE VIX, daily since 1990.
- `datasets/gold-prices` — LBMA gold prices.
- `datasets/s-and-p-500-companies` — current constituents and sectors.

Using these mirrors kept the project on real data. The downloader
(`data/download_data.py`) also includes a labelled synthetic fallback so the pipeline still runs
if a source is unreachable.

### 2. Recent months stored `0.0` instead of missing
The latest S&P 500 rows had `0.0` for dividends, earnings, CPI, the interest rate, and CAPE.
Shiller backfills these on a lag, so the most recent months are placeholders rather than true
zeros. Treating them as real values would have produced nonsense (a CAPE of 0, infinite dividend
yields) and skewed every average. I replaced those zeros with missing values during cleaning and
checked that the remaining missing-value counts matched what I expected: VIX absent before 1990,
and a handful of lagged fundamentals at the very end.

### 3. VIX is daily but everything else is monthly
The VIX file is daily while the S&P 500 spine is monthly, so a direct join would not align. I
resampled VIX to a monthly average (`resample("MS").mean()`) before joining. A monthly average is
the right summary for a monthly study and avoids over-weighting any single noisy day.

### 4. The "p ≈ 1e-40" on the valuation regression was misleading — overlapping windows
My first version regressed each month's CAPE on the *following* 10 years of real return and
reported the ordinary OLS p-value, which came out around 1e-40. That number is not trustworthy:
consecutive 10-year windows overlap by 119 of their 120 months, so the ~1,593 observations are
heavily autocorrelated and nowhere near independent. The effective sample is closer to the number
of non-overlapping decades — about 13 in 150 years — and ordinary standard errors are far too
small. I corrected this two ways and report all three side by side in the notebook: (a) Newey-West
(HAC) standard errors with a 120-month lag, which give p ≈ 0.003; and (b) a regression on only
non-overlapping decades (every 120th month, n = 14), which gives p ≈ 0.27 — not significant on its
own. The negative relationship is real and economically sensible, but I now describe it as a
*moderate, suggestive* signal rather than something "statistically proven."

### 5. "Today's" valuation is actually about 2023, and the fit ends in 2013
Two date issues that I now flag explicitly. First, because Shiller's real-price/CAPE columns lag
the raw price index by ~2-3 years, the most recent *valid* CAPE is dated September 2023 even though
the price series runs to 2026 — so I label every "today" valuation figure with its real date rather
than implying it is current. Second, the forward-return regression needs the *following* decade to
compute its outcome, so the last usable start-point is ~2013; today's high-CAPE regime is outside
the range the model was fit on, which makes the forward estimate an out-of-range extrapolation. I
also treat the most recent mirrored gold and nominal-price values as indicative rather than
authoritative, since the tail of a public mirror can run ahead of confirmed data.

### 6. The linear valuation model extrapolates poorly at record-high CAPE
A simple straight-line (OLS) fit of CAPE against the next ten years' return implies a slightly
negative real return when evaluated at today's near-record CAPE. A straight line keeps falling
indefinitely, while real returns have a practical floor. I kept the simple, interpretable model
because it answers the question, but I labelled the point estimate as "below average" rather than a
precise figure and compared it with the historical average for context. A proper out-of-sample
backtest with block-bootstrap bands is listed as the next step.

### 5. Environment setup
I worked in a clean Python environment with pandas, numpy, matplotlib, seaborn,
scikit-learn, statsmodels, jupyter, and nbconvert. The notebook is built
programmatically (`build_notebook.py`) and then run with `jupyter nbconvert --execute`, which
confirms it runs top to bottom without errors before the project is considered done.
