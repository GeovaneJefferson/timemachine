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
import fcntl

from stylesheet import *
from pathlib import Path
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import (
    Qt, QSize, QRect, QPropertyAnimation,
    QEasingCurve, QPoint, QSocketNotifier)
from PySide6.QtGui import (QFont, QPixmap , QIcon, QMovie, QAction,
                            QPalette, QColor,QCursor,QImage)
from PySide6.QtWidgets import (QMainWindow, QWidget, QApplication,
                            QPushButton, QLabel, QCheckBox, QLineEdit,
                            QWidget, QFrame, QGridLayout, QHBoxLayout,
                            QVBoxLayout, QMessageBox, QRadioButton,
                            QScrollArea, QSpacerItem, QSizePolicy,
                            QSpinBox, QComboBox, QGraphicsBlurEffect,
                            QSystemTrayIcon, QMenu, QStackedWidget)

timer = QtCore.QTimer()

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
fontsFolderName = "fonts"
gtkThemeFolderName = "gtktheme"
themeFolderName = "theme"
cursorFolderName = "cursor"
colorSchemeName = "color-schemes"
plasmaFolderName = "plasma"
kdeScriptsFolderName = "kde-scripts"
kdeNotesFolderName = "plasma-notes"
auroraeFolderName = "aurorae"
kdeGlobalsFolderName = "kdeglobals"
kGlobalShortcutSrcFolderName = "kglobalshortcutsrc"
kWinRcFolderName = "kwinrc"
gnomeShellFolder = "gnome-shell"
varFolderName = "var"
localFolderName = "share"
kdeFolderName = "kde"

configurationFolderName = "configurations"
shareFolderName = "share"

configFolderName = "config"
shareConfigFolderName = "share_config"
flatpakTxt = "flatpak.txt"
restoreSettingsIni = "restore_settings.ini"

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
supportedOS = ["gnome", "ubuntu", "ubuntu:gnome", "unity", "pop", "kde"]
supportedDEBPackageManager = ["debian", "ubuntu"]
supportedRPMPackageManager = ["fedora", "opensuse"]
getUserDE = "echo $XDG_CURRENT_DESKTOP"
getUserPackageManager = "cat /etc/os-release"

# Theme
iconThemeName = "Adwaita"

systemTrayPipeName = "/tmp/system_tray.pipe"
appPipeName = f"/tmp/{appNameClose}.pipe"
backupNowPipeName = f"/tmp/backup_now.pipe"

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
getUserIconCMD = "gsettings get org.gnome.desktop.interface icon-theme"
setUserIconCMD = "gsettings set org.gnome.desktop.interface icon-theme"

# Theme
getUserThemeCMD = "gsettings get org.gnome.desktop.interface gtk-theme"
setUserThemeCMD = "gsettings set org.gnome.desktop.interface gtk-theme"

# Cursor
getUserCursorCMD = "gsettings get org.gnome.desktop.interface cursor-theme"
setUserCursorCMD = "gsettings set org.gnome.desktop.interface cursor-theme"

# Font
# gsettings set org.gnome.desktop.interface font-name "FreeSans Regular 11"
getUserFontCMD = "gsettings get org.gnome.desktop.interface font-name"
# 'FreeSans Regular 11'
setUserFontCMD = "gsettings get org.gnome.desktop.interface font-name"

################################################################################
# KDE
################################################################################
# Cursor
getKDEUserCursorCMD = "plasma-apply-cursortheme --list-themes"
# Color Scheme
getKDEUserColorSchemeCMD = "plasma-apply-colorscheme --list-schemes"
# Plasma Style
getKDEUserPlasmaStyleCMD = "plasma-apply-desktoptheme --list-themes"

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
## Times
################################################################################
timeModeHours60 = ['0000', '0100', '0200', '0300', '0400', '0500', '0600', '0700',
                      '0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500',
                      '1600', '1700', '1800', '1900', '2000', '2100', '2200', '2300']
timeModeHours120 = ['0000', '0200', '0400', '0600', '0800', '1000', '1200', '1400',
                       '1600', '1800', '2000', '2200']
timeModeHours240 = ['0000', '0400', '0800', '1200', '1600', '2000']

################################################################################
## FIX
################################################################################# 
fixMinutes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

################################################################################
## LOCATION
################################################################################
homeUser = str(Path.home())
userName = getpass.getuser()
getHomeFolders = os.listdir(homeUser)

