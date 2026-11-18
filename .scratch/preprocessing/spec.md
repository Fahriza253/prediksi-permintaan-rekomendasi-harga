# Spec — M2 preprocessing

**Status:** resolved

## Entrypoint

`python -m py_prediction_system.preprocessing.pipeline`

## Transformasi

1. Sort & filter: tanggal valid, `harga_produk` > 0.
2. Cutoff latih 80% kronologis (`TRAIN_FRACTION` di `config.py`).
3. Median impute `harga_pesaing`, `permintaan` — **fit pada latih saja**.
4. Fitur: `selisih_harga_pesaing`, `rasio_harga_pesaing`; `persen_diskon`, `musim_liburan` tetap.
5. Output: `data/processed/demand_preprocessed.csv`, `preprocessing_metadata.json`.

## Cutoff untuk M5

Lihat `train_cutoff_exclusive` di metadata (dihasilkan ulang saat pipeline dijalankan).