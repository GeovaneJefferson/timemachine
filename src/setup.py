import getpass
import os
import pathlib
import subprocess as sub
import configparser
import shutil
import time
import sys
import images

from pathlib import Path
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QLabel, QCheckBox
from PyQt5.QtGui import QFont, QPixmap, QIcon

app_name = "Time Machine - Alpha Version"
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
# src_user_config = "user.ini"
# src_backup_now = "backup_now.py"
# src_ui_where = "where.ui"
# src_restore_small_icon = "icons/restore_small.png"
# src_folders_py = "options.py"
# src_backup_icon = "icons/backup.png"
# src_backup_check = "backup_check.desktop"
# src_backup_check_py = "backup_check.py"
# src_backup_check_desktop = ".config/autostart/backup_check.desktop"
# src_ui = "gui.ui"
# src_ui_options = "options.ui"
# src_timemachine_desktop = "timemachine.desktop"
# src_backup_check = "backup_check.desktop"

# Home location
src_options_py = home_user + "/.local/share/timemachine/src/options.py"
src_schedule_py = home_user + "/.local/share/timemachine/src/schedule.py"
src_backup_check_py = home_user + "/.local/share/timemachine/src/backup_check.py"
src_backup_check_desktop = home_user + "/.config/autostart/backup_check.desktop"
src_timemachine_desktop = home_user + "/.local/share/applications/timemachine.desktop"
src_folder_timemachine = home_user + "/.local/share/timemachine"
src_user_config = home_user + "/.local/share/timemachine/src/user.ini"
src_restore_icon = home_user + "/.local/share/timemachine/src/icons/restore_48.png"
src_backup_icon = home_user + "/.local/share/timemachine/src/icons/backup.png"
src_folders_py = home_user + "/.local/share/timemachine/src/folders.py"
src_backup_now = home_user + "/.local/share/timemachine/src/backup_now.py"
src_backup_check = home_user + "/.local/share/timemachine/src/backup_check.desktop"
src_ui = home_user + "/.local/share/timemachine/src/gui.ui"
src_ui_where = home_user + "/.local/share/timemachine/src/where.ui"
src_restore_small_icon = home_user + "/.local/share/timemachine/src/icons/restore_small.png"
src_ui_options = home_user + "/.local/share/timemachine/src/options.ui"
src_backup_py = home_user + "/.local/share/timemachine/src/backup_check.py"


# Notifications
def auto_backup_notification():
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup is enable!' 5", shell=True)


def auto_backup_off_notification():
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup is disable!' 5", shell=True)


def will_start_shortly_notification():
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",
              shell=True)
    exit()


def done_backup_notification():
    # After backup is done
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Time Machine is done backing up your files!' 5",
              shell=True)


def not_available_notification():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your external HD could not be found!' 5", shell=True)

    print("No HD found...")
    print("Existing...")
    exit()
