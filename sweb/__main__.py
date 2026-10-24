import logging
import os
import sys

from PyQt6.QtWidgets import QApplication

# QtWebEngineWidgets (pres window -> browser) musi byt importovan jeste pred
# vytvorenim QApplication, jinak Qt skonci chybou. Proto je import zde nahore.
from .window import MainWindow

# prepinace pro Chromium uvnitr QtWebEngine
CHROMIUM_FLAGS = [
    "--disable-gpu",
    # "--disable-software-rasterizer",
    "--disable-dev-shm-usage",
    # "--disable-webgl"
    "--disable-features=UseHardwareVideoDecoder",
]


def _configure_logging() -> None:
    """Jednotny format logu pro celou aplikaci.

    Uroven lze zmenit promennou prostredi, napr. SWEB_LOG_LEVEL=DEBUG
    (pak se vypisuje i kazdy pozadavek zablokovany adblockem).
    """
    level = os.environ.get("SWEB_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def _prepare_qt_environment() -> None:
    """Nastavi promenne prostredi a argumenty pro QtWebEngine.

    Musi probehnout pred vytvorenim QApplication - Chromium si je cte
    pri svem startu.
    """
    # Na host pc zadat  xhost +local:
    # Aplikujeme záchranná opatření pouze pokud běžíme ve vývojovém kontejneru
    if os.environ.get("REMOTE_CONTAINERS"):
        os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    sys.argv.extend(CHROMIUM_FLAGS)


def main() -> None:
    _configure_logging()
    _prepare_qt_environment()

    app = QApplication(sys.argv)

    # podle techto nazvu urcuje QStandardPaths slozky pro config a data
    # (napr. ~/.config/vut/sweb) - nemenit, jinak se "ztrati" nastaveni
    app.setApplicationName("sweb")
    app.setOrganizationName("vut")

    window = MainWindow()
    window.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

