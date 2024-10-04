# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGraphicsView, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMinimumSize(QSize(600, 400))
        self.action_open_file = QAction(MainWindow)
        self.action_open_file.setObjectName(u"action_open_file")
        self.action_open_file.setCheckable(False)
        self.action_open_file.setIconVisibleInMenu(False)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save_as = QAction(MainWindow)
        self.action_save_as.setObjectName(u"action_save_as")
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        self.actionMiniMessage = QAction(MainWindow)
        self.actionMiniMessage.setObjectName(u"actionMiniMessage")
        self.action_force_unicode = QAction(MainWindow)
        self.action_force_unicode.setObjectName(u"action_force_unicode")
        self.action_force_unicode.setCheckable(True)
        self.action_jp_font = QAction(MainWindow)
        self.action_jp_font.setObjectName(u"action_jp_font")
        self.action_jp_font.setCheckable(True)
        self.action_allow_page_split = QAction(MainWindow)
        self.action_allow_page_split.setObjectName(u"action_allow_page_split")
        self.action_allow_page_split.setCheckable(True)
        self.action_export = QAction(MainWindow)
        self.action_export.setObjectName(u"action_export")
        self.action_chinese = QAction(MainWindow)
        self.action_chinese.setObjectName(u"action_chinese")
        self.action_english = QAction(MainWindow)
        self.action_english.setObjectName(u"action_english")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 2, 10, 10)
        self.verticalLayout_left = QVBoxLayout()
        self.verticalLayout_left.setObjectName(u"verticalLayout_left")
        self.frame_file_options = QFrame(self.centralwidget)
        self.frame_file_options.setObjectName(u"frame_file_options")
        self.frame_file_options.setFrameShape(QFrame.StyledPanel)
        self.frame_file_options.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_file_options)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(6)
        self.label_0 = QLabel(self.frame_file_options)
        self.label_0.setObjectName(u"label_0")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_0)

        self.le_filepath = QLineEdit(self.frame_file_options)
        self.le_filepath.setObjectName(u"le_filepath")
        self.le_filepath.setMaximumSize(QSize(16777215, 25))
        self.le_filepath.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.le_filepath)

        self.label_1 = QLabel(self.frame_file_options)
        self.label_1.setObjectName(u"label_1")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_1)

        self.cmb_encoding = QComboBox(self.frame_file_options)
        self.cmb_encoding.addItem("")
        self.cmb_encoding.addItem("")
        self.cmb_encoding.addItem("")
        self.cmb_encoding.addItem("")
        self.cmb_encoding.setObjectName(u"cmb_encoding")
        self.cmb_encoding.setMaximumSize(QSize(16777215, 25))

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cmb_encoding)


        self.verticalLayout_left.addWidget(self.frame_file_options)

        self.frame_export_options = QFrame(self.centralwidget)
        self.frame_export_options.setObjectName(u"frame_export_options")
        self.frame_export_options.setFrameShape(QFrame.StyledPanel)
        self.frame_export_options.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_export_options)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, -1, -1, -1)
        self.chk_edit_single_page = QCheckBox(self.frame_export_options)
        self.chk_edit_single_page.setObjectName(u"chk_edit_single_page")

        self.horizontalLayout_3.addWidget(self.chk_edit_single_page)

        self.chk_allow_page_split = QCheckBox(self.frame_export_options)
        self.chk_allow_page_split.setObjectName(u"chk_allow_page_split")
        self.chk_allow_page_split.setChecked(True)
        self.chk_allow_page_split.setTristate(False)

        self.horizontalLayout_3.addWidget(self.chk_allow_page_split)


        self.verticalLayout_left.addWidget(self.frame_export_options)

        self.txe_text = QPlainTextEdit(self.centralwidget)
        self.txe_text.setObjectName(u"txe_text")

        self.verticalLayout_left.addWidget(self.txe_text)


        self.horizontalLayout_2.addLayout(self.verticalLayout_left)

        self.frame_right = QFrame(self.centralwidget)
        self.frame_right.setObjectName(u"frame_right")
        self.frame_right.setFrameShape(QFrame.StyledPanel)
        self.frame_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_right)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pbtn_last_page = QPushButton(self.frame_right)
        self.pbtn_last_page.setObjectName(u"pbtn_last_page")
        self.pbtn_last_page.setMinimumSize(QSize(0, 0))
        self.pbtn_last_page.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.pbtn_last_page)

        self.lb_index = QLabel(self.frame_right)
        self.lb_index.setObjectName(u"lb_index")
        self.lb_index.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lb_index)

        self.pbtn_next_page = QPushButton(self.frame_right)
        self.pbtn_next_page.setObjectName(u"pbtn_next_page")
        self.pbtn_next_page.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.pbtn_next_page)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gv_book_view = QGraphicsView(self.frame_right)
        self.gv_book_view.setObjectName(u"gv_book_view")

        self.verticalLayout_2.addWidget(self.gv_book_view)


        self.horizontalLayout_2.addWidget(self.frame_right)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 600, 17))
        self.menu_file = QMenu(self.menuBar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_help = QMenu(self.menuBar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_help.setToolTipsVisible(False)
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        self.menu_lang = QMenu(self.menuBar)
        self.menu_lang.setObjectName(u"menu_lang")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_lang.menuAction())
        self.menuBar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_open_file)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_export)
        self.menu_help.addAction(self.action_about)
        self.menu.addAction(self.action_force_unicode)
        self.menu.addAction(self.action_jp_font)
        self.menu_lang.addAction(self.action_chinese)
        self.menu_lang.addAction(self.action_english)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"WrittenBookEditor", None))
        self.action_open_file.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58...", None))
        self.action_save_as.setText(QCoreApplication.translate("MainWindow", u"\u53e6\u5b58\u4e3a...", None))
        self.action_new.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa", None))
        self.actionMiniMessage.setText(QCoreApplication.translate("MainWindow", u"MiniMessage", None))
        self.action_force_unicode.setText(QCoreApplication.translate("MainWindow", u"\u5f3a\u5236\u4f7f\u7528Unicode\u5b57\u4f53", None))
        self.action_jp_font.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u672c\u5b57\u5f62\u53d8\u4f53", None))
        self.action_allow_page_split.setText(QCoreApplication.translate("MainWindow", u"\u5141\u8bb8\u4e66\u9875\u5206\u9694\u5355\u8bcd", None))
        self.action_export.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa", None))
        self.action_chinese.setText(QCoreApplication.translate("MainWindow", u"\u7b80\u4f53\u4e2d\u6587", None))
        self.action_english.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.label_0.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u6587\u4ef6", None))
        self.le_filepath.setText(QCoreApplication.translate("MainWindow", u"\u8fd8\u6ca1\u6709\u6253\u5f00\u4efb\u4f55\u6587\u4ef6\u5462~", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u7801\u683c\u5f0f", None))
        self.cmb_encoding.setItemText(0, QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u8bc6\u522b", None))
        self.cmb_encoding.setItemText(1, QCoreApplication.translate("MainWindow", u"UTF-8", None))
        self.cmb_encoding.setItemText(2, QCoreApplication.translate("MainWindow", u"GBK", None))
        self.cmb_encoding.setItemText(3, QCoreApplication.translate("MainWindow", u"BIG5", None))

        self.chk_edit_single_page.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91\u5355\u9875", None))
        self.chk_allow_page_split.setText(QCoreApplication.translate("MainWindow", u"\u5141\u8bb8\u4e66\u9875\u5206\u9694\u5355\u8bcd", None))
        self.pbtn_last_page.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e00\u9875", None))
        self.lb_index.setText(QCoreApplication.translate("MainWindow", u"\u7b2c0\u5377 \u7b2c0/0\u9875 (\u51710\u9875)", None))
        self.pbtn_next_page.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u9875", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.menu_lang.setTitle(QCoreApplication.translate("MainWindow", u"\u8bed\u8a00", None))
    # retranslateUi

