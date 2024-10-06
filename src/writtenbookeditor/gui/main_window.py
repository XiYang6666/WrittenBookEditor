from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from .ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./data/icon/icon.png"))
