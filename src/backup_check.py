#! /usr/bin/python3
from setup import *
from check_connection import is_connected
from get_time import *
from get_backup_date import get_backup_date
from get_system_language import system_language
from languages import determine_days_language
from calculate_time_left_to_backup import calculate_time_left_to_backup
from search_download_for_packages import search_download_for_packages
from read_ini_file import UPDATEINIFILE


################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class CLI:
    def __init__(self):
        pass
         
    def updates(self):
        try:
            print("Backup Checker is running...")
        except KeyError as error:
            print(error)
            exit()

    def check_connection(self):
        if is_connected(str(mainIniFile.ini_hd_name())):
            self.search_downloads()

    ################################################################################
    # Auto Packages
    ################################################################################
    def search_downloads(self):
        search_download_for_packages()

        self.check_the_date()

    def check_the_date(self):
        if str(mainIniFile.ini_multiple_time_mode()) == "true":
            self.check_the_mode()

        else:
            if str(mainIniFile.day_name()) in determine_days_language((system_language()))[0] and str(mainIniFile.ini_next_backup_sun()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[1] and str(mainIniFile.ini_next_backup_mon()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[2] and str(mainIniFile.ini_next_backup_tue()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[3] and str(mainIniFile.ini_next_backup_wed()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[4] and str(mainIniFile.ini_next_backup_thu()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[5] and str(mainIniFile.ini_next_backup_fri()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[6] and str(mainIniFile.ini_next_backup_sat()) == "true":
                self.check_the_mode()
            
            else:
                pass
    
    def check_the_mode(self):
        if str(mainIniFile.ini_backup_now()) == "false":
            if str(mainIniFile.ini_one_time_mode()) == "true":
                if int(mainIniFile.current_time()) >= int(mainIniFile.backup_time_military()):
                    if today_date() not in get_backup_date():
                        self.call_backup_now()

                    else:
                        # Reset time left
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('SCHEDULE', 'time_left', 'None')
                            config.write(configfile)

                # elif int(mainIniFile.current_time()) == int(mainIniFile.backup_time_military()):
                #     self.call_backup_now()

                else:
                    calculate_time_left_to_backup()
                 
            else:
                # Multiple time per day
                if str(mainIniFile.everytime()) == '60' and str(mainIniFile.current_time()) in timeModeHours60:
                    self.call_backup_now()

                elif str(mainIniFile.everytime()) == '120' and str(mainIniFile.current_time()) in timeModeHours120:
                    self.call_backup_now()

                elif str(mainIniFile.everytime()) == '240' and str(mainIniFile.current_time()) in timeModeHours240:
                    self.call_backup_now()
                
                else:
                    pass

    def call_backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        sub.run(f"python3 {src_prepare_backup_py}", shell=True)


mainIniFile = UPDATEINIFILE()
main = CLI()

while True:
    main.updates()
    main.check_connection()

    ################################################################################
    # Prevent multiples backup checker running
    ################################################################################
    try:
        if mainIniFile.ini_automatically_backup() == "false":
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', 'false')
                config.write(configfile)

            break

    except Exception as error:
        print(error)
        break
        
    time.sleep(5)

exit()

