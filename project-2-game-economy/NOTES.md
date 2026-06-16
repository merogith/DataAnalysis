# NOTES — Project 2 (what failed & how I worked around it)

A running, honest log of problems hit while building this project. Showing this is
deliberate: real analytics work is full of these, and handling them well is the job.

### 1. The public game dataset was not reachable → switched to a synthetic generator
- **What happened:** the natural source for this project would be a public Steam / Kaggle
  F2P telemetry dataset, but those hosts are blocked by this sandbox's network policy
  (`host_not_allowed`); only PyPI and `raw.githubusercontent.com` are reachable, and no
  suitable real game-economy file lives there.
- **How I worked around it:** I built a **reproducible, seeded synthetic generator**
  (`data/generate_data.py`) that produces all six telemetry tables. This is the expected
  path for this brief. The data is clearly **labelled SYNTHETIC** everywhere, and because it's
  seeded (`np.random.default_rng(20260616)`), every number in the notebook is reproducible.
- **Bonus:** generating the data myself let me bake in a *known* ground truth (two overpowered
  items, mild inflation, a D1 cliff) so I could verify the analysis actually *recovers* it.

### 2. `itertuples` silently renamed my internal helper columns
- **What happened:** I stashed two internal columns (`_propensity`, `_install_dt`) on the players
  frame to drive sessions/spend, then iterated with `df.itertuples()`. pandas **renames any
  column starting with an underscore** to a positional name like `_0`, so `r._propensity` raised
  `AttributeError`.
- **Fix:** renamed the helper columns to `prop_` / `install_dt_` (trailing underscore) and dropped
  them before saving. Small gotcha, but a classic one.

### 3. Designing *realistic* synthetic numbers took iteration
- **What happened:** my first generator was too extreme — overpowered items hit 91% win rate, D7
  retention collapsed to 4%, and the payer rate was 20%. None of that is believable.
- **Why it mattered:** a portfolio piece is judged on whether the story is *plausible*. I re-tuned
  the model so the two OP items land at ~59–61%, retention reads D1 47% / D7 18% / D30 4% (a
  realistic curve with a genuine D1 cliff), and the payer rate is ~6% with ARPPU ~$16.
- **Key modelling fix:** I originally let raw item "power" drive win probability *plus* a skill
  term — but in skill-matched PvP, opponents are similar skill, so a *balanced* item should sit at
  **50%**. I rewrote win probability as a direct per-item value centred on 50%, with only the
  deliberately mis-tuned items deviating. That's both more realistic and the correct mental model
  for an item-balance study.

### 4. Mixed timestamp formats in one column
- **What happened:** I intentionally wrote half the session timestamps as ISO
  (`2026-03-04 14:05:00`) and half as US-style (`03/04/2026 02:05 PM`) to mimic a messy export.
  A naive `pd.to_datetime` would choke or mis-parse.
- **Fix:** `pd.to_datetime(..., format="mixed", errors="coerce")` reads both styles row-by-row.
  Documented as cleaning decision #4 in the notebook.

### 5. Statistical vs *practical* significance in the item z-test
- **What happened:** with ~3,000–10,000 matches per item, the proportion z-test flags even tiny
  deviations from 50% as "significant" — so a couple of essentially-fair items (e.g. 51.5% win
  rate) technically test as "overpowered" (p < 0.05).
- **How I handled it:** I kept the honest statistical output but called this out explicitly in the
  notebook and docs — *the two items that matter are the ones with a large effect size* (59–61%),
  not the ones that are 1–2 points off 50%. This is a real, teachable distinction between
  **statistical** and **practical** significance, and a good interview talking point rather than
  something to hide.

### 6. Environment / verification
- The notebook is **built programmatically** (`build_notebook.py`) and then **executed with
  `jupyter nbconvert --execute`**, which is how I verify it runs top-to-bottom with **zero errors**
  (checked programmatically via `nbformat` — no cell has an `error` output) before declaring done.
- Every dashboard CSV is re-opened with pandas to confirm it imports with no index junk.
