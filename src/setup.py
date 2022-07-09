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
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap, QIcon, QMovie, QAction
from PySide6.QtWidgets import (QMainWindow, QWidget, QApplication,
                            QPushButton, QLabel, QCheckBox, QLineEdit,
                            QWidget, QFrame, QGridLayout, QHBoxLayout,
                            QVBoxLayout, QMessageBox, QRadioButton,
                            QScrollArea, QSpacerItem, QSizePolicy,
                            QSpinBox, QComboBox, QGraphicsBlurEffect,
                            QProgressBar, QSystemTrayIcon, QMenu,
                            QStackedWidget)

################################################################################
## Variables
################################################################################
# Names
appName = "Time Machine"
appNameClose = "timemachine"
appVersion = "v1.1.1"
baseFolderName = "TMB"
backupFolderName = "backups"
applicationFolderName = "applications"
wallpaperFolderName = "wallpaper"
varFolderName = "var"
localFolderName = "share"
flatpakTxt = "flatpak.txt"

# CMD commands
copyCmd = "rsync -avrh --exclude={'cache','.cache'}" 
createCMDFolder = "mkdir"
createCMDFile = "touch"


# Locations
media = "/media"
run = "/run/media"

################################################################################
## Fonts
################################################################################
bigTitle = QFont("DeJaVu Sans", 18)
topicTitle = QFont("DeJaVu Sans", 10.5)
item = QFont("Ubuntu", 10)

################################################################################
## Locations
################################################################################
homeUser = str(Path.home())
userName = getpass.getuser()
getHomeFolders = os.listdir(homeUser)

################################################################################
## Times
################################################################################
timeModeMinutes30 = ['00', '30']
timeModeHours60 = ['00', '01', '02', '03', '04', '05', '06', '07',
                      '08', '09', '10', '11', '12', '13', '14', '15',
                      '16', '17', '18', '19', '20', '21', '22', '23']
timeModeHours120 = ['00', '02', '04', '06', '08', '10', '12', '14',
                       '16', '18', '20', '22']
timeModeHours240 = ['00', '04', '08', '12', '16', '20']

# Fix time
fixMinutes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# # Home location
src_flatpak_var_location = f"{homeUser}/.var/app"
src_flatpak_local_location = f"{homeUser}/.local/share/flatpak"
src_options_py = f"{homeUser}/.local/share/timemachine/src/options.py"
src_schedule_py = f"{homeUser}/.local/share/timemachine/src/schedule.py"
src_backup_check_py = f"{homeUser}/.local/share/timemachine/src/backup_check.py"
src_backup_check_desktop = f"{homeUser}/.config/autostart/backup_check.desktop"
src_timemachine_desktop = f"{homeUser}/.local/share/applications/timemachine.desktop"
src_folder_timemachine = f"{homeUser}/.local/share/timemachine"
src_user_config = f"{homeUser}/.local/share/timemachine/src/ini/user.ini"
src_restore_icon = f"{homeUser}/.local/share/timemachine/src/icons/restore_48.png"
src_backup_icon = f"{homeUser}/.local/share/timemachine/src/icons/backup.png"
src_backup_now = f"{homeUser}/.local/share/timemachine/src/backup_now.py"
src_backup_check = f"{homeUser}/.local/share/timemachine/src/desktop/backup_check.desktop"
src_restore_small_icon = f"{homeUser}/.local/share/timemachine/src/icons/restore_small.png"
src_backup_py = f"{homeUser}/.local/share/timemachine/src/backup_check.py"
src_enter_time_machine_py = f"{homeUser}/.local/share/timemachine/src/enter_time_machine.py"

src_system_tray = f"{homeUser}/.local/share/timemachine/src/systemtray.py"
src_system_bar_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayicon.png"
src_system_bar_run_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayiconrun.png"
src_system_bar_error_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayiconerror.png"
src_system_bar_restore_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayiconrestore.png"

src_notification = f"{homeUser}/.local/share/timemachine/src/notification.py"
src_search_for_devices = f"{homeUser}/.local/share/timemachine/src/search_for_devices.py"
src_welcome_screen = f"{homeUser}/.local/share/timemachine/src/welcome_screen.py"
src_restore_cmd = f"{homeUser}/.local/share/timemachine/src/restore_cmd.py"

