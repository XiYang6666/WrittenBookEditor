# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jump_form.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_JumpForm(object):
    def setupUi(self, JumpForm):
        if not JumpForm.objectName():
            JumpForm.setObjectName(u"JumpForm")
        JumpForm.resize(200, 102)
        self.verticalLayout = QVBoxLayout(JumpForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lb_message = QLabel(JumpForm)
        self.lb_message.setObjectName(u"lb_message")
        self.lb_message.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lb_message)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lb_volume = QLabel(JumpForm)
        self.lb_volume.setObjectName(u"lb_volume")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_volume)

        self.lb_page = QLabel(JumpForm)
        self.lb_page.setObjectName(u"lb_page")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_page)

        self.sb_volume = QSpinBox(JumpForm)
        self.sb_volume.setObjectName(u"sb_volume")
        self.sb_volume.setMinimum(1)
        self.sb_volume.setMaximum(1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sb_volume)

        self.sb_page = QSpinBox(JumpForm)
        self.sb_page.setObjectName(u"sb_page")
        self.sb_page.setMinimum(1)
        self.sb_page.setMaximum(1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sb_page)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pbtn_ok = QPushButton(JumpForm)
        self.pbtn_ok.setObjectName(u"pbtn_ok")

        self.horizontalLayout.addWidget(self.pbtn_ok)

        self.pbtn_cancel = QPushButton(JumpForm)
        self.pbtn_cancel.setObjectName(u"pbtn_cancel")

        self.horizontalLayout.addWidget(self.pbtn_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(JumpForm)

        QMetaObject.connectSlotsByName(JumpForm)
    # setupUi

    def retranslateUi(self, JumpForm):
        JumpForm.setWindowTitle(QCoreApplication.translate("JumpForm", u"\u8df3\u8f6c\u5230...", None))
        self.lb_message.setText(QCoreApplication.translate("JumpForm", u"\u8df3\u8f6c\u5230", None))
        self.lb_volume.setText(QCoreApplication.translate("JumpForm", u"\u5377", None))
        self.lb_page.setText(QCoreApplication.translate("JumpForm", u"\u9875", None))
        self.pbtn_ok.setText(QCoreApplication.translate("JumpForm", u"\u786e\u5b9a", None))
        self.pbtn_cancel.setText(QCoreApplication.translate("JumpForm", u"\u53d6\u6d88", None))
    # retranslateUi

