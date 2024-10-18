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
        self.lb_title = QLabel(AboutForm)
        self.lb_title.setObjectName(u"lb_title")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.lb_title.setFont(font)

        self.verticalLayout.addWidget(self.lb_title)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.tabWidget = QTabWidget(AboutForm)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_about = QWidget()
        self.tab_about.setObjectName(u"tab_about")
        self.gridLayout_2 = QGridLayout(self.tab_about)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lb_about = QLabel(self.tab_about)
        self.lb_about.setObjectName(u"lb_about")
        self.lb_about.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.lb_about.setOpenExternalLinks(True)

        self.gridLayout_2.addWidget(self.lb_about, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_about, "")
        self.tab_author = QWidget()
        self.tab_author.setObjectName(u"tab_author")
        self.verticalLayout_3 = QVBoxLayout(self.tab_author)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gb_author = QGroupBox(self.tab_author)
        self.gb_author.setObjectName(u"gb_author")
        self.gridLayout = QGridLayout(self.gb_author)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lb_github = QLabel(self.gb_author)
        self.lb_github.setObjectName(u"lb_github")

        self.gridLayout.addWidget(self.lb_github, 2, 0, 1, 1)

        self.lb_email = QLabel(self.gb_author)
        self.lb_email.setObjectName(u"lb_email")

        self.gridLayout.addWidget(self.lb_email, 4, 0, 1, 1)

        self.lb_email_link = QLabel(self.gb_author)
        self.lb_email_link.setObjectName(u"lb_email_link")
        self.lb_email_link.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.lb_email_link, 4, 1, 1, 1)

        self.lb_author_name = QLabel(self.gb_author)
        self.lb_author_name.setObjectName(u"lb_author_name")
        font1 = QFont()
        font1.setPointSize(10)
        self.lb_author_name.setFont(font1)

        self.gridLayout.addWidget(self.lb_author_name, 0, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 2, 1, 1)

        self.lb_github_link = QLabel(self.gb_author)
        self.lb_github_link.setObjectName(u"lb_github_link")
        self.lb_github_link.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.lb_github_link, 2, 1, 1, 1)

        self.lb_mainpage = QLabel(self.gb_author)
        self.lb_mainpage.setObjectName(u"lb_mainpage")

        self.gridLayout.addWidget(self.lb_mainpage, 1, 0, 1, 1)

        self.lb_mainpage_link = QLabel(self.gb_author)
        self.lb_mainpage_link.setObjectName(u"lb_mainpage_link")
        self.lb_mainpage_link.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.lb_mainpage_link, 1, 1, 1, 1)

        self.lb_bilibili = QLabel(self.gb_author)
        self.lb_bilibili.setObjectName(u"lb_bilibili")

        self.gridLayout.addWidget(self.lb_bilibili, 3, 0, 1, 1)

        self.lb_bilibili_link = QLabel(self.gb_author)
        self.lb_bilibili_link.setObjectName(u"lb_bilibili_link")
        self.lb_bilibili_link.setMouseTracking(True)
        self.lb_bilibili_link.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.lb_bilibili_link, 3, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.gb_author)

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
        self.lb_title.setText(QCoreApplication.translate("AboutForm", u"WrittenBookEditor v0.1.0", None))
        self.lb_about.setText(QCoreApplication.translate("AboutForm", u"\u829d\u58eb\u7b80\u4ecb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about), QCoreApplication.translate("AboutForm", u"\u5173\u4e8e", None))
        self.gb_author.setTitle(QCoreApplication.translate("AboutForm", u"\u4f5c\u8005", None))
        self.lb_github.setText(QCoreApplication.translate("AboutForm", u"Github", None))
        self.lb_email.setText(QCoreApplication.translate("AboutForm", u"\u7535\u5b50\u90ae\u4ef6", None))
        self.lb_email_link.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"mailto:1782356858@qq.com\"><span style=\" text-decoration: underline; color:#007af4;\">1782356858@qq.com</span></a></p></body></html>", None))
        self.lb_author_name.setText(QCoreApplication.translate("AboutForm", u"XiYang6666", None))
        self.lb_github_link.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"https://github.com/XiYang6666\"><span style=\" text-decoration: underline; color:#007af4;\">https://github.com/XiYang6666</span></a></p></body></html>", None))
        self.lb_mainpage.setText(QCoreApplication.translate("AboutForm", u"\u4e3b\u9875", None))
        self.lb_mainpage_link.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"https://xiyang6666.top/\"><span style=\" text-decoration: underline; color:#007af4;\">https://xiyang6666.top/</span></a></p></body></html>", None))
        self.lb_bilibili.setText(QCoreApplication.translate("AboutForm", u"BiliBili", None))
        self.lb_bilibili_link.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"https://space.bilibili.com/1088981781\"><span style=\" text-decoration: underline; color:#007af4;\">https://space.bilibili.com/1088981781</span></a></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_author), QCoreApplication.translate("AboutForm", u"\u4f5c\u8005", None))
    # retranslateUi

