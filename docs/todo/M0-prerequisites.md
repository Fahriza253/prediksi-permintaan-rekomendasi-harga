# M0 — Prerequisites

**Status modul:** `done`  
**Scratch (opsional):** `.scratch/repo-setup/`  
**Selesai jika:** dataset siap dipakai, lingkungan Python terpasang, struktur repo minimal ada.

## Dataset & spesifikasi

- [x] Tentukan sumber data: dari dosen/perusahaan **atau** generator (Mopt) — **generator sintetis**
- [x] Jawab pertanyaan README §3.5 (tanggal, harga pesaing, diskon, jumlah baris, missing) — lihat `DATASET_GENERATOR_SPECS.md`
- [x] Letakkan file data di path tetap (catat di bawah **Catatan**)
- [x] Jika sintetis: isi `DATASET_GENERATOR_SPECS.md` dan aktifkan Mopt

**Catatan path dataset:** `data/raw/synthetic_demand.csv` (2.500 baris; regenerate: `python -m py_prediction_system.dataset_generator.generate`)

## Lingkungan & dependensi

- [x] Python 3.10+ tersedia — **3.13.5**
- [x] Buat virtual env (`.venv` atau setara)
- [x] Tambah `requirements.txt` / `pyproject.toml` (pandas, scikit-learn, matplotlib; sesuaikan nanti)
- [x] Verifikasi `pip install` sukses — `pip install -e .` dari repo root

## Struktur repo (minimal)

- [x] Buat kerangka `src/py_prediction_system/` (subfolder mengikuti pipeline-modules)
- [x] Buat `data/raw/` (atau path yang dicatat) untuk input
- [x] Buat `outputs/` atau `artifacts/` untuk model, fig, metrik
- [x] Buat folder `report/` untuk naskah laporan
- [ ] (Opsional) `git init` + commit dokumen — repo sudah `git init`; commit diserahkan ke human

## Agent setup (sudah sebagian)

- [x] `AGENTS.md`, `GLOSSARY.md`, `docs/agents/*`
- [x] ADR-0001 validasi berbasis waktu
- [ ] Buat `.scratch/<slug>/spec.md` saat mulai M1 (tidak wajib di M0)

## Catatan / blocker

Generator dasar sudah di `src/py_prediction_system/dataset_generator/generate.py` agar dataset dapat dipakai M1; detail validasi & dokumentasi lanjutan mengikuti checklist **Mopt**.