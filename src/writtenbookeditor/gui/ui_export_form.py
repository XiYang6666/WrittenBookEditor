# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_form.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ExportForm(object):
    def setupUi(self, ExportForm):
        if not ExportForm.objectName():
            ExportForm.setObjectName(u"ExportForm")
        ExportForm.resize(250, 310)
        self.verticalLayout_2 = QVBoxLayout(ExportForm)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gb_book_options = QGroupBox(ExportForm)
        self.gb_book_options.setObjectName(u"gb_book_options")
        self.formLayout_2 = QFormLayout(self.gb_book_options)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lb_author = QLabel(self.gb_book_options)
        self.lb_author.setObjectName(u"lb_author")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.lb_author)

        self.le_author = QLineEdit(self.gb_book_options)
        self.le_author.setObjectName(u"le_author")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.le_author)

        self.lb_title = QLabel(self.gb_book_options)
        self.lb_title.setObjectName(u"lb_title")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.lb_title)

        self.le_title = QLineEdit(self.gb_book_options)
        self.le_title.setObjectName(u"le_title")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.le_title)


        self.verticalLayout_2.addWidget(self.gb_book_options)

        self.gb_export_options = QGroupBox(ExportForm)
        self.gb_export_options.setObjectName(u"gb_export_options")
        self.formLayout_3 = QFormLayout(self.gb_export_options)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.lb_item_type = QLabel(self.gb_export_options)
        self.lb_item_type.setObjectName(u"lb_item_type")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.lb_item_type)

        self.cmb_item_type = QComboBox(self.gb_export_options)
        self.cmb_item_type.addItem("")
        self.cmb_item_type.addItem("")
        self.cmb_item_type.setObjectName(u"cmb_item_type")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.cmb_item_type)

        self.lb_file_type = QLabel(self.gb_export_options)
        self.lb_file_type.setObjectName(u"lb_file_type")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.lb_file_type)

        self.cmb_file_type = QComboBox(self.gb_export_options)
        self.cmb_file_type.addItem("")
        self.cmb_file_type.addItem("")
        self.cmb_file_type.addItem("")
        self.cmb_file_type.setObjectName(u"cmb_file_type")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.cmb_file_type)

        self.lb_command_version = QLabel(self.gb_export_options)
        self.lb_command_version.setObjectName(u"lb_command_version")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.lb_command_version)

        self.cmb_command_version = QComboBox(self.gb_export_options)
        self.cmb_command_version.addItem("")
        self.cmb_command_version.addItem("")
        self.cmb_command_version.setObjectName(u"cmb_command_version")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.cmb_command_version)


        self.verticalLayout_2.addWidget(self.gb_export_options)

        self.gb_extra_options = QGroupBox(ExportForm)
        self.gb_extra_options.setObjectName(u"gb_extra_options")
        self.verticalLayout = QVBoxLayout(self.gb_extra_options)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.chk_text_component = QCheckBox(self.gb_extra_options)
        self.chk_text_component.setObjectName(u"chk_text_component")
        self.chk_text_component.setChecked(True)

        self.verticalLayout.addWidget(self.chk_text_component)

        self.chk_filter = QCheckBox(self.gb_extra_options)
        self.chk_filter.setObjectName(u"chk_filter")

        self.verticalLayout.addWidget(self.chk_filter)


        self.verticalLayout_2.addWidget(self.gb_extra_options)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_0 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_0)

        self.pbtn_export = QPushButton(ExportForm)
        self.pbtn_export.setObjectName(u"pbtn_export")

        self.horizontalLayout.addWidget(self.pbtn_export)

        self.horizontalSpacer_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_1)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ExportForm)

        QMetaObject.connectSlotsByName(ExportForm)
    # setupUi

    def retranslateUi(self, ExportForm):
        ExportForm.setWindowTitle(QCoreApplication.translate("ExportForm", u"\u5bfc\u51fa...", None))
        self.gb_book_options.setTitle(QCoreApplication.translate("ExportForm", u"\u4e66\u7c4d\u4fe1\u606f", None))
        self.lb_author.setText(QCoreApplication.translate("ExportForm", u"\u4f5c\u8005", None))
        self.le_author.setText(QCoreApplication.translate("ExportForm", u"XiYang6666/WrittenBookEditor", None))
        self.lb_title.setText(QCoreApplication.translate("ExportForm", u"\u6807\u9898", None))
#if QT_CONFIG(tooltip)
        self.le_title.setToolTip(QCoreApplication.translate("ExportForm", u"\u4f7f\u7528{volume}\u5360\u4f4d\u7b26\u53ef\u4ee5\u5728\u4e66\u540d\u4e2d\u6dfb\u52a0\u5377\u53f7", None))
#endif // QT_CONFIG(tooltip)
        self.le_title.setText("")
        self.gb_export_options.setTitle(QCoreApplication.translate("ExportForm", u"\u5bfc\u51fa\u9009\u9879", None))
        self.lb_item_type.setText(QCoreApplication.translate("ExportForm", u"\u7269\u54c1\u7c7b\u578b", None))
        self.cmb_item_type.setItemText(0, QCoreApplication.translate("ExportForm", u"\u6210\u4e66", None))
        self.cmb_item_type.setItemText(1, QCoreApplication.translate("ExportForm", u"\u6f5c\u5f71\u76d2", None))

        self.lb_file_type.setText(QCoreApplication.translate("ExportForm", u"\u6587\u4ef6\u7c7b\u578b", None))
        self.cmb_file_type.setItemText(0, QCoreApplication.translate("ExportForm", u"\u6307\u4ee4\u7eaf\u6587\u672c", None))
        self.cmb_file_type.setItemText(1, QCoreApplication.translate("ExportForm", u"mc \u51fd\u6570\u6587\u4ef6", None))
        self.cmb_file_type.setItemText(2, QCoreApplication.translate("ExportForm", u"\u6570\u636e\u5305", None))

        self.lb_command_version.setText(QCoreApplication.translate("ExportForm", u"\u6307\u4ee4\u7248\u672c", None))
        self.cmb_command_version.setItemText(0, QCoreApplication.translate("ExportForm", u">=1.13 <1.20.5", None))
        self.cmb_command_version.setItemText(1, QCoreApplication.translate("ExportForm", u">=1.20.5", None))

#if QT_CONFIG(tooltip)
        self.gb_extra_options.setToolTip(QCoreApplication.translate("ExportForm", u"\u5982\u679c\u4f60\u4e0d\u77e5\u9053\u8fd9\u4e9b\u914d\u7f6e\u7684\u542b\u4e49\u8bf7\u4e0d\u8981\u968f\u610f\u4fee\u6539", None))
#endif // QT_CONFIG(tooltip)
        self.gb_extra_options.setTitle(QCoreApplication.translate("ExportForm", u"\u989d\u5916\u9009\u9879", None))
        self.chk_text_component.setText(QCoreApplication.translate("ExportForm", u"\u4f7f\u7528\u6587\u672c\u7ec4\u4ef6", None))
        self.chk_filter.setText(QCoreApplication.translate("ExportForm", u"\u4f7f\u7528\u8fc7\u6ee4", None))
        self.pbtn_export.setText(QCoreApplication.translate("ExportForm", u"\u5bfc\u51fa", None))
    # retranslateUi

