import logging
import re

from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView

log = logging.getLogger(__name__)


class SimpleBrowserView(QWebEngineView):
    def __init__(self) -> None:
        super().__init__()
        # docasny pohled pro odkazy typu target="_blank", viz createWindow()
        self.temp_view: QWebEngineView | None = None

        # odstraneni "QtWebEngine/x.y" z User-Agentu - nektere weby
        # neznamy prohlizec odmitaji nebo mu servirujou horsi verzi stranky
        profile = QWebEngineProfile.defaultProfile()
        if profile is not None:
            default_ua = profile.httpUserAgent()
            clean_ua = re.sub(r"QtWebEngine/[\d\.]+\s?", "", default_ua)
            profile.setHttpUserAgent(clean_ua)

        settings = self.settings()
        if settings is not None:
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
            settings.setAttribute(
                QWebEngineSettings.WebAttribute.JavascriptEnabled, True
            )
            settings.setAttribute(
                QWebEngineSettings.WebAttribute.LocalStorageEnabled, True
            )
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
            settings.setAttribute(
                QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
            )
            settings.setAttribute(
                QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True
            )

        self.renderProcessTerminated.connect(self._on_render_process_terminated)

    def _on_render_process_terminated(self, status, exit_code: int) -> None:
        # proces vykreslujici stranku spadl (nedostatek pameti, chyba GPU...)
        log.warning(
            "Render process ended! Status: %s, exit code: %s", status, exit_code
        )

    def createWindow(
        self, type: QWebEnginePage.WebWindowType
    ) -> QWebEngineView | None:
        # Prohlizec ma jen jedno okno. Kdyz stranka chce otevrit nove okno/zalozku,
        # dame ji docasny neviditelny pohled a jakmile se v nem objevi URL,
        # nacteme ji v hlavnim okne.
        self.temp_view = QWebEngineView()
        self.temp_view.urlChanged.connect(self.setUrl)
        return self.temp_view
