from setup import *


class BOOT:
    def __init__(self):
        try:
            ################################################################################
            ## Read ini file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            self.getSystemTray = config['SYSTEMTRAY']['system_tray']

            if self.getSystemTray == "true":
                ################################################################################
                ## Call system tray
                ################################################################################
                sub.Popen(f"python3 {src_system_tray}", shell=True)

            ################################################################################
            ## Call backup checker
            ################################################################################
            sub.Popen(f"python3 {src_backup_check_py}", shell=True)
            exit()

        except:
            exit()


main = BOOT()
