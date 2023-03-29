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

# Now
now = datetime.now()


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


def day_name(self):
    dayName = now.strftime("%a")
    return dayName

def current_date(self):
    dateDay = now.strftime("%d")
    return dateDay

def current_month(self):
    dateMonth = now.strftime("%m")
    return dateMonth

def current_year(self):
    dateYear = now.strftime("%y")
    return dateYear

def current_hour(self):
    currentHour = now.strftime("%H")
    return currentHour

def current_minute(self):
    currentMinute = now.strftime("%M")
    return currentMinute

def current_time(self):
    currentTime = int(current_hour()) + int(current_minute())
    return currentTime

def backup_time(self):
    backupTime = int(ini_next_hour()) + int(ini_next_minute())
    return backupTime
    
def create_backup_folder(self):
    createBackupFolder = f"{str(ini_external_location())}/{baseFolderName}/{backupFolderName}"
    return createBackupFolder

def wallpaper_main_folder(self):
    wallpaperMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}"
    return wallpaperMainFolder

def application_var_folder(self):
    applicationVarFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{varFolderName}"
    return applicationVarFolder

def application_local_folder(self):
    applicationLocalFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{localFolderName}"
    return applicationLocalFolder

def icon_main_folder(self):
    iconsMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{iconFolderName}"
    return iconsMainFolder

def cursor_main_folder(self):
    cursorMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{cursorFolderName}"
    return cursorMainFolder

def theme_main_folder(self):
    themeMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{themeFolderName}"
    return themeMainFolder

def gnomeshell_main_folder(self):
    gnomeShellMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{themeFolderName}/{gnomeShellFolder}"
    return gnomeShellMainFolder

def rpm_main_folder(self):
    rpmMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{rpmFolderName}"
    return rpmMainFolder

def deb_main_folder(self):
    debMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{debFolderName}"
    return debMainFolder

def date_folder_format(self):
    dateFolder = f"{str(mainIniFile.create_backup_folder())}/{str(mainIniFile.current_date())}-{str(mainIniFile.current_month())}-{str(mainIniFile.current_year())}"
    return dateFolder

def time_folder_format(self):
    timeFolder = f"{str(mainIniFile.create_backup_folder())}/{str(mainIniFile.current_date())}-{str(mainIniFile.current_month())}-{str(mainIniFile.current_year())}/{str(mainIniFile.current_hour())}-{str(mainIniFile.current_minute(()))}"
    return timeFolder

def flatpak_txt_location(self):
    flatpakTxtFile = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{flatpakTxt}"
    return flatpakTxtFile
