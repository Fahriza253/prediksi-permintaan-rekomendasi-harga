# M6 — Price simulation (`price-simulation`)

**Status modul:** `done`  
**Depends on:** M5  
**Scratch:** `.scratch/price-simulation/`

## Task

- [x] Tentukan grid harga (rentang & langkah; asumsi harga pesaing/konteks tetap atau skenario)
- [x] Prediksi **permintaan** tiap titik dengan model terpilih
- [x] Hitung **pendapatan** = harga × permintaan
- [x] Identifikasi harga **rekomendasi** (maksimalkan pendapatan atau kriteria yang didokumentasikan)
- [x] Grafik kurva permintaan & pendapatan vs harga → `outputs/figures/`
- [x] Catat angka rekomendasi + sensitivitas singkat

## Laporan (potongan bab 6)

- [x] Draft poin rekomendasi harga dengan angka pasti

**Catatan / blocker:** `python -m py_prediction_system.simulation.price_grid`. **Rekomendasi: ~126.283 IDR** (lihat `outputs/metrics/price_recommendation.json`). Grafik slot 4: `simulation_price_revenue_curve.png`.