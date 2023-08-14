import sys
import os
from PySide6.QtCore import Qt, QDir, QSize
from PySide6.QtGui import QIcon, QPixmap, QImageReader, QImage
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QVBoxLayout, QWidget, QLabel, QFileDialog, QFileSystemModel

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.file_list_view = QListView()
        self.layout.addWidget(self.file_list_view)

        self.file_list_view.setIconSize(QSize(64, 64))
        self.file_list_view.setViewMode(QListView.IconMode)
        self.file_list_view.setResizeMode(QListView.Adjust)
        self.file_list_view.setSelectionMode(QListView.SingleSelection)
        self.file_list_view.setSpacing(10)

        self.file_list_view.clicked.connect(self.show_preview)

        self.preview_label = QLabel()
        self.layout.addWidget(self.preview_label)

        self.load_downloads_folder()

    def load_downloads_folder(self):
        downloads_path = QDir.homePath() + "/Documents"
        self.model = QFileSystemModel()
        self.model.setRootPath(downloads_path)
        self.file_list_view.setModel(self.model)
        self.file_list_view.setRootIndex(self.model.index(downloads_path))

    def show_preview(self, index):
        file_info = self.model.fileInfo(index)
        file_path = file_info.filePath()

        if file_info.isDir():
            self.preview_label.clear()
        else:
            mime_type = QImageReader.imageFormat(file_path)
            if mime_type:
                pixmap = QPixmap(file_path)
                self.preview_label.setPixmap(pixmap.scaledToWidth(300))
            else:
                self.preview_label.clear()

def main():
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
