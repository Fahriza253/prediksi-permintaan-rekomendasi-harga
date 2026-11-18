"""Pipeline prapemrosesan (M2): bersihkan, imputasi, fitur turunan, simpan artefak.

Transformasi utama:
- Filter baris tidak valid (tanggal/harga produk).
- Imputasi median hanya dari rentang **latih** (menghindari leakage label/statistik masa depan).
- Fitur per-baris: selisih & rasio harga vs pesaing; kolom diskon & musim liburan dipertahankan.
- Cutoff tanggal latih/uji dicatat untuk M4/M5.

Jalankan: ``python -m py_prediction_system.preprocessing.pipeline``
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from py_prediction_system.config import (
    DEFAULT_DATASET_PATH,
    DEFAULT_PREPROCESSING_METADATA_PATH,
    DEFAULT_PROCESSED_PATH,
    TRAIN_FRACTION,
)
from py_prediction_system.data.profile import DATE_COLUMN, DEMAND_COLUMN, load_dataset

IMPUTE_COLUMNS = ("harga_pesaing", DEMAND_COLUMN)
PRICE_COLUMN = "harga_produk"
COMPETITOR_COLUMN = "harga_pesaing"
DISCOUNT_COLUMN = "persen_diskon"
HOLIDAY_COLUMN = "musim_liburan"
DERIVED_DIFF = "selisih_harga_pesaing"
DERIVED_RATIO = "rasio_harga_pesaing"

MODEL_FEATURE_COLUMNS = (
    PRICE_COLUMN,
    COMPETITOR_COLUMN,
    DISCOUNT_COLUMN,
    HOLIDAY_COLUMN,
    DERIVED_DIFF,
    DERIVED_RATIO,
)


@dataclass(frozen=True)
class PreprocessMetadata:
    source_path: str
    output_path: str
    n_rows_raw: int
    n_rows_dropped: int
    train_fraction: float
    train_cutoff_exclusive: str
    train_rows: int
    test_rows: int
    imputation_medians: dict[str, float]
    imputation_fit_scope: str
    model_feature_columns: tuple[str, ...]
    target_column: str
    date_column: str
    no_future_leakage: str


def temporal_train_cutoff(dates: pd.Series, train_fraction: float) -> pd.Timestamp:
    """Tanggal pertama yang masuk set tes (latih = tanggal < cutoff)."""
    ordered = dates.sort_values().reset_index(drop=True)
    train_count = int(len(ordered) * train_fraction)
    if train_count <= 0 or train_count >= len(ordered):
        raise ValueError("train_fraction menghasilkan split kosong")
    return pd.Timestamp(ordered.iloc[train_count])


def drop_invalid_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    work = df.sort_values(DATE_COLUMN).reset_index(drop=True)
    valid = (
        work[DATE_COLUMN].notna()
        & work[PRICE_COLUMN].notna()
        & (work[PRICE_COLUMN] > 0)
    )
    cleaned = work.loc[valid].reset_index(drop=True)
    return cleaned, before - len(cleaned)


def fit_imputation_medians(df_train: pd.DataFrame, columns: tuple[str, ...]) -> dict[str, float]:
    medians: dict[str, float] = {}
    for col in columns:
        if col not in df_train.columns:
            raise KeyError(col)
        medians[col] = float(df_train[col].median())
    return medians


def apply_imputation(df: pd.DataFrame, medians: dict[str, float]) -> pd.DataFrame:
    out = df.copy()
    for col, value in medians.items():
        out[col] = out[col].fillna(value)
    return out


def add_derived_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """Fitur hanya dari kolom baris yang sama (tanpa rolling / masa depan)."""
    out = df.copy()
    comp = out[COMPETITOR_COLUMN]
    out[DERIVED_DIFF] = out[PRICE_COLUMN] - comp
    out[DERIVED_RATIO] = out[PRICE_COLUMN] / comp
    if DISCOUNT_COLUMN not in out.columns:
        raise KeyError(DISCOUNT_COLUMN)
    if HOLIDAY_COLUMN not in out.columns:
        raise KeyError(HOLIDAY_COLUMN)
    return out


def build_preprocess_metadata(
    source_path: Path,
    output_path: Path,
    n_rows_raw: int,
    n_rows_dropped: int,
    cutoff: pd.Timestamp,
    df: pd.DataFrame,
    medians: dict[str, float],
) -> PreprocessMetadata:
    train_mask = df[DATE_COLUMN] < cutoff
    return PreprocessMetadata(
        source_path=str(source_path),
        output_path=str(output_path),
        n_rows_raw=n_rows_raw,
        n_rows_dropped=n_rows_dropped,
        train_fraction=TRAIN_FRACTION,
        train_cutoff_exclusive=str(cutoff.date()),
        train_rows=int(train_mask.sum()),
        test_rows=int((~train_mask).sum()),
        imputation_medians=medians,
        imputation_fit_scope="Median dihitung hanya pada baris latih (tanggal < cutoff); diterapkan ke seluruh data.",
        model_feature_columns=MODEL_FEATURE_COLUMNS,
        target_column=DEMAND_COLUMN,
        date_column=DATE_COLUMN,
        no_future_leakage="Fitur turunan dan penanda musim per-baris; tidak ada agregasi rolling atau statistik global dari masa depan.",
    )


def run_preprocessing(
    input_path: Path | None = None,
    output_path: Path | None = None,
    metadata_path: Path | None = None,
    train_fraction: float = TRAIN_FRACTION,
) -> tuple[pd.DataFrame, PreprocessMetadata]:
    source = input_path or DEFAULT_DATASET_PATH
    out_path = output_path or DEFAULT_PROCESSED_PATH
    meta_path = metadata_path or DEFAULT_PREPROCESSING_METADATA_PATH

    raw = load_dataset(source)
    n_raw = len(raw)
    cleaned, dropped = drop_invalid_rows(raw)
    cutoff = temporal_train_cutoff(cleaned[DATE_COLUMN], train_fraction)
    train_df = cleaned.loc[cleaned[DATE_COLUMN] < cutoff]
    medians = fit_imputation_medians(train_df, IMPUTE_COLUMNS)
    imputed = apply_imputation(cleaned, medians)
    featured = add_derived_price_features(imputed)

    leftover = featured[DEMAND_COLUMN].isna().sum()
    if leftover:
        featured = featured.loc[featured[DEMAND_COLUMN].notna()].reset_index(drop=True)

    meta = build_preprocess_metadata(
        source, out_path, n_raw, dropped, cutoff, featured, medians
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(out_path, index=False)
    meta_path.write_text(
        json.dumps(asdict(meta), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return featured, meta


def load_preprocessing_metadata(path: Path | None = None) -> dict[str, Any]:
    meta_path = path or DEFAULT_PREPROCESSING_METADATA_PATH
    return json.loads(meta_path.read_text(encoding="utf-8"))


def split_train_test(
    df: pd.DataFrame,
    cutoff: pd.Timestamp | str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if cutoff is None:
        meta = load_preprocessing_metadata()
        cutoff = pd.Timestamp(meta["train_cutoff_exclusive"])
    else:
        cutoff = pd.Timestamp(cutoff)
    train = df.loc[df[DATE_COLUMN] < cutoff].copy()
    test = df.loc[df[DATE_COLUMN] >= cutoff].copy()
    return train, test


def main() -> None:
    df, meta = run_preprocessing()
    print(f"Wrote {meta.output_path} ({len(df)} rows)")
    print(f"Metadata: {DEFAULT_PREPROCESSING_METADATA_PATH}")
    print(f"Train cutoff (test starts): {meta.train_cutoff_exclusive}")
    print(f"Train / test rows: {meta.train_rows} / {meta.test_rows}")


if __name__ == "__main__":
    main()