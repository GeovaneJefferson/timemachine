# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow_new.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 200)
        MainWindow.setMaximumSize(QSize(480, 200))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.external_name_label = QLabel(self.centralwidget)
        self.external_name_label.setObjectName(u"external_name_label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.external_name_label.setFont(font)
        self.external_name_label.setStyleSheet(u"color: gray;")

        self.gridLayout.addWidget(self.external_name_label, 0, 1, 1, 1)

        self.progressbar_main_window = QProgressBar(self.centralwidget)
        self.progressbar_main_window.setObjectName(u"progressbar_main_window")
        self.progressbar_main_window.setMaximumSize(QSize(16777215, 16))
        font1 = QFont()
        font1.setPointSize(10)
        self.progressbar_main_window.setFont(font1)
        self.progressbar_main_window.setMaximum(100)
        self.progressbar_main_window.setValue(0)
        self.progressbar_main_window.setTextVisible(True)

        self.gridLayout.addWidget(self.progressbar_main_window, 7, 1, 1, 1)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 6, 1, 1, 1)

        self.last_backup_label = QLabel(self.centralwidget)
        self.last_backup_label.setObjectName(u"last_backup_label")

        self.gridLayout.addWidget(self.last_backup_label, 3, 1, 1, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 2, 1, 1, 1)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 4, 1, 1, 1)

        self.app_logo_image = QLabel(self.centralwidget)
        self.app_logo_image.setObjectName(u"app_logo_image")

        self.gridLayout.addWidget(self.app_logo_image, 0, 0, 1, 1)

        self.next_backup_label = QLabel(self.centralwidget)
        self.next_backup_label.setObjectName(u"next_backup_label")

        self.gridLayout.addWidget(self.next_backup_label, 5, 1, 1, 1)

        self.external_size_label = QLabel(self.centralwidget)
        self.external_size_label.setObjectName(u"external_size_label")

        self.gridLayout.addWidget(self.external_size_label, 1, 1, 1, 1)

        self.remove_backup_device = QPushButton(self.centralwidget)
        self.remove_backup_device.setObjectName(u"remove_backup_device")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_backup_device.sizePolicy().hasHeightForWidth())
        self.remove_backup_device.setSizePolicy(sizePolicy)
        self.remove_backup_device.setMaximumSize(QSize(26, 16777215))

        self.gridLayout.addWidget(self.remove_backup_device, 0, 2, 1, 1, Qt.AlignRight|Qt.AlignVCenter)

        self.gridLayout.setColumnStretch(1, 1)

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
        self.update_available_button.setFont(font1)
        self.update_available_button.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")

        self.horizontalLayout.addWidget(self.update_available_button)

        self.select_disk_button = QPushButton(self.centralwidget)
        self.select_disk_button.setObjectName(u"select_disk_button")

        self.horizontalLayout.addWidget(self.select_disk_button)

        self.options_button = QPushButton(self.centralwidget)
        self.options_button.setObjectName(u"options_button")
        self.options_button.setFont(font1)

        self.horizontalLayout.addWidget(self.options_button)

        self.help_button = QPushButton(self.centralwidget)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setMaximumSize(QSize(26, 16777215))
        self.help_button.setFont(font1)

        self.horizontalLayout.addWidget(self.help_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.external_name_label.setToolTip(QCoreApplication.translate("MainWindow", u"Devices name", None))
#endif // QT_CONFIG(tooltip)
        self.external_name_label.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.last_backup_label.setText(QCoreApplication.translate("MainWindow", u"Last Backup:", None))
        self.app_logo_image.setText(QCoreApplication.translate("MainWindow", u"IMAGE", None))
        self.next_backup_label.setText(QCoreApplication.translate("MainWindow", u"Next Backup:", None))
        self.external_size_label.setText(QCoreApplication.translate("MainWindow", u"Available Space: ", None))
#if QT_CONFIG(tooltip)
        self.remove_backup_device.setToolTip(QCoreApplication.translate("MainWindow", u"Remove This Backup Device", None))
#endif // QT_CONFIG(tooltip)
        self.remove_backup_device.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.update_available_button.setText(QCoreApplication.translate("MainWindow", u" Update Available ", None))
        self.select_disk_button.setText(QCoreApplication.translate("MainWindow", u" Add Backup Device ", None))
#if QT_CONFIG(tooltip)
        self.options_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.options_button.setText(QCoreApplication.translate("MainWindow", u"Options...", None))
#if QT_CONFIG(tooltip)
        self.help_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.help_button.setText(QCoreApplication.translate("MainWindow", u"?", None))
    # retranslateUi

