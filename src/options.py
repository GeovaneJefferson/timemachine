import configparser
import sys
import subprocess as sub
import os

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

home_user = str(Path.home())
get_home_folders = os.listdir(home_user)
min_fix = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# SRC LOCATION
src_user_config = "/home/geovane/Downloads/timemachine/src/user.ini"
src_ui_options = "/home/geovane/Downloads/timemachine/src/options.ui"
src_restore_icon = "/home/geovane/Downloads/timemachine/src/icons/restore_48.png"
src_backup_py = "/home/geovane/Downloads/timemachine/src/backup_check.py"

# DST LOCATION
# src_user_config = home_user + "/.local/share/timemachine/src/user.ini"
# src_ui_options = home_user + "/.local/share/timemachine/src/options.ui"
# src_restore_icon = home_user + "/.local/share/timemachine/src/icons/restore_48.png"
# src_backup_py = home_user + "/.local/share/timemachine/src/backup_check.py"

# CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

# TIMER
timer = QtCore.QTimer()


class Options(QMainWindow):
    def __init__(self):
        super(Options, self).__init__()
        loadUi(src_ui_options, self)
        self.check_desktop.clicked.connect(self.on_check_desktop_checked)
        self.check_downloads.clicked.connect(self.on_check_downloads_checked)
        self.check_documents.clicked.connect(self.on_check_documents_checked)
        self.check_music.clicked.connect(self.on_check_music_checked)
        self.check_pictures.clicked.connect(self.on_check_pictures_checked)
        self.check_videos.clicked.connect(self.on_check_videos_checked)
        self.label_hours.valueChanged.connect(self.label_hours_changed)
        self.label_minutes.valueChanged.connect(self.label_minutes_changed)
        self.one_time_mode.clicked.connect(self.on_frequency_clicked)
        self.more_time_mode.clicked.connect(self.on_frequency_clicked)
        self.every_combox.currentIndexChanged.connect(self.on_every_combox_changed)
        self.button_save.clicked.connect(self.on_buttons_save_clicked)

        # CHECK FOR FOLDERS:
        read_desktop = config['FOLDER']['desktop']
        read_downloads = config['FOLDER']['downloads']
        read_documents = config['FOLDER']['documents']
        read_music = config['FOLDER']['music']
        read_pictures = config['FOLDER']['pictures']
        read_videos = config['FOLDER']['videos']

        # READ FOLDERS
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

        # # MORE FOLDERS
        # vertical_checkbox = 210
        # vertical_label = 170
        # for self.files in (get_home_folders):
        #     if not self.files.startswith("."):
        #         if not self.files in ["Desktop", "Documents", "Downloads", "Music", "Videos", "Pictures"]:
        #             label_text = QLabel(self.files, self.folders_frame)
        #             label_text.setFixedSize(200, 22)
        #             label_text.move(35, vertical_label)
        #             vertical_label = vertical_label + 22
        #
        #             folders_checkbox = QCheckBox(self)
        #             folders_checkbox.setFixedSize(200, 22)
        #             folders_checkbox.move(32, vertical_checkbox)
        #             vertical_checkbox = vertical_checkbox + 22
        #             self.text = label_text.text()
        #             folders_checkbox.show()
        #             folders_checkbox.clicked.connect(lambda ch, text=self.text: print(text))
        #             folders_checkbox.clicked.connect(lambda ch, text=self.text: self.here(text))

        # CHECK FOR SCHEDULE:
        sun = config['SCHEDULE']['sun']
        mon = config['SCHEDULE']['mon']
        tue = config['SCHEDULE']['tue']
        wed = config['SCHEDULE']['wed']
        thu = config['SCHEDULE']['thu']
        fri = config['SCHEDULE']['fri']
        sat = config['SCHEDULE']['sat']

        if sun == "true":
            self.check_sun.setChecked(True)

        if mon == "true":
            self.check_mon.setChecked(True)

        if tue == "true":
            self.check_tue.setChecked(True)

        if wed == "true":
            self.check_wed.setChecked(True)

        if thu == "true":
            self.check_thu.setChecked(True)

        if fri == "true":
            self.check_fri.setChecked(True)

        if sat == "true":
            self.check_sat.setChecked(True)

            # SCHEDULE OPTIONS
        # HOURS
        hrs = (config.get('SCHEDULE', 'hours'))
        hrs = int(hrs)
        self.label_hours.setValue(hrs)

        # MINUTES
        min = (config.get('SCHEDULE', 'minutes'))
        min = int(min)
        self.label_minutes.setValue(min)

        # EVERYTIME
        read_everytime = config['SCHEDULE']['everytime']
        if read_everytime == "15":
            self.every_combox.setCurrentIndex(0)

        elif read_everytime == "30":
            self.every_combox.setCurrentIndex(1)

        elif read_everytime == "60":
            self.every_combox.setCurrentIndex(2)

        elif read_everytime == "120":
            self.every_combox.setCurrentIndex(3)

        elif read_everytime == "240":
            self.every_combox.setCurrentIndex(4)

        # TIMER
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

    def updates(self):
        # CONFIGPARSER
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # FREQUENCY CHECK
        one_time_mode = config['MODE']['one_time_mode']
        more_time_mode = config['MODE']['more_time_mode']

        if one_time_mode == "true":
            self.every_combox.setEnabled(False)
            self.label_hours.setEnabled(True)
            self.label_minutes.setEnabled(True)
            self.one_time_mode.setChecked(True)

        if more_time_mode == "true":
            self.label_hours.setEnabled(False)
            self.label_minutes.setEnabled(False)
            self.every_combox.setEnabled(True)
            self.more_time_mode.setChecked(True)

    def on_every_combox_changed(self):
        choose_every_combox = self.every_combox.currentIndex()
        if choose_every_combox == 0:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'everytime', '15')
                config.write(configfile)

        elif choose_every_combox == 1:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'everytime', '30')
                config.write(configfile)

        elif choose_every_combox == 2:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'everytime', '60')
                config.write(configfile)

        elif choose_every_combox == 3:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'everytime', '120')
                config.write(configfile)

        elif choose_every_combox == 4:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'everytime', '240')
                config.write(configfile)

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

                # SCHEDULE

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

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'hours', hours)
            config.write(configfile)

        if hours in min_fix:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'hours', '0' + hours)
                config.write(configfile)

    def label_minutes_changed(self):
        minutes = self.label_minutes.value()
        minutes = str(minutes)

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'minutes', minutes)
            config.write(configfile)

        if minutes in min_fix:
            with open(src_user_config, 'w') as configfile:
                config.set('SCHEDULE', 'minutes', '0' + minutes)
                config.write(configfile)

    def on_frequency_clicked(self):
        if self.one_time_mode.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('MODE', 'one_time_mode', 'true')
                config.write(configfile)
                print("One time mode selected")

            # DISABLE MORE TIME MODE
            with open(src_user_config, 'w') as configfile:
                config.set('MODE', 'more_time_mode', 'false')
                config.write(configfile)
                print("More time mode disabled")

        elif self.more_time_mode.isChecked():
            with open(src_user_config, 'w') as configfile:
                config.set('MODE', 'more_time_mode', 'true')
                config.write(configfile)
                print("Multiple time mode selected")

            # DISABLE ONE TIME MODE
            with open(src_user_config, 'w') as configfile:
                config.set('MODE', 'one_time_mode', 'false')
                config.write(configfile)
                print("One time mode disabled")

    def on_buttons_save_clicked(self):
        sub.Popen("python3 " + src_backup_py, shell=True)
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
