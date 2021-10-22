import configparser
import subprocess as sub
import getpass
import sys

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

home_user = str(Path.home())
user_name = getpass.getuser()

min_fix = ["0","1","2","3","4","5","6","7","8","9"]

#SRC LOCATION 
src_backup_check_py = "src/backup_check.py"
src_user_config = "src/user.ini"

#DST LOCATION
# dst_backup_check_py = home_user+"/.local/share/timemachine/src/backup_check.py"
# dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

class Schedule(QMainWindow):
    def __init__(self):
        super(Schedule, self).__init__()
        loadUi("src/schedule.ui",self)
        self.button_save.clicked.connect(self.on_save_clicked)
        self.label_hours.valueChanged.connect(self.label_hours_changed)
        self.label_minutes.valueChanged.connect(self.label_minutes_changed)

        config.read(src_user_config)
        
        #---read hours to show saved time---#        
        hrs = (config.get('SCHEDULE', 'hours'))
        hrs = int(hrs)
        self.label_hours.setValue(hrs)

        #---read minutes to show saved time---#        
        min = (config.get('SCHEDULE', 'minutes'))
        min = int(min)
        self.label_minutes.setValue(min)   

        #---read hours to show saved time---#        
        sun = config['SCHEDULE']['sun']
        if sun == "true":
            self.check_sun.setChecked(True) 
        mon = config['SCHEDULE']['mon']
        if mon == "true":
            self.check_mon.setChecked(True) 
        tue = config['SCHEDULE']['tue']
        if tue == "true":
            self.check_tue.setChecked(True) 
        wed = config['SCHEDULE']['wed']
        if wed == "true":
            self.check_wed.setChecked(True) 
        thu = config['SCHEDULE']['thu']
        if thu == "true":
            self.check_thu.setChecked(True) 
        fri = config['SCHEDULE']['fri']
        if fri == "true":
            self.check_fri.setChecked(True) 
        sat = config['SCHEDULE']['sat']
        if sat == "true":
            self.check_sat.setChecked(True) 

    def on_check_sun_clicked(self):
        if self.check_sun.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'sun', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Sun")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'sun', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_check_mon_clicked(self):
        if self.check_mon.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'mon', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Mon")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'mon', 'false')
            config.write(cfgfile)
            cfgfile.close()        
            print("Mon")

    def on_check_tue_clicked(self):
        if self.check_tue.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'tue', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Tue")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'tue', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_check_wed_clicked(self):
        if self.check_wed.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'wed', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Wed")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'wed', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_check_thu_clicked(self):
        if self.check_thu.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'thu', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Thu")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'thu', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_check_fri_clicked(self):
        if self.check_fri.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'fri', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Fri")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'fri', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_check_sat_clicked(self):
        if self.check_sat.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'sat', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Sat")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'sat', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def label_hours_changed(self):
        hours = self.label_hours.value()
        hours = str(hours)
        print((str(hours)))

        cfgfile = open(src_user_config, 'w')
        config.set('SCHEDULE', 'hours', hours)
        config.write(cfgfile)
        cfgfile.close()
        
        if hours in min_fix:
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'hours', '0'+hours)
            config.write(cfgfile)
            cfgfile.close()

    def label_minutes_changed(self):
        minutes = self.label_minutes.value()
        minutes = str(minutes)
        print((str(minutes)))

        cfgfile = open(src_user_config, 'w')
        config.set('SCHEDULE', 'minutes', minutes)
        config.write(cfgfile)
        cfgfile.close()
        
        if minutes in min_fix:
            cfgfile = open(src_user_config, 'w')
            config.set('SCHEDULE', 'minutes', '0'+minutes)
            config.write(cfgfile)
            cfgfile.close()

    def on_save_clicked(self):
        exit()

# main
app = QApplication(sys.argv)
main_screen = Schedule()
widget = QtWidgets.QStackedWidget()
appIcon = QIcon("src/icons/restore.png")
widget.setWindowIcon(appIcon)
widget.addWidget(main_screen)
widget.setFixedHeight(450)
widget.setFixedWidth(700)
widget.setWindowTitle("Schedule")
widget.show()
sys.exit(app.exec_())


