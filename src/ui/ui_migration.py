# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'migration.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QHBoxLayout, QLabel, QListView, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_WelcomeScreen(object):
    def setupUi(self, WelcomeScreen):
        if not WelcomeScreen.objectName():
            WelcomeScreen.setObjectName(u"WelcomeScreen")
        WelcomeScreen.resize(900, 600)
        WelcomeScreen.setMinimumSize(QSize(900, 600))
        WelcomeScreen.setMaximumSize(QSize(900, 600))
        self.verticalLayout_2 = QVBoxLayout(WelcomeScreen)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(WelcomeScreen)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setMinimumSize(QSize(900, 600))
        self.page_1.setMaximumSize(QSize(900, 600))
        self.verticalLayout_3 = QVBoxLayout(self.page_1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.title = QLabel(self.page_1)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setStyleSheet(u"color: rgb(70, 70, 70);")
        self.title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.image = QLabel(self.page_1)
        self.image.setObjectName(u"image")
        self.image.setMinimumSize(QSize(212, 212))
        self.image.setMaximumSize(QSize(212, 212))
        self.image.setStyleSheet(u"image: url(:/new/prefix1/icons/migration_assistant_212px.png);")

        self.verticalLayout.addWidget(self.image, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.description = QLabel(self.page_1)
        self.description.setObjectName(u"description")
        font1 = QFont()
        font1.setPointSize(11)
        self.description.setFont(font1)
        self.description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.description.setWordWrap(False)

        self.verticalLayout.addWidget(self.description, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.widget = QWidget(self.page_1)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"border-top: 1px solid rgba(110, 109, 112, 0.6)")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 1, 0, 1)

        self.verticalLayout_3.addWidget(self.widget, 0, Qt.AlignBottom)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(9)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.button_continue = QPushButton(self.page_1)
        self.button_continue.setObjectName(u"button_continue")
        self.button_continue.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")

        self.horizontalLayout_2.addWidget(self.button_continue, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalLayout_3.setStretch(0, 1)
        self.stackedWidget.addWidget(self.page_1)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_17 = QVBoxLayout(self.page_5)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(20)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(20, 20, 20, 20)
        self.image_page5 = QLabel(self.page_5)
        self.image_page5.setObjectName(u"image_page5")
        self.image_page5.setMinimumSize(QSize(64, 64))
        self.image_page5.setMaximumSize(QSize(64, 64))
        self.image_page5.setStyleSheet(u"image: url(:/new/prefix1/icons/migration_assistant_212px.png);")

        self.verticalLayout_16.addWidget(self.image_page5, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.title_5 = QLabel(self.page_5)
        self.title_5.setObjectName(u"title_5")
        self.title_5.setFont(font)
        self.title_5.setStyleSheet(u"color: rgb(70, 70, 70);")
        self.title_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_16.addWidget(self.title_5, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.description_5 = QLabel(self.page_5)
        self.description_5.setObjectName(u"description_5")
        self.description_5.setFont(font1)
        self.description_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.description_5.setWordWrap(False)

        self.verticalLayout_16.addWidget(self.description_5, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.reboot_label = QLabel(self.page_5)
        self.reboot_label.setObjectName(u"reboot_label")
        self.reboot_label.setMinimumSize(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(10)
        self.reboot_label.setFont(font2)

        self.verticalLayout_16.addWidget(self.reboot_label, 0, Qt.AlignHCenter)


        self.verticalLayout_17.addLayout(self.verticalLayout_16)

        self.widget_6 = QWidget(self.page_5)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setStyleSheet(u"border-top: 1px solid rgba(110, 109, 112, 0.6)")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_9.setSpacing(1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 1, 0, 1)

        self.verticalLayout_17.addWidget(self.widget_6, 0, Qt.AlignBottom)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(9)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(9, 9, 9, 9)
        self.button_close_page5 = QPushButton(self.page_5)
        self.button_close_page5.setObjectName(u"button_close_page5")
        self.button_close_page5.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")

        self.horizontalLayout_10.addWidget(self.button_close_page5, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_17.addLayout(self.horizontalLayout_10)

        self.verticalLayout_17.setStretch(1, 1)
        self.stackedWidget.addWidget(self.page_5)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setMinimumSize(QSize(900, 600))
        self.page_2.setMaximumSize(QSize(900, 600))
        self.verticalLayout_5 = QVBoxLayout(self.page_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.title_2 = QLabel(self.page_2)
        self.title_2.setObjectName(u"title_2")
        self.title_2.setFont(font)
        self.title_2.setStyleSheet(u"color: rgb(70, 70, 70);")
        self.title_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.title_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.description_2 = QLabel(self.page_2)
        self.description_2.setObjectName(u"description_2")
        self.description_2.setFont(font1)
        self.description_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.description_2.setWordWrap(False)

        self.verticalLayout_4.addWidget(self.description_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.devices_area_page2 = QListView(self.page_2)
        self.devices_area_page2.setObjectName(u"devices_area_page2")
        self.devices_area_page2.setMinimumSize(QSize(400, 220))
        self.devices_area_page2.setMaximumSize(QSize(400, 220))
        self.devices_area_page2.setFrameShape(QFrame.NoFrame)
        self.devices_area_page2.setFrameShadow(QFrame.Sunken)
        self.devices_area_page2.setDragDropMode(QAbstractItemView.DragDrop)
        self.devices_area_page2.setIconSize(QSize(48, 48))
        self.devices_area_page2.setViewMode(QListView.IconMode)
        self.devices_area_page2.setWordWrap(True)
        self.devices_area_page2.setItemAlignment(Qt.AlignHCenter)

        self.verticalLayout_4.addWidget(self.devices_area_page2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.verticalLayout_4.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(3, 1)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.widget_2 = QWidget(self.page_2)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"border-top: 1px solid rgba(110, 109, 112, 0.6)")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setSpacing(1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 1, 0, 1)

        self.verticalLayout_5.addWidget(self.widget_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.button_back_page2 = QPushButton(self.page_2)
        self.button_back_page2.setObjectName(u"button_back_page2")

        self.horizontalLayout_3.addWidget(self.button_back_page2)

        self.button_continue_page2 = QPushButton(self.page_2)
        self.button_continue_page2.setObjectName(u"button_continue_page2")
        self.button_continue_page2.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")

        self.horizontalLayout_3.addWidget(self.button_continue_page2, 0, Qt.AlignRight)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setMinimumSize(QSize(900, 600))
        self.page_3.setMaximumSize(QSize(900, 600))
        self.verticalLayout_7 = QVBoxLayout(self.page_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(20)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(20, 20, 20, 20)
        self.title_3 = QLabel(self.page_3)
        self.title_3.setObjectName(u"title_3")
        self.title_3.setFont(font)
        self.title_3.setStyleSheet(u"color: rgb(70, 70, 70);")
        self.title_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.title_3)

        self.description_3 = QLabel(self.page_3)
        self.description_3.setObjectName(u"description_3")
        self.description_3.setFont(font1)
        self.description_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.description_3.setWordWrap(False)

        self.verticalLayout_6.addWidget(self.description_3, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.widget_4 = QWidget(self.page_3)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(400, 300))
        self.widget_4.setMaximumSize(QSize(400, 300))
        self.verticalLayout_9 = QVBoxLayout(self.widget_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(9, 9, 9, 9)
        self.scrollArea = QScrollArea(self.widget_4)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setFrameShadow(QFrame.Sunken)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 362, 262))
        self.verticalLayout_10 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.checkbox_applications_page3 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkbox_applications_page3.setObjectName(u"checkbox_applications_page3")
        icon = QIcon()
        iconThemeName = u"application-x-executable"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.checkbox_applications_page3.setIcon(icon)
        self.checkbox_applications_page3.setIconSize(QSize(32, 32))

        self.verticalLayout_10.addWidget(self.checkbox_applications_page3)

        self.applications_sub_widget_page3 = QWidget(self.scrollAreaWidgetContents)
        self.applications_sub_widget_page3.setObjectName(u"applications_sub_widget_page3")
        self.applications_sub_widget_page3.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applications_sub_widget_page3.sizePolicy().hasHeightForWidth())
        self.applications_sub_widget_page3.setSizePolicy(sizePolicy)
        self.applications_sub_widget_page3.setMinimumSize(QSize(0, 0))
        self.applications_sub_widget_page3.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_12 = QVBoxLayout(self.applications_sub_widget_page3)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 0, -1, 0)
        self.applications_sub_checkbox_layout_page3 = QVBoxLayout()
        self.applications_sub_checkbox_layout_page3.setObjectName(u"applications_sub_checkbox_layout_page3")
        self.applications_sub_checkbox_layout_page3.setContentsMargins(9, 0, 9, 0)

        self.verticalLayout_12.addLayout(self.applications_sub_checkbox_layout_page3)


        self.verticalLayout_10.addWidget(self.applications_sub_widget_page3, 0, Qt.AlignTop)

        self.checkbox_flatpaks_page3 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkbox_flatpaks_page3.setObjectName(u"checkbox_flatpaks_page3")
        icon1 = QIcon()
        iconThemeName = u"applications-utilities"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.checkbox_flatpaks_page3.setIcon(icon1)
        self.checkbox_flatpaks_page3.setIconSize(QSize(32, 32))

        self.verticalLayout_10.addWidget(self.checkbox_flatpaks_page3)

        self.flatpaks_sub_widget_page3 = QWidget(self.scrollAreaWidgetContents)
        self.flatpaks_sub_widget_page3.setObjectName(u"flatpaks_sub_widget_page3")
        sizePolicy.setHeightForWidth(self.flatpaks_sub_widget_page3.sizePolicy().hasHeightForWidth())
        self.flatpaks_sub_widget_page3.setSizePolicy(sizePolicy)
        self.verticalLayout_15 = QVBoxLayout(self.flatpaks_sub_widget_page3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.flatpaks_sub_checkbox_layout_page3 = QVBoxLayout()
        self.flatpaks_sub_checkbox_layout_page3.setObjectName(u"flatpaks_sub_checkbox_layout_page3")
        self.flatpaks_sub_checkbox_layout_page3.setContentsMargins(9, -1, 9, -1)

        self.verticalLayout_15.addLayout(self.flatpaks_sub_checkbox_layout_page3)


        self.verticalLayout_10.addWidget(self.flatpaks_sub_widget_page3)

        self.checkBox_3 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setEnabled(False)
        icon2 = QIcon()
        iconThemeName = u"system-file-manager"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.checkBox_3.setIcon(icon2)
        self.checkBox_3.setIconSize(QSize(32, 32))

        self.verticalLayout_10.addWidget(self.checkBox_3)

        self.checkbox_files_folders_page3 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkbox_files_folders_page3.setObjectName(u"checkbox_files_folders_page3")
        self.checkbox_files_folders_page3.setIcon(icon2)
        self.checkbox_files_folders_page3.setIconSize(QSize(32, 32))

        self.verticalLayout_10.addWidget(self.checkbox_files_folders_page3)

        self.checkbox_system_settings_page3 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkbox_system_settings_page3.setObjectName(u"checkbox_system_settings_page3")
        icon3 = QIcon()
        iconThemeName = u"applications-system"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.checkbox_system_settings_page3.setIcon(icon3)
        self.checkbox_system_settings_page3.setIconSize(QSize(32, 32))

        self.verticalLayout_10.addWidget(self.checkbox_system_settings_page3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_8.addWidget(self.scrollArea)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)


        self.verticalLayout_6.addWidget(self.widget_4, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_6.setStretch(2, 1)

        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.widget_3 = QWidget(self.page_3)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"border-top: 1px solid rgba(110, 109, 112, 0.6)")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 1, 0, 1)

        self.verticalLayout_7.addWidget(self.widget_3, 0, Qt.AlignBottom)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(9)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.button_back_page3 = QPushButton(self.page_3)
        self.button_back_page3.setObjectName(u"button_back_page3")

        self.horizontalLayout_5.addWidget(self.button_back_page3)

        self.button_continue_page3 = QPushButton(self.page_3)
        self.button_continue_page3.setObjectName(u"button_continue_page3")
        self.button_continue_page3.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")

        self.horizontalLayout_5.addWidget(self.button_continue_page3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.verticalLayout_7.setStretch(0, 1)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setMinimumSize(QSize(900, 600))
        self.page_4.setMaximumSize(QSize(900, 600))
        self.verticalLayout_18 = QVBoxLayout(self.page_4)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, -1, 0, -1)
        self.restore = QVBoxLayout()
        self.restore.setSpacing(6)
        self.restore.setObjectName(u"restore")
        self.restore.setContentsMargins(20, 20, 20, 20)
        self.title_4 = QLabel(self.page_4)
        self.title_4.setObjectName(u"title_4")
        self.title_4.setFont(font)
        self.title_4.setStyleSheet(u"color: rgb(70, 70, 70);")
        self.title_4.setAlignment(Qt.AlignCenter)

        self.restore.addWidget(self.title_4)

        self.description_4 = QLabel(self.page_4)
        self.description_4.setObjectName(u"description_4")
        self.description_4.setFont(font1)
        self.description_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.description_4.setWordWrap(False)

        self.restore.addWidget(self.description_4, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.images_layout_page4 = QHBoxLayout()
        self.images_layout_page4.setObjectName(u"images_layout_page4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.images_layout_page4.addItem(self.horizontalSpacer_4)

        self.from_image = QWidget(self.page_4)
        self.from_image.setObjectName(u"from_image")
        self.from_image.setMinimumSize(QSize(180, 140))
        self.from_image.setMaximumSize(QSize(120, 140))
        self.verticalLayout_21 = QVBoxLayout(self.from_image)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.from_image_layout = QVBoxLayout()
        self.from_image_layout.setObjectName(u"from_image_layout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.from_image_layout.addItem(self.verticalSpacer_2)

        self.pushButton = QPushButton(self.from_image)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        self.pushButton.setAutoFillBackground(False)
        icon4 = QIcon()
        iconThemeName = u"drive-removable-media"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton.setIcon(icon4)
        self.pushButton.setIconSize(QSize(64, 64))
        self.pushButton.setFlat(True)

        self.from_image_layout.addWidget(self.pushButton, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.from_image_layout.addItem(self.verticalSpacer_4)

        self.from_image_label = QLabel(self.from_image)
        self.from_image_label.setObjectName(u"from_image_label")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        self.from_image_label.setFont(font3)

        self.from_image_layout.addWidget(self.from_image_label, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.verticalLayout_21.addLayout(self.from_image_layout)


        self.images_layout_page4.addWidget(self.from_image, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.pushButton_3 = QPushButton(self.page_4)
        self.pushButton_3.setObjectName(u"pushButton_3")
        icon5 = QIcon()
        iconThemeName = u"go-next"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_3.setIcon(icon5)
        self.pushButton_3.setIconSize(QSize(48, 48))
        self.pushButton_3.setFlat(True)

        self.images_layout_page4.addWidget(self.pushButton_3)

        self.to_image = QWidget(self.page_4)
        self.to_image.setObjectName(u"to_image")
        self.to_image.setMinimumSize(QSize(180, 140))
        self.to_image.setMaximumSize(QSize(120, 140))
        self.verticalLayout_22 = QVBoxLayout(self.to_image)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.to_image_layout = QVBoxLayout()
        self.to_image_layout.setObjectName(u"to_image_layout")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.to_image_layout.addItem(self.verticalSpacer_5)

        self.pushButton_2 = QPushButton(self.to_image)
        self.pushButton_2.setObjectName(u"pushButton_2")
        icon6 = QIcon()
        iconThemeName = u"computer"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_2.setIcon(icon6)
        self.pushButton_2.setIconSize(QSize(64, 64))
        self.pushButton_2.setFlat(True)

        self.to_image_layout.addWidget(self.pushButton_2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.to_image_layout.addItem(self.verticalSpacer_6)

        self.to_image_label = QLabel(self.to_image)
        self.to_image_label.setObjectName(u"to_image_label")
        self.to_image_label.setFont(font3)

        self.to_image_layout.addWidget(self.to_image_label, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.verticalLayout_22.addLayout(self.to_image_layout)


        self.images_layout_page4.addWidget(self.to_image, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.images_layout_page4.addItem(self.horizontalSpacer_5)


        self.restore.addLayout(self.images_layout_page4)

        self.label_restoring_status = QLabel(self.page_4)
        self.label_restoring_status.setObjectName(u"label_restoring_status")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_restoring_status.sizePolicy().hasHeightForWidth())
        self.label_restoring_status.setSizePolicy(sizePolicy1)
        self.label_restoring_status.setMinimumSize(QSize(350, 30))
        self.label_restoring_status.setMaximumSize(QSize(16777215, 30))

        self.restore.addWidget(self.label_restoring_status, 0, Qt.AlignHCenter)

        self.progress_bar_restoring = QProgressBar(self.page_4)
        self.progress_bar_restoring.setObjectName(u"progress_bar_restoring")
        self.progress_bar_restoring.setMinimumSize(QSize(320, 0))
        self.progress_bar_restoring.setMaximumSize(QSize(320, 16777215))
        self.progress_bar_restoring.setValue(0)

        self.restore.addWidget(self.progress_bar_restoring, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.restore.addItem(self.verticalSpacer)

        self.checkbox_automatically_reboot_page4 = QCheckBox(self.page_4)
        self.checkbox_automatically_reboot_page4.setObjectName(u"checkbox_automatically_reboot_page4")
        self.checkbox_automatically_reboot_page4.setFont(font2)
        self.checkbox_automatically_reboot_page4.setLayoutDirection(Qt.LeftToRight)

        self.restore.addWidget(self.checkbox_automatically_reboot_page4, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.restore.setStretch(2, 1)

        self.verticalLayout_18.addLayout(self.restore)

        self.widget_5 = QWidget(self.page_4)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setStyleSheet(u"border-top: 1px solid rgba(110, 109, 112, 0.6)")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_8.setSpacing(1)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 1, 0, 1)

        self.verticalLayout_18.addWidget(self.widget_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.button_back_page4 = QPushButton(self.page_4)
        self.button_back_page4.setObjectName(u"button_back_page4")

        self.horizontalLayout_7.addWidget(self.button_back_page4)

        self.button_restore_page4 = QPushButton(self.page_4)
        self.button_restore_page4.setObjectName(u"button_restore_page4")
        self.button_restore_page4.setFocusPolicy(Qt.StrongFocus)
        self.button_restore_page4.setStyleSheet(u"background-color: #2196f3;\n"
"color: white;")
        self.button_restore_page4.setAutoDefault(False)

        self.horizontalLayout_7.addWidget(self.button_restore_page4, 0, Qt.AlignRight)


        self.verticalLayout_18.addLayout(self.horizontalLayout_7)

        self.stackedWidget.addWidget(self.page_4)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.retranslateUi(WelcomeScreen)

        self.button_restore_page4.setDefault(False)


        QMetaObject.connectSlotsByName(WelcomeScreen)
    # setupUi

    def retranslateUi(self, WelcomeScreen):
        WelcomeScreen.setWindowTitle(QCoreApplication.translate("WelcomeScreen", u"Migration Assistant", None))
        self.title.setText(QCoreApplication.translate("WelcomeScreen", u"Migration Assistant", None))
        self.image.setText("")
        self.description.setText(QCoreApplication.translate("WelcomeScreen", u"Restore your applications, Documents, Pictures, Music, Videos, and more to this PC with Migration Assistant.", None))
        self.button_continue.setText(QCoreApplication.translate("WelcomeScreen", u"Continue", None))
        self.image_page5.setText("")
        self.title_5.setText(QCoreApplication.translate("WelcomeScreen", u"Migration Completed", None))
        self.description_5.setText(QCoreApplication.translate("WelcomeScreen", u"Your data has been migrated, and is ready to use.", None))
        self.reboot_label.setText("")
        self.button_close_page5.setText(QCoreApplication.translate("WelcomeScreen", u"Close", None))
        self.title_2.setText(QCoreApplication.translate("WelcomeScreen", u"Restore Information To This PC", None))
        self.description_2.setText(QCoreApplication.translate("WelcomeScreen", u"Select a disk with a Time Machine's backup to retore it's information to this PC.", None))
        self.label.setText(QCoreApplication.translate("WelcomeScreen", u"Make sure that your disk with a Time Machine's backup is already connected to this PC.", None))
        self.button_back_page2.setText(QCoreApplication.translate("WelcomeScreen", u"Back", None))
        self.button_continue_page2.setText(QCoreApplication.translate("WelcomeScreen", u"Continue", None))
        self.title_3.setText(QCoreApplication.translate("WelcomeScreen", u"Select The Information To Restore", None))
        self.description_3.setText(QCoreApplication.translate("WelcomeScreen", u"Choose which information you'd like to restore to this PC.", None))
#if QT_CONFIG(tooltip)
        self.checkbox_applications_page3.setToolTip(QCoreApplication.translate("WelcomeScreen", u"<html><head/><body><p>- Install backed up applications.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_applications_page3.setText(QCoreApplication.translate("WelcomeScreen", u"Applications", None))
#if QT_CONFIG(tooltip)
        self.checkbox_flatpaks_page3.setToolTip(QCoreApplication.translate("WelcomeScreen", u"<html><head/><body><p>- Install backed up flatpaks.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_flatpaks_page3.setText(QCoreApplication.translate("WelcomeScreen", u"Flatpaks", None))
        self.checkBox_3.setText(QCoreApplication.translate("WelcomeScreen", u"Flatpaks Data Coming soon...", None))
#if QT_CONFIG(tooltip)
        self.checkbox_files_folders_page3.setToolTip(QCoreApplication.translate("WelcomeScreen", u"<html><head/><body><p>- Restore backed up HOME folders.</p><p>- Restore some hidden files and folder.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_files_folders_page3.setText(QCoreApplication.translate("WelcomeScreen", u"Files and Folders", None))
#if QT_CONFIG(tooltip)
        self.checkbox_system_settings_page3.setToolTip(QCoreApplication.translate("WelcomeScreen", u"<html><head/><body><p>- Apply backed up wallpaper.</p><p>- Restore some system settings.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_system_settings_page3.setText(QCoreApplication.translate("WelcomeScreen", u"System Settings", None))
        self.button_back_page3.setText(QCoreApplication.translate("WelcomeScreen", u"Back", None))
        self.button_continue_page3.setText(QCoreApplication.translate("WelcomeScreen", u"Continue", None))
        self.title_4.setText(QCoreApplication.translate("WelcomeScreen", u"Begin Restoring", None))
        self.description_4.setText(QCoreApplication.translate("WelcomeScreen", u"Backup from Time Machine will been transferred to this PC.", None))
        self.pushButton.setText("")
        self.from_image_label.setText(QCoreApplication.translate("WelcomeScreen", u"Name", None))
        self.pushButton_3.setText("")
        self.pushButton_2.setText("")
        self.to_image_label.setText(QCoreApplication.translate("WelcomeScreen", u"Name", None))
        self.label_restoring_status.setText(QCoreApplication.translate("WelcomeScreen", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#if QT_CONFIG(whatsthis)
        self.checkbox_automatically_reboot_page4.setWhatsThis(QCoreApplication.translate("WelcomeScreen", u"<html><head/><body><p align=\"center\">Automatically reboot after restoring is done to ensure that some applications and system settings \\nwork properly. (Recommended)</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.checkbox_automatically_reboot_page4.setText(QCoreApplication.translate("WelcomeScreen", u"Automatically reboot, to ensure that some applications, and system settings work properly. (Recommended)", None))
        self.button_back_page4.setText(QCoreApplication.translate("WelcomeScreen", u"Back", None))
        self.button_restore_page4.setText(QCoreApplication.translate("WelcomeScreen", u"Restore", None))
    # retranslateUi

