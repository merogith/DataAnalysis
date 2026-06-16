# DASHBOARD GUIDE — Project 2 (Tableau and Power BI)

A click-by-click guide for someone who has not opened these tools before. Tableau Public is free and produces a shareable public link, so it is a reasonable default for this project.

## The files to load (in `dashboard/`) — a star schema
| File | Grain (one row = …) | Use it for |
|---|---|---|
| `fact_daily_economy.csv` | one calendar day | the time-series core (currency flow, DAU, revenue) |
| `dim_item.csv` | one item | item-balance bars and the price/power scatter |
| `dim_player.csv` | one player | payer rate, spend, retention attributes, slicers |
| `dim_date.csv` | one calendar day (date attributes) | a proper date dimension for filtering |

How they relate (the star):
- `fact_daily_economy[date]` → `dim_date[date]` (many days of facts → one date row). It's 1-to-1 here, but keeping `dim_date` separate is best practice for time filtering.
- `dim_item` and `dim_player` are standalone snapshots (item-level and player-level summaries). You don't need to join them to the fact table for this dashboard; each powers its own visuals. Drag them in as separate tables.

### Column dictionaries
`fact_daily_economy.csv` — `date` · `faucet_coins` (coins minted that day) · `sink_coins` (coins drained, negative) · `dau` (daily active players) · `matches` · `revenue_usd` · `net_coins` (faucet+sink) · `cum_net_coins` (running surplus = the inflation curve) · `sink_recovery_pct` (sinks as % of faucets; ~90–100% is healthy).

`dim_item.csv` — `item_name` · `slot` · `is_premium` · `base_price_soft` · `design_power` · `matches` · `pick_rate_pct` · `win_rate_pct` · `ci_low_pct` / `ci_high_pct` (95% CI) · `p_value` · `verdict` (OVERPOWERED / UNDERPOWERED / balanced).

`dim_player.csv` — `player_id` · `install_date` · `platform` · `country` · `acquisition_channel` · `is_payer` (0/1) · `early_sessions` · `early_matches` · `early_playmin` · `lifetime_usd` · `last_active_day`.

---

## The dashboard's headline insight
> The economy is mildly inflationary and two paid items are overpowered, so the game is drifting toward pay-to-win while half of new players quit on Day 1. Every chart should support that story.

---

## The 6 visuals / KPIs to build (both tools)
1. KPI: Payer rate % — from `dim_player`, `is_payer` averaged.
2. KPI: D7 retention % — share of players with `last_active_day >= 7`.
3. KPI: Sink recovery % — average of `sink_recovery_pct` (how much of minted coin gets drained).
4. Line: daily net currency flow — `net_coins` (and/or `cum_net_coins`) over `date`.
5. Bar: item win rates — `win_rate_pct` per `item_name`, with a reference line at 50%, coloured by `verdict`.
6. Scatter: price vs win rate — `base_price_soft` (or `design_power`) vs `win_rate_pct`, coloured by `is_premium` (the pay-to-win view).

---

## Build it in Tableau Public
1. Install Tableau Public (free) from tableau.com/products/public and create a free account.
2. Connect: open Tableau Public → Connect → Text file → choose `fact_daily_economy.csv`. On the Data Source tab, also bring in `dim_date.csv`, `dim_item.csv`, `dim_player.csv` (drag each onto the canvas). For `fact_daily_economy` ↔ `dim_date`, in the relationship pop-up pick `date` = `date`. Leave `dim_item` and `dim_player` unrelated (separate snapshots).
3. Check types: `date`/`install_date` should show a Date icon; the rest should be `#` (numbers). If `date` reads as text, click its icon → Date.
4. Build each visual on a new sheet (the tab with the small chart icon at the bottom):

   - KPI — Payer rate %. Use `dim_player`. Drag `is_payer` to Text. Click the pill → Measure → Average. Right-click → Format → Percentage. (Average of a 0/1 column = the rate.)
   - KPI — D7 retention %. Create a calculated field (Analysis → Create Calculated Field), name it D7 retained: `IF [last_active_day] >= 7 THEN 1 ELSE 0 END`. Drag it to Text, set to Average, format as %.
   - KPI — Sink recovery %. From `fact_daily_economy`, drag `sink_recovery_pct` to Text → Average.
   - Line — daily net currency flow. From the fact table: `date` (set to continuous day, right-click the pill → Day under the green/exact-date section) to Columns, `net_coins` to Rows. Add a second line for the running surplus by dragging `cum_net_coins` to Rows too (dual axis if you like). Add a zero reference line (Analytics tab → Reference Line).
   - Bar — item win rates. Use `dim_item`: `item_name` to Rows, `win_rate_pct` to Columns; drag `verdict` to Colour. Analytics tab → drag a Constant Line at 50 onto the axis (the fair line). Sort descending.
   - Scatter — price vs win rate (pay-to-win). Use `dim_item`: `base_price_soft` to Columns, `win_rate_pct` to Rows, `is_premium` to Colour, `item_name` to Label.
