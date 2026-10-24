from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # jen pro typove napovedy - skutecny import by zpusobil cyklus window <-> moduly
    from PyQt6.QtGui import QAction
    from .browser import SimpleBrowserView
    from .window import MainWindow


class SwebModule:
    """Zakladni trida pro rozsireni (pluginy) ve slozce sweb/modules/.

    ModuleManager automaticky najde a vytvori kazdou podtridu teto tridy.
    Podtrida prepise jen ty metody, ktere potrebuje.
    """

    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window

    def get_toolbar_actions(self) -> list[QAction]:
        """Akce, ktere modul chce pridat do navigace."""
        return []

    def setup_browser(self, browser: SimpleBrowserView) -> None:
        """Zavola se jednou po vytvoreni prohlizece - napr. pro nastaveni filtru."""
        pass
