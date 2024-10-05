from typing import TypedDict

from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QCloseEvent

from .ui_export_form import Ui_ExportForm


class Result(TypedDict):
    author: str
    title: str
    item_type: str
    file_type: str
    command_version: str
    text_component: bool
    filter: bool


class ExportDialog(QDialog, Ui_ExportForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.result_value = None

    def closeEvent(self, event: QCloseEvent) -> None:
        self.reject()
        super().closeEvent(event)

    def get_result(self) -> Result:
        return {
            "author": self.le_author.text(),
            "title": self.le_title.text(),
            "item_type": self.cmb_item_type.currentText(),
            "file_type": self.cmb_file_type.currentText(),
            "command_version": self.cmb_command_version.currentText(),
            "text_component": self.chk_text_component.isChecked(),
            "filter": self.chk_filter.isChecked(),
        }
