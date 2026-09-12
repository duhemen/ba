# report_generator.py
# Modul Khusus Penanganan Generator Dokumen Manifes Laporan BP2JK_Kalteng dengan Jalur Absolut & Logo Proporsional

import os
import base64
import pandas as pd
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QMessageBox

class ReportGenerator:
    def __init__(self, jalur_lengkap, output_dir):
        self.jalur_lengkap = jalur_lengkap
        self.output_dir = output_dir

    def aksi_fungsi_cetak(self, parent_widget, nama_sheet, config_data):
        """Membuka QPrintDialog resmi sistem untuk memilih printer fisik yang ready."""
        if not os.path.exists(self.jalur_lengkap):
            QMessageBox.warning(parent_widget, "Data Kosong", "Berkas database Excel tidak ditemukan.")
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, parent_widget)
        
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            document = QTextDocument()
            html_konten = self.buat_struktur_html_manifes(nama_sheet, "MANIFES CETAK FISIK", config_data)
            document.setHtml(html_konten)
            document.print(printer)
            QMessageBox.information(parent_widget, "Cetak Sukses", f"Dokumen '{nama_sheet}' berhasil dikirim ke antrean mesin printer.")

    def aksi_fungsi_pdf(self, parent_widget, nama_sheet, config_data):
        """Membuat berkas PDF murni asli (.pdf) secara langsung berbasis HTML dalam layout Landscape."""
        if not os.path.exists(self.jalur_lengkap):
            QMessageBox.warning(parent_widget, "Data Kosong", "Berkas database Excel tidak ditemukan.")
            return

        path_pdf = os.path.join(self.output_dir, f"Ekspor_{nama_sheet}.pdf")
        
        # 1. Inisialisasi printer resolusi tinggi
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(path_pdf)
        
        # 2. KUNCI ORIENTASI KERTAS SECARA ABSOLUT KE LANDSCAPE DI PYQT6
        from PyQt6.QtGui import QPageLayout, QPageSize
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)

        # 3. Render dokumen HTML ke printer
        document = QTextDocument()
        html_konten = self.buat_struktur_html_manifes(nama_sheet, "MANIFES ARSIP PDF", config_data)
        document.setHtml(html_konten)
        document.print(printer)

        QMessageBox.information(parent_widget, "Ekspor PDF Sukses", f"Berkas PDF resmi berhasil diterbitkan di:\n{path_pdf}")


    def buat_struktur_html_manifes(self, nama_sheet, tipe_manifes, config_data):
        """Membaca data Excel dan membungkusnya ke HTML dengan Kop Dinamis dan LOGO PROPORSI KECIL."""
        try:
            # 1. Penanganan filter data Jurnal Khusus dari Jurnal Umum
            if nama_sheet == "Jurnal Khusus":
                df = pd.read_excel(self.jalur_lengkap, sheet_name="Jurnal Umum")
                df = df[df['Keterangan'].str.contains('Pembayaran|Pembelian|Kas', case=False, na=False)].copy()
                df.reset_index(drop=True, inplace=True)
            else:
                df = pd.read_excel(self.jalur_lengkap, sheet_name=nama_sheet)
            
                        # 2. Pelacakan Jalur Absolut Berkas Gambar (Mendukung PyInstaller _MEIPASS Bundle)
            import sys
            nama_file_logo = config_data.get("logo_path", "logo_keu.png")
            
            if not os.path.isabs(nama_file_logo):
                # Jika berjalan sebagai .exe hasil compile PyInstaller
                if hasattr(sys, '_MEIPASS'):
                    nama_file_logo = os.path.join(sys._MEIPASS, nama_file_logo)
                else:
                    nama_file_logo = os.path.join(os.getcwd(), nama_file_logo)
                    
            img_base64 = ""
            if os.path.exists(nama_file_logo):
                with open(nama_file_logo, "rb") as image_file:
                    img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            src_gambar = f"data:image/png;base64,{img_base64}" if img_base64 else ""
            font_size_val = config_data.get("ukuran_font", "11")

            # STRUKTUR PENATAAN CSS LOGO DIKUNCI KECIL & PROPORSI
            html = f"""
            <html>
            <head>
                <style>
                    @page {{ size: landscape; margin: 20mm; }}
                    body {{ 
                        font-family: 'Segoe UI', Arial, sans-serif; 
                        color: #212529; 
                        margin: 0; 
                        font-size: {font_size_val}pt; 
                        line-height: 1.4;
                    }}
                    .header-table {{
                        width: 100%;
                        border-collapse: collapse;
                        border-bottom: 3pt double #1a1b26;
                        margin-bottom: 25pt;
                    }}
                    .header-table td {{
                        border: none !important;
                        padding: 5pt;
                    }}
                    .logo-td {{
                        width: 10%;
                        text-align: left;
                        vertical-align: middle;
                        padding: 5pt;
                    }}
                    .title-td {{
                        width: 90%;
                        text-align: center;
                        vertical-align: middle;
                        padding-right: 10%;
                    }}
                    .logo-img {{
                        /* Menggunakan pembatas mm agar ukuran konstan di portrait maupun landscape */
                        max-height: 20mm;  
                        max-width: 20mm;
                        width: auto;
                        height: auto;
                        display: block;
                    }}
                    .main-title {{ 
                        font-size: 18pt; 
                        font-weight: bold; 
                        color: #0078d4; 
                        margin: 0; 
                    }}
                    .sub-title {{
                        font-size: 13pt;
                        font-weight: bold;
                        color: #1f2937;
                        margin: 4pt 0 0 0;
                    }}
                    .meta-info {{ 
                        font-size: 10.5pt; 
                        margin: 6pt 0 0 0; 
                        font-weight: 500; 
                        color: #4b5563;
                    }}
                    table {{ 
                        border-collapse: collapse; 
                        width: 100%; 
                        font-size: {int(font_size_val)-1}pt; 
                    }}
                    th {{ 
                        background-color: #0078d4; 
                        color: white; 
                        padding: 10pt 6pt; 
                        text-align: left; 
                        font-weight: bold; 
                        border: 1pt solid #006cc1; 
                    }}
                    td {{ 
                        padding: 9pt 6pt; 
                        border: 1pt solid #e5e7eb; 
                        word-break: break-all;
                    }}
                    tr:nth-child(even) {{ 
                        background-color: #f9fafb; 
                    }}
                </style>
            </head>
            <body>
                <table class='header-table'>
                    <tr>
                        <td class='logo-td'>
                            {"<img class='logo-img' src='" + src_gambar + "'>" if src_gambar else "<span style='color:red;font-size:8pt;'>Logo Kosong</span>"}
                        </td>
                        <td class='title-td'>
                            <div class='main-title'>{config_data['nama_instansi']}</div>
                            <div class='sub-title'>{config_data['sub_title']}</div>
                            <div class='meta-info'>KELOMPOK SHEET DATA : {nama_sheet.upper()} &nbsp;|&nbsp; STATUS VERIFIKASI : SECURED SHA-256 LEDGER ({tipe_manifes})</div>
                        </td>
                    </tr>
                </table>
                <table>
                    <thead>
                        <tr>
            """
            
            for col in df.columns:
                html += f"<th>{col}</th>"
            html += "</tr></thead><tbody>"
            
            for _, row in df.iterrows():
                html += "<tr>"
                for col_idx, val in enumerate(row.values):
                    if isinstance(val, (int, float)) and val > 0 and "Kode" not in str(df.columns[col_idx]) and "Ref" not in str(df.columns[col_idx]):
                        val_str = f"Rp {val:,.0f}"
                    else:
                        val_str = str(val) if pd.notna(val) else "-"
                    html += f"<td>{val_str}</td>"
                html += "</tr>"
                
            html += "</tbody></table></body></html>"
            return html
        except Exception as e:
            return f"<html><body><h3>Gagal Memproses Manifes Laporan Keuangan: {str(e)}</h3></body></html>"
