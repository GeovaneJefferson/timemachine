#! /usr/bin/env python3
from setup import *


class BOOT:
    def __init__(self):
        ################################################################################
        ## Dalay startup
        ################################################################################
        time.sleep(30)  # Seconds
        
        ################################################################################
        ## Read ini file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        self.getSystemTray = config['SYSTEMTRAY']['system_tray']

        ################################################################################
        ## Set startup to True
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'first_startup', 'true')
            config.write(configfile)

        self.check_system_tray()

    def check_system_tray(self):
        if self.getSystemTray == "true":
            print("Starting system tray 'at_boot.py'")
            ################################################################################
            ## Call system tray
            ################################################################################
            sub.Popen(f"python3 {src_system_tray}", shell=True)

        self.call_backup_checker()

    def call_backup_checker(self):
        ################################################################################
        ## Call backup checker
        ################################################################################
        print("Calling backup check")
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)
        exit()


main = BOOT()
