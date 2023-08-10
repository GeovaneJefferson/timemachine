# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1465, 796)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(1200, 680))
        self.widget.setMaximumSize(QSize(800, 550))
        self.widget.setStyleSheet(u"background-color:gray;\n"
"border-radius:20px;")
        self.horizontalLayout_5 = QHBoxLayout(self.widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(180, 0))
        self.widget_3.setMaximumSize(QSize(180, 16777215))
        self.widget_3.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"\n"
"border-top-left-radius: 20px 20px;\n"
"border-top-right-radius: 0px 0px;\n"
"border-bottom-right-radius: 0px 0px;\n"
"border-bottom-left-radius: 20px 20px;\n"
"\n"
"border-right: 2px solid gray;")
        self.verticalLayout_10 = QVBoxLayout(self.widget_3)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.folders_layout = QVBoxLayout()
        self.folders_layout.setObjectName(u"folders_layout")

        self.verticalLayout_10.addLayout(self.folders_layout)


        self.horizontalLayout_4.addWidget(self.widget_3, 0, Qt.AlignHCenter)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"background-color: white;\n"
"\n"
"border-top-right-radius: 20px 20px;\n"
"border-top-left-radius: 0px 0px;\n"
"border-bottom-right-radius: 20px 20px;\n"
"border-bottom-left-radius: 0px 0px;")
        self.gridLayout_7 = QGridLayout(self.widget_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.scrollArea = QScrollArea(self.widget_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.results_scroll_grid = QWidget()
        self.results_scroll_grid.setObjectName(u"results_scroll_grid")
        self.results_scroll_grid.setGeometry(QRect(0, 0, 982, 642))
        self.gridLayout_2 = QGridLayout(self.results_scroll_grid)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.results_layout_grid = QGridLayout()
        self.results_layout_grid.setObjectName(u"results_layout_grid")

        self.gridLayout_2.addLayout(self.results_layout_grid, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.results_scroll_grid)

        self.gridLayout_7.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.widget_2)

        self.horizontalLayout_4.setStretch(1, 1)

        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.widget, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        self.pushButton_2.setMinimumSize(QSize(140, 34))
        self.pushButton_2.setMaximumSize(QSize(140, 34))
        font = QFont()
        font.setFamilies([u"Open Sans Medium"])
        font.setPointSize(12)
        font.setBold(False)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(u"PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
"    color: black;\n"
"    background: rgba(255, 255, 255, 0.7);\n"
"    border: 1px solid rgba(0, 0, 0, 0.073);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"    border-radius: 5px;\n"
"    /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */\n"
"    padding: 5px 12px 6px 12px;\n"
"    outline: none;\n"
"}")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.btn_restore = QPushButton(self.centralwidget)
        self.btn_restore.setObjectName(u"btn_restore")
        sizePolicy1.setHeightForWidth(self.btn_restore.sizePolicy().hasHeightForWidth())
        self.btn_restore.setSizePolicy(sizePolicy1)
        self.btn_restore.setMinimumSize(QSize(140, 34))
        self.btn_restore.setMaximumSize(QSize(140, 34))
        font1 = QFont()
        font1.setPointSize(12)
        self.btn_restore.setFont(font1)
        self.btn_restore.setStyleSheet(u"PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
"    color: black;\n"
"    background: rgba(255, 255, 255, 0.7);\n"
"    border: 1px solid rgba(0, 0, 0, 0.073);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"    border-radius: 5px;\n"
"    /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */\n"
"    padding: 5px 12px 6px 12px;\n"
"    outline: none;\n"
"}")

        self.horizontalLayout_2.addWidget(self.btn_restore)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.btn_up = QPushButton(self.centralwidget)
        self.btn_up.setObjectName(u"btn_up")
        self.btn_up.setMinimumSize(QSize(38, 38))
        self.btn_up.setMaximumSize(QSize(38, 38))
        font2 = QFont()
        font2.setBold(True)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        self.btn_up.setFont(font2)
        self.btn_up.setStyleSheet(u"QPushButton\n"
" {\n"
"	color: black;\n"
"	background: rgba(255, 255, 255, 0.7);\n"
"	border: 1px solid rgba(0, 0, 0, 0.073);\n"
"	border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"	border-radius: 5px;\n"
"	padding: 5px 12px 6px 12px;\n"
"	outline: none;\n"
"	font-size: 8px;\n"
"}\n"
"                    \n"
" QPushButton:hover \n"
"{\n"
"	font-size: 12px;\n"
"	background: rgba(249, 249, 249, 0.5);\n"
"}\n"
" QPushButton:disabled \n"
" {\n"
"	color: rgba(0, 0, 0, 0.36);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border: 1px solid rgba(0, 0, 0, 0.06);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
" }\n"
" QPushButton:pressed \n"
" {\n"
"    color: rgba(0, 0, 0, 0.63);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
" }")

        self.verticalLayout_4.addWidget(self.btn_up, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label_gray_time = QLabel(self.centralwidget)
        self.label_gray_time.setObjectName(u"label_gray_time")
        self.label_gray_time.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.label_gray_time, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.btn_down = QPushButton(self.centralwidget)
        self.btn_down.setObjectName(u"btn_down")
        self.btn_down.setMinimumSize(QSize(38, 38))
        self.btn_down.setMaximumSize(QSize(38, 38))
        font3 = QFont()
        font3.setBold(True)
        self.btn_down.setFont(font3)
        self.btn_down.setStyleSheet(u"QPushButton\n"
" {\n"
"	color: black;\n"
"	background: rgba(255, 255, 255, 0.7);\n"
"	border: 1px solid rgba(0, 0, 0, 0.073);\n"
"	border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"	border-radius: 5px;\n"
"	padding: 5px 12px 6px 12px;\n"
"	outline: none;\n"
"	font-size: 8px;\n"
"}\n"
"                    \n"
" QPushButton:hover \n"
"{\n"
"	font-size: 12px;\n"
"	background: rgba(249, 249, 249, 0.5);\n"
"}\n"
" QPushButton:disabled \n"
" {\n"
"	color: rgba(0, 0, 0, 0.36);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border: 1px solid rgba(0, 0, 0, 0.06);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
" }\n"
" QPushButton:pressed \n"
" {\n"
"    color: rgba(0, 0, 0, 0.63);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
" }")

        self.verticalLayout_4.addWidget(self.btn_down, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.dates_layout = QVBoxLayout()
        self.dates_layout.setSpacing(20)
        self.dates_layout.setObjectName(u"dates_layout")

        self.horizontalLayout.addLayout(self.dates_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"   Cancel   ", None))
        self.btn_restore.setText(QCoreApplication.translate("MainWindow", u"   Restore   ", None))
        self.btn_up.setText(QCoreApplication.translate("MainWindow", u"\ufe3f", None))
        self.label_gray_time.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.btn_down.setText(QCoreApplication.translate("MainWindow", u"\ufe40", None))
    # retranslateUi

