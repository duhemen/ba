# app_styles.py
# Modul Khusus Gaya Visual QSS Tema Terang Korporat Modern

CORPORATE_LIGHT_STYLE = """
    QMainWindow {
        background-color: #f3f4f6;
    }
    QLabel {
        color: #212529;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        font-weight: 500;
    }
    QWidget#SidebarPanel {
        background-color: #1e293b;
        border-top-left-radius: 12px;
        border-bottom-left-radius: 12px;
    }
    QLabel#SidebarTitle {
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        padding: 10px;
    }
    QPushButton.MenuBtn {
        background-color: transparent;
        color: #cbd5e1;
        border: none;
        border-radius: 6px;
        padding: 12px 15px;
        text-align: left;
        font-size: 13px;
        font-weight: bold;
        font-family: 'Segoe UI';
    }
    QPushButton.MenuBtn:hover {
        background-color: #334155;
        color: #ffffff;
    }
    QPushButton.MenuBtn:checked {
        background-color: #0078d4;
        color: #ffffff;
    }
    QComboBox, QLineEdit, QDateEdit {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 13px;
        color: #212529;
    }
    QComboBox:focus, QLineEdit:focus, QDateEdit:focus {
        border: 2px solid #0078d4;
        background-color: #f9fbfd;
    }
    QPushButton#BtnPost {
        background-color: #0078d4;
        color: #ffffff !important;
        border: none;
        border-radius: 6px;
        padding: 12px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton#BtnPost:hover {
        background-color: #006cc1;
    }
    QPushButton.ActionBtn {
        background-color: #ffffff;
        color: #4b5563;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 8px 14px;
        font-size: 12px;
        font-weight: bold;
        font-family: 'Segoe UI';
    }
    QPushButton.ActionBtn:hover {
        background-color: #f3f4f6;
        color: #1f2937;
        border: 1px solid #9ca3af;
    }
    QTableWidget {
        background-color: #ffffff;
        gridline-color: #e5e7eb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        color: #212529;
        font-family: 'Segoe UI';
    }
    QHeaderView::section {
        background-color: #0078d4;
        color: #ffffff;
        padding: 8px;
        font-weight: bold;
        font-size: 12px;
        border: 1px solid #006cc1;
    }
    QTextBrowser#DocPreview {
        background-color: #ffffff;
        color: #212529;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
    }
"""
