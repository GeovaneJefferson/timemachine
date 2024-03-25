# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 360)
        MainWindow.setMinimumSize(QSize(500, 360))
        MainWindow.setMaximumSize(QSize(500, 360))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 0)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(False)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.frame_1 = QFrame(self.centralwidget)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.app_logo_image = QLabel(self.frame_1)
        self.app_logo_image.setObjectName(u"app_logo_image")

        self.gridLayout.addWidget(self.app_logo_image, 0, 0, 1, 1)

        self.external_name_label = QLabel(self.frame_1)
        self.external_name_label.setObjectName(u"external_name_label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.external_name_label.setFont(font1)
        self.external_name_label.setStyleSheet(u"")

        self.gridLayout.addWidget(self.external_name_label, 0, 1, 1, 1)

        self.last_backup_label = QLabel(self.frame_1)
        self.last_backup_label.setObjectName(u"last_backup_label")

        self.gridLayout.addWidget(self.last_backup_label, 2, 1, 1, 1)

        self.next_backup_label = QLabel(self.frame_1)
        self.next_backup_label.setObjectName(u"next_backup_label")

        self.gridLayout.addWidget(self.next_backup_label, 3, 1, 1, 1)

        self.remove_backup_device = QPushButton(self.frame_1)
        self.remove_backup_device.setObjectName(u"remove_backup_device")

        self.gridLayout.addWidget(self.remove_backup_device, 3, 2, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.progressbar_main_window = QProgressBar(self.frame_2)
        self.progressbar_main_window.setObjectName(u"progressbar_main_window")
        self.progressbar_main_window.setEnabled(True)
        self.progressbar_main_window.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setPointSize(10)
        self.progressbar_main_window.setFont(font2)
        self.progressbar_main_window.setMaximum(100)
        self.progressbar_main_window.setValue(0)
        self.progressbar_main_window.setTextVisible(True)

        self.gridLayout_3.addWidget(self.progressbar_main_window, 2, 0, 1, 1)

        self.external_size_label = QLabel(self.frame_2)
        self.external_size_label.setObjectName(u"external_size_label")

        self.gridLayout_3.addWidget(self.external_size_label, 1, 0, 1, 1)

        self.processbar_space = QProgressBar(self.frame_2)
        self.processbar_space.setObjectName(u"processbar_space")
        self.processbar_space.setValue(39)
        self.processbar_space.setTextVisible(False)

        self.gridLayout_3.addWidget(self.processbar_space, 0, 0, 1, 2)

        self.browser_backup_device = QPushButton(self.frame_2)
        self.browser_backup_device.setObjectName(u"browser_backup_device")

        self.gridLayout_3.addWidget(self.browser_backup_device, 1, 1, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 9, 0, 9)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.update_available_button = QPushButton(self.centralwidget)
        self.update_available_button.setObjectName(u"update_available_button")
        self.update_available_button.setFont(font2)
        self.update_available_button.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")

        self.horizontalLayout.addWidget(self.update_available_button)

        self.select_disk_button = QPushButton(self.centralwidget)
        self.select_disk_button.setObjectName(u"select_disk_button")

        self.horizontalLayout.addWidget(self.select_disk_button)

        self.options_button = QPushButton(self.centralwidget)
        self.options_button.setObjectName(u"options_button")
        self.options_button.setFont(font2)

        self.horizontalLayout.addWidget(self.options_button)

        self.help_button = QPushButton(self.centralwidget)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setMaximumSize(QSize(26, 16777215))
        self.help_button.setFont(font2)

        self.horizontalLayout.addWidget(self.help_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Backup Device", None))
        self.app_logo_image.setText(QCoreApplication.translate("MainWindow", u"IMAGE", None))
#if QT_CONFIG(tooltip)
        self.external_name_label.setToolTip(QCoreApplication.translate("MainWindow", u"Devices name", None))
#endif // QT_CONFIG(tooltip)
        self.external_name_label.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.last_backup_label.setText(QCoreApplication.translate("MainWindow", u"Last Backup:", None))
        self.next_backup_label.setText(QCoreApplication.translate("MainWindow", u"Next Backup:", None))
        self.remove_backup_device.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Storage Space", None))
        self.external_size_label.setText(QCoreApplication.translate("MainWindow", u"Available Space: ", None))
        self.browser_backup_device.setText(QCoreApplication.translate("MainWindow", u"Browser", None))
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

