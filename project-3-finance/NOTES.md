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

The downloader (`data/download_data.py`) stages all four sources before replacing the data.
A failed fetch leaves the existing inputs in place. The optional `--synthetic` mode marks its
fixtures, and the analysis rejects that marker or an interrupted replacement.

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

### 5. Data and evaluation dates
The last valid CAPE in the saved extract is from September 2023. The nominal price series extends
further. The last regression start point is in 2013 because each observation needs a full decade of
subsequent price data. The case presents the historical relationship and leaves forecasting to a
separate out-of-sample evaluation.

### 6. Environment setup
I worked in a clean Python environment with pandas, numpy, matplotlib, seaborn,
scikit-learn, statsmodels, jupyter, and nbconvert. The notebook is built
programmatically (`build_notebook.py`) and then run with `jupyter nbconvert --execute`, which
confirms it runs top to bottom without errors before the project is considered done.
