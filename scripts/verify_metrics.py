"""Independent checks of the exported metrics against the checked-in raw snapshots."""
from pathlib import Path
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def verify_game():
    project = ROOT / "project-2-game-economy"
    data, dashboard = project / "data", project / "dashboard"
    sessions = pd.read_csv(data / "sessions.csv").drop_duplicates()
    players = pd.read_csv(dashboard / "dim_player.csv").set_index("player_id")
    metrics = json.loads((dashboard / "metrics.json").read_text())
    for day in (1, 7, 30):
        active = set(sessions.loc[sessions.day_since_install == day, "player_id"])
        expected = players.index.isin(active).astype(int)
        np.testing.assert_array_equal(players[f"active_d{day}"], expected)
        assert np.isclose(expected.mean(), metrics["retention"][f"d{day}"])
    ledger = pd.read_csv(data / "currency_transactions.csv").drop_duplicates()
    totals = ledger.groupby("player_id").amount.sum().sort_index()
    wallets = pd.read_csv(dashboard / "wallet_balances.csv").set_index("player_id")
    pd.testing.assert_series_equal(totals, wallets.final_wallet.sort_index(),
                                   check_names=False, check_dtype=False)
    assert totals.loc[1] == -27  # Tied timestamps previously returned 127.
    ratio = -ledger.loc[ledger.flow == "sink", "amount"].sum() / ledger.loc[ledger.flow == "source", "amount"].sum()
    assert np.isclose(ratio, metrics["sink_recovery"])
    fact = pd.read_csv(dashboard / "fact_daily_economy.csv")
    assert fact.date.is_monotonic_increasing
    np.testing.assert_allclose(fact.net_coins.cumsum(), fact.cum_net_coins)
    purchases = pd.read_csv(data / "purchases.csv").drop_duplicates()
    raw_players = pd.read_csv(data / "players.csv").drop_duplicates().set_index("player_id")
    purchase_days = (pd.to_datetime(purchases.purchase_time) -
                     pd.to_datetime(purchases.player_id.map(raw_players.install_date))).dt.days
    early = set(purchases.loc[purchase_days.between(0, 3), "player_id"])
    later = set(purchases.loc[purchase_days.between(4, 30), "player_id"])
    np.testing.assert_array_equal(players.eligible_day4, ~players.index.isin(early))
    np.testing.assert_array_equal(players.pays_d4_d30, players.index.isin(later).astype(int))
    assert metrics["payer_model"]["eligible_players"] == int(players.eligible_day4.sum())
    print("PASS game: exact retention, all wallets, period recovery, temporal target and ordered exports")


def verify_finance():
    project = ROOT / "project-3-finance"
    raw = pd.read_csv(project / "data/raw_sp500.csv", parse_dates=["Date"]).set_index("Date")
    fact = pd.read_csv(project / "dashboard/fact_market_monthly.csv", parse_dates=["month"]).set_index("month")
    metrics = json.loads((project / "dashboard/metrics.json").read_text())
    real = raw["Real Price"].replace(0, np.nan)
    expected = real.pct_change(fill_method=None).round(4)
    np.testing.assert_allclose(fact.real_return_m, expected, equal_nan=True)
    assert fact.loc[real.isna(), "real_return_m"].isna().all()
    valid = real.dropna()
    years = (valid.index[-1] - valid.index[0]).days / 365.25
    cagr = (valid.iloc[-1] / valid.iloc[0]) ** (1 / years) - 1
    assert np.isclose(cagr, metrics["real_price_cagr"])
    cape = raw.PE10.replace(0, np.nan).dropna()
    assert metrics["valuation_as_of"] == str(cape.index[-1].date())
    assert np.isclose(metrics["latest_cape"], cape.iloc[-1])
    calendar = pd.read_csv(project / "dashboard/calendar_returns.csv")
    december_years = set(raw.loc[raw.index.month == 12].index.year)
    assert set(calendar.year) <= december_years
    assert 2026 not in set(calendar.year)  # Shipped snapshot ends in May 2026.
    print("PASS finance: missing returns, real-series CAGR interval, last-valid valuation and full calendar years")


def verify_pharma():
    dashboard = ROOT / "project-1-pharma-crm/dashboard"
    fact = pd.read_csv(dashboard / "fact_scripts.csv")
    hcp = pd.read_csv(dashboard / "dim_hcp.csv")
    region = pd.read_csv(dashboard / "dim_region.csv")
    assert hcp.hcp_id.is_unique and region.region_id.is_unique
    assert hcp.region_id.isin(region.region_id).all()
    joined = fact.merge(hcp[["hcp_id", "region_id"]], on="hcp_id", validate="many_to_one",
                       suffixes=("_fact", "_hcp"))
    assert (joined.region_id_fact == joined.region_id_hcp).all()
    assert len(joined) == len(fact)
    assert hcp.groupby("region_id").size().sum() == len(hcp)
    print("PASS pharma: region→physician→prescription filter keys reconcile")


if __name__ == "__main__":
    verify_game()
    verify_finance()
    verify_pharma()
