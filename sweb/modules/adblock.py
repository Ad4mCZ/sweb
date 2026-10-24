from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from PyQt6.QtCore import QStandardPaths
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)

from sweb.json_store import JsonStore
from sweb.module_base import SwebModule

if TYPE_CHECKING:
    from sweb.browser import SimpleBrowserView
    from sweb.window import MainWindow

log = logging.getLogger(__name__)

DEFAULT_BLOCKED_DOMAINS = [
    "doubleclick.net",
    "googlesyndication.com",
    "google-analytics.com",
    "googletagmanager.com",
    "clarity.ms",
    "facebook.com/tr",
    "imrworldwide.com",
    "chartbeat.net",
    "imedia.cz",
    "criteo.com",
    "adform.net",
]


class AdBlockInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self) -> None:
        super().__init__()
        config_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppConfigLocation
        )
        # chyba v adblock.json neni kriticka - pouziji se vychozi domeny
        self.store = JsonStore(
            file_path=os.path.join(config_dir, "adblock.json"),
            defaults={"blocked_domains": DEFAULT_BLOCKED_DOMAINS},
            file_label="souboru adblocku",
            critical=False,
        )
        self.blocked_domains: list[str] = self.store.get("blocked_domains", [])

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        url = info.requestUrl().toString()
        for domain in self.blocked_domains:
            if domain in url:
                log.debug("AdBlock blocked %s", domain)
                info.block(True)
                return


class AdBlockModule(SwebModule):
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__(main_window)
        self.interceptor = AdBlockInterceptor()

    def setup_browser(self, browser: SimpleBrowserView) -> None:
        profile = QWebEngineProfile.defaultProfile()
        if profile is not None:
            profile.setUrlRequestInterceptor(self.interceptor)
