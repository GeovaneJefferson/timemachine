import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QLabel

class ThumbnailDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 0:  # Assuming the thumbnail is in the first column
            thumbnail = index.data(Qt.DecorationRole)
            if thumbnail:
                thumbnail = thumbnail.scaledToHeight(option.rect.height(), Qt.SmoothTransformation)
                painter.drawPixmap(option.rect, thumbnail)
        else:
            super().paint(painter, option, index)

def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    # Create a QTreeWidget and set up the central widget
    tree_widget = QTreeWidget(main_window)
    main_window.setCentralWidget(tree_widget)

    # Set the delegate for the first column
    tree_widget.setItemDelegateForColumn(0, ThumbnailDelegate())

    # Add items to the QTreeWidget with thumbnails
    item1 = QTreeWidgetItem(tree_widget, ["", "Item 1"])
    thumbnail1 = QPixmap("path_to_thumbnail_1.png")  # Replace with the actual path
    item1.setData(0, Qt.DecorationRole, thumbnail1)

    item2 = QTreeWidgetItem(tree_widget, ["", "Item 2"])
    thumbnail2 = QPixmap("path_to_thumbnail_2.png")  # Replace with the actual path
    item2.setData(0, Qt.DecorationRole, thumbnail2)

    # ... add more items with thumbnails

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
