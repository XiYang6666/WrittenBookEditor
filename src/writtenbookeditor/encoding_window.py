from typing import Optional

from PySide6.QtWidgets import QDialog
from PySide6.QtGui import Qt, QCloseEvent

from .gui.ui_encoding_form import Ui_EncodingForm


class EncodingWindow(QDialog, Ui_EncodingForm):
    def __init__(self, parent=None):
        super(EncodingWindow, self).__init__(parent)
        self.setupUi(self)
        self.result_value = None
        self.pbtn_ok.clicked.connect(self.on_ok_clicked)
        self.pbtn_cancel.clicked.connect(self.on_cancel_clicked)

    def on_ok_clicked(self):
        self.result_value = self.cmb_encoding.currentText()
        self.close()

    def on_cancel_clicked(self):
        self.close()
