# Project UTS: AI & ML

_Ujian Praktik Mata Kuliah Artificial Intelligence dan Machine Learning, Program Studi Teknik Informatika_

Dokumen ini menjelaskan soal, analisis, dan pola pikir perancangan untuk menyelesaikan ujian praktik berupa prediksi permintaan produk berdasarkan perubahan harga menggunakan algoritma Machine Learning.

## Menjalankan cepat

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
python -m py_prediction_system.run_pipeline          # M2→M6: preprocess … rekomendasi harga
python -m py_prediction_system.reporting.export_docx # LAPORAN_UTS.md → .docx
```

Laporan: [`report/LAPORAN_UTS.md`](report/LAPORAN_UTS.md) · Profil data (M1): `python -m py_prediction_system.data.profile`

## 1. Soal

Berikut adalah soal yang diberikan oleh dosen:

> Misalkan ada sebuah perusahaan berencana menawarkan diskon untuk produknya selama musim liburan atau waktu tertentu. Perusahaan ingin menemukan harga di mana produk dapat terjual lebih baik dibandingkan dengan pesaingnya. Untuk tugas ini, perusahaan menyediakan kumpulan data perubahan penjualan pada waktu yang lalu berdasarkan perubahan harga. Dengan dataset tersebut, kita perlu membuat model yang dapat memprediksi permintaan produk di pasar pada segmen harga yang berbeda menggunakan algoritma ML.

## 2. Analisis

### 2.1 Pemahaman Masalah

Tugas ini adalah studi kasus analitik menggunakan Python. Inti tugasnya bukan sekadar mencari produk terlaris, melainkan **mempelajari hubungan antara harga dan permintaan, lalu memanfaatkan hubungan tersebut untuk menentukan harga yang tepat**.

Dataset disediakan oleh perusahaan, sehingga proses pencarian dataset mentah tidak menjadi fokus utama. Fokus utamanya adalah pemodelan dan rekomendasi harga.

### 2.2 Perumusan Masalah

Masalah dirumuskan dalam tiga tingkat agar arah penyelesaian jelas.

| Tingkat          | Pertanyaan                                                                        | Penjelasan                                              |
| ---------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Bisnis           | Pada harga berapa produk terjual lebih baik dibanding pesaing?                    | Tujuan akhir perusahaan                                 |
| Machine Learning | Berapa permintaan jika harga = P, harga pesaing = C, dan kondisi = musim liburan? | Masalah **regresi**: memprediksi angka jumlah penjualan |
| Keputusan        | Harga mana yang memaksimalkan pendapatan (atau keuntungan)?                       | Dihitung dari simulasi berbagai harga memakai model     |

### 2.3 Konsep Kunci

- **Elastisitas harga permintaan (price elasticity of demand)**: ukuran seberapa sensitif jumlah permintaan terhadap perubahan harga. Ini menjadi landasan teori utama laporan.
- **Pendapatan bukan sama dengan permintaan**: harga turun biasanya menaikkan jumlah terjual, tetapi pendapatan belum tentu naik. Pendapatan = harga × jumlah terjual, sehingga harga terbaik berada di titik keseimbangan.
- **Korelasi bukan sebab-akibat**: diskon besar biasanya dilakukan saat liburan, sehingga pengaruh harga dan pengaruh musim bisa tercampur. Karena itu, fitur musim atau liburan harus ikut dimasukkan ke model.
- **Validasi sadar waktu**: jika data berupa deret waktu, data lama dipakai untuk melatih model dan data terbaru untuk menguji, bukan dibagi secara acak.

### 2.4 Alur Penyelesaian

1. **Memahami dan memeriksa dataset**: struktur kolom, tipe data, data kosong, dan data pencilan (outlier).
2. **Pembersihan dan penyiapan data (preprocessing)**: penanganan data kosong, pembentukan fitur seperti selisih harga dengan pesaing, penanda musim liburan, dan persentase diskon. Tahap penyaringan (filtering) berada di sini.
3. **Analisis data eksploratif (EDA)**: grafik hubungan harga dan permintaan untuk melihat pola awal.
4. **Pembuatan model**: model dasar (baseline) berupa Linear Regression, lalu model lanjutan seperti Random Forest atau Gradient Boosting.
5. **Evaluasi model**: membandingkan model dengan metrik MAE, RMSE, dan R².
6. **Simulasi harga**: menguji banyak kemungkinan harga, memprediksi permintaan, menghitung pendapatan, lalu mengambil harga dengan pendapatan tertinggi.
7. **Penyajian hasil**: grafik kurva harga terhadap permintaan dan pendapatan, serta rekomendasi harga.

### 2.5 Keluaran (Output)

- **Sistem Python yang dapat dipakai ulang** untuk kasus serupa: menerima dataset, melatih model, dan menghasilkan rekomendasi harga.
- **Laporan formal singkat**: teori, rancangan, implementasi, pengujian, dan hasil—**maksimal 10 halaman Word** (tanpa lampiran tambahan). Format bab dan anggaran halaman: `docs/agents/report-format.md`.
- **Video penjelasan** (opsional).

## 3. Brainstorming: Pola Pikir Perancangan

Bagian ini merangkum pola pikir yang perlu dipegang sebelum memulai perancangan sistem.

### 3.1 Pergeseran Pola Pikir

| Pola pikir awal                           | Pola pikir yang diperbaiki                    | Alasan                                              |
| ----------------------------------------- | --------------------------------------------- | --------------------------------------------------- |
| Mencari produk dengan penjualan terbanyak | Mempelajari hubungan harga dan permintaan     | Soal meminta prediksi permintaan pada harga berbeda |
| Filtering sebagai inti pekerjaan          | Filtering hanya tahap persiapan data          | Inti penilaian ada pada model ML                    |
| Sistem memberi kandidat produk            | Sistem memberi prediksi dan rekomendasi harga | Tujuan perusahaan adalah menemukan harga yang tepat |
| Mencari dataset mentah sendiri            | Memakai dataset yang disediakan perusahaan    | Disebutkan jelas dalam soal                         |

### 3.2 Prinsip yang Dipegang

1. **Mulai dari pertanyaan, bukan dari algoritma.** Tentukan dahulu apa yang diprediksi dan keputusan apa yang dihasilkan.
2. **Bangun model dasar terlebih dahulu.** Model sederhana menjadi pembanding agar peningkatan dari model rumit dapat dibuktikan.
3. **Hasil harus dapat dijelaskan.** Rekomendasi harga perlu didukung grafik dan angka yang mudah dipahami pembaca laporan.
4. **Sistem harus dapat dipakai ulang.** Pisahkan modul pemuatan data, preprocessing, pelatihan, evaluasi, dan simulasi harga.
5. **Ketahui batas model.** Model hanya belajar dari data masa lalu, sehingga rekomendasi adalah perkiraan, bukan kepastian.

### 3.3 Rancangan Alur Sistem (Usulan)

**Dataset** → **Preprocessing dan pembentukan fitur** → **Pelatihan model** → **Evaluasi** → **Simulasi harga** → **Rekomendasi harga dan laporan grafik**

### 3.4 Kaitan dengan Struktur Laporan

| Bagian laporan (ringkas) | Isi yang disiapkan (muat dalam ~10 halaman Word total)              |
| ------------------------ | ------------------------------------------------------------------- |
| Teori                    | Elastisitas, regresi, algoritma, metrik—poin utama saja           |
| Rancangan sistem         | Satu diagram alur + fitur kunci + pembagian modul                 |
| Implementasi sistem      | Ringkasan modul; cuplikan kode singkat (detail di repo)             |
| Pengujian sistem         | Split waktu, skenario, baseline vs lanjutan                         |
| Hasil pengujian          | Tabel metrik, kurva simulasi, **rekomendasi harga**                 |

### 3.5 Hal yang Perlu Dipastikan Selanjutnya

Sebelum perancangan fitur dan arsitektur, perlu dipastikan isi dataset dari perusahaan atau dosen:

- Apakah tersedia kolom tanggal (untuk menentukan musim dan validasi berbasis waktu)?
- Apakah tersedia kolom harga pesaing?
- Apakah tersedia penanda diskon atau liburan?
- Berapa jumlah baris data dan apakah ada banyak data kosong?

Jawaban atas pertanyaan tersebut menentukan fitur dan model yang realistis untuk digunakan.
