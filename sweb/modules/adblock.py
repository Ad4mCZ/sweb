import json
import os
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineProfile
from sweb.module_base import SwebModule


class AdBlockInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self):
        super().__init__()
        self.blocked_domains = self._load_blocked_domains()

    def _load_blocked_domains(self):
        config_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppConfigLocation
        )
        adblock_file = os.path.join(config_dir, "adblock.json")
        default_domains = [
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

        if not os.path.exists(adblock_file):
            os.makedirs(config_dir, exist_ok=True)
            try:
                with open(adblock_file, "w", encoding="utf-8") as f:
                    json.dump({"blocked_domains": default_domains}, f, indent=4)
            except Exception:
                pass
            return default_domains

        try:
            with open(adblock_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("blocked_domains", default_domains)
        except Exception:
            return default_domains

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        for domain in self.blocked_domains:
            if domain in url:
                print(f"AdBlock is working: blocked {domain}")
                info.block(True)
                return


class AdBlockModule(SwebModule):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.interceptor = AdBlockInterceptor()

    def setup_browser(self, browser):
        profile = QWebEngineProfile.defaultProfile()
        profile.setUrlRequestInterceptor(self.interceptor)
