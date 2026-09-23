import os
from PyQt5.QtWidgets import (
    QToolBar,
    QSizePolicy,
    QHBoxLayout,
    QToolButton,
    QMainWindow,
    QWidget,
)
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtGui import QIcon
from .browser import SimpleBrowserView
from .settings import Settings
from .module_manager import ModuleManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = Settings()
        self.module_manager = ModuleManager(self)
        self.module_manager.load_all_modules()

        self.setWindowTitle("Sweb - Prohlížeč pro seniory")
        self.resize(1280, 720)

        self.browser = SimpleBrowserView()
        self.browser.setUrl(QUrl("https://www.seznam.cz"))

        self.browser.setZoomFactor(self.settings.get("web_zoom_factor"))

        self.setCentralWidget(self.browser)

        self._setup_navigation_bar()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.seznam.cz"))

    def show_first_menu(self):
        self.bookmarks_toolbar.hide()
        self.main_toolbar.show()

    def show_second_menu(self):
        self.main_toolbar.hide()
        self.bookmarks_toolbar.show()

    def _setup_navigation_bar(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        font_size = self.settings.get("ui_font_size")
        theme = self.settings.get("color_theme")

        if theme == "high_contrast":
            bg_color = "#000000"
            btn_bg = "#000000"
            btn_text = "#ffff00"
            btn_border = "#ffff00"
            hover_bg = "#ffff00"
            hover_text = "#000000"
            hover_border = "#ffffff"
            pressed_bg = "#ffffff"
            pressed_text = "#000000"
            pressed_border = "#000000"
        else:
            bg_color = "#f5f5f5"
            btn_bg = "#e0e0e0"
            btn_text = "#000000"
            btn_border = "#b0b0b0"
            hover_bg = "#fff9c4"
            hover_text = "#000000"
            hover_border = "#fbc02d"
            pressed_bg = "#81d4fa"
            pressed_text = "#000000"
            pressed_border = "#0288d1"

        nav_style = f"""
            QToolBar {{
                spacing: 0px; 
                padding: 0px;
                background-color: {bg_color}; 
            }}
            QToolButton {{
                padding: 10px; 
                background-color: {bg_color};
                border: 1px solid {btn_border};
                border-radius: 0px;
                color: {btn_text};

                font-size: {font_size}px;
                font-weight: bold;
                font-family: Arial, sans-serif;
            }}
            QToolButton:hover {{
                background-color: {hover_bg}; 
                border: 2px solid {hover_border};
            }}
            QToolButton:pressed {{
                background-color: {pressed_bg};
                border: 2px solid {pressed_border};
            }}
        """

        # MENU 1

        self.main_toolbar = QToolBar("Navigace")
        self.main_toolbar.setMovable(False)
        self.main_toolbar.setStyleSheet(nav_style)
        self.main_toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        self.addToolBar(self.main_toolbar)

        ##<a href="https://www.flaticon.com/free-icons/next" title="next icons">Next icons created by Roundicons - Flaticon</a>

        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        class SeniorButton(QToolButton):
            def enterEvent(self, event):
                self.setStyleSheet(f"color: {hover_text};")
                super().enterEvent(event)

            def leaveEvent(self, event):
                self.setStyleSheet("")
                super().leaveEvent(event)

            def mousePressEvent(self, event):
                self.setStyleSheet(f"color: {pressed_text};")
                super().mousePressEvent(event)

            def mouseReleaseEvent(self, event):
                if self.underMouse():
                    self.setStyleSheet(f"color: {hover_text};")
                else:
                    self.setStyleSheet("")
                super().mouseReleaseEvent(event)

        def add_button(layout, icon, text, action):
            btn = SeniorButton()
            btn.setText(text)
            btn.setIcon(QIcon(os.path.join(base_dir, "icons", icon)))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setIconSize(QSize(80, 80))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            btn.clicked.connect(action)
            layout.addWidget(btn)

        add_button(main_layout, "menu.png", "Menu 2", self.show_second_menu)
        add_button(main_layout, "previous.png", "Zpět", self.browser.back)
        add_button(main_layout, "next.png", "Vpřed", self.browser.forward)
        add_button(main_layout, "home.png", "Domů", self.navigate_home)
        add_button(main_layout, "cancel.png", "Ukončit", self.close)

        self.main_toolbar.addWidget(main_container)

        # MENU 2

        self.bookmarks_toolbar = QToolBar("Navigace")
        self.bookmarks_toolbar.setMovable(False)
        self.bookmarks_toolbar.setStyleSheet(nav_style)
        self.bookmarks_toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        self.addToolBar(self.bookmarks_toolbar)

        bookmarks_container = QWidget()
        bookmarks_layout = QHBoxLayout(bookmarks_container)
        bookmarks_layout.setContentsMargins(0, 0, 0, 0)
        bookmarks_layout.setSpacing(0)

        add_button(bookmarks_layout, "menu.png", "Menu 1", self.show_first_menu)
        add_button(
            bookmarks_layout,
            "seznam.png",
            "Seznam.cz",
            lambda: self.browser.setUrl(QUrl("https://www.seznam.cz")),
        )

        self.bookmarks_toolbar.addWidget(bookmarks_container)

        self.bookmarks_toolbar.hide()
