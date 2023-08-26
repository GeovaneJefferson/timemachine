from setup import *
from read_ini_file import UPDATEINIFILE

MAIN_INI_FILE = UPDATEINIFILE()

class BOOT:
    def __init__(self):
        # Delay startup for x seconds
        time.sleep(0) 
        self.system_tray()

    def system_tray(self):
        MAIN_INI_FILE.set_database_value('STATUS', 'first_startup', 'True')

        if MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
            sub.Popen(["python3", src_system_tray_py], stdout=sub.PIPE, stderr=sub.PIPE)

        if MAIN_INI_FILE.get_database_value('EXTERNAL', 'name') != "None":
            if MAIN_INI_FILE.get_database_value('STATUS', 'automatically_backup',):
                self.call_backup_checker()
        exit()

    def call_backup_checker(self):
        sub.Popen(["python3", SRC_BACKUP_CHECKER_PY], stdout=sub.PIPE, stderr=sub.PIPE)


if __name__=='__main__':
    main = BOOT()
