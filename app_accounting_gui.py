# app_accounting_gui.py
# Berkas Utama Aplikasi Akuntansi Modern Premium dengan Arsitektur Split Modul Clean Code

import sys
import os
import subprocess
import json
import pandas as pd

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTabWidget, QMessageBox, 
                             QPushButton, QButtonGroup, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QHeaderView, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

# Import modul lokal buatan kita
from accounting_engine import ImmutableAccountingEngine
from report_generator import ReportGenerator  # IMPORT MODUL SPLIT BARU KITA
from app_styles import CORPORATE_LIGHT_STYLE
from form_widget import TransactionFormWidget

class AccountingAppWorkspace(QMainWindow):
    def __init__(self):
        super().__init__()
        self.output_dir = r"C:\edge_ai\accounting_app_version"
        self.engine = ImmutableAccountingEngine(output_dir=self.output_dir)
        self.file_baku = "sistem_akuntansi_baku.xlsx"
        self.jalur_lengkap = os.path.join(self.output_dir, self.file_baku)
        self.config_file = "config_satker.json"
        
        # Menginisialisasi jembatan pemicu generator cetak dari modul split
        self.reporter = ReportGenerator(self.jalur_lengkap, self.output_dir)
        
        self.config_data = {
            "nama_instansi": "Buku Pencatatan Akuntansi BP2JK_Kalteng",
            "sub_title": "MANIFES LAPORAN KEUANGAN BP2JK KALTENG",
            "logo_path": "logo_keu.png",  # <-- REVISI NAMA FILE DI SINI
            "ukuran_font": "11"
        }
        self.muat_konfigurasi_json()

        self.setWindowTitle("Sistem Informasi Akuntansi Premium - Imutabel Ledger")
        self.setGeometry(50, 50, 1350, 850)
        
        if os.path.exists(r"C:\edge_ai\edge_ai.ico"):
            self.setWindowIcon(QIcon(r"C:\edge_ai\edge_ai.ico"))
            
        self.init_ui()

    def muat_konfigurasi_json(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config_data.update(json.load(f))
            except Exception as e:
                print(f"Gagal memuat config: {e}")

    def simpan_konfigurasi_json(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Pengaturan Disimpan", "Konfigurasi instansi berhasil diperbarui!")
            self.muat_data_ke_layar_laporan()
        except Exception as e:
            QMessageBox.critical(self, "Gagal Menyimpan", f"Error sistem: {str(e)}")

    def init_ui(self):
        widget_utama = QWidget()
        self.setCentralWidget(widget_utama)
        layout_global = QHBoxLayout(widget_utama)
        layout_global.setContentsMargins(10, 10, 10, 10)
        layout_global.setSpacing(0)

        self.setStyleSheet(CORPORATE_LIGHT_STYLE)

        # PANEL SIDEBAR KIRI
        sidebar = QWidget()
        sidebar.setObjectName("SidebarPanel")
        sidebar.setFixedWidth(220)
        layout_sidebar = QVBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(10, 20, 10, 20)
        layout_sidebar.setSpacing(8)

        logo_title = QLabel("📂  Akuntansi Buku")
        logo_title.setObjectName("SidebarTitle")
        layout_sidebar.addWidget(logo_title)
        layout_sidebar.addSpacing(15)

        self.menu_group = QButtonGroup(self)
        self.menu_group.setExclusive(True)

        menu_items = [
            ("📊  Dashboard Analisis", 0),
            ("📝  Entri Transaksi Baru", 1),
            ("📓  Buku Jurnal Umum", 2),
            ("📕  Buku Jurnal Khusus", 3),
            ("📘  Buku Besar Utama", 4),
            ("📈  Laporan Laba Rugi", 5),
            ("⚙️  Pengaturan Satker", 6)
        ]

        self.buttons = {}
        for teks, indeks in menu_items:
            btn = QPushButton(teks)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("class", "MenuBtn")
            layout_sidebar.addWidget(btn)
            self.menu_group.addButton(btn, indeks)
            self.buttons[indeks] = btn

        layout_sidebar.addSpacing(20)
        self.btn_audit = QPushButton("🛡️  Audit Rekonsiliasi")
        self.btn_audit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_audit.setStyleSheet("""
            QPushButton {
                background-color: #d20f39; color: white; font-weight: bold; 
                border-radius: 6px; padding: 10px; border: none;
            }
            QPushButton:hover { background-color: #bc0d32; }
        """)
        self.btn_audit.clicked.connect(self.jalankan_fitur_audit)
        layout_sidebar.addWidget(self.btn_audit)

        layout_sidebar.addStretch()
        layout_global.addWidget(sidebar)

        self.tabs_konten = QTabWidget()
        self.tabs_konten.tabBar().hide()
        layout_global.addWidget(self.tabs_konten)

        self.menu_group.idClicked.connect(self.pindah_halaman_tab)
        
        self.rakit_halaman_dashboard()
        self.rakit_halaman_formulir()
        self.rakit_halaman_laporan("Jurnal Umum", 2)
        self.rakit_halaman_laporan("Jurnal Khusus", 3)
        self.rakit_halaman_laporan("Buku Besar", 4)
        self.rakit_halaman_laba_rugi()
        self.rakit_halaman_pengaturan()

        self.buttons[0].setChecked(True)
        self.pindah_halaman_tab(0)

    def pindah_halaman_tab(self, indeks):
        self.tabs_konten.setCurrentIndex(indeks)
        self.muat_data_ke_layar_laporan()

    def rakit_halaman_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        layout.addWidget(QLabel("📊  Dashboard Ringkasan Executive Keuangan"))
        
        dash_content = QHBoxLayout()
        self.table_dash_summary = QTableWidget()
        self.table_dash_summary.setColumnCount(2)
        self.table_dash_summary.setHorizontalHeaderLabels(["Nama Akun Rekening", "Saldo Akhir"])
        self.table_dash_summary.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_dash_summary.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        dash_content.addWidget(self.table_dash_summary, stretch=2)
        
        self.dash_figure = Figure(figsize=(5, 4), dpi=100)
        self.dash_canvas = FigureCanvas(self.dash_figure)
        self.dash_ax = self.dash_figure.add_subplot(111)
        dash_content.addWidget(self.dash_canvas, stretch=3)
        
        layout.addLayout(dash_content)
        self.tabs_konten.addTab(page, "Dashboard")

    def rakit_halaman_formulir(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.form_entri = TransactionFormWidget()
        self.form_entri.btn_posting.clicked.connect(self.proses_simpan_transaksi)
        layout.addWidget(self.form_entri)
        self.tabs_konten.addTab(page, "Formulir")

    def rakit_halaman_laporan(self, nama_sheet, indeks_tab):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        layout_header = QHBoxLayout()
        layout_header.addWidget(QLabel(f"Daftar Tabel Finansial - {nama_sheet}"))
        layout_header.addStretch()
        
        btn_print = QPushButton("🖨️  Cetak")
        btn_print.setProperty("class", "ActionBtn")
        btn_print.clicked.connect(lambda: self.reporter.aksi_fungsi_cetak(self, nama_sheet, self.config_data))
        
        btn_pdf = QPushButton("📕  Ekspor PDF")
        btn_pdf.setProperty("class", "ActionBtn")
        btn_pdf.clicked.connect(lambda: self.reporter.aksi_fungsi_pdf(self, nama_sheet, self.config_data))
        
        btn_excel = QPushButton("📊  Buka Excel")
        btn_excel.setProperty("class", "ActionBtn")
        btn_excel.clicked.connect(self.aksi_fungsi_excel)
        
        layout_header.addWidget(btn_print)
        layout_header.addWidget(btn_pdf)
        layout_header.addWidget(btn_excel)
        layout.addLayout(layout_header)
        
        layout_perkakas = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText(f"🔍  Cari data pada {nama_sheet} secara instan...")
        search_box.textChanged.connect(lambda: self.filter_tabel_live(indeks_tab))
        layout_perkakas.addWidget(search_box)
        
        setattr(self, f"search_box_tab_{indeks_tab}", search_box)
        layout.addLayout(layout_perkakas)
        
        tabel_view = QTableWidget()
        tabel_view.setSortingEnabled(True)
        tabel_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabel_view.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabel_view.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(tabel_view)
        
        setattr(self, f"tabel_tab_{indeks_tab}", tabel_view)
        self.tabs_konten.addTab(page, nama_sheet)

    def rakit_halaman_laba_rugi(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        layout.addWidget(QLabel("📈  Laporan Perhitungan Laba Rugi UPT Satker Bersih"))

        self.tabel_lr = QTableWidget()
        self.tabel_lr.setColumnCount(2)
        self.tabel_lr.setHorizontalHeaderLabels(["Komponen Keuangan Akuntansi", "Jumlah Total (IDR)"])
        self.tabel_lr.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabel_lr.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabel_lr)
        self.tabs_konten.addTab(page, "Laba Rugi")

    def rakit_halaman_pengaturan(self):
        """Merakit UI Form Pengaturan Parameter Satker secara Dinamis."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        layout.addWidget(QLabel("⚙️  Pengaturan Struktur Organisasi & Parameter Laporan Satker"))

        layout.addWidget(QLabel("Nama Instansi Utama / Satker (Kop Atas):"))
        self.edit_instansi = QLineEdit(self.config_data["nama_instansi"])
        layout.addWidget(self.edit_instansi)

        layout.addWidget(QLabel("Sub-Judul Dokumen Manifes Laporan:"))
        self.edit_sub_title = QLineEdit(self.config_data["sub_title"])
        layout.addWidget(self.edit_sub_title)

        layout.addWidget(QLabel("Berkas File Logo Instansi (.png aktif di root):"))
        layout_logo = QHBoxLayout()
        self.edit_logo_path = QLineEdit(self.config_data["logo_path"])
        layout_logo.addWidget(self.edit_logo_path)
        btn_cari_logo = QPushButton("Cari File")
        btn_cari_logo.setProperty("class", "ActionBtn")
        btn_cari_logo.clicked.connect(self.aksi_pilih_berkas_logo)
        layout_logo.addWidget(btn_cari_logo)
        layout.addLayout(layout_logo)

        layout.addWidget(QLabel("Ukuran Standar Font Laporan Cetak (Poin/Pt):"))
        self.edit_font_size = QLineEdit(self.config_data["ukuran_font"])
        layout.addWidget(self.edit_font_size)

        layout.addSpacing(15)
        btn_simpan_config = QPushButton("💾  Simpan Perubahan Pengaturan")
        btn_simpan_config.setObjectName("BtnPost")
        btn_simpan_config.clicked.connect(self.aksi_simpan_pengaturan_form)
        layout.addWidget(btn_simpan_config)

        layout.addStretch()
        self.tabs_konten.addTab(page, "Pengaturan")

    def aksi_pilih_berkas_logo(self):
        """Membuka dialog pencarian file logo lokal secara visual."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Logo Satker", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            if os.path.dirname(file_path) == os.getcwd():
                self.edit_logo_path.setText(os.path.basename(file_path))
            else:
                self.edit_logo_path.setText(file_path)

    def aksi_simpan_pengaturan_form(self):
        """Mengambil data dari inputan form dan memicu penyimpanan permanen."""
        self.config_data["nama_instansi"] = self.edit_instansi.text().strip()
        self.config_data["sub_title"] = self.edit_sub_title.text().strip()
        self.config_data["logo_path"] = self.edit_logo_path.text().strip()
        self.config_data["ukuran_font"] = self.edit_font_size.text().strip()
        self.simpan_konfigurasi_json()

    def muat_data_ke_layar_laporan(self):
        """Sinkronisasi data backend Excel dengan visualisasi tabel dan grafik UI."""
        if not os.path.exists(self.jalur_lengkap): 
            return
        try:
            df_bb = pd.read_excel(self.jalur_lengkap, sheet_name="Buku Besar")
            self.table_dash_summary.setRowCount(len(df_bb.index))
            akuns = []
            saldos = []
            
            for idx, row in df_bb.iterrows():
                nama_ak = str(row["Nama Akun Rekening"])
                sal_val = float(row["Total Saldo Mutasi"]) if pd.notna(row["Total Saldo Mutasi"]) else 0.0
                akuns.append(nama_ak.split(" - ")[1] if " - " in nama_ak else nama_ak)
                saldos.append(sal_val)
                
                self.table_dash_summary.setItem(idx, 0, QTableWidgetItem(nama_ak))
                item_sal = QTableWidgetItem(f"Rp {sal_val:,.0f}")
                item_sal.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table_dash_summary.setItem(idx, 1, item_sal)
            
            self.dash_ax.clear()
            self.dash_figure.patch.set_facecolor('#ffffff')
            self.dash_ax.set_facecolor('#f8f9fa')
            self.dash_ax.bar(akuns, saldos, color=['#0078d4', '#7aa2f7', '#bb9af7', '#e0af68', '#a6e3a1', '#d20f39'])
            self.dash_ax.set_title("Statistik Saldo Akhir Komponen Finansial", fontsize=11, fontweight='bold', color='#212529')
            self.dash_ax.set_ylabel("Nominal Saldo (IDR)", fontsize=9)
            self.dash_ax.tick_params(axis='x', rotation=15, labelsize=8)
            self.dash_canvas.draw()

            df_ju = pd.read_excel(self.jalur_lengkap, sheet_name="Jurnal Umum")
            self.isi_data_ke_table_widget(self.tabel_tab_2, df_ju)
            
            df_jk = df_ju[df_ju['Keterangan'].str.contains('Pembayaran|Pembelian|Kas', case=False, na=False)].copy()
            if df_jk.empty:
                self.isi_data_ke_table_widget(self.tabel_tab_3, df_ju)
            else:
                df_jk.reset_index(drop=True, inplace=True)
                self.isi_data_ke_table_widget(self.tabel_tab_3, df_jk)

            self.isi_data_ke_table_widget(self.tabel_tab_4, df_bb)
            self.hitung_dan_isi_laba_rugi(df_bb)
            
        except Exception as e:
            print(f"[Error Pemetaan Laporan UI]: {str(e)}")

    def hitung_dan_isi_laba_rugi(self, df_bb):
        """Memproses perhitungan pendapatan dikurangi beban operasional satker."""
        self.tabel_lr.setRowCount(3)
        try: 
            pendapatan = float(df_bb[df_bb['Kode'] == 401]['Total Saldo Mutasi'].values)
        except: 
            pendapatan = 0.0
        try: 
            beban = float(df_bb[df_bb['Kode'] == 501]['Total Saldo Mutasi'].values)
        except: 
            beban = 0.0
            
        laba_bersih = pendapatan - beban

        items = [
            ("(+) Total Pendapatan Usaha (Kode 401)", pendapatan),
            ("(-) Total Beban Operasional (Kode 501)", beban),
            ("(=) TOTAL LABA BERSIH PERUSAHAAN", laba_bersih)
        ]

        for idx, (label, nilai) in enumerate(items):
            item_lbl = QTableWidgetItem(label)
            item_val = QTableWidgetItem(f"Rp {nilai:,.0f}")
            if idx == 2:
                font_bold = QFont("Segoe UI", 11, QFont.Weight.Bold)
                item_lbl.setFont(font_bold)
                item_val.setFont(font_bold)
            item_val.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tabel_lr.setItem(idx, 0, item_lbl)
            self.tabel_lr.setItem(idx, 1, item_val)

    def jalankan_fitur_audit(self):
        """Trigger aksi validasi kriptografi ledger."""
        sukses, pesan = self.engine.audit_rekonsiliasi_integritas()
        if sukses: 
            QMessageBox.information(self, "Audit Valid", pesan)
        else: 
            QMessageBox.critical(self, "Security Alert!", pesan)

    def isi_data_ke_table_widget(self, table_widget, dataframe):
        """Mengubah Pandas Dataframe menjadi baris cell QTableWidget secara presisi."""
        table_widget.setSortingEnabled(False)
        table_widget.clear()
        table_widget.setColumnCount(len(dataframe.columns))
        table_widget.setRowCount(len(dataframe.index))
        table_widget.setHorizontalHeaderLabels([str(col) for col in dataframe.columns])
        
        for row_idx, row in dataframe.iterrows():
            for col_idx, value in enumerate(row):
                if isinstance(value, (int, float)) and value > 0 and "Kode" not in str(dataframe.columns[col_idx]):
                    val_str = f"Rp {value:,.0f}"
                else:
                    val_str = str(value) if pd.notna(value) else "-"
                
                item = QTableWidgetItem(val_str)
                if isinstance(value, (int, float)) and "Kode" not in str(dataframe.columns[col_idx]):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                table_widget.setItem(row_idx, col_idx, item)
                
        table_widget.setSortingEnabled(True)

    def filter_tabel_live(self, indeks_tab):
        """Fungsi FILTER & PENCARIAN REAL-TIME: Menyembunyikan baris yang tidak sesuai keyword."""
        search_box = getattr(self, f"search_box_tab_{indeks_tab}")
        tabel_view = getattr(self, f"tabel_tab_{indeks_tab}")
        kata_kunci = search_box.text().lower()
        for row in range(tabel_view.rowCount()):
            baris_cocok = False
            for col in range(tabel_view.columnCount()):
                item = tabel_view.item(row, col)
                if item and kata_kunci in item.text().lower():
                    baris_cocok = True
                    break
            tabel_view.setRowHidden(row, not baris_cocok)

    def proses_simpan_transaksi(self):
        """Validasi data form input sebelum dikunci masuk ledger imutabel Excel."""
        data = self.form_entri.dapatkan_data_form()
        ref_kode = data["ref_full"].split(" - ")[0]
        try:
            debit = float(data["debit_raw"] or 0)
            kredit = float(data["kredit_raw"] or 0)
        except ValueError:
            QMessageBox.warning(self, "Validasi Input", "Nilai nominal Debit/Kredit harus berupa angka!")
            return
        if not data["no_bukti"] or not data["keterangan"]:
            QMessageBox.warning(self, "Validasi Input", "Nomor Bukti dan Keterangan wajib diisi!")
            return

        self.engine.tambah_transaksi_imutabel(data["tanggal"], data["no_bukti"], data["keterangan"], ref_kode, debit, kredit)
        self.form_entri.bersihkan_input_rutin()
        self.muat_data_ke_layar_laporan()
        QMessageBox.information(self, "Ledger Secured", "Transaksi sukses diposting ke ledger Excel terproteksi!")

    def aksi_fungsi_excel(self):
        """Membuka lokasi folder ledger utama."""
        if os.path.exists(self.jalur_lengkap):
            subprocess.Popen(f'explorer /select,"{self.jalur_lengkap}"')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccountingAppWorkspace()
    window.show()
    sys.exit(app.exec())

            
