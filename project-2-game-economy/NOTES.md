# NOTES — Project 2 (issues encountered and how I resolved them)

A log of the problems I hit while building this project and what I did about each.

### 1. The public game dataset was not reachable, so I switched to a synthetic generator
The natural source for this project would be a public Steam or Kaggle F2P telemetry dataset, but those hosts are blocked by this sandbox's network policy (`host_not_allowed`). Only PyPI and `raw.githubusercontent.com` are reachable, and no suitable real game-economy file lives there.

I built a reproducible, seeded generator (`data/generate_data.py`) that produces all six telemetry tables. The data is labelled SYNTHETIC throughout, and because it's seeded (`np.random.default_rng(20260616)`), every number in the notebook reproduces. Generating it myself also let me bake in a known ground truth (two overpowered items, mild inflation, a D1 drop), so I could check that the analysis actually recovers it.

### 2. `itertuples` silently renamed my internal helper columns
I stashed two internal columns (`_propensity`, `_install_dt`) on the players frame to drive sessions and spend, then iterated with `df.itertuples()`. pandas renames any column starting with an underscore to a positional name like `_0`, so `r._propensity` raised `AttributeError`. I renamed the helpers to `prop_` and `install_dt_` (trailing underscore) and dropped them before saving.

### 3. Designing realistic synthetic numbers took iteration
My first generator was too extreme: overpowered items hit 91% win rate, D7 retention collapsed to 4%, and the payer rate was 20%, none of which is believable. A portfolio piece is judged on whether the story is plausible, so I re-tuned the model. The two OP items now land at ~59–61%, retention reads D1 47% / D7 18% / D30 4%, and the payer rate is ~6% with ARPPU ~$16.

The key modelling fix: I originally let raw item power drive win probability plus a skill term, but in skill-matched PvP, opponents are similar skill, so a balanced item should sit at 50%. I rewrote win probability as a direct per-item value centred on 50%, with only the deliberately mis-tuned items deviating. That is both more realistic and the correct mental model for an item-balance study.

### 4. Mixed timestamp formats in one column
I intentionally wrote half the session timestamps as ISO (`2026-03-04 14:05:00`) and half as US-style (`03/04/2026 02:05 PM`) to mimic a messy export. A naive `pd.to_datetime` would choke or mis-parse. The fix was `pd.to_datetime(..., format="mixed", errors="coerce")`, which reads both styles row-by-row. It's documented as cleaning decision #4 in the notebook.

### 5. Statistical vs practical significance in the item z-test
With ~3,000–10,000 matches per item, the proportion z-test flags even tiny deviations from 50% as significant, so a couple of essentially-fair items (for example a 51.5% win rate) technically test as overpowered (p < 0.05). I kept the honest statistical output but flagged this in the notebook and docs: the items worth acting on are the ones with a large effect size (59–61%), not the ones sitting 1–2 points off 50%. The distinction between statistical and practical significance matters here, so I surfaced it rather than hiding it.

### 6. Environment and verification
The notebook is built programmatically (`build_notebook.py`) and then executed with `jupyter nbconvert --execute`, which is how I confirm it runs top-to-bottom with zero errors (checked via `nbformat`, no cell has an `error` output) before calling it done. Every dashboard CSV is re-opened with pandas to confirm it imports with no index junk.
