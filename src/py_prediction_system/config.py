"""Path terpusat untuk dataset dan artefak."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = REPO_ROOT / "data" / "raw"
DEFAULT_DATASET_PATH = RAW_DATA_DIR / "synthetic_demand.csv"

PROCESSED_DATA_DIR = REPO_ROOT / "data" / "processed"
DEFAULT_PROCESSED_PATH = PROCESSED_DATA_DIR / "demand_preprocessed.csv"
DEFAULT_PREPROCESSING_METADATA_PATH = PROCESSED_DATA_DIR / "preprocessing_metadata.json"

# Pembagian latih sesuai ADR-0001; cutoff dipakai M4/M5.
TRAIN_FRACTION = 0.8

OUTPUTS_DIR = REPO_ROOT / "outputs"
MODELS_DIR = OUTPUTS_DIR / "models"
FIGURES_DIR = OUTPUTS_DIR / "figures"
METRICS_DIR = OUTPUTS_DIR / "metrics"
REPORTS_DIR = OUTPUTS_DIR / "reports"

REPORT_DIR = REPO_ROOT / "report"