import json

from PySide6.QtWidgets import QDialog

from .ui_about_form import Ui_AboutForm
from ..i18n import translate as tr, get_lang


class AboutDialog(QDialog, Ui_AboutForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        try:
            with open("./data/metadata.json") as f:
                metadata = json.load(f)
            self.lb_title.setText(f"WrittenBookEditor v{metadata['version']}")
        except Exception:
            self.lb_title.setText("WrittenBookEditor")

        try:
            with open(f"./data/lang/about_{get_lang()}.html", encoding="utf-8") as f:
                self.lb_about.setText(f.read())
        except Exception:
            pass

        self.setWindowTitle(tr("about_dialog.title"))
        self.tabWidget.setTabText(0, tr("about_dialog.about"))
        self.tabWidget.setTabText(1, tr("about_dialog.author"))
        self.gb_author.setTitle(tr("about_dialog.author"))
        self.lb_mainpage.setText(tr("about_dialog.mainpage"))
        self.lb_github.setText(tr("about_dialog.github"))
        self.lb_bilibili.setText(tr("about_dialog.bilibili"))
        self.lb_email.setText(tr("about_dialog.email"))

        # self.adjustSize()
