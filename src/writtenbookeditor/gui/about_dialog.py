from PySide6.QtWidgets import QDialog

from .ui_about_form import Ui_AboutForm


class AboutDialog(QDialog, Ui_AboutForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
