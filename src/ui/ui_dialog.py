# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 360)
        Dialog.setMinimumSize(QSize(500, 360))
        Dialog.setMaximumSize(QSize(500, 360))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 480, 303))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_4.addWidget(self.label)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_4.addWidget(self.label_2)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.available_disk_dialog_layout = QVBoxLayout()
        self.available_disk_dialog_layout.setObjectName(u"available_disk_dialog_layout")

        self.verticalLayout_4.addLayout(self.available_disk_dialog_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_button_dialog = QPushButton(Dialog)
        self.cancel_button_dialog.setObjectName(u"cancel_button_dialog")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_button_dialog.sizePolicy().hasHeightForWidth())
        self.cancel_button_dialog.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setKerning(True)
        self.cancel_button_dialog.setFont(font2)

        self.horizontalLayout.addWidget(self.cancel_button_dialog, 0, Qt.AlignRight)

        self.use_disk_button_dialog = QPushButton(Dialog)
        self.use_disk_button_dialog.setObjectName(u"use_disk_button_dialog")
        sizePolicy.setHeightForWidth(self.use_disk_button_dialog.sizePolicy().hasHeightForWidth())
        self.use_disk_button_dialog.setSizePolicy(sizePolicy)
        self.use_disk_button_dialog.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")

        self.horizontalLayout.addWidget(self.use_disk_button_dialog, 0, Qt.AlignRight)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Choose a device", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Backup your Home with a local device.", None))
        self.cancel_button_dialog.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.use_disk_button_dialog.setText(QCoreApplication.translate("Dialog", u"Use Disk", None))
    # retranslateUi

