"""Profil dataset (M1): inventaris kolom, missing, outlier, dan ringkasan teks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from py_prediction_system.config import DEFAULT_DATASET_PATH, REPORTS_DIR

DATE_COLUMN = "tanggal"
DEMAND_COLUMN = "permintaan"
OUTLIER_COLUMNS = ("harga_produk", DEMAND_COLUMN)
MISSING_HANDLING_PLAN = {
    "harga_pesaing": "Imputasi median (M2); kolom fitur utama untuk selisih harga.",
    DEMAND_COLUMN: "Imputasi median (M2); baris tanpa target tidak dipakai untuk latih jika masih NA setelah imputasi.",
}


@dataclass(frozen=True)
class IqrOutlierSummary:
    method: str
    q1: float
    q3: float
    iqr: float
    lower_fence: float
    upper_fence: float
    count: int
    pct: float
    min_outlier: float | None
    max_outlier: float | None


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    dataset_path = path or DEFAULT_DATASET_PATH
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {dataset_path}")
    return pd.read_csv(dataset_path, parse_dates=[DATE_COLUMN])


def iqr_outlier_summary(series: pd.Series) -> IqrOutlierSummary:
    clean = series.dropna()
    q1 = float(clean.quantile(0.25))
    q3 = float(clean.quantile(0.75))
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    mask = (clean < lower_fence) | (clean > upper_fence)
    outlier_vals = clean[mask]
    return IqrOutlierSummary(
        method="IQR (Tukey 1.5×IQR)",
        q1=q1,
        q3=q3,
        iqr=iqr,
        lower_fence=lower_fence,
        upper_fence=upper_fence,
        count=int(mask.sum()),
        pct=round(100 * mask.mean(), 2),
        min_outlier=float(outlier_vals.min()) if not outlier_vals.empty else None,
        max_outlier=float(outlier_vals.max()) if not outlier_vals.empty else None,
    )


def build_profile_dict(df: pd.DataFrame, dataset_path: Path) -> dict[str, Any]:
    missing = {col: int(df[col].isna().sum()) for col in df.columns}
    missing_pct = {col: round(100 * df[col].isna().mean(), 2) for col in df.columns}
    inventory = []
    for col in df.columns:
        s = df[col]
        inventory.append(
            {
                "name": col,
                "dtype": str(s.dtype),
                "non_null": int(s.notna().sum()),
                "example_values": [repr(v) for v in s.dropna().head(3).tolist()],
            }
        )
    outliers = {
        col: asdict(iqr_outlier_summary(df[col])) for col in OUTLIER_COLUMNS if col in df.columns
    }
    expected = {
        "tanggal (validasi waktu & musim)": DATE_COLUMN in df.columns,
        "harga_pesaing": "harga_pesaing" in df.columns,
        "persen_diskon": "persen_diskon" in df.columns,
        "musim_liburan": "musim_liburan" in df.columns,
        DEMAND_COLUMN: DEMAND_COLUMN in df.columns,
    }
    return {
        "dataset_path": str(dataset_path),
        "format": "CSV (UTF-8), pemisah koma, satu baris header",
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "inventory": inventory,
        "missing_count": missing,
        "missing_pct": missing_pct,
        "missing_handling_plan": MISSING_HANDLING_PLAN,
        "outliers": outliers,
        "time_column": {
            "name": DATE_COLUMN,
            "min": str(df[DATE_COLUMN].min().date()) if DATE_COLUMN in df.columns else None,
            "max": str(df[DATE_COLUMN].max().date()) if DATE_COLUMN in df.columns else None,
            "chronological": bool(df[DATE_COLUMN].is_monotonic_increasing)
            if DATE_COLUMN in df.columns
            else False,
            "adr_reference": "docs/adr/0001-time-based-train-test-split.md",
        },
        "competitor_and_promo_flags": {
            "harga_pesaing": "harga_pesaing" in df.columns,
            "persen_diskon": "persen_diskon" in df.columns,
            "musim_liburan": "musim_liburan" in df.columns,
            "musim_liburan_levels": sorted(df["musim_liburan"].dropna().unique().tolist())
            if "musim_liburan" in df.columns
            else [],
        },
        "target_column": DEMAND_COLUMN,
        "expected_readme_features": expected,
        "missing_expected_features": [k for k, ok in expected.items() if not ok],
    }


def render_markdown(profile: dict[str, Any]) -> str:
    lines = [
        "# Laporan profil data (M1)",
        "",
        f"**Sumber:** `{profile['dataset_path']}`  ",
        f"**Format:** {profile['format']}  ",
        f"**Ukuran:** {profile['n_rows']:,} baris × {profile['n_columns']} kolom",
        "",
        "## Inventaris kolom",
        "",
        "| Kolom | Tipe pandas | Contoh nilai |",
        "|-------|-----------|--------------|",
    ]
    for row in profile["inventory"]:
        examples = ", ".join(row["example_values"])
        lines.append(f"| `{row['name']}` | {row['dtype']} | {examples} |")

    lines.extend(
        [
            "",
            "## Nilai hilang (missing)",
            "",
            "| Kolom | Jumlah | % | Rencana awal |",
            "|-------|--------|---|--------------|",
        ]
    )
    for col in profile["missing_count"]:
        plan = profile["missing_handling_plan"].get(col, "Tidak ada missing; tidak ada aksi khusus.")
        lines.append(
            f"| `{col}` | {profile['missing_count'][col]} | {profile['missing_pct'][col]}% | {plan} |"
        )

    lines.extend(["", "## Outlier (harga produk & permintaan)", ""])
    for col, stats in profile["outliers"].items():
        lines.append(f"### `{col}`")
        lines.append(f"- **Metode:** {stats['method']}")
        lines.append(
            f"- **Pagar bawah/atas:** {stats['lower_fence']:,.2f} / {stats['upper_fence']:,.2f}"
        )
        lines.append(
            f"- **Jumlah outlier:** {stats['count']} ({stats['pct']}% dari baris non-missing)"
        )
        if stats["count"]:
            lines.append(
                f"- **Rentang outlier:** {stats['min_outlier']:,.2f} – {stats['max_outlier']:,.2f}"
            )
        lines.append(
            "- **Keputusan awal:** Pertahankan untuk EDA; cap atau transformasi (log) hanya jika M2/M3 menunjukkan dominasi titik ekstrem."
        )
        lines.append("")

    t = profile["time_column"]
    lines.extend(
        [
            "## Kolom waktu & ADR-0001",
            "",
            f"- Kolom **`{t['name']}`** tersedia; rentang **{t['min']}** s/d **{t['max']}**.",
            f"- Urutan kronologis naik: **{'ya' if t['chronological'] else 'tidak'}** → cocok untuk **validasi berbasis waktu** ({t['adr_reference']}).",
            "",
            "## Harga pesaing & penanda promosi",
            "",
        ]
    )
    cp = profile["competitor_and_promo_flags"]
    lines.append(
        f"- `harga_pesaing`: **{'ada' if cp['harga_pesaing'] else 'tidak ada'}**"
    )
    lines.append(f"- `persen_diskon`: **{'ada' if cp['persen_diskon'] else 'tidak ada'}**")
    lines.append(
        f"- `musim_liburan` (0/1): **{'ada' if cp['musim_liburan'] else 'tidak ada'}**"
        + (f"; nilai unik {cp['musim_liburan_levels']}" if cp["musim_liburan"] else "")
    )

    lines.extend(
        [
            "",
            "## Fitur target vs kebutuhan pipeline",
            "",
            "| Fitur yang dibutuhkan README / M2 | Status |",
            "|-----------------------------------|--------|",
        ]
    )
    for name, ok in profile["expected_readme_features"].items():
        lines.append(f"| {name} | {'✓ tersedia' if ok else '✗ hilang'} |")

    if profile["missing_expected_features"]:
        lines.append("")
        lines.append(
            f"**Fitur hilang:** {', '.join(profile['missing_expected_features'])}"
        )
    else:
        lines.append("")
        lines.append("Semua fitur yang diasumsikan di `DATASET_GENERATOR_SPECS.md` hadir di file aktual.")

    lines.extend(
        [
            "",
            "## Keputusan utama untuk M2+",
            "",
            f"- **Kolom target regresi:** `{profile['target_column']}` (permintaan dalam unit terjual).",
            "- **Split evaluasi:** urut waktu (bukan acak), mengikuti ADR-0001.",
            "- **Missing:** imputasi median pada `harga_pesaing` dan `permintaan` di tahap preprocessing.",
            "",
            "## Draft poin laporan (bab Dataset, ≤1 halaman nanti di M7)",
            "",
            "- Dataset sintetis 2.500 hari (2022–2028) dengan harga sendiri, harga pesaing, diskon, penanda musim liburan, dan target permintaan.",
            "- Missing terkendali (~2%) pada harga pesaing dan permintaan; ditangani di prapemrosesan.",
            "- Outlier IQR moderat pada permintaan (~5%); dipertahankan untuk pemodelan elastisitas.",
            "- Validasi model memakai pemisahan latih/uji berbasis waktu.",
            "",
        ]
    )
    return "\n".join(lines)


def write_data_profile_report(
    path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    dataset_path = path or DEFAULT_DATASET_PATH
    df = load_dataset(dataset_path)
    profile = build_profile_dict(df, dataset_path)
    markdown = render_markdown(profile)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = output_path or REPORTS_DIR / "data_profile.md"
    out.write_text(markdown, encoding="utf-8")
    return out


def main() -> None:
    out = write_data_profile_report()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()