# LEARN — Project 3 explained in plain language

This is a walkthrough for readers who are new to finance or to data analysis. It explains what
the project does, how the analysis fits together, and what the technical terms mean.

## What this project does
It studies the US stock market using more than 150 years of real historical data. It looks at
four questions: how much the market has actually grown, how risky it has been, whether it is
expensive today, and whether stocks and gold protect each other. The central result is that how
expensive the market is at a given point has historically been linked to the returns over the
following ten years.

## How the analysis works
The work moves through four stages, and each one exists for a reason.

First, the data. The project is built on actual prices, inflation figures, and valuations going
back to 1871, so the conclusions rest on the historical record rather than opinion.

Second, cleaning. The raw files had a trap: recent months stored `0` where a value had not been
reported yet. Left alone, those zeros would have dragged down every average, so I converted them
to missing values. I also collapsed the daily VIX into monthly figures so it lined up with the
monthly market data.

Third, exploration. Before any modelling, it helps to look. Plotting the market after removing
inflation shows that real growth is modest, and plotting the VIX shows a spike at every crisis.
These views point to where the deeper analysis should focus.

Fourth, testing and conclusions. I measured the worst losses the market has put investors through
(drawdowns), then tested whether today's valuation predicts the next decade's return. It does,
and the relationship is statistically significant. I also checked whether gold and stocks move
together; they mostly do not, which is what makes gold useful in a portfolio. The findings then
turn into three concrete actions: expect lower returns, diversify, and automate discipline.

## Glossary
- Real (inflation-adjusted): a value after removing the effect of rising prices, expressed in
  today's dollars.
- Return: the percentage gain or loss over a period.
- Volatility: how much returns move around, a common measure of risk.
- Drawdown: how far an investment sits below its previous peak.
- CAPE / PE10: a valuation ratio comparing price with ten years of average earnings. Higher means
  more expensive.
- VIX: a market index that rises when investors expect large swings, often called the "fear gauge".
- Correlation: a number from −1 to +1 describing whether two things move together (+1), in
  opposite directions (−1), or independently (0).
- Regression (OLS): fitting the best straight line through a set of points to summarise a
  relationship and measure its strength.
- R²: the share of the variation that the line explains, from 0 (none) to 1 (all).
- p-value: the probability the pattern could appear by chance. A small value (below 0.05) suggests
  it is real.
- Window function (SQL): a query that compares each row with other rows, here this year's price
  against last year's.

## How to run it
1. Open a terminal in the project folder:
   ```bash
   cd project-3-finance
   ```
2. Install the tools (first time only):
   ```bash
   pip install pandas numpy matplotlib seaborn statsmodels jupyter
   ```
3. Refresh the data (optional):
   ```bash
   python data/download_data.py
   ```
4. Open the notebook:
   ```bash
   python -m jupyter notebook analysis.ipynb
   ```
   When it opens, choose Kernel then Restart and Run All. The charts and numbers regenerate as it
   runs.
