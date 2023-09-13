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
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.app_logo_image = QLabel(self.widget_2)
        self.app_logo_image.setObjectName(u"app_logo_image")
        self.app_logo_image.setMinimumSize(QSize(128, 128))
        self.app_logo_image.setMaximumSize(QSize(128, 128))

        self.verticalLayout_2.addWidget(self.app_logo_image, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.automatically_backup_checkbox = QCheckBox(self.widget_2)
        self.automatically_backup_checkbox.setObjectName(u"automatically_backup_checkbox")

        self.verticalLayout_2.addWidget(self.automatically_backup_checkbox, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.update_available_button = QPushButton(self.widget_2)
        self.update_available_button.setObjectName(u"update_available_button")

        self.verticalLayout_2.addWidget(self.update_available_button, 0, Qt.AlignHCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.horizontalLayout.addWidget(self.widget_2)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setStyleSheet(u"color: rgb(128, 128, 128);")
        self.line_3.setLineWidth(1)
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayoutWidget_3 = QWidget(self.widget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(0, 50, 451, 111))
        self.horizontalLayout_7 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_7.setSpacing(20)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(20, 0, 6, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, -1, 0, -1)
        self.app_disk_image = QLabel(self.horizontalLayoutWidget_3)
        self.app_disk_image.setObjectName(u"app_disk_image")
        self.app_disk_image.setMinimumSize(QSize(64, 64))
        self.app_disk_image.setMaximumSize(QSize(64, 64))

        self.verticalLayout_7.addWidget(self.app_disk_image, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.select_disk_button = QPushButton(self.horizontalLayoutWidget_3)
        self.select_disk_button.setObjectName(u"select_disk_button")
        sizePolicy.setHeightForWidth(self.select_disk_button.sizePolicy().hasHeightForWidth())
        self.select_disk_button.setSizePolicy(sizePolicy)

        self.verticalLayout_7.addWidget(self.select_disk_button, 0, Qt.AlignHCenter)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.external_name_label = QLabel(self.horizontalLayoutWidget_3)
        self.external_name_label.setObjectName(u"external_name_label")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.external_name_label.setFont(font1)

        self.verticalLayout_8.addWidget(self.external_name_label)

        self.external_size_label = QLabel(self.horizontalLayoutWidget_3)
        self.external_size_label.setObjectName(u"external_size_label")
        self.external_size_label.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_8.addWidget(self.external_size_label)

        self.oldest_backup_label = QLabel(self.horizontalLayoutWidget_3)
        self.oldest_backup_label.setObjectName(u"oldest_backup_label")
        self.oldest_backup_label.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_8.addWidget(self.oldest_backup_label)

        self.latest_backup_label = QLabel(self.horizontalLayoutWidget_3)
        self.latest_backup_label.setObjectName(u"latest_backup_label")
        self.latest_backup_label.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_8.addWidget(self.latest_backup_label)

        self.next_backup_label = QLabel(self.horizontalLayoutWidget_3)
        self.next_backup_label.setObjectName(u"next_backup_label")
        self.next_backup_label.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_8.addWidget(self.next_backup_label)

        self.backing_up_label = QLabel(self.horizontalLayoutWidget_3)
        self.backing_up_label.setObjectName(u"backing_up_label")
        self.backing_up_label.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_8.addWidget(self.backing_up_label)


        self.horizontalLayout_7.addLayout(self.verticalLayout_8)

        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayoutWidget = QWidget(self.widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 410, 421, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.show_in_system_tray_checkbox = QCheckBox(self.horizontalLayoutWidget)
        self.show_in_system_tray_checkbox.setObjectName(u"show_in_system_tray_checkbox")
        font2 = QFont()
        font2.setPointSize(10)
        self.show_in_system_tray_checkbox.setFont(font2)

        self.horizontalLayout_3.addWidget(self.show_in_system_tray_checkbox)

        self.options_button = QPushButton(self.horizontalLayoutWidget)
        self.options_button.setObjectName(u"options_button")
        sizePolicy.setHeightForWidth(self.options_button.sizePolicy().hasHeightForWidth())
        self.options_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.options_button)

        self.help_button = QPushButton(self.horizontalLayoutWidget)
        self.help_button.setObjectName(u"help_button")
        sizePolicy.setHeightForWidth(self.help_button.sizePolicy().hasHeightForWidth())
        self.help_button.setSizePolicy(sizePolicy)
        self.help_button.setMinimumSize(QSize(24, 24))
        self.help_button.setMaximumSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.help_button)

        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 190, 421, 166))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)
        self.label_9.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_3.addWidget(self.label_9)

        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font2)
        self.label_10.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_3.addWidget(self.label_10)

        self.label_11 = QLabel(self.verticalLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font2)
        self.label_11.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_3.addWidget(self.label_11)

        self.label_12 = QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font2)
        self.label_12.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_3.addWidget(self.label_12)

        self.label_15 = QLabel(self.verticalLayoutWidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font2)
        self.label_15.setStyleSheet(u"color: rgb(128, 128, 128);")

        self.verticalLayout_3.addWidget(self.label_15)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(5, 1)
        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 20, 441, 20))
        self.line.setStyleSheet(u"color: rgb(128, 128, 128);")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self.widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(10, 170, 441, 20))
        self.line_2.setStyleSheet(u"color: rgb(128, 128, 128);")
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
        self.app_logo_image.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">IMAGE</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Time Machine", None))
        self.automatically_backup_checkbox.setText(QCoreApplication.translate("MainWindow", u"Back Up Automatically", None))
        self.update_available_button.setText(QCoreApplication.translate("MainWindow", u"Update Available", None))
#if QT_CONFIG(whatsthis)
        self.app_disk_image.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">IMAGE</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.app_disk_image.setText(QCoreApplication.translate("MainWindow", u"IMAGE", None))
        self.select_disk_button.setText(QCoreApplication.translate("MainWindow", u"Select Disk...", None))
        self.external_name_label.setText(QCoreApplication.translate("MainWindow", u"Backup_Drive", None))
        self.external_size_label.setText(QCoreApplication.translate("MainWindow", u"No information available", None))
        self.oldest_backup_label.setText(QCoreApplication.translate("MainWindow", u"Oldest Backup:", None))
        self.latest_backup_label.setText(QCoreApplication.translate("MainWindow", u"Latest Backup:", None))
        self.next_backup_label.setText(QCoreApplication.translate("MainWindow", u"Next Backup:", None))
        self.backing_up_label.setText(QCoreApplication.translate("MainWindow", u"Backing up:", None))
        self.show_in_system_tray_checkbox.setText(QCoreApplication.translate("MainWindow", u"Show Time Machine in system tray", None))
        self.options_button.setText(QCoreApplication.translate("MainWindow", u"Options...", None))
        self.help_button.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"How Time Machine works:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u2022 Choose which folders to back up from HOME.", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u2022 Hourly, Daily or Weekly backups.", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u2022 Packages such as .DEB, and .RPM that are stored in the \n"
"   Downloads folder, wiil be backed up.", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u2022 Installed flatpaks and their data can also be backed up.", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"The oldest backups are deleted when your disk becomes full.", None))
    # retranslateUi

