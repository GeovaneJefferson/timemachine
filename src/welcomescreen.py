from setup import *
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_dialog import Ui_Dialog

class WelcomeScreen(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.select_disk_button.clicked.connect(self.on_selected_disk_button_clicked)

    def on_selected_disk_button_clicked(self):
        # Open dialog
        dialog = QDialog(self)
        dialog_ui = Ui_Dialog()
        dialog_ui.setupUi(dialog)
        
        # dialog.move(self.width()/4,-300)
        dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        # Conenction
        dialog_ui.cancel_button_dialog.clicked.connect(lambda: dialog.close())
        
        # Show the dialog
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = WelcomeScreen()
    widget.show()
    sys.exit(app.exec())
