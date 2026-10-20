# Sesi 1: Data Analytics di Dunia Bisnis
**Mitigasi "Garbage In, Garbage Out" pada Data Inventaris Agribisnis**

## 📖 Deskripsi Studi Kasus
Dalam penerapan analitika data di dunia bisnis yang sesungguhnya, data operasional yang ditarik dari berbagai cabang atau gudang sering kali sangat berantakan. Algoritma visualisasi dan dasbor semahal apa pun tidak akan berguna jika data dasarnya cacat—sebuah prinsip yang dikenal sebagai *Garbage In, Garbage Out* (GIGO). 

Studi kasus ini mensimulasikan peran seorang Data Analyst yang harus menangani data mentah distribusi logistik (seperti pupuk untuk perkebunan kelapa sawit) yang ditarik dari input manual berbagai *supervisor* gudang. Data ini penuh dengan anomali: format tanggal yang tidak konsisten, *human error* (seperti input angka negatif pada stok), dan nilai yang hilang (*missing values*).

## 🎯 Tujuan Eksekusi
1. **Standarisasi Tipe Data:** Mengonversi format tanggal yang tumpang tindih menjadi format `datetime` standar.
2. **Penanganan Anomali (Outliers/Errors):** Memperbaiki nilai input yang tidak masuk akal (misalnya stok bernilai negatif) menggunakan logika bisnis.
3. **Imputasi Nilai Kosong:** Mengisi data yang hilang menggunakan pendekatan statistik (median) dan asumsi berdasarkan *domain knowledge* (pengetahuan konteks bisnis).
4. **Agregasi Laporan:** Menyajikan ringkasan eksekutif yang bersih dan siap dihubungkan ke *dashboard* visualisasi (seperti Tableau, PowerBI, atau Vue.js frontend).

## 💻 Implementasi Kode (Python - Pandas)
Berikut adalah skrip pemrosesan datanya yang dapat Anda jalankan melalui file `data_cleaning.py`.

```python
import pandas as pd
import numpy as np

# 1. Memuat Data Mentah (Simulasi data kotor dari berbagai cabang perkebunan)
data_mentah = {
    'tanggal_distribusi': ['2026-10-01', '02/10/2026', '2026-10-03', 'TBD', '2026-10-05'],
    'kode_gudang': ['GDG-01', 'GDG-02', None, 'GDG-01', 'GDG-03'],
    'stok_pupuk_keluar_kg': [5000, -150, 4500, None, 6000], # Terdapat anomali negatif dan nilai kosong
    'status': ['Terkirim', 'Terkirim', 'Pending', 'Terkirim', 'Terkirim']
}
df = pd.DataFrame(data_mentah)

print("--- Data Mentah Awal ---")
print(df)

# 2. Proses Pembersihan Data (Data Cleaning)
# a. Standarisasi Format Tanggal (Data 'TBD' atau format salah akan diubah menjadi NaT)
df['tanggal_distribusi'] = pd.to_datetime(df['tanggal_distribusi'], errors='coerce')

# b. Menangani Anomali Data (Stok keluar tidak mungkin negatif, kita ubah menjadi nilai absolut)
df['stok_pupuk_keluar_kg'] = df['stok_pupuk_keluar_kg'].apply(lambda x: abs(x) if x < 0 else x)

# c. Imputasi Nilai Kosong (Missing Values)
# Mengisi stok kosong dengan nilai median agar tidak merusak distribusi data historis
median_stok = df['stok_pupuk_keluar_kg'].median()
df['stok_pupuk_keluar_kg'] = df['stok_pupuk_keluar_kg'].fillna(median_stok)

# Mengisi kode gudang yang kosong dengan asumsi bisnis: jika 'Pending', barang masih di 'GDG-PUSAT'
df['kode_gudang'] = df['kode_gudang'].fillna('GDG-PUSAT')

# d. Menghapus baris yang tanggalnya benar-benar tidak bisa diselamatkan (Data Korup)
df = df.dropna(subset=['tanggal_distribusi'])

# 3. Agregasi Data untuk Dashboard Analitik
print("\n--- Data Bersih Siap Analisis ---")
print(df)

# Menghitung total pupuk yang didistribusikan per gudang
laporan_gudang = df.groupby('kode_gudang')['stok_pupuk_keluar_kg'].sum().reset_index()
laporan_gudang.rename(columns={'stok_pupuk_keluar_kg': 'total_distribusi_kg'}, inplace=True)

print("\n--- Ringkasan Eksekutif untuk Dashboard ---")
print(laporan_gudang)
