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
                          used to show the constituents in the downloaded snapshot.

WHY THESE SOURCES
-----------------
GitHub's curated "datasets/" collection mirrors the SAME underlying real data
(Shiller, CBOE, LBMA) exposed by yfinance / FRED and is openly downloadable, so
we use it (see NOTES.md). This keeps Project 3 a genuine REAL-DATA project.

If any source is unavailable, the download exits without replacing the existing
CSV files. The optional --synthetic flag writes a marked fixture set that the
real-data analysis rejects.

HOW TO RUN
----------
    python download_data.py
"""

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent

SOURCES = {
    "raw_sp500.csv": "https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv",
    "raw_vix.csv": "https://raw.githubusercontent.com/datasets/finance-vix/main/data/vix-daily.csv",
    "raw_gold.csv": "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv",
    "raw_constituents.csv": "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv",
}


SYNTHETIC_MARKER = "_SYNTHETIC_FALLBACK_USED"
INCOMPLETE_MARKER = "_DOWNLOAD_INCOMPLETE"


def download_real_data(output_dir: Path) -> None:
    """Write the complete real-data set to a staging directory."""
    for filename, url in SOURCES.items():
        frame = pd.read_csv(url)
        if frame.empty:
            raise ValueError(f"No rows returned for {filename}")
        frame.to_csv(output_dir / filename, index=False)
        print(f"  downloaded {filename:24s} {len(frame):>6,} rows  <- {url}")


def write_synthetic_data(output_dir: Path) -> None:
    """Write deterministic stand-ins for downloader and pipeline testing."""
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
    sp.to_csv(output_dir / "raw_sp500.csv", index=False)

    days = pd.date_range("1990-01-01", "2026-06-12", freq="B")
    vclose = np.clip(rng.normal(19, 7, len(days)).cumsum() * 0 + rng.gamma(4, 4, len(days)), 9, 80)
    pd.DataFrame({
        "DATE": days.strftime("%Y-%m-%d"),
        "OPEN": vclose, "HIGH": vclose * 1.05, "LOW": vclose * 0.95, "CLOSE": vclose.round(2),
    }).to_csv(output_dir / "raw_vix.csv", index=False)

    gold = 35 * np.exp(np.linspace(0, 4.8, len(months)) + rng.normal(0, 0.03, len(months)).cumsum() * 0.1)
    pd.DataFrame({"Date": months.strftime("%Y-%m"), "Price": gold.round(2)}).to_csv(output_dir / "raw_gold.csv", index=False)

    pd.DataFrame({
        "Symbol": ["AAA", "BBB", "CCC"],
        "Security": ["Synthetic Co A", "Synthetic Co B", "Synthetic Co C"],
        "GICS Sector": ["Information Technology", "Financials", "Health Care"],
    }).to_csv(output_dir / "raw_constituents.csv", index=False)

def refresh_data(*, synthetic: bool = False) -> None:
    with TemporaryDirectory(dir=HERE, prefix=".market-data-") as staging:
        staged = Path(staging)
        if synthetic:
            write_synthetic_data(staged)
        else:
            download_real_data(staged)

        incomplete = HERE / INCOMPLETE_MARKER
        provenance = HERE / SYNTHETIC_MARKER
        incomplete.write_text("Market data replacement did not finish.\n")
        if synthetic:
            provenance.write_text("Synthetic fixtures were explicitly requested.\n")

        for filename in SOURCES:
            (staged / filename).replace(HERE / filename)

        if not synthetic:
            provenance.unlink(missing_ok=True)
        incomplete.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synthetic", action="store_true",
                        help="Replace local files with marked synthetic fixtures for testing.")
    args = parser.parse_args()

    try:
        refresh_data(synthetic=args.synthetic)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Market data refresh failed: {exc}\n")
    print("Wrote synthetic fixtures." if args.synthetic else "Wrote all four real datasets.")


if __name__ == "__main__":
    main()
