# TODO — UTS prediksi permintaan & rekomendasi harga

Pelacakan progress untuk **human** dan **agent**. Rincian task per modul ada di [`docs/todo/`](docs/todo/README.md); file ini hanya ringkasan dan aturan—jangan menambah task panjang di sini.

**Acuan:** [`README.md`](README.md) · [`GLOSSARY.md`](GLOSSARY.md) · [`docs/agents/pipeline-modules.md`](docs/agents/pipeline-modules.md) · [`docs/agents/report-format.md`](docs/agents/report-format.md)

## Cara pakai

| Peran | Langkah                                                                                                                                                                                                                                          |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Human | Pilih modul berikutnya dari tabel Progress; buka file `docs/todo/M*.md`; centang task; set `Status:` tiap blok.                                                                                                                                  |
| Agent | Baca modul bertanda `in_progress` atau permintaan user yang menyebut slug (mis. `preprocessing`); selesaikan task di file modul itu; update checkbox + `Status:`; jangan menandai `done` jika kriteria di `pipeline-modules.md` belum terpenuhi. |

**Urutan disarankan:** M0 → M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8 (Mopt hanya jika dataset sintetis).

## Progress (perbarui saat modul selesai)

| Modul | Slug / file                                    | Status modul | Depends on                                       |
| ----- | ---------------------------------------------- | ------------ | ------------------------------------------------ |
| M0    | [prerequisites](docs/todo/M0-prerequisites.md) | `done`       | —                                                |
| M1    | `data-profile`                                 | `pending`    | M0                                               |
| M2    | `preprocessing`                                | `pending`    | M1                                               |
| M3    | `eda`                                          | `pending`    | M1 (M2 untuk final)                              |
| M4    | `modeling`                                     | `pending`    | M2                                               |
| M5    | `evaluation`                                   | `pending`    | M4                                               |
| M6    | `price-simulation`                             | `pending`    | M5                                               |
| M7    | `reporting`                                    | `pending`    | M3, M5, M6                                       |
| Mopt  | `dataset-generator`                            | `pending`    | — (spesifikasi terisi; generator awal ada di `src/`) |
| M8    | [closure](docs/todo/M8-closure.md)             | `pending`    | M7                                               |

Legenda status modul: `pending` · `in_progress` · `blocked` · `done` · `skipped`

## Deliverable akhir (cek sekali di M8)

- [ ] Pipeline Python modular di `src/` dapat dijalankan end-to-end
- [ ] Rekomendasi harga terdokumentasi (angka + asumsi)
- [ ] `report/LAPORAN_UTS.md` + `.docx` **≤ 10 halaman** ([format](docs/agents/report-format.md))
- [ ] Video (opsional)

## Quick links modul

- [M0 — Prerequisites](docs/todo/M0-prerequisites.md)
- [M1 — Data profile](docs/todo/M1-data-profile.md)
- [M2 — Preprocessing](docs/todo/M2-preprocessing.md)
- [M3 — EDA](docs/todo/M3-eda.md)
- [M4 — Modeling](docs/todo/M4-modeling.md)
- [M5 — Evaluation](docs/todo/M5-evaluation.md)
- [M6 — Price simulation](docs/todo/M6-price-simulation.md)
- [M7 — Reporting](docs/todo/M7-reporting.md)
- [Mopt — Dataset generator](docs/todo/Mopt-dataset-generator.md)
- [M8 — Closure](docs/todo/M8-closure.md)
