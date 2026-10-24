from __future__ import annotations

import logging
import os
from typing import Callable
from urllib.parse import urlparse

from PyQt6.QtCore import QStandardPaths, QUrl
from PyQt6.QtGui import QImage
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from .json_store import JsonStore

log = logging.getLogger(__name__)


class Bookmarks(JsonStore):
    def __init__(self) -> None:
        # cesta pro uzivatelska data (na Linuxu ~/.local/share/vut/sweb, na Macu ~/Library/Application Support/vut/sweb)
        data_location = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )

        self.icons_dir = os.path.join(data_location, "downloaded_icons")
        os.makedirs(self.icons_dir, exist_ok=True)

        # asynchronni stahovani ikonek na pozadi, aby nezamrzalo okno pri startu
        self._net_manager = QNetworkAccessManager()

        super().__init__(
            file_path=os.path.join(data_location, "bookmarks.json"),
            # zakladni zalozky po prvnim spusteni
            defaults={
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
            },
            file_label="souboru se záložkami",
        )

    def get_first_menu(self) -> list[dict[str, str]]:
        return self.data.get("first_menu", [])

    def get_second_menu(self) -> list[dict[str, str]]:
        return self.data.get("second_menu", [])

    def get_icon_for_url(
        self,
        url: str,
        fallback_icon: str = "star.png",
        on_downloaded: Callable[[str], None] | None = None,
    ) -> str:
        """Vrati cestu k ikone pro danou URL.

        Pokud ikona jeste neni stazena na disku, ihned vrati fallback_icon 
        a spusti stahovani na pozadi pres QNetworkAccessManager.
        Po dostazeni ulozi soubor a pripadne zavola callback on_downloaded(icon_path).
        """
        domain = urlparse(url).netloc
        if not domain:
            return fallback_icon

        icon_filename = f"{domain}.png"
        icon_path = os.path.join(self.icons_dir, icon_filename)

        if os.path.exists(icon_path):
            return icon_path

        api_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
        request = QNetworkRequest(QUrl(api_url))
        reply = self._net_manager.get(request)
        if reply is not None:
            reply.finished.connect(
                lambda r=reply, p=icon_path, cb=on_downloaded, u=url: self._on_icon_reply(
                    r, p, cb, u
                )
            )
        return fallback_icon

    def _on_icon_reply(
        self,
        reply: QNetworkReply,
        icon_path: str,
        on_downloaded: Callable[[str], None] | None,
        url: str,
    ) -> None:
        """Ulozi stazenou ikonu na disk a upozorni tlacitko, aby si ji prekreslilo."""
        try:
            if reply.error() == QNetworkReply.NetworkError.NoError:
                raw_bytes = reply.readAll().data()
                # overime, ze stazena data jsou opravdu platny obrazek
                # (ne napr. HTML chybova stranka pri vypadku site)
                if raw_bytes and not QImage.fromData(raw_bytes).isNull():
                    with open(icon_path, "wb") as f:
                        f.write(raw_bytes)
                    if on_downloaded is not None:
                        on_downloaded(icon_path)
            else:
                log.warning(
                    "Error while retrieving icon for %s: %s", url, reply.errorString()
                )
        except Exception as e:
            log.warning("Error while saving icon for %s: %s", url, e)
        finally:
            reply.deleteLater()
