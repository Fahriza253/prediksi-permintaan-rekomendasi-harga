# M7 — Reporting (`reporting`)

**Status modul:** `done`  
**Depends on:** M3, M5, M6  
**Scratch:** `.scratch/reporting/`  
**Format:** [`report-format.md`](../agents/report-format.md)

## Task integrasi sistem

- [x] Entrypoint CLI atau skrip `run_pipeline` (dataset → rekomendasi)
- [x] README pengguna: cara install & jalankan (ringkas)

## Task laporan (≤ 10 halaman Word)

- [x] Susun `report/LAPORAN_UTS.md` bab 1–7 sesuai anggaran halaman
- [x] Bab 2 Teori (ringkas, istilah dari `GLOSSARY.md`)
- [x] Bab 3 Rancangan (satu diagram alur)
- [x] Bab 4 Dataset & prapemrosesan (dari M1–M2)
- [x] Bab 5 Model & evaluasi (dari M5)
- [x] Bab 6 Simulasi & rekomendasi (dari M6)
- [x] Bab 7 Kesimpulan & keterbatasan model
- [x] Sisipkan ≤4 gambar, ≤3 tabel; kode ≤15 baris per cuplikan
- [x] Ekspor `.docx`; hitung halaman → **wajib ≤ 10**
- [x] Catat jumlah halaman di abstrak atau akhir naskah

## Selesai modul

- [x] Semua angka/grafik konsisten dengan run terakhir pipeline

**Catatan / blocker:** Isi `[NAMA LENGKAP]` dan `[NIM]` di bab 1. Pipeline: `python -m py_prediction_system.run_pipeline`. Ekspor: `python -m py_prediction_system.reporting.export_docx` → `report/LAPORAN_UTS.docx`; estimasi halaman: `report/page_count_estimate.txt` (~3,7 halaman heuristik; verifikasi di Word).