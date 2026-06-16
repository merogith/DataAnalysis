# DASHBOARD GUIDE — Project 3 (Tableau **and** Power BI)

A complete, click-by-click guide for someone who has **never** opened these tools.
⭐ **Recommended for this project: Tableau Public** — it's free and gives you a public link
you can paste straight into your résumé/portfolio.

## The files to load (in `dashboard/`)
| File | Grain (one row = …) | Use it for |
|---|---|---|
| `fact_market_monthly.csv` | one **month** of market data | the time-series charts (the core) |
| `dim_year.csv` | one **calendar year** (summary) | KPI cards & year-level bars |
| `dim_sector.csv` | one **GICS sector** of today's index | the "what's in the index" treemap |

**How they relate:** `fact_market_monthly.year` links to `dim_year.year` (many months → one year).
`dim_sector` is standalone (a snapshot of today's index). In both tools you create a relationship
by dragging `year` to `year`.

### Column dictionary (`fact_market_monthly.csv`)
`month` (date) · `sp500_nominal` · `sp500_real` (inflation-adjusted) · `cape` (valuation) ·
`vix` (fear gauge) · `gold_price` · `rate_10y` · `sp_return_m` (monthly %) · `real_return_m` ·
`volatility_12m` · `drawdown` (% below peak) · `year` · `decade`.

---

## The dashboard's one headline insight
> **"The market is near its most expensive in history (top 5% CAPE), and history says that means
> below-average returns ahead."** Every chart should support that story.

---

## Build it in Tableau Public (recommended)
1. **Install** Tableau Public (free) from tableau.com/products/public and create a free account.
2. **Connect:** open Tableau Public → **Connect → Text file** → choose `fact_market_monthly.csv`.
   On the **Data Source** tab, drag in `dim_year.csv` and drop it next to the first table; in the
   relationship pop-up pick `year` = `year`. Add `dim_sector.csv` as a separate table.
3. **Check types:** Tableau should read `month` as a Date and the rest as numbers (a `#` icon).
   If `month` shows as text, click its icon → **Date**.
4. **Build these 5 charts** (each on a new sheet — the tab marked with the small chart icon at the
   bottom):

   - **KPI card — Current CAPE.** Drag `cape` to **Text**. Click the measure → **Measure → Maximum**
     won't help; instead create a calculated field **Latest CAPE** (Analysis → Create Calculated
     Field): `WINDOW_MAX(LAST()==0)` is fiddly — simplest beginner route: filter `month` to the
     latest month (drag `month` to Filters → choose the most recent), then drop `cape` on **Text**.
   - **Line — Real market over time.** Drag `month` to **Columns**, `sp500_real` to **Rows**.
     Right-click the vertical axis → **Logarithmic** (because it grows exponentially).
   - **Line — Valuation (CAPE) over time** with an average line. Drag `month` to Columns, `cape` to
     Rows. From the **Analytics** tab (top-left), drag **Average Line** onto the chart.
   - **Scatter — does the fear gauge track losses?** `vix` to Columns, `sp_return_m` to Rows;
     set both to **Measure → Average** off (use **Dimension** for month detail by dragging `month`
     to **Detail**). Analytics tab → drag **Trend Line** on.
   - **Treemap — what's in the index today.** Use `dim_sector`: drag `sector` to **Detail**,
     `company_count` to **Size** and **Colour**. Marks card → choose **Treemap**.
5. **Assemble a dashboard:** click the **New Dashboard** icon (bottom). Drag the 5 sheets in.
   Put the KPI card top-left, the two time-series lines across the top, the scatter and treemap
   below.
6. **Add a filter/slicer:** on the dashboard, click the real-price line → the little funnel icon →
   **Use as Filter**, or drag `decade` to the dashboard as a filter so the viewer can focus on an era.
7. **Calculated field you'll want — Drawdown %:** Analysis → Create Calculated Field →
   name `Drawdown %`, formula: `[drawdown] * 100`. Format as a percentage.
8. **Publish:** **File → Save to Tableau Public As…**, sign in, and you get a **public link** —
   put it in your portfolio. 🎉

## Build it in Power BI Desktop
1. **Install** Power BI Desktop (free) from the Microsoft Store.
2. **Get data:** **Home → Get data → Text/CSV** → load all three CSVs (one at a time).
   In **Transform data**, confirm `month` is a *Date* type and the numbers are *Decimal*.
3. **Model relationships:** go to the **Model** view (left rail). Drag `fact_market_monthly[year]`
   onto `dim_year[year]`. Leave `dim_sector` unrelated (it's a snapshot).
4. **Create measures** (right-click the fact table → **New measure**):
   - `Current CAPE = CALCULATE( MAX(fact_market_monthly[cape]), fact_market_monthly[month] = MAX(fact_market_monthly[month]) )`
   - `Worst Drawdown % = MIN(fact_market_monthly[drawdown]) * 100`
   - `Avg Volatility % = AVERAGE(fact_market_monthly[volatility_12m]) * 100`
5. **Build 6 visuals** (click a visual icon in the **Visualizations** pane, then tick fields):
   - **Card:** `Current CAPE`. **Card:** `Worst Drawdown %`.
   - **Line chart:** Axis = `month`, Values = `sp500_real` (right-click the axis → Logarithmic if
     offered, else leave linear).
   - **Line chart:** Axis = `month`, Values = `cape`.
   - **Scatter chart:** X = `vix`, Y = `sp_return_m`, Details = `month`; turn on the **Trend line**
     under the **Analytics** pane (the magnifying-glass icon).
   - **Treemap:** Category = `dim_sector[sector]`, Values = `dim_sector[company_count]`.
6. **Add a slicer:** drop a **Slicer** visual and put `decade` in it so viewers can filter by era.
7. **Save** the `.pbix`. (Public sharing needs a Power BI account; for a free public link, use
   Tableau Public above.)

## Suggested layout (both tools)
```
┌──────────────┬───────────────────────────────────────────────┐
│ KPI: CAPE    │  Line: Real market over time (log)            │
│ KPI: Drawdown│  Line: Valuation (CAPE) with average line     │
├──────────────┴───────────────────────────────────────────────┤
│ Scatter: VIX vs monthly return (trend) │ Treemap: sectors     │
└────────────────────────────────────────┴──────────────────────┘
   Slicer:  [ decade ▼ ]
```
