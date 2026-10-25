import sys
from typing import NoReturn

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from .theme import error_dialog_stylesheet


def show_critical_error(
    title: str, message: str, error_detail: str = ""
) -> NoReturn:
    """Zobrazi celoobrazovkovou chybovou obrazovku s vycentrovanymi texty a tlacitky
    a po potvrzeni bezpečně ukonci aplikaci.

    Nepouziva QMessageBox, protoze ten ma v Qt pevny interni layout, ktery
    neumoznuje roztahnout a vycentrovat obsah pres celou obrazovku.
    """
    dialog = QDialog()
    dialog.setObjectName("errorScreen")
    dialog.setWindowTitle(title)
    dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    dialog.setStyleSheet(error_dialog_stylesheet())

    # zajisti plnou velikost obrazovky i v prostredi bez spravce oken (napr. kontejner)
    screen = QApplication.primaryScreen()
    if screen is not None:
        dialog.setGeometry(screen.geometry())

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(80, 60, 80, 60)
    layout.setSpacing(30)

    # horni pruzna mezera pro vertikalni vycentrovani
    layout.addStretch(1)

    # nadpis chyby (vycentrovany)
    title_label = QLabel(title)
    title_label.setObjectName("errorTitle")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setWordWrap(True)
    layout.addWidget(title_label)

    # hlavni text chyby (vycentrovany)
    msg_label = QLabel(message)
    msg_label.setObjectName("errorMessage")
    msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    msg_label.setWordWrap(True)
    layout.addWidget(msg_label)

    # volitelny technicky detail (ve vychozim stavu skryty, lze rozbalit tlacitkem)
    detail_label = QLabel(f"Technický detail chyby:\n{error_detail}")
    detail_label.setObjectName("errorDetail")
    detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    detail_label.setWordWrap(True)
    detail_label.hide()

    # radek s tlacitky - vycentrovany pomoci pruznych mezer po stranach
    btn_layout = QHBoxLayout()
    btn_layout.setSpacing(20)
    btn_layout.addStretch(1)

    if error_detail:
        detail_btn = QPushButton("Zobrazit podrobnosti")

        def toggle_detail() -> None:
            is_visible = detail_label.isVisible()
            detail_label.setVisible(not is_visible)
            detail_btn.setText(
                "Skrýt podrobnosti" if not is_visible else "Zobrazit podrobnosti"
            )

        detail_btn.clicked.connect(toggle_detail)
        btn_layout.addWidget(detail_btn)

    exit_btn = QPushButton("Ukončit")
    exit_btn.setObjectName("exitBtn")
    exit_btn.clicked.connect(dialog.accept)
    btn_layout.addWidget(exit_btn)

    btn_layout.addStretch(1)
    layout.addLayout(btn_layout)

    if error_detail:
        layout.addWidget(detail_label)

    # spodni pruzna mezera pro vertikalni vycentrovani
    layout.addStretch(1)

    dialog.showFullScreen()
    dialog.exec()
    sys.exit(1)
