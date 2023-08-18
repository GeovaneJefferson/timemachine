import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QListWidget Example")
        self.setGeometry(100, 100, 400, 300)

        list_widget = QListWidget(self)
        list_widget.setGeometry(10, 10, 380, 280)

        # Add items to the list
        for i in range(5):
            item = QListWidgetItem(f"Item {i}")
            list_widget.addItem(item)

        # Connect item selection signal to a function
        list_widget.itemClicked.connect(self.item_clicked)

    def item_clicked(self, item):
        print(f"Clicked: {item.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
