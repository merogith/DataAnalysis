# LEARN — Project 2, explained for a beginner 🎓

*No game-industry or coding background needed. Read top to bottom.*

## What this project does (in 4 sentences)
This project studies a free-to-play (F2P) mobile game using made-up but realistic "telemetry" —
records of who played, what they did, what they bought, and which in-game items they used.
It answers three questions a game's producer cares about: **is the coin economy healthy, are the
items fair, and what makes players keep playing and start paying?** Using simple statistics it
shows the game has mild "coin inflation", two unfairly strong paid items, and a sharp drop-off of
new players after day one. The result is a clear, evidence-based to-do list for the next update.

## The story of the analysis (why each step, not just what)

1. **Generate the data → why:** the real public dataset was blocked by the sandbox, so I built a
   *seeded* generator. A bonus: because I designed the data, I know the "right answers" hidden
   inside it, so I can check that the analysis actually finds them.
2. **Clean the data → why:** the raw files were deliberately messy — the same platform written five
   ways (`iOS`, `ios`, `ANDROID `), the same item as `phoenix blade` / `PHOENIX BLADE`, two
   different date formats mixed together, and a few impossible values (a session lasting −12
   minutes). If you don't fix these, your counts and averages are silently wrong.
3. **Explore (EDA) → why:** before any fancy maths, just *look*. How many players? On which
   platforms? Is the daily active count rising or falling? Looking first tells you where to dig.
4. **Analyse deeper → why:**
   - **Economy:** add up coins coming *in* (faucets) vs going *out* (sinks). If more comes in than
     goes out, coins pile up and lose value — inflation.
   - **Items:** a fair item wins half its games. We test each item's win rate against 50% with a
     real statistical test, so we can *prove* which items are too strong or too weak.
   - **Retention:** what fraction of players come back 1, 7 and 30 days after installing? A steep
     drop after day 1 is the classic "retention cliff".
   - **Money:** who pays, and can we predict it early? We train a simple model on each player's
     *first three days* to guess whether they'll ever spend.
5. **SQL → why:** databases are the native habitat of this data, so I also answered a question in
   SQL using a "window function" — a running coin balance per player over time.
6. **Conclude → why:** numbers only matter if they change a decision. The findings become four
   concrete actions for the next update.

## Glossary (plain-English, one line each)
- **F2P (free-to-play):** the game is free; revenue comes from a minority who buy items/currency.
- **Telemetry:** the event logs a game records — sessions, matches, purchases, etc.
- **Faucet (source):** anything that *adds* in-game currency to the economy (quest rewards, daily logins).
- **Sink (drain):** anything that *removes* currency (buying items, upgrades, repairs).
- **Inflation / deflation:** when faucets exceed sinks, coins pile up and lose value (inflation); the opposite is deflation.
- **Retention:** the % of a group of players still active N days after they installed.
- **Cohort:** a group of players grouped by something they share (here, when they installed).
- **D1 / D7 / D30:** retention checkpoints — day 1, day 7, day 30.
- **Churn:** a player leaving and not coming back (the opposite of retention).
- **Funnel:** a step-by-step drop-off chart (installed → played → returned → paid).
- **Win rate:** the share of matches won when a given item is equipped; 50% = perfectly fair.
- **Pick rate:** how often an item is chosen out of all matches.
- **Pay-to-win:** when paying real money buys a gameplay advantage (a balance/fairness problem).
- **ARPU / ARPPU:** Average Revenue Per User / Per *Paying* User.
- **Proportion z-test:** a statistical test for whether an observed rate (e.g. a 59% win rate) is meaningfully different from a target (50%).
- **Confidence interval (CI):** a plausible range for the true value; if a 95% CI for win rate sits entirely above 50%, the item is genuinely too strong.
- **Logistic regression:** a model that predicts a yes/no outcome (here, "will this player ever pay?") and gives each input an interpretable weight.
- **Odds ratio:** how much a feature multiplies the odds of the outcome; >1 = makes paying more likely.
- **Accuracy / AUC:** how good the model is — accuracy = % correct; AUC (0.5 = coin-flip, 1.0 = perfect) = how well it ranks payers above non-payers.
- **Window function (SQL):** a database calculation that looks across related rows without collapsing them — here, a running coin balance per player over time.
- **Star schema:** a BI-friendly data layout — one central "fact" table of measurements surrounded by "dimension" tables that describe it.

## How to run this yourself (exact steps)
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
   Or open it interactively with `python -m jupyter notebook analysis.ipynb` and click
   **Kernel → Restart & Run All**. Every chart and number regenerates in front of you.

## Questions an interviewer might ask (with suggested answers)
- **"Walk me through this project."** → "I built an end-to-end F2P game-economy analysis on
  synthetic telemetry. I answered three producer questions — economy health, item fairness, and
  retention/monetization — and turned them into a concrete balancing and monetization plan. The
  headline findings are mild coin inflation, two overpowered *paid* items (a pay-to-win signal), a
  Day-1 retention cliff, and a payer model with AUC 0.80 from early behaviour."
- **"The data is synthetic — why should I trust the analysis?"** → "The *methods* are exactly what
  I'd run on real telemetry: a z-test for item balance, cohort retention, a funnel, a logistic
  payer model, and SQL window functions. And because I seeded the generator, I could embed a known
  ground truth and confirm the analysis recovers it — the public dataset was network-blocked, which
  I documented."
- **"How did you handle data quality?"** → "The raw files had duplicates, five spellings of each
  platform, mixed-case item names, two timestamp formats in one column, missing categoricals and
  impossible negative durations. I documented every cleaning decision in a table and fixed each —
  e.g. `pd.to_datetime(format='mixed')` to parse both date styles."
- **"A couple of 'balanced' items still tested as significant — explain."** → "That's statistical
  vs practical significance: with thousands of matches per item, even a 51.5% win rate is
  statistically off 50%, but it doesn't matter for gameplay. The items worth acting on are the ones
  with a large effect size — 59–61% — which are also the *paid* ones, hence the pay-to-win flag."
- **"What would you do differently with more time?"** → "Design an A/B test for the proposed coin
  sink and onboarding fixes, move from 'ever pays' to predicted LTV and a churn-timing survival
  model, and add a win-rate control chart so future content can't silently break balance."

## Talking points (say these out loud)
"This project analyses a free-to-play game's telemetry to answer what a producer actually cares
about: is the economy healthy, are the items fair, and what drives players to stay and pay. I found
mild coin inflation because rewards out-pace spending, two overpowered *paid* items that make the
game read as pay-to-win, and a textbook Day-1 retention cliff. I proved the item imbalance with a
proportion z-test and confidence intervals, measured D1/D7/D30 retention and a payer funnel, and
built a logistic model that predicts payers from their first three days with AUC 0.80. I handled
real-world messiness like duplicate rows and mixed date formats, verified the notebook runs
end-to-end with zero errors, and turned it all into a concrete next-sprint plan: add a coin sink,
nerf the two items, fix onboarding, and target a fair early offer at likely payers."
