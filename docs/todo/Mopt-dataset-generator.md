# Mopt — Dataset generator (`dataset-generator`)

**Status modul:** `done`  
**Aktif jika:** `DATASET_GENERATOR_SPECS.md` terisi ✓  
**Scratch:** `.scratch/dataset-generator/`

## Task

- [x] Tulis spesifikasi kolom & distribusi di `DATASET_GENERATOR_SPECS.md`
- [x] Implementasi generator (skrip Python) — `dataset_generator/generate.py`
- [x] Output ke `data/raw/` sesuai path M0
- [x] Dokumentasi cara menjalankan (spec + README Menjalankan cepat + `python -m py_prediction_system.dataset_generator.generate`)
- [x] Validasi: kolom memenuhi kebutuhan M1 (waktu, harga, pesaing, permintaan)

**Catatan / blocker:** `python -m py_prediction_system.dataset_generator.generate` menghasilkan 2.500 baris dengan 6 kolom wajib.