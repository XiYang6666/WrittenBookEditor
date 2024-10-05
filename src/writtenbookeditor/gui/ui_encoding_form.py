# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'encoding_form.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_EncodingForm(object):
    def setupUi(self, EncodingForm):
        if not EncodingForm.objectName():
            EncodingForm.setObjectName(u"EncodingForm")
        EncodingForm.resize(200, 100)
        self.verticalLayout = QVBoxLayout(EncodingForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(EncodingForm)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_0 = QLabel(EncodingForm)
        self.label_0.setObjectName(u"label_0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_0)

        self.cmb_encoding = QComboBox(EncodingForm)
        self.cmb_encoding.addItem("")
        self.cmb_encoding.addItem("")
        self.cmb_encoding.addItem("")
        self.cmb_encoding.addItem("")
        self.cmb_encoding.setObjectName(u"cmb_encoding")
        self.cmb_encoding.setEditable(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cmb_encoding)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pbtn_ok = QPushButton(EncodingForm)
        self.pbtn_ok.setObjectName(u"pbtn_ok")

        self.horizontalLayout.addWidget(self.pbtn_ok)

        self.pbtn_cancel = QPushButton(EncodingForm)
        self.pbtn_cancel.setObjectName(u"pbtn_cancel")

        self.horizontalLayout.addWidget(self.pbtn_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(EncodingForm)

        QMetaObject.connectSlotsByName(EncodingForm)
    # setupUi

    def retranslateUi(self, EncodingForm):
        EncodingForm.setWindowTitle(QCoreApplication.translate("EncodingForm", u"\u8bbe\u7f6e\u7f16\u7801\u683c\u5f0f", None))
        self.label.setText(QCoreApplication.translate("EncodingForm", u"\u65e0\u6cd5\u6253\u5f00\u6587\u4ef6, \u6b63\u786e\u7684\u7f16\u7801\u683c\u5f0f.", None))
        self.label_0.setText(QCoreApplication.translate("EncodingForm", u"\u7f16\u7801\u683c\u5f0f", None))
        self.cmb_encoding.setItemText(0, QCoreApplication.translate("EncodingForm", u"\u81ea\u52a8\u8bc6\u522b", None))
        self.cmb_encoding.setItemText(1, QCoreApplication.translate("EncodingForm", u"UTF-8", None))
        self.cmb_encoding.setItemText(2, QCoreApplication.translate("EncodingForm", u"GBK", None))
        self.cmb_encoding.setItemText(3, QCoreApplication.translate("EncodingForm", u"BIG5", None))

        self.pbtn_ok.setText(QCoreApplication.translate("EncodingForm", u"\u786e\u5b9a", None))
        self.pbtn_cancel.setText(QCoreApplication.translate("EncodingForm", u"\u53d6\u6d88", None))
    # retranslateUi

