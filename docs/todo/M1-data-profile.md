# M1 — Data profile (`data-profile`)

**Status modul:** `done`  
**Depends on:** M0  
**Scratch:** `.scratch/data-profile/`  
**Kriteria modul:** [`pipeline-modules`](../agents/pipeline-modules.md#modul-wajib-urutan-disarankan) baris `data-profile`

## Task

- [x] Muat dataset; dokumentasikan path dan format file
- [x] Inventaris kolom: nama, tipe, contoh nilai
- [x] Hitung missing per kolom; rencana penanganan awal
- [x] Deteksi outlier pada harga dan permintaan (metode disebutkan)
- [x] Konfirmasi kolom waktu (untuk musim & ADR-0001)
- [x] Konfirmasi kolom harga pesaing dan penanda diskon/liburan (atau catat tidak ada)
- [x] Tulis ringkasan 1 halaman (bisa `outputs/reports/data_profile.md`)

## Keluaran untuk modul berikutnya

- [x] Daftar fitur target vs fitur yang hilang
- [x] Keputusan: kolom target **permintaan** teridentifikasi

## Laporan (potongan bab 4, nanti di M7)

- [x] Draft poin untuk bab Dataset & prapemrosesan (≤1 halaman saat digabung)

**Catatan / blocker:** Laporan: [`outputs/reports/data_profile.md`](../../outputs/reports/data_profile.md). Regenerate: `python -m py_prediction_system.data.profile`. Semua fitur README §3.5 hadir; tidak ada blocker untuk M2.