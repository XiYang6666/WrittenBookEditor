# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_AboutForm(object):
    def setupUi(self, AboutForm):
        if not AboutForm.objectName():
            AboutForm.setObjectName(u"AboutForm")
        AboutForm.resize(320, 180)
        self.verticalLayout_2 = QVBoxLayout(AboutForm)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 3, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(AboutForm)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.tabWidget = QTabWidget(AboutForm)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_about = QWidget()
        self.tab_about.setObjectName(u"tab_about")
        self.gridLayout_2 = QGridLayout(self.tab_about)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = QLabel(self.tab_about)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_9.setOpenExternalLinks(True)

        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_about, "")
        self.tab_author = QWidget()
        self.tab_author.setObjectName(u"tab_author")
        self.verticalLayout_3 = QVBoxLayout(self.tab_author)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.tab_author)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label_8, 1, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMouseTracking(True)

        self.gridLayout.addWidget(self.label_11, 3, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_author, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(AboutForm)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AboutForm)
    # setupUi

    def retranslateUi(self, AboutForm):
        AboutForm.setWindowTitle(QCoreApplication.translate("AboutForm", u"\u5173\u4e8e", None))
        self.label.setText(QCoreApplication.translate("AboutForm", u"WrittenBookEditor v0.1.0", None))
        self.label_9.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p>\u57fa\u4e8e Pyside6 \u7684 Minecraft \u6210\u4e66\u7f16\u8f91\u5668<br/></p><table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\"><tr><td><p>\u4e3b\u9875</p></td><td><p><a href=\"https://github.com/XiYang6666/WrittenBookEditor\"><span style=\" text-decoration: underline; color:#007af4;\">https://github.com/XiYang6666/WrittenBookEditor</span></a></p></td></tr><tr><td><p>\u62a5\u544a\u95ee\u9898</p></td><td><p><a href=\"https://github.com/XiYang6666/WrittenBookEditor/issues\"><span style=\" text-decoration: underline; color:#007af4;\">https://github.com/XiYang6666/WrittenBookEditor/issues</span></a></p></td></tr></table></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about), QCoreApplication.translate("AboutForm", u"\u5173\u4e8e", None))
        self.groupBox.setTitle(QCoreApplication.translate("AboutForm", u"\u4f5c\u8005", None))
        self.label_5.setText(QCoreApplication.translate("AboutForm", u"Github", None))
        self.label_3.setText(QCoreApplication.translate("AboutForm", u"\u7535\u5b50\u90ae\u4ef6", None))
        self.label_4.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"mailto:1782356858@qq.com\"><span style=\" text-decoration: underline; color:#007af4;\">1782356858@qq.com</span></a></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("AboutForm", u"XiYang6666", None))
        self.label_6.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"https://github.com/XiYang6666\"><span style=\" text-decoration: underline; color:#007af4;\">https://github.com/XiYang6666</span></a></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("AboutForm", u"\u4e3b\u9875", None))
        self.label_8.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"https://xiyang6666.top/\"><span style=\" text-decoration: underline; color:#007af4;\">https://xiyang6666.top/</span></a></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("AboutForm", u"BiliBili", None))
        self.label_11.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"https://space.bilibili.com/1088981781\"><span style=\" text-decoration: underline; color:#007af4;\">https://space.bilibili.com/1088981781</span></a></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_author), QCoreApplication.translate("AboutForm", u"\u4f5c\u8005", None))
    # retranslateUi

