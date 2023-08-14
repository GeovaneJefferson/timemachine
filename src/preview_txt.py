import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QTextBrowser
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

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

        self.text_browser = QTextBrowser()

        self.splitter = QWidget()
        splitter_layout = QVBoxLayout()
        splitter_layout.addWidget(self.tree_view)
        splitter_layout.addWidget(self.text_browser)
        self.splitter.setLayout(splitter_layout)

        layout.addWidget(self.splitter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def preview_file(self, current, previous):
        file_path = self.model.filePath(current)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.read()
                self.text_browser.setPlainText(content)
                self.text_browser.moveCursor(QTextCursor.Start)

def main():
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
