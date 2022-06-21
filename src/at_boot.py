#! /usr/bin/env python3
from setup import *


class BOOT:
    def __init__(self):
        # Delay startup for x seconds
        time.sleep(30)  # Seconds

        ################################################################################
        # Read ini file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniSystemTray = config['SYSTEMTRAY']['system_tray']

        # Set startup to True
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'first_startup', 'true')
            config.write(configfile)

        self.read_ini_system_tray()

    def read_ini_system_tray(self):
        if self.iniSystemTray == "true":
            print("Starting system tray 'at_boot.py'")
            ################################################################################
            # Call system tray
            ################################################################################
            sub.Popen(f"python3 {src_system_tray}", shell=True)

        self.call_backup_checker()

    def call_backup_checker(self):
        ################################################################################
        # Call backup checker
        ################################################################################
        print("Calling backup check")
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)
        exit()


main = BOOT()
