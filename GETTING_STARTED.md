# Getting Started 🚀 — a beginner's guide to this portfolio

Welcome! This guide assumes **no prior experience**. It explains how the portfolio is
organised, what to install, the order to read things, and what every tool does and why.

---

## 1. How the portfolio is organised (folder by folder)

```
DataAnalysis/
├── README.md                 ← the portfolio landing page (start here on GitHub)
├── GETTING_STARTED.md        ← this file
├── portfolio/
│   ├── index.html            ← a simple, professional web version of the landing page
│   └── README.md             ← notes for the landing page
│
├── project-3-finance/        ← ⭐ FLAGSHIP. Real stock-market data, statistics
├── project-1-pharma-crm/     ← Pharma sales analytics (synthetic data)
└── project-2-game-economy/   ← Free-to-play game economy & balance (synthetic data)
```

**Every project folder has the same layout**, so once you understand one, you understand all three:

| Inside each project | What it is |
|---|---|
| `analysis.ipynb` | The main analysis — a Jupyter notebook you can open and run |
| `README.md` | A 1-page write-up: summary, findings, charts, recommendation |
| `LEARN.md` | A beginner walkthrough + glossary + interview questions |
| `NOTES.md` | An honest log of what went wrong and how it was fixed |
| `DASHBOARD_GUIDE.md` | How to build a Tableau / Power BI dashboard from the data |
| `data/` | The dataset + the script that generates or downloads it |
| `charts/` | The picture files (PNG) the analysis produced |
| `dashboard/` | Clean CSV files ready to load into Tableau / Power BI |
| `build_notebook.py` | The script that assembles the notebook (reproducibility) |

---

## 2. Software you need (and how to check it's installed)

You need **Python 3.9+** and a few libraries. Open a terminal and check Python first:

```bash
python3 --version       # should print Python 3.9 or higher
```

If that works, install the libraries (one command, copy-paste it):

```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels jupyter
```

Check it worked:

```bash
python3 -c "import pandas, numpy, matplotlib, seaborn, sklearn, statsmodels; print('All good!')"
```

If you see `All good!`, you're ready. (If `pip` isn't found, try `pip3`.)

---

## 3. The exact order to review things

1. **`README.md`** (the landing page) — a 2-minute overview of all three projects.
2. **`project-3-finance/`** — the flagship. Read its `README.md`, then its `LEARN.md`,
   then open `analysis.ipynb`.
3. **`project-1-pharma-crm/`** then **`project-2-game-economy/`** — same order each time:
   `README.md` → `LEARN.md` → `analysis.ipynb`.
4. **`DASHBOARD_GUIDE.md`** in any project — if you want to try building a real dashboard.

**To open a notebook:**
```bash
cd project-3-finance
python3 -m jupyter notebook analysis.ipynb
```
A browser tab opens. Click **Kernel → Restart & Run All** to re-run everything. The notebooks
are already saved *with* their outputs, so you can also just read them without running.

---

## 4. Every tool & library, in plain English

| Tool / library | What it is | Why it's used here |
|---|---|---|
| **Python** | A popular, readable programming language | The language all the analysis is written in |
| **Jupyter Notebook** | A document that mixes code, charts, and notes | Lets you run analysis step-by-step and see results inline |
| **pandas** | A spreadsheet-like toolkit for Python | Loading, cleaning, and reshaping data — the workhorse |
| **NumPy** | Fast maths on big lists of numbers | Powers calculations under the hood |
| **Matplotlib** | A charting library | Draws the line/bar/scatter charts |
| **seaborn** | A prettier layer on top of Matplotlib | Nice-looking statistical charts with less code |
| **scikit-learn** | A machine-learning toolkit | Segmentation (KMeans) and the payer-prediction model |
| **statsmodels** | A statistics toolkit | Regression with proper p-values and R² |
| **SQLite** | A tiny database built into Python | Runs the SQL queries (no setup needed) |
| **SQL** | The language for querying databases | Shows database skills employers ask for |
| **Tableau / Power BI** | Drag-and-drop dashboard tools | Turning the data into interactive dashboards |

---

## 5. What each project demonstrates (skills at a glance)

| Project | Headline skill on show |
|---|---|
| **3 — Finance (real data)** | Real-world data sourcing, time-series, hypothesis testing with statistics |
| **1 — Pharma CRM** | Data cleaning, correlation/regression, customer segmentation (clustering) |
| **2 — Game economy** | Behavioural analytics, retention cohorts, a predictive model, A/B-style balance tests |

Across all three: **data cleaning · SQL · exploratory analysis · statistics · visualisation ·
BI dashboards · clear business communication.**

Enjoy exploring — and if you only have five minutes, read `project-3-finance/README.md`. 🎯
