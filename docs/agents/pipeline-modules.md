# Pipeline modules (agent)

Peta antara tahap di `README.md` §2.4, slug issue tracker (`.scratch/<slug>/`), dan kriteria selesai task agent.

Edit file ini untuk mengubah definisi “selesai” per tahap tanpa menyentuh `README.md` atau `AGENTS.md`.

## Modul wajib (urutan disarankan)

| Urutan | Slug `.scratch/` | Tahap README | Kriteria selesai (agent) |
|--------|------------------|--------------|---------------------------|
| 1 | `data-profile` | Memahami & memeriksa dataset | Laporan struktur kolom, tipe, missing, outlier; daftar asumsi dataset (tanggal, harga pesaing, diskon). |
| 2 | `preprocessing` | Pembersihan & penyiapan | Pipeline reproducible: imputasi/filtering, fitur turunan (selisih harga pesaing, diskon, musim). |
| 3 | `eda` | EDA | Grafik hubungan harga–permintaan (+ konteks musim jika ada); temuan tertulis untuk laporan. |
| 4 | `modeling` | Pembuatan model | Baseline Linear Regression + ≥1 model lanjutan; artefak model tersimpan/serialisasi. |
| 5 | `evaluation` | Evaluasi | Metrik MAE, RMSE, R² pada split sesuai ADR-0001; perbandingan baseline vs lanjutan. |
| 6 | `price-simulation` | Simulasi harga | Grid harga → prediksi permintaan → pendapatan; titik rekomendasi teridentifikasi. |
| 7 | `reporting` | Penyajian hasil | `report/LAPORAN_UTS.md` + ekspor `.docx` **≤ 10 halaman Word**; isi sesuai `docs/agents/report-format.md`. |

## Modul opsional

| Slug | Pemicu | Kriteria selesai |
|------|--------|------------------|
| `dataset-generator` | `DATASET_GENERATOR_SPECS.md` terisi | Generator menghasilkan dataset yang memenuhi spec; dokumentasi cara menjalankan. |

## Dependensi antar slug

- `preprocessing` bergantung pada `data-profile`.
- `eda` dapat paralel sebagian setelah `data-profile`; hasil final setelah `preprocessing` lebih andal.
- `modeling` → `evaluation` → `price-simulation` → `reporting` berurutan.

## Label task vs laporan

- Issue bertag **ML/kode** (default): selesai dengan kode + artefak; teks laporan ringkas opsional di issue `Answer`.
- Issue bertag **laporan**: selesai dengan potongan teks yang muat anggaran halaman di `docs/agents/report-format.md` (total dokumen akhir tetap ≤ 10 halaman Word).

## Skill yang cocok per fase

| Fase | Skill disarankan |
|------|------------------|
| Spesifikasi | `/to-spec`, `/grill-with-docs` bila masih ambigu |
| Pecah task | `/to-tickets` |
| Implementasi | `/implement-spec`, `/tdd` untuk modul kritikal |
| Arsitektur kode | `/codebase-design` sebelum `src/` besar |