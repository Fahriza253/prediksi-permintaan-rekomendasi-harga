# M1 — Data profile (`data-profile`)

**Status modul:** `pending`  
**Depends on:** M0  
**Scratch:** `.scratch/data-profile/`  
**Kriteria modul:** [`pipeline-modules`](../agents/pipeline-modules.md#modul-wajib-urutan-disarankan) baris `data-profile`

## Task

- [ ] Muat dataset; dokumentasikan path dan format file
- [ ] Inventaris kolom: nama, tipe, contoh nilai
- [ ] Hitung missing per kolom; rencana penanganan awal
- [ ] Deteksi outlier pada harga dan permintaan (metode disebutkan)
- [ ] Konfirmasi kolom waktu (untuk musim & ADR-0001)
- [ ] Konfirmasi kolom harga pesaing dan penanda diskon/liburan (atau catat tidak ada)
- [ ] Tulis ringkasan 1 halaman (bisa `outputs/reports/data_profile.md`)

## Keluaran untuk modul berikutnya

- [ ] Daftar fitur target vs fitur yang hilang
- [ ] Keputusan: kolom target **permintaan** teridentifikasi

## Laporan (potongan bab 4, nanti di M7)

- [ ] Draft poin untuk bab Dataset & prapemrosesan (≤1 halaman saat digabung)

**Catatan / blocker:**