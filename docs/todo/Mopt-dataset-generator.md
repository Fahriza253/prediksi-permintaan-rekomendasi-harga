# Mopt — Dataset generator (`dataset-generator`)

**Status modul:** `pending`  
**Aktif jika:** `DATASET_GENERATOR_SPECS.md` terisi ✓  
**Scratch:** `.scratch/dataset-generator/`

## Task

- [x] Tulis spesifikasi kolom & distribusi di `DATASET_GENERATOR_SPECS.md`
- [x] Implementasi generator (skrip Python) — `dataset_generator/generate.py`
- [x] Output ke `data/raw/` sesuai path M0
- [ ] Dokumentasi cara menjalankan (sebagian di spec + perlu README singkat di modul jika diperlukan)
- [ ] Validasi: kolom memenuhi kebutuhan M1 (waktu, harga, pesaing, permintaan)

Setelah selesai: set Mopt `done` di [`TODO.md`](../../TODO.md) dan lanjut M1.

**Catatan / blocker:** Generator M0 sudah menghasilkan CSV; task validasi & dokumentasi tersisa untuk Mopt `done`.