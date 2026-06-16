"""Reproducible SYNTHETIC F2P game-economy telemetry generator.

This writes raw CSVs that deliberately contain real-world messiness (missing
values, duplicate rows, inconsistent formats, stray whitespace, a few impossible
values) so the cleaning step in analysis.ipynb has something genuine to fix.

The synthetic world is engineered to tell a coherent, realistic story:
  * a MILD currency INFLATION  (faucets out-pace sinks slightly over time)
  * two OVERPOWERED items       ("Phoenix Blade", "Aegis Shield" ~ 60% win rate)
  * one UNDERPOWERED item       ("Rusty Dagger" ~ 41% win rate)
  * a RETENTION CLIFF after D1  (most churn happens on day 1)
  * SPENDERS are a small, high-value minority driven by early engagement.

Run:  python data/generate_data.py
Everything is seeded, so re-running reproduces byte-identical raw files.

DATA LABEL: 100% SYNTHETIC. No real players or real money involved.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

RNG = np.random.default_rng(20260616)        # one seed to rule them all
HERE = Path(__file__).resolve().parent
N_PLAYERS = 6000
START = datetime(2026, 1, 1)                  # day-0 of the game's launch window
HORIZON_DAYS = 120                            # observation window length

# --------------------------------------------------------------------------- #
#  Reference dimensions
# --------------------------------------------------------------------------- #
PLATFORMS = ["iOS", "Android", "Web"]
COUNTRIES = ["US", "BR", "DE", "IN", "GB", "JP", "FR", "TR"]
ACQ_CHANNELS = ["organic", "paid_social", "influencer", "cross_promo"]

# item_name, slot, base_price_soft, power(0-100 design rating), is_premium
ITEMS = [
    ("Phoenix Blade",  "weapon", 1800, 92, True),    # OVERPOWERED (premium)
    ("Aegis Shield",   "armor",  1500, 88, True),     # OVERPOWERED
    ("Storm Bow",      "weapon", 1200, 74, False),
    ("Iron Sword",     "weapon",  400, 55, False),
    ("Leather Vest",   "armor",   350, 50, False),
    ("Healing Charm",  "trinket", 900, 68, False),
    ("Lucky Coin",     "trinket", 600, 52, False),
    ("Frost Wand",     "weapon", 1100, 71, False),
    ("Plate Mail",     "armor",  1000, 70, False),
    ("Rusty Dagger",   "weapon",  150, 30, False),    # UNDERPOWERED (a trap item)
]

# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
def messy_platform(p):
    """Inconsistent casing/whitespace that a real export would contain."""
    variants = {
        "iOS":     ["iOS", "ios", "IOS", " iOS"],
        "Android": ["Android", "android", "ANDROID", "Android "],
        "Web":     ["Web", "web", "WEB", " web "],
    }
    return RNG.choice(variants[p])


def messy_item_name(name):
    roll = RNG.random()
    if roll < 0.08:
        return name.lower()
    if roll < 0.14:
        return "  " + name + " "        # stray whitespace
    if roll < 0.18:
        return name.upper()
    return name


# --------------------------------------------------------------------------- #
#  1. PLAYERS
# --------------------------------------------------------------------------- #
def make_players():
    ids = np.arange(1, N_PLAYERS + 1)
    # installs spread across the first 90 days (so D30 is observable for early cohorts)
    install_offsets = RNG.integers(0, 90, size=N_PLAYERS)
    install_dates = [START + timedelta(days=int(o),
                                       hours=int(RNG.integers(0, 24)),
                                       minutes=int(RNG.integers(0, 60)))
                     for o in install_offsets]

    platform = [messy_platform(RNG.choice(PLATFORMS, p=[0.45, 0.45, 0.10]))
                for _ in range(N_PLAYERS)]
    country = RNG.choice(COUNTRIES, size=N_PLAYERS,
                         p=[0.30, 0.12, 0.10, 0.18, 0.09, 0.08, 0.07, 0.06])
    channel = RNG.choice(ACQ_CHANNELS, size=N_PLAYERS, p=[0.50, 0.25, 0.15, 0.10])

    # "engagement propensity" latent score drives sessions, retention & spend
    propensity = RNG.beta(2, 5, size=N_PLAYERS)        # right-skewed: most players low

    df = pd.DataFrame({
        "player_id": ids,
        "install_date": [d.strftime("%Y-%m-%d %H:%M:%S") for d in install_dates],
        "platform": platform,
        "country": country,
        "acquisition_channel": channel,
        "prop_": propensity,                      # internal, dropped before save
        "install_dt_": install_dates,
    })
    return df


# --------------------------------------------------------------------------- #
#  2. SESSIONS  (drives retention)
# --------------------------------------------------------------------------- #
def make_sessions(players):
    rows = []
    for r in players.itertuples(index=False):
        prop = r.prop_
        install_dt = r.install_dt_
        # expected active days ~ propensity, with a hard D1 cliff baked in
        # day-0 everyone plays; survival each subsequent day depends on propensity
        active_days = [0]
        alive = True
        for day in range(1, HORIZON_DAYS):
            # base daily retention probability climbs with propensity but there is
            # a sharp extra drop specifically after day 0 -> day 1 (the cliff)
            if day == 1:
                p_ret = 0.30 + 0.60 * prop          # big day-1 drop for low-prop players
            else:
                p_ret = 0.80 + 0.18 * prop          # much stickier once they survive D1
                p_ret *= 0.992 ** day                # gentle long-run decay
            if not alive or RNG.random() > p_ret:
                alive = False
                # small chance of a resurrection (win-back) for engaged players
                if prop > 0.45 and RNG.random() < 0.08:
                    alive = True
                else:
                    continue
            active_days.append(day)

        for day in active_days:
            # 1-4 sessions on an active day, more for engaged players
            n_sess = 1 + RNG.poisson(0.4 + 2.0 * prop)
            for _ in range(int(n_sess)):
                sess_dt = install_dt + timedelta(days=int(day),
                                                 hours=int(RNG.integers(0, 24)),
                                                 minutes=int(RNG.integers(0, 60)))
                duration = max(1, int(RNG.normal(8 + 14 * prop, 6)))   # minutes
                rows.append((r.player_id, sess_dt, day, duration))

    s = pd.DataFrame(rows, columns=["player_id", "session_dt", "day_since_install",
                                    "duration_min"])
    # mixed timestamp formats: half ISO, half US-style M/D/Y with AM/PM
    fmt_mask = RNG.random(len(s)) < 0.5
    iso = s["session_dt"].dt.strftime("%Y-%m-%d %H:%M:%S")
    usf = s["session_dt"].dt.strftime("%m/%d/%Y %I:%M %p")
    s["session_time"] = np.where(fmt_mask, iso, usf)
    s = s.drop(columns=["session_dt"])
    # a few impossible negative durations (sensor glitches)
    bad = RNG.choice(len(s), size=max(1, len(s) // 800), replace=False)
    s.loc[bad, "duration_min"] = -s.loc[bad, "duration_min"].abs()
    return s


# --------------------------------------------------------------------------- #
#  3. MATCHES  (drives item win-rate balance analysis)
# --------------------------------------------------------------------------- #
def make_matches(players, sessions):
    """Each active day a player may play matches; the item they equip nudges
    their win probability. Overpowered items push win-rate well above 50%."""
    item_names = [it[0] for it in ITEMS]
    # pick weights: cheap/common items picked more; the two OP items popular too
    base_pick = np.array([18, 16, 9, 14, 12, 8, 7, 7, 6, 13], dtype=float)
    base_pick = base_pick / base_pick.sum()

    # TRUE per-item win probability. In skill-matched PvP, opponents are similar
    # skill, so a *balanced* item sits at ~50%. Only the deliberately mis-tuned
    # items deviate: the two premium items are OVERPOWERED, Rusty Dagger is a trap.
    # These are the ground-truth values the analysis should recover (+/- noise).
    item_winprob = {
        "Phoenix Blade": 0.61,   # OVERPOWERED
        "Aegis Shield":  0.59,   # OVERPOWERED
        "Storm Bow":     0.52,
        "Iron Sword":    0.50,
        "Leather Vest":  0.49,
        "Healing Charm": 0.51,
        "Lucky Coin":    0.50,
        "Frost Wand":    0.515,
        "Plate Mail":    0.505,
        "Rusty Dagger":  0.41,   # UNDERPOWERED
    }

    rows = []
    # build a quick lookup of active days per player
    active = sessions.groupby("player_id")["day_since_install"].apply(
        lambda s: sorted(set(int(d) for d in s)))
    inst = dict(zip(players.player_id, players.install_dt_))
    match_id = 1
    for pid, days in active.items():
        for day in days:
            if RNG.random() > 0.6:        # not every active day has ranked matches
                continue
            n_matches = RNG.integers(1, 5)
            for _ in range(int(n_matches)):
                item = RNG.choice(item_names, p=base_pick)
                p = item_winprob[item]
                won = RNG.random() < p
                mdt = inst[pid] + timedelta(days=int(day),
                                            hours=int(RNG.integers(0, 24)),
                                            minutes=int(RNG.integers(0, 60)))
                rows.append((match_id, pid, mdt.strftime("%Y-%m-%d %H:%M:%S"),
                             messy_item_name(item), int(won),
                             int(RNG.integers(5, 26))))   # match duration minutes
                match_id += 1
    m = pd.DataFrame(rows, columns=["match_id", "player_id", "match_time",
                                    "item_equipped", "won", "match_duration_min"])
    return m


# --------------------------------------------------------------------------- #
#  4. CURRENCY TRANSACTIONS  (faucets vs sinks -> inflation analysis)
# --------------------------------------------------------------------------- #
def make_currency(players, sessions):
    """Soft-currency ledger. Positive = faucet (source), negative = sink (drain).
    We tilt faucets slightly above sinks to create MILD INFLATION over time."""
    faucet_types = ["quest_reward", "daily_login", "match_reward", "achievement"]
    sink_types = ["item_purchase", "upgrade", "gacha_pull", "repair"]
    inst = dict(zip(players.player_id, players.install_dt_))
    rows = []
    txn_id = 1
    for r in sessions.itertuples(index=False):
        pid = r.player_id
        day = int(r.day_since_install)
        base_dt = inst[pid] + timedelta(days=day,
                                        hours=int(RNG.integers(0, 24)),
                                        minutes=int(RNG.integers(0, 60)))
        # faucets per active day
        for _ in range(int(RNG.integers(1, 4))):
            ft = RNG.choice(faucet_types, p=[0.4, 0.2, 0.3, 0.1])
            # faucet payouts inflate slightly with calendar day (live-ops generosity creep)
            inflate = 1.0 + 0.0025 * day
            amt = int(RNG.integers(20, 160) * inflate)
            rows.append((txn_id, pid, base_dt.strftime("%Y-%m-%d %H:%M:%S"),
                         ft, "source", amt))
            txn_id += 1
        # sinks: less frequent than faucets (the imbalance) and not inflating
        if RNG.random() < 0.7:
            for _ in range(int(RNG.integers(1, 3))):
                st = RNG.choice(sink_types, p=[0.35, 0.3, 0.2, 0.15])
                amt = -int(RNG.integers(30, 200))
                rows.append((txn_id, pid, base_dt.strftime("%Y-%m-%d %H:%M:%S"),
                             st, "sink", amt))
                txn_id += 1
    c = pd.DataFrame(rows, columns=["txn_id", "player_id", "txn_time",
                                    "txn_type", "flow", "amount"])
    return c


# --------------------------------------------------------------------------- #
#  5. PURCHASES  (real-money + soft-currency; drives monetization model)
# --------------------------------------------------------------------------- #
def make_purchases(players, sessions):
    """Whether a player pays is driven by early engagement (propensity + early
    sessions). Spenders are a small minority (realistic 2-5% payer rate)."""
    inst = dict(zip(players.player_id, players.install_dt_))
    # early sessions = sessions in first 3 days
    early = (sessions[sessions["day_since_install"] <= 3]
             .groupby("player_id").size())
    item_premium = {name: prem for name, _, _, _, prem in ITEMS}
    item_names = [it[0] for it in ITEMS]
    item_price_usd = {it[0]: round(0.99 + it[2] / 350, 2) for it in ITEMS}  # rough $ tiers
    rows = []
    pur_id = 1
    for r in players.itertuples(index=False):
        pid = r.player_id
        prop = r.prop_
        e = int(early.get(pid, 0))
        # logistic propensity to ever pay (tuned for a realistic ~4-6% payer rate)
        z = -5.3 + 4.5 * prop + 0.16 * e
        p_pay = 1 / (1 + np.exp(-z))
        if RNG.random() < p_pay:
            n_pur = 1 + RNG.poisson(0.8 + 2.5 * prop)     # whales buy repeatedly
            for _ in range(int(n_pur)):
                # spenders favour the premium OP items
                if RNG.random() < 0.45:
                    item = RNG.choice(["Phoenix Blade", "Aegis Shield"])
                else:
                    item = RNG.choice(item_names)
                day = int(RNG.integers(0, HORIZON_DAYS))
                pdt = inst[pid] + timedelta(days=day,
                                            hours=int(RNG.integers(0, 24)))
                usd = item_price_usd[item] * RNG.choice([1, 1, 1, 2])  # bundles
                rows.append((pur_id, pid, pdt.strftime("%Y-%m-%d %H:%M:%S"),
                             messy_item_name(item),
                             "real_money", round(float(usd), 2)))
                pur_id += 1
    p = pd.DataFrame(rows, columns=["purchase_id", "player_id", "purchase_time",
                                    "item_name", "payment_type", "usd_amount"])
    return p


# --------------------------------------------------------------------------- #
#  6. ITEMS dimension (clean reference table, with one duplicate injected)
# --------------------------------------------------------------------------- #
def make_items():
    df = pd.DataFrame(ITEMS, columns=["item_name", "slot", "base_price_soft",
                                      "design_power", "is_premium"])
    return df


# --------------------------------------------------------------------------- #
#  Inject duplicates & missing values, then write
# --------------------------------------------------------------------------- #
def inject_messiness(name, df):
    # duplicate a handful of rows
    if len(df) > 50:
        dup = df.sample(n=max(2, len(df) // 500), random_state=7)
        df = pd.concat([df, dup], ignore_index=True)
    return df


def punch_missing(df, cols, frac=0.02):
    for c in cols:
        if c in df.columns:
            idx = RNG.choice(len(df), size=int(len(df) * frac), replace=False)
            df.loc[idx, c] = np.nan
    return df


def main():
    players = make_players()
    sessions = make_sessions(players)
    matches = make_matches(players, sessions)
    currency = make_currency(players, sessions)
    purchases = make_purchases(players, sessions)
    items = make_items()

    # drop internal helper cols before saving the players table
    players_out = players.drop(columns=["prop_", "install_dt_"]).copy()

    # ---- inject realistic missingness ----
    players_out = punch_missing(players_out, ["country", "acquisition_channel"], 0.03)
    sessions = punch_missing(sessions, ["duration_min"], 0.015)
    purchases = punch_missing(purchases, ["usd_amount"], 0.01)

    # ---- inject duplicate rows ----
    players_out = inject_messiness("players", players_out)
    matches = inject_messiness("matches", matches)
    currency = inject_messiness("currency", currency)
    items = pd.concat([items, items.iloc[[0]]], ignore_index=True)   # 1 dup item row

    # ---- write ----
    players_out.to_csv(HERE / "players.csv", index=False)
    sessions.to_csv(HERE / "sessions.csv", index=False)
    matches.to_csv(HERE / "matches.csv", index=False)
    currency.to_csv(HERE / "currency_transactions.csv", index=False)
    purchases.to_csv(HERE / "purchases.csv", index=False)
    items.to_csv(HERE / "items.csv", index=False)

    print("SYNTHETIC raw data written to", HERE)
    for fn, d in [("players", players_out), ("sessions", sessions),
                  ("matches", matches), ("currency_transactions", currency),
                  ("purchases", purchases), ("items", items)]:
        print(f"  {fn:24s} {d.shape}")


if __name__ == "__main__":
    main()
