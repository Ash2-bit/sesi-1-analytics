import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

print("=== TAHAP 1: DATA GENERATION & UNDERSTANDING ===")
# 1. GENERATE DATASET SINTETIS (1.000 Baris)
np.random.seed(42)
n_rows = 1000

# a. Generate tanggal acak (dengan 5% anomali menjadi teks 'TBD')
start_date = datetime(2026, 1, 1)
dates = [start_date + timedelta(days=np.random.randint(0, 300)) for _ in range(n_rows)]
dates = [d.strftime('%Y-%m-%d') if np.random.rand() > 0.05 else 'TBD' for d in dates]

# b. Generate gudang (dengan 10% data kosong / NaN)
gudang_list = ['GDG-01', 'GDG-02', 'GDG-03']
gudang = [np.random.choice(gudang_list) if np.random.rand() > 0.1 else np.nan for _ in range(n_rows)]

# c. Generate stok (dengan 10% data kosong dan 5% anomali angka negatif)
stok = np.random.normal(5000, 1500, n_rows)
stok = [s if np.random.rand() > 0.1 else np.nan for s in stok]
stok = [s * -1 if pd.notna(s) and np.random.rand() > 0.95 else s for s in stok]

# d. Generate status pengiriman
status = np.random.choice(['Terkirim', 'Pending', 'Gagal'], n_rows, p=[0.8, 0.15, 0.05])

# Membuat DataFrame Mentah
df_mentah = pd.DataFrame({
    'tanggal_distribusi': dates,
    'kode_gudang': gudang,
    'stok_pupuk_keluar_kg': stok,
    'status': status
})

print(f"Total Baris Data Mentah: {len(df_mentah)}")
print("\nJumlah Missing Values (Data Kosong) Awal:")
print(df_mentah.isnull().sum())

# Simpan salinan untuk visualisasi nanti
df_clean = df_mentah.copy()


print("\n=== TAHAP 2: DATA PREPROCESSING (CLEANING) ===")
# a. Standarisasi Format Tanggal (Data 'TBD' akan diubah menjadi NaT)
df_clean['tanggal_distribusi'] = pd.to_datetime(df_clean['tanggal_distribusi'], errors='coerce')

# b. Menangani Anomali Data (Mengubah stok negatif menjadi absolut/positif)
df_clean['stok_pupuk_keluar_kg'] = df_clean['stok_pupuk_keluar_kg'].apply(lambda x: abs(x) if pd.notna(x) and x < 0 else x)

# c. Imputasi Nilai Kosong (Missing Values)
# Mengisi stok kosong dengan nilai Median
median_stok = df_clean['stok_pupuk_keluar_kg'].median()
df_clean['stok_pupuk_keluar_kg'] = df_clean['stok_pupuk_keluar_kg'].fillna(median_stok)

# Logika Bisnis: Jika status 'Pending' dan gudang kosong, asumsikan barang masih di 'GDG-PUSAT'
kondisi_pending = (df_clean['status'] == 'Pending') & (df_clean['kode_gudang'].isnull())
df_clean.loc[kondisi_pending, 'kode_gudang'] = 'GDG-PUSAT'
# Sisa gudang yang kosong dan bukan pending diisi 'TIDAK-DIKETAHUI'
df_clean['kode_gudang'] = df_clean['kode_gudang'].fillna('TIDAK-DIKETAHUI')

# d. Menghapus baris yang tanggalnya benar-benar tidak bisa diselamatkan
df_clean = df_clean.dropna(subset=['tanggal_distribusi'])

print("\nJumlah Missing Values (Data Kosong) Setelah Cleaning:")
print(df_clean.isnull().sum())
print(f"Total Baris Data Terselamatkan: {len(df_clean)} baris (Data Retention: {(len(df_clean)/n_rows)*100:.1f}%)")


print("\n=== TAHAP 3: DATA VISUALIZATION (EVALUASI) ===")
# Membuat grafik perbandingan sebelum dan sesudah dibersihkan
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot Kiri: Data Kotor
sns.histplot(df_mentah['stok_pupuk_keluar_kg'].dropna(), kde=True, color='red', ax=axes[0])
axes[0].set_title('Sebelum Cleaning: Distribusi Stok\n(Terdapat Anomali Negatif)', fontweight='bold')
axes[0].set_xlabel('Stok Pupuk Keluar (Kg)')
axes[0].set_ylabel('Frekuensi')

# Plot Kanan: Data Bersih
sns.histplot(df_clean['stok_pupuk_keluar_kg'], kde=True, color='green', ax=axes[1])
axes[1].set_title('Sesudah Cleaning: Distribusi Stok\n(Negatif di-absolutkan, Kosong diisi Median)', fontweight='bold')
axes[1].set_xlabel('Stok Pupuk Keluar (Kg)')
axes[1].set_ylabel('Frekuensi')

plt.tight_layout()
plt.show()
