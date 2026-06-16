# LEARN — Project 2 explained

## What this project does
This project studies a free-to-play (F2P) mobile game using synthetic but realistic telemetry: records of who played, what they did, what they bought, and which in-game items they used. It answers three questions a game's producer cares about: is the coin economy healthy, are the items fair, and what makes players keep playing and start paying? Using straightforward statistics, the analysis shows mild coin inflation, two unfairly strong paid items, and a sharp drop-off of new players after day one, and turns those findings into a list of changes for the next update.

## How the analysis works
1. Generate the data. The real public dataset was blocked by the sandbox, so I built a seeded generator. Because I designed the data, I know the answers hidden inside it and can check that the analysis finds them.
2. Clean the data. The raw files are deliberately messy: the same platform written several ways (`iOS`, `ios`, `ANDROID `), the same item as `phoenix blade` or `PHOENIX BLADE`, two date formats mixed together, and a few impossible values such as a session lasting −12 minutes. Left unfixed, these quietly corrupt counts and averages.
3. Explore (EDA). Before any modelling, look at the basics: how many players, on which platforms, and whether the daily active count is rising or falling. That tells you where to dig.
4. Analyse deeper:
   - Economy: add up coins coming in (faucets) versus going out (sinks). When more comes in than goes out, coins pile up and lose value, which is inflation.
   - Items: a fair item wins half its games, so I test each item's win rate against 50% with a proportion z-test to show which items are too strong or too weak.
   - Retention: what fraction of players come back 1, 7 and 30 days after installing. A steep drop after day 1 is the classic retention cliff.
   - Money: who pays, and can it be predicted early? I train a simple model on each player's first three days to estimate whether they'll ever spend.
5. SQL. Databases are the native home of this data, so I also answered a question in SQL using a window function, a running coin balance per player over time.
6. Conclude. Numbers only matter if they change a decision, so the findings become four concrete actions for the next update.

## Glossary
- **F2P (free-to-play):** the game is free; revenue comes from a minority who buy items or currency.
- **Telemetry:** the event logs a game records (sessions, matches, purchases).
- **Faucet (source):** anything that adds in-game currency (quest rewards, daily logins).
- **Sink (drain):** anything that removes currency (buying items, upgrades, repairs).
- **Inflation / deflation:** faucets above sinks means coins pile up and lose value (inflation); the reverse is deflation.
- **Retention:** the share of a group of players still active N days after installing.
- **Cohort:** a group of players sharing something (here, install date).
- **D1 / D7 / D30:** retention checkpoints at day 1, 7 and 30.
- **Churn:** a player leaving and not coming back (the opposite of retention).
- **Funnel:** a step-by-step drop-off chart (installed → played → returned → paid).
- **Win rate:** the share of matches won when a given item is equipped; 50% is fair.
- **Pick rate:** how often an item is chosen across all matches.
- **Pay-to-win:** when spending real money buys a gameplay advantage.
- **ARPU / ARPPU:** average revenue per user / per paying user.
- **Proportion z-test:** a test for whether an observed rate (e.g. 59% win rate) differs meaningfully from a target (50%).
- **Confidence interval (CI):** a plausible range for the true value; a 95% CI sitting entirely above 50% means the item is genuinely too strong.
- **Logistic regression:** a model that predicts a yes/no outcome (here, "will this player ever pay?") and gives each input an interpretable weight.
- **Odds ratio:** how much a feature multiplies the odds of the outcome; above 1 makes paying more likely.
- **Accuracy / AUC:** accuracy is the percent correct; AUC (0.5 = coin-flip, 1.0 = perfect) measures how well the model ranks payers above non-payers.
- **Window function (SQL):** a calculation that looks across related rows without collapsing them, here a running coin balance per player over time.
- **Star schema:** a BI-friendly layout with one central fact table of measurements surrounded by dimension tables that describe it.

## How to run it
1. Open a terminal in the project folder:
   ```bash
   cd project-2-game-economy
   ```
2. (First time only) install the tools:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn statsmodels jupyter nbconvert
   ```
3. Generate the synthetic data:
   ```bash
   python data/generate_data.py
   ```
4. Rebuild and run the notebook:
   ```bash
   python build_notebook.py
   python -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
   ```
   Or open it interactively with `python -m jupyter notebook analysis.ipynb` and use Kernel → Restart & Run All. Every chart and number regenerates.
