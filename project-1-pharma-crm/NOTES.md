# NOTES — Project 1 (what was tricky & how I worked around it)

An honest, running log of problems hit while building this project. Showing this is deliberate:
real analytics work is full of these, and handling them well is the job.

### 1. The synthetic correlation was too weak to be a meaningful finding
- **What happened:** my first data generator produced a calls→scripts correlation of only **r ≈ 0.16**.
  Technically "significant" given the sample size, but far too weak to headline a recommendation, and
  not realistic for a pharma promotion-response relationship.
- **Why:** the script-intensity model leaned too heavily on each doctor's *baseline* prescribing and
  spread call effect too thinly, drowning the signal in noise. The responsiveness factor also varied
  too widely (a `beta(2,3)` with a long left tail).
- **Fix:** I rebalanced the data-generating model so **calls are the dominant lever** (raised the call
  coefficient, lowered the baseline term) and tightened the responsiveness distribution to `beta(4,4)`.
  That moved the correlation to a realistic, clearly-meaningful **r ≈ 0.49** (R² ≈ 0.24) — moderate and
  honest, not a suspiciously perfect 0.95. I verified the number *before* building the notebook around it.

### 2. `numpy` scalar `.clip()` crash in the generator
- **What happened:** `rng.normal(18, 7).clip(2, 60)` raised `AttributeError: 'float' object has no
  attribute 'clip'`. When `rng.normal` is called with scalar args it returns a plain Python float,
  which has no `.clip` method (only numpy arrays do).
- **Fix:** switched to the free function `np.clip(rng.normal(18, 7), 2, 60)`, which works on scalars.

### 3. Impossible values had to be injected *and* survive into the raw CSV
- **What happened:** I inject deliberate bad values (negative durations, potential > 100, a 300-script
  month, a 2025 date) so the cleaning step has real work to do. The risk is injecting them and then
  having a later transform quietly "fix" or shuffle them away before they reach disk.
- **Fix:** I inject the bad values *after* the main generation, then concatenate duplicates and shuffle,
  and I confirmed via a quick read-back that each defect (3 over-100 potentials, 5 bad durations, 2 bad
  script counts, 1 future date, 30 dupe calls, 40 dupe scripts) actually lands in the CSV and is then
  caught and reported by the notebook's cleaning cells.

### 4. KMeans labels are arbitrary, so segment *names* must be derived from profiles
- **What happened:** KMeans assigns cluster numbers (0,1,2,3) in a non-deterministic-feeling order, so
  I can't hard-code "segment 2 = Champions". A re-run could swap the numbers.
- **Fix:** I label segments *programmatically from their profiles* — highest average scripts becomes
  "Champions", highest potential (not already champions) becomes the "High-potential growth (TARGET)",
  lowest scripts becomes "Low priority", and the rest "Steady mid-tier". The names follow the data, so
  they stay correct even if the cluster numbering changes. (Seed is fixed for reproducibility regardless.)

### 5. Mixed date formats needed `format="mixed"`
- **What happened:** calls were stored in three formats on purpose (`2024-03-01`, `03/01/2024`,
  `01-Mar-2024`). A single `pd.to_datetime` with one format would fail two-thirds of the rows.
- **Fix:** used `pd.to_datetime(..., format="mixed", errors="coerce")` so pandas parses each row's
  format individually and turns genuine garbage into `NaT`, which I then drop alongside the out-of-period
  (2025) date.

### 6. Environment notes
- pandas is v3.x here, so I avoided the removed `applymap` (used `.map`/vectorised ops) and any
  deprecated args. The notebook is **built programmatically** (`build_notebook.py`) and then **executed
  with `jupyter nbconvert --execute`**, which is how I verify it runs top-to-bottom with **zero errors**
  before declaring it done.
