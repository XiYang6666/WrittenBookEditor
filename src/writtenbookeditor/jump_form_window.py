from typing import Optional

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt

from .gui.ui_jump_form import Ui_Form


class JumpFormWindow(QDialog, Ui_Form):
    def __init__(self, parent=None, page_count=0, current_page=0):
        super(JumpFormWindow, self).__init__(parent)
        self.setupUi(self)

        self.page_count = page_count
        self.current_page = current_page

        self.pbtn_ok.clicked.connect(self.on_ok_clicked)
        self.pbtn_cancel.clicked.connect(self.close)

        self.sb_volume.valueChanged.connect(self.on_volume_changed)
        self.sb_volume.setMaximum(self.page_count // 100 + 1)

        self.update_sb_page_max()

        self.sb_volume.setValue(self.current_page // 100 + 1)
        self.sb_page.setValue(self.current_page % 100 + 1)

        self.result_value: Optional[int] = None

    def on_ok_clicked(self):
        self.result_value = (self.sb_volume.value() - 1) * 100 + self.sb_page.value() - 1
        self.close()

    def on_volume_changed(self, value):
        self.update_sb_page_max()

    def update_sb_page_max(self):
        value = self.sb_volume.value()
        max_page = max(min(self.page_count - (value - 1) * 100, 100), 1)
        self.sb_page.setMaximum(max_page)
