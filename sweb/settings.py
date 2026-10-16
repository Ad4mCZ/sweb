import os
import json
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtWidgets import QMessageBox
from .utils import show_critical_error


class Settings:
    def __init__(self):

        # cesta ke slozce pro konfiguraci (na Linuxu ~/.config/vut/sweb, na Macu ~/Library/Preferences/vut/sweb)
        config_location = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppConfigLocation
        )
        if not os.path.exists(config_location):
            os.makedirs(config_location)

        self.config_path = os.path.join(config_location, "config.json")
        print(f"Config location: {self.config_path}")

        self.default_config = {
            "ui_font_size": 24,
            "web_zoom_factor": 1.5,
            "color_theme": "default",
        }

        self.data = self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            self._save_all(self.default_config)
            return self.default_config.copy()

        try:
            # raise Exception("Test chyby")
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                changed = False
                for key, value in self.default_config.items():
                    if key not in data:
                        data[key] = value
                        changed = True

                if changed:
                    self._save_all(data)

                return data
        except Exception as e:
            show_critical_error(
                title="Kritická chyba konfigurace",
                message="Chyba při čtení konfiguračního souboru!\n\nAplikaci nelze bezpečně spustit a bude ukončena.",
                error_detail=str(e),
            )
            print(f"Error while reading the config file, error: {e}")
            return self.default_config.copy()

    def _save_all(self, data_to_save):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            show_critical_error(
                title="Kritická chyba konfigurace",
                message="Chyba při ukládání konfiguračního souboru!\n\nAplikaci nelze bezpečně spustit a bude ukončena.",
                error_detail=str(e),
            )
            print(f"Error while saving the configuration: {e}")

    def get(self, key):
        return self.data.get(key, self.default_config.get(key))

    def set(self, key, value):
        self.data[key] = value
        self._save_all(self.data)
