import getpass
import os
import pathlib
import subprocess as sub
import configparser
import shutil
import time
import sys
import signal
import asyncio

from threading import Thread
from pathlib import Path
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import (Qt, QSize, QRect, QPropertyAnimation,
    QEasingCurve, QPoint)
from PySide6.QtGui import (QFont, QPixmap , QIcon, QMovie, QAction,
                            QPalette, QColor)
from PySide6.QtWidgets import (QMainWindow, QWidget, QApplication,
                            QPushButton, QLabel, QCheckBox, QLineEdit,
                            QWidget, QFrame, QGridLayout, QHBoxLayout,
                            QVBoxLayout, QMessageBox, QRadioButton,
                            QScrollArea, QSpacerItem, QSizePolicy,
                            QSpinBox, QComboBox, QGraphicsBlurEffect,
                            QSystemTrayIcon, QMenu, QStackedWidget)

################################################################################
## Variables
################################################################################
# Github
githubHome = "https://www.github.com/geovanejefferson/timemachine"

# Names
appName = "Time Machine"
appNameClose = "timemachine"
appVersion = "v1.1.7 dev"
baseFolderName = "TMB"
backupFolderName = "backups"
applicationFolderName = "applications"
wallpaperFolderName = "wallpaper"
iconFolderName = "icon"
themeFolderName = "theme"
cursorFolderName = "cursor"
gnomeShellFolder = "gnome-shell"
varFolderName = "var"
localFolderName = "share"
flatpakTxt = "flatpak.txt"

debFolderName = "deb"
rpmFolderName = "rpm"

# CMD commands
copyRsyncCMD = "rsync -avr --exclude={'cache','.cache'}"
copyCPCMD = "cp -rv"
createCMDFolder = "mkdir"
createCMDFile = "touch"
getFlatpaks = "flatpak list --columns=app --app"
installRPM = "sudo rpm -ivh --replacepkgs"
installDEB = "sudo dpkg -i"
flatpakInstallCommand = "flatpak install --system --noninteractive --assumeyes --or-update"

# DE
supportedOS = ["gnome", "ubuntu", "ubuntu:gnome", "unity", "pop"]
supportedDEBPackageManager = ["debian", "ubuntu"]
supportedRPMPackageManager = ["fedora", "opensuse"]
getUserDE = "echo $XDG_CURRENT_DESKTOP"
getUserPackageManager = "cat /etc/os-release"

# Theme
iconThemeName = "Adwaita"

################################################################################
# GNOME
################################################################################
detectThemeMode = "gsettings get org.gnome.desktop.interface color-scheme"

getGnomeWallpaper = "gsettings get org.gnome.desktop.background picture-uri"
getGnomeWallpaperDark = "gsettings get org.gnome.desktop.background picture-uri-dark"

setGnomeWallpaper = "gsettings set org.gnome.desktop.background picture-uri"
setGnomeWallpaperDark = "gsettings set org.gnome.desktop.background picture-uri-dark"

zoomGnomeWallpaper = "gsettings set org.gnome.desktop.background picture-options zoom"

# Icon
getUserIcon = "gsettings get org.gnome.desktop.interface icon-theme"
setUserIcon = "gsettings set org.gnome.desktop.interface icon-theme"

# Theme
getUserTheme = "gsettings get org.gnome.desktop.interface gtk-theme"
setUserTheme = "gsettings set org.gnome.desktop.interface gtk-theme"

# cursor
getUserCursor = "gsettings get org.gnome.desktop.interface cursor-theme"
setUserCursor = "gsettings set org.gnome.desktop.interface cursor-theme"

# Locations
media = "/media"
run = "/run/media"

# Fonts
mainFont = "Ubuntu"
normalFontSize = 10
smallFontSize = 5

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
timeModeHours60 = ['0000', '0100', '0200', '0300', '0400', '0500', '0600', '0700',
                      '0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500',
                      '1600', '1700', '1800', '1900', '2000', '2100', '2200', '2300']
timeModeHours120 = ['0000', '0200', '0400', '0600', '0800', '1000', '1200', '1400',
                       '1600', '1800', '2000', '2200']
timeModeHours240 = ['0000', '0400', '0800', '1200', '1600', '2000']

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
src_restore_icon = f"{homeUser}/.local/share/timemachine/src/icons/restore_64px.svg"
src_backup_icon = f"{homeUser}/.local/share/timemachine/src/icons/backup_128px.png"
src_migration_assistant_96px = f"{homeUser}/.local/share/timemachine/src/icons/migration_assistant_96px.png"
src_migration_assistant_clean_128px = f"{homeUser}/.local/share/timemachine/src/icons/migration_assistant_clean_128px.svg"
src_backup_now = f"{homeUser}/.local/share/timemachine/src/backup_now.py"
src_backup_check = f"{homeUser}/.local/share/timemachine/src/desktop/backup_check.desktop"
src_main_window_py = f"{homeUser}/.local/share/timemachine/src/mainwindow.py"
src_enter_time_machine_py = f"{homeUser}/.local/share/timemachine/src/enter_time_machine.py"
src_package_backup_py = f"{homeUser}/.local/share/timemachine/src/auto-package.py"
src_prepare_backup_py = f"{homeUser}/.local/share/timemachine/src/prepare_backup.py"
src_update_py = f"{homeUser}/.local/share/timemachine/src/update.py"

src_system_tray = f"{homeUser}/.local/share/timemachine/src/systemtray.py"
src_system_bar_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayicon.png"
src_system_bar_run_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayiconrun.png"
src_system_bar_error_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayiconerror.png"
src_system_bar_restore_icon = f"{homeUser}/.local/share/timemachine/src/icons/systemtrayiconrestore.png"

src_notification = f"{homeUser}/.local/share/timemachine/src/notification.py"
src_search_for_devices = f"{homeUser}/.local/share/timemachine/src/search_for_devices.py"
src_migration_assistant = f"{homeUser}/.local/share/timemachine/src/migration_assistant.py"
src_restore_cmd = f"{homeUser}/.local/share/timemachine/src/restore_cmd.py"

# .Exclude-applications
src_exclude_applications = ".exclude-applications.txt"


def signal_exit(*args):
    print("Updating INI settings... Exiting...")
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('BACKUP', 'backup_now', 'false')
        config.set('BACKUP', 'checker_running', 'false')
        config.write(configfile)

    exit()
    
# Error fuction
def error_trying_to_backup(error):
    # Set notification_id to 2
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('INFO', 'notification_id', "2")
        config.set('INFO', 'notification_add_info', f"{error}")
        config.set('BACKUP', 'checker_running', 'false')
        config.write(configfile)

    print(error)
    exit()