import json

from PySide6.QtWidgets import QDialog

from .ui_about_form import Ui_AboutForm


class AboutDialog(QDialog, Ui_AboutForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        try:
            with open("./data/metadata.json") as f:
                metadata = json.load(f)
            self.label_title.setText(f"WrittenBookEditor v{metadata['version']}")
        except Exception:
            self.label_title.setText("WrittenBookEditor")
