from __future__ import annotations

import importlib.util
import logging
import os
from typing import TYPE_CHECKING

from .module_base import SwebModule

if TYPE_CHECKING:
    from PyQt6.QtGui import QAction
    from .browser import SimpleBrowserView
    from .window import MainWindow

log = logging.getLogger(__name__)


class ModuleManager:
    """Najde, nacte a spravuje rozsireni ze slozky sweb/modules/."""

    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window
        self.modules: list[SwebModule] = []

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.modules_dir = os.path.join(self.base_dir, "modules")

    def load_all_modules(self) -> None:
        """Nacte kazdy .py soubor ve slozce modules a vytvori v nem vsechny SwebModule."""
        os.makedirs(self.modules_dir, exist_ok=True)

        # sorted() = moduly se nacitaji vzdy ve stejnem poradi
        # (os.listdir poradi nezarucuje)
        for filename in sorted(os.listdir(self.modules_dir)):
            # preskocime __init__.py a ostatni ne-Python soubory
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                filepath = os.path.join(self.modules_dir, filename)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    if spec is None or spec.loader is None:
                        continue
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    # v modulu hledame tridy odvozene od SwebModule
                    # (samotnou SwebModule, kterou modul importuje, vynechame)
                    for attr in dir(mod):
                        obj = getattr(mod, attr)
                        if (
                            isinstance(obj, type)
                            and issubclass(obj, SwebModule)
                            and obj is not SwebModule
                        ):
                            instance = obj(self.main_window)
                            self.modules.append(instance)
                            log.info("Module loaded successfully: %s", obj.__name__)
                except Exception as e:
                    # chyba v jednom pluginu nesmi shodit cely prohlizec
                    log.error("Failed to load module '%s': %s", filename, e)

    def get_all_actions(self) -> list[QAction]:
        actions = []
        for module in self.modules:
            actions.extend(module.get_toolbar_actions())
        return actions

    def setup_all_browsers(self, browser: SimpleBrowserView) -> None:
        for module in self.modules:
            module.setup_browser(browser)
