import os
from PyQt6.QtCore import QStandardPaths
from .json_store import JsonStore


class Settings(JsonStore):
    def __init__(self) -> None:
        # cesta ke slozce pro konfiguraci (na Linuxu ~/.config/vut/sweb, na Macu ~/Library/Preferences/vut/sweb)
        config_location = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppConfigLocation
        )

        super().__init__(
            file_path=os.path.join(config_location, "config.json"),
            defaults={
                "ui_font_size": 24,
                "web_zoom_factor": 1.5,
                "color_theme": "default",
                "home_url": "https://www.seznam.cz",
                "search_url": "https://search.seznam.cz/?q={}",
                # pozice tlacitka "Hledat" v Menu 2: "before" (pred zalozkami) nebo "after" (za zalozkami)
                "search_button_position": "after",
            },
            file_label="konfiguračního souboru",
        )
