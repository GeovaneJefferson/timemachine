import configparser
import sys
import subprocess as sub
import os

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize    
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *

home_user = str(Path.home())
get_home_folders = os.listdir(home_user)
min_fix = ["0","1","2","3","4","5","6","7","8","9"]

# src_user_config = "src/user.ini"
# src_ui_options = "src/options.ui"
# src_restore_icon = "src/icons/restore_48.png"
# src_backup_py = "src/backup_check.py"

#DST LOCATION
src_user_config = home_user+"/.local/share/timemachine/src/user.ini"
src_ui_options = home_user+"/.local/share/timemachine/src/options.ui"
src_restore_icon = home_user+"/.local/share/timemachine/src/icons/restore_48.png"
src_backup_py = home_user+"/.local/share/timemachine/src/backup_check.py"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

class Options(QMainWindow):
    def __init__(self):
        super(Options, self).__init__()
        loadUi(src_ui_options,self)
        self.check_desktop.clicked.connect(self.on_check_desktop_checked)
        self.check_downloads.clicked.connect(self.on_check_downloads_checked)
        self.check_documents.clicked.connect(self.on_check_documents_checked)
        self.check_music.clicked.connect(self.on_check_music_checked)
        self.check_pictures.clicked.connect(self.on_check_pictures_checked)
        self.check_videos.clicked.connect(self.on_check_videos_checked)
        self.label_hours.valueChanged.connect(self.label_hours_changed)
        self.label_minutes.valueChanged.connect(self.label_minutes_changed)
        self.button_save.clicked.connect(self.on_buttons_save_clicked)
        
        #CHECK FOR FOLDERS:
        read_desktop = config['FOLDER']['desktop']
        read_downloads = config['FOLDER']['downloads']
        read_documents = config['FOLDER']['documents']
        read_music = config['FOLDER']['music']
        read_pictures = config['FOLDER']['pictures']
        read_videos = config['FOLDER']['videos']

        if read_desktop == "true":
            self.check_desktop.setChecked(True) 

        if read_downloads == "true":
            self.check_downloads.setChecked(True) 

        if read_documents == "true":
            self.check_documents.setChecked(True) 

        if read_music == "true":
            self.check_music.setChecked(True) 

        if read_pictures == "true":
            self.check_pictures.setChecked(True) 

        if read_videos == "true":
            self.check_videos.setChecked(True) 
            
        #CHECK FOR SCHEDULE:
        sun = config['SCHEDULE']['sun']
        if sun == "true":
            self.check_sun.setChecked(True)

        mon = config['SCHEDULE']['mon']
        if mon == "true":
            self.check_mon.setChecked(True) 

        tue = config['SCHEDULE']['tue']
        if tue == "true":
            self.check_tue.setChecked(True) 

        wed = config['SCHEDULE']['wed']
        if wed == "true":
            self.check_wed.setChecked(True) 

        thu = config['SCHEDULE']['thu']
        if thu == "true":
            self.check_thu.setChecked(True) 

        fri = config['SCHEDULE']['fri']
        if fri == "true":
            self.check_fri.setChecked(True) 
            
        sat = config['SCHEDULE']['sat']
        if sat == "true":
            self.check_sat.setChecked(True) 

        #SCHEDULE OPTIONS
        #HOURS        
        hrs = (config.get('SCHEDULE', 'hours'))
        hrs = int(hrs)
        self.label_hours.setValue(hrs)

        #MINUTES        
        min = (config.get('SCHEDULE', 'minutes'))
        min = int(min)
        self.label_minutes.setValue(min)   

    def on_check_desktop_checked(self):
        if self.check_desktop.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'desktop', 'true')
                config.write(configfile) 
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'desktop', 'false')
                config.write(configfile) 
    
    def on_check_downloads_checked(self):
        if self.check_downloads.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'downloads', 'true')
                config.write(configfile) 
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'downloads', 'false')
                config.write(configfile) 
    
    def on_check_documents_checked(self):
        if self.check_documents.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'documents', 'true')
                config.write(configfile) 
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'documents', 'false')
                config.write(configfile) 
    
    def on_check_music_checked(self):
        if self.check_music.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'music', 'true')
                config.write(configfile) 
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'music', 'false')
                config.write(configfile) 
    
    def on_check_pictures_checked(self):
        if self.check_pictures.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'pictures', 'true')
                config.write(configfile) 
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'pictures', 'false')
                config.write(configfile) 
    
    def on_check_videos_checked(self):
        if self.check_videos.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'videos', 'true')
                config.write(configfile) 
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('FOLDER', 'videos', 'false')
                config.write(configfile) 

    #SCHEDULE
    def on_check_sun_clicked(self):
        if self.check_sun.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'sun', 'true')
                config.write(configfile)  
                print("Sun")
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'sun', 'false')
                config.write(configfile) 

    def on_check_mon_clicked(self):
        if self.check_mon.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'mon', 'true')
                config.write(configfile) 
                print("Mon")
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'mon', 'false')
                config.write(configfile) 

    def on_check_tue_clicked(self):
        if self.check_tue.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'tue', 'true')
                config.write(configfile) 
                print("Tue")
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'tue', 'false')
                config.write(configfile) 

    def on_check_wed_clicked(self):
        if self.check_wed.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'wed', 'true')
                config.write(configfile) 
                print("Wed")
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'wed', 'false')
                config.write(configfile) 

    def on_check_thu_clicked(self):
        if self.check_thu.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'thu', 'true')
                config.write(configfile) 
                print("Thu")
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'thu', 'false')
                config.write(configfile) 

    def on_check_fri_clicked(self):
        if self.check_fri.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'fri', 'true')
                config.write(configfile) 
                print("Fri")
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'fri', 'false')
                config.write(configfile) 

    def on_check_sat_clicked(self):
        if self.check_sat.isChecked():
             with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'sat', 'true')
                config.write(configfile) 
                print("Sat")
        else:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'sat', 'false')
                config.write(configfile) 

    def label_hours_changed(self):
        hours = self.label_hours.value()
        hours = str(hours)
        print((str(hours)))

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'hours', hours)
            config.write(configfile) 

        if hours in min_fix:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'hours', '0'+hours)
                config.write(configfile) 

    def label_minutes_changed(self):
        minutes = self.label_minutes.value()
        minutes = str(minutes)
        print((str(minutes)))

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'minutes', minutes)
            config.write(configfile) 

        if minutes in min_fix:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'minutes', '0'+minutes)
                config.write(configfile) 

    def on_buttons_save_clicked(self):
        sub.Popen("python3 "+src_backup_py,shell=True)
        exit()

# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
appIcon = QIcon(src_restore_icon)
widget.setWindowIcon(appIcon)
main_window = Options()
widget.addWidget(main_window)
widget.setFixedHeight(550)
widget.setFixedWidth(800)
widget.setWindowTitle("Options")
widget.show()
sys.exit(app.exec_())


