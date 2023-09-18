from setup import *
from read_ini_file import UPDATEINIFILE

MAIN_INI_FILE = UPDATEINIFILE()


def system_tray():
    # First startup
    MAIN_INI_FILE.set_database_value(
        'STATUS', 'first_startup', 'True')

    # System tray
    if MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
        sub.Popen(
            ['python3', SRC_SYSTEM_TRAY_PY],
            stdout=sub.PIPE,
            stderr=sub.PIPE)

    if MAIN_INI_FILE.hd_name() is not None:
        if MAIN_INI_FILE.get_database_value(
            'STATUS', 'automatically_backup'):
            call_backup_checker()
    
    # Exit
    exit()

def call_backup_checker():
    sub.Popen(
        ['python3', SRC_BACKUP_CHECKER_PY],
        stdout=sub.PIPE,
        stderr=sub.PIPE)


if __name__=='__main__':
    # Delay startup for x seconds
    time.sleep(0) 
    system_tray()