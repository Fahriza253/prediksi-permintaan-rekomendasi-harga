"""Pelatihan model (M4): baseline Linear Regression + Random Forest, serialisasi.

Split latih/uji dari metadata M2. Seed tetap untuk reproduksi.

Jalankan: ``python -m py_prediction_system.models.train``
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from py_prediction_system.config import MODELS_DIR
from py_prediction_system.data.profile import DEMAND_COLUMN
from py_prediction_system.eda.explore import load_processed
from py_prediction_system.preprocessing.pipeline import (
    MODEL_FEATURE_COLUMNS,
    load_preprocessing_metadata,
    split_train_test,
)

RANDOM_SEED = 42
BASELINE_NAME = "baseline_linear_regression"
ADVANCED_NAME = "advanced_random_forest"
ARTIFACT_META_NAME = "training_manifest.json"


@dataclass(frozen=True)
class TrainingManifest:
    random_seed: int
    feature_columns: tuple[str, ...]
    target_column: str
    train_rows: int
    test_rows: int
    train_cutoff_exclusive: str
    baseline_model: str
    advanced_model: str
    baseline_artifact: str
    advanced_artifact: str


def build_baseline_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            ("model", LinearRegression()),
        ]
    )


def build_advanced_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "model",
                RandomForestRegressor(
                    n_estimators=200,
                    max_depth=12,
                    min_samples_leaf=4,
                    random_state=RANDOM_SEED,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def prepare_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    x = df[list(MODEL_FEATURE_COLUMNS)]
    y = df[DEMAND_COLUMN]
    return x, y


def save_artifact(pipeline: Pipeline, name: str, models_dir: Path) -> Path:
    models_dir.mkdir(parents=True, exist_ok=True)
    path = models_dir / f"{name}.joblib"
    joblib.dump(pipeline, path)
    return path


def run_training(
    data_path: Path | None = None,
    models_dir: Path | None = None,
) -> tuple[Pipeline, Pipeline, TrainingManifest]:
    df = load_processed(data_path)
    train_df, test_df = split_train_test(df)
    x_train, y_train = prepare_xy(train_df)
    x_test, y_test = prepare_xy(test_df)

    meta_raw = load_preprocessing_metadata()

    baseline = build_baseline_pipeline()
    advanced = build_advanced_pipeline()
    baseline.fit(x_train, y_train)
    advanced.fit(x_train, y_train)

    out_dir = models_dir or MODELS_DIR
    baseline_path = save_artifact(baseline, BASELINE_NAME, out_dir)
    advanced_path = save_artifact(advanced, ADVANCED_NAME, out_dir)

    manifest = TrainingManifest(
        random_seed=RANDOM_SEED,
        feature_columns=MODEL_FEATURE_COLUMNS,
        target_column=DEMAND_COLUMN,
        train_rows=len(train_df),
        test_rows=len(test_df),
        train_cutoff_exclusive=meta_raw["train_cutoff_exclusive"],
        baseline_model="sklearn LinearRegression + StandardScaler",
        advanced_model="sklearn RandomForestRegressor",
        baseline_artifact=str(baseline_path),
        advanced_artifact=str(advanced_path),
    )
    manifest_path = out_dir / ARTIFACT_META_NAME
    manifest_path.write_text(
        json.dumps(asdict(manifest), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Touch holdout for M5 (predictions optional stub in manifest sidecar)
    holdout_path = out_dir / "holdout_frames.joblib"
    joblib.dump(
        {"x_train": x_train, "y_train": y_train, "x_test": x_test, "y_test": y_test},
        holdout_path,
    )

    _ = y_test  # used in M5 evaluation
    return baseline, advanced, manifest


def load_training_manifest(models_dir: Path | None = None) -> dict[str, Any]:
    path = (models_dir or MODELS_DIR) / ARTIFACT_META_NAME
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    _, _, manifest = run_training()
    print(f"Baseline: {manifest.baseline_artifact}")
    print(f"Advanced: {manifest.advanced_artifact}")
    print(f"Features: {list(manifest.feature_columns)}")
    print(f"Train/test rows: {manifest.train_rows} / {manifest.test_rows}")


if __name__ == "__main__":
    main()