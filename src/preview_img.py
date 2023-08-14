import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QImageReader, QImage
from PySide6.QtCore import Qt

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.path.expanduser("~")))
        self.tree_view.selectionModel().currentChanged.connect(self.preview_file)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.splitter = QWidget()
        splitter_layout = QVBoxLayout()
        splitter_layout.addWidget(self.tree_view)
        splitter_layout.addWidget(self.image_label)
        self.splitter.setLayout(splitter_layout)

        layout.addWidget(self.splitter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def resize_image(self, pixmap, max_size):
        if pixmap.width() > max_size or pixmap.height() > max_size:
            pixmap = pixmap.scaled(max_size, max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    def preview_file(self, current, previous):
        file_path = self.model.filePath(current)
        
        if os.path.isfile(file_path) and file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            image_reader = QImageReader(file_path)
            pixmap = QPixmap.fromImageReader(image_reader)
            max_size = 300  # Set your maximum image size here
            pixmap = self.resize_image(pixmap, max_size)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.clear()

def main():
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
