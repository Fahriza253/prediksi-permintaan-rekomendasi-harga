# M2 — Preprocessing (`preprocessing`)

**Status modul:** `done`  
**Depends on:** M1  
**Scratch:** `.scratch/preprocessing/`  
**Kriteria modul:** pipeline-modules → `preprocessing`

## Task

- [x] Skrip/modul load + clean (reproducible, satu entrypoint)
- [x] Penanganan missing sesuai profil M1
- [x] Filtering baris tidak valid (jika ada)
- [x] Fitur: selisih harga vs pesaing (atau rasio)
- [x] Fitur: persentase diskon (jika kolom ada)
- [x] Fitur: penanda musim liburan (dari tanggal atau kolom)
- [x] Simpan dataset terproses (`data/processed/` atau artefak setara)
- [x] Dokumentasi singkat transformasi (README modul atau komentar)

## Validasi

- [x] Tidak ada leakage fitur masa depan ke baris masa lalu
- [x] Split waktu direncanakan (tanggal cutoff dicatat untuk M5)

**Catatan / blocker:** `python -m py_prediction_system.preprocessing.pipeline` → `data/processed/demand_preprocessed.csv` + `preprocessing_metadata.json`. Cutoff tes (`train_cutoff_exclusive`) dan median imputasi ada di metadata. Helper `split_train_test` untuk M4.