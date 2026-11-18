# Laporan profil data (M1)

**Sumber:** `/home/thinkpad/Documents/S1 - TEKNIK INFORMATIKA/AI & ML/py-prediction-system/data/raw/synthetic_demand.csv`  
**Format:** CSV (UTF-8), pemisah koma, satu baris header  
**Ukuran:** 2,500 baris × 6 kolom

## Inventaris kolom

| Kolom           | Tipe pandas    | Contoh nilai                                                                                         |
| --------------- | -------------- | ---------------------------------------------------------------------------------------------------- |
| `tanggal`       | datetime64[us] | Timestamp('2022-01-01 00:00:00'), Timestamp('2022-01-02 00:00:00'), Timestamp('2022-01-03 00:00:00') |
| `harga_produk`  | float64        | 126067.1, 137183.71, 141155.03                                                                       |
| `harga_pesaing` | float64        | 148848.53, 147587.4, 149424.05                                                                       |
| `persen_diskon` | float64        | 13.71, 4.4, 1.8                                                                                      |
| `musim_liburan` | int64          | 0, 0, 0                                                                                              |
| `permintaan`    | float64        | 609.82, 459.83, 444.64                                                                               |

## Nilai hilang (missing)

| Kolom           | Jumlah | %     | Rencana awal                                                                                       |
| --------------- | ------ | ----- | -------------------------------------------------------------------------------------------------- |
| `tanggal`       | 0      | 0.0%  | Tidak ada missing; tidak ada aksi khusus.                                                          |
| `harga_produk`  | 0      | 0.0%  | Tidak ada missing; tidak ada aksi khusus.                                                          |
| `harga_pesaing` | 46     | 1.84% | Imputasi median (M2); kolom fitur utama untuk selisih harga.                                       |
| `persen_diskon` | 0      | 0.0%  | Tidak ada missing; tidak ada aksi khusus.                                                          |
| `musim_liburan` | 0      | 0.0%  | Tidak ada missing; tidak ada aksi khusus.                                                          |
| `permintaan`    | 60     | 2.4%  | Imputasi median (M2); baris tanpa target tidak dipakai untuk latih jika masih NA setelah imputasi. |

## Outlier (harga produk & permintaan)

### `harga_produk`

- **Metode:** IQR (Tukey 1.5×IQR)
- **Pagar bawah/atas:** 28,359.46 / 142,019.56
- **Jumlah outlier:** 40 (1.6% dari baris non-missing)
- **Rentang outlier:** 142,242.81 – 157,495.28
- **Keputusan awal:** Pertahankan untuk EDA; cap atau transformasi (log) hanya jika M2/M3 menunjukkan dominasi titik ekstrem.

### `permintaan`

- **Metode:** IQR (Tukey 1.5×IQR)
- **Pagar bawah/atas:** 267.09 / 862.34
- **Jumlah outlier:** 131 (5.37% dari baris non-missing)
- **Rentang outlier:** 863.00 – 964.27
- **Keputusan awal:** Pertahankan untuk EDA; cap atau transformasi (log) hanya jika M2/M3 menunjukkan dominasi titik ekstrem.

## Kolom waktu & ADR-0001

- Kolom **`tanggal`** tersedia; rentang **2022-01-01** s/d **2028-11-04**.
- Urutan kronologis naik: **ya** → cocok untuk **validasi berbasis waktu** (docs/adr/0001-time-based-train-test-split.md).

## Harga pesaing & penanda promosi

- `harga_pesaing`: **ada**
- `persen_diskon`: **ada**
- `musim_liburan` (0/1): **ada**; nilai unik [0, 1]

## Fitur target vs kebutuhan pipeline

| Fitur yang dibutuhkan README / M2 | Status     |
| --------------------------------- | ---------- |
| tanggal (validasi waktu & musim)  | ✓ tersedia |
| harga_pesaing                     | ✓ tersedia |
| persen_diskon                     | ✓ tersedia |
| musim_liburan                     | ✓ tersedia |
| permintaan                        | ✓ tersedia |

Semua fitur yang diasumsikan di `DATASET_GENERATOR_SPECS.md` hadir di file aktual.

## Keputusan utama untuk M2+

- **Kolom target regresi:** `permintaan` (permintaan dalam unit terjual).
- **Split evaluasi:** urut waktu (bukan acak), mengikuti ADR-0001.
- **Missing:** imputasi median pada `harga_pesaing` dan `permintaan` di tahap preprocessing.

## Draft poin laporan (bab Dataset, ≤1 halaman nanti di M7)

- Dataset sintetis 2.500 hari (2022–2028) dengan harga sendiri, harga pesaing, diskon, penanda musim liburan, dan target permintaan.
- Missing terkendali (~2%) pada harga pesaing dan permintaan; ditangani di prapemrosesan.
- Outlier IQR moderat pada permintaan (~5%); dipertahankan untuk pemodelan elastisitas.
- Validasi model memakai pemisahan latih/uji berbasis waktu.
