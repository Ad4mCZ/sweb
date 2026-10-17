import os
import json
from PyQt6.QtCore import QStandardPaths
import urllib.request
from urllib.parse import urlparse
from PyQt6.QtWidgets import QMessageBox
from .utils import show_critical_error


class Bookmarks:
    def __init__(self):
        # cesta pro uzivatelska data (na Linuxu ~/.local/share/vut/sweb, na Macu ~/Library/Application Support/vut/sweb)
        data_location = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        if not os.path.exists(data_location):
            os.makedirs(data_location)

        self.icons_dir = os.path.join(data_location, "downloaded_icons")
        if not os.path.exists(self.icons_dir):
            os.makedirs(self.icons_dir)

        self.bookmarks_path = os.path.join(data_location, "bookmarks.json")
        print(f"Bookmarks location: {self.bookmarks_path}")

        # zakladni zalozky po prvnim spusteni
        self.default_bookmarks = {
            "first_menu": [
                {"name": "Seznam", "url": "https://www.seznam.cz"},
                {"name": "ČT24", "url": "https://ct24.ceskatelevize.cz"},
                {"name": "Počasí", "url": "https://www.in-pocasi.cz"},
            ],
            "second_menu": [
                {"name": "Deník", "url": "https://www.denik.cz"},
                {"name": "Novinky", "url": "https://www.novinky.cz"},
                {"name": "Lékárna", "url": "https://www.lekarna.cz"},
            ],
        }

        self.data = self.load()

    def load(self):
        if not os.path.exists(self.bookmarks_path):
            self._save_all(self.default_bookmarks)
            return self.default_bookmarks.copy()

        try:
            with open(self.bookmarks_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            show_critical_error(
                title="Kritická chyba konfigurace",
                message="Chyba při čtení souboru se záložkami!\n\nAplikaci nelze bezpečně spustit a bude ukončena.",
                error_detail=str(e),
            )
            print(f"Error while reading the bookmarks file, error {e}")
            return self.default_bookmarks.copy()

    def _save_all(self, data_to_save):
        try:
            with open(self.bookmarks_path, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            show_critical_error(
                title="Kritická chyba konfigurace",
                message="Chyba při ukládání souboru se záložkami!\n\nAplikaci nelze bezpečně spustit a bude ukončena.",
                error_detail=str(e),
            )
            print(f"Error while saving bookmarks, error {e}")

    def get_first_menu(self):
        return self.data.get("first_menu", [])

    def get_second_menu(self):
        return self.data.get("second_menu", [])

    def get_icon_for_url(self, url, fallback_icon="star.png"):
        try:
            domain = urlparse(url).netloc
            icon_filename = f"{domain}.png"
            icon_path = os.path.join(self.icons_dir, icon_filename)

            if not os.path.exists(icon_path):
                api_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
                urllib.request.urlretrieve(api_url, icon_path)
            return icon_path
        except Exception as e:
            print(f"Error while retrieving icon for {url}, error {e}")
            return fallback_icon
