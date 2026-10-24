from __future__ import annotations

import os
from typing import Callable, Sequence
from urllib.parse import quote_plus

from PyQt6.QtCore import QEvent, QSize, Qt, QUrl
from PyQt6.QtGui import QEnterEvent, QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from .bookmarks import Bookmarks
from .browser import SimpleBrowserView
from .module_manager import ModuleManager
from .settings import Settings
from .theme import get_theme, nav_stylesheet, search_dialog_stylesheet

# typ pro definici tlacitka v navigaci: (nazev_ikony, popisek, akce_po_kliknuti)
ButtonSpec = tuple[str, str, Callable[[], object]]


class SearchDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Vyhledávání")
        self.setModal(True)
        self.setMinimumWidth(500)  # sirka okna

        # stylovani okna, obri písmo a velka tlacitka (definice v theme.py)
        self.setStyleSheet(search_dialog_stylesheet())

        layout = QVBoxLayout(self)

        # hlavni text
        label = QLabel("Co chcete na internetu najít?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # textove pole
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        # tlacitka
        btn_layout = QHBoxLayout()

        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)  # Zavře okno s výsledkem "Zrušeno"

        search_btn = QPushButton("Hledat")
        search_btn.setObjectName("searchBtn")  # aplikace stylu styl
        search_btn.clicked.connect(self.accept)  # Zavře okno s výsledkem "Potvrzeno"

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(search_btn)

        layout.addLayout(btn_layout)

    def get_text(self) -> str:
        return self.input_field.text().strip()


