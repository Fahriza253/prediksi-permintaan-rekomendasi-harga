# M5 — Evaluation (`evaluation`)

**Status modul:** `done`  
**Depends on:** M4  
**Scratch:** `.scratch/evaluation/`

## Task

- [x] Prediksi pada set uji (bukan latih)
- [x] Hitung **MAE**, **RMSE**, **R²** untuk baseline dan model lanjutan
- [x] Tabel perbandingan (kandidat 1 dari maks. 3 tabel laporan)
- [x] Simpan metrik ke `outputs/metrics.json` atau CSV
- [x] Pilih model utama untuk simulasi M6 (dengan alasan singkat)

## Laporan (potongan bab 5)

- [x] Draft teks + tabel metrik untuk bab Model & evaluasi

**Catatan / blocker:** `python -m py_prediction_system.evaluation.metrics`. Model simulasi: **baseline_linear_regression** (RMSE uji lebih rendah). Metrik: `outputs/metrics/metrics_test.json`, grafik slot 3: `evaluation_metrics_comparison.png`.