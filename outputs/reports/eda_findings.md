# Temuan EDA (M3)

Sumber data: `data/processed/demand_preprocessed.csv`.

## Poin untuk laporan

- Harga produk dan permintaan berkorelasi negatif (r ≈ -0.37), sesuai elastisitas: harga naik cenderung menurunkan unit terjual.
- Rasio harga terhadap pesaing (`rasio_harga_pesaing`) berkorelasi -0.86 dengan permintaan — posisi relatif harga penting untuk prediksi.
- Persentase diskon berkorelasi 0.98 dengan permintaan; diskon lebih tinggi cenderung menaikkan permintaan pada data ini.
- Rata-rata permintaan saat musim liburan 757.9 unit vs non-liburan 523.9 unit (selisih ≈ +234.0 unit).
- Fitur dengan |korelasi| terbesar terhadap permintaan (di antara fitur model): `persen_diskon` (r = 0.98).
- Tidak terlihat pola non-linear ekstrem pada scatter harga–permintaan; regresi linear layak sebagai baseline, model lanjutan untuk menangkap interaksi.
- EDA memakai 2,500 baris data terproses M2 (tanpa missing pada kolom inti).

## Gambar (`outputs/figures/`)

- `eda_price_vs_demand.png` — Scatter harga produk vs permintaan (warna musim liburan) (✓ masuk laporan, slot 1; M3-eda)
- `eda_feature_correlation.png` — Heatmap korelasi fitur utama & permintaan (✓ masuk laporan, slot 2; M3-eda)
- `(reserved-m5-metrics)` — Perbandingan metrik baseline vs lanjutan (✓ masuk laporan, slot 3; M5-evaluation)
- `(reserved-m6-simulation)` — Kurva simulasi harga–pendapatan (✓ masuk laporan, slot 4; M6-price-simulation)

**Anggaran gambar laporan:** 4 total; M3 memakai slot 1–2; slot 3–4 untuk M5/M6.
