import subprocess as sub
import configparser
import shutil
import getpass
import datetime
import os
import sys
import images

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

home_user = str(Path.home())
user_name = getpass.getuser()

#SRC LOCATION 
src_schedule_py = "src/schedule.py"
src_backup_py = "src/backup_check.py"
src_restore_icon = "src/icons/restore_48.png"
src_backup_py = "src/backup_check.py"
src_user_config = "src/user.ini"
src_where_py  = "src/where.py"
src_backup_now = "src/backup_now.py"
src_folders_py = "src/folders.py"
src_backup_icon = "src/icons/backup.png"
src_backup_check = "src/backup_check.desktop"
src_backup_check_py  = "src/backup_check.py"
src_backup_check_desktop = home_user+"/.config/autostart/backup_check.desktop"
src_ui = "src/gui.ui"

#DST LOCATION
# dst_schedule_py = home_user+"/.local/share/timemachine/src/schedule.py"
# dst_backup_check_py  = home_user+"/.local/share/timemachine/src/backup_check.py"
# dst_backup_check_desktop = home_user+"/.config/autostart/backup_check.desktop"
# dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"
# dst_restore_icon = home_user+"/.local/share/timemachine/src/icons/restore_48.png"
# dst_backup_icon = home_user+"/.local/share/timemachine/src/icons/backup.png"
# dst_folders_py = home_user+"/.local/share/timemachine/src/folders.py"
# dst_where_py  = home_user+"/.local/share/timemachine/src/where.py"
# dst_backup_now = home_user+"/.local/share/timemachine/src/backup_now.py" 
# dst_backup_check = home_user+"/.local/share/timemachine/src/backup_check.desktop"
# dst_ui = home_user+"/.local/share/timemachine/src/gui.ui"

#GET HOUR, MINUTE
now = datetime.datetime.now()
day_name = (now.strftime("%a"))
current_hour = now.strftime("%H")
current_hour = str(current_hour)
current_minute = now.strftime("%M")
current_minute = str(current_minute)

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

#TIMER
timer = QtCore.QTimer()

