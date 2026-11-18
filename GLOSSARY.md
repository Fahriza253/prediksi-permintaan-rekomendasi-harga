# Prediksi permintaan & rekomendasi harga

Konteks domain untuk UTS AI & ML: hubungan harga–permintaan, pemodelan regresi, dan keputusan harga berdasarkan simulasi pendapatan.

## Language

**Permintaan**:
Jumlah unit yang terjual pada suatu kondisi harga dan konteks; target prediksi model regresi.
_Avoid_: Penjualan (ambigu dengan pendapatan), sales (tanpa mapping di spec)

**Pendapatan**:
Hasil perkalian harga dengan permintaan pada skenario yang sama; dipakai untuk membandingkan harga, bukan sebagai target regresi langsung.
_Avoid_: Omzet (jika tidak didefinisikan sama), revenue (di teks laporan tanpa padanan)

**Rekomendasi harga**:
Harga (atau segmen harga) yang dipilih setelah simulasi karena memaksimalkan tujuan bisnis yang dipilih (mis. pendapatan).
_Avoid_: Harga optimal (tanpa menyebut kriteria optimasi), best price

**Simulasi harga**:
Uji banyak kandidat harga dengan model terlatih: prediksi permintaan lalu hitung pendapatan tiap titik.
_Avoid_: Forecast tunggal (satu harga saja)

**Harga pesaing**:
Harga produk kompetitor yang dipakai sebagai fitur atau perbandingan relatif.
_Avoid_: Competitor price (di laporan Indonesia)

**Model dasar (baseline)**:
Model regresi linear sederhana sebagai pembanding sebelum model yang lebih kompleks.
_Avoid_: Dummy model, trivial model

**Elastisitas harga permintaan**:
Konsep teoritis: sensitivitas permintaan terhadap perubahan harga; landasan teori laporan, bukan nama kolom wajib.
_Avoid_: Korelasi harga–permintaan sebagai pengganti elastisitas

**Musim liburan**:
Konteks waktu (fitur atau penanda) yang memisahkan pengaruh diskon/harga dari efek musiman.
_Avoid_: Holiday flag (di teks laporan tanpa definisi)

**Validasi berbasis waktu**:
Pembagian data latih/uji menurut urutan waktu: masa lalu untuk latih, masa lebih baru untuk uji.
_Avoid_: Random split, K-fold acak (untuk deret waktu proyek ini)

**Laporan UTS**:
Dokumen Word resmi penilaian, berisi teori–hasil secara ringkas, dengan batas **maksimal 10 halaman** tanpa lampiran ekstra.
_Avoid_: Laporan panjang, lampiran kode terpisah yang menambah halaman