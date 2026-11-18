# Format laporan UTS (singkat)

**Batas keras:** dokumen Word akhir **maksimal 10 halaman**. Tidak boleh lebih. Tidak ada lampiran terpisah yang menambah halaman di luar file utama.

Asumsi hitung halaman (Word): A4, margin standar (2,5 cm), font Times New Roman 12 pt, spasi 1,15, judul bab tidak dihitung ganda.

## Lokasi sumber

- Naskah sumber disusun di repo: `report/LAPORAN_UTS.md` (Markdown).
- Ekspor ke Word (`.docx`) wajib diverifikasi jumlah halaman ≤ 10 sebelum pengumpulan.

## Struktur wajib & anggaran halaman

Total anggaran **≤ 10 halaman** (termasuk gambar dan tabel).

| Bab | Isi (singkat) | Maks. halaman |
|-----|----------------|---------------|
| 1 | Judul, identitas, abstrak (±150 kata) | 1 |
| 2 | Teori: elastisitas, regresi, metrik; tanpa ulasan pustaka panjang | 1,5 |
| 3 | Rancangan: alur data → rekomendasi; diagram 1 halaman jika perlu | 1 |
| 4 | Dataset & prapemrosesan: ringkasan kolom, fitur utama | 1 |
| 5 | Model & evaluasi: baseline vs lanjutan, tabel metrik | 2 |
| 6 | Simulasi harga, grafik kurva, **rekomendasi harga** (angka) | 2 |
| 7 | Kesimpulan & keterbatasan model | 1,5 |

Jika bab melebihi anggaran, **potong teks**—jangan menambah halaman. Prioritas isi: bab 5–6 (bukti ML) > bab 2 (teori).

## Aturan singkat (agen & penulis)

- Paragraf pendek; gunakan poin bernomor untuk langkah metode.
- **Kode:** cuplikan penting saja (≤15 baris per cuplikan); kode lengkap hanya di repo `src/`, tidak di lampiran Word.
- **Gambar:** maksimal **4** gambar di seluruh laporan (mis. scatter harga–permintaan, perbandingan metrik, kurva simulasi, rekomendasi); legenda satu baris.
- **Tabel:** maksimal **3** tabel; hindari tabel lebar.
- Tidak ada duplikasi `README.md`; laporan merangkum hasil run, bukan mengulang analisis soal panjang.
- Video (jika ada) tidak mengganti kewajiban laporan 10 halaman.

## Selesai (definisi untuk modul `reporting`)

- `report/LAPORAN_UTS.md` lengkap sesuai bab di atas.
- Ekspor `.docx` tersedia dan **≤ 10 halaman** (catat jumlah halaman di baris terakhir issue atau di abstrak).
- Grafik/angka konsisten dengan run terakhir pipeline (`evaluation`, `price-simulation`).