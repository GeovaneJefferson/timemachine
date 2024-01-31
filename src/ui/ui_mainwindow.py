# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(460, 339)
        MainWindow.setMaximumSize(QSize(460, 16777215))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(18)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setContentsMargins(9, -1, 9, 9)
        self.backups_label = QLabel(self.centralwidget)
        self.backups_label.setObjectName(u"backups_label")
        font = QFont()
        font.setPointSize(9)
        self.backups_label.setFont(font)
        self.backups_label.setStyleSheet(u"color: gray;")

        self.gridLayout.addWidget(self.backups_label, 6, 1, 1, 1)

        self.external_name_label = QLabel(self.centralwidget)
        self.external_name_label.setObjectName(u"external_name_label")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.external_name_label.setFont(font1)
        self.external_name_label.setStyleSheet(u"color: gray;")

        self.gridLayout.addWidget(self.external_name_label, 3, 1, 1, 1)

        self.App_Description = QLabel(self.centralwidget)
        self.App_Description.setObjectName(u"App_Description")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        self.App_Description.setFont(font2)
        self.App_Description.setStyleSheet(u"color: gray;")
        self.App_Description.setScaledContents(True)
        self.App_Description.setWordWrap(True)

        self.gridLayout.addWidget(self.App_Description, 1, 1, 1, 1, Qt.AlignLeft|Qt.AlignTop)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)

        self.next_backup_label = QLabel(self.centralwidget)
        self.next_backup_label.setObjectName(u"next_backup_label")
        self.next_backup_label.setFont(font)
        self.next_backup_label.setStyleSheet(u"color: gray;")

        self.gridLayout.addWidget(self.next_backup_label, 7, 1, 1, 1)

        self.remove_backup_device = QPushButton(self.centralwidget)
        self.remove_backup_device.setObjectName(u"remove_backup_device")
        font3 = QFont()
        font3.setPointSize(10)
        self.remove_backup_device.setFont(font3)
        icon = QIcon()
        iconThemeName = u"list-remove"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.remove_backup_device.setIcon(icon)
        self.remove_backup_device.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.remove_backup_device, 8, 1, 1, 1, Qt.AlignLeft)

        self.progressbar_main_window = QProgressBar(self.centralwidget)
        self.progressbar_main_window.setObjectName(u"progressbar_main_window")
        self.progressbar_main_window.setMaximumSize(QSize(16777215, 16))
        self.progressbar_main_window.setFont(font3)
        self.progressbar_main_window.setMaximum(100)
        self.progressbar_main_window.setValue(0)
        self.progressbar_main_window.setTextVisible(True)

        self.gridLayout.addWidget(self.progressbar_main_window, 5, 1, 1, 1)

        self.App_Title_Name = QLabel(self.centralwidget)
        self.App_Title_Name.setObjectName(u"App_Title_Name")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.App_Title_Name.setFont(font4)

        self.gridLayout.addWidget(self.App_Title_Name, 0, 1, 1, 1, Qt.AlignLeft|Qt.AlignTop)

        self.app_logo_image = QLabel(self.centralwidget)
        self.app_logo_image.setObjectName(u"app_logo_image")

        self.gridLayout.addWidget(self.app_logo_image, 0, 0, 1, 1, Qt.AlignLeft|Qt.AlignTop)

        self.external_size_label = QLabel(self.centralwidget)
        self.external_size_label.setObjectName(u"external_size_label")
        self.external_size_label.setFont(font)
        self.external_size_label.setStyleSheet(u"color: gray;")

        self.gridLayout.addWidget(self.external_size_label, 4, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.update_available_button = QPushButton(self.centralwidget)
        self.update_available_button.setObjectName(u"update_available_button")
        self.update_available_button.setFont(font3)

        self.horizontalLayout.addWidget(self.update_available_button)

        self.select_disk_button = QPushButton(self.centralwidget)
        self.select_disk_button.setObjectName(u"select_disk_button")
        self.select_disk_button.setFont(font3)

        self.horizontalLayout.addWidget(self.select_disk_button)

        self.options_button = QPushButton(self.centralwidget)
        self.options_button.setObjectName(u"options_button")
        self.options_button.setFont(font3)

        self.horizontalLayout.addWidget(self.options_button)

        self.help_button = QPushButton(self.centralwidget)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setMaximumSize(QSize(26, 16777215))
        self.help_button.setFont(font3)

        self.horizontalLayout.addWidget(self.help_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.backups_label.setToolTip(QCoreApplication.translate("MainWindow", u"Oldest - Latest backup", None))
#endif // QT_CONFIG(tooltip)
        self.backups_label.setText(QCoreApplication.translate("MainWindow", u"Backups:", None))
#if QT_CONFIG(tooltip)
        self.external_name_label.setToolTip(QCoreApplication.translate("MainWindow", u"Devices name", None))
#endif // QT_CONFIG(tooltip)
        self.external_name_label.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.App_Description.setText(QCoreApplication.translate("MainWindow", u"Time Machine ensure the safety of your essential files by learning how to set up automatic backups for your PC. Safeguard your personal data, cherished music, precious photos, and vital documents effortlessly. Having a reliable backup system in place grants you the power to recover mistakenly deleted files or access data that might otherwise be out of reach.", None))
        self.label_2.setText("")
#if QT_CONFIG(tooltip)
        self.next_backup_label.setToolTip(QCoreApplication.translate("MainWindow", u"Next backup", None))
#endif // QT_CONFIG(tooltip)
        self.next_backup_label.setText(QCoreApplication.translate("MainWindow", u"Next Backup:", None))
#if QT_CONFIG(tooltip)
        self.remove_backup_device.setToolTip(QCoreApplication.translate("MainWindow", u"Remove a backup disk: Click the Remove button.", None))
#endif // QT_CONFIG(tooltip)
        self.remove_backup_device.setText("")
        self.App_Title_Name.setText(QCoreApplication.translate("MainWindow", u"Time Machine", None))
        self.app_logo_image.setText(QCoreApplication.translate("MainWindow", u"IMAGE", None))
#if QT_CONFIG(tooltip)
        self.external_size_label.setToolTip(QCoreApplication.translate("MainWindow", u"Device space available", None))
#endif // QT_CONFIG(tooltip)
        self.external_size_label.setText(QCoreApplication.translate("MainWindow", u"Space Available:", None))
        self.update_available_button.setText(QCoreApplication.translate("MainWindow", u"Update Available", None))
#if QT_CONFIG(tooltip)
        self.select_disk_button.setToolTip(QCoreApplication.translate("MainWindow", u"If you haven\u2019t set up Time Machine, click Add Backup Disk to set up a backup disk.", None))
#endif // QT_CONFIG(tooltip)
        self.select_disk_button.setText(QCoreApplication.translate("MainWindow", u"Add Backup Disk...", None))
#if QT_CONFIG(tooltip)
        self.options_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.options_button.setText(QCoreApplication.translate("MainWindow", u"Options...", None))
#if QT_CONFIG(tooltip)
        self.help_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.help_button.setText(QCoreApplication.translate("MainWindow", u"?", None))
    # retranslateUi

