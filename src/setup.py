import getpass
import os
import pathlib
import subprocess as sub
import configparser
import shutil
import time
import sys
import signal

from pathlib import Path
from datetime import datetime
from random import randint
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont, QPixmap, QIcon, QMovie, QAction
from PySide6.QtWidgets import (QMainWindow, QWidget, QApplication,
                            QPushButton, QLabel, QCheckBox, QLineEdit,
                            QWidget, QFrame, QGridLayout, QHBoxLayout,
                            QVBoxLayout, QMessageBox, QRadioButton,
                            QScrollArea, QSpacerItem, QSizePolicy,
                            QSpinBox, QComboBox, QGraphicsBlurEffect,
                            QProgressBar, QSystemTrayIcon, QMenu)

################################################################################
## Variables
################################################################################
app_name = "Time Machine"
appVersion = "v1.0.9"
folderName = "TMB"
exclude = ("linux", "mesa", "lib")
copyCmd = "rsync -avruzh"

################################################################################
## Fonts
################################################################################
bigTitle = QFont("DeJaVu Sans", 18)
topicTitle = QFont("DeJaVu Sans", 10.5)
item = QFont("DeJaVu Sans", 9)

################################################################################
## Locations
################################################################################
home_user = str(Path.home())
user_name = getpass.getuser()
get_home_folders = os.listdir(home_user)

time_mode_hours_60 = ['00', '01', '02', '03', '04', '05', '06', '07',
                      '08', '09', '10', '11', '12', '13', '14', '15',
                      '16', '17', '18', '19', '20', '21', '22', '23']

time_mode_hours_120 = ['00', '02', '04', '06', '08', '10', '12', '14',
                       '16', '18', '20', '22']

time_mode_hours_240 = ['00', '04', '08', '12', '16', '20']
time_mode_minutes_15 = ['00', '15', '30', '45']
time_mode_minutes_30 = ['00', '30']
min_fix = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# To edit locally
# src_current_location = pathlib.Path().resolve()  # Current folder
# src_options_py = "options.py"
# src_backup_py = "backup_check.py"
# src_restore_icon = "icons/restore_48.png"
# src_user_config = "ini/user.ini"
# src_backup_now = "backup_now.py"
# src_restore_small_icon = "icons/restore_small.png"
# src_folders_py = "options.py"
# src_backup_icon = "icons/backup.png"
# src_backup_check = "backup_check.desktop"
# src_backup_check_py = "backup_check.py"
# src_backup_check_desktop = ".config/autostart/backup_check.desktop"
# src_timemachine_desktop = "timemachine.desktop"
# src_backup_check = "desktop/backup_check.desktop"
# src_restore_py = "restore.py"
# src_system_tray = "systemtray.py"
# src_loadingGif = "icons/loading.gif"
# src_system_bar_icon = "icons/systemtrayicon.png"
# src_system_bar_run_icon = "icons/systemtrayiconrun.png"


# # Home location
src_options_py = f"{home_user}/.local/share/timemachine/src/options.py"
src_schedule_py = f"{home_user}/.local/share/timemachine/src/schedule.py"
src_backup_check_py = f"{home_user}/.local/share/timemachine/src/backup_check.py"
src_backup_check_desktop = f"{home_user}/.config/autostart/backup_check.desktop"
src_timemachine_desktop = f"{home_user}/.local/share/applications/timemachine.desktop"
src_folder_timemachine = f"{home_user}/.local/share/timemachine"
src_user_config = f"{home_user}/.local/share/timemachine/src/ini/user.ini"
src_restore_icon = f"{home_user}/.local/share/timemachine/src/icons/restore_48.png"
src_backup_icon = f"{home_user}/.local/share/timemachine/src/icons/backup.png"
src_backup_now = f"{home_user}/.local/share/timemachine/src/backup_now.py"
src_backup_check = f"{home_user}/.local/share/timemachine/src/desktop/backup_check.desktop"
src_restore_small_icon = f"{home_user}/.local/share/timemachine/src/icons/restore_small.png"
src_backup_py = f"{home_user}/.local/share/timemachine/src/backup_check.py"
src_restore_py = f"{home_user}/.local/share/timemachine/src/restore.py"
src_system_tray = f"{home_user}/.local/share/timemachine/src/systemtray.py"
src_loadingGif = f"{home_user}/.local/share/timemachine/src/icons/loading.gif"
src_system_bar_icon = f"{home_user}/.local/share/timemachine/src/icons/systemtrayicon.png"
src_system_bar_run_icon = f"{home_user}/.local/share/timemachine/src/icons/systemtrayiconrun.png"

# Notifications
def done_backup_notification():
    # After backup is done
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Time Machine is done backing up your files!' 5",
              shell=True)


def not_available_notification():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'No external devices mounted or available...' 5",
              shell=True)


def error_backup():
    # If error happens
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Error trying to back up folders...' 5", shell=True)


def error_reading():
    # If error happens
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Error trying to read user.ini...' 5", shell=True)


def error_delete():
    # If error happens
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Error trying to delete old backups!' 5", shell=True)


def manual_free_space():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Please, manual delete file(s)/folder(s) inside your external HD/SSD, to make space for Time Machine's backup!' 5", shell=True)


def no_external_info():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Location is empty... \n Select the external location "
              "first!' 5", shell=True)


def no_restore_folder_found():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'We could not find this folder inside the external.' 5", shell=True)


def been_restored():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your files are been restored...' 5",
              shell=True)


def failed_restore():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Error trying to restore your files!' 5",
              shell=True)
