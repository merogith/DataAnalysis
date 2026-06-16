# Data Analyst Portfolio 📊

Three complete, end-to-end analytics projects — from raw, messy data to a clear business
recommendation — plus ready-to-build BI dashboards. Each project shows the full workflow a
data analyst does on the job: **define the question → clean the data → explore → analyse with
statistics/ML → communicate a decision.**

> 👋 **New here?** Read **[GETTING_STARTED.md](GETTING_STARTED.md)** first — it assumes zero
> experience and explains the folders, the tools, and the order to read things.

---

## The three projects

### ⭐ [Project 3 — US Stock Market: Trends, Risk & Valuation](project-3-finance/) · *flagship, REAL data*
**Hook:** *150 years of real market data — where are we, how risky is it, and what should we expect next?*
**Key result:** market valuation (CAPE) **statistically predicts** the next decade's returns
(p ≈ 1e-40); today's valuation sits in the **top 5%** of all history, implying below-average
returns ahead. Worst-ever real drawdown: **−81%**. Gold's correlation with stocks ≈ **0** (a real diversifier).
**Tech:** Python · pandas · **statsmodels** (OLS regression) · matplotlib/seaborn · **SQLite** (window functions) · real data (Shiller S&P 500, CBOE VIX, gold)
→ [Notebook](project-3-finance/analysis.ipynb) · [README](project-3-finance/README.md) · [Dashboard guide](project-3-finance/DASHBOARD_GUIDE.md) · [Learn](project-3-finance/LEARN.md)

### [Project 1 — Pharmaceutical CRM Sales Analytics](project-1-pharma-crm/) · *synthetic data*
**Hook:** *Which doctors should the sales team prioritise, and do sales calls actually drive prescriptions?*
**Key result:** sales calls correlate with prescriptions (**r = 0.49, p = 1.5e-37**); each extra
call/year is worth **~5.5 more scripts**. **KMeans** grouped 600 doctors into 4 segments and
surfaced a **99-doctor high-potential target list** for re-allocating effort. Top 20% of doctors drive **37%** of volume.
**Tech:** Python · pandas · **scikit-learn** (KMeans clustering) · statsmodels (OLS) · matplotlib/seaborn · **SQLite** (`RANK() OVER`)
→ [Notebook](project-1-pharma-crm/analysis.ipynb) · [README](project-1-pharma-crm/README.md) · [Dashboard guide](project-1-pharma-crm/DASHBOARD_GUIDE.md) · [Learn](project-1-pharma-crm/LEARN.md)

### [Project 2 — Free-to-Play Game Economy & Balance](project-2-game-economy/) · *synthetic data*
**Hook:** *Is the in-game economy balanced, which items are overpowered, and what drives players to stay and pay?*
**Key result:** the economy runs a **mild inflation** (sinks recover only **63%** of minted coins);
**Phoenix Blade (61% win rate)** is overpowered and **pay-to-win**; retention shows a textbook
**Day-1 cliff (47% → 18% → 4%** at D1/D7/D30); a **logistic-regression** payer model predicts
spenders with **AUC 0.80**.
**Tech:** Python · pandas · **scikit-learn** (logistic regression) · proportion z-tests · matplotlib/seaborn · **SQLite** (window functions)
→ [Notebook](project-2-game-economy/analysis.ipynb) · [README](project-2-game-economy/README.md) · [Dashboard guide](project-2-game-economy/DASHBOARD_GUIDE.md) · [Learn](project-2-game-economy/LEARN.md)

---

## Skills demonstrated
| Skill | Where to see it |
|---|---|
| **Data cleaning & wrangling** | Every project documents each cleaning decision in a table (dupes, missing values, inconsistent formats, impossible values) |
| **SQL** | A SQLite query with **window functions** in every project (ranking, running totals) |
| **Exploratory data analysis (EDA)** | Clear, labelled visualisations across all three |
| **Statistics** | OLS regression with p-values/R² (P1, P3), proportion z-tests & confidence intervals (P2) |
| **Machine learning** | KMeans segmentation (P1), logistic-regression prediction (P2) |
| **Data visualisation** | 20+ professional charts (matplotlib/seaborn), consistent palettes |
| **BI dashboards** | Star-schema CSV exports + click-by-click Tableau **and** Power BI guides |
| **Business communication** | Each README opens with an executive summary and ends with an actionable recommendation |

---

## How to view / run any project
```bash
# 1) install the tools (once)
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels jupyter

# 2) open a project's notebook
cd project-3-finance
python3 -m jupyter notebook analysis.ipynb     # then: Kernel → Restart & Run All
```
The notebooks are saved **with their outputs**, so you can also just read them on GitHub
without running anything. Full beginner instructions: **[GETTING_STARTED.md](GETTING_STARTED.md)**.

A simple web version of this landing page lives in **[portfolio/index.html](portfolio/index.html)**.

---

## A note on data honesty
- **Project 3 uses real, public market data** (Shiller / CBOE / LBMA). The brief asked for
  `yfinance`/FRED; those were blocked by the sandbox network, so I pivoted to GitHub-mirrored
  copies of the **same** real sources and documented it (see the project's `NOTES.md`).
- **Projects 1 & 2 use synthetic data**, clearly labelled, generated by reproducible seeded
  scripts that inject realistic messiness — because real pharma CRM and game telemetry are proprietary.
