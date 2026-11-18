# Spesifikasi dataset sintetis

**Sumber data proyek:** generator (tidak ada file dari dosen/perusahaan).  
**Path output:** `data/raw/synthetic_demand.csv`  
**Generator:** `src/py_prediction_system/dataset_generator/generate.py`

## Jawaban README §3.5

| Pertanyaan | Keputusan |
|------------|-----------|
| Kolom tanggal (musim & validasi waktu)? | **Ya** — `tanggal` (`YYYY-MM-DD`), urutan kronologis |
| Kolom harga pesaing? | **Ya** — `harga_pesaing` (IDR/unit, float) |
| Penanda diskon atau liburan? | **Ya** — `persen_diskon` (0–50) dan `musim_liburan` (0/1) |
| Jumlah baris & missing? | **2.500 baris**; missing terkontrol ~**2%** pada `harga_pesaing` dan `permintaan` (diimputasi di M2) |

## Skema kolom

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `tanggal` | date | Satu observasi per hari, rentang 2022-01-01 s/d 2028-10-17 (~2.500 hari) |
| `harga_produk` | float | Harga jual perusahaan (IDR) |
| `harga_pesaing` | float | Harga kompetitor utama |
| `persen_diskon` | float | Diskon dari harga dasar (%) |
| `musim_liburan` | int | 1 jika dalam jendela liburan (Des, Jun–Jul, Idul Fitri sintetis), else 0 |
| `permintaan` | float | Target regresi: jumlah unit terjual |

## Mekanisme generasi (ringkas)

- Harga dasar dengan random walk harian; diskon lebih tinggi saat `musim_liburan`.
- Permintaan = fungsi elastisitas terhadap `harga_produk`, selisih dengan pesaing, diskon, dan musim + noise Gauss.
- Missing: MCAR pada subset baris untuk kolom yang disebut di atas.

## Menjalankan

```bash
source .venv/bin/activate
python -m py_prediction_system.dataset_generator.generate
```

Setelah generate, file siap untuk M1 (`data-profile`).