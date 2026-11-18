# Spec — M1 data-profile

**Status:** resolved  
**Modul:** `data-profile` (M1)

## Tujuan

Memeriksa `data/raw/synthetic_demand.csv` dan menulis artefak `outputs/reports/data_profile.md` plus skrip reproducible `py_prediction_system.data.profile`.

## Keputusan

- **Target regresi:** kolom `permintaan`.
- **Waktu:** kolom `tanggal`, monoton naik → ADR-0001 berlaku.
- **Pesaing & promo:** `harga_pesaing`, `persen_diskon`, `musim_liburan` semua hadir.
- **Missing (~2%):** `harga_pesaing` (46), `permintaan` (60) → imputasi median di M2.
- **Outlier:** deteksi IQR pada `harga_produk` dan `permintaan`; tidak di-drop di M1.

## Perintah

```bash
python -m py_prediction_system.data.profile
```