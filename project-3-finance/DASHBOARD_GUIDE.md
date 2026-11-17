# Dashboard guide — Project 3 (Tableau and Power BI)

A step-by-step guide for building the dashboard in either tool, written for someone who has not
used them before. Tableau Public is free and produces a public link you can share, so it is a
reasonable default for this project.

## The files to load (in `dashboard/`)
| File | Grain (one row = …) | Use it for |
|---|---|---|
| `fact_market_monthly.csv` | one month of market data | the time-series charts (the core) |
| `dim_year.csv` | one calendar year (summary) | KPI cards and year-level bars |
| `dim_sector.csv` | one GICS sector in the source snapshot | the "what's in the index" treemap |

How they relate: `fact_market_monthly.year` links to `dim_year.year` (many months to one year).
`dim_sector` stands alone as a dated source snapshot of index composition. In both tools you create the
relationship by dragging `year` onto `year`.

### Column dictionary (`fact_market_monthly.csv`)
`month` (date), `sp500_nominal`, `sp500_real` (inflation-adjusted), `cape` (valuation),
`vix` (fear gauge), `gold_price`, `rate_10y`, `sp_return_m` (monthly %), `real_return_m`,
`volatility_12m`, `drawdown` (% below peak), `year`, `decade`.

## The headline the dashboard should make obvious
> In this historical extract, the last valid CAPE is September 2023 (30.8, near the top 5%
> of historical readings). Show that date beside the KPI. This is a historical association,
> not a current-market reading or a forecast.

## Build it in Tableau Public
1. Install Tableau Public (free) from tableau.com/products/public and create a free account.
2. Connect: open Tableau Public, choose **Connect → Text file**, and select
   `fact_market_monthly.csv`. On the **Data Source** tab, drag in `dim_year.csv` next to the first
   table and, in the relationship pop-up, match `year` to `year`. Add `dim_sector.csv` as a
   separate table.
3. Check types: Tableau should read `month` as a Date and the rest as numbers (a `#` icon). If
   `month` shows as text, click its icon and choose **Date**.
4. Build these five charts, each on a new sheet (the tab with the small chart icon at the bottom):
   - Latest valid CAPE (KPI). Filter out null `cape` values first, then keep the most recent
     remaining month. Drop `cape` onto **Text** and place that `month` beside it as the
     “Valuation as of” date. The nominal series extends beyond the last valid valuation.
   - Real market over time (line). Drag `month` to **Columns** and `sp500_real` to **Rows**, then
     right-click the vertical axis and choose **Logarithmic**, since the index grows exponentially.
   - Valuation over time (line) with an average line. Drag `month` to **Columns** and `cape` to
     **Rows**, then from the **Analytics** tab drag **Average Line** onto the chart.
   - VIX vs monthly return (scatter). Put `vix` on **Columns** and `sp_return_m` on **Rows**, drag
     `month` to **Detail**, then from the **Analytics** tab add a **Trend Line**.
   - Sector mix (treemap). Using `dim_sector`, drag `sector` to **Detail** and `company_count` to
     both **Size** and **Colour**, then set the Marks card to **Treemap**.
5. Assemble the dashboard: click the **New Dashboard** icon at the bottom and drag the five sheets
   in. Put the KPI top-left, the two line charts across the top, and the scatter and treemap below.
6. Add a filter: drag `decade` onto the dashboard as a filter, or click a chart and use the funnel
   icon to **Use as Filter**, so a viewer can focus on a single era.
7. Add a calculated field for Drawdown %: choose **Analysis → Create Calculated Field**, name it
   `Drawdown`, and enter `[drawdown]`. Format the fractional value as a percentage exactly once.
8. Publish: choose **File → Save to Tableau Public As…** and sign in. Tableau returns a public link
   you can share.

## Build it in Power BI Desktop
1. Install Power BI Desktop (free) from the Microsoft Store.
2. Get data: choose **Home → Get data → Text/CSV** and load all three CSVs one at a time. In
   **Transform data**, confirm `month` is a Date type and the numbers are Decimal.
3. Model relationships: in the **Model** view, drag `fact_market_monthly[year]` onto
   `dim_year[year]`. Leave `dim_sector` unrelated, since it is a snapshot.
4. Create measures (right-click the fact table, then **New measure**):
   - `Valuation As Of = MAXX(FILTER(fact_market_monthly, NOT ISBLANK(fact_market_monthly[cape])), fact_market_monthly[month])`
   - `Latest Valid CAPE = VAR d = [Valuation As Of] RETURN CALCULATE(MAX(fact_market_monthly[cape]), KEEPFILTERS(fact_market_monthly[month] = d))`
   - `Worst Drawdown = MIN(fact_market_monthly[drawdown])`
   - `Avg Volatility = AVERAGE(fact_market_monthly[volatility_12m])`
   Format Valuation As Of as a date, CAPE as a decimal, and Drawdown/Volatility as Percentage. Do not scale percentages twice. These measures respect the selected time context; keep the as-of date visible.
5. Build six visuals (click a visual icon in the **Visualizations** pane, then tick fields):
   - Card: `Latest Valid CAPE` with `Valuation As Of`. Card: `Worst Drawdown`.
   - Line chart: Axis = `month`, Values = `sp500_real` (set the axis to Logarithmic if offered).
   - Line chart: Axis = `month`, Values = `cape`.
   - Scatter chart: X = `vix`, Y = `sp_return_m`, Details = `month`, then turn on the **Trend line**
     in the **Analytics** pane.
   - Treemap: Category = `dim_sector[sector]`, Values = `dim_sector[company_count]`.
6. Add a slicer: drop a **Slicer** visual and put `decade` in it so viewers can filter by era.
7. Save the `.pbix`. Public sharing needs a Power BI account; for a free public link, use Tableau
   Public as above.

## Snapshot checks

The complete nominal series ends in May 2026; valid real-price/CAPE observations end in
September 2023. Missing returns remain missing. `dashboard/metrics.json` records both dates
and the real-price CAGR, using the valid real-price date interval. `calendar_returns.csv`
contains December-to-December observations only; a partial current year is not a calendar return.
`dim_year.csv` records nominal-year completeness and the number of real-price observations,
so a last-observed value is not mistaken for a complete real year.

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
