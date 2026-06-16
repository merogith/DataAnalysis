# NOTES — Project 3 (what failed & how I worked around it)

A running, honest log of problems hit while building this project. Showing this
is deliberate: real analytics work is full of these, and handling them well is
the job.

### 1. `yfinance` and FRED were blocked by the sandbox network
- **What happened:** the brief asked for `yfinance` (stock prices) and FRED (macro data).
  Both hosts returned `HTTP 403 host_not_allowed` — the environment's network policy
  blocks them. `stooq`, `alphavantage` and `nasdaq` were also blocked.
- **How I worked around it:** I confirmed **GitHub raw** *was* reachable, and that GitHub's
  curated `datasets/` collection mirrors the **same underlying real data**:
  - `datasets/s-and-p-500` → Robert Shiller's monthly S&P 500 series (1871→), the canonical
    long-run market dataset, including CPI, the 10-year rate, real values and CAPE/PE10.
  - `datasets/finance-vix` → the official CBOE VIX, daily since 1990.
  - `datasets/gold-prices` → LBMA gold prices.
  - `datasets/s-and-p-500-companies` → current constituents & sectors.
- **Result:** the project stayed a genuine **REAL-DATA** project. The downloader
  (`data/download_data.py`) also includes a clearly-labelled **synthetic fallback** so the
  pipeline still runs end-to-end if even GitHub is unreachable.

### 2. Recent months stored `0.0` instead of "missing"
- **What happened:** the latest S&P 500 rows had `0.0` for Dividend, Earnings, CPI, the
  interest rate and CAPE. Shiller back-fills these with a reporting lag, so the most recent
  months are placeholders — **not** real zeros.
- **Why it matters:** treating `0.0` as a true value would have produced nonsense (e.g. a CAPE
  of 0, infinite dividend yields) and skewed every average.
- **Fix:** replaced `0.0` with `NaN` (missing) in those columns during cleaning, and verified
  the remaining missing-value counts were exactly what we'd expect (VIX missing before 1990,
  a handful of lagged fundamentals at the very end).

### 3. VIX is daily but everything else is monthly
- **What happened:** the VIX file is daily; the S&P 500 spine is monthly, so a naive join
  would not line up.
- **Fix:** resampled VIX to a **monthly average** (`resample("MS").mean()`) before joining.
  A monthly average is the right summary for a monthly study and avoids over-weighting any
  single noisy day.

### 4. The linear valuation model extrapolates poorly at record-high CAPE
- **What happened:** a simple straight-line (OLS) fit of CAPE → next-10-year return, when
  evaluated at today's near-record CAPE, implies a slightly **negative** real return. A
  straight line keeps going down forever; reality has a floor.
- **How I handled it:** kept the simple, interpretable model (it answers the question and is
  honestly reported with R²/slope/p-value), but **explicitly caveated** the point estimate in
  both the notebook and README as "well below average" rather than a precise figure, and
  compared it to the historical average for context. Listed a proper out-of-sample backtest as
  the next step.

### 5. Environment setup
- Fresh container had **no** data libraries. Installed `pandas, numpy, matplotlib, seaborn,
  scikit-learn, statsmodels, jupyter, nbconvert, yfinance` via pip (PyPI was reachable).
- The notebook was **built programmatically** (`build_notebook.py`) and then **executed with
  `jupyter nbconvert --execute`**, which is how I verify it runs top-to-bottom with zero errors
  before declaring it done.
