# form_widget.py
# Modul Khusus Penanganan Komponen Formulir Input Akuntansi

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont

class TransactionFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 5px;")
        self.init_sub_ui()

    def init_sub_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        judul_form = QLabel("Formulir Entri Transaksi Jurnal (Immutable)")
        judul_form.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        judul_form.setStyleSheet("color: #0078d4; padding-bottom: 5px; border: none;")
        layout.addWidget(judul_form)

        # 1. Tanggal
        layout.addWidget(QLabel("Tanggal Transaksi Pembukuan:"))
        self.input_tanggal = QDateEdit()
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDate(QDate.currentDate())
        layout.addWidget(self.input_tanggal)

        # 2. No Bukti
        layout.addWidget(QLabel("Nomor Bukti (Kuitansi / Faktur / Cek):"))
        self.input_bukti = QLineEdit()
        self.input_bukti.setPlaceholderText("Contoh: BKK-001, BM-002, FB-2026")
        layout.addWidget(self.input_bukti)

        # 3. Keterangan
        layout.addWidget(QLabel("Keterangan Ringkas Transaksi Keuangan:"))
        self.input_keterangan = QLineEdit()
        self.input_keterangan.setPlaceholderText("Contoh: Setoran modal investasi awal usaha")
        layout.addWidget(self.input_keterangan)

        # 4. Akun Dropdown
        layout.addWidget(QLabel("Rekening Perkiraan Akun (Ref):"))
        self.input_akun = QComboBox()
        self.input_akun.addItems([
            "101 - Kas Utama",
            "102 - Piutang Dagang",
            "201 - Utang Dagang",
            "301 - Modal Pemilik",
            "401 - Pendapatan Usaha",
            "501 - Beban Operasional"
        ])
        layout.addWidget(self.input_akun)

        # 5. Nominal Debit / Kredit
        layout_nominal = QHBoxLayout()
        
        vbox_debit = QVBoxLayout()
        vbox_debit.addWidget(QLabel("Nominal Pos Debit (IDR):"))
        self.input_debit = QLineEdit()
        self.input_debit.setText("0")
        vbox_debit.addWidget(self.input_debit)
        
        vbox_kredit = QVBoxLayout()
        vbox_kredit.addWidget(QLabel("Nominal Pos Kredit (IDR):"))
        self.input_kredit = QLineEdit()
        self.input_kredit.setText("0")
        vbox_kredit.addWidget(self.input_kredit)
        
        layout_nominal.addLayout(vbox_debit)
        layout_nominal.addLayout(vbox_kredit)
        layout.addLayout(layout_nominal)

        # 6. Tombol Aksi
        self.btn_posting = QPushButton("🔒  Posting Transaksi ke Buku Jurnal")
        self.btn_posting.setObjectName("BtnPost")
        self.btn_posting.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_posting)
        
        layout.addStretch()

    def dapatkan_data_form(self):
        """Mengembalikan data inputan mentah dari formulir."""
        return {
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "no_bukti": self.input_bukti.text().strip(),
            "keterangan": self.input_keterangan.text().strip(),
            "ref_full": self.input_akun.currentText(),
            "debit_raw": self.input_debit.text().strip(),
            "kredit_raw": self.input_kredit.text().strip()
        }

    def bersihkan_input_rutin(self):
        """Mengosongkan form isian setelah berhasil diposting."""
        self.input_keterangan.clear()
        self.input_debit.setText("0")
        self.input_kredit.setText("0")
