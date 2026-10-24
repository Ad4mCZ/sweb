import sys
from typing import NoReturn

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from .theme import error_dialog_stylesheet


def show_critical_error(
    title: str, message: str, error_detail: str = ""
) -> NoReturn:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)

    if error_detail:
        msg.setDetailedText(f"Technický detail chyby: \n{error_detail}")

    # styl je spolecny s ostatnimi dialogy, viz theme.py
    msg.setStyleSheet(error_dialog_stylesheet())

    msg.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    msg.showFullScreen()
    msg.exec()
    sys.exit(1)
