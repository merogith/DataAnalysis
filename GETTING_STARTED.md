# Getting started

This guide explains how the portfolio is organised, what to install, and a sensible order to read
through it. It assumes only that you can open a terminal.

## How the portfolio is organised

```
DataAnalysis/
├── README.md                 The portfolio overview (start here on GitHub)
├── GETTING_STARTED.md        This file
├── portfolio/
│   ├── index.html            A simple web version of the overview
│   └── README.md             Notes on the web page
│
├── project-3-finance/        Real stock-market data and statistics (main project)
├── project-1-pharma-crm/     Pharma sales analytics (synthetic data)
└── project-2-game-economy/   Free-to-play game economy and balance (synthetic data)
```

Every project folder has the same layout, so once you have read one you know your way around all
three:

| Inside each project | What it is |
|---|---|
| `analysis.ipynb` | The main analysis, as a Jupyter notebook you can open and run |
| `README.md` | A one-page write-up: summary, findings, charts, recommendation |
| `LEARN.md` | A plain-language walkthrough and glossary |
| `NOTES.md` | A log of problems hit during the work and how they were resolved |
| `DASHBOARD_GUIDE.md` | How to build a Tableau or Power BI dashboard from the data |
| `data/` | The dataset and the script that generates or downloads it |
| `charts/` | The figures the analysis produced |
| `dashboard/` | Clean CSVs ready to load into Tableau or Power BI |
| `build_notebook.py` | The script that assembles the notebook (for reproducibility) |

## Software you need

You need Python 3.9 or newer and a few libraries. Check Python first:

```bash
python3 --version       # expect Python 3.9 or higher
```

Then install the libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels jupyter
```

Confirm it worked:

```bash
python3 -c "import pandas, numpy, matplotlib, seaborn, sklearn, statsmodels; print('ready')"
```

If it prints `ready`, you are set. If `pip` is not found, try `pip3`.

## A suggested reading order

1. `README.md`, for a short overview of all three projects.
2. `project-3-finance/`, the main project. Read its `README.md`, then `LEARN.md`, then open
   `analysis.ipynb`.
3. `project-1-pharma-crm/` and `project-2-game-economy/`, in the same order each time:
   `README.md`, then `LEARN.md`, then the notebook.
4. Any `DASHBOARD_GUIDE.md`, if you want to try building a dashboard yourself.

To open a notebook:

```bash
cd project-3-finance
python3 -m jupyter notebook analysis.ipynb
```

A browser tab opens. Choose Kernel, then Restart and Run All, to re-run everything. The notebooks
are saved with their outputs, so you can also just read them without running anything.

## The tools, in brief

| Tool / library | What it is | Why it is used here |
|---|---|---|
| Python | A readable, widely used programming language | The language the analysis is written in |
| Jupyter Notebook | A document that mixes code, charts, and notes | Runs the analysis step by step with results inline |
| pandas | A table/spreadsheet toolkit for Python | Loading, cleaning, and reshaping the data |
| NumPy | Fast numerical operations | Powers the calculations underneath pandas |
| Matplotlib | A charting library | Draws the line, bar, and scatter charts |
| seaborn | A statistical layer on top of Matplotlib | Cleaner statistical charts with less code |
| scikit-learn | A machine-learning toolkit | Segmentation (KMeans) and the payer-prediction model |
| statsmodels | A statistics toolkit | Regression with p-values and R² |
| SQLite | A small database built into Python | Runs the SQL queries with no setup |
| SQL | The language for querying databases | Demonstrates database querying |
| Tableau / Power BI | Dashboard tools | Turning the exported data into interactive dashboards |

## What each project demonstrates

| Project | Main skill on show |
|---|---|
| 3 — Finance (real data) | Sourcing real data, time-series work, hypothesis testing |
| 1 — Pharma CRM | Cleaning, correlation and regression, customer segmentation |
| 2 — Game economy | Behavioural analytics, retention cohorts, a predictive model |

Across all three: data cleaning, SQL, exploratory analysis, statistics, visualisation, BI
dashboards, and business communication.
