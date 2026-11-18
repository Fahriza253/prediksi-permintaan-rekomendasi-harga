"""Evaluasi (M5): MAE, RMSE, R² pada set uji; pilih model untuk M6.

Jalankan: ``python -m py_prediction_system.evaluation.metrics``
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import matplotlib.pyplot as plt

from py_prediction_system.config import FIGURES_DIR, METRICS_DIR, MODELS_DIR, REPORTS_DIR
from py_prediction_system.models.train import (
    ADVANCED_NAME,
    BASELINE_NAME,
    load_training_manifest,
)

METRICS_JSON = "metrics_test.json"
METRICS_CSV = "metrics_test.csv"
REPORT_SNIPPET = "evaluation_report_draft.md"
METRICS_FIGURE = "evaluation_metrics_comparison.png"


@dataclass(frozen=True)
class ModelMetrics:
    model: str
    mae: float
    rmse: float
    r2: float


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))
    return mae, rmse, r2


def evaluate_models(models_dir: Path | None = None) -> dict:
    mdir = models_dir or MODELS_DIR
    holdout = joblib.load(mdir / "holdout_frames.joblib")
    x_test = holdout["x_test"]
    y_test = holdout["y_test"].to_numpy()

    results: list[ModelMetrics] = []
    for name in (BASELINE_NAME, ADVANCED_NAME):
        pipe = joblib.load(mdir / f"{name}.joblib")
        pred = pipe.predict(x_test)
        mae, rmse, r2 = regression_metrics(y_test, pred)
        results.append(ModelMetrics(model=name, mae=mae, rmse=rmse, r2=r2))

    advanced = next(m for m in results if m.model == ADVANCED_NAME)
    baseline = next(m for m in results if m.model == BASELINE_NAME)
    if advanced.rmse < baseline.rmse:
        chosen = ADVANCED_NAME
        reason = "RMSE terendah pada set uji; menangkap non-linearitas lebih baik dari baseline linear."
    else:
        chosen = BASELINE_NAME
        reason = "Baseline linear unggul atau setara pada set uji; dipilih demi interpretabilitas."

    manifest = load_training_manifest(mdir)
    payload = {
        "split": "test",
        "train_cutoff_exclusive": manifest["train_cutoff_exclusive"],
        "test_rows": manifest["test_rows"],
        "metrics": [asdict(m) for m in results],
        "primary_model_for_simulation": chosen,
        "selection_reason": reason,
    }
    return payload


def metrics_to_csv_frame(metrics: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(metrics)


def render_report_draft(payload: dict) -> str:
    lines = [
        "# Draft evaluasi (M5) — bab Model & evaluasi",
        "",
        f"Set uji: {payload['test_rows']} baris (cutoff latih `{payload['train_cutoff_exclusive']}`).",
        "",
        "| Model | MAE | RMSE | R² |",
        "|-------|-----|------|-----|",
    ]
    for row in payload["metrics"]:
        lines.append(
            f"| {row['model']} | {row['mae']:.2f} | {row['rmse']:.2f} | {row['r2']:.3f} |"
        )
    lines.extend(
        [
            "",
            f"**Model utama untuk simulasi (M6):** `{payload['primary_model_for_simulation']}` — {payload['selection_reason']}",
            "",
        ]
    )
    return "\n".join(lines)


def plot_metrics_comparison(payload: dict, out_path: Path) -> None:
    labels = [row["model"].replace("_", "\n") for row in payload["metrics"]]
    rmse = [row["rmse"] for row in payload["metrics"]]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(labels, rmse, color=["#3498db", "#9b59b6"])
    ax.set_ylabel("RMSE (set uji)")
    ax.set_title("Perbandingan RMSE — baseline vs lanjutan")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _update_metrics_figure_manifest() -> None:
    manifest_path = FIGURES_DIR / "report_figure_manifest.json"
    if not manifest_path.is_file():
        return
    items = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in items:
        if item.get("report_slot") == 3:
            item["filename"] = METRICS_FIGURE
            item["module"] = "M5-evaluation"
            item["notes"] = "RMSE baseline vs Random Forest pada set uji."
    manifest_path.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")


def run_evaluation(models_dir: Path | None = None) -> Path:
    payload = evaluate_models(models_dir)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    json_path = METRICS_DIR / METRICS_JSON
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    csv_path = METRICS_DIR / METRICS_CSV
    metrics_to_csv_frame(payload["metrics"]).to_csv(csv_path, index=False)

    snippet_path = REPORTS_DIR / REPORT_SNIPPET
    snippet_path.write_text(render_report_draft(payload), encoding="utf-8")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_metrics_comparison(payload, FIGURES_DIR / METRICS_FIGURE)
    _update_metrics_figure_manifest()
    return json_path


def main() -> None:
    path = run_evaluation()
    payload = json.loads(path.read_text(encoding="utf-8"))
    print(f"Wrote {path}")
    print(f"Primary model: {payload['primary_model_for_simulation']}")
    for row in payload["metrics"]:
        print(f"  {row['model']}: MAE={row['mae']:.2f} RMSE={row['rmse']:.2f} R²={row['r2']:.3f}")


if __name__ == "__main__":
    main()