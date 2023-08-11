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
import threading
import locale
import datetime
import sqlite3


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

# Remember to change INSTALL too!
################################################################################
## Variables
################################################################################
# Github
GITHUB_HOME = "https://www.github.com/geovanejefferson/timemachine"

# Names
APP_NAME = "Time Machine"
APP_NAME_CLOSE = "timemachine"
APP_VERSION = "v1.1.7.04 dev"
BASE_FOLDER_NAME = "TMB"
BACKUP_FOLDER_NAME = "backups"
APPLICATIONS_FOLDER_NAME = "applications"
WALLPAPER_FOLDER_NAME = "wallpaper"
ICONS_FOLDER_NAME = "icon"
FONTS_FOLDER_NAME = "fonts"
GTK_THEME_FOLDER_NAME = "gtktheme"
THEMES_FOLDER_NAME = "theme"
CURSORS_FOLDER_NAME = "cursor"
COLORSCHEMEFOLDERNAME = "color-schemes"
PLASMA_FOLDER_NAME = "plasma"
KDE_SCRIPT_FOLDER_NAME = "kde-scripts"
KDE_NOTES_FOLDER_NAME = "plasma-notes"
KDEGLOBALDSFOLDERNAME = "kdeglobals"
kGlobalShortcutSrcFolderName = "kglobalshortcutsrc"
kWinRcFolderName = "kwinrc"
GNOME_SHELL_FOLDER_NAME = "gnome-shell"
VAR_FOLDER_NAME = "var"
LOCAL_FOLDER_NAME = "share"
KDE_FOLDER_NAME = "kde"
GNOME_FOLDER_NAME = "gnome"
FLATPAK_FOLDER_NAME = "flatpak"

CONFIGURATIONS_FOLDER_NAME = "configurations"
SHARE_FOLDER_NAME = "share"

CONFIG_FOLDER_NAME = "config"
SHARE_CONFIG_FOLDER_NAME = "share_config"
FLATPAK_TXT = "flatpak.txt"
RESTORE_SETTINGS_INI = "restore_settings.ini"

DEB_FOLDER_NAME = "deb"
RPM_FOLDER_NAME = "rpm"

# CMD commands
COPY_RSYNC_CMD = "rsync -avr"
COPY_CP_CMD = "cp -rv"
CREATE_CMD_FOLDER = "mkdir"
CREATE_CMD_FILE = "touch"
GET_FLATPAKS_APPLICATIONS_NAME = "flatpak list --app --columns=application"
INSTALL_DEB = "sudo dpkg -i"
INSTALL_RPM = "sudo rpm -ivh --replacepkgs"
FLATPAK_INSTALL_CMD = "flatpak install --system --noninteractive --assumeyes --or-update"

# DE
SUPPORT_OS = ["gnome", "ubuntu", "ubuntu:gnome", "unity", "pop", "kde"]
SUPPORT_DEB_PACKAGES_MANAGER = ["debian", "ubuntu"]
SUPPORT_RPM_PACKAGE_MANAGER = ["fedora", "opensuse"]
GET_USER_DE = "echo $XDG_CURRENT_DESKTOP"
GET_USER_PACKAGE_MANAGER = "cat /etc/os-release"

# Theme
ICON_THEME_NAME = "Adwaita"

systemTrayPipeName = "/tmp/system_tray.pipe"
appPipeName = f"/tmp/{APP_NAME_CLOSE}.pipe"
backupNowPipeName = f"/tmp/backup_now.pipe"

################################################################################
# GNOME
################################################################################
DETECT_THEME_MODE = "gsettings get org.gnome.desktop.interface color-scheme"

GET_GNOME_WALLPAPER = "gsettings get org.gnome.desktop.background picture-uri"
GET_GNOME_WALLPAPER_DARK = "gsettings get org.gnome.desktop.background picture-uri-dark"

SET_GNOME_WALLPAPER = "gsettings set org.gnome.desktop.background picture-uri"
SET_GNOME_WALLPAPER_DARK = "gsettings set org.gnome.desktop.background picture-uri-dark"

ZOOM_GNOME_WALLPAPER = "gsettings set org.gnome.desktop.background picture-options zoom"

# Icon
GET_USER_ICON_CMD = "gsettings get org.gnome.desktop.interface icon-theme"
SET_USER_ICON_CMD = "gsettings set org.gnome.desktop.interface icon-theme"

# Theme
GET_USER_THEME_CMD = "gsettings get org.gnome.desktop.interface gtk-theme"
SET_USER_THEME_CMD = "gsettings set org.gnome.desktop.interface gtk-theme"

# Cursor
GET_USER_CURSOR_CMD = "gsettings get org.gnome.desktop.interface cursor-theme"
SET_USER_CURSOR_CMD = "gsettings set org.gnome.desktop.interface cursor-theme"

# Font
# gsettings set org.gnome.desktop.interface font-name "FreeSans Regular 11"
GET_USER_FONT_CMD = "gsettings get org.gnome.desktop.interface font-name"
# 'FreeSans Regular 11'
SET_USER_FONT_CMD = "gsettings get org.gnome.desktop.interface font-name"

################################################################################
# KDE
################################################################################
# Cursor
GET_KDE_USER_CURSOR_CMD = "plasma-apply-cursortheme --list-themes"
# Color Scheme
GET_KDE_USER_COLOR_SCHEME_CMD = "plasma-apply-colorscheme --list-schemes"
# Plasma Style
GET_KDE_USER_PLASMA_STYLE_CMD = "plasma-apply-desktoptheme --list-themes"

# Locations
MEDIA = "/media"
RUN = "/run/media"

