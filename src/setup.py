import getpass
import os
import subprocess as sub
import configparser
import shutil
import sys

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QFont, QPixmap, QIcon

app_name = "Time Machine"
home_user = str(Path.home())
user_name = getpass.getuser()
local_media = os.listdir("/media/" + user_name + "/")
min_fix = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# To edit locally
# src_options_py = home_user + "/Dropbox/Python-Projects/timemachine/src/options.py"
# src_backup_py = home_user + "/Dropbox/Python-Projects/timemachine/src/backup_check.py"
# src_restore_icon = home_user + "/Dropbox/Python-Projects/timemachine/src/icons/restore_48.png"
# src_user_config = home_user + "/Dropbox/Python-Projects/timemachine/src/user.ini"
# src_where_py = home_user + "/Dropbox/Python-Projects/timemachine/src/where.py"
# src_backup_now = home_user + "/Dropbox/Python-Projects/timemachine/src/backup_now.py"
# src_ui_where = home_user + "/Dropbox/Python-Projects/timemachine/src/where.ui"
# src_restore_small_icon = home_user + "/Dropbox/Python-Projects/timemachine/src/icons/restore_small.png"
# src_folders_py = home_user + "/Dropbox/Python-Projects/timemachine/src/options.py"
# src_backup_icon = home_user + "/Dropbox/Python-Projects/timemachine/src/icons/backup.png"
# src_backup_check = home_user + "/Dropbox/Python-Projects/timemachine/src/backup_check.desktop"
# src_backup_check_py = home_user + "/Dropbox/Python-Projects/timemachine/src/backup_check.py"
# src_backup_check_desktop = home_user + "/.config/autostart/backup_check.desktop"
# src_ui = home_user + "/Dropbox/Python-Projects/timemachine/src/gui.ui"
# src_ui_options = home_user + "/Dropbox/Python-Projects/timemachine/src/options.ui"

# Home location
src_options_py = home_user + "/.local/share/timemachine/src/options.py"
src_schedule_py = home_user + "/.local/share/timemachine/src/schedule.py"
src_backup_check_py = home_user + "/.local/share/timemachine/src/backup_check.py"
src_backup_check_desktop = home_user + "/.config/autostart/backup_check.desktop"
src_user_config = home_user + "/.local/share/timemachine/src/user.ini"
src_restore_icon = home_user + "/.local/share/timemachine/src/icons/restore_48.png"
src_backup_icon = home_user + "/.local/share/timemachine/src/icons/backup.png"
src_folders_py = home_user + "/.local/share/timemachine/src/folders.py"
src_where_py = home_user + "/.local/share/timemachine/src/where.py"
src_backup_now = home_user + "/.local/share/timemachine/src/backup_now.py"
src_backup_check = home_user + "/.local/share/timemachine/src/backup_check.desktop"
src_ui = home_user + "/.local/share/timemachine/src/gui.ui"
src_ui_where = home_user + "/.local/share/timemachine/src/where.ui"
src_restore_small_icon = home_user + "/.local/share/timemachine/src/icons/restore_small.png"
src_ui_options = home_user + "/.local/share/timemachine/src/options.ui"
src_backup_py = home_user + "/.local/share/timemachine/src/backup_check.py"

