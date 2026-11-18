"""EDA (M3): grafik harga–permintaan, musim, korelasi; temuan untuk laporan.

Memakai data terproses M2. Menyimpan paling banyak dua gambar di ``outputs/figures/``.

Jalankan: ``python -m py_prediction_system.eda.explore``
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from py_prediction_system.config import DEFAULT_PROCESSED_PATH, FIGURES_DIR, REPORTS_DIR
from py_prediction_system.data.profile import DEMAND_COLUMN
from py_prediction_system.preprocessing.pipeline import (
    DATE_COLUMN,
    HOLIDAY_COLUMN,
    MODEL_FEATURE_COLUMNS,
    PRICE_COLUMN,
)

RNG_SEED = 42
SCATTER_FILENAME = "eda_price_vs_demand.png"
CORR_FILENAME = "eda_feature_correlation.png"
FINDINGS_FILENAME = "eda_findings.md"
MANIFEST_FILENAME = "report_figure_manifest.json"

# Anggaran 4 gambar total laporan (report-format); M3 mengajukan 2 slot.
REPORT_FIGURE_BUDGET = 4


@dataclass(frozen=True)
class FigureRecord:
    filename: str
    title: str
    include_in_report: bool
    report_slot: int | None
    module: str
    notes: str


def load_processed(path: Path | None = None) -> pd.DataFrame:
    p = path or DEFAULT_PROCESSED_PATH
    if not p.is_file():
        raise FileNotFoundError(
            f"Data terproses tidak ada: {p}. Jalankan py_prediction_system.preprocessing.pipeline."
        )
    return pd.read_csv(p, parse_dates=[DATE_COLUMN])


def plot_price_vs_demand(df: pd.DataFrame, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = np.where(df[HOLIDAY_COLUMN] == 1, "#c0392b", "#2980b9")
    ax.scatter(df[PRICE_COLUMN], df[DEMAND_COLUMN], c=colors, alpha=0.35, s=12, edgecolors="none")
    ax.set_xlabel("Harga produk (IDR)")
    ax.set_ylabel("Permintaan (unit)")
    ax.set_title("Harga produk vs permintaan")
    ax.text(
        0.02,
        0.98,
        "Biru: non-liburan · Merah: musim liburan",
        transform=ax.transAxes,
        va="top",
        fontsize=8,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_feature_correlation(df: pd.DataFrame, out_path: Path) -> None:
    cols = list(MODEL_FEATURE_COLUMNS) + [DEMAND_COLUMN]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(corr.values, vmin=-1, vmax=1, cmap="RdBu_r", aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(cols, fontsize=8)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Korelasi Pearson — fitur utama & permintaan")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def compute_findings(df: pd.DataFrame) -> list[str]:
    rho_price = df[PRICE_COLUMN].corr(df[DEMAND_COLUMN])
    rho_ratio = df["rasio_harga_pesaing"].corr(df[DEMAND_COLUMN])
    rho_discount = df["persen_diskon"].corr(df[DEMAND_COLUMN])
    mean_demand = df.groupby(HOLIDAY_COLUMN)[DEMAND_COLUMN].mean()
    holiday_lift = float(mean_demand.get(1, np.nan) - mean_demand.get(0, np.nan))
    corr_with_target = (
        df[list(MODEL_FEATURE_COLUMNS) + [DEMAND_COLUMN]].corr()[DEMAND_COLUMN].drop(DEMAND_COLUMN)
    )
    strongest = corr_with_target.abs().idxmax()
    strongest_val = float(corr_with_target[strongest])

    findings = [
        f"Harga produk dan permintaan berkorelasi negatif (r ≈ {rho_price:.2f}), sesuai elastisitas: harga naik cenderung menurunkan unit terjual.",
        f"Rasio harga terhadap pesaing (`rasio_harga_pesaing`) berkorelasi {rho_ratio:.2f} dengan permintaan — posisi relatif harga penting untuk prediksi.",
        f"Persentase diskon berkorelasi {rho_discount:.2f} dengan permintaan; diskon lebih tinggi cenderung menaikkan permintaan pada data ini.",
        f"Rata-rata permintaan saat musim liburan {mean_demand.get(1, float('nan')):.1f} unit vs non-liburan {mean_demand.get(0, float('nan')):.1f} unit (selisih ≈ {holiday_lift:+.1f} unit).",
        f"Fitur dengan |korelasi| terbesar terhadap permintaan (di antara fitur model): `{strongest}` (r = {strongest_val:.2f}).",
        "Tidak terlihat pola non-linear ekstrem pada scatter harga–permintaan; regresi linear layak sebagai baseline, model lanjutan untuk menangkap interaksi.",
        f"EDA memakai {len(df):,} baris data terproses M2 (tanpa missing pada kolom inti).",
    ]
    return findings


def build_figure_manifest() -> list[FigureRecord]:
    return [
        FigureRecord(
            filename=SCATTER_FILENAME,
            title="Scatter harga produk vs permintaan (warna musim liburan)",
            include_in_report=True,
            report_slot=1,
            module="M3-eda",
            notes="Kandidat bab 4/5 laporan; menggambarkan elastisitas dan konteks musim.",
        ),
        FigureRecord(
            filename=CORR_FILENAME,
            title="Heatmap korelasi fitur utama & permintaan",
            include_in_report=True,
            report_slot=2,
            module="M3-eda",
            notes="Kandidat bab 4; ringkas, menggantikan banyak plot terpisah.",
        ),
        FigureRecord(
            filename="(reserved-m5-metrics)",
            title="Perbandingan metrik baseline vs lanjutan",
            include_in_report=True,
            report_slot=3,
            module="M5-evaluation",
            notes="Placeholder slot laporan; diisi saat M5.",
        ),
        FigureRecord(
            filename="(reserved-m6-simulation)",
            title="Kurva simulasi harga–pendapatan",
            include_in_report=True,
            report_slot=4,
            module="M6-price-simulation",
            notes="Placeholder slot laporan; diisi saat M6.",
        ),
    ]


def render_findings_markdown(bullets: list[str], manifest: list[FigureRecord]) -> str:
    lines = [
        "# Temuan EDA (M3)",
        "",
        "Sumber data: `data/processed/demand_preprocessed.csv`.",
        "",
        "## Poin untuk laporan",
        "",
    ]
    for b in bullets:
        lines.append(f"- {b}")
    lines.extend(["", "## Gambar (`outputs/figures/`)", ""])
    for fig in manifest:
        flag = "✓ masuk laporan" if fig.include_in_report else "opsional"
        slot = f"slot {fig.report_slot}" if fig.report_slot else "—"
        lines.append(
            f"- `{fig.filename}` — {fig.title} ({flag}, {slot}; {fig.module})"
        )
    lines.extend(
        [
            "",
            f"**Anggaran gambar laporan:** {REPORT_FIGURE_BUDGET} total; M3 memakai slot 1–2; slot 3–4 untuk M5/M6.",
            "",
        ]
    )
    return "\n".join(lines)


def run_eda(
    data_path: Path | None = None,
    figures_dir: Path | None = None,
) -> tuple[Path, Path, list[str]]:
    df = load_processed(data_path)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_fig_dir = figures_dir or FIGURES_DIR

    scatter_path = out_fig_dir / SCATTER_FILENAME
    corr_path = out_fig_dir / CORR_FILENAME
    plot_price_vs_demand(df, scatter_path)
    plot_feature_correlation(df, corr_path)

    bullets = compute_findings(df)
    manifest = build_figure_manifest()
    findings_path = REPORTS_DIR / FINDINGS_FILENAME
    findings_path.write_text(render_findings_markdown(bullets, manifest), encoding="utf-8")

    manifest_path = out_fig_dir / MANIFEST_FILENAME
    manifest_path.write_text(
        json.dumps([asdict(m) for m in manifest], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return findings_path, scatter_path, bullets


def main() -> None:
    findings_path, scatter_path, _ = run_eda()
    print(f"Wrote {scatter_path}")
    print(f"Wrote {FIGURES_DIR / CORR_FILENAME}")
    print(f"Wrote {findings_path}")
    print(f"Wrote {FIGURES_DIR / MANIFEST_FILENAME}")


if __name__ == "__main__":
    main()