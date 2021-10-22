import subprocess as sub
import configparser
import shutil
import getpass
import datetime
import os
import sys
import images

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

home_user = str(Path.home())
user_name = getpass.getuser()

src_user_config = "src/user.ini"


get_folder = ()
get_type = ()

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

class Restore(QMainWindow):
    def __init__(self):
        super(Restore, self).__init__()
        loadUi("src/restore.ui",self)
        self.folder_desktop.toggled.connect(self.on_desktop_selected)
        self.folder_downloads.toggled.connect(self.on_desktop_selected)
        self.folder_documents.toggled.connect(self.on_desktop_selected)
        self.folder_Music.toggled.connect(self.on_desktop_selected)
        self.folder_pictures.toggled.connect(self.on_desktop_selected)
        self.folder_videos.toggled.connect(self.on_desktop_selected)
        
        #RADIO CHOOSE
        if self.folder_desktop.setCheck(True):
            print("Desktop")
        if self.folder_documents.setCheck(True):
            print("Documents")
        if self.folder_downloads.setCheck(True):
            print("Downloads")
        if self.folder_music.setCheck(True):
            print("Music")
        if self.folder_pictures.setCheck(True):
            print("Pictures")            
        if self.folder_videos.setCheck(True):
            print("videos")

    def on_desktop_selected(self):
        if self.folder_desktop.isChecked():
            print("You did choose desktop")

    def on_downloads_selected(self):
        if self.folder_downloads.isChecked():
            print("You did choose downloads")

    def on_documents_selected(self):
        if self.folder_documents.isChecked():
            print("You did choose documents")

    def on_music_selected(self):
        if self.folder_music.isChecked():
            print("You did choose music")

    def on_pictures_selected(self):
        if self.folder_pictures.isChecked():
            print("You did choose pictures")

    def on_videos_selected(self):
        if self.folder_videos.isChecked():
            print("You did choose videos")

app = QApplication(sys.argv)
main_screen = Restore()
widget = QtWidgets.QStackedWidget()
appIcon = QIcon("src/icons/restore.png")
widget.setWindowIcon(appIcon)
widget.addWidget(main_screen)
widget.setFixedHeight(600)
widget.setFixedWidth(900)
widget.setWindowTitle("Time Machine")
widget.show()
app.exit(app.exec_())