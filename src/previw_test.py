import sys
# from PySide6.QtCore import Qt, QDir, QSize, QTimer, QEvent
# from PySide6.QtGui import QPixmap, QImageReader
# from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QVBoxLayout, QWidget, QLabel, QFileSystemModel, QDialog



from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PreviewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.preview_label = QLabel(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.preview_label)
        self.setModal(True)

    def set_preview(self, pixmap):
        self.preview_label.setPixmap(pixmap)

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
        self.file_list_view.viewport().installEventFilter(self)

        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.show_hover_preview)

        self.preview_window = None

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
            self.show_hover_preview()
        else:
            mime_type = QImageReader.imageFormat(file_path)
            if mime_type:
                pixmap = QPixmap(file_path)
                self.show_hover_preview(pixmap)
            else:
                self.show_hover_preview()

    def eventFilter(self, obj, event):
        if obj == self.file_list_view.viewport() and event.type() == QEvent.Type.MouseMove:
            index = self.file_list_view.indexAt(event.pos())
            if index.isValid():
                self.preview_timer.start(500)  # Delay before showing preview
            else:
                self.preview_timer.stop()
                self.hide_hover_preview()
        return super().eventFilter(obj, event)

    def show_hover_preview(self, pixmap=None):
        if not self.preview_window:
            self.preview_window = PreviewWindow(self)

        if pixmap:
            self.preview_window.set_preview(pixmap.scaledToWidth(800))
        else:
            self.preview_window.set_preview(QPixmap())  # Clear preview

        # self.preview_window.setGeometry(self.x() + self.width(), self.y(), 400, 300)
        self.preview_window.show()

    def hide_hover_preview(self):
        if self.preview_window:
            self.preview_window.hide()
    
    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress:
            text = event.text()
            print(text)
            if event.modifiers():
                text = event.keyCombination().key().name.decode(encoding="utf-8")
            widget.label1.setText(text)
        return False
    
def main():
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
