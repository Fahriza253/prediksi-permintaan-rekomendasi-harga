# M8 — Closure (pengumpulan)

**Status modul:** `done`  
**Depends on:** M7

## Checklist akhir

- [x] Jalankan pipeline end-to-end dari mesin bersih (atau env baru) — `python -m py_prediction_system.run_pipeline` + ekspor laporan OK (2026-11-18)
- [x] Deliverable di [`TODO.md`](../../TODO.md) § Deliverable akhir — semua tercentang
- [x] Laporan Word diverifikasi ≤ 10 halaman — estimasi `report/page_count_estimate.txt` ≈ 3,7; verifikasi manual Word diserahkan ke mahasiswa
- [ ] (Opsional) Rekam video penjelasan
- [ ] (Opsional) Arsip zip: kode + laporan + dataset jika diizinkan

## Retro singkat

Tiga keterbatasan model (lisan / video):

1. **Data sintetis** — pola elastisitas & diskon dibentuk generator; generalisasi ke data perusahaan nyata belum diuji.
2. **Skenario simulasi tetap** — harga pesaing, diskon, dan musim dipegang pada median latih; rekomendasi 126.283 IDR sensitif terhadap asumsi itu.
3. **Waktu & kausalitas** — validasi berbasis waktu sudah diterapkan, tetapi korelasi kuat diskon–permintaan pada data sintetis bukan bukti sebab-akibat di lapangan.

**Verifikasi cepat sebelum kumpul:**

```bash
source .venv/bin/activate && pip install -e .
python -m py_prediction_system.run_pipeline
python -m py_prediction_system.reporting.export_docx
```

Isi identitas di `report/LAPORAN_UTS.md` bab 1, lalu ekspor ulang `.docx`.

**Catatan / blocker:** Tidak ada blocker teknis. Video dan zip opsional.