# M2 — Preprocessing (`preprocessing`)

**Status modul:** `pending`  
**Depends on:** M1  
**Scratch:** `.scratch/preprocessing/`  
**Kriteria modul:** pipeline-modules → `preprocessing`

## Task

- [ ] Skrip/modul load + clean (reproducible, satu entrypoint)
- [ ] Penanganan missing sesuai profil M1
- [ ] Filtering baris tidak valid (jika ada)
- [ ] Fitur: selisih harga vs pesaing (atau rasio)
- [ ] Fitur: persentase diskon (jika kolom ada)
- [ ] Fitur: penanda musim liburan (dari tanggal atau kolom)
- [ ] Simpan dataset terproses (`data/processed/` atau artefak setara)
- [ ] Dokumentasi singkat transformasi (README modul atau komentar)

## Validasi

- [ ] Tidak ada leakage fitur masa depan ke baris masa lalu
- [ ] Split waktu direncanakan (tanggal cutoff dicatat untuk M5)

**Catatan / blocker:**