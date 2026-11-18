# Desain: Setup agent modular (UTS AI & ML)

**Status:** disetujui pengguna (ronde grilling 1, rekomendasi diterima penuh).  
**Tujuan:** Agent Cursor menghasilkan output task yang selaras dengan `README.md`, dengan dokumen terpisah agar mudah diubah tanpa duplikasi.

## Konteks

Proyek UTS: prediksi **permintaan** dari harga/konteks, lalu **rekomendasi harga** via simulasi pendapatan. Deliverable: sistem Python modular + **laporan Word maks. 10 halaman** (`docs/agents/report-format.md`) + video opsional.

Repo sudah memiliki skill engineering (`.agents/skills/`) dan konfigurasi agent (`AGENTS.md`, `docs/agents/*`). Belum ada kode ML, `GLOSSARY.md`, atau `.scratch/` aktif.

## Keputusan (grilling 1)

| # | Keputusan |
|---|-----------|
| 1 | Task selesai jika artefak ML/kode + metrik/grafik jelas; teks laporan hanya pada task yang memang berlabel laporan. |
| 2 | Issue tracker: markdown lokal di `.scratch/<feature-slug>/`. |
| 3 | Unit kerja agent: tahap pipeline `README.md` (§2.4); generator dataset = effort terpisah bila `DATASET_GENERATOR_SPECS.md` diisi. |
| 4 | Istilah wajib mengikuti `GLOSSARY.md`; kode boleh Inggris dengan mapping di spec modul. |
| 5 | `README.md` = north star domain/alur; `AGENTS.md` = routing skill + pointer proyek saja. |

## Arsitektur dokumen (modular)

```
README.md                 → tujuan, alur ML, mapping laporan (human + agent)
GLOSSARY.md               → istilah domain (tanpa detail implementasi)
docs/adr/                 → keputusan sulit dibalik
docs/agents/              → cara skill memakai repo (sudah ada)
docs/agents/pipeline-modules.md  → slug .scratch per tahap + kriteria selesai
docs/agents/report-format.md     → struktur laporan singkat + anggaran halaman (≤10)
AGENTS.md                 → pointer: skills, issue tracker, glossary, pipeline map, report format
.scratch/<slug>/          → spec + issues per upaya (dibuat saat mulai task)
```

**Prinsip perubahan:**

- Ubah alur/soal → edit `README.md`.
- Ubah istilah laporan → edit `GLOSSARY.md`.
- Ubah keputusan teknis tetap → ADR baru atau revise ADR.
- Ubah definisi “selesai” per tahap → edit `docs/agents/pipeline-modules.md` saja.
- Ubah batas/format laporan → edit `docs/agents/report-format.md` saja.
- Ubah workflow agent global → edit `docs/agents/*` atau `AGENTS.md`.

## Alur kerja agent per task

1. Baca `README.md` §2 untuk batas masalah; `GLOSSARY.md` untuk bahasa.
2. Buka `docs/agents/pipeline-modules.md` → pilih slug tahap yang dikerjakan.
3. Jika belum ada folder: buat `.scratch/<slug>/spec.md` (via `/to-spec` atau manual), pecah issue via `/to-tickets`.
4. Set `Status: ready-for-agent` pada issue yang sudah jelas; kerjakan dengan `/implement-spec` atau implement manual.
5. Penyelesaian task:
   - **Kode/ML:** modul/fungsi + tes atau skrip demo + metrik/grafik bila relevan.
   - **Laporan:** hanya jika issue menandai deliverable laporan.

## Pemetaan modul pipeline

Detail slug, dependensi, dan kriteria selesai: `docs/agents/pipeline-modules.md`.

Urutan referensi README §2.4:

1. `data-profile` — pemahaman & pemeriksaan dataset  
2. `preprocessing` — pembersihan & feature engineering  
3. `eda` — EDA harga–permintaan  
4. `modeling` — baseline + model lanjutan  
5. `evaluation` — MAE, RMSE, R²  
6. `price-simulation` — grid harga → prediksi → pendapatan  
7. `reporting` — grafik & rekomendasi harga (artefak untuk laporan)

Effort opsional: `dataset-generator` — mengikuti `DATASET_GENERATOR_SPECS.md` bila dipakai.

## Struktur kode (target, belum diimplementasi)

Satu paket Python dengan modul sejajar tahap (nama dapat disesuaikan saat implementasi):

```
src/py_prediction_system/
  data/           # load, profile
  preprocessing/
  eda/            # atau notebook + export fig
  models/
  evaluation/
  simulation/
  reporting/
```

Konvensi: setiap modul punya entrypoint jelas; konfigurasi path dataset terpusat.

## ADR awal

- `docs/adr/0001-time-based-train-test-split.md` — validasi deret waktu, bukan split acak.

## Yang sengaja tidak dilakukan di fase ini

- Implementasi kode ML  
- Isi `DATASET_GENERATOR_SPECS.md` (menunggu kebutuhan dataset sintetis)  
- Remote GitHub (opsional nanti)

## Langkah berikutnya

Setelah pengguna meninjau file spec ini: jalankan skill **writing-plans** untuk rencana implementasi repo (git init, struktur `src/`, effort `.scratch/` pertama, dll.).