from PySide6.QtWidgets import QDialog

from .ui_encoding_form import Ui_EncodingForm


class EncodingDialog(QDialog, Ui_EncodingForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.result_value = None
        self.pbtn_ok.clicked.connect(self.accept)
        self.pbtn_cancel.clicked.connect(self.reject)

    def get_result(self) -> str:
        return self.cmb_encoding.currentText()
