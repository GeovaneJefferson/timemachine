#! /usr/bin/python3
from setup import *
from read_ini_file import UPDATEINIFILE


class BOOT:
    def __init__(self):
        # Delay startup for x seconds
        time.sleep(30)  # Seconds
        
        self.system_tray()

    def system_tray(self):
        mainIniFile = UPDATEINIFILE()

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'first_startup', 'true')
            config.write(configfile)

        if str(mainIniFile.ini_system_tray()) == "true":
            sub.Popen(f"python3 {src_system_tray}", shell=True)

        # If external devices has already been saved inside INI file
        if str(mainIniFile.ini_hd_name()) != "None":
            # If auto backup is activated
            if str(mainIniFile.ini_automatically_backup()) == "true":
                self.call_backup_checker()

    def call_backup_checker(self):
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)
        exit()


main = BOOT()
