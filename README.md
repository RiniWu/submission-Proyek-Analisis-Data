# submission-Proyek-Analisis-Data

Deskripsi Proyek

Proyek ini bertujuan menganalisis data transaksi Olist E-Commerce untuk memahami kinerja penjualan, performa pengiriman, perilaku pelanggan, dan distribusi geografis revenue di Brasil.

Analisis dilakukan menggunakan Python dan Pandas melalui Google Colab, kemudian disajikan dalam dashboard interaktif menggunakan Streamlit.

Pertanyaan Bisnis

Bagaimana tren revenue bulanan dan kategori produk yang berkontribusi terhadap penjualan?

Bagaimana hubungan ketepatan waktu pengiriman dengan skor ulasan pelanggan?

Bagaimana karakteristik pelanggan berdasarkan segmentasi RFM?

Bagaimana distribusi revenue dan rata-rata waktu pengiriman berdasarkan state pelanggan?

Teknologi yang Digunakan

Python

Pandas dan NumPy

Matplotlib dan Seaborn

Streamlit

Folium

Fitur Dashboard

Ringkasan indikator kinerja penjualan.

Analisis revenue kategori produk dan pertumbuhan penjualan.

Analisis waktu pengiriman dan skor review.

Segmentasi pelanggan menggunakan RFM.

Peta persebaran revenue dan waktu pengiriman berdasarkan state.

Struktur Proyek

E-Commerce-Public-Dataset/
├── dashboard/
│   ├── app.py
│   └── requirements.txt
├── main_data.csv
├── state_geo.csv
├── notebook.ipynb
└── README.md

Cara Menjalankan Dashboard

Pastikan Python telah terpasang.

Buka terminal pada folder dashboard.

Instal dependensi:

python -m pip install -r requirements.txt

Jalankan dashboard:

python -m streamlit run app.py

Buka alamat lokal yang ditampilkan pada terminal.

Sumber Data

Olist E-Commerce Public Dataset.

Catatan

Nama file, struktur folder, dan daftar fitur perlu disesuaikan dengan versi akhir proyek.
