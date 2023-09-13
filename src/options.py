from setup import *
from ui.ui_options import Ui_Options


class Options(QWidget):
    def __init__(self, parent=None):
        super(Options, self).__init__()
        self.ui = Ui_Options()
        self.ui.setupUi(self)

    def auto_select_stackwidget(self):
        # Auto check the first stack button
        self.ui.backup_stack_button.setChecked(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    stackedWidget = QStackedWidget()
	
    main = Options()
    
    stackedWidget.addWidget(main)
    stackedWidget.setCurrentIndex(0)
    stackedWidget.setFixedSize(400, 300)
    stackedWidget.show()
	
    sys.exit(app.exec())

    