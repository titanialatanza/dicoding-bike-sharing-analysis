# Proyek Analisis Data — Bike Sharing (Dicoding)

Proyek analisis pola penggunaan layanan Bike Sharing pada **2011–2012** berdasarkan dataset resmi yang disediakan untuk submission Dicoding.

**Identitas penyusun:** Titania Latanza Shauvinna (`titanialatanza`). Notebook menggunakan **template notebook yang ditautkan pada kriteria proyek**, dengan penjelasan setiap tahap mulai dari SMART Questions, Data Wrangling, EDA, Visualization, Analisis Lanjutan, hingga Conclusion & Recommendation.

## Struktur folder

```text
submission_dicoding_bike_sharing/
├── data/
│   ├── day.csv                # Data asli: 731 hari
│   ├── hour.csv               # Data asli: 17.379 jam teramati
│   └── Readme_dataset.txt     # Dokumentasi asli dataset
├── dashboard/
│   ├── dashboard.py           # Streamlit
│   └── main_data.csv          # Data hasil cleaning: 17.544 slot jam
├── notebook.ipynb            # Notebook dengan output eksekusi
├── README.md
├── requirements.txt
└── cek_submission.py
```

## Persiapan lingkungan

1. Ekstrak ZIP **dengan mempertahankan semua subfolder**.
2. Buka **Terminal**/**PowerShell** di direktori `submission_dicoding_bike_sharing` (tempat `requirements.txt` berada).
3. Pastikan Python 3.10–3.12 sudah tersedia, lalu jalankan:

   ```bash
   python -m pip install -r requirements.txt
   ```

   Di Windows, jika `python` tidak tersedia, gunakan `py`.

## Menjalankan dashboard di lokal

Dari folder utama `submission_dicoding_bike_sharing`, jalankan:

```bash
python -m streamlit run dashboard/dashboard.py
```

Buka alamat lokal yang ditampilkan oleh Streamlit di terminal (umumnya `http://localhost:8501`). Di sidebar pilih **2011 & 2012**, **2011**, atau **2012** untuk mengubah seluruh grafik dan metrik.

> File `dashboard/main_data.csv` **sudah disertakan**. Dashboard **tidak** membutuhkan notebook dijalankan ulang untuk ditampilkan. Data dibaca relatif ke lokasi `dashboard.py`, sehingga tidak bergantung pada folder terminal.

## Menjalankan notebook

Buka notebook pada Jupyter Lab/Jupyter Notebook atau VS Code, setel working directory ke folder utama proyek, lalu lakukan **Run All**. Data mentah dibaca dari `data/day.csv` dan `data/hour.csv`. Notebook otomatis memperbarui `dashboard/main_data.csv` di bagian Analisis Lanjutan. Jangan menghapus output notebook sebelum submission.

## Pertanyaan bisnis

1. Bagaimana selisih rata-rata penyewaan per hari di **hari kerja vs non-kerja**, per bulan kalender, selama **1 Januari 2011–31 Desember 2012**?
2. Jam berapa rata-rata jumlah penyewaan **per jam** paling tinggi pada masing-masing jenis hari selama periode tersebut?

Kedua pertanyaan terukur dan berorientasi penyediaan/redistribusi armada. `workingday=0` berarti akhir pekan **atau** hari libur, bukan hanya Sabtu dan Minggu.

## Metodologi kualitas data

- Pemeriksaan tidak menemukan nilai kosong eksplisit, duplikasi tanggal/jam, penyewaan negatif, maupun ketidaksesuaian `cnt = casual + registered`.
- Ada **165 slot jam** yang tidak muncul di `hour.csv`. Validasi menunjukkan **total jam di setiap hari sama persis dengan `day.csv`** dan semua catatan jam asli berisi `cnt > 0`; karenanya **slot tanpa catatan diisi 0 untuk variabel jumlah penyewaan saja**. Setelah itu jumlah baris 731 × 24 = **17.544** dan total penyewaan tidak berubah.
- Nilai kelembapan nol yang mencurigakan ditandai lalu diimputasi dengan median berdasarkan kelompok waktu **hanya di notebook** sebagai penanganan variabel cuaca. Analisis dan dashboard **tidak** menggunakan kelembapan sebagai prediktor.
- Analisis lanjut berupa **binning non-ML** ke tiga kategori relatif berdasarkan persentil dataset penuh.

## Cara pemeriksaan sebelum submit

```bash
python cek_submission.py
```

Script tersebut mengecek file wajib, output notebook, kesesuaian total per hari, kelengkapan 24 jam dan validitas kategori. **Tetap jalankan dashboard di laptop** untuk memeriksa tampilan sesungguhnya.

## Penting sebelum dikirim

- **Periksa ulang** identitas nama, email, dan username di header notebook agar sesuai akun Dicoding.
- Pastikan notebook tetap memuat outputnya setelah mengganti identitas. Jika membuka notebook di tempat lain, gunakan working directory yang benar saat Run All.
- Jika ingin poin tambahan deployment, unggah proyek ke GitHub, deploy pada **Streamlit Community Cloud**, uji bahwa dashboard publik benar-benar berjalan, **baru tambahkan** `url.txt` berisi URL deployment yang valid. **Tidak ada `url.txt` palsu** dalam ZIP ini karena belum ada deployment yang berhasil diverifikasi.
- ZIP folder proyek (bukan file terpisah) sesuai petunjuk Dicoding. Jangan memasukkan `.venv/`, cache, credential, atau folder sistem.

## Rekomendasi operasional

Pertimbangkan ketersediaan sepeda menjelang jam 08.00 dan 17.00 pada hari kerja, serta jam 12.00–14.00 pada hari non-kerja. Ini **indikasi deskriptif**, dan harus dibandingkan dengan stok serta lokasi stasiun aktual sebelum mengambil keputusan.

## Sumber

Fanaee-T, H., & Gama, J. (2013). *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence. Dataset distribusi awal: [UCI Bike Sharing](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset), bersumber dari arsip resmi yang disediakan di halaman submission Dicoding.
