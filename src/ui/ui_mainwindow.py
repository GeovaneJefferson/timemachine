# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 450)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(660, 450))
        MainWindow.setMaximumSize(QSize(700, 450))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(220, 0))
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(128, 128))
        self.label_2.setMaximumSize(QSize(128, 128))

        self.verticalLayout_2.addWidget(self.label_2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.checkBox = QCheckBox(self.widget_2)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_2.addWidget(self.checkBox, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.horizontalLayout.addWidget(self.widget_2)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayoutWidget_3 = QWidget(self.widget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(0, 50, 451, 98))
        self.horizontalLayout_7 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_7.setSpacing(20)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(20, 0, 6, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, -1, 0, -1)
        self.label_17 = QLabel(self.horizontalLayoutWidget_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(64, 64))
        self.label_17.setMaximumSize(QSize(64, 64))

        self.verticalLayout_7.addWidget(self.label_17, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.select_disk_button = QPushButton(self.horizontalLayoutWidget_3)
        self.select_disk_button.setObjectName(u"select_disk_button")
        sizePolicy.setHeightForWidth(self.select_disk_button.sizePolicy().hasHeightForWidth())
        self.select_disk_button.setSizePolicy(sizePolicy)

        self.verticalLayout_7.addWidget(self.select_disk_button, 0, Qt.AlignHCenter)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_4 = QLabel(self.horizontalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.label_4.setFont(font1)

        self.verticalLayout_8.addWidget(self.label_4)

        self.label_5 = QLabel(self.horizontalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_8.addWidget(self.label_5)

        self.label_6 = QLabel(self.horizontalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_8.addWidget(self.label_6)

        self.label_7 = QLabel(self.horizontalLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_8.addWidget(self.label_7)

        self.label_8 = QLabel(self.horizontalLayoutWidget_3)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_8.addWidget(self.label_8)


        self.horizontalLayout_7.addLayout(self.verticalLayout_8)

        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayoutWidget = QWidget(self.widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 410, 441, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.checkBox_2 = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_3.addWidget(self.checkBox_2)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QSize(24, 24))
        self.pushButton_3.setMaximumSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 190, 441, 166))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_3.addWidget(self.label_9)

        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_3.addWidget(self.label_10)

        self.label_11 = QLabel(self.verticalLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_3.addWidget(self.label_11)

        self.label_12 = QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_3.addWidget(self.label_12)

        self.label_13 = QLabel(self.verticalLayoutWidget)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_3.addWidget(self.label_13)

        self.label_15 = QLabel(self.verticalLayoutWidget)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_3.addWidget(self.label_15)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(6, 1)
        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 20, 441, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self.widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(10, 160, 441, 20))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.widget)

        self.horizontalLayout.setStretch(2, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">IMAGE</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Time Machine", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Back Up Automatically", None))
#if QT_CONFIG(whatsthis)
        self.label_17.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">IMAGE</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"IMAGE", None))
        self.select_disk_button.setText(QCoreApplication.translate("MainWindow", u"   Select Disk...   ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Backup_Drive", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Space", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Oldest Backup:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Latest Backup:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Next Backup:", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Show Time Machine in system tray", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Options...", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"How Time Machine works:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u2022 Choose which folders to back up from HOME.", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u2022 Hourly, Daily or Weekly backups.", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u2022 Packages such as .DEB, and .RPM that are stored in the \n"
"   Downloads folder, wiil be backed up.", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u2022 Installed flatpaks and their data are also backed up.", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u2022 Installed flatpaks and their data are also backed up.", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"The oldest backups are deleted when your disk becomes full.", None))
    # retranslateUi

