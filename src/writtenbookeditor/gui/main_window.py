from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from .ui_mainwindow import Ui_MainWindow
from ..i18n import translate as tr


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./data/icon/icon.png"))
        self.adjustSize()

    def update_lang(self):
        self.menu_file.setTitle(tr("menu.file"))
        self.menu_settings.setTitle(tr("menu.settings"))
        self.menu_lang.setTitle(tr("menu.language"))
        self.menu_help.setTitle(tr("menu.help"))

        self.action_new.setText(tr("action.new"))
        self.action_open_file.setText(tr("action.open_file"))
        self.action_save.setText(tr("action.save"))
        self.action_save_as.setText(tr("action.save_as"))
        self.action_export.setText(tr("action.export"))
        self.action_force_unicode.setText(tr("action.force_unicode_font"))
        self.action_jp_font.setText(tr("action.jp_glyph_variant"))
        self.action_about.setText(tr("action.about"))

        self.lb_current_file.setText(tr("app.current_file"))
        self.lb_encoding.setText(tr("app.encoding"))
        if self.le_filepath.text() == "":
            self.le_filepath.setPlaceholderText(tr("app.did_not_open_file"))

        self.cmb_encoding.setItemText(0, tr("encoding.auto_detect"))

        self.chk_edit_single_page.setText(tr("app.edit_single_page"))
        self.chk_allow_page_split.setText(tr("app.allow_page_split"))
        self.chk_force_no_wrap.setText(tr("app.force_no_wrap"))

        self.chk_edit_single_page.setToolTip(tr("app.edit_single_page_tips"))
        self.chk_allow_page_split.setToolTip(tr("app.allow_page_split_tips"))
        self.chk_force_no_wrap.setToolTip(tr("app.force_no_wrap_tips"))

        self.lb_index.setToolTip(tr("page_label.tips"))

        self.pbtn_last_page.setText(tr("app.last_page"))
        self.pbtn_next_page.setText(tr("app.next_page"))
