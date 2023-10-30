import sys
from PySide6.QtCore import Qt, QProcess, QTextStream
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit

class UpdateApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Update App')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.update_button = QPushButton('Run sudo apt update', self)
        self.update_button.clicked.connect(self.run_update)
        self.layout.addWidget(self.update_button)

        self.command_output = QTextEdit(self)
        self.command_output.setReadOnly(True)
        self.layout.addWidget(self.command_output)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)

    def run_update(self):
        self.process.start('sudo', ['apt', 'update'])
        self.update_button.setDisabled(True)

    def handle_output(self):
        output_stream = QTextStream(self.process)
        while not output_stream.atEnd():
            line = output_stream.readLine()
            self.command_output.append(line)

    def closeEvent(self, event):
        # Make sure to kill the process if the application is closed.
        if self.process.state() == QProcess.Running:
            self.process.kill()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UpdateApp()
    window.show()
    sys.exit(app.exec_())