# Fonts
MAIN_FONT = "Ubuntu"
BIGGER_FONT_SIZE = 12
NORMAL_FONT_SIZE = 10
SMALL_FONT_SIZE = 5


################################################################################
## Fonts
################################################################################
BIG_TITLE = QFont("DeJaVu Sans", 18)
TOP_TITLE = QFont("DeJaVu Sans", 10.5)
ITEM = QFont("Ubuntu", 10)

################################################################################
## Times
################################################################################
MULTIPLE_TIME_OPTION1 = ['0000', '0100', '0200', '0300', '0400', '0500', '0600', '0700',
                      '0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500',
                      '1600', '1700', '1800', '1900', '2000', '2100', '2200', '2300']

MULTIPLE_TIME_OPTION2 = ['0000', '0200', '0400', '0600', '0800', '1000', '1200', '1400',
                       '1600', '1800', '2000', '2200']

MULTIPLE_TIME_OPTION3 = ['0000', '0400', '0800', '1200', '1600', '2000']

################################################################################
## FIX
#################################################################################
FIX_MINUTES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

################################################################################
## Time options
#################################################################################
TIME1 = '60'
TIME2 = '120'
TIME3 = '240'

################################################################################
## LOCATION
################################################################################
HOME_USER = str(Path.home())
USERNAME = getpass.getuser()
GET_HOME_FOLDERS = os.listdir(HOME_USER)
GET_CURRENT_LOCATION = pathlib.Path().resolve()

DST_APPLICATIONS_LOCATION = f"{HOME_USER}/.local/share/applications"
SRC_AUTOSTART_FOLDER_LOCATION = f"{HOME_USER}/.config/autostart"
src_flatpak_var_folder_location = f"{HOME_USER}/.var/app"
src_flatpak_local_folder_location = f"{HOME_USER}/.local/share/flatpak"

# KDE
src_color_scheme_folder_location = f"{HOME_USER}/.local/share/color-schemes"
src_plasma_style_folder_location = f"{HOME_USER}/.local/share/plasma/desktoptheme"

SRC_AUTOSTARTFOLDER_LOCATION=f"{HOME_USER}/.config/autostart"

################################################################################
## PY
################################################################################
src_options_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/options.py"
src_schedule_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/schedule.py"
SRC_BACKUP_CHECKER_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/backup_checker.py"
SRC_MAIN_WINDOW_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/mainwindow.py"
SRC_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/migration_assistant.py"
SRC_CALL_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/call_migration_assistant.py"
src_enter_time_machine_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/enter_time_machine.py"
src_enter_time_machine_test_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/test.py"
src_package_backup_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/auto-package.py"
src_prepare_backup_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/prepare_backup.py"
src_update_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/update.py"
src_backup_now_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/backup_now.py"
src_system_tray_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/systemtray.py"
src_notification_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/notification.py"
src_search_for_devices_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/search_for_devices.py"
src_restore_cmd_py = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/restore_cmd.py"

################################################################################
## Desktop
################################################################################
# Source
SRC_TIMEMACHINE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"

src_autostart_location = f"desktop/backup_check.desktop"
# SRC_TIMEMACHINE_DESKTOP = f"desktop/{APP_NAME_CLOSE}.desktop"
src_migration_assistant_desktop = "desktop/migration_assistant.desktop"
src_backup_check_desktop = f"desktop/backup_check.desktop"


# Destination
dst_autostart_location = f"{HOME_USER}/.config/autostart/backup_check.desktop"
DST_BACKUP_CHECK_DESKTOP = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"
DST_FILE_EXE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP = f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"

################################################################################
## Config
################################################################################
DST_FOLDER_INSTALL = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}"
SRC_USER_CONFIG = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/ini/config.ini"
SRC_USER_CONFIG_DB = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/ini/config.db"
src_pycache = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/__pycache__"

################################################################################
## Icons
################################################################################
SRC_RESTORE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/restore_64px.svg"
src_monitor_icon = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/applications-system.svg"
src_settings_up_icon = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/laptop-symbolic.svg"
SRC_BACKUP_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/backup_128px.png"
SRC_MIGRATION_ASSISTANT_ICON_212PX = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/migration_assistant_212px.png"
src_migration_assistant_clean_icon_128px = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/migration_assistant_clean_128px.svg"
src_system_bar_icon = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayicon.png"
src_system_bar_white_icon = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtraywhiteicon.png"
SRC_SYSTEM_BAR_RUN_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayiconrun.png"
src_system_bar_error_icon = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayiconerror.png"
src_system_bar_restore_icon = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayiconrestore.png"

################################################################################
## TXT
################################################################################
# .Exclude-applications
SRC_EXCLUDE_APPLICATIONS = ".exclude-applications.txt"

# LOG
APP_LOGS = f"{DST_FOLDER_INSTALL}/app_logs.txt"

def signal_exit(*args):
    print("Updating INI settings...")
    print("Exiting...")

    CONFIG = configparser.ConfigParser()
    CONFIG.read(SRC_USER_CONFIG)
    with open(SRC_USER_CONFIG, 'w') as configfile:
        CONFIG.set('STATUS', 'unfinished_backup', 'Yes')
        CONFIG.write(configfile)

    # Quit
    exit()

def error_trying_to_backup(e):
    CONFIG = configparser.ConfigParser()
    CONFIG.read(SRC_USER_CONFIG)
    with open(SRC_USER_CONFIG, 'w') as configfile:
        CONFIG.set('INFO', 'saved_notification', f"{e}")
        CONFIG.write(configfile)

    # Quit
    exit()


