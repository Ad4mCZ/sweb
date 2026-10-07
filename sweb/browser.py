from PyQt6.QtWebEngineWidgets import QWebEngineView


class SimpleBrowserView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.temp_view = None

    def createWindow(self, windowType):
        self.temp_view = QWebEngineView()
        self.temp_view.urlChanged.connect(self.setUrl)
        return self.temp_view
