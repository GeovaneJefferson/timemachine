from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MyWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setGeometry(100, 100, 300, 200)

        print("App Instance:", app)
        print("Returned App Instance:", app_instance)

def main():
    app = QApplication([])
    window = MyWindow(app)
    window.show()
    app.exec_()

    return app  # Return the QApplication instance

if __name__ == "__main__":
    app_instance = main()  # Get the QApplication instance from main()

