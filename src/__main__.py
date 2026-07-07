import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Sweb - Základní verze")
    window.resize(1024, 768)

    # Vytvoření webového jádra a načtení stránky
    browser = QWebEngineView()
    browser.setUrl(QUrl("https://www.seznam.cz"))
    
    window.setCentralWidget(browser)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()