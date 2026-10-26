# Analisis Data Olist E-Commerce

Proyek ini bertujuan untuk menganalisis data transaksi e-commerce menggunakan **E-Commerce Public Dataset** dari Olist. Analisis dilakukan untuk memahami performa penjualan, kualitas pengiriman, karakteristik pelanggan, serta distribusi revenue berdasarkan wilayah di Brasil. Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1FiqH1jn6isHpqZUxHTjYRJp1jjX1ghmY?usp=sharing)

## 🔗 Akses Proyek

- **Repository GitHub:** [submission-Proyek-Analisis-Data](https://github.com/RiniWu/submission-Proyek-Analisis-Data)
- **Google Colab:** [Buka Notebook Analisis](https://colab.research.google.com/drive/1FiqH1jn6isHpqZUxHTjYRJp1jjX1ghmY?usp=sharing)
- **Dashboard Streamlit:** [Lihat Dashboard](https://6zenhokbgreyok3ejkvaxp.streamlit.app/)

## 🎯 Tujuan Analisis

Analisis ini dilakukan untuk menjawab beberapa pertanyaan bisnis berikut:

1. Bagaimana tren revenue bulanan dan kategori produk yang berkontribusi terhadap penjualan?
2. Bagaimana hubungan antara ketepatan waktu pengiriman dan skor ulasan pelanggan?
3. Bagaimana karakteristik pelanggan berdasarkan segmentasi RFM (_Recency, Frequency, Monetary_)?
4. Bagaimana distribusi revenue dan rata-rata waktu pengiriman berdasarkan state pelanggan?

## 🛠️ Tools dan Teknologi

Teknologi yang digunakan dalam proyek ini meliputi:

- **Python** — bahasa pemrograman untuk analisis data.
- **Pandas** — pengolahan dan manipulasi data.
- **NumPy** — komputasi numerik.
- **Matplotlib** — visualisasi data.
- **Seaborn** — visualisasi statistik.
- **Streamlit** — pengembangan dashboard interaktif.
- **Folium** — visualisasi data geografis.

## 🎛️ Fitur Interaktif

Dashboard menyediakan filter pada sidebar yang langsung memperbarui seluruh KPI, grafik, tabel, dan peta:

- **Rentang tanggal pembelian:** menampilkan data pada periode tertentu.
- **State pelanggan:** menyaring data berdasarkan satu atau beberapa state. Jika tidak ada state yang dipilih, seluruh state ditampilkan.
- **Kategori produk:** menyaring data berdasarkan satu atau beberapa kategori. Jika tidak ada kategori yang dipilih, seluruh kategori ditampilkan.

## 📊 Fitur Dashboard

Dashboard interaktif menyediakan beberapa visualisasi utama untuk membantu memahami kondisi bisnis e-commerce, yaitu:

- **Tren Revenue Bulanan:** memantau perkembangan revenue dari waktu ke waktu.
- **Kategori Produk:** menganalisis kontribusi kategori produk terhadap revenue.
- **Pengiriman dan Review:** mengevaluasi hubungan antara ketepatan waktu pengiriman dan skor ulasan pelanggan.
- **Segmentasi RFM:** memahami karakteristik pelanggan berdasarkan Recency, Frequency, dan Monetary.
- **Peta Geografis:** melihat distribusi revenue dan waktu pengiriman berdasarkan state pelanggan.

## 🔍 Hasil dan Kesimpulan Analisis

### 1. Penjualan

Kategori produk dengan revenue tertinggi dapat menjadi prioritas dalam pengelolaan stok dan penyusunan strategi promosi.

### 2. Pengiriman

Perbedaan skor ulasan antara pesanan yang dikirim tepat waktu dan terlambat perlu menjadi perhatian dalam evaluasi kualitas layanan logistik.

### 3. Pelanggan

Segmen **At-Risk High Spenders** merupakan peluang untuk menjalankan strategi reaktivasi karena memiliki nilai revenue yang relatif besar.

### 4. Geospasial

Distribusi revenue dan waktu pengiriman berdasarkan state dapat membantu menentukan prioritas wilayah dalam perencanaan distribusi dan evaluasi layanan logistik.

## 💡 Rekomendasi Bisnis

Berdasarkan hasil analisis, beberapa rekomendasi yang dapat dipertimbangkan adalah:

1. Memprioritaskan pengelolaan stok dan promosi pada kategori produk dengan revenue tinggi.
2. Mengevaluasi proses pengiriman pada state dengan durasi pengiriman terlama.
3. Menjalankan kampanye reaktivasi untuk segmen **At-Risk High Spenders** serta mengembangkan program loyalitas untuk mendorong pembelian berulang.
4. Memanfaatkan informasi revenue per state untuk mendukung perencanaan distribusi dan evaluasi mitra logistik.

## 📁 Struktur Proyek

```text
E-Commerce Public Dataset/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
│   └── state_geo.csv
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## ⚙️ Setup Environment

Gunakan environment terisolasi agar library proyek tidak bentrok dengan package lain. Proyek ini disarankan dijalankan menggunakan Python 3.10 atau lebih baru.

Sebelum memulai, pastikan Python atau Anaconda telah terinstal pada komputer.

### 1. Setup Environment dengan Anaconda

Buat environment Conda menggunakan Python 3.11, kemudian aktifkan environment tersebut.

```bash
conda create --name main-ds python=3.11
conda activate main-ds
```

Clone repository GitHub dan masuk ke direktori proyek jika belum memilikinya secara lokal.

```bash
git clone https://github.com/RiniWu/submission-Proyek-Analisis-Data.git
cd submission-Proyek-Analisis-Data
```

Instal seluruh library yang dibutuhkan melalui `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 2. Setup Environment dengan Shell/Terminal (venv)

Clone repository GitHub dan masuk ke direktori proyek.

```bash
git clone https://github.com/RiniWu/submission-Proyek-Analisis-Data.git
cd submission-Proyek-Analisis-Data
```

Buat virtual environment.

```bash
python -m venv venv
```

Aktifkan virtual environment sesuai sistem operasi yang digunakan.

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Setelah environment aktif, instal seluruh dependensi proyek.

```bash
pip install -r requirements.txt
```

### 3. Setup Environment dengan Pipenv

Pastikan Python dan Pipenv telah terinstal. Clone repository terlebih dahulu jika belum tersedia di komputer.

```bash
git clone https://github.com/RiniWu/submission-Proyek-Analisis-Data.git
cd submission-Proyek-Analisis-Data
```

Instal dependensi yang didefinisikan pada konfigurasi Pipenv dan aktifkan environment.

```bash
pipenv install
pipenv shell
```

Instal library dari `requirements.txt` apabila diperlukan.

```bash
pip install -r requirements.txt
```

**Catatan:** Penggunaan Pipenv memerlukan file konfigurasi seperti `Pipfile`. Jika repository hanya menyediakan `requirements.txt`, metode `venv` atau Anaconda merupakan pilihan yang lebih sederhana.

## 🚀 Menjalankan Dashboard Secara Lokal

Pastikan environment sudah aktif dan terminal berada di direktori utama proyek, yaitu folder yang berisi direktori `dashboard/`.

Jalankan dashboard menggunakan perintah berikut.

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis di browser pada alamat berikut.

```text
http://localhost:8501
```

Jika dashboard tidak terbuka secara otomatis, salin alamat lokal yang ditampilkan di terminal ke browser.

Untuk menghentikan dashboard, tekan `Ctrl + C` pada terminal.

**Catatan:** Dashboard membaca file `dashboard/main_data.csv` dan `data/state_geo.csv`. Oleh karena itu, jalankan perintah dari direktori utama proyek agar path file dapat ditemukan dengan benar.

## 📓 Menjalankan Notebook

Notebook analisis tersedia dalam file `notebook.ipynb`.

Untuk menjalankannya secara lokal:

1. Aktifkan environment proyek.
2. Pastikan seluruh dataset tersedia pada direktori `data/`.
3. Buka `notebook.ipynb` menggunakan Jupyter Notebook atau JupyterLab.
4. Jalankan seluruh sel notebook secara berurutan.
5. Notebook akan memproses dataset dan menghasilkan file `dashboard/main_data.csv` serta `data/state_geo.csv` yang digunakan oleh dashboard.

Jika menggunakan Google Colab, buka notebook melalui tautan yang tersedia pada bagian **Akses Proyek**. Sesuaikan path dataset dan direktori output dengan lokasi penyimpanan file di lingkungan Colab.

## 📚 Dataset

Dataset yang digunakan dalam proyek ini adalah **E-Commerce Public Dataset** dari DiCoding.

## 👩‍💻 Penulis

**Rini Wulandari**

---

_Dashboard analisis telah di-deploy dan dapat diakses secara publik melalui Streamlit._
