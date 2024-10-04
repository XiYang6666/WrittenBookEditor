import math
from io import StringIO
from typing import Optional
from pathlib import Path

from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMessageBox
from PySide6.QtGui import QImage, QPixmap, QPainter, QResizeEvent, QMouseEvent, QShortcut, QKeySequence
from PySide6.QtCore import Qt
import chardet

from .main_window import MainWindow
from .jump_form_window import JumpFormWindow
from .encoding_window import EncodingWindow
from .book import Page
from .render import render_page, RENDERED_PAGE_WIDTH, RENDERED_PAGE_HEIGHT


class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self.dpi = self.devicePixelRatio()
        self.graph_scale = 1

        self.main_window = MainWindow()
        self.main_window.show()

        self.filepath: Optional[Path] = None
        self.content: str = ""

        self.pages = []
        self.page_index = 0
        self.not_saved = False

        self.setup_graph_view()
        self.setup_graph_scene()
        self.setup_background()
        self.setup_page()

        self.update_graph()
        self.update_buttons_and_label()

        self.setup_events()
        self.setup_shortcuts()

    # setup
    def setup_graph_view(self):
        self.main_window.gv_book_view.scale(1 / self.dpi, 1 / self.dpi)
        self.main_window.gv_book_view.resize(int(self.main_window.gv_book_view.width() * self.dpi), int(self.main_window.gv_book_view.height() * self.dpi))
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
        self.main_window.gv_book_view.resizeEvent = self.on_gv_resize

        self.main_window.action_new.triggered.connect(self.on_action_new)
        self.main_window.action_open_file.triggered.connect(self.on_action_open_file)
        self.main_window.action_save.triggered.connect(self.on_action_save)
        self.main_window.action_save_as.triggered.connect(self.on_action_save_as)
        self.main_window.action_force_unicode.triggered.connect(self.on_action_setting_changed)
        self.main_window.action_jp_font.triggered.connect(self.on_action_setting_changed)

        self.main_window.txe_text.textChanged.connect(self.on_text_changed)
        self.main_window.chk_edit_single_page.stateChanged.connect(self.on_chk_edit_single_page_changed)

        self.main_window.cmb_encoding.currentTextChanged.connect(self.on_cmb_encoding_changed)

        self.main_window.pbtn_last_page.clicked.connect(self.on_click_last_page)
        self.main_window.pbtn_next_page.clicked.connect(self.on_click_next_page)

        self.main_window.lb_index.mouseReleaseEvent = self.on_index_label_clicked

    def setup_shortcuts(self):
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self.main_window)
        self.shortcut_save.activated.connect(self.on_action_save)

    # methods

    def get_encoding(self) -> Optional[str]:
        encoding = self.main_window.cmb_encoding.currentText()
        if encoding == "自动识别":
            return None
        else:
            return encoding

    def set_text_block_event(self, text: str):
        self.main_window.txe_text.blockSignals(True)
        self.main_window.txe_text.setPlainText(text)
        self.main_window.txe_text.blockSignals(False)

    def set_encoding_block_event(self, encoding: str):
        self.main_window.cmb_encoding.blockSignals(True)
        self.main_window.cmb_encoding.setCurrentText(encoding)
        self.main_window.cmb_encoding.blockSignals(False)

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
        pre_length = 0
        for page in self.pages[:from_index]:
            pre_length += len(page.origin_text())
        content = self.content[pre_length:]
        unicode = self.main_window.action_force_unicode.isChecked()
        jp = self.main_window.action_jp_font.isChecked()
        stream = StringIO(content)
        pages = []
        while True:
            pages.append(Page.from_plaintext_stream(stream, unicode, jp))
            if stream.read(1) == "":
                break
            else:
                stream.seek(stream.tell() - 1)
        self.pages = self.pages[:from_index] + pages
        self.page_index = min(len(self.pages) - 1, max(0, self.page_index))
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
        self.main_window.lb_index.setText(f"第{current_volume+1}/{total_volume+1}卷 第{current_page+1}/{max(total_pages,1)}页 共{len(self.pages)}页")

    def update_single_page_mode(self):
        state = self.main_window.chk_edit_single_page.isChecked()
        if not state:
            self.set_text_block_event(self.content)
        elif self.page_index < len(self.pages):
            self.set_text_block_event(self.pages[self.page_index].origin_text())

    def update_title(self):
        if self.filepath is None:
            self.main_window.setWindowTitle("WrittenBookEditor")
        else:
            self.main_window.setWindowTitle(f"WrittenBookEditor - {self.filepath.name}{' *' if self.not_saved else ''}")

    # events

    def on_gv_resize(self, event: QResizeEvent):
        self.update_graph()

    # action events

    def on_action_new(self):
        if self.not_saved:
            reply = QMessageBox.question(self.main_window, "新建文件", "文件尚未保存，是否保存？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Yes:
                self.on_action_save()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
        file_name, _ = QFileDialog.getSaveFileName(self.main_window, "新建文件", "", "文本文件 (*.txt)")
        try:
            filepath = Path(file_name)
            filepath.touch()
        except Exception as e:
            QMessageBox.warning(self.main_window, "新建文件", f"创建文件失败: {e}")
            return
        else:
            self.filepath = filepath
            self.content = ""
            self.on_action_save()
            self.set_text_block_event(self.content)
            self.update_title()
            self.update_pages()
            self.update_view_page()

    def on_action_open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, "打开文件", "", "文本文件 (*.txt)")
        filepath = Path(file_name)
        if not filepath.exists():
            QMessageBox.warning(self.main_window, "打开文件", "文件不存在！")
            return
        if not filepath.is_file():
            QMessageBox.warning(self.main_window, "打开文件", "不是文件！")
            return
        bytes = filepath.read_bytes()
        encoding = self.get_encoding() or chardet.detect(bytes)["encoding"] or "utf-8"
        while True:
            try:
                self.content = bytes.decode(encoding)
            except UnicodeDecodeError as e:
                encoding_dialog = EncodingWindow(self.main_window)
                encoding_dialog.exec()
                encoding = encoding_dialog.result_value
                if encoding is None:
                    return
                if encoding == "自动识别":
                    encoding = chardet.detect(bytes)["encoding"] or "utf-8"
                continue
            except Exception as e:
                QMessageBox.warning(self.main_window, "打开文件", f"读取文件失败: {e}")
            else:
                break
        self.set_encoding_block_event(encoding)
        self.filepath = filepath
        self.main_window.le_filepath.setText(str(self.filepath))
        self.update_title()
        self.set_text_block_event(self.content)
        self.update_pages()
        self.update_view_page()

    def on_action_save(self):
        self.not_saved = False
        if self.filepath is None:
            filename, _ = QFileDialog.getSaveFileName(self.main_window, "保存文件", "", "文本文件 (*.txt)")
            filepath = Path(filename)
        else:
            filepath = self.filepath
        try:
            filepath.touch()
            filepath.write_text(self.content, encoding=self.get_encoding() or "utf-8", newline="\n")
        except Exception as e:
            QMessageBox.warning(self.main_window, "保存文件", f"写入文件失败: {e}")
        else:
            self.filepath = filepath
            self.main_window.le_filepath.setText(str(self.filepath))
            self.update_title()

    def on_action_save_as(self):
        filename, _ = QFileDialog.getSaveFileName(self.main_window, "另存为", "", "文本文件 (*.txt)")
        filepath = Path(filename)
        try:
            filepath.touch()
            filepath.write_text(self.content, encoding=self.get_encoding() or "utf-8")
        except Exception as e:
            QMessageBox.warning(self.main_window, "另存为", f"写入文件失败: {e}")
        else:
            self.filepath = filepath
            self.main_window.le_filepath.setText(str(self.filepath))
            self.update_title()

    def on_action_setting_changed(self):
        self.update_pages()
        self.update_view_page()
        self.update_single_page_mode()

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
            self.set_text_block_event(self.pages[self.page_index].origin_text())
            cursor.setPosition(min(position, len(self.main_window.txe_text.toPlainText())))
            self.main_window.txe_text.setTextCursor(cursor)
        else:
            self.content = self.main_window.txe_text.toPlainText()
            self.update_pages()
        self.update_view_page()

    # checkbox events

    def on_chk_edit_single_page_changed(self, state):
        self.update_single_page_mode()

    # button events

    def on_click_last_page(self):
        self.page_index = max(0, self.page_index - 1)
        self.update_single_page_mode()
        self.update_view_page()
        self.update_buttons_and_label()

    def on_click_next_page(self):
        self.page_index = min(len(self.pages) - 1, self.page_index + 1)
        self.update_single_page_mode()
        self.update_view_page()
        self.update_buttons_and_label()

    # label events

    def on_index_label_clicked(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            jump_dialog = JumpFormWindow(self.main_window, len(self.pages), self.page_index)
            jump_dialog.exec()
            if jump_dialog.result_value is not None:
                self.page_index = jump_dialog.result_value
                self.update_single_page_mode()
                self.update_view_page()
                self.update_buttons_and_label()

    # combo box events
    def on_cmb_encoding_changed(self, index):
        if self.filepath is not None:
            self.not_saved = True
            self.update_title()
