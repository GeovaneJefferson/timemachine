import os
import configparser
import getpass
import subprocess as sub
import datetime
import time
from pathlib import Path

t = 2
home_user = str(Path.home())
user_name = getpass.getuser()

#SRC LOCATION
# src_user_config = "src/user.ini"
# src_backup_now_py = "src/backup_now.py"

#DST LOCATION
src_user_config = home_user+"/.local/share/timemachine/src/user.ini"
src_backup_now_py = home_user+"/.local/share/timemachine/src/backup_now.py"

#GET FLATPAK
r = os.popen('flatpak --app list --columns=application')
flatpak_list = r.readlines()

def checker(): 
    for i in range(3):
        #CONFIGPARSER
        config = configparser.ConfigParser()
        config.read(src_user_config)
        read_hd_hd = config['EXTERNAL']['name']

        try:
            os.listdir("/media/"+user_name+"/"+read_hd_hd)
            print("HD found!")
            break
        except FileNotFoundError:
            #---If external HD is not available ---# 
            sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your external HD could not be found!\n Insert your external HD, mount it\n and we will do the rest for you.' 5",shell=True)
            print("No HD found...")
            time.sleep(10)

    while True:
        #----Read/Load user.config (backup automatically)----#
        config = configparser.ConfigParser()
        config.read(src_user_config)

        get_schedule_sun = (config.get('SCHEDULE', 'sun'))
        get_schedule_mon = (config.get('SCHEDULE', 'mon'))
        get_schedule_tue = (config.get('SCHEDULE', 'tue'))
        get_schedule_wed = (config.get('SCHEDULE', 'wed'))
        get_schedule_thu = (config.get('SCHEDULE', 'thu'))
        get_schedule_fri = (config.get('SCHEDULE', 'fri'))
        get_schedule_sat = (config.get('SCHEDULE', 'sat'))

        get_schedule_hours = (config.get('SCHEDULE', 'hours'))
        get_schedule_hours = int(get_schedule_hours)

        get_schedule_minutes = (config.get('SCHEDULE', 'minutes'))
        get_schedule_minutes = int(get_schedule_minutes)

        #---Get date---#
        day_name = datetime.datetime.now()
        day_name = (day_name.strftime("%a"))
        day_name = day_name.lower()
        print("Backup checker is running...")

        if day_name == "sun" and get_schedule_sun == "true":
            break
    
        elif day_name == "mon" and get_schedule_mon == "true":
            break

        elif day_name == "tue" and get_schedule_tue == "true":
            break

        elif day_name == "wed" and get_schedule_wed == "true":
            break

        elif day_name == "thu" and get_schedule_thu == "true":
            break

        elif day_name == "fri" and get_schedule_fri == "true":
            break

        elif day_name == "sat" and get_schedule_sat == "true":
            break
        
        print("No back up for today.")
        exit()

    while True:
        now = datetime.datetime.now()
        hour = now.strftime("%H")
        hour = int(hour)
        minute = now.strftime("%M")
        minute = int(minute)
        time.sleep(t)

        if int(hour) > int(get_schedule_hours):
            print("Time to back up has passed")
            exit()

        if int(hour) <= int(get_schedule_hours):
            if int(minute) == int(get_schedule_minutes):
                break
        else:
            print("Waiting for the right time to backup...")
            time.sleep(t)

    cfgfile = open(src_user_config, 'w')
    config.set('DEFAULT', 'backup_now', 'true')
    config.write(cfgfile)
    cfgfile.close() 
    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",shell=True)
    sub.Popen("python3 "+src_backup_now_py,shell=True)
    exit()

checker()
