import sys
import os


# Aplikujeme záchranná opatření pouze pokud běžíme ve vývojovém kontejneru
if os.environ.get("REMOTE_CONTAINERS"):
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    sys.argv.extend([
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-webgl"
    ])

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Vlastní třída pro jádro prohlížeče
class SimpleBrowserView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.temp_view = None

    # Odchycení požadavku na nové okno/záložku (target="_blank")
    def createWindow(self, windowType):
        self.temp_view = QWebEngineView()
        self.temp_view.urlChanged.connect(self.setUrl)
        # Vrácením 'self' donutíme odkaz otevřít se ve stávajícím zobrazení
        return self.temp_view

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Sweb - Prohlížeč pro seniory")
    window.resize(1024, 768)

    
    

    # Použití naší nové upravené třídy
    browser = SimpleBrowserView()
    browser.setUrl(QUrl("https://www.seznam.cz"))
    
    window.setCentralWidget(browser)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()