class TimeMachine(QMainWindow):
    def __init__(self):
        super(TimeMachine, self).__init__()
        loadUi(src_ui,self)
        self.auto_checkbox.clicked.connect(self.on_backup_automatically_toggled)
        self.button_disk.clicked.connect(self.on_selected_backup_disk_clicked)
        self.button_schedule.clicked.connect(self.on_schedule_clicked)
        self.button_folders.clicked.connect(self.on_folders_clicked)
        
        #TIMER
        timer.timeout.connect(self.updates)
        timer.start(1000) # update every second
        self.updates()

    def updates(self):
        #Read/Load user.config
        config.read(src_user_config)
        auto_backup = config['DEFAULT']['auto_backup'] 
        read_hd_name = config['EXTERNAL']['name']     
        read_last_backup = config['INFO']['latest']
        read_next_backup = config['INFO']['next']

        #VAR#        
        next_day = "None"
        next_hour  = (config.get('SCHEDULE', 'hours'))
        next_minute  = (config.get('SCHEDULE', 'minutes'))
        read_next_backup_sun = (config.get('SCHEDULE', 'sun'))
        read_next_backup_mon = (config.get('SCHEDULE', 'mon'))
        read_next_backup_tue = (config.get('SCHEDULE', 'tue'))
        read_next_backup_wed = (config.get('SCHEDULE', 'wed'))
        read_next_backup_thu = (config.get('SCHEDULE', 'thu'))
        read_next_backup_fri = (config.get('SCHEDULE', 'fri'))
        read_next_backup_sat= (config.get('SCHEDULE', 'sat'))
        self.button_backup_now = QPushButton("Back Up Now",self)
        self.button_backup_now.setGeometry(430, 150, 120, 30)
        self.button_backup_now.clicked.connect(self.on_button_backup_now_clicked)

        #AUTO BACKUP
        if auto_backup == "true":
            self.auto_checkbox.setChecked(True)

        #EXTERNAL NAME
        if read_hd_name != "":
            self.label_usb_name.setText(read_hd_name)
            self.label_usb_name.setFont(QFont('Arial', 18))
            self.button_backup_now.show()
        else:
            self.button_backup_now.hide()
        
        #LAST BACKUP LABEL
        if read_last_backup == "":
            self.label_last_backup.setText("Last backup: None")
            self.label_last_backup.setFont(QFont('Arial', 10))
        else:
            self.label_last_backup.setText("Last backup: "+read_last_backup)
            self.label_last_backup.setFont(QFont('Arial', 10))

        #NEXT BACKUP LABEL
        if read_next_backup == "":
            self.label_next_backup.setText("Next backup: None")
            self.label_next_backup.setFont(QFont('Arial', 10))
        else:
            self.label_next_backup.setText("Next backup: "+read_next_backup)
            self.label_next_backup.setFont(QFont('Arial', 10))  

        print("Current time:"+current_hour+":"+current_minute)
        print("Day:"+day_name)

        if day_name == "Mon":
            if read_next_backup_mon == "true" and current_hour <= next_hour and current_minute <= next_minute:
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
            if read_next_backup_tue == "true" and current_hour <= next_hour and current_minute <= next_minute:
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
            if read_next_backup_wed == "true" and current_hour <= next_hour and current_minute <= next_minute:
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
            if read_next_backup_thu == "true" and current_hour <= next_hour and current_minute <= next_minute:
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
            if read_next_backup_fri == "true" and current_hour <= next_hour and current_minute <= next_minute:
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
            if read_next_backup_sat == "true" and current_hour <= next_hour and current_minute <= next_minute:
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

        #AVA NEXT BACKUP TO INI FILE
        config.read(src_user_config)
        cfgfile = open(src_user_config, 'w')
        config.set('INFO', 'next', next_day+', '+next_hour+':'+next_minute)
        config.write(cfgfile)  
        cfgfile.close()

    def on_selected_backup_disk_clicked(self, button):
        #CHOOSE EXTERNAL HD
        sub.call("python3 "+src_where_py,shell=True)

    def on_backup_automatically_toggled(self):
        #AUTOMATICALLY BACKUP SELECTED
        if self.auto_checkbox.isChecked():
            if os.path.exists(src_backup_check_desktop):
                pass
            else:
                #COPY SRC .DESKTOP TO DST .DESKTOP
                shutil.copy(src_backup_check,src_backup_check_desktop)
                #NOTIFICATION
                sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup was activated!' 5",shell=True)
                print("Auto backup was successfully activated!")
                
                #SET AUTO BACKUP TO TRUE
                cfgfile = open(src_user_config, 'w')
                config.set('DEFAULT', 'auto_backup', 'true')
                config.write(cfgfile)
                cfgfile.close()
        else:
            #REMOVE .DESKTOP FROM DST
            sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Auto backup was deactivated!' 5",shell=True)
            print("Auto backup was successfully deactivated!")
            sub.Popen("rm "+src_backup_check_desktop,shell=True)

            #SET AUTO BACKUP TO FALSE
            cfgfile = open(src_user_config, 'w')
            config.set('DEFAULT', 'auto_backup', 'false')
            config.write(cfgfile)
            cfgfile.close()

        #START BACKUP CHECK
        sub.Popen("python3 "+src_backup_check_py,shell=True)

    def on_schedule_clicked(self, button):
        #CALL SCHEDULE
        sub.call("python3 "+src_schedule_py,shell=True)

    def on_folders_clicked(self, button):
        #CALL FOLDERS SELECTOR
        sub.call("python3 "+src_folders_py,shell=True)   

    def on_button_backup_now_clicked(self, button):
        #SET BACKUP NOW TO TRUE
        config.read(src_user_config)
        cfgfile = open(src_user_config, 'w')
        config.set('DEFAULT', 'backup_now', 'true')
        config.write(cfgfile)
        cfgfile.close()

        #START BACKUP NOW
        sub.Popen("python3 "+src_backup_now,shell=True)

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