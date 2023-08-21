import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import (
    Qt, QSize, QRect, QPropertyAnimation,
    QEasingCurve, QPoint, QSocketNotifier,QDir)
from PySide6.QtGui import (QFont, QPixmap , QIcon, QMovie, QAction,
                            QPalette, QColor,QCursor,QImage,QImageReader,QTextCursor,QScreen,QGuiApplication)
from PySide6.QtWidgets import (QMainWindow, QWidget, QApplication,
                            QPushButton, QLabel, QCheckBox, QLineEdit,
                            QWidget, QFrame, QGridLayout, QHBoxLayout,
                            QVBoxLayout, QMessageBox, QRadioButton,
                            QScrollArea, QSpacerItem, QSizePolicy,
                            QSpinBox, QComboBox, QGraphicsBlurEffect,
                            QSystemTrayIcon, QMenu, QStackedWidget,QDialog,
                            QListView,QFileSystemModel,QTextBrowser)


class PreviewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.setModal(True)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.preview_label = QLabel(self)
        self.text_browser = QTextBrowser()
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.preview_label)
        self.layout.addWidget(self.text_browser)

    def set_preview(self, pixmap):
        self.preview_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.close()

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loc = []
        self.opened = False

        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.file_list_view = QListView()
        self.file_list_view.setWordWrap(True)
        self.layout.addWidget(self.file_list_view)

        self.file_list_view.setIconSize(QSize(64, 64))
        self.file_list_view.setViewMode(QListView.IconMode)
        self.file_list_view.setResizeMode(QListView.Adjust)
        self.file_list_view.setSelectionMode(QListView.MultiSelection)
        self.file_list_view.setSpacing(10)

        self.file_list_view.clicked.connect(self.selected_item)
        self.file_list_view.viewport().installEventFilter(self)

        self.preview_window = None

        self.load_downloads_folder()

    def load_downloads_folder(self):

        # downloads_path = QDir.homePath() + "/Downloads"
        downloads_path = "/media/geovane/"
        self.model = QFileSystemModel()
        self.model.setRootPath(downloads_path)
        self.file_list_view.setModel(self.model)
        self.file_list_view.setRootIndex(self.model.index(downloads_path))

    def selected_item(self, index):
        self.image_type = ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf']
        self.text_type = ['txt', 'py', 'cpp', 'h']

        file_info = self.model.fileInfo(index)
        file_path = file_info.filePath()

        print(file_path)

        if file_path.split(".")[-1] in self.image_type or file_path.split(".")[-1] in self.text_type:
            if file_path in self.loc:
                self.loc.remove(file_path)
            else:
                self.loc.append(file_path)
        else:
            self.loc.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            # Has value inside list
            if self.loc:
                last_item = self.loc[-1]
                last_item_extension = str(last_item).split(".")[-1]

                if not self.preview_window:
                    self.preview_window = PreviewWindow(self)

                if last_item_extension in self.image_type:
                    pixmap = QPixmap(self.loc[-1])

                    self.preview_window.text_browser.setFixedSize(0, 0)
                    self.preview_window.text_browser.clear()

                    self.preview_window.set_preview(pixmap.scaledToWidth(round(900/2)))
                    self.preview_window.show()

                elif last_item_extension in self.text_type:
                    with open(last_item, "r") as file:
                        self.preview_window.preview_label.clear()

                        self.preview_window.text_browser.setFixedSize(round(900/2), round(1080/2))
                        self.preview_window.text_browser.adjustSize()
                        self.preview_window.text_browser.setPlainText(file.read())
                        self.preview_window.text_browser.moveCursor(QTextCursor.Start)

                    # Open preview
                    self.preview_window.show()

def main():
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
