import sys
import os
from PyQt6.QtWidgets import QApplication

# Na host pc zadat  xhost +local:

# Aplikujeme záchranná opatření pouze pokud běžíme ve vývojovém kontejneru
# if os.environ.get("REMOTE_CONTAINERS"):
# os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
# sys.argv.extend([
#     "--disable-gpu",
#     "--disable-software-rasterizer",
#     "--disable-webgl"
# ])

# Vypnutí sandboxu musí zůstat pro běh v kontejneru
if os.environ.get("REMOTE_CONTAINERS"):
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

from .window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("sweb")
    app.setOrganizationName("vut")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
