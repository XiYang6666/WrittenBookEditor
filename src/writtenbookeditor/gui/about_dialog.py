from typing import Optional

from PySide6.QtWidgets import QDialog
from PySide6.QtGui import Qt, QCloseEvent

from .ui_about_form import Ui_AboutForm


class AboutDialog(QDialog, Ui_AboutForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)