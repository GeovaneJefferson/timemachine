from setup import *
from read_ini_file import UPDATEINIFILE

MAIN_INI_FILE=UPDATEINIFILE()

class BOOT:
    def __init__(self):
        # Delay startup for x seconds
        time.sleep(0)  # Seconds
        
        self.system_tray()

    def system_tray(self):
        CONFIG=configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        with open(SRC_USER_CONFIG, 'w') as configfile:
            CONFIG.set('STATUS', 'first_startup', 'true')
            CONFIG.write(configfile)

        if MAIN_INI_FILE.ini_system_tray():
            sub.Popen(f"python3 {src_system_tray_py}",shell=True)

        if MAIN_INI_FILE.ini_hd_name() != "None":
            if MAIN_INI_FILE.ini_automatically_backup():
                self.call_backup_checker()
        exit()

    def call_backup_checker(self):
        sub.Popen(f"python3 {SRC_BACKUP_CHECKER_PY}", shell=True)

if __name__=='__main__':
    main=BOOT()
