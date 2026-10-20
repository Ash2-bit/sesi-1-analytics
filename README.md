# Pembersihan Data Inventaris Agribisnis (Mencegah "Garbage In, Garbage Out")

## Deskripsi

Proyek ini merupakan studi kasus sederhana penerapan *Data Analytics* untuk pembersihan data (*data cleaning*) dan agregasi pada data operasional logistik perkebunan.
Proyek ini dibuat berdasarkan materi "Make Sense of Data with Analysis and AI" yang membahas pentingnya *data preparation*, penanganan anomali data, serta bahaya dari prinsip "Garbage In, Garbage Out" (GIGO) sebelum data divisualisasikan ke dalam *dashboard* manajemen.

## Tujuan

Tujuan proyek ini adalah:
1. Memproses dan membersihkan data logistik mentah yang memiliki banyak anomali.
2. Mengetahui pengaruh nilai kosong (*missing values*) dan kesalahan input (*human error*) terhadap validitas laporan akhir.
3. Membandingkan distribusi data sebelum dan sesudah dilakukan imputasi (pengisian nilai kosong) menggunakan pendekatan statistik (*Median*).
4. Menghasilkan ringkasan data (*insight*) yang valid dan siap digunakan sebagai pendukung keputusan distribusi logistik.

## Studi Kasus

Sebuah perusahaan agribisnis memiliki data transaksi distribusi logistik (seperti pupuk) yang ditarik dari input manual berbagai supervisor gudang cabang. Karena tidak adanya validasi pada sistem input, data dipenuhi anomali seperti format tanggal yang berantakan, jumlah stok bernilai negatif, dan data yang kosong.
Pemrosesan ini diperlukan sebagai *decision support*, agar manajemen pusat tidak mengambil keputusan alokasi anggaran yang salah akibat membaca laporan metrik dari data yang korup.

## Dataset

Dataset yang digunakan merupakan dataset sintetis yang dibuat menggunakan library Python (`Faker` dan `NumPy`).
Dataset berisi data transaksi distribusi dengan beberapa atribut, antara lain:
*   `tanggal_distribusi` — tanggal pupuk keluar dari gudang (terdapat format yang tidak konsisten)
*   `kode_gudang` — lokasi gudang penyimpanan
*   `stok_keluar_kg` — jumlah pupuk yang didistribusikan (terdapat anomali angka negatif dan nilai kosong)
*   `status_pengiriman` — status logistik (Terkirim/Pending/Gagal)

Target dari pemrosesan ini adalah menciptakan dataset baru yang terstandarisasi, bebas dari data kosong (NaN), dan anomali logika.

## Metode

Tahapan utama yang dilakukan:
1. *Data Understanding* (Pemeriksaan ringkasan data dan deteksi anomali)
2. *Preprocessing Data*:
    * Standarisasi format `datetime`
    * Transformasi nilai absolut untuk mengatasi anomali input stok negatif
    * Imputasi (pengisian) nilai kosong pada kolom numerik menggunakan nilai *Median*
    * Imputasi nilai kosong pada kolom kategorikal berdasarkan logika bisnis (Logika *Pending* = Gudang Pusat)
3. *Data Aggregation* (Pengelompokan data per gudang)
4. Evaluasi kualitas data akhir

## Pendekatan Analisis

Pendekatan utama yang digunakan:
*   *Descriptive Statistics* untuk mendeteksi pencilan (*outliers*).
*   *Median Imputation*. Penggunaan *Median* (nilai tengah) dipilih alih-alih *Mean* (rata-rata) agar data tidak terdistorsi oleh angka ekstrem (*outliers*) dari kesalahan input manual.

## Evaluasi

Performa pembersihan data dievaluasi menggunakan:
*   *Missing Value Ratio* (Rasio data hilang sebelum dan sesudah)
*   *Data Retention Rate* (Persentase baris data yang berhasil diselamatkan tanpa harus dihapus)
Dalam kasus ini, *Data Retention* menjadi metrik penting karena perusahaan ingin meminimalisir hilangnya rekam jejak transaksi akibat pembersihan data.

## Teknologi

*   Python
*   Google Colab / Jupyter Notebook (`.ipynb`)
*   Pandas
*   NumPy
*   Matplotlib
*   Seaborn

## Cara Menjalankan

1. Proyek dapat dijalankan menggunakan Google Colab.
2. Buka file `data_cleaning_agribisnis.ipynb` menggunakan Google Colab.
3. Jalankan *notebook* dari awal hingga akhir.
4. Dataset sintetis akan dibuat secara otomatis di dalam *cell* pertama untuk digunakan pada proses analisis selanjutnya.
5. Hasil perbandingan data kotor dan data bersih dapat dilihat langsung pada visualisasi di dalam *notebook*.

## Kesimpulan
Proyek ini menunjukkan bahwa dalam ekosistem Data Analytics, algoritma visualisasi yang canggih tidak akan berguna jika tidak didahului oleh Data Preparation yang ketat.
Pada kondisi data operasional dunia nyata, pemahaman aturan bisnis (business domain) sama pentingnya dengan kemampuan coding; misalnya, mengetahui bahwa "stok tidak mungkin negatif" atau "status pending berarti barang masih di pusat" adalah kunci untuk menyelamatkan data tanpa mengubah maknanya.
Hasil akhir data ini siap dihubungkan ke platform Business Intelligence atau dashboard UI/UX.

Referensi
Arisal, A. (2026). Make Sense of Data with Analysis and AI. Research Center for Data and Information Sciences, Badan Riset dan Inovasi Nasional (BRIN).


## Struktur Repository

```text
sesi-1-analytics/
├── data_cleaning_agribisnis.ipynb
├── README.md
└── requirements.txt
Keterangan
data_cleaning_agribisnis.ipynb — notebook utama yang berisi seluruh proses ekstraksi, transformasi, dan pembersihan data.
