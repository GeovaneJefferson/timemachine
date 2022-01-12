import subprocess as sub
import configparser
import shutil
import getpass
import os
import sys
import images

from datetime import datetime
from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

home_user = str(Path.home())
user_name = getpass.getuser()

# SRC LOCATION
# src_options_py = "src/options.py"
# src_backup_py = "src/backup_check.py"
# src_restore_icon = "src/icons/restore_48.png"
# src_backup_py = "src/backup_check.py"
# src_user_config = "src/user.ini"
# src_where_py  = "src/where.py"
# src_backup_now = "src/backup_now.py"
# src_folders_py = "src/options.py"
# src_backup_icon = "src/icons/backup.png"
# src_backup_check = "src/backup_check.desktop"
# src_backup_check_py  = "src/backup_check.py"
# src_backup_check_desktop = home_user+"/.config/autostart/backup_check.desktop"
# src_ui = "src/gui.ui"

# DST LOCATION
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

# GET HOUR, MINUTE
now = datetime.now()
day_name = now.strftime("%a")
current_hour = now.strftime("%H")
current_minute = now.strftime("%M")

# CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

# TIMER
timer = QtCore.QTimer()


class TimeMachine(QMainWindow):
    def __init__(self):
        super(TimeMachine, self).__init__()
        loadUi(src_ui, self)
        self.auto_checkbox.clicked.connect(self.on_backup_automatically_toggled)
        self.button_disk.clicked.connect(self.on_selected_backup_disk_clicked)
        self.button_options.clicked.connect(self.on_options_clicked)
        self.button_donate.clicked.connect(self.on_button_donate_clicked)

        # BACKUP NOW BUTTON
        self.button_backup_now = QPushButton("Back Up Now", self)
        self.button_backup_now.setGeometry(452, 157, 120, 34)
        self.button_backup_now.clicked.connect(self.on_button_backup_now_clicked)

        # TIMER
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

    def updates(self):
        # READ INI FILE
        config.read(src_user_config)
        auto_backup = config['DEFAULT']['auto_backup']
        read_hd_name = config['EXTERNAL']['name']
        read_last_backup = config['INFO']['latest']
        read_next_backup = config['INFO']['next']
        more_time_mode = config['MODE']['more_time_mode']
        everytime = config['SCHEDULE']['everytime']

        # VAR
        next_day = "None"
        next_hour = (config.get('SCHEDULE', 'hours'))
        next_minute = (config.get('SCHEDULE', 'minutes'))
        read_next_backup_sun = (config.get('SCHEDULE', 'sun'))
        read_next_backup_mon = (config.get('SCHEDULE', 'mon'))
        read_next_backup_tue = (config.get('SCHEDULE', 'tue'))
        read_next_backup_wed = (config.get('SCHEDULE', 'wed'))
        read_next_backup_thu = (config.get('SCHEDULE', 'thu'))
        read_next_backup_fri = (config.get('SCHEDULE', 'fri'))
        read_next_backup_sat = (config.get('SCHEDULE', 'sat'))

        total_current_time = current_hour + current_minute
        total_next_time = next_hour + next_minute

        print(total_current_time)
        print(total_next_time)

        # AUTO BACKUP
        if auto_backup == "true":
            self.auto_checkbox.setChecked(True)

        # SET HD NAME TO LABEL
        self.label_usb_name.setText(read_hd_name)
        self.label_usb_name.setFont(QFont('Arial', 18))

        try:
            # CHECK IF EXTERNAL CAN BE FOUND
            os.listdir("/media/" + user_name + "/" + read_hd_name)
            # EXTERNAL NAME AND STATUS
            if read_hd_name != "":
                self.label_usb_name.setText(read_hd_name)
                self.label_usb_name.setFont(QFont('Arial', 18))
                # SHOW BACKUP NOW BUTTON
                self.button_backup_now.show()
                # SET NAME AND COLOR
                self.label_external_hd.setText("External HD: Conected")
                self.label_external_hd.setFont(QFont('Arial', 10))
                palette = self.label_external_hd.palette()
                color = QColor('Green')
                palette.setColor(QPalette.Foreground, color)
                self.label_external_hd.setPalette(palette)
            else:
                self.button_backup_now.hide()
        except FileNotFoundError:
            # HIDE BACKUP NOW BUTTON
            self.button_backup_now.hide()
            # SET NAME AND COLOR
            self.label_external_hd.setText("External HD: Disconected")
            palette = self.label_external_hd.palette()
            color = QColor('Red')
            palette.setColor(QPalette.Foreground, color)
            self.label_external_hd.setPalette(palette)

            # LAST BACKUP LABEL
        if read_last_backup == "":
            self.label_last_backup.setText("Last Backup: None")
            self.label_last_backup.setFont(QFont('Arial', 10))
        else:
            self.label_last_backup.setText("Last Backup: " + read_last_backup)
            self.label_last_backup.setFont(QFont('Arial', 10))

        # NEXT BACKUP LABEL
        if read_next_backup == "":
            self.label_next_backup.setText("Next Backup: None")
            self.label_next_backup.setFont(QFont('Arial', 10))
        else:
            self.label_next_backup.setText("Next Backup: " + read_next_backup)
            self.label_next_backup.setFont(QFont('Arial', 10))

            # NEXT BACKUP LABEL(EVERYTIME)
        if more_time_mode == "true" and everytime == "15":
            self.label_next_backup.setText("Next Backup: Every 15 minutes")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "30":
            self.label_next_backup.setText("Next Backup: Every 30 minutes")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "60":
            self.label_next_backup.setText("Next Backup: Every 1 hour")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "120":
            self.label_next_backup.setText("Next Backup: Every 2 hours")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "240":
            self.label_next_backup.setText("Next Backup: Every 4 hours")
            self.label_next_backup.setFont(QFont('Arial', 10))

        # PRINT CURRENT TIME AND DAY
        print("Current time:" + current_hour + ":" + current_minute)
        print("Day:" + day_name)

        if day_name == "Sun":
            if read_next_backup_sun == "true" and current_hour <= next_hour and current_minute <= next_minute:
                next_day = "Today"
            else:
                if read_next_backup_mon == "true":
                    next_day = "Mon"
                elif read_next_backup_tue == "true":
                    next_day = "Tue"
                elif read_next_backup_wed == "true":
                    next_day = "Wed"
                elif read_next_backup_thu == "true":
                    next_day = "Thu"
                elif read_next_backup_fri == "true":
                    next_day = "Fri"
                elif read_next_backup_sat == "true":
                    next_day = "Sat"
                elif read_next_backup_sun == "true":
                    next_day = "Sun"

        if day_name == "Mon":
            if read_next_backup_mon == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if read_next_backup_tue == "true":
                    next_day = "Tue"
                elif read_next_backup_wed == "true":
                    next_day = "Wed"
                elif read_next_backup_thu == "true":
                    next_day = "Thu"
                elif read_next_backup_fri == "true":
                    next_day = "Fri"
                elif read_next_backup_sat == "true":
                    next_day = "Sat"
                elif read_next_backup_sun == "true":
                    next_day = "Sun"
                elif read_next_backup_mon == "true":
                    next_day = "Mon"

        if day_name == "Tue":
            if read_next_backup_tue == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if read_next_backup_wed == "true":
                    next_day = "Wed"
                elif read_next_backup_thu == "true":
                    next_day = "Thu"
                elif read_next_backup_fri == "true":
                    next_day = "Fri"
                elif read_next_backup_sat == "true":
                    next_day = "Sat"
                elif read_next_backup_sun == "true":
                    next_day = "Sun"
                elif read_next_backup_mon == "true":
                    next_day = "Mon"
                elif read_next_backup_tue == "true":
                    next_day = "Tue"

        if day_name == "Wed":
            if read_next_backup_wed == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if read_next_backup_thu == "true":
                    next_day = "Thu"
                elif read_next_backup_fri == "true":
                    next_day = "Fri"
                elif read_next_backup_sat == "true":
                    next_day = "Sat"
                elif read_next_backup_sun == "true":
                    next_day = "Sun"
                elif read_next_backup_mon == "true":
                    next_day = "Mon"
                elif read_next_backup_tue == "true":
                    next_day = "Tue"
                elif read_next_backup_wed == "true":
                    next_day = "Wed"

        if day_name == "Thu":
            if read_next_backup_thu == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if read_next_backup_fri == "true":
                    next_day = "Fri"
                elif read_next_backup_sat == "true":
                    next_day = "Sat"
                elif read_next_backup_sun == "true":
                    next_day = "Sun"
                elif read_next_backup_mon == "true":
                    next_day = "Mon"
                elif read_next_backup_tue == "true":
                    next_day = "Tue"
                elif read_next_backup_wed == "true":
                    next_day = "Wed"
                elif read_next_backup_thu == "true":
                    next_day = "Thu"

        if day_name == "Fri":
            if read_next_backup_fri == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if read_next_backup_sat == "true":
                    next_day = "Sat"
                elif read_next_backup_sun == "true":
                    next_day = "Sun"
                elif read_next_backup_mon == "true":
                    next_day = "Mon"
                elif read_next_backup_tue == "true":
                    next_day = "Tue"
                elif read_next_backup_wed == "true":
                    next_day = "Wed"
                elif read_next_backup_thu == "true":
                    next_day = "Thu"
                elif read_next_backup_fri == "true":
                    next_day = "Fri"

        if day_name == "Sat":
            if read_next_backup_sat == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if read_next_backup_sun == "true":
                    next_day = "Sun"
                elif read_next_backup_mon == "true":
                    next_day = "Mon"
                elif read_next_backup_tue == "true":
                    next_day = "Tue"
                elif read_next_backup_wed == "true":
                    next_day = "Wed"
                elif read_next_backup_thu == "true":
                    next_day = "Thu"
                elif read_next_backup_fri == "true":
                    next_day = "Fri"
                elif read_next_backup_sat == "true":
                    next_day = "Sat"

        # SAVE NEXT BACKUP TO INI FILE
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'next', next_day + ', ' + next_hour + ':' + next_minute)
            config.write(configfile)

    def on_selected_backup_disk_clicked(self):
        # CHOOSE EXTERNAL HD
        sub.call("python3 " + src_where_py, shell=True)

    def on_backup_automatically_toggled(self):
        # AUTOMATICALLY BACKUP SELECTED
        if self.auto_checkbox.isChecked():
            if os.path.exists(src_backup_check_desktop):
                pass
            else:
                # COPY SRC .DESKTOP TO DST .DESKTOP
                shutil.copy(src_backup_check, src_backup_check_desktop)
                # NOTIFICATION
                sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup was activated!' 5", shell=True)
                print("Auto backup was successfully activated!")

                # SET AUTO BACKUP TO TRUE
                with open(src_user_config, 'w') as configfile:
                    config.set('DEFAULT', 'auto_backup', 'true')
                    config.write(configfile)
        else:
            # REMOVE .DESKTOP FROM DST
            sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup was deactivated!' 5", shell=True)
            print("Auto backup was successfully deactivated!")
            sub.Popen("rm " + src_backup_check_desktop, shell=True)

            # SET AUTO BACKUP TO FALSE
            with open(src_user_config, 'w') as configfile:
                config.set('DEFAULT', 'auto_backup', 'false')
                config.write(configfile)

                # START BACKUP CHECK
        sub.Popen("python3 " + src_backup_check_py, shell=True)

    def on_options_clicked(self):
        # CALL SCHEDULE
        sub.call("python3 " + src_options_py, shell=True)

    def on_button_backup_now_clicked(self):
        # SET BACKUP NOW TO TRUE
        with open(src_user_config, 'w') as configfile:
            config.set('DEFAULT', 'backup_now', 'true')
            config.write(configfile)

            # START BACKUP NOW
        sub.Popen("python3 " + src_backup_now, shell=True)

    def on_button_donate_clicked(self):
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)


app = QApplication(sys.argv)
main_screen = TimeMachine()
widget = QtWidgets.QStackedWidget()
appIcon = QIcon(src_restore_icon)
widget.setWindowIcon(appIcon)
widget.addWidget(main_screen)
widget.setFixedHeight(450)
widget.setFixedWidth(700)
widget.setWindowTitle("Time Machine")
widget.show()
app.exit(app.exec_())
