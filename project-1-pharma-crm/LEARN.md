# LEARN — Project 1, explained for a beginner 🎓

*No pharma or coding background needed. Read top to bottom.*

## What this project does (in 4 sentences)
This project analyses how a pharmaceutical sales team works: sales reps visit doctors ("calls"), and
doctors write prescriptions ("scripts"). Using fake-but-realistic data, it answers three questions:
who is performing well, whether visiting doctors more actually leads to more prescriptions, and which
doctors the team should focus on. It uses basic statistics to **prove** that more calls lead to more
scripts, and machine learning to **group doctors** into segments worth different amounts of effort.
The result is a clear, evidence-based plan a sales leader could act on.

## The story of the analysis (why each step, not just what)

1. **Generate the data → why:** real CRM data is private and proprietary, so we fabricate a realistic
   world with a fixed random seed (so it's reproducible). We *deliberately* add messiness — duplicates,
   blanks, typos, impossible numbers — because real data is never clean, and handling that is half the job.
2. **Inspect, then clean → why:** before changing anything we *look* at what we got, then fix each
   problem on purpose and write down every decision. We remove duplicate rows (so we don't double-count
   visits), make "WEST" and "west" the same region, parse three different date formats, and turn
   impossible values (a −5 minute call, a 300-script month) into "missing" instead of trusting them.
3. **Explore (EDA) → why:** before any fancy maths we plot the basics — scripts by product and region,
   and how prescribing is spread across doctors. This instantly reveals that a small group of doctors
   writes a big share of scripts, which tells us *targeting* matters.
4. **Analyse deeper → why:** we build a **leaderboard** of reps; run a real **statistical test** of
   whether more calls mean more scripts (it does, strongly); and use **machine learning (KMeans)** to
   split doctors into segments so we can recommend who to prioritise.
5. **SQL → why:** we show a database skill by ranking each rep *within their own region* using a SQL
   **window function** — useful when you want "best in each group", not just "best overall".
6. **Conclude → why:** numbers only matter if they change a decision. We turn the findings into a
   concrete plan: shift calls to the high-potential doctors, protect the top doctors, coach weak reps.

## Glossary (plain-English, one line each)
- **HCP:** HealthCare Provider — a doctor who can write prescriptions.
- **Call:** a sales rep's visit to a doctor (in person, video, or phone).
- **Script:** a prescription a doctor writes (our main measure of success).
- **Potential:** an estimate of how much a doctor *could* prescribe (their ceiling), 0–100.
- **Decile:** an industry rank (1–10) of how much a doctor prescribes vs peers.
- **Segmentation:** splitting customers (here, doctors) into groups that behave similarly, so you can
  treat each group differently.
- **Correlation (r):** a number from −1 to +1 saying whether two things move together (+1), oppositely
  (−1), or are unrelated (0). Here, calls vs scripts.
- **Regression (OLS):** drawing the best straight line through a cloud of points to summarise a
  relationship and measure its strength.
- **Slope:** how much the outcome changes per one-unit change in the input — here, extra scripts per
  extra call.
- **R²:** of all the ups and downs in scripts, what fraction the line explains (0 = nothing, 1 = everything).
- **p-value:** the chance the pattern is just luck — tiny (e.g. < 0.001) means "almost certainly real".
- **KMeans:** a machine-learning method that automatically groups data points into a chosen number of
  clusters that are similar to each other.
- **Standardise (scale):** put features on the same scale before clustering, so one big-numbered feature
  doesn't dominate just because of its units.
- **Window function (SQL):** a database calculation that compares a row with *other* rows in a group —
  here, ranking a rep against other reps in the same region.
- **Star schema:** a clean data layout with one central "fact" table (the events) surrounded by
  "dimension" tables (the descriptions) — the standard shape BI tools like best.
- **Synthetic data:** fabricated data designed to look realistic, used when real data is private.

## How to run this yourself (exact steps)
1. Open a terminal in the project folder:
   ```bash
   cd project-1-pharma-crm
   ```
2. (First time only) install the tools:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn statsmodels jupyter nbconvert
   ```
3. Regenerate the synthetic data (seeded, so you get the same numbers):
   ```bash
   python3 data/generate_data.py
   ```
4. Rebuild and run the notebook:
   ```bash
   python3 build_notebook.py
   python3 -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
   ```
   Or open it interactively with `python3 -m jupyter notebook analysis.ipynb` and click
   **Kernel → Restart & Run All**. Every chart and number regenerates in front of you.

## Questions an interviewer might ask (with suggested answers)
- **"Walk me through this project."** → "I analysed a pharma sales CRM to answer three questions: who's
  performing, whether calling doctors more drives prescriptions, and which doctors to prioritise. The
  headline is a statistically significant link between call frequency and prescriptions (r ≈ 0.49,
  p ≪ 0.001), and a doctor segmentation that isolates a high-potential growth group to target."
- **"It's synthetic — does that make it less valid?"** → "The *data* is fabricated because real CRM data
  is proprietary, but the *methods* are exactly what I'd run on real data: documented cleaning, a
  regression with proper diagnostics, KMeans segmentation, and a SQL window function. I built the
  generator to inject realistic messiness so the cleaning work is genuine."
- **"How did you handle data quality?"** → "I deduped by ID, standardised inconsistent region/product
  text, parsed three different date formats, dropped an out-of-period date, and turned impossible values
  (negative call durations, potential scores over 100, a 300-script month) into missing or dropped rows —
  documenting every decision in a table so nothing changes silently."
- **"Correlation isn't causation — so can you really say calls drive scripts?"** → "Correct, and I say so
  explicitly. The relationship is strong and significant, but to claim causation I'd want a call-to-script
  time lag and ideally a matched-control or A/B experiment — which I listed as next steps."
- **"How did you choose the number of segments?"** → "I looked at the KMeans inertia (an elbow check) and
  settled on four because it gave clearly distinct, *actionable* groups — Champions, Steady mid-tier,
  High-potential growth, and Low priority — rather than the maximum that the maths allowed."
- **"What would you do with more time?"** → "Add a time-lagged call→script model, bring in cost-per-call
  to optimise ROI rather than raw volume, and run a real experiment to establish causation."

## Talking points (say these out loud)
"This project analyses a pharmaceutical sales CRM to answer what a commercial leader actually cares
about: who's performing, what drives prescriptions, and where to focus. The standout result is a
statistically significant link between how often reps call on doctors and how much those doctors
prescribe — about 5.5 extra scripts per additional call. I then used machine-learning segmentation to
split 600 doctors into four groups and pinpoint a high-potential segment to target. I built the whole
pipeline reproducibly — seeded synthetic data with realistic messiness, documented cleaning, regression,
KMeans, and a SQL window function — and verified it by running the notebook end-to-end with zero errors."
