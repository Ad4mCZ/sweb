import os
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QSizePolicy, QWidget
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtGui import QIcon
from .browser import SimpleBrowserView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sweb - Prohlížeč pro seniory")
        self.resize(1280, 720)

        self.browser = SimpleBrowserView()
        self.browser.setUrl(QUrl("https://www.seznam.cz"))
        self.setCentralWidget(self.browser)

        self._setup_navigation_bar()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.seznam.cz"))

    def show_first_menu(self):
        self.nav_menu2.hide()
        self.nav_menu1.show()

    def show_second_menu(self):
        self.nav_menu1.hide()
        self.nav_menu2.show()

    def _setup_navigation_bar(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        nav_style = """
            QToolBar {
                spacing: 15px; 
                padding: 10px; 
            }
            QToolButton {
                padding: 10px; 
                background-color: #e0e0e0;
                border: 1px solid #b0b0b0;
                border-radius: 8px; 
            }
            QToolButton:hover {
                background-color: #d0d0d0; 
            }
            QToolButton:pressed {
                background-color: #a0a0a0;
            }
        """

        # MENU 1

        self.nav_menu1 = QToolBar("Navigace")
        self.nav_menu1.setMovable(False)
        self.nav_menu1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nav_menu1.setIconSize(QSize(48, 48))
        self.nav_menu1.setStyleSheet(nav_style)
        self.nav_menu1.setContextMenuPolicy(Qt.PreventContextMenu)

        font = self.nav_menu1.font()
        font.setPointSize(16)
        font.setBold(True)
        self.nav_menu1.setFont(font)

        self.addToolBar(self.nav_menu1)

        ##<a href="https://www.flaticon.com/free-icons/next" title="next icons">Next icons created by Roundicons - Flaticon</a>

        # Tlacitko Menu2
        menu2_btn = QAction(QIcon(os.path.join(base_dir, "icons", "menu.png")), "Menu 2", self)
        menu2_btn.triggered.connect(self.show_second_menu)
        self.nav_menu1.addAction(menu2_btn)

        # Tlacitko zpet
        back_btn = QAction(QIcon(os.path.join(base_dir, "icons", "previous.png")), "Zpět", self)
        back_btn.triggered.connect(self.browser.back)
        self.nav_menu1.addAction(back_btn)

        # Tlacitko vpred
        forward_btn = QAction(QIcon(os.path.join(base_dir,"icons", "next.png")), "Vpřed", self)
        forward_btn.triggered.connect(self.browser.forward)
        self.nav_menu1.addAction(forward_btn)

        # Tlacitko domu
        home_btn = QAction(QIcon(os.path.join(base_dir,"icons", "home.png")), "Domů", self)
        home_btn.triggered.connect(self.navigate_home)
        self.nav_menu1.addAction(home_btn)

        # Oddeleni, aby tlacitko pro vypnuti bylo vpravo
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.nav_menu1.addWidget(spacer)

        # Tlacitko na vypnuti
        close_btn = QAction(QIcon(os.path.join(base_dir,"icons", "cancel")), "Ukončit", self)
        close_btn.triggered.connect(self.close)
        self.nav_menu1.addAction(close_btn)

        # MENU 2

        self.nav_menu2 = QToolBar("Navigace")
        self.nav_menu2.setMovable(False)
        self.nav_menu2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nav_menu2.setIconSize(QSize(48, 48))
        self.nav_menu2.setStyleSheet(nav_style)
        self.nav_menu2.setFont(font)
        self.nav_menu2.setContextMenuPolicy(Qt.PreventContextMenu)

        self.addToolBar(self.nav_menu2)

        # Tlacitko Menu2
        menu1_btn = QAction(QIcon(os.path.join(base_dir,"icons", "menu.png")), "Menu 1", self)
        menu1_btn.triggered.connect(self.show_first_menu)
        self.nav_menu2.addAction(menu1_btn)

        # Tlacitko bookmark1
        bookmark1_btn = QAction(QIcon(os.path.join(base_dir,"icons", "seznam .png")), "Seznam", self)
        bookmark1_btn.triggered.connect(
            lambda: self.browser.setUrl(QUrl("https://www.seznam.cz"))
        )
        self.nav_menu2.addAction(bookmark1_btn)

        self.nav_menu2.hide()
