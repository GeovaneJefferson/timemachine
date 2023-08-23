import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar

class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
        if self.minimum() != self.maximum():
            self.timer = QTimer(self, timeout=self.onTimeout)
            self.timer.start(100)
            
    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        # layout.addWidget(ProgressBar(self, minimum=0, maximum=100))
        layout.addWidget(ProgressBar(self, minimum=0, maximum=0))
        # layout.addWidget(ProgressBar(self, minimum=0, maximum=100, textVisible=False))
        # layout.addWidget(ProgressBar(self, minimum=0, maximum=0, textVisible=False))
        # layout.addWidget(ProgressBar(self, minimum=0, maximum=100, textVisible=False))
        # layout.addWidget(ProgressBar(self, minimum=0, maximum=0, textVisible=False))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
