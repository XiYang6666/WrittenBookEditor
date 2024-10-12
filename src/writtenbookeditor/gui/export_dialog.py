from typing import TypedDict

from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QCloseEvent

from .ui_export_form import Ui_ExportForm
from ..i18n import translate as tr


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

        self.setWindowTitle(tr("export_dialog.window_title"))
        self.gb_book_options.setTitle(tr("export_dialog.book_options"))
        self.gb_export_options.setTitle(tr("export_dialog.export_options"))
        self.gb_extra_options.setTitle(tr("export_dialog.extra_options"))
        self.lb_author.setText(tr("export_dialog.author"))
        self.lb_title.setText(tr("export_dialog.title"))
        self.lb_item_type.setText(tr("export_dialog.item_type"))
        self.lb_file_type.setText(tr("export_dialog.file_type"))
        self.lb_command_version.setText(tr("export_dialog.command_version"))
        self.cmb_item_type.setItemText(0, tr("item_type.written_book"))
        self.cmb_item_type.setItemText(1, tr("item_type.shulker_box"))
        self.cmb_file_type.setItemText(0, tr("file_type.command_text"))
        self.cmb_file_type.setItemText(1, tr("file_type.function_text"))
        self.cmb_file_type.setItemText(2, tr("file_type.data_pack"))
        self.cmb_command_version.setItemText(0, tr("command_version.upper_1_13"))
        self.cmb_command_version.setItemText(1, tr("command_version.upper_1_20_5"))
        self.chk_text_component.setText(tr("export_dialog.use_text_component"))
        self.chk_filter.setText(tr("export_dialog.use_filter"))
        self.pbtn_export.setText(tr("export_dialog.export"))

        self.adjustSize()

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
