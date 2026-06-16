# Project 1 — Pharmaceutical CRM Sales Analytics 💊
**SYNTHETIC pharma sales data · Python + statistics + machine learning + SQL**

## Executive summary (for a non-technical reader)
- This project answers what a pharma sales leader most wants to know: **who is performing, what
  actually drives prescriptions, and which doctors to focus on next.**
- **Calling doctors works — and it's proven, not assumed.** More rep visits reliably lead to more
  prescriptions: a clear positive correlation (**r = 0.49**) and a highly significant regression
  (**p ≈ 1.5e-37**). On this data, each extra call is associated with **~5.5 more scripts a year**.
- **Prescribing is concentrated:** the top 20% of doctors write roughly a **third of all scripts**,
  so *which* doctors a rep visits matters as much as *how many* visits they make.
- **Performance is uneven:** the top rep drove **6,007 scripts** vs **154** for the lowest — a huge
  coaching and territory-balancing opportunity. **Southeast** leads on volume; **Cardiplex** is the
  flagship product.
- **There is a clear growth target:** a machine-learning segmentation split the **600 doctors into 4
  groups** and isolated a **99-doctor "High-potential growth"** segment — high potential, responsive
  to calls, but not yet prescribing at capacity. That is where to add call effort.
- **Bottom line:** shift calls toward the high-potential growth segment, protect the champions,
  coach the bottom reps using the top reps' playbook.

> **Data label: SYNTHETIC.** Real CRM data (rep calls, doctor prescribing) is proprietary and
> privacy-sensitive, so every row is fabricated by a seeded generator (`data/generate_data.py`).
> The relationships are realistic by design; the people and numbers are not real. See `NOTES.md`.

---

## Problem
A pharmaceutical commercial team needs an evidence-based read on **rep/region/product performance**,
**what actually drives prescriptions**, and **where to focus limited call capacity**. The three
business questions:
1. Which **reps, regions and products** are performing best and worst?
2. Does **call frequency** correlate with **prescription volume** (tested with correlation + regression)?
3. Which **doctor (HCP) segments** should the team prioritise?

## Approach
1. **Generated synthetic data** with a reproducible, seeded script (`data/generate_data.py`) that
   injects realistic messiness (duplicates, missing values, mixed text/date formats, impossible values).
2. **Cleaned & documented every decision** in a markdown table — deduped, standardised region/product
   text, parsed mixed date formats, set impossible values to missing, imputed sensibly.
3. **EDA** — scripts by product/region, the concentration of prescribing across doctors, call activity.
4. **Deeper analysis** — a rep/region/product leaderboard, an **OLS regression** of calls→scripts, and
   a **KMeans segmentation** of doctors into actionable groups.
5. **SQL (SQLite)** — a `RANK() OVER (PARTITION BY region ...)` **window function** to rank reps within
   their region.
6. **BI-ready star-schema exports** + a concrete, prioritised recommendation.

## Key findings (with charts)

**1. More calls → more prescriptions (the flagship result).** Each dot is a doctor. The upward line
means visiting a doctor more is associated with more scripts. r = 0.49, R² = 0.24, p ≈ 1.5e-37.
![Calls vs scripts](charts/05_calls_vs_scripts.png)

**2. A small group of doctors drives a large share of scripts** — so targeting matters.
![Prescribing concentration](charts/02_script_concentration.png)

**3. The segmentation isolates a clear growth target.** The "High-potential growth" group has headroom
*and* responds to calls — the best place to invest.
![HCP segments](charts/06_hcp_segments.png)

| Metric (SYNTHETIC) | Value |
|---|---|
| Calls ↔ scripts correlation | **r = 0.49** (R² = 0.24, p ≈ 1.5e-37) |
| Lift per additional call | **~5.5 scripts / year** |
| Top product / region | **Cardiplex** / **Southeast** |
| Top vs bottom rep (scripts driven) | **6,007** vs **154** |
| Doctor segments found (KMeans, k=4) | Champions (133) · Steady mid-tier (51) · **High-potential growth (99)** · Low priority (317) |
| Prescribing concentration | top 20% of doctors ≈ **37%** of all scripts |

## Recommendation
- **Reallocate calls toward the "High-potential growth" segment** — they have room to grow and respond
  to visits, so each call should return more scripts than visiting already-loyal doctors.
- **Protect the "Champions"** with enough contact to retain them; don't over-invest where there's no upside.
- **Coach the bottom reps using the top reps' patterns** (call frequency and scripts-per-call) and
  rebalance territory load toward the highest-potential regions.

## What I'd do next
- Add a **call-to-script time lag** (does *this* month's call lift *next* month's scripts?).
- Move from correlation toward **causal evidence** (a matched-control or A/B call experiment).
- Layer in **cost per call** so recommendations optimise **ROI**, not just script volume.

---

## Repository contents
| Path | What it is |
|---|---|
| `analysis.ipynb` | The full, runnable analysis (executed top-to-bottom, outputs included) |
| `build_notebook.py` | Reproducibly builds `analysis.ipynb` from code (run, then execute with nbconvert) |
| `data/generate_data.py` | Seeded synthetic data generator (writes the raw CSVs) |
| `data/*.csv` | The generated raw datasets (reps, hcps, calls, prescriptions, products, regions) |
| `charts/` | All 7 generated figures |
| `dashboard/` | BI-ready star schema (`fact_scripts`, `fact_region_product_monthly`, `dim_rep/hcp/product/region`) |
| `DASHBOARD_GUIDE.md` | Step-by-step Tableau **and** Power BI build guide |
| `LEARN.md` | Beginner-friendly walkthrough, glossary & interview Q&A |
| `NOTES.md` | What was tricky and how I worked around it |

## How to run it
```bash
cd project-1-pharma-crm
python3 data/generate_data.py        # regenerate the synthetic raw CSVs (seeded)
python3 build_notebook.py            # rebuild analysis.ipynb from code
python3 -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
```
See `LEARN.md` → "How to run this yourself" for a zero-experience version.
