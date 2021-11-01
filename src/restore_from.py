import subprocess as sub
import configparser
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
src_restore_icon = "src/icons/restore_48.png"
src_ui_restore = "src/restore.ui"

#dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"

desktop_selected = False
downloads_selected = False
documents_selected = False
music_selected = False
pictures_selected = False
videos_selected = False

application_selected = False
text_selected = False
audio_selected = False
image_selected = False
video_selected = False
other_selected = False

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

#TIMER
timer = QtCore.QTimer()

class Restore(QMainWindow):

    def __init__(self):
        super(Restore, self).__init__()
        loadUi(src_ui_restore,self)
        self.folder_desktop.toggled.connect(self.on_desktop_selected)
        self.folder_downloads.toggled.connect(self.on_desktop_selected)
        self.folder_documents.toggled.connect(self.on_documents_selected)
        self.folder_music.toggled.connect(self.on_desktop_selected)
        self.folder_pictures.toggled.connect(self.on_desktop_selected)
        self.folder_videos.toggled.connect(self.on_desktop_selected)

        self.type_application.toggled.connect(self.on_application_selected)
        self.type_text.toggled.connect(self.on_text_selected)
        self.type_audio.toggled.connect(self.on_audio_selected)
        self.type_image.toggled.connect(self.on_image_selected)
        self.type_video.toggled.connect(self.on_video_selected)
        self.type_other.toggled.connect(self.on_other_selected)
                
        #RADIO FOLDER
        if desktop_selected == True:
            print("Desktop")
            self.folder_desktop.setCheck(True)

        if downloads_selected == True:
            print("Downloads")
            self.folder_downloads.setCheck(True)

        if documents_selected == True:
            print("Documents")
            self.folder_documents.setCheck(True)

        if music_selected == "true":
            print("Music")
            self.folder_music.setCheck(True)

        if pictures_selected == "true":
            print("Pictures")  
            self.folder_pictures.setCheck(True)

        if videos_selected == True:
            print("videos")
            self.folder_videos.setCheck(True)

        if videos_selected == True:
            print("videos")
            self.folder_videos.setCheck(True) 

        #WHEN CHECKBOXES  (SHOW FOLDERS OPTIONS)
        self.read_hd_name = config['EXTERNAL']['name']    
        self.tmb_folder = "/media/"+user_name+'/'+'USB'+"/TMB"

        vertical = 108
        for self.file in os.listdir(self.tmb_folder):  
            if not self.file.startswith('.'):
                self.when_checkbox = QRadioButton(self.file, self)
                self.when_checkbox.autoExclusive
                self.when_checkbox.setFixedSize(310, 22)
                self.when_checkbox.move(10, vertical)
                vertical = vertical + 30
                text = self.when_checkbox.text()
                self.when_checkbox.show()   
                self.when_checkbox.clicked.connect(lambda ch, text=text : self.test(text))

    def test(self,x):
        print(x)
        if self.folder_desktop.isChecked():
            self.folder_loc = "/Desktop" 

        if self.folder_downloads.isChecked():
            self.folder_loc = "/Downloads" 

        if self.folder_documents.isChecked():
            self.folder_loc = "/Documents" 

        if self.folder_music.isChecked():
            self.folder_loc = "/Music" 

        if self.folder_pictures.isChecked():
            self.folder_loc = "/Pictures" 

        if self.folder_videos.isChecked():
            self.folder_loc = "/Videos" 


    #     #TIMER
    #     timer.timeout.connect(self.updates)
    #     timer.start(2000) # update every second
    #     self.updates()

    # def updates(self):
    #     #GET FOLDERS


    def on_desktop_selected(self):
        if self.folder_desktop.isChecked():
            self.folder_loc = "/Desktop" 
            go_to = self.tmb_folder+"/27-10-21"+self.folder_loc
            when_vert_space = 310
            for self.file in os.listdir(go_to):  
                if not self.file.startswith('.'):
                    self.files_checkbox = QCheckBox(self.file, self)
                    self.files_checkbox.autoExclusive
                    self.files_checkbox.setFixedSize(310, 22)
                    self.files_checkbox.move(280, when_vert_space)
                    when_vert_space = when_vert_space + 30
                    text = self.files_checkbox.text()
                    self.files_checkbox.show()  

    def on_documents_selected(self):
        if self.folder_documents.isChecked():
            self.folder_loc = "/Documents" 
            go_to = self.tmb_folder+"/27-10-21"+self.folder_loc
            when_vert_space = 310
            for self.file in os.listdir(go_to):  
                if not self.file.startswith('.'):
                    self.files_checkbox = QCheckBox(self.file, self)
                    self.files_checkbox.autoExclusive
                    self.files_checkbox.setFixedSize(310, 22)
                    self.files_checkbox.move(280, when_vert_space)
                    when_vert_space = when_vert_space + 30
                    text = self.files_checkbox.text()
                    self.files_checkbox.show()  
            # for root, directories, files in os.walk(loc):
            #     for file in files:
            #         if file.endswith(".txt"):
            #             show_file = (os.path.join(root, file))
            #             print(show_file)
    
    def on_application_selected(self):
        if self.type_application.isChecked():
            print("You did choose application")

    def on_text_selected(self):
        if self.type_text.isChecked():
            print("You did choose text")

    def on_audio_selected(self):
        if self.type_audio.isChecked():
            print("You did choose audio")

    def on_image_selected(self):
        if self.type_image.isChecked():
            print("You did choose image")

    def on_video_selected(self):
        if self.type_video.isChecked():
            print("You did choose video")

    def on_other_selected(self):
        if self.type_other.isChecked():
            print("You did choose other")

app = QApplication(sys.argv)
main_screen = Restore()
widget = QtWidgets.QStackedWidget()
appIcon = QIcon(src_restore_icon)
widget.setWindowIcon(appIcon)
widget.addWidget(main_screen)
widget.setFixedHeight(750)
widget.setFixedWidth(900)
widget.setWindowTitle("Time Machine")
widget.show()
app.exit(app.exec_())