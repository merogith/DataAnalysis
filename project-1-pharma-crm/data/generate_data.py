"""Generate SYNTHETIC pharmaceutical CRM data for project-1-pharma-crm.

This is FAKE data. Real pharma CRM data (rep calls, HCP prescribing) is
proprietary and privacy-sensitive, so we fabricate a realistic-looking world
with a fixed random seed for full reproducibility.

We deliberately inject realistic messiness so the cleaning step in the
notebook has something genuine to do:
  - missing values (blank emails, missing potential scores, NaN call durations)
  - duplicate rows (a few calls/prescriptions logged twice)
  - inconsistent formats (mixed-case region names, stray whitespace,
    mixed date formats, mixed-case product names)
  - a few impossible values (negative call duration, a 300-script day,
    a future date)

Run:  python3 data/generate_data.py
Writes: regions.csv, products.csv, reps.csv, hcps.csv, calls.csv, prescriptions.csv
into the same data/ folder.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
OUT = Path(__file__).resolve().parent

# ----------------------------------------------------------------------------
# Reference dimensions
# ----------------------------------------------------------------------------
# Regions — we will store them in MIXED CASE on purpose to create a cleaning task.
REGION_CANON = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]
# product portfolio: brand, therapy area, launch maturity multiplier (affects scripts)
PRODUCTS = [
    ("Cardiplex", "Cardiology", 1.30),   # flagship, mature, high volume
    ("Neurova",   "Neurology",  1.00),
    ("Pulmoair",  "Respiratory", 0.85),
    ("Glucosane", "Endocrinology", 1.10),
    ("Dermacalm", "Dermatology", 0.60),   # niche, newer, low volume
]

N_REPS = 40
N_HCPS = 600
DATE_START = pd.Timestamp("2024-01-01")
DATE_END = pd.Timestamp("2024-12-31")


def _whitespace_noise(s, p=0.05):
    """Randomly add stray leading/trailing whitespace to a fraction of strings."""
    out = []
    for v in s:
        r = rng.random()
        if r < p:
            out.append("  " + str(v))
        elif r < 2 * p:
            out.append(str(v) + " ")
        else:
            out.append(v)
    return out


def _case_noise(name):
    """Return region name in a randomly inconsistent case."""
    choice = rng.integers(0, 4)
    if choice == 0:
        return name.upper()
    if choice == 1:
        return name.lower()
    if choice == 2:
        return name  # canonical Title case
    return name.title()


# ----------------------------------------------------------------------------
# regions.csv
# ----------------------------------------------------------------------------
regions = pd.DataFrame({
    "region_id": [f"R{i+1:02d}" for i in range(len(REGION_CANON))],
    "region_name": REGION_CANON,
    # number of HCPs in the region's addressable market (potential)
    "market_size": rng.integers(800, 2000, len(REGION_CANON)),
})
regions.to_csv(OUT / "regions.csv", index=False)

# ----------------------------------------------------------------------------
# products.csv
# ----------------------------------------------------------------------------
products = pd.DataFrame({
    "product_id": [f"P{i+1:02d}" for i in range(len(PRODUCTS))],
    "product_name": [p[0] for p in PRODUCTS],
    "therapy_area": [p[1] for p in PRODUCTS],
    "list_price_usd": rng.integers(120, 900, len(PRODUCTS)),
})
# inconsistent formatting: make a couple product names lower/upper case
pn = products["product_name"].tolist()
pn[2] = pn[2].upper()        # PULMOAIR
pn[4] = pn[4].lower()        # dermacalm
products["product_name"] = _whitespace_noise(pn, p=0.15)
products.to_csv(OUT / "products.csv", index=False)

# map of underlying maturity multiplier by product_id
prod_mult = {f"P{i+1:02d}": PRODUCTS[i][2] for i in range(len(PRODUCTS))}

# ----------------------------------------------------------------------------
# reps.csv — each rep belongs to one region, has a hidden "skill" factor
# ----------------------------------------------------------------------------
first = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Jamie",
         "Avery", "Quinn", "Drew", "Cameron", "Skyler", "Reese", "Parker",
         "Hayden", "Rowan", "Emerson", "Finley", "Sage"]
last = ["Patel", "Nguyen", "Garcia", "Smith", "Khan", "Rossi", "Müller", "Costa",
        "Adeyemi", "Lopez", "Chen", "Okafor", "Dubois", "Haas", "Silva",
        "Yilmaz", "Kim", "Novak", "Brown", "Ivanov"]

rep_skill = rng.normal(1.0, 0.22, N_REPS).clip(0.45, 1.7)  # hidden productivity factor
reps = pd.DataFrame({
    "rep_id": [f"REP{i+1:03d}" for i in range(N_REPS)],
    "rep_name": [f"{rng.choice(first)} {rng.choice(last)}" for _ in range(N_REPS)],
    "region_id": rng.choice(regions["region_id"], N_REPS),
    "tenure_years": rng.integers(1, 18, N_REPS),
    "_skill": rep_skill,  # internal; we drop before saving
})
# email with a realistic format, but leave some MISSING (blank)
emails = [f"{n.split()[0].lower()}.{n.split()[1].lower()}@synthpharma.example"
          for n in reps["rep_name"]]
emails = [e.encode("ascii", "ignore").decode() for e in emails]  # strip accents
mask_missing_email = rng.random(N_REPS) < 0.08
for i in np.where(mask_missing_email)[0]:
    emails[i] = ""  # missing email
reps["email"] = emails
reps_out = reps.drop(columns=["_skill"]).copy()
reps_out.to_csv(OUT / "reps.csv", index=False)

skill_by_rep = dict(zip(reps["rep_id"], reps["_skill"]))
region_by_rep = dict(zip(reps["rep_id"], reps["region_id"]))

# ----------------------------------------------------------------------------
# hcps.csv — doctors. Each has a "potential" (how much they could prescribe)
# and a "responsiveness" (how much a rep call moves their prescribing).
# These hidden drivers create the real signal the KMeans segmentation finds.
# ----------------------------------------------------------------------------
specialties = ["Cardiologist", "Neurologist", "Pulmonologist",
               "Endocrinologist", "Dermatologist", "General Practitioner"]
hcp_region = rng.choice(regions["region_id"], N_HCPS)
potential = rng.gamma(shape=2.0, scale=1.0, size=N_HCPS)        # right-skewed
potential = (potential / potential.max() * 100).round(1)        # 0-100 potential score
responsiveness = rng.beta(4, 4, N_HCPS).round(3)                # 0-1, how much calls help
baseline = rng.gamma(2.0, 6.0, N_HCPS)                          # baseline monthly scripts

hcps = pd.DataFrame({
    "hcp_id": [f"HCP{i+1:04d}" for i in range(N_HCPS)],
    "hcp_name": [f"Dr. {rng.choice(last)}" for _ in range(N_HCPS)],
    "specialty": rng.choice(specialties, N_HCPS),
    "region_id": hcp_region,
    "potential_score": potential,
    "decile": rng.integers(1, 11, N_HCPS),  # industry "decile" 1-10 prescriber rank
    "_responsiveness": responsiveness,
    "_baseline": baseline,
})
# inject missing potential scores (~6%)
mask_missing_pot = rng.random(N_HCPS) < 0.06
hcps.loc[mask_missing_pot, "potential_score"] = np.nan
# a few impossible potential values (>100) to catch in cleaning
bad_pot_idx = rng.choice(N_HCPS, 3, replace=False)
hcps.loc[bad_pot_idx, "potential_score"] = [145.0, 220.0, 130.0]

hcps_out = hcps.drop(columns=["_responsiveness", "_baseline"]).copy()
hcps_out.to_csv(OUT / "hcps.csv", index=False)

resp_by_hcp = dict(zip(hcps["hcp_id"], hcps["_responsiveness"]))
base_by_hcp = dict(zip(hcps["hcp_id"], hcps["_baseline"]))
potential_by_hcp = dict(zip(hcps["hcp_id"], potential))  # the true (clean) potential
region_by_hcp = dict(zip(hcps["hcp_id"], hcps["region_id"]))

# ----------------------------------------------------------------------------
# calls.csv — rep visits to HCPs across the year.
# A rep mostly calls HCPs in their own region. More skilled reps make more calls.
# ----------------------------------------------------------------------------
rep_ids = reps["rep_id"].tolist()
hcp_by_region = {rid: hcps.loc[hcps["region_id"] == rid, "hcp_id"].tolist()
                 for rid in regions["region_id"]}

call_rows = []
call_counter = 0
date_span_days = (DATE_END - DATE_START).days
date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y"]  # mixed formats on purpose

for rid in rep_ids:
    skill = skill_by_rep[rid]
    home = region_by_rep[rid]
    # number of calls this rep makes in the year scales with skill
    n_calls = int(rng.normal(220, 40) * skill)
    n_calls = max(40, n_calls)
    pool = hcp_by_region[home] if hcp_by_region[home] else hcps["hcp_id"].tolist()
    for _ in range(n_calls):
        # 85% of calls in home region, 15% spill to a random HCP
        if rng.random() < 0.85 and pool:
            hcp = rng.choice(pool)
        else:
            hcp = rng.choice(hcps["hcp_id"].values)
        day = rng.integers(0, date_span_days + 1)
        dt = DATE_START + pd.Timedelta(days=int(day))
        fmt = date_formats[rng.integers(0, len(date_formats))]
        call_type = rng.choice(["In-Person", "Virtual", "Phone"], p=[0.55, 0.30, 0.15])
        duration = float(np.clip(rng.normal(18, 7), 2, 60))  # minutes
        call_counter += 1
        call_rows.append({
            "call_id": f"C{call_counter:06d}",
            "rep_id": rid,
            "hcp_id": hcp,
            "call_date": dt.strftime(fmt),
            "call_type": call_type,
            "duration_min": round(duration, 1),
        })

calls = pd.DataFrame(call_rows)
# missing durations (~4%)
mask_missing_dur = rng.random(len(calls)) < 0.04
calls.loc[mask_missing_dur, "duration_min"] = np.nan
# a few impossible durations (negative / absurd)
bad_dur_idx = rng.choice(len(calls), 5, replace=False)
calls.loc[bad_dur_idx, "duration_min"] = [-5.0, -12.0, 999.0, -3.0, 250.0]
# one future date (data-entry error)
calls.loc[calls.index[0], "call_date"] = "2025-07-15"
# stray whitespace in call_type
calls["call_type"] = _whitespace_noise(calls["call_type"].tolist(), p=0.04)
# DUPLICATE rows: copy ~30 calls verbatim and append
dupe_calls = calls.sample(30, random_state=SEED)
calls = pd.concat([calls, dupe_calls], ignore_index=True)
calls = calls.sample(frac=1, random_state=SEED).reset_index(drop=True)  # shuffle
calls.to_csv(OUT / "calls.csv", index=False)

# count clean calls per (hcp, product) implicitly: calls are product-agnostic,
# but a rep promotes the products relevant to that HCP's region mix. For the
# script model we use total calls received per HCP as the driver.
calls_per_hcp = (calls.drop_duplicates(subset="call_id")
                 .groupby("hcp_id").size().to_dict())

# ----------------------------------------------------------------------------
# prescriptions.csv — monthly script counts per HCP per product.
# THE CORE SIGNAL: scripts = baseline + responsiveness * calls + product effect
# + region/rep noise. This makes call frequency genuinely correlate with scripts.
# ----------------------------------------------------------------------------
months = pd.date_range("2024-01-01", "2024-12-01", freq="MS")
script_rows = []
script_counter = 0

for hcp in hcps["hcp_id"]:
    total_calls = calls_per_hcp.get(hcp, 0)
    resp = resp_by_hcp[hcp]
    base = base_by_hcp[hcp]
    reg = region_by_hcp[hcp]
    pot = potential_by_hcp[hcp]
    pot = 50.0 if (pot is None or np.isnan(pot)) else pot
    # how the year's calls spread across 12 months (roughly even with noise)
    monthly_calls = rng.multinomial(total_calls, [1/12]*12) if total_calls else [0]*12
    for pid, mult in prod_mult.items():
        # each HCP only prescribes a subset of products meaningfully
        if rng.random() < 0.35:
            continue  # this HCP doesn't really write this product
        for mi, m in enumerate(months):
            mc = monthly_calls[mi]
            # script intensity model: calls are the dominant lever (with a
            # responsiveness multiplier), plus a smaller baseline + potential term.
            lam = (base * 0.10 * mult
                   + resp * mc * 4.0 * mult
                   + (pot / 100.0) * 3.0 * mult)
            lam = max(0.1, lam)
            scripts = rng.poisson(lam)
            if scripts == 0 and rng.random() < 0.6:
                continue  # don't log zero-script months most of the time
            script_counter += 1
            script_rows.append({
                "script_id": f"S{script_counter:07d}",
                "hcp_id": hcp,
                "product_id": pid,
                "month": m.strftime("%Y-%m-%d"),
                "script_count": int(scripts),
            })

scripts_df = pd.DataFrame(script_rows)
# a few impossible values: one 300-script month, one negative
bad_idx = rng.choice(len(scripts_df), 2, replace=False)
scripts_df.loc[bad_idx[0], "script_count"] = 300
scripts_df.loc[bad_idx[1], "script_count"] = -4
# DUPLICATE rows (~40 verbatim)
dupe_scripts = scripts_df.sample(40, random_state=SEED)
scripts_df = pd.concat([scripts_df, dupe_scripts], ignore_index=True)
scripts_df = scripts_df.sample(frac=1, random_state=SEED).reset_index(drop=True)
scripts_df.to_csv(OUT / "prescriptions.csv", index=False)

print("SYNTHETIC pharma CRM data written to", OUT)
for name in ["regions", "products", "reps", "hcps", "calls", "prescriptions"]:
    df = pd.read_csv(OUT / f"{name}.csv")
    print(f"  {name+'.csv':20s} {df.shape[0]:6d} rows x {df.shape[1]} cols")
