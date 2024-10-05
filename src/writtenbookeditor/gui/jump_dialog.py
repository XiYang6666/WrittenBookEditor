from PySide6.QtWidgets import QDialog

from .ui_jump_form import Ui_JumpForm


class JumpDialog(QDialog, Ui_JumpForm):
    def __init__(self, parent=None, page_count=0, current_page=0):
        super().__init__(parent)
        self.setupUi(self)

        self.page_count = page_count
        self.current_page = current_page

        self.pbtn_ok.clicked.connect(self.accept)
        self.pbtn_cancel.clicked.connect(self.reject)

        self.sb_volume.valueChanged.connect(self.on_sb_volume_changed)
        self.sb_volume.setMaximum(self.page_count // 100 + 1)

        self.update_sb_page_max()

        self.sb_volume.setValue(self.current_page // 100 + 1)
        self.sb_page.setValue(self.current_page % 100 + 1)

    def get_result(self) -> int:
        return (self.sb_volume.value() - 1) * 100 + self.sb_page.value() - 1

    def on_sb_volume_changed(self, value):
        self.update_sb_page_max()

    def update_sb_page_max(self):
        value = self.sb_volume.value()
        max_page = max(min(self.page_count - (value - 1) * 100, 100), 1)
        self.sb_page.setMaximum(max_page)
