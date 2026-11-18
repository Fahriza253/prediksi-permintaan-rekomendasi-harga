"""Simulasi harga (M6): grid harga → permintaan → pendapatan → rekomendasi.

Konteks fitur non-harga dipegang tetap pada median set latih (skenario tunggal terdokumentasi).

Jalankan: ``python -m py_prediction_system.simulation.price_grid``
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from py_prediction_system.config import FIGURES_DIR, METRICS_DIR, MODELS_DIR, REPORTS_DIR
from py_prediction_system.eda.explore import load_processed
from py_prediction_system.preprocessing.pipeline import (
    COMPETITOR_COLUMN,
    DERIVED_DIFF,
    DERIVED_RATIO,
    DISCOUNT_COLUMN,
    HOLIDAY_COLUMN,
    MODEL_FEATURE_COLUMNS,
    PRICE_COLUMN,
    split_train_test,
)

FIGURE_NAME = "simulation_price_revenue_curve.png"
RESULT_JSON = "price_recommendation.json"
REPORT_SNIPPET = "simulation_report_draft.md"


def load_primary_model_name() -> str:
    metrics_path = METRICS_DIR / "metrics_test.json"
    data = json.loads(metrics_path.read_text(encoding="utf-8"))
    return data["primary_model_for_simulation"]


def reference_context(train_df: pd.DataFrame) -> dict[str, float]:
    """Median fitur non-harga dari latih (skenario tetap saat menggeser harga)."""
    return {
        COMPETITOR_COLUMN: float(train_df[COMPETITOR_COLUMN].median()),
        DISCOUNT_COLUMN: float(train_df[DISCOUNT_COLUMN].median()),
        HOLIDAY_COLUMN: float(train_df[HOLIDAY_COLUMN].median()),
    }


def rows_for_price_grid(
    prices: np.ndarray,
    context: dict[str, float],
) -> pd.DataFrame:
    comp = context[COMPETITOR_COLUMN]
    rows = []
    for price in prices:
        rows.append(
            {
                PRICE_COLUMN: float(price),
                COMPETITOR_COLUMN: comp,
                DISCOUNT_COLUMN: context[DISCOUNT_COLUMN],
                HOLIDAY_COLUMN: context[HOLIDAY_COLUMN],
                DERIVED_DIFF: float(price) - comp,
                DERIVED_RATIO: float(price) / comp,
            }
        )
    return pd.DataFrame(rows)


def run_simulation(
    price_min: float | None = None,
    price_max: float | None = None,
    n_steps: int = 80,
) -> dict:
    df = load_processed()
    train_df, _ = split_train_test(df)
    ctx = reference_context(train_df)

    p10, p90 = train_df[PRICE_COLUMN].quantile(0.1), train_df[PRICE_COLUMN].quantile(0.9)
    lo = price_min if price_min is not None else float(p10)
    hi = price_max if price_max is not None else float(p90)
    prices = np.linspace(lo, hi, n_steps)

    model_name = load_primary_model_name()
    model = joblib.load(MODELS_DIR / f"{model_name}.joblib")
    grid_x = rows_for_price_grid(prices, ctx)
    demand = np.maximum(model.predict(grid_x[list(MODEL_FEATURE_COLUMNS)]), 0.0)
    revenue = prices * demand

    best_idx = int(np.argmax(revenue))
    result = {
        "model": model_name,
        "scenario": {
            "description": "Harga produk divariasikan; fitur lain pada median latih.",
            COMPETITOR_COLUMN: ctx[COMPETITOR_COLUMN],
            DISCOUNT_COLUMN: ctx[DISCOUNT_COLUMN],
            HOLIDAY_COLUMN: ctx[HOLIDAY_COLUMN],
        },
        "grid": {
            "price_min": lo,
            "price_max": hi,
            "steps": n_steps,
        },
        "rekomendasi_harga": {
            "harga_idr": float(prices[best_idx]),
            "permintaan_prediksi": float(demand[best_idx]),
            "pendapatan_prediksi": float(revenue[best_idx]),
            "kriteria": "Maksimalkan pendapatan = harga × permintaan pada grid.",
        },
        "sensitivitas": {
            "pendapatan_at_min_grid": float(revenue[0]),
            "pendapatan_at_max_grid": float(revenue[-1]),
            "demand_range_on_grid": [float(demand.min()), float(demand.max())],
        },
    }

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax1.plot(prices, demand, color="#2980b9", label="Permintaan (prediksi)")
    ax1.set_xlabel("Harga produk (IDR)")
    ax1.set_ylabel("Permintaan (unit)", color="#2980b9")
    ax2 = ax1.twinx()
    ax2.plot(prices, revenue, color="#27ae60", label="Pendapatan")
    ax2.set_ylabel("Pendapatan (IDR)", color="#27ae60")
    ax1.axvline(prices[best_idx], color="#c0392b", linestyle="--", linewidth=1, label="Rekomendasi")
    ax1.set_title("Simulasi harga: permintaan & pendapatan")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / FIGURE_NAME, dpi=150)
    plt.close(fig)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    (METRICS_DIR / RESULT_JSON).write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    rec = result["rekomendasi_harga"]
    draft = "\n".join(
        [
            "# Draft simulasi harga (M6)",
            "",
            f"Model: `{model_name}`.",
            f"Skenario: harga pesaing ≈ {ctx[COMPETITOR_COLUMN]:,.0f} IDR, "
            f"diskon median {ctx[DISCOUNT_COLUMN]:.1f}%, musim liburan={int(ctx[HOLIDAY_COLUMN])}.",
            "",
            f"**Rekomendasi harga:** **{rec['harga_idr']:,.0f} IDR** "
            f"(permintaan ≈ {rec['permintaan_prediksi']:.0f} unit, "
            f"pendapatan ≈ {rec['pendapatan_prediksi']:,.0f} IDR).",
            "",
            "Grafik: `outputs/figures/simulation_price_revenue_curve.png` (slot laporan 4).",
        ]
    )
    (REPORTS_DIR / REPORT_SNIPPET).write_text(draft, encoding="utf-8")

    _update_figure_manifest()
    return result


def _update_figure_manifest() -> None:
    manifest_path = FIGURES_DIR / "report_figure_manifest.json"
    if not manifest_path.is_file():
        return
    items = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in items:
        if item.get("report_slot") == 4:
            item["filename"] = FIGURE_NAME
            item["module"] = "M6-price-simulation"
            item["notes"] = "Kurva simulasi harga–pendapatan dengan titik rekomendasi."
    manifest_path.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    result = run_simulation()
    rec = result["rekomendasi_harga"]
    print(f"Wrote {FIGURES_DIR / FIGURE_NAME}")
    print(f"Wrote {METRICS_DIR / RESULT_JSON}")
    print(f"Rekomendasi harga: {rec['harga_idr']:,.0f} IDR")


if __name__ == "__main__":
    main()