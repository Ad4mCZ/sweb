import sys
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt


def show_critical_error(title, message, error_detail=""):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)

    if error_detail:
        msg.setDetailedText(f"Technický detail chyby: \n{error_detail}")

    msg.setStyleSheet("""
        QMessageBox {
            background-color: #f5f5f5;
        }
        QLabel {
            font-size: 24px;
            color: black;
        }
        QPushButton {
            font-size: 20px;
            font-weight: bold;
            padding: 15px 40px;
            background-color: #ff2a2a;
            color: white;
            border: 2px solid #cc0000;
        }
    """)

    msg.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    msg.showFullScreen()
    msg.exec()
    sys.exit(1)
