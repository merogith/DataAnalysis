# Project 3 — US Stock Market: Trends, Risk & Valuation 📈
**Flagship project · REAL public market data · Python + statistics + SQL**

## Executive summary (for a non-technical reader)
- Using **150+ years of real market data**, this project answers what a long-term investor most wants to know: *where are we, how risky is it, and what should I expect next?*
- After removing inflation, the US market's **price** has grown only **~2.4%/year** — the giant headline numbers are mostly inflation plus reinvested dividends. Expectations should be set accordingly.
- **Risk is recurring, not rare:** the market has been as much as **−81% below its peak** (1930s) in real terms, and the "fear gauge" (VIX) spikes at *every* crisis.
- **Valuation predicts returns — and I proved it statistically.** Higher starting valuation (CAPE) has reliably been followed by **lower** 10-year returns (p ≈ 0.000000…, i.e. not luck). Today's valuation sits in the **top 5%** of all history.
- **Gold is a genuine diversifier:** its correlation with stocks is ≈ 0, so it cushions the deep drawdowns history guarantees will return.
- **Bottom line:** plan for *below-average* real returns over the next decade, diversify deliberately, and automate discipline — the biggest risk is behavioural (selling at the bottom).

> **Data label: REAL.** Sources: Robert Shiller's S&P 500 dataset, CBOE VIX, LBMA gold — all public, mirrored on GitHub's curated `datasets/` collection (the brief's `yfinance`/FRED were blocked by the sandbox network; see `NOTES.md`).

---

## Problem
A long-term investor needs a clear, evidence-based read on **trend, risk, valuation, and diversification** — not marketing, and not gut feel. The four business questions:
1. What is the long-run **real** (inflation-adjusted) trajectory, and where are we today?
2. How **risky** is the market now vs history (volatility, VIX, worst-case drawdowns)?
3. Is the market **expensive**, and does valuation actually predict future returns?
4. Do stocks, gold, and bonds **diversify** each other?

## Approach
1. **Sourced real data** with a reproducible script (`data/download_data.py`) — Shiller monthly S&P 500 (1871→), daily VIX (1990→), monthly gold, current index constituents.
2. **Cleaned & documented every decision** — most importantly, recent months store `0.0` as a *placeholder* for not-yet-reported fundamentals; treating those as real zeros would have corrupted the analysis, so they became missing values.
3. **EDA** — long-run real trend (log scale), valuation history, return distribution, the VIX.
4. **Deeper analysis** — drawdown ("underwater") analysis, a real **OLS regression** of CAPE vs the *following* 10-year real return, and a cross-asset **correlation** matrix.
5. **SQL (SQLite)** — a `LAG` **window function** to rank the best/worst calendar years.
6. **Key findings + a concrete, caveated recommendation.**

## Key findings (with charts)

**1. The real trend is steady but modest — inflation does most of the "growth".**
![Real vs nominal S&P 500](charts/01_real_trend.png)

**2. Valuation has historically predicted the next decade's returns (the flagship result).** Each dot is a month; the downward line means *higher price paid → lower future return*. R² = 0.11, slope highly significant (p ≈ 1e-40). Today's CAPE (gold line) is near the all-time high.
![CAPE vs forward 10-year return](charts/05_cape_vs_forward_return.png)

**3. Deep drawdowns are a feature of the market, not a bug.** The worst real loss reached −81%.
![Drawdowns](charts/04_drawdowns.png)

| Metric (latest real data) | Value |
|---|---|
| Long-run **real** price growth | ~2.4% / year |
| Current CAPE valuation | **30.8** — higher than **95%** of all months since 1881 |
| Model-implied next-10y real return | **well below** the 2.3% historical average |
| Worst real drawdown in history | **−81%** (trough June 1932) |
| Stocks ↔ Gold correlation | **≈ 0** (genuine diversifier) |
| Worst / best calendar years | 1931 (−46%) / 1933 (+46%) |

## Recommendation
- **Set realistic expectations** — plan around below-average real returns given today's top-5% valuation.
- **Diversify deliberately** — pair equities with low-correlation assets (gold, bonds) to soften inevitable drawdowns.
- **Automate discipline** — dollar-cost-average and pre-commit to rebalancing; the data shows the real danger is selling during the long underwater stretches.

## What I'd do next
- Build a **total-return** series (price + reinvested dividends) for a truer long-run figure.
- Add an **out-of-sample backtest** with confidence bands around the valuation forecast.
- Test whether the valuation signal **travels** to sectors and international markets.

---

## Repository contents
| Path | What it is |
|---|---|
| `analysis.ipynb` | The full, runnable analysis (executed top-to-bottom, outputs included) |
| `data/download_data.py` | Reproducible real-data downloader (+ synthetic fallback) |
| `data/raw_*.csv` | The downloaded real datasets |
| `charts/` | All generated figures |
| `dashboard/` | BI-ready CSVs (`fact_market_monthly`, `dim_year`, `dim_sector`) |
| `DASHBOARD_GUIDE.md` | Step-by-step Tableau **and** Power BI build guide |
| `LEARN.md` | Beginner-friendly walkthrough, glossary & interview Q&A |
| `NOTES.md` | What failed and how I worked around it |

## How to run it
```bash
cd project-3-finance
python data/download_data.py          # refresh the real data (optional)
python -m jupyter notebook analysis.ipynb   # open and Run-All
```
See `LEARN.md` → "How to run this yourself" for a zero-experience version.