src_applications_location = f"{homeUser}/.local/share/applications"
src_autostart_folder_location = f"{homeUser}/.config/autostart"
src_flatpak_var_folder_location = f"{homeUser}/.var/app"
src_flatpak_local_folder_location = f"{homeUser}/.local/share/flatpak"

# KDE
src_color_scheme_folder_location = f"{homeUser}/.local/share/color-schemes"
src_plasma_style_folder_location = f"{homeUser}/.local/share/plasma/desktoptheme"

################################################################################
## PY
################################################################################
src_options_py = f"{homeUser}/.local/share/{appNameClose}/src/options.py"
src_schedule_py = f"{homeUser}/.local/share/{appNameClose}/src/schedule.py"
src_backup_check_py = f"{homeUser}/.local/share/{appNameClose}/src/backup_check.py"
src_main_window_py = f"{homeUser}/.local/share/{appNameClose}/src/mainwindow.py"
src_migration_assistant_py = f"{homeUser}/.local/share/{appNameClose}/src/migration_assistant.py"
src_call_migration_assistant_py = f"{homeUser}/.local/share/{appNameClose}/src/call_migration_assistant.py"
src_enter_time_machine_py = f"{homeUser}/.local/share/{appNameClose}/src/enter_time_machine.py"
src_package_backup_py = f"{homeUser}/.local/share/{appNameClose}/src/auto-package.py"
src_prepare_backup_py = f"{homeUser}/.local/share/{appNameClose}/src/prepare_backup.py"
src_update_py = f"{homeUser}/.local/share/{appNameClose}/src/update.py"
src_backup_now_py = f"{homeUser}/.local/share/{appNameClose}/src/backup_now.py"
src_system_tray_py = f"{homeUser}/.local/share/{appNameClose}/src/systemtray.py"
src_notification_py = f"{homeUser}/.local/share/{appNameClose}/src/notification.py"
src_search_for_devices_py = f"{homeUser}/.local/share/{appNameClose}/src/search_for_devices.py"
src_migration_assistant_py = f"{homeUser}/.local/share/{appNameClose}/src/migration_assistant.py"
src_restore_cmd_py = f"{homeUser}/.local/share/{appNameClose}/src/restore_cmd.py"

################################################################################
## Desktop
################################################################################
src_autostart_location = f"{homeUser}/.config/autostart/backup_check.desktop"
src_timemachine_desktop = f"{homeUser}/.local/share/applications/{appNameClose}.desktop"
src_migration_assistant_desktop = f"{homeUser}/.local/share/applications/migration_assistant.desktop"
src_backup_check_desktop = f"{homeUser}/.local/share/{appNameClose}/src/desktop/backup_check.desktop"

################################################################################
## Config
################################################################################
src_folder_timemachine = f"{homeUser}/.local/share/{appNameClose}"
src_user_config = f"{homeUser}/.local/share/{appNameClose}/src/ini/user.ini"
src_pycache = f"{homeUser}/.local/share/{appNameClose}/src/__pycache__"

################################################################################
## Icons
################################################################################
src_restore_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/restore_64px.svg"
src_monitor_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/applications-system.svg"
src_settings_up_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/laptop-symbolic.svg"
src_backup_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/backup_128px.png"
src_migration_assistant_icon_212px = f"{homeUser}/.local/share/{appNameClose}/src/icons/migration_assistant_212px.png"
src_migration_assistant_clean_icon_128px = f"{homeUser}/.local/share/{appNameClose}/src/icons/migration_assistant_clean_128px.svg"
src_system_bar_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/systemtrayicon.png"
src_system_bar_white_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/systemtraywhiteicon.png"
src_system_bar_run_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/systemtrayiconrun.png"
src_system_bar_error_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/systemtrayiconerror.png"
src_system_bar_restore_icon = f"{homeUser}/.local/share/{appNameClose}/src/icons/systemtrayiconrestore.png"

################################################################################
## TXT
################################################################################
# .Exclude-applications
src_exclude_applications = ".exclude-applications.txt"

# LOG
appLogTxt = f"{src_folder_timemachine}/logs.txt"

def signal_exit(*args):
    print("Updating INI settings... Exiting...")
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('BACKUP', 'backup_now', 'unfinished')
        config.set('BACKUP', 'checker_running', 'false')
        config.write(configfile)

    exit()
    
# Error fuction
def error_trying_to_backup(error):
    # Set notification_massage to 2
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('INFO', 'notification_massage', "2")
        config.set('INFO', 'notification_add_info', f"{error}")
        config.set('BACKUP', 'checker_running', 'false')
        config.write(configfile)

    print(error)
    exit()