# NOTES — Project 2 (issues encountered and how I resolved them)

A log of the problems I hit while building this project and what I did about each.

### 1. Why synthetic data here
Real F2P telemetry (player sessions, in-game purchases, match logs) is proprietary and privacy-sensitive, and public game-economy datasets at this level of detail are hard to come by. Rather than stretch a thin public file, I built my own data so the economy, item balance and monetization questions all had something realistic to work with.

I built a reproducible, seeded generator (`data/generate_data.py`) that produces all six telemetry tables. The data is labelled SYNTHETIC throughout, and because it's seeded (`np.random.default_rng(20260616)`), every number in the notebook reproduces. Generating it myself also let me bake in a known ground truth (two overpowered items, mild inflation, a D1 drop), so I could check that the analysis actually recovers it.

### 2. `itertuples` silently renamed my internal helper columns
I stashed two internal columns (`_propensity`, `_install_dt`) on the players frame to drive sessions and spend, then iterated with `df.itertuples()`. pandas renames any column starting with an underscore to a positional name like `_0`, so `r._propensity` raised `AttributeError`. I renamed the helpers to `prop_` and `install_dt_` (trailing underscore) and dropped them before saving.

### 3. Designing realistic synthetic numbers took iteration
My first generator was too extreme: overpowered items hit 91% win rate, D7 retention collapsed to 4%, and the payer rate was 20%, none of which is believable. A portfolio piece is judged on whether the story is plausible, so I re-tuned the model. The two OP items now land at ~59–61%, retention reads D1 47% / D7 18% / D30 4%, and the payer rate is ~6% with ARPPU ~$16.

The key modelling fix: I originally let raw item power drive win probability plus a skill term, but in skill-matched PvP, opponents are similar skill, so a balanced item should sit at 50%. I rewrote win probability as a direct per-item value centred on 50%, with only the deliberately mis-tuned items deviating. That is both more realistic and the correct mental model for an item-balance study.

### 4. Mixed timestamp formats in one column
I intentionally wrote half the session timestamps as ISO (`2026-03-04 14:05:00`) and half as US-style (`03/04/2026 02:05 PM`) to mimic a messy export. A naive `pd.to_datetime` would choke or mis-parse. The fix was `pd.to_datetime(..., format="mixed", errors="coerce")`, which reads both styles row-by-row. It's documented as cleaning decision #4 in the notebook.

### 5. Statistical vs practical significance in the item z-test (now fixed in the verdict logic)
With ~3,000–10,000 matches per item, the proportion z-test flags even tiny deviations from 50% as significant, so essentially-fair items (e.g. Plate Mail at 52.4%, Storm Bow at 51.8%) used to test as "OVERPOWERED" purely on `p < 0.05`. An earlier version only mentioned this in prose while still printing the wrong verdict. I fixed the code: a verdict now requires **both** statistical significance (the 95% CI clears 50%) **and** a practical effect size (win rate ≥5 percentage points off 50%). Items that are significant but trivially off 50% now read `skewed (sig., small)` instead of OVERPOWERED, so only Phoenix Blade (61.3%) and Aegis Shield (59.4%) — and Rusty Dagger on the low side — get an action verdict. Surfacing effect size, not just the p-value, is the whole point.

### 6. Being honest that the headlines recover designed ground truth
Because I baked the ground truth into the generator (win rates of 0.61/0.59/0.41, a faucet-above-sink tilt, a D1 retention cliff, and a `pay ~ propensity + early_sessions` logistic), several headline numbers in the notebook are *recovering parameters I chose*, not discovering facts. That is legitimate as a **pipeline demonstration** — it shows clean → test → model → recommend works and lands on sensible numbers — but it is not evidence about a real game. I reworded the notebook and README so every such finding is framed as "designed-in / recovered," and called out two places where it matters most: (a) the payer model's AUC ≈0.79 is partly mechanical because early-session count is literally a term in the pay formula (shared hidden propensity → mild target leakage), so I label it a sanity check rather than a generalisable result; and (b) item win rate would be confounded by player skill on real data, which this toy world avoids only by construction.

### 7. `early_matches` was computed from all-time matches, not the first 3 days
The payer-model feature `early_matches` was mistakenly built from each player's *entire* match history despite its name and the "first-3-day behaviour" framing. I now derive a per-match days-since-install from `install_date` and `match_time` and count only matches with `match_day <= 3`, so the three "early" features are consistently scoped to the first three days. (Also removed a dead intermediate frame that was left over from the original attempt.)

### 8. Verification
The notebook is built programmatically (`build_notebook.py`) and then executed with `jupyter nbconvert --execute`, which is how I confirm it runs top-to-bottom with zero errors (checked via `nbformat`, no cell has an `error` output) before calling it done. Every dashboard CSV is re-opened with pandas to confirm it imports with no index junk.
