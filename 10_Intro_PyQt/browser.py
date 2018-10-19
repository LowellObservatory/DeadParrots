from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon
import PyQt5
import sys

class Web(QWebEngineView):

    def load(self, url):
        self.setUrl(QUrl(url))

    def adjustTitle(self):
        self.setWindowTitle(self.title())

    def disableJS(self):
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)

class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Name')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 1400, 1000)

        web = Web()
        web.load("http://lowell.edu")

        lay = QVBoxLayout(self)
        lay.addWidget(web)

app = QApplication(sys.argv)
main = Main()
main.show()
app.exec_()
