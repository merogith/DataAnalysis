"""
download_data.py — Fetch REAL financial market data for Project 3 (flagship).

WHAT THIS DOES
--------------
Downloads four real, public datasets and saves them as raw_*.csv in this folder:

  1. raw_sp500.csv        S&P 500 index, MONTHLY, since 1871 (Robert Shiller's
                          long-run dataset). Includes price, dividends, earnings,
                          the Consumer Price Index (CPI, a measure of inflation),
                          the 10-year interest rate, inflation-adjusted ("real")
                          values, and CAPE / PE10 (a famous valuation ratio).
  2. raw_vix.csv          CBOE Volatility Index ("VIX", the market's "fear gauge"),
                          DAILY, since 1990.
  3. raw_gold.csv         Gold price, MONTHLY, long history.
  4. raw_constituents.csv The current list of S&P 500 companies and their sector,
                          used to show what the index is made of today.

WHY THESE SOURCES
-----------------
The project brief asked for yfinance / FRED. In this sandbox those hosts are
blocked by the network policy (see NOTES.md). GitHub's curated "datasets/"
collection mirrors the SAME underlying real data (Shiller, CBOE, LBMA) and IS
reachable, so we use it. This keeps Project 3 a genuine REAL-DATA project.

If the network is unavailable, the script falls back to a clearly-labelled
synthetic generator so the rest of the pipeline still runs reproducibly.

HOW TO RUN
----------
    python download_data.py
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent

SOURCES = {
    "raw_sp500.csv": "https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv",
    "raw_vix.csv": "https://raw.githubusercontent.com/datasets/finance-vix/main/data/vix-daily.csv",
    "raw_gold.csv": "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv",
    "raw_constituents.csv": "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv",
}


def try_download() -> bool:
    """Attempt to download every source. Return True only if all succeed."""
    ok = True
    for fname, url in SOURCES.items():
        try:
            df = pd.read_csv(url)
            df.to_csv(HERE / fname, index=False)
            print(f"  downloaded {fname:24s} {len(df):>6,} rows  <- {url}")
        except Exception as exc:  # noqa: BLE001 - we want any failure to trigger fallback
            print(f"  FAILED     {fname:24s} ({exc})")
            ok = False
    return ok


def synthetic_fallback() -> None:
    """Generate clearly-labelled SYNTHETIC stand-ins if the real data is blocked."""
    print("  network unreachable -> generating SYNTHETIC fallback data")
    rng = np.random.default_rng(42)

    # Monthly S&P 500-like series with drift + noise
    months = pd.date_range("1950-01-01", "2026-05-01", freq="MS")
    drift = np.linspace(0, 4.2, len(months))            # exponential-ish growth in log space
    price = 20 * np.exp(drift + rng.normal(0, 0.04, len(months)).cumsum() * 0.1)
    cpi = 24 * np.exp(np.linspace(0, 2.4, len(months)))  # rising price level
    sp = pd.DataFrame({
        "Date": months.strftime("%Y-%m-%d"),
        "SP500": price.round(2),
        "Dividend": (price * 0.02).round(2),
        "Earnings": (price * 0.05).round(2),
        "Consumer Price Index": cpi.round(2),
        "Long Interest Rate": rng.uniform(1.5, 8, len(months)).round(2),
        "Real Price": price.round(2),
        "Real Dividend": (price * 0.02).round(2),
        "Real Earnings": (price * 0.05).round(2),
        "PE10": rng.uniform(8, 35, len(months)).round(2),
    })
    sp.to_csv(HERE / "raw_sp500.csv", index=False)

    days = pd.date_range("1990-01-01", "2026-06-12", freq="B")
    vclose = np.clip(rng.normal(19, 7, len(days)).cumsum() * 0 + rng.gamma(4, 4, len(days)), 9, 80)
    pd.DataFrame({
        "DATE": days.strftime("%Y-%m-%d"),
        "OPEN": vclose, "HIGH": vclose * 1.05, "LOW": vclose * 0.95, "CLOSE": vclose.round(2),
    }).to_csv(HERE / "raw_vix.csv", index=False)

    gold = 35 * np.exp(np.linspace(0, 4.8, len(months)) + rng.normal(0, 0.03, len(months)).cumsum() * 0.1)
    pd.DataFrame({"Date": months.strftime("%Y-%m"), "Price": gold.round(2)}).to_csv(HERE / "raw_gold.csv", index=False)

    pd.DataFrame({
        "Symbol": ["AAA", "BBB", "CCC"],
        "Security": ["Synthetic Co A", "Synthetic Co B", "Synthetic Co C"],
        "GICS Sector": ["Information Technology", "Financials", "Health Care"],
    }).to_csv(HERE / "raw_constituents.csv", index=False)

    # Leave a marker so the README/NOTES can detect which path was used.
    (HERE / "_SYNTHETIC_FALLBACK_USED").write_text("Synthetic fallback data was generated.\n")


def main() -> None:
    print("Project 3 — downloading REAL financial data...")
    marker = HERE / "_SYNTHETIC_FALLBACK_USED"
    if marker.exists():
        marker.unlink()
    if not try_download():
        synthetic_fallback()
        print("DONE (synthetic fallback).")
        sys.exit(0)
    print("DONE (real data).")


if __name__ == "__main__":
    main()
