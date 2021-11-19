import os
import configparser
import getpass
import subprocess as sub
import time
from pathlib import Path
from datetime import datetime

t = 5
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

#VAR 
time_mode_hours_60 = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
time_mode_hours_120 = ['00','02','04','06','08','10','12','14','16','18','20','22']
time_mode_hours_240 = ['00','04','08','12','16','20']
time_mode_minutes_15 = ['00','15','30','45']
time_mode_minutes_30 = ['00','30']

def checker(): 
    time.sleep(30)
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
            sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your external HD could not be found!\n Please, insert your external HD...' 5",shell=True)
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

        next_hour = (config.get('SCHEDULE', 'hours'))
        next_minute = (config.get('SCHEDULE', 'minutes'))

        #FREQUENCY CHECK
        one_time_mode = config['MODE']['one_time_mode']

        #---Get date---#
        day_name = datetime.now()
        day_name = day_name.strftime("%a")
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

    if one_time_mode == "true":
        while True:
            now = datetime.now()
            current_hour = now.strftime("%H")
            current_minute = now.strftime("%M")

            total_current_time = current_hour+current_minute
            total_next_time = next_hour+next_minute
            
            print(total_current_time)
            print(total_next_time)

            time.sleep(t)

            if total_current_time > total_next_time:
                print("Time to back up has passed")
                exit()

            if total_current_time == total_next_time:
                break
            else:
                print("Waiting for the right time to backup...")
                time.sleep(t)

        with open(src_user_config, 'w') as configfile:
            config.set('DEFAULT', 'backup_now', 'true')
            config.write(configfile)  
            
            sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",shell=True)
            sub.Popen("python3 "+src_backup_now_py,shell=True)
            exit()

    else:
        while True:
            #----Read/Load user.config (backup automatically)----#
            config = configparser.ConfigParser()
            config.read(src_user_config)
            more_time_mode = config['MODE']['more_time_mode']
            everytime = config['SCHEDULE']['everytime']

            now = datetime.now()
            current_hour = now.strftime("%H")
            current_minute = now.strftime("%M")
            print(current_minute)
            time.sleep(t)

            if everytime == '15':
                print('evertime: '+everytime)
                if current_minute in time_mode_minutes_15:
                    with open(src_user_config, 'w') as configfile:
                        config.set('DEFAULT', 'backup_now', 'true')
                        config.write(configfile) 

                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",shell=True)
                    sub.call("python3 "+src_backup_now_py,shell=True)
                    time.sleep(60)
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(t)

            if everytime == '30':
                print('evertime: '+everytime)
                if current_minute in time_mode_minutes_30:
                    with open(src_user_config, 'w') as configfile:
                        config.set('DEFAULT', 'backup_now', 'true')
                        config.write(configfile) 

                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",shell=True)
                    sub.call("python3 "+src_backup_now_py,shell=True)
                    time.sleep(60)
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(t)

            if everytime == '60':
                print('evertime: '+everytime)
                if current_hour in time_mode_hours_60:
                    with open(src_user_config, 'w') as configfile:
                        config.set('DEFAULT', 'backup_now', 'true')
                        config.write(configfile) 

                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",shell=True)
                    sub.call("python3 "+src_backup_now_py,shell=True)
                    time.sleep(60)
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(t)

            if everytime == '120':
                print('evertime: '+everytime)
                if current_hour in time_mode_hours_120:
                    with open(src_user_config, 'w') as configfile:
                        config.set('DEFAULT', 'backup_now', 'true')
                        config.write(configfile) 

                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",shell=True)
                    sub.call("python3 "+src_backup_now_py,shell=True)
                    time.sleep(60)
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(t)

            if everytime == '240':
                print('evertime: '+everytime)
                if current_hour in time_mode_hours_240:
                    with open(src_user_config, 'w') as configfile:
                        config.set('DEFAULT', 'backup_now', 'true')
                        config.write(configfile) 

                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5",shell=True)
                    sub.call("python3 "+src_backup_now_py,shell=True)
                    time.sleep(60)
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(t)

            if more_time_mode == "false":
                break
        checker()

checker()
