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
# SRC LOCATION
# src_user_config = "src/user.ini"
# src_backup_now_py = "src/backup_now.py"

# DST LOCATION
src_user_config = home_user + "/.local/share/timemachine/src/user.ini"
src_backup_now_py = home_user + "/.local/share/timemachine/src/backup_now.py"

# VAR
time_mode_hours_60 = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                      '16', '17', '18', '19', '20', '21', '22', '23']
time_mode_hours_120 = ['00', '02', '04', '06', '08', '10', '12', '14', '16', '18', '20', '22']
time_mode_hours_240 = ['00', '04', '08', '12', '16', '20']
time_mode_minutes_15 = ['00', '15', '30', '45']
time_mode_minutes_30 = ['00', '30']


class Checker:
    def __init__(self):
        print("Time Machine will look for the external hd in 30 seconds...")
        time.sleep(30)

        # CONFIGPARSER
        config = configparser.ConfigParser()
        config.read(src_user_config)
        read_hd_name = config['EXTERNAL']['name']

        storage = []
        for storage in os.listdir("/media/" + user_name + "/"):
            if not storage.startswith('.'):
                print("Local media        : ", storage)
                print("Saved external name: ", read_hd_name)

        if read_hd_name in storage:  # If user.ini has external hd name
            print("HD found!")
            self.begin_to_check()
        else:
            # If external HD is not available
            sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your external HD could not be found!\n Please, insert your external HD...' 5", shell=True)
            print("No HD found...")
            print("Existing...")
            exit()

    def begin_to_check(self):
        while True:
            # Read/Load user.config (backup automatically)
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

            # FREQUENCY CHECK
            one_time_mode = config['MODE']['one_time_mode']

            # ---Get date---#
            day_name = datetime.now()
            day_name = day_name.strftime("%a")
            day_name = day_name.lower()
            print("Backup checker is running...")

            if day_name == "sun" and get_schedule_sun:
                break

            elif day_name == "mon" and get_schedule_mon:
                break

            elif day_name == "tue" and get_schedule_tue:
                break

            elif day_name == "wed" and get_schedule_wed:
                break

            elif day_name == "thu" and get_schedule_thu:
                break

            elif day_name == "fri" and get_schedule_fri:
                break

            elif day_name == "sat" and get_schedule_sat:
                break

            print("No back up for today.")
            exit()

        if one_time_mode:
            while True:
                now = datetime.now()
                current_hour = now.strftime("%H")
                current_minute = now.strftime("%M")

                total_current_time = current_hour + current_minute
                total_next_time = next_hour + next_minute

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

                sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5", shell=True)
                sub.Popen("python3 " + src_backup_now_py, shell=True)
                exit()

        else:
            while True:
                # ----Read/Load user.config (backup automatically)----#
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
                    print('everytime: ' + everytime)
                    if current_minute in time_mode_minutes_15:
                        with open(src_user_config, 'w') as configfile:
                            config.set('DEFAULT', 'backup_now', 'true')
                            config.write(configfile)

                        sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5", shell=True)
                        sub.call("python3 " + src_backup_now_py, shell=True)
                        time.sleep(60)
                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(t)

                if everytime == '30':
                    print('everytime: ' + everytime)
                    if current_minute in time_mode_minutes_30:
                        with open(src_user_config, 'w') as configfile:
                            config.set('DEFAULT', 'backup_now', 'true')
                            config.write(configfile)

                        sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5", shell=True)
                        sub.call("python3 " + src_backup_now_py, shell=True)
                        time.sleep(60)
                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(t)

                if everytime == '60':
                    print('everytime: ' + everytime)
                    if current_hour in time_mode_hours_60:
                        with open(src_user_config, 'w') as configfile:
                            config.set('DEFAULT', 'backup_now', 'true')
                            config.write(configfile)

                        sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5", shell=True)
                        sub.call("python3 " + src_backup_now_py, shell=True)
                        time.sleep(60)
                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(t)

                if everytime == '120':
                    print('everytime: ' + everytime)
                    if current_hour in time_mode_hours_120:
                        with open(src_user_config, 'w') as configfile:
                            config.set('DEFAULT', 'backup_now', 'true')
                            config.write(configfile)

                        sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5", shell=True)
                        sub.call("python3 " + src_backup_now_py, shell=True)
                        time.sleep(60)
                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(t)

                if everytime == '240':
                    print('everytime: ' + everytime)
                    if current_hour in time_mode_hours_240:
                        with open(src_user_config, 'w') as configfile:
                            config.set('DEFAULT', 'backup_now', 'true')
                            config.write(configfile)

                        sub.Popen("kdialog --title 'Time Machine' --passivepopup 'TimeMachine 'Your backup will start shortly...' 5", shell=True)
                        sub.call("python3 " + src_backup_now_py, shell=True)
                        time.sleep(60)
                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(t)

                if not more_time_mode:
                    break


Object = Checker()
Object.__init__()
