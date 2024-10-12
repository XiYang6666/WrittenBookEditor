import math
import locale
from io import StringIO
from typing import Optional
from pathlib import Path

from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsPixmapItem, QDialog, QFileDialog, QMessageBox
from PySide6.QtGui import QResizeEvent, QMouseEvent, QCloseEvent, QShortcut, QKeySequence, QDragEnterEvent, QDropEvent, QWheelEvent
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtCore import Qt
import chardet

from .gui.main_window import MainWindow
from .gui.jump_dialog import JumpDialog
from .gui.encoding_dialog import EncodingDialog
from .gui.about_dialog import AboutDialog
from .gui.export_dialog import ExportDialog
from .book import Page
from .render import render_page, RENDERED_PAGE_WIDTH, RENDERED_PAGE_HEIGHT
from .export import export_book, ExportItemType, ExportFileType, CommandVersion
from .util.open_folder import open_folder
from .i18n import set_lang, translate as tr


class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self.dpi: float = self.devicePixelRatio()
        self.graph_scale: int = 1
        self.filepath: Optional[Path] = None
        self.content: str = ""
        self.not_saved: bool = False
        self.pages: list[Page] = []
        self.page_index: int = 0
        self.about_dialog: Optional[AboutDialog] = None

        self.main_window = MainWindow()
        self.main_window.setAcceptDrops(True)
        self.main_window.show()

        current_locale, _ = locale.getlocale()
        if current_locale and (current_locale.startswith("zh_") or current_locale.startswith("Chinese")):
            self.setup_lang("zh_CN")
        else:
            self.setup_lang("en_US")
        self.setup_graph_view()
        self.setup_graph_scene()
        self.setup_background()
        self.setup_page()

        self.update_graph()
        self.update_buttons_and_label()

        self.setup_events()
        self.setup_shortcuts()

    # setup

    def setup_lang(self, lang: str):
        set_lang(lang)
        self.main_window.update_lang()
        self.update_buttons_and_label()

    def setup_graph_view(self):
        self.main_window.gv_book_view.scale(1 / self.dpi, 1 / self.dpi)
        self.main_window.gv_book_view.resize(
            int(self.main_window.gv_book_view.width() * self.dpi),
            int(self.main_window.gv_book_view.height() * self.dpi),
        )
        self.main_window.gv_book_view.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    def setup_graph_scene(self):
        self.scene = QGraphicsScene()
        self.main_window.gv_book_view.setScene(self.scene)

    def setup_background(self):
        self.graph_original_background = QImage("./data/textures/book.png")  # 146*180
        self.graph_bg_item = QGraphicsPixmapItem()
        self.scene.addItem(self.graph_bg_item)

    def setup_page(self):
        self.pages: list[Page] = []
        self.page_index: int = 0
        self.graph_page_item = QGraphicsPixmapItem()
        self.scene.addItem(self.graph_page_item)

    def setup_events(self):
        self.main_window.dragEnterEvent = self.on_drag_enter
        self.main_window.dropEvent = self.on_drop
        self.main_window.gv_book_view.resizeEvent = self.on_gv_resize

        self.main_window.action_new.triggered.connect(self.on_action_new)
        self.main_window.action_open_file.triggered.connect(self.on_action_open_file)
        self.main_window.action_save.triggered.connect(self.on_action_save)
        self.main_window.action_save_as.triggered.connect(self.on_action_save_as)
        self.main_window.action_export.triggered.connect(self.on_action_export)
        self.main_window.action_force_unicode.triggered.connect(self.on_action_setting_changed)
        self.main_window.action_jp_font.triggered.connect(self.on_action_setting_changed)
        self.main_window.action_chinese.triggered.connect(self.on_action_chinese)
        self.main_window.action_english.triggered.connect(self.on_action_english)
        self.main_window.action_about.triggered.connect(self.on_action_about)

        self.main_window.txe_text.textChanged.connect(self.on_text_changed)
        self.main_window.chk_edit_single_page.stateChanged.connect(self.on_chk_edit_single_page_changed)
        self.main_window.chk_allow_page_split.stateChanged.connect(self.on_chk_book_option_changed)
        self.main_window.chk_force_no_wrap.stateChanged.connect(self.on_chk_book_option_changed)

        self.main_window.cmb_encoding.currentTextChanged.connect(self.on_cmb_encoding_changed)

        self.main_window.pbtn_last_page.clicked.connect(self.on_click_last_page)
        self.main_window.pbtn_next_page.clicked.connect(self.on_click_next_page)

        self.main_window.lb_index.mouseReleaseEvent = self.on_index_label_clicked
        self.main_window.lb_index.wheelEvent = self.on_index_label_scroll

    def setup_shortcuts(self):
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self.main_window)
        self.shortcut_save.activated.connect(self.on_action_save)

    # methods

    def get_encoding(self) -> Optional[str]:
        encoding = self.main_window.cmb_encoding.currentText()
        if encoding == tr("encoding.auto_detect"):  # "自动识别"
            return None
        else:
            return encoding

    def set_encoding(self, encoding: str):
        self.main_window.cmb_encoding.blockSignals(True)
        self.main_window.cmb_encoding.setCurrentText(encoding)
        self.main_window.cmb_encoding.blockSignals(False)

    def set_text(self, text: str):
        self.main_window.txe_text.blockSignals(True)
        self.main_window.txe_text.setPlainText(text)
        self.main_window.txe_text.blockSignals(False)

    def set_content_with_unknown_encoding(self, data: bytes) -> Optional[str]:
        encoding = self.get_encoding() or chardet.detect(data)["encoding"] or "utf-8"
        while True:
            try:
                self.content = data.decode(encoding)
            except UnicodeDecodeError:
                encoding_dialog = EncodingDialog(self.main_window)
                if encoding_dialog.exec() == QDialog.DialogCode.Rejected:
                    return None
                encoding = encoding_dialog.get_result()
                if encoding == tr("encoding.auto_detect"):  # "自动识别"
                    encoding = chardet.detect(data)["encoding"] or "utf-8"
                continue
            except Exception as e:
                QMessageBox.warning(
                    self.main_window,
                    tr("file_dialog.open_file"),  # "打开文件"
                    tr("file_dialog.failed_to_read_file").format(exception=e),  # f"读取文件失败: {e}"
                )
            else:
                return encoding

    def set_filepath(self, filepath: Path):
        self.filepath = filepath
        self.main_window.le_filepath.setText(str(self.filepath))

    def confirm_save(self) -> bool:
        if self.not_saved:
            reply = QMessageBox.question(
                self.main_window,
                tr("file_dialog.open_file"),  # "打开文件"
                tr("file_dialog.file_not_saved"),  # "文件尚未保存，是否保存？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.on_action_save()
            elif reply == QMessageBox.StandardButton.Cancel:
                return False
        self.not_saved = False
        return True

    # update

    def update_graph(self):
        width = self.main_window.gv_book_view.viewport().width() * self.dpi
        height = self.main_window.gv_book_view.viewport().height() * self.dpi
        self.main_window.gv_book_view.setSceneRect(0, 0, width, height)
        self.scene.setSceneRect(0, 0, width, height)
        self.update_background()
        self.update_view_page()

    def update_background(self):
        self.graph_scale = int(max(min(self.scene.width() // 146 // 2, self.scene.height() // 180 // 2), 1))
        bg_image = self.graph_original_background.scaled(146 * self.graph_scale * 2, 180 * self.graph_scale * 2)
        bg_pixmap = QPixmap.fromImage(bg_image)
        self.graph_bg_item.setPixmap(bg_pixmap)
        self.graph_bg_item.setPos((self.scene.width() - bg_pixmap.width()) / 2, (self.scene.height() - bg_pixmap.height()) / 2)

    def update_view_page(self):
        if len(self.pages) == 0:
            page_pixmap = QPixmap(RENDERED_PAGE_WIDTH, RENDERED_PAGE_HEIGHT)
            page_pixmap.fill("#00000000")
        else:
            unicode = self.main_window.action_force_unicode.isChecked()
            jp = self.main_window.action_jp_font.isChecked()
            page = self.pages[self.page_index]
            page_img = render_page(page, unicode, jp)
            page_img = page_img.scaled(page_img.width() * self.graph_scale, page_img.height() * self.graph_scale)
            page_pixmap = QPixmap.fromImage(page_img)
        self.graph_page_item.setPixmap(page_pixmap)
        self.graph_page_item.setPos((self.scene.width() - page_pixmap.width()) / 2, (self.scene.height() - page_pixmap.height()) / 2)

    def update_pages(self, from_index: int = 0):
        # options
        unicode = self.main_window.action_force_unicode.isChecked()
        jp = self.main_window.action_jp_font.isChecked()
        allow_page_split = self.main_window.chk_allow_page_split.isChecked()
        force_no_wrap = self.main_window.chk_force_no_wrap.isChecked()
        # update pages
        pre_length = 0
        for page in self.pages[:from_index]:
            pre_length += len(page.origin_text())
        content = self.content[pre_length:]
        stream = StringIO(content)
        pages = []
        while True:
            if stream.read(1) == "":
                break
            else:
                stream.seek(stream.tell() - 1)
            page = Page.from_plaintext_stream(
                stream,
                unicode=unicode,
                jp=jp,
                allow_page_split=allow_page_split,
                force_no_wrap=force_no_wrap,
            )
            pages.append(page)

        self.pages = self.pages[:from_index] + pages
        self.page_index = max(0, min(len(self.pages) - 1, self.page_index))
        self.update_buttons_and_label()

    def update_buttons_and_label(self):
        # update buttons
        if self.page_index <= 0:
            self.main_window.pbtn_last_page.setEnabled(False)
        else:
            self.main_window.pbtn_last_page.setEnabled(True)
        if self.page_index >= len(self.pages) - 1:
            self.main_window.pbtn_next_page.setEnabled(False)
        else:
            self.main_window.pbtn_next_page.setEnabled(True)
        # update label
        total_volume = math.ceil(len(self.pages) // 100)
        current_volume = self.page_index // 100
        total_pages = min(100, len(self.pages) - current_volume * 100)
        current_page = self.page_index % 100
        label_text = (
            tr("page_label.volume_index").format(index=current_volume + 1, total=total_volume + 1)
            + " "
            + tr("page_label.page_index").format(index=current_page + 1, total=max(total_pages, 1))
            + " "
            + tr("page_label.total_pages").format(total=len(self.pages))
        )
        # f"第{current_volume+1}/{total_volume+1}卷 "
        # f"第{current_page+1}/{max(total_pages,1)}页 "
        # f"共{len(self.pages)}页"
        self.main_window.lb_index.setText(label_text)

    def update_text_editor(self):
        state = self.main_window.chk_edit_single_page.isChecked()
        if not state:
            self.set_text(self.content)
        elif self.page_index < len(self.pages):
            self.set_text(self.pages[self.page_index].origin_text())

    def update_title(self):
        if self.filepath is None:
            self.main_window.setWindowTitle("WrittenBookEditor")
        else:
            self.main_window.setWindowTitle(f"WrittenBookEditor - {self.filepath.name}{' *' if self.not_saved else ''}")

    # events

    def on_drag_enter(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1 and Path(event.mimeData().urls()[0].toLocalFile()).is_file():
            event.acceptProposedAction()
        else:
            event.ignore()

    def on_drop(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if not self.confirm_save():
            return
        filepath = Path(urls[0].toLocalFile())
        try:
            data = filepath.read_bytes()
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                tr("file_dialog.open_file"),  # "打开文件"
                tr("file_dialog.failed_to_read_file").format(exception=e),  # f"读取文件失败: {e}"
            )
            return
        encoding = self.set_content_with_unknown_encoding(data)
        if encoding is None:
            return
        self.set_filepath(filepath)
        self.update_pages()
        self.update_view_page()
        self.update_text_editor()
        self.update_title()
        self.set_encoding(encoding)

    def on_gv_resize(self, event: QResizeEvent):
        self.update_graph()

    # action events

    def on_action_new(self):
        if not self.confirm_save():
            return
        file_name, _ = QFileDialog.getSaveFileName(
            self.main_window,
            tr("file_dialog.new_file"),  # "新建文件"
            "",
            f"{tr('general.txt_file')} (*.txt)",  # "文本文件 (*.txt)",
        )
        if file_name == "":
            return
        try:
            filepath = Path(file_name)
            filepath.touch()
            if not filepath.exists():
                QMessageBox.warning(
                    self.main_window,
                    tr("file_dialog.new_file"),  # "新建文件"
                    tr("file_dialog.no_such_file"),  # "文件不存在！"
                )
                return
            if not filepath.is_file():
                QMessageBox.warning(
                    self.main_window,
                    tr("file_dialog.new_file"),  # "新建文件"
                    tr("file_dialog.not_a_file"),  # "不是文件！"
                )
                return
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                tr("file_dialog.new_file"),  # "新建文件"
                tr("file_dialog.failed_to_create_file").format(exception=e),  # f"创建文件失败: {e}"
            )
            return
        else:
            self.set_filepath(filepath)
            self.content = ""
            self.on_action_save()
            self.update_title()
            self.update_pages()
            self.update_view_page()
            self.update_text_editor()

    def on_action_open_file(self):
        if not self.confirm_save():
            return
        file_name, _ = QFileDialog.getOpenFileName(
            self.main_window,
            tr("file_dialog.open_file"),  # "打开文件"
            "",
            f"{tr('general.txt_file')} (*.txt)",  # "文本文件 (*.txt)",
        )
        if file_name == "":
            return
        self.not_saved = False
        filepath = Path(file_name)
        if not filepath.exists():
            QMessageBox.warning(
                self.main_window,
                tr("file_dialog.open_file"),  # "打开文件"
                tr("file_dialog.no_such_file"),  # "文件不存在！"
            )
            return
        if not filepath.is_file():
            QMessageBox.warning(
                self.main_window,
                tr("file_dialog.open_file"),  # "打开文件"
                tr("file_dialog.not_a_file"),  # "不是文件！"
            )
            return
        try:
            data = filepath.read_bytes()
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                tr("file_dialog.open_file"),  # "打开文件"
                tr("file_dialog.failed_to_read_file").format(exception=e),  # f"读取文件失败: {e}"
            )
            return
        encoding = self.set_content_with_unknown_encoding(data)
        if encoding is None:
            return
        self.set_filepath(filepath)
        self.update_pages()
        self.update_view_page()
        self.update_text_editor()
        self.update_title()
        self.set_encoding(encoding)

    def on_action_save(self):
        self.not_saved = False
        if self.filepath is None:
            filename, _ = QFileDialog.getSaveFileName(
                self.main_window,
                tr("file_dialog.save_file"),  # "保存文件"
                "",
                f"{tr('general.txt_file')} (*.txt)",  # "文本文件 (*.txt)"
            )
            if filename == "":
                return
            filepath = Path(filename)
        else:
            filepath = self.filepath
        try:
            filepath.touch()
            filepath.write_text(self.content, encoding=self.get_encoding() or "utf-8", newline="\n")  # 统一使用 LF
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                tr("file_dialog.save_file"),  # "保存文件"
                tr("file_dialog.failed_to_write_file").format(exception=e),  # f"写入文件失败: {e}"
            )
        else:
            self.set_filepath(filepath)
            self.update_title()

    def on_action_save_as(self):
        filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            tr("file_dialog.save_as"),  # "另存为"
            "",
            f"{tr('general.txt_file')} (*.txt)",  # "文本文件 (*.txt)"
        )
        if filename == "":
            return
        filepath = Path(filename)
        try:
            filepath.touch()
            filepath.write_text(self.content, encoding=self.get_encoding() or "utf-8")
        except Exception as e:
            QMessageBox.warning(
                self.main_window,
                tr("file_dialog.save_as"),  # "另存为"
                tr("file_dialog.failed_to_write_file").format(exception=e),  # f"写入文件失败: {e}"
            )
        else:
            self.set_filepath(filepath)
            self.update_title()

    def on_action_export(self):
        dialog = ExportDialog(self.main_window)

        def on_export():
            result = dialog.get_result()
            # get export path
            if not result["title"]:
                QMessageBox.warning(
                    dialog,
                    tr("export_dialog_message.export"),  # "导出"
                    tr("export_dialog_message.title_must_not_be_empty"),  # "标题不能为空！"
                )
                return
            if result["file_type"] == tr("file_type.command_text"):  # "指令纯文本"
                filepath = QFileDialog.getExistingDirectory(
                    dialog,
                    tr("export_dialog_message.select_export_folder"),  # "选择导出文件夹"
                    "",
                    QFileDialog.Option.ShowDirsOnly,
                )
                export_type = ExportFileType.COMMAND_TEXT
            elif result["file_type"] == tr("file_type.function_text"):  # "mc 函数文件"
                filepath, _ = QFileDialog.getSaveFileName(
                    dialog,
                    tr("export_dialog_message.select_export_file"),  # "选择导出文件"
                    result["title"] + ".mcfunction",
                    f"{tr('file_type.function_text')} (*.mcfunction)",
                )
                export_type = ExportFileType.FUNCTION_FILE
            elif result["file_type"] == tr("file_type.data_pack"):  # "数据包"
                filepath, _ = QFileDialog.getSaveFileName(
                    dialog,
                    tr("export_dialog_message.select_export_file"),  # "选择导出文件"
                    result["title"] + ".zip",
                    f"{tr('file_type.data_pack')} (*.zip)",  # "数据包 (*.zip)"
                )
                export_type = ExportFileType.DATA_PACK
            else:
                QMessageBox.warning(
                    dialog,
                    tr("export_dialog_message.export"),  # "导出"
                    tr("export_dialog_message.unknown_export_type"),  # "未知导出类型！"
                )
                return
            if filepath == "":
                return
            # get item options
            if result["item_type"] == tr("item_type.written_book"):  # "成书"
                item_type = ExportItemType.WRITTEN_BOOK
            elif result["item_type"] == tr("item_type.shulker_box"):  # "潜影盒"
                item_type = ExportItemType.SHULKER_BOX
            else:
                QMessageBox.warning(
                    dialog,
                    tr("export_dialog_message.export"),  # "导出"
                    tr("export_dialog_message.unknown_export_type"),  # "未知导出类型！"
                )
                return
            # get command version
            if result["command_version"] == tr("command_version.upper_1_13"):  # ">=1.13 <1.20.5"
                command_version = CommandVersion.UPPER_1_13
            elif result["command_version"] == tr("command_version.upper_1_20_5"):  # ">=1.20.5"
                command_version = CommandVersion.UPPER_1_20_5
            else:
                QMessageBox.warning(
                    dialog,
                    tr("export_dialog_message.export"),  # "导出"
                    tr("export_dialog_message.unknown_command_version"),  # "未知指令版本！"
                )
                return
            try:
                export_book(
                    self.pages,
                    filepath,
                    result["title"],
                    result["author"],
                    item_type,
                    export_type,
                    command_version,
                    text_component=result["text_component"],
                    filter=result["filter"],
                )
            except Exception as e:
                QMessageBox.warning(
                    dialog,
                    tr("export_dialog_message.export"),  # "导出"
                    tr("export_dialog_message.failed_to_export").format(exception=e),  # f"导出失败: {e}"
                )
                return
            else:
                QMessageBox.information(
                    dialog,
                    tr("export_dialog_message.export"),  # "导出"
                    tr("export_dialog_message.successfully_exported"),  # "导出成功！"
                )
                open_folder(filepath)

        dialog.pbtn_export.clicked.connect(on_export)
        dialog.exec()

    def on_action_chinese(self):
        self.setup_lang("zh_CN")

    def on_action_english(self):
        self.setup_lang("en_US")

    def on_action_about(self):
        if self.about_dialog is not None:
            return

        def close_about_dialog(arg__1: QCloseEvent):
            self.about_dialog = None

        self.about_dialog = AboutDialog(self.main_window)
        self.about_dialog.closeEvent = close_about_dialog
        self.about_dialog.show()

    def on_action_setting_changed(self):
        self.update_pages()
        self.update_view_page()
        self.update_text_editor()

    # combo box events

    def on_cmb_encoding_changed(self, index):
        if self.filepath is not None:
            self.not_saved = True
            self.update_title()

    # text editor events

    def on_text_changed(self):
        self.not_saved = True
        self.update_title()
        if self.main_window.chk_edit_single_page.isChecked():
            content = ""
            for i, page in enumerate(self.pages):
                if i == self.page_index:
                    content += self.main_window.txe_text.toPlainText()
                else:
                    content += page.origin_text()
            self.content = content
            self.update_pages()
            cursor = self.main_window.txe_text.textCursor()
            position = cursor.position()
            self.set_text(self.pages[self.page_index].origin_text())
            cursor.setPosition(min(position, len(self.main_window.txe_text.toPlainText())))
            self.main_window.txe_text.setTextCursor(cursor)
        else:
            self.content = self.main_window.txe_text.toPlainText()
            self.update_pages(self.page_index)
        self.update_view_page()

    # checkbox events

    def on_chk_edit_single_page_changed(self, state):
        self.update_text_editor()

    def on_chk_book_option_changed(self, state):
        self.update_pages()
        self.update_view_page()
        self.update_text_editor()

    # button events

    def on_click_last_page(self):
        self.page_index = max(0, self.page_index - 1)
        self.update_view_page()
        self.update_text_editor()
        self.update_buttons_and_label()

    def on_click_next_page(self):
        self.page_index = min(max(0, len(self.pages) - 1), self.page_index + 1)
        self.update_view_page()
        self.update_text_editor()
        self.update_buttons_and_label()

    # label events

    def on_index_label_clicked(self, ev: QMouseEvent):
        if ev.button() != Qt.MouseButton.LeftButton:
            return
        jump_dialog = JumpDialog(self.main_window, len(self.pages), self.page_index)
        if jump_dialog.exec() == QDialog.DialogCode.Accepted:
            self.page_index = jump_dialog.get_result()
            self.update_view_page()
            self.update_text_editor()
            self.update_buttons_and_label()

    def on_index_label_scroll(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        shift = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        if delta > 0:
            self.page_index = max(0, self.page_index - (10 if shift else 1))
        elif delta < 0:
            self.page_index = min(max(0, len(self.pages) - 1), self.page_index + (10 if shift else 1))
        self.update_view_page()
        self.update_text_editor()
        self.update_buttons_and_label()
