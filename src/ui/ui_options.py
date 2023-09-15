# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'options.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Options(object):
    def setupUi(self, Options):
        if not Options.objectName():
            Options.setObjectName(u"Options")
        Options.resize(417, 300)
        Options.setMinimumSize(QSize(400, 300))
        Options.setMaximumSize(QSize(417, 300))
        self.verticalLayout = QVBoxLayout(Options)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Options)
        self.tabWidget.setObjectName(u"tabWidget")
        self.back_up_tab = QWidget()
        self.back_up_tab.setObjectName(u"back_up_tab")
        self.gridLayout_3 = QGridLayout(self.back_up_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_4 = QLabel(self.back_up_tab)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)

        self.scroll_area_folders = QScrollArea(self.back_up_tab)
        self.scroll_area_folders.setObjectName(u"scroll_area_folders")
        self.scroll_area_folders.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 375, 179))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.grid_folders_layout = QGridLayout()
        self.grid_folders_layout.setObjectName(u"grid_folders_layout")

        self.gridLayout_4.addLayout(self.grid_folders_layout, 0, 0, 1, 1)

        self.scroll_area_folders.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_3.addWidget(self.scroll_area_folders, 1, 0, 1, 1)

        self.tabWidget.addTab(self.back_up_tab, "")
        self.others_tab = QWidget()
        self.others_tab.setObjectName(u"others_tab")
        self.verticalLayout_4 = QVBoxLayout(self.others_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_5 = QLabel(self.others_tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.verticalLayout_3.addWidget(self.label_5)

        self.allow_flatpak_data_checkBox = QCheckBox(self.others_tab)
        self.allow_flatpak_data_checkBox.setObjectName(u"allow_flatpak_data_checkBox")
        self.allow_flatpak_data_checkBox.setEnabled(False)

        self.verticalLayout_3.addWidget(self.allow_flatpak_data_checkBox)

        self.label_6 = QLabel(self.others_tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout_3.addWidget(self.label_6)

        self.label_7 = QLabel(self.others_tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setScaledContents(False)
        self.label_7.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_7)

        self.reset_button = QPushButton(self.others_tab)
        self.reset_button.setObjectName(u"reset_button")

        self.verticalLayout_3.addWidget(self.reset_button, 0, Qt.AlignLeft)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.others_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.version_label = QLabel(Options)
        self.version_label.setObjectName(u"version_label")

        self.horizontalLayout_2.addWidget(self.version_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.cancel_button_options = QPushButton(Options)
        self.cancel_button_options.setObjectName(u"cancel_button_options")

        self.horizontalLayout_2.addWidget(self.cancel_button_options, 0, Qt.AlignRight)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Options)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Options)
    # setupUi

    def retranslateUi(self, Options):
        Options.setWindowTitle(QCoreApplication.translate("Options", u"Dialog", None))
        self.label_4.setText(QCoreApplication.translate("Options", u"Folders to be back up:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.back_up_tab), QCoreApplication.translate("Options", u"Back Up", None))
        self.label_5.setText(QCoreApplication.translate("Options", u"Flatpak Settings:", None))
        self.allow_flatpak_data_checkBox.setText(QCoreApplication.translate("Options", u"Back up flatpaks Data", None))
        self.label_6.setText(QCoreApplication.translate("Options", u"Reset:", None))
        self.label_7.setText(QCoreApplication.translate("Options", u"<html><head/><body><p>If something seems broken, click on Reset, to reset all settings.</p></body></html>", None))
        self.reset_button.setText(QCoreApplication.translate("Options", u"Reset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.others_tab), QCoreApplication.translate("Options", u"Others", None))
        self.version_label.setText(QCoreApplication.translate("Options", u"Version", None))
        self.cancel_button_options.setText(QCoreApplication.translate("Options", u"Close", None))
    # retranslateUi

