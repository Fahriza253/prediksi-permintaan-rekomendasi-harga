"""Buat dataset sintetis sesuai DATASET_GENERATOR_SPECS.md."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from py_prediction_system.config import DEFAULT_DATASET_PATH

NUM_ROWS = 2_500
MISSING_RATE = 0.02
RNG = np.random.default_rng(42)


def _holiday_window(dates: pd.DatetimeIndex) -> np.ndarray:
    month = dates.month
    holiday = (month == 12) | (month.isin([6, 7]))
    # Idul Fitri sintetis: beberapa blok 14 hari per tahun (seed tetap)
    extra = np.zeros(len(dates), dtype=int)
    for year in dates.year.unique():
        start = RNG.integers(0, max(1, len(dates[dates.year == year]) - 14))
        idx = np.where(dates.year == year)[0][start : start + 14]
        extra[idx] = 1
    return (holiday.astype(int) | extra).astype(int)


def build_dataframe(n_rows: int = NUM_ROWS) -> pd.DataFrame:
    start = pd.Timestamp("2022-01-01")
    dates = pd.date_range(start, periods=n_rows, freq="D")
    musim_liburan = _holiday_window(dates)

    base_price = 150_000 + RNG.normal(0, 2_000, n_rows).cumsum()
    base_price = np.clip(base_price, 80_000, 250_000)

    harga_pesaing = base_price * RNG.uniform(0.92, 1.08, n_rows)
    persen_diskon = np.where(musim_liburan, RNG.uniform(10, 35, n_rows), RNG.uniform(0, 15, n_rows))
    harga_produk = base_price * (1 - persen_diskon / 100)

    rel_price = harga_produk / harga_pesaing
    permintaan = (
        420
        - 180 * (rel_price - 1)
        + 12 * persen_diskon
        + 35 * musim_liburan
        + RNG.normal(0, 18, n_rows)
    )
    permintaan = np.clip(permintaan, 15, None)

    df = pd.DataFrame(
        {
            "tanggal": dates.strftime("%Y-%m-%d"),
            "harga_produk": np.round(harga_produk, 2),
            "harga_pesaing": np.round(harga_pesaing, 2),
            "persen_diskon": np.round(persen_diskon, 2),
            "musim_liburan": musim_liburan,
            "permintaan": np.round(permintaan, 2),
        }
    )

    for col in ("harga_pesaing", "permintaan"):
        mask = RNG.random(n_rows) < MISSING_RATE
        df.loc[mask, col] = np.nan

    return df


def write_dataset(output_path: Path | None = None) -> Path:
    path = output_path or DEFAULT_DATASET_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    df = build_dataframe()
    df.to_csv(path, index=False)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic demand dataset.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_DATASET_PATH,
        help="CSV output path",
    )
    args = parser.parse_args()
    out = write_dataset(args.output)
    print(f"Wrote {out} ({NUM_ROWS} rows)")


if __name__ == "__main__":
    main()