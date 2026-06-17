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

### 4. The linear valuation model extrapolates poorly at record-high CAPE
A simple straight-line (OLS) fit of CAPE against the next ten years' return implies a slightly
negative real return when evaluated at today's near-record CAPE. A straight line keeps falling
indefinitely, while real returns have a practical floor. I kept the simple, interpretable model
because it answers the question and reports its R², slope, and p-value honestly, but I labelled
the point estimate as "below average" rather than a precise figure and compared it with the
historical average for context. A proper out-of-sample backtest is listed as the next step.

### 5. Environment setup
I worked in a clean Python environment with pandas, numpy, matplotlib, seaborn,
scikit-learn, statsmodels, jupyter, and nbconvert. The notebook is built
programmatically (`build_notebook.py`) and then run with `jupyter nbconvert --execute`, which
confirms it runs top to bottom without errors before the project is considered done.
