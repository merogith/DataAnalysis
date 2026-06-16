# DASHBOARD GUIDE — Project 1 (Tableau and Power BI)

A step-by-step guide for someone who hasn't opened these tools before. Tableau Public is free and gives
a shareable public link, which is why it's used for the recommended walkthrough below.

## The files to load (in `dashboard/`)
This is a star schema: one central fact table surrounded by dimension tables.

| File | Grain (one row = …) | Use it for |
|---|---|---|
| `fact_scripts.csv` | one prescription record (doctor · product · month) | the core: KPIs, trends, breakdowns |
| `fact_region_product_monthly.csv` | one region × product × month total | a pre-aggregated trend if you prefer |
| `dim_rep.csv` | one sales rep | slice/colour by rep, the rep leaderboard |
| `dim_hcp.csv` | one doctor (with its segment) | segment analysis, targeting |
| `dim_product.csv` | one product | product names, therapy area, price |
| `dim_region.csv` | one region | region names, market size |

How they relate (the keys):
- `fact_scripts.rep_id` → `dim_rep.rep_id`
- `fact_scripts.hcp_id` → `dim_hcp.hcp_id`
- `fact_scripts.product_id` → `dim_product.product_id`
- `fact_scripts.region_id` → `dim_region.region_id`

You create a relationship by dragging the key from the fact table onto the matching key in each
dimension table (a "many facts → one dimension" link).

### Column dictionary (`fact_scripts.csv`)
`script_id` · `script_month` (date) · `hcp_id` · `rep_id` · `product_id` · `region_id` ·
`script_count` (the number to sum).

### Column dictionary (`dim_hcp.csv`)
`hcp_id` · `specialty` · `region` · `potential_score` (0–100) · `decile` (1–10) · `segment` (0–3) ·
`segment_name` (Champions / Steady mid-tier / High-potential growth / Low priority) ·
`hcp_total_scripts` · `hcp_total_calls`.

---

## The dashboard's headline insight
> Calling doctors is associated with more prescriptions, and a specific 99-doctor "High-potential
> growth" segment is where extra calls should return the most prescriptions. Every chart supports that
> story.

---

## Build it in Tableau Public
1. Install Tableau Public (free) from tableau.com/products/public and create a free account.
2. Connect: open Tableau Public → **Connect → Text file** → choose `fact_scripts.csv`. On the
   **Data Source** tab, drag in `dim_rep.csv`, `dim_hcp.csv`, `dim_product.csv`, `dim_region.csv` one
   at a time; in each relationship pop-up, match the key (e.g. `rep_id` = `rep_id`).
3. Check types: Tableau should read `script_month` as a Date and `script_count` as a number (`#`).
   If `script_month` shows as text, click its icon → **Date**.
4. Build these 5 sheets (each on a new sheet, the tab with the small chart icon at the bottom):

   - **KPI card — Total scripts.** Drag `script_count` to **Text**. It defaults to SUM, which is what
     you want. (Optional: format with thousands separators via the measure's number format.)
   - **Bar — Scripts by region.** Drag `region` (from `dim_region`) to **Columns** and `script_count`
     to **Rows**. Sort descending with the toolbar sort button. Southeast leads.
   - **Bar — Scripts by product.** Drag `product` (from `dim_product`) to **Columns**, `script_count`
     to **Rows**. Cardiplex leads.
   - **Scatter — calls vs scripts (with trend line).** Use `dim_hcp`: drag `hcp_total_calls` to
     **Columns** and `hcp_total_scripts` to **Rows**; drag `hcp_id` to **Detail** so each dot is one
     doctor. Open the **Analytics** tab (top-left) and drag **Trend Line** onto the chart. The upward
     line shows the calls-to-scripts relationship.
   - **Bar/treemap — doctors by segment.** Use `dim_hcp`: drag `segment_name` to **Rows** and
     `COUNT(hcp_id)` (or `Number of Records`) to **Columns**. Colour by `segment_name`.
5. Assemble a dashboard: click the **New Dashboard** icon (bottom). Put the **Total scripts** KPI card
   top-left, the two region/product bars across the top, and the scatter and segment chart below.
6. Add a slicer/filter: drag `region` onto the dashboard as a filter, or right-click the region bar →
   **Use as Filter**, so the viewer can focus on one region.
7. Calculated field — Scripts per call: Analysis → Create Calculated Field, name it `Scripts per Call`,
   formula:
   ```
   SUM([Hcp Total Scripts]) / SUM([Hcp Total Calls])
   ```
   (Use the `dim_hcp` fields.) Drop it on a bar by `segment_name` to show which segment is most
   responsive.
8. Publish: **File → Save to Tableau Public As…**, sign in, and you get a public link for your
   portfolio.

## Build it in Power BI Desktop
1. Install Power BI Desktop (free) from the Microsoft Store.
2. Get data: **Home → Get data → Text/CSV** → load all six CSVs (one at a time). In **Transform data**,
   confirm `script_month` is a *Date* type and `script_count` is a *Whole number*.
3. Model relationships: go to the **Model** view (left rail). Drag `fact_scripts[rep_id]` onto
   `dim_rep[rep_id]`; repeat for `hcp_id`, `product_id`, `region_id` onto their dimension tables. Each
   should create a **many-to-one** relationship (many facts, one dimension).
4. Create measures (right-click `fact_scripts` → **New measure**):
   - `Total Scripts = SUM(fact_scripts[script_count])`
   - `Total Calls = SUM(dim_hcp[hcp_total_calls])`
   - `Scripts per Call = DIVIDE( SUM(dim_hcp[hcp_total_scripts]), SUM(dim_hcp[hcp_total_calls]) )`
   - `HCP Count = DISTINCTCOUNT(dim_hcp[hcp_id])`
5. Build 6 visuals (click a visual icon in the **Visualizations** pane, then tick fields):
   - **Card:** `Total Scripts`. **Card:** `HCP Count`.
   - **Clustered bar:** Axis = `dim_region[region]`, Values = `Total Scripts` (sort descending).
   - **Clustered bar:** Axis = `dim_product[product]`, Values = `Total Scripts`.
   - **Scatter chart:** X = `dim_hcp[hcp_total_calls]`, Y = `dim_hcp[hcp_total_scripts]`,
     Details = `dim_hcp[hcp_id]`; turn on the **Trend line** under the **Analytics** pane.
   - **Clustered bar / treemap:** Axis/Category = `dim_hcp[segment_name]`, Values = `HCP Count`
     (and add a second bar with `Scripts per Call` to show segment responsiveness).
6. Add a slicer: drop a **Slicer** visual and put `dim_region[region]` (or `dim_product[product]`) in it
   so viewers can filter.
7. Save the `.pbix`. (Public sharing needs a Power BI account; for a free public link, use Tableau
   Public above.)

## Suggested layout (both tools)
```
┌──────────────┬───────────────────────────────────────────────┐
│ KPI: Total   │  Bar: Scripts by region (Southeast leads)     │
│   scripts    │  Bar: Scripts by product (Cardiplex leads)    │
│ KPI: #Doctors│                                               │
├──────────────┴───────────────────────────────────────────────┤
│ Scatter: calls vs scripts (trend line) │ Bar: doctors by      │
│   — calls vs scripts                    │   segment + scripts/ │
│                                         │   call (the target)  │
└─────────────────────────────────────────┴──────────────────────┘
   Slicer:  [ region ▼ ]
```

## Headline insight for the dashboard title
> More calls go with more scripts. Focus the next calls on the 99-doctor High-potential Growth segment.
