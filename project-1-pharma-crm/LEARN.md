# LEARN — Project 1, explained

## What this project does
The project analyses how a pharmaceutical sales team works: sales reps visit doctors ("calls"), and
doctors write prescriptions ("scripts"). Using fake-but-realistic data, it answers three questions: who
is performing well, whether visiting doctors more often goes with more prescriptions, and which doctors
the team should focus on. It uses basic statistics to test the calls-to-scripts link and machine
learning to group doctors into segments worth different amounts of effort. The output is an
evidence-based plan a sales leader could act on.

## How the analysis works

1. Generate the data. Real CRM data is private and proprietary, so I fabricate a realistic world with a
   fixed random seed for reproducibility. I deliberately add messiness (duplicates, blanks, typos,
   impossible numbers) because real data is never clean, and handling that is part of the work.
2. Inspect, then clean. Before changing anything I look at what came out, then fix each problem and
   record the decision. I remove duplicate rows so visits aren't double-counted, make "WEST" and "west"
   the same region, parse three different date formats, and turn impossible values (a −5 minute call, a
   300-script month) into missing rather than trusting them.
3. Explore (EDA). Before any modelling I plot the basics: scripts by product and region, and how
   prescribing is spread across doctors. This shows that a small group of doctors writes a big share of
   scripts, which is why targeting matters.
4. Analyse deeper. I build a leaderboard of reps, run a statistical test of whether more calls go with
   more scripts (they do, strongly), and use KMeans to split doctors into segments so I can recommend
   who to prioritise.
5. SQL. I rank each rep within their own region using a SQL window function, which is the right tool
   when you want "best in each group" rather than "best overall".
6. Conclude. Numbers only matter if they change a decision, so I turn the findings into a concrete plan:
   shift calls to the high-potential doctors, keep contact with the top doctors, and coach the weaker
   reps.

## Glossary
- **HCP:** HealthCare Provider, a doctor who can write prescriptions.
- **Call:** a sales rep's visit to a doctor (in person, video, or phone).
- **Script:** a prescription a doctor writes; the main measure of success here.
- **Potential:** an estimate of how much a doctor could prescribe (their ceiling), 0–100.
- **Decile:** an industry rank (1–10) of how much a doctor prescribes versus peers.
- **Segmentation:** splitting customers (here, doctors) into groups that behave similarly so each group
  can be treated differently.
- **Correlation (r):** a number from −1 to +1 for whether two things move together (+1), oppositely
  (−1), or are unrelated (0). Here, calls versus scripts.
- **Regression (OLS):** fitting the best straight line through a cloud of points to summarise a
  relationship and measure its strength.
- **Slope:** how much the outcome changes per one-unit change in the input; here, extra scripts per
  extra call.
- **R²:** the fraction of the variation in scripts that the line explains (0 = none, 1 = all).
- **p-value:** the chance the pattern is just luck; a tiny value (e.g. < 0.001) means it's almost
  certainly real.
- **KMeans:** a machine-learning method that groups data points into a chosen number of clusters of
  similar points.
- **Standardise (scale):** put features on the same scale before clustering so one large-numbered
  feature doesn't dominate on units alone.
- **Window function (SQL):** a database calculation that compares a row with other rows in a group; here,
  ranking a rep against other reps in the same region.
- **Star schema:** a data layout with one central "fact" table (the events) surrounded by "dimension"
  tables (the descriptions), which is the shape BI tools handle best.
- **Synthetic data:** fabricated data designed to look realistic, used when real data is private.

## How to run it
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
   Or open it interactively with `python3 -m jupyter notebook analysis.ipynb` and choose
   **Kernel → Restart & Run All**. Every chart and number regenerates.
