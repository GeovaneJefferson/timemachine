import os
import shutil
from PySide6.QtCore import Qt, QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QProgressBar, QLabel
from setup import *
from get_folders_to_be_backup import get_folders

class BackupApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Backup App")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.backup_button = QPushButton("Start Backup")
        self.backup_button.clicked.connect(self.start_backup)
        self.layout.addWidget(self.backup_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.file_label = QLabel("Backing up: ")
        self.layout.addWidget(self.file_label)

        self.central_widget.setLayout(self.layout)


    @Slot()
    def start_backup(self):
        # Get a list of subdirectories to back up
        subdirectories = get_folders()
        copied_files = 0
        #target_folder = "/media/macbook/Backup_Drive/TMB/test"

        for i in subdirectories:
            source_folder = os.path.join(HOME_USER, i)
            total_files = count_files(source_folder)


            #for root, dirs, files in os.walk(source_folder):
                #for file in files:
                    #source_path = os.path.join(root, file)
                    #relative_path = os.path.relpath(source_path, source_folder)
                    #target_path = os.path.join(target_folder, i, relative_path)
                    #os.makedirs(os.path.dirname(target_path), exist_ok=True)

                    #try:
                        #shutil.copy(source_path, target_path)
                        #print(f"Backed up: {source_path}")
                    #except Exception as e:
                        #print(f"Error while backing up {source_path}: {e}")

            copied_files += 1
            progress = int(copied_files / total_files * 100)
            self.progress_bar.setValue(progress)

def count_files(folder_path):
    file_count = 0
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)
    return file_count


if __name__ == "__main__":
    app = QApplication([])
    window = BackupApp()
    window.show()
    app.exec()