class SeniorButton(QToolButton):
    """Velke tlacitko do navigace, ktere meni barvu textu pri najeti a stisku.

    Barvu pozadi a ramecku resi stylesheet toolbaru (:hover, :pressed),
    ale barva textu se tam u QToolButton spolehlive nemeni. Proto ji
    prepiname rucne v obsluze udalosti mysi.
    """

    def __init__(
        self, hover_text: str, pressed_text: str, parent: QWidget | None = None
    ) -> None:
        """
        :param hover_text: barva textu pri najeti mysi
        :param pressed_text: barva textu pri stisknuti tlacitka
        """
        super().__init__(parent)
        self._hover_text = hover_text
        self._pressed_text = pressed_text

    def enterEvent(self, a0: QEnterEvent | None) -> None:
        self.setStyleSheet(f"color: {self._hover_text};")
        super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent | None) -> None:
        # prazdny styl = vratit se k vychozimu stylu z toolbaru
        self.setStyleSheet("")
        super().leaveEvent(a0)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        self.setStyleSheet(f"color: {self._pressed_text};")
        super().mousePressEvent(a0)

    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        # pokud uzivatel pusti tlacitko mimo nej, hover uz neplati
        if self.underMouse():
            self.setStyleSheet(f"color: {self._hover_text};")
        else:
            self.setStyleSheet("")
        super().mouseReleaseEvent(a0)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.settings = Settings()
        self.bookmarks = Bookmarks()
        self.module_manager = ModuleManager(self)
        self.module_manager.load_all_modules()

        self.setWindowTitle("Sweb - Prohlížeč pro seniory")
        self.resize(1280, 720)

        self.browser = SimpleBrowserView()
        self.browser.setUrl(QUrl("https://www.seznam.cz"))

        self.module_manager.setup_all_browsers(self.browser)

        zoom = self.settings.get("web_zoom_factor")
        self.browser.setZoomFactor(zoom)
        # QtWebEngine pri prechodu na jinou domenu obcas resetuje zoom na 1.0,
        # proto ho pri zmene URL vzdy znovu nastavime
        self.browser.urlChanged.connect(
            lambda _url, z=zoom: self.browser.setZoomFactor(z)
        )

        self.setCentralWidget(self.browser)

        self._setup_navigation_bar()

    def navigate_home(self) -> None:
        self.browser.setUrl(QUrl("https://www.seznam.cz"))

    def get_icon_path(self, icon_name: str) -> str:
        if os.path.isabs(icon_name):
            return icon_name

        system_path = os.path.join("/usr/share/icons/sweb", icon_name)
        local_path = os.path.join(os.path.dirname(__file__), "icons", icon_name)

        if os.path.exists(system_path):
            return system_path
        return local_path

    def open_search(self) -> None:
        dialog = SearchDialog(self)

        # Pokud uživatel klikne na "Hledat" a okno se úspěšně potvrdí
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = dialog.get_text()
            if text:
                base_url = self.settings.get("search_url")
                # quote_plus escapuje znaky jako &, #, % nebo mezery do platneho dotazu v URL
                search_url = base_url.format(quote_plus(text))
                self.browser.setUrl(QUrl(search_url))

    def show_first_menu(self) -> None:
        self.bookmarks_toolbar.hide()
        self.main_toolbar.show()

    def show_second_menu(self) -> None:
        self.main_toolbar.hide()
        self.bookmarks_toolbar.show()

    def _setup_navigation_bar(self) -> None:
        # barvy a styl se berou z theme.py podle nastaveni "color_theme"
        theme = get_theme(self.settings.get("color_theme"))
        font_size = self.settings.get("ui_font_size")

        # styl a barvy textu si ulozime, aby je mohly pouzit
        # _create_toolbar() a _add_button() pri stavbe obou menu
        self._nav_style = nav_stylesheet(theme, font_size)
        self._hover_text = theme["hover_text"]
        self._pressed_text = theme["pressed_text"]

        ##<a href="https://www.flaticon.com/free-icons/next" title="next icons">Next icons created by Roundicons - Flaticon</a>

        # MENU 1 - ovladani prohlizece + prvni sada zalozek
        # (prepinac menu a "Ukoncit" jsou pred zalozkami)
        self.main_toolbar = self._create_toolbar(
            name="Navigace",
            bookmarks=self.bookmarks.get_first_menu(),
            buttons_before=[
                ("menu.png", "Menu 2", self.show_second_menu),
                # ("previous.png", "Zpět", self.browser.back),
                # ("next.png", "Vpřed", self.browser.forward),
                # ("home.png", "Domů", self.navigate_home),
                ("cancel.png", "Ukončit", self.close),
            ],
        )

        # MENU 2 - druha sada zalozek + vyhledavani
        # (prepinac menu je vlevo, "Hledat" az za zalozkami vpravo)
        self.bookmarks_toolbar = self._create_toolbar(
            name="Navigace",
            bookmarks=self.bookmarks.get_second_menu(),
            buttons_before=[("menu.png", "Menu 1", self.show_first_menu)],
            buttons_after=[("search.png", "Hledat", self.open_search)],
        )

        # po spusteni je videt jen MENU 1, MENU 2 se zobrazi tlacitkem "Menu 2"
        self.bookmarks_toolbar.hide()

    def _create_toolbar(
        self,
        name: str,
        bookmarks: Sequence[dict[str, str]],
        buttons_before: Sequence[ButtonSpec] = (),
        buttons_after: Sequence[ButtonSpec] = (),
    ) -> QToolBar:
        """Vytvori jednu radu velkych tlacitek (toolbar) a prida ji do okna.

        Obe menu se skladaji stejne: pevna tlacitka vlevo, pak zalozky,
        pak pripadna pevna tlacitka vpravo. Diky tomu je postup na jednom miste.

        :param name: nazev toolbaru
        :param bookmarks: seznam zalozek ve tvaru [{"name": ..., "url": ...}, ...]
        :param buttons_before: tlacitka pred zalozkami jako (ikona, text, akce)
        :param buttons_after: tlacitka za zalozkami jako (ikona, text, akce)
        :return: hotovy QToolBar, aby ho slo pozdeji skryt/zobrazit
        """
        toolbar = QToolBar(name)
        # toolbar nejde pretahnout mysi ani skryt pravym klikem,
        # aby si ho senior omylem "neztratil"
        toolbar.setMovable(False)
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        toolbar.setStyleSheet(self._nav_style)
        self.addToolBar(toolbar)

        # tlacitka davame do vlastniho layoutu (ne primo do toolbaru),
        # protoze jen tak se mohou roztahnout pres celou sirku okna
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for icon, text, action in buttons_before:
            self._add_button(layout, icon, text, action)

        for bm in bookmarks:
            # nejdriv vytvorime tlacitko s aktualne dostupnou ikonou (nebo hvezdickou)
            # a pokud se ikona teprve stahuje na pozadi, po dotazeni ji na tlacitku vymenime
            btn = self._add_button(
                layout,
                "star.png",
                bm["name"],
                lambda _=False, u=bm["url"]: self.browser.setUrl(QUrl(u)),
            )
            icon_path = self.bookmarks.get_icon_for_url(
                bm["url"],
                on_downloaded=lambda path, b=btn: b.setIcon(
                    QIcon(self.get_icon_path(path))
                ),
            )
            btn.setIcon(QIcon(self.get_icon_path(icon_path)))

        for icon, text, action in buttons_after:
            self._add_button(layout, icon, text, action)

        toolbar.addWidget(container)
        return toolbar

    def _add_button(
        self,
        layout: QHBoxLayout,
        icon_filename: str,
        text: str,
        action: Callable[[], object],
    ) -> SeniorButton:
        """Vytvori jedno velke tlacitko s ikonou, vlozi ho do layoutu a vrati ho.

        :param icon_filename: nazev ikony ze slozky icons/ nebo absolutni cesta
        :param action: funkce, ktera se zavola po kliknuti
        """
        btn = SeniorButton(self._hover_text, self._pressed_text)
        btn.setText(text)
        btn.setIcon(QIcon(self.get_icon_path(icon_filename)))
        # tohle pak zakomentovat, aby tam nebyli popisky, jen ikonka
        # btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn.setIconSize(QSize(80, 80))
        # tlacitka se rovnomerne roztahnou a vyplni celou sirku toolbaru
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        btn.clicked.connect(action)
        layout.addWidget(btn)
        return btn
