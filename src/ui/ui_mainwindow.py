# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(618, 312)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.WinPanel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.app_logo_image = QLabel(self.frame)
        self.app_logo_image.setObjectName(u"app_logo_image")

        self.horizontalLayout.addWidget(self.app_logo_image, 0, Qt.AlignTop)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label, 0, Qt.AlignTop)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.label_2.setFont(font1)
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_2, 0, Qt.AlignTop)

        self.verticalLayout_3.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame)

        self.backup_device_informations = QFrame(self.centralwidget)
        self.backup_device_informations.setObjectName(u"backup_device_informations")
        self.backup_device_informations.setMinimumSize(QSize(600, 120))
        self.backup_device_informations.setMaximumSize(QSize(600, 120))
        self.backup_device_informations.setFrameShape(QFrame.StyledPanel)
        self.backup_device_informations.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.backup_device_informations)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, 6, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_3 = QPushButton(self.backup_device_informations)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(32, 32))
        self.pushButton_3.setMaximumSize(QSize(32, 32))
        icon = QIcon()
        iconThemeName = u"drive-removable-media"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QSize(32, 32))
        self.pushButton_3.setFlat(True)

        self.horizontalLayout_3.addWidget(self.pushButton_3, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.external_name_label = QLabel(self.backup_device_informations)
        self.external_name_label.setObjectName(u"external_name_label")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        font2.setKerning(True)
        self.external_name_label.setFont(font2)

        self.verticalLayout_2.addWidget(self.external_name_label)

        self.external_size_label = QLabel(self.backup_device_informations)
        self.external_size_label.setObjectName(u"external_size_label")
        font3 = QFont()
        font3.setPointSize(10)
        self.external_size_label.setFont(font3)

        self.verticalLayout_2.addWidget(self.external_size_label)

        self.progressbar_main_window = QProgressBar(self.backup_device_informations)
        self.progressbar_main_window.setObjectName(u"progressbar_main_window")
        self.progressbar_main_window.setMaximumSize(QSize(16777215, 16))
        self.progressbar_main_window.setFont(font3)
        self.progressbar_main_window.setMaximum(100)
        self.progressbar_main_window.setValue(0)
        self.progressbar_main_window.setTextVisible(True)

        self.verticalLayout_2.addWidget(self.progressbar_main_window)

        self.backups_label = QLabel(self.backup_device_informations)
        self.backups_label.setObjectName(u"backups_label")
        self.backups_label.setFont(font3)

        self.verticalLayout_2.addWidget(self.backups_label)

        self.next_backup_label = QLabel(self.backup_device_informations)
        self.next_backup_label.setObjectName(u"next_backup_label")
        self.next_backup_label.setFont(font3)

        self.verticalLayout_2.addWidget(self.next_backup_label)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.remove_backup_device = QPushButton(self.backup_device_informations)
        self.remove_backup_device.setObjectName(u"remove_backup_device")
        icon1 = QIcon()
        iconThemeName = u"list-remove"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.remove_backup_device.setIcon(icon1)
        self.remove_backup_device.setIconSize(QSize(16, 16))

        self.horizontalLayout_7.addWidget(self.remove_backup_device, 0, Qt.AlignLeft)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3.setStretch(1, 1)

        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.backup_device_informations)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.bottom_settings = QFrame(self.centralwidget)
        self.bottom_settings.setObjectName(u"bottom_settings")
        self.bottom_settings.setMinimumSize(QSize(600, 45))
        self.bottom_settings.setMaximumSize(QSize(600, 45))
        self.bottom_settings.setFrameShape(QFrame.NoFrame)
        self.bottom_settings.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottom_settings)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.update_available_button = QPushButton(self.bottom_settings)
        self.update_available_button.setObjectName(u"update_available_button")
        font4 = QFont()
        font4.setPointSize(9)
        self.update_available_button.setFont(font4)

        self.horizontalLayout_4.addWidget(self.update_available_button)

        self.select_disk_button = QPushButton(self.bottom_settings)
        self.select_disk_button.setObjectName(u"select_disk_button")
        self.select_disk_button.setFont(font4)

        self.horizontalLayout_4.addWidget(self.select_disk_button)

        self.options_button = QPushButton(self.bottom_settings)
        self.options_button.setObjectName(u"options_button")
        self.options_button.setFont(font4)

        self.horizontalLayout_4.addWidget(self.options_button)

        self.help_button = QPushButton(self.bottom_settings)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setMaximumSize(QSize(26, 16777215))
        self.help_button.setFont(font4)

        self.horizontalLayout_4.addWidget(self.help_button)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.bottom_settings)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.app_logo_image.setText(QCoreApplication.translate("MainWindow", u"IMAGE", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Time Machine", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Time Machine ensure the safety of your essential files by learning how to set up automatic backups for your PC. Safeguard your personal data, cherished music, precious photos, and vital documents effortlessly. Having a reliable backup system in place grants you the power to recover mistakenly deleted files or access data that might otherwise be out of reach.", None))
        self.pushButton_3.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_3.setShortcut(QCoreApplication.translate("MainWindow", u"Enter", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.external_name_label.setToolTip(QCoreApplication.translate("MainWindow", u"Devices name", None))
#endif // QT_CONFIG(tooltip)
        self.external_name_label.setText(QCoreApplication.translate("MainWindow", u"None", None))
#if QT_CONFIG(tooltip)
        self.external_size_label.setToolTip(QCoreApplication.translate("MainWindow", u"Device space available", None))
#endif // QT_CONFIG(tooltip)
        self.external_size_label.setText(QCoreApplication.translate("MainWindow", u"Space Available:", None))
#if QT_CONFIG(tooltip)
        self.backups_label.setToolTip(QCoreApplication.translate("MainWindow", u"Oldest - Latest backup", None))
#endif // QT_CONFIG(tooltip)
        self.backups_label.setText(QCoreApplication.translate("MainWindow", u"Backups:", None))
#if QT_CONFIG(tooltip)
        self.next_backup_label.setToolTip(QCoreApplication.translate("MainWindow", u"Next backup", None))
#endif // QT_CONFIG(tooltip)
        self.next_backup_label.setText(QCoreApplication.translate("MainWindow", u"Next Backup:", None))
#if QT_CONFIG(tooltip)
        self.remove_backup_device.setToolTip(QCoreApplication.translate("MainWindow", u"Remove this backup device", None))
#endif // QT_CONFIG(tooltip)
        self.remove_backup_device.setText("")
        self.update_available_button.setText(QCoreApplication.translate("MainWindow", u"Update Available", None))
#if QT_CONFIG(tooltip)
        self.select_disk_button.setToolTip(QCoreApplication.translate("MainWindow", u"Add a backup device", None))
#endif // QT_CONFIG(tooltip)
        self.select_disk_button.setText(QCoreApplication.translate("MainWindow", u"Add Backup Disk...", None))
#if QT_CONFIG(tooltip)
        self.options_button.setToolTip(QCoreApplication.translate("MainWindow", u"Options", None))
#endif // QT_CONFIG(tooltip)
        self.options_button.setText(QCoreApplication.translate("MainWindow", u"Options...", None))
#if QT_CONFIG(tooltip)
        self.help_button.setToolTip(QCoreApplication.translate("MainWindow", u"Help", None))
#endif // QT_CONFIG(tooltip)
        self.help_button.setText(QCoreApplication.translate("MainWindow", u"?", None))
    # retranslateUi

