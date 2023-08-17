# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1131, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dates_layout = QHBoxLayout()
        self.dates_layout.setObjectName(u"dates_layout")

        self.verticalLayout.addLayout(self.dates_layout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.btn_up = QPushButton(self.centralwidget)
        self.btn_up.setObjectName(u"btn_up")

        self.horizontalLayout_5.addWidget(self.btn_up, 0, Qt.AlignHCenter)

        self.label_gray_time = QLabel(self.centralwidget)
        self.label_gray_time.setObjectName(u"label_gray_time")

        self.horizontalLayout_5.addWidget(self.label_gray_time)

        self.btn_down = QPushButton(self.centralwidget)
        self.btn_down.setObjectName(u"btn_down")

        self.horizontalLayout_5.addWidget(self.btn_down, 0, Qt.AlignHCenter)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(180, 0))
        self.widget_3.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout_6 = QVBoxLayout(self.widget_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.verticalLayout_6.addWidget(self.label)

        self.folders_layout = QVBoxLayout()
        self.folders_layout.setObjectName(u"folders_layout")

        self.verticalLayout_6.addLayout(self.folders_layout)

        self.verticalLayout_6.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.widget_3)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_7 = QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tree_widget = QTreeWidget(self.widget_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_widget.setHeaderItem(__qtreewidgetitem)
        self.tree_widget.setObjectName(u"tree_widget")
        self.tree_widget.setMinimumSize(QSize(600, 400))
        self.tree_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tree_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree_widget.setIconSize(QSize(16, 16))
        self.tree_widget.setAnimated(True)

        self.verticalLayout_7.addWidget(self.tree_widget)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(220, 0))
        self.widget.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.small_preview_text = QTextBrowser(self.widget)
        self.small_preview_text.setObjectName(u"small_preview_text")
        self.small_preview_text.setMaximumSize(QSize(16777215, 0))

        self.verticalLayout_3.addWidget(self.small_preview_text)

        self.small_preview_label = QLabel(self.widget)
        self.small_preview_label.setObjectName(u"small_preview_label")
        self.small_preview_label.setMinimumSize(QSize(190, 140))
        self.small_preview_label.setMaximumSize(QSize(0, 140))

        self.verticalLayout_3.addWidget(self.small_preview_label, 0, Qt.AlignTop)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_cancel = QPushButton(self.widget)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setMinimumSize(QSize(88, 34))
        self.btn_cancel.setMaximumSize(QSize(88, 34))
        self.btn_cancel.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.btn_cancel, 0, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout_4.addItem(self.verticalSpacer)

        self.btn_restore = QPushButton(self.widget)
        self.btn_restore.setObjectName(u"btn_restore")
        self.btn_restore.setMinimumSize(QSize(88, 34))
        self.btn_restore.setMaximumSize(QSize(88, 34))
        self.btn_restore.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.btn_restore, 0, Qt.AlignTop)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_up.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.label_gray_time.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.btn_down.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Folders", None))
        self.small_preview_label.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.btn_restore.setText(QCoreApplication.translate("MainWindow", u"Restore", None))
    # retranslateUi

