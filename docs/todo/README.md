# Modul TODO (progress)

Satu file per **modul** agar human/agent hanya mengedit bagian yang relevan.

## Cara memperbarui

1. Ubah checkbox dan baris `Status:` di file modul yang bersangkutan.
2. Setelah modul selesai, centang baris modul di [`TODO.md`](../../TODO.md) (tabel Progress).
3. Detail kriteria selesai: [`docs/agents/pipeline-modules.md`](../agents/pipeline-modules.md).
4. Issue rinci (opsional): buat `.scratch/<slug>/` sesuai [`docs/agents/issue-tracker.md`](../agents/issue-tracker.md).

## Status task

| Nilai | Arti |
|-------|------|
| `pending` | Belum dimulai |
| `in_progress` | Sedang dikerjakan |
| `blocked` | Menunggu dependency atau input luar |
| `done` | Kriteria modul terpenuhi |

## File modul

| File | Modul |
|------|--------|
| [M0-prerequisites.md](./M0-prerequisites.md) | Repo, dataset, lingkungan |
| [M1-data-profile.md](./M1-data-profile.md) | `data-profile` |
| [M2-preprocessing.md](./M2-preprocessing.md) | `preprocessing` |
| [M3-eda.md](./M3-eda.md) | `eda` |
| [M4-modeling.md](./M4-modeling.md) | `modeling` |
| [M5-evaluation.md](./M5-evaluation.md) | `evaluation` |
| [M6-price-simulation.md](./M6-price-simulation.md) | `price-simulation` |
| [M7-reporting.md](./M7-reporting.md) | `reporting` + laporan ≤10 halaman |
| [Mopt-dataset-generator.md](./Mopt-dataset-generator.md) | Opsional: generator dataset |
| [M8-closure.md](./M8-closure.md) | Pengumpulan & opsional video |