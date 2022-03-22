import getpass
import os
import pathlib
import subprocess as sub
import configparser
import shutil
import time
import sys

from pathlib import Path
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtWidgets import (QMainWindow, QWidget, QApplication,
                            QPushButton, QLabel, QCheckBox, QLineEdit,
                            QWidget, QFrame, QGridLayout, QHBoxLayout,
                            QVBoxLayout, QMessageBox, QRadioButton,
                            QScrollArea, QSpacerItem, QSizePolicy,
                            QSpinBox, QComboBox)

################################################################################
## Variables
################################################################################
app_name = "Time Machine"
folderName = "TMB"
exclude = ("linux", "mesa", "lib")
copyCmd = "rsync -avruzh"

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
# src_ui_where = "ui/where.ui"
# src_restore_small_icon = "icons/restore_small.png"
# src_folders_py = "options.py"
# src_backup_icon = "icons/backup.png"
# src_backup_check = "backup_check.desktop"
# src_backup_check_py = "backup_check.py"
# src_backup_check_desktop = ".config/autostart/backup_check.desktop"
# src_ui = "ui/gui.ui"
# src_ui_options = "ui/options.ui"
# src_timemachine_desktop = "timemachine.desktop"
# src_backup_check = "desktop/backup_check.desktop"
# src_service = "service.desktop"
# src_restore_settings = "scripts/restore_settings.txt"

# Home location
src_options_py = f"{home_user}/.local/share/timemachine/src/options.py"
src_schedule_py = f"{home_user}/.local/share/timemachine/src/schedule.py"
src_backup_check_py = f"{home_user}/.local/share/timemachine/src/backup_check.py"
src_backup_check_desktop = f"{home_user}/.config/autostart/backup_check.desktop"
src_timemachine_desktop = f"{home_user}/.local/share/applications/timemachine.desktop"
src_folder_timemachine = f"{home_user}/.local/share/timemachine"
src_user_config = f"{home_user}/.local/share/timemachine/src/ini/user.ini"
src_restore_icon = f"{home_user}/.local/share/timemachine/src/icons/restore_48.png"
src_backup_icon = f"{home_user}/.local/share/timemachine/src/icons/backup.png"
src_folders_py = f"{home_user}/.local/share/timemachine/src/folders.py"
src_backup_now = f"{home_user}/.local/share/timemachine/src/backup_now.py"
src_backup_check = f"{home_user}/.local/share/timemachine/src/desktop/backup_check.desktop"
src_ui = f"{home_user}/.local/share/timemachine/src/ui/gui.ui"
src_ui_where = f"{home_user}/.local/share/timemachine/src/ui/where.ui"
src_restore_small_icon = f"{home_user}/.local/share/timemachine/src/icons/restore_small.png"
src_ui_options = f"{home_user}/.local/share/timemachine/src/ui/options.ui"
src_backup_py = f"{home_user}/.local/share/timemachine/src/backup_check.py"
src_service = f"{home_user}/.local/share/timemachine/src/desktop/service.desktop"
src_restore_settings = f"{home_user}/.local/share/timemachine/src/scripts/restore_settings.txt"

# Notifications
def auto_backup_notification():
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup is enabled!' 5", shell=True)


def auto_backup_off_notification():
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup was disabled!' 5", shell=True)


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


def no_external_info():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Location is empty... \n Select the external location "
              "first!' 5", shell=True)


def been_restored():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your files are been restored...' 5",
              shell=True)


def failed_restore():
    # If external is not available
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Error trying to restore your files!' 5",
              shell=True)