5. Assemble a dashboard: click the New Dashboard icon (bottom). Put the three KPI cards along the top, the net-flow line and item-balance bar across the middle, and the scatter bottom-right.
6. Add a slicer/filter: drag `platform` (from `dim_player`) onto the dashboard as a filter so the viewer can focus on iOS / Android / Web. You can also add `acquisition_channel`.
7. Useful calculated field — Net flow direction: `IF [cum_net_coins] > 0 THEN "Inflation" ELSE "Deflation" END` — drop on a KPI's colour.
8. Publish: File → Save to Tableau Public As…, sign in, and you get a public link.

## Build it in Power BI Desktop
1. Install Power BI Desktop (free) from the Microsoft Store.
2. Get data: Home → Get data → Text/CSV → load all four CSVs (one at a time). In Transform data, confirm `date`/`install_date` are Date and the numbers are Decimal/Whole.
3. Model relationships (Model view, left rail): drag `fact_daily_economy[date]` onto `dim_date[date]`. Leave `dim_item` and `dim_player` unrelated (snapshots).
4. Create measures (right-click a table → New measure):
   - `Payer Rate % = AVERAGE(dim_player[is_payer]) * 100`
   - `D7 Retention % = DIVIDE( CALCULATE(COUNTROWS(dim_player), dim_player[last_active_day] >= 7), COUNTROWS(dim_player) ) * 100`
   - `D1 Retention % = DIVIDE( CALCULATE(COUNTROWS(dim_player), dim_player[last_active_day] >= 1), COUNTROWS(dim_player) ) * 100`
   - `Sink Recovery % = AVERAGE(fact_daily_economy[sink_recovery_pct])`
   - `Total Revenue = SUM(fact_daily_economy[revenue_usd])`
   - `Overpowered Items = CALCULATE( COUNTROWS(dim_item), dim_item[verdict] = "OVERPOWERED" )`
5. Build 6 visuals (click a visual icon in Visualizations, then tick fields):
   - Card: `Payer Rate %`. Card: `D7 Retention %`. Card: `Sink Recovery %`.
   - Line chart: Axis = `date`, Values = `net_coins` and `cum_net_coins`.
   - Bar chart: Axis = `dim_item[item_name]`, Values = `dim_item[win_rate_pct]`, Legend = `dim_item[verdict]`. Add a constant line at 50 (Analytics pane → magnifying-glass icon).
   - Scatter chart: X = `base_price_soft`, Y = `win_rate_pct`, Legend = `is_premium`, Details = `item_name`.
6. Add a slicer: drop a Slicer visual with `dim_player[platform]` (and optionally `acquisition_channel`).
7. Save the `.pbix`. (Public sharing needs a Power BI account; for a free public link, use Tableau Public above.)

## Suggested layout (both tools)
```
┌───────────────┬───────────────┬───────────────┐
│ KPI: Payer %  │ KPI: D7 ret % │ KPI: Sink rec%│
├───────────────┴───────────────┴───────────────┤
│ Line: daily net currency flow (+ running)      │
├────────────────────────────┬───────────────────┤
│ Bar: item win rates (50%)  │ Scatter: price vs  │
│                            │ win rate (premium) │
└────────────────────────────┴───────────────────┘
   Slicer:  [ platform ▼ ]  [ acquisition_channel ▼ ]
```
