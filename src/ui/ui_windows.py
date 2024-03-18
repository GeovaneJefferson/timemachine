# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'windows.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(364, 377)
        Form.setStyleSheet(u"background-color: rgb(171, 171, 171);")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_3.addWidget(self.label_7)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(30, 30))
        self.pushButton_3.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
"")

        self.horizontalLayout_3.addWidget(self.pushButton_3, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(6)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color: rgb(91, 91, 91);")
        self.label_4.setWordWrap(True)

        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1, Qt.AlignTop)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color: rgb(25, 25, 25);")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(60, 60))

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(160, 30))
        self.pushButton.setMaximumSize(QSize(160, 30))
        self.pushButton.setStyleSheet(u"color: rgb(26, 26, 26);\n"
"border: 4px;\n"
"background-color:  rgb(250, 250, 250);")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(160, 30))
        self.pushButton_2.setMaximumSize(QSize(160, 30))
        self.pushButton_2.setStyleSheet(u"color: rgb(26, 26, 26);\n"
"border: 4px;\n"
"background-color:  rgb(250, 250, 250);")

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"IMAGE", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"IMAGE", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Google Chrome", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"...", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"x", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"OneSignal announces 500% growth, delivering 2 trillion messages annually.", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"We\u2019re blasting off \ud83d\ude80", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">IMAGE</p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Save Story", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Share", None))
    # retranslateUi

