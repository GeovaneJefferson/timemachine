#! /usr/bin/python3
from setup import *


class BOOT:
    def __init__(self):
        # Delay startup for x seconds
        time.sleep(30)  # Seconds
        
        self.read_ini_file()

    def read_ini_file(self):
        # Read ini file
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # INI file
        self.iniHDName = config['EXTERNAL']['name']
        self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
        self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']

        self.system_tray()

    def system_tray(self):
        # Read ini file
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Set startup to True
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'first_startup', 'true')
            config.write(configfile)

        if self.iniSystemTray == "true":
            ####################################################################
            # Call system tray
            ####################################################################
            sub.Popen(f"python3 {src_system_tray}", shell=True)

        # If external devices has already been saved inside INI file
        if self.iniHDName != "None":
            # If auto backup is activated
            if self.iniAutomaticallyBackup == "true":
                self.call_backup_checker()

    def call_backup_checker(self):
        ########################################################################
        # Call backup checker
        ########################################################################
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)
        # Start auto package backup
        sub.Popen(f"python3 {src_package_backup_py}", shell=True)
        exit()


main = BOOT()
