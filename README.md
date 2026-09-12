# 📂 Sistem Informasi Akuntansi Premium - Imutabel Ledger

![Python](https://shields.io)
![PyQt6](https://shields.io)
![Blockchain](https://shields.io)
![Status](https://shields.io)

Aplikasi pembukuan keuangan modern berbasis **Imutabel Ledger** yang dirancang khusus untuk memenuhi standar transparansi, integritas, dan akuntabilitas. Menggunakan sistem pengaman kriptografi berantai (SHA-256) layaknya teknologi *blockchain* untuk mendeteksi manipulasi data ilegal pada berkas database Excel.

---

## 🚀 Fitur Utama Sistem

*   🔒 **Immutable Transaction Ledger:** Mengunci setiap baris jurnal menggunakan sidik jari kriptografi SHA-256 berantai.
*   🛡️ **Blockchain Audit & Auto-Backup:** Memverifikasi integritas database Excel dari manipulasi eksternal. Jika valid, sistem otomatis membuat berkas cadangan bertanda waktu (*timestamp*) di dalam folder `backups/`.
*   📊 **Dashboard Analisis Eksekutif:** Visualisasi grafik batang komponen finansial riil (Matplotlib Canvas) dan ringkasan saldo akun berjalan.
*   📓 **Dua Sistem Jurnal Otomatis:** Memisahkan Buku Jurnal Umum kronologis dan Buku Jurnal Khusus (mutasi Kas, Pembelian, Pembayaran) secara otonom.
*   📈 **Laporan Laba Rugi Otomatis:** Menghitung laba/rugi bersih berjalan satker (Pendapatan Usaha - Beban Operasional).
*   ⚙️ **Pengaturan Satker Dinamis:** Tab konfigurasi untuk mengubah nama instansi, sub-judul, ukuran font, dan unggah berkas logo lokal melalui UI tanpa menyentuh kode program.
*   🖨️ **Native Landscape Printing & PDF:** Cetak fisik langsung lewat `QPrintDialog` Windows dan ekspor berkas `.pdf` murni dengan susunan kop dinamis ber-logo Kementerian Keuangan RI.

---

## 📂 Struktur Arsitektur Program

Aplikasi menerapkan prinsip *Separation of Concerns* (Pemisahan Tanggung Jawab Modul) agar kode terhindar dari konflik *crash*:
*   `app_accounting_gui.py`: Manajemen visual antarmuka pengguna PyQt6, tata letak form, dan *event-handling*.
*   `accounting_engine.py`: Logika matematika akuntansi, manipulasi berkas Excel openpyxl, dan rantai enkripsi SHA-256.
*   `report_generator.py`: Pemroses dokumen cetak manifes berbasis HTML-CSS dan interaksi perangkat printer keras.
*   `app_styles.py`: Pengatur gaya kosmetik korporat modern (QSS style).
*   `form_widget.py`: Komponen masukan entri jurnal finansial.

---

## 🛠️ Panduan Kompilasi Menjadi `buku_akuntan.exe`

Untuk mengubah skrip Python ini menjadi satu file eksekusi mandiri tanpa ketergantungan Python interpreter di komputer target, ikuti langkah-langkah berikut:

1.  Buka terminal PowerShell Anda dan pastikan lingkungan virtual (`edge_ai_env`) aktif.
2.  Install paket compiler PyInstaller:
    ```bash
    pip install pyinstaller
    ```
3.  Eksekusi perintah kompilasi premium berikut di dalam direktori proyek:
    ```bash
    pyinstaller --noconfirm --onedir --windowed --add-data "app_styles.py;." --add-data "form_widget.py;." --add-data "accounting_engine.py;." --add-data "report_generator.py;." --add-data "logo_keu.png;." --icon="C:\edge_ai\edge_ai.ico" --name "buku_akuntan" app_accounting_gui.py
    ```
    *(Catatan: Jika ingin dikompresi menjadi satu file tunggal, Anda bisa mengganti argumen `--onedir` menjadi `--onefile`)*.
4.  File executable final Anda akan berada di dalam folder `dist/buku_akuntan/buku_akuntan.exe`.

---

## 📖 User Guide (Panduan Penggunaan Aplikasi)

### 1. Inisialisasi Awal & Entri Data
*   Saat pertama kali dijalankan, sistem otomatis menerbitkan database `sistem_akuntansi_baku.xlsx` di folder output kerja.
*   Masuk ke menu **📝 Entri Transaksi Baru**. Isilah Tanggal, Nomor Bukti Dokumen (Kuitansi/Faktur), Keterangan mutasi, pilih Akun Rekiran (Ref), masukkan nominal Debit/Kredit, lalu klik **🔒 Posting Transaksi**.

### 2. Pencarian Real-Time & Live Filtering
*   Buka tab **Buku Jurnal Umum** atau **Jurnal Khusus**.
*   Ketik kata kunci tertentu (Misal: *"Gaji"*, *"Komputer"*, atau nominal tertentu) pada kolom pencarian bagian atas. Tabel interaktif PyQt6 akan langsung menyembunyikan baris yang tidak sesuai secara instan.

### 3. Mengubah Profil Satker
*   Masuk ke menu **⚙️ Pengaturan Satker**.
*   Ganti Nama Instansi menjadi `Buku Pencatatan Akuntansi BP2JK_Kalteng` dan sub-judul menjadi `MANIFES LAPORAN KEUANGAN BP2JK KALTENG`.
*   Klik **Cari File** untuk mengarahkan ke berkas gambar `logo_keu.png` Anda di komputer, sesuaikan ukuran font laporan, kemudian klik **💾 Simpan Perubahan Pengaturan**.

### 4. Melakukan Ekspor Dokumen & Cetak Fisik
*   Pada tab laporan finansial apa pun, tekan tombol **📕 Ekspor PDF** untuk menerbitkan arsip dokumen formal berformat `.pdf` lanskap rapi di folder program Anda.
*   Tekan tombol **🖨️ Cetak** untuk membuka jendela pilihan printer fisik bawaan Windows. Pilih perangkat printer Anda yang bertanda *Ready*, lalu klik *Print*.

### 5. Menguji Keamanan Enkripsi (Simulasi Audit)
*   Tekan tombol merah **🛡️ Audit Rekonsiliasi** di sidebar kiri. Jika database aman, pop-up hijau bertuliskan verifikasi sukses dan nama file backup cadangan akan diterbitkan.
*   **Uji Manipulasi:** Tutup aplikasi, buka berkas Excel langsung lewat MS Excel, ubah satu angka nominal transaksi secara ilegal, lalu simpan. Buka kembali aplikasi dan klik tombol audit. Sistem akan mengeluarkan alarm tanda bahaya (*Security Alert*) dan menolak memproses laporan karena rantai hash kriptografi terputus!
