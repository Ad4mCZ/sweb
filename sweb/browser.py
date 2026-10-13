import re
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings

class SimpleBrowserView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.temp_view = None

        profile = QWebEngineProfile.defaultProfile()
        default_ua = profile.httpUserAgent()
        clean_ua = re.sub(r"QtWebEngine/[\d\.]+\s?", "", default_ua)
        profile.setHttpUserAgent(clean_ua)

        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True
        )
        self.page().renderProcessTerminated.connect(
            lambda status, code: print(f"Core ended! Status: {status}")
        )

    def createWindow(self, windowType):
        self.temp_view = QWebEngineView()
        self.temp_view.urlChanged.connect(self.setUrl)
        return self.temp_view
