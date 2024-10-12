from PySide6.QtWidgets import QDialog

from .ui_encoding_form import Ui_EncodingForm
from ..i18n import translate as tr


class EncodingDialog(QDialog, Ui_EncodingForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.result_value = None
        self.pbtn_ok.clicked.connect(self.accept)
        self.pbtn_cancel.clicked.connect(self.reject)

        self.setWindowTitle(tr("encoding_dialog.title"))
        self.lb_message.setText(tr("encoding_dialog.message"))
        self.lb_encoding.setText(tr("encoding_dialog.encoding"))
        self.cmb_encoding.setItemText(0, tr("encoding.auto_detect"))
        self.pbtn_ok.setText(tr("general.ok"))
        self.pbtn_cancel.setText(tr("general.cancel"))

        self.adjustSize()

    def get_result(self) -> str:
        return self.cmb_encoding.currentText()
