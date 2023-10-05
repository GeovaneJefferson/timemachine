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
import logging
import traceback

from stylesheet import *
from pathlib import Path
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui


from PySide6.QtCore import (
    Qt, QSize, QRect, QPropertyAnimation,
    QEasingCurve, QPoint, QSocketNotifier, QDir, QTimer,
    QResource)

from PySide6.QtGui import (
    QFont, QPixmap , QIcon, QMovie, QAction,
    QPalette, QColor,QCursor,QImage,QImageReader,
    QTextCursor)

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QApplication,
    QPushButton, QLabel, QCheckBox, QLineEdit,
    QWidget, QFrame, QGridLayout, QHBoxLayout,
    QVBoxLayout, QMessageBox, QRadioButton,
    QScrollArea, QSpacerItem, QSizePolicy,
    QSpinBox, QComboBox, QGraphicsBlurEffect,
    QSystemTrayIcon, QMenu, QStackedWidget,QListView,
    QFileSystemModel,QDialog,QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QAbstractItemView,
    QButtonGroup
    )
from PySide6.QtSvgWidgets import QSvgWidget

timer = QtCore.QTimer()

# Remember to change INSTALL too!
################################################################################
## Variables
################################################################################
# Github
GITHUB_HOME = "https://github.com/GeovaneJefferson/timemachine/issues"

# Names
APP_NAME = "Time Machine"
APP_NAME_CLOSE = "timemachine"
APP_VERSION = "v1.1.6.093 dev"
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
GNOME_SHELL_FOLDER_NAME = "gnome-shell"
VAR_FOLDER_NAME = "var"
KDE_FOLDER_NAME = "kde"
GNOME_FOLDER_NAME = "gnome"
FLATPAK_FOLDER_NAME = "flatpak"

CONFIGURATIONS_FOLDER_NAME = "configurations"

CONFIG_FOLDER_NAME = "config"
SHARE_FOLDER_NAME = "share"
SHARE_CONFIG_FOLDER_NAME = 'share_config'
FLATPAK_TXT = "flatpak.txt"
RESTORE_SETTINGS_INI = "restore_settings.ini"

DEB_FOLDER_NAME = "deb"
RPM_FOLDER_NAME = "rpm"

# Flatpak
GET_FLATPAKS_APPLICATIONS_NAME = "flatpak list --app --columns=application"

# DE
SUPPORT_OS = ["gnome", "ubuntu", "ubuntu:gnome",
            "unity", "pop", "kde","zorin:gnome", 
            "pop:gnome", "budgie:gnome"]
GET_USER_DE = "echo $XDG_CURRENT_DESKTOP"
GET_USER_PACKAGE_MANAGER = "cat /etc/os-release"

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

################################################################################
# Location
################################################################################
MEDIA = "/media"
RUN = "/run/media"

################################################################################
## Fonts
################################################################################
MAIN_FONT = "Ubuntu"

################################################################################
## Times
################################################################################
MILITARY_TIME_OPTION = [
    '0000', '0100', '0200', '0300', '0400', '0500', '0600', '0700',
    '0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500',
    '1600', '1700', '1800', '1900', '2000', '2100', '2200', '2300']

################################################################################
## Time
#################################################################################
# Time left to calculate 'time left'
TIME_LEFT_WINDOW = 10  # Minutes

################################################################################
## LOCATION
################################################################################
HOME_USER = str(Path.home())
USERNAME = getpass.getuser()
GET_HOME_FOLDERS = os.listdir(HOME_USER)
GET_CURRENT_LOCATION = pathlib.Path().resolve()

DST_APPLICATIONS_LOCATION = f"{HOME_USER}/.local/share/applications"
SRC_AUTOSTART_FOLDER_LOCATION = f"{HOME_USER}/.config/autostart"
SRC_FLATPAK_VAR_FOLDER_LOCATION = f"{HOME_USER}/.var/app"
SRC_FLATPAK_LOCAL_FOLDER_LOCATION = f"{HOME_USER}/.local/share/flatpak"

# AUTOSTART
SRC_AUTOSTARTFOLDER_LOCATION=f"{HOME_USER}/.config/autostart"

################################################################################
## PY
################################################################################
SRC_ANALYSE_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/analyse.py"
SRC_BACKUP_CHECKER_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/backup_checker.py"
SRC_MAIN_WINDOW_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/main_window.py"
SRC_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/migration_assistant.py"
SRC_CALL_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/call_migration_assistant.py"
SRC_ENTER_TIME_MACHINE_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/new_enter_time_machine.py"
SRC_PREPARE_BACKUP_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/prepare_backup.py"
SRC_UPDATE_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/update.py"
SRC_BACKUP_NOW_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/backup_now.py"
SRC_SYSTEM_TRAY_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/systemtray.py"
SRC_RESTORE_CMD_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/restore_cmd.py"

################################################################################
## Desktop
################################################################################
# Destination
DST_AUTOSTART_LOCATION = f"{HOME_USER}/.config/autostart/backup_check.desktop"
DST_BACKUP_CHECK_DESKTOP = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"
DST_FILE_EXE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP = f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"

################################################################################
## Config
################################################################################
DST_FOLDER_INSTALL = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}"
SRC_USER_CONFIG_DB = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/ini/config.db"
SRC_PYCACHE = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/__pycache__"

################################################################################
## Icons
################################################################################
SRC_RESTORE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/restore_64px.svg"
SRC_MONITOR_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/applications-system.svg"
SRC_LAPTOP_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/laptop-symbolic.svg"
SRC_BACKUP_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/backup_128px.png"
SRC_MIGRATION_ASSISTANT_ICON_212PX = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/migration_assistant_212px.png"
SRC_SYSTEM_BAR_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayicon.png"
SRC_SYSTEM_BAR_WHITE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtraywhiteicon.png"
SRC_SYSTEM_BAR_RUN_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayiconrun.png"
SRC_SYSTEM_BAR_ERROR_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayiconerror.png"
SRC_SYSTEM_BAR_RESTORE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/systemtrayiconrestore.png"
SRC_ARROW_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/arrow.png"
SRC_HARDISK_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/harddisk.svg"
SRC_DONE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/check.png"

################################################################################
## TXT
################################################################################
# .Exclude-applications
SRC_EXCLUDE_APPLICATIONS = ".exclude-applications.txt"
SRC_EXCLUDE_FLATPAKS = ".exclude-flatpaks.txt"

# Log
LOG_LOCATION = f'{HOME_USER}/.log_time_machine.txt' 

# File extensions
TXT_TYPES = [
    "txt", "py", "cpp", "h", "c", "cgi",
    "cs", "class", "java", "php", "sh",
    "swift", "vb", "doc", "docx", "odt",
    "pdf", "rtf", "tex", "wpd"
]

IMAGE_TYPES = [
    "png", "jpg", "jpeg", "webp", "gif", "svg",
    "eps", "pdf", "ai", "raw", "tiff",
    "bmp", "ps", "tif"
]