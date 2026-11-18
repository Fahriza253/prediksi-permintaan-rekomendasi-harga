# M3 — EDA (`eda`)

**Status modul:** `done`  
**Depends on:** M1 (data mentah); hasil final setelah M2  
**Scratch:** `.scratch/eda/`  
**Kriteria modul:** pipeline-modules → `eda`

## Task

- [x] Scatter/grafik harga vs permintaan
- [x] Eksplorasi efek musim/liburan (jika fitur ada)
- [x] Korelasi fitur utama (ringkas, tidak berlebihan)
- [x] Simpan hingga **2** figuran kandidat laporan di `outputs/figures/`
- [x] Tulis temuan bullet (3–7 poin) untuk laporan

## Batas laporan

- [x] Pilih maks. **4** gambar total proyek; tandai mana yang masuk laporan di M7

**Catatan / blocker:** `python -m py_prediction_system.eda.explore`. Gambar: `eda_price_vs_demand.png`, `eda_feature_correlation.png`. Temuan: `outputs/reports/eda_findings.md`. Manifest 4 slot: `outputs/figures/report_figure_manifest.json`.