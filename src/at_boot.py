from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def system_tray():
    # Update DB
    MAIN_INI_FILE.set_database_value(
        'STATUS', 'first_startup', 'True')

    if MAIN_INI_FILE.get_database_value(
        'SYSTEMTRAY', 'system_tray'):
        # System tray
        sub.Popen(
            ['python3', SRC_SYSTEM_TRAY_PY],
            stdout=sub.PIPE,
            stderr=sub.PIPE)

    if MAIN_INI_FILE.hd_name() is not None:
        if MAIN_INI_FILE.get_database_value(
            'STATUS', 'automatically_backup'):
            
            # Unfinished backup
            if MAIN_INI_FILE.get_database_value(
                'STATUS', 'unfinished_backup'):
                
                # Start backup checker
                sub.Popen(
                    ['python3', SRC_BACKUP_NOW_PY],
                    stdout=sub.PIPE,
                    stderr=sub.PIPE)
            else:
                # Start backup checker
                sub.Popen(
                    ['python3', SRC_BACKUP_CHECKER_PY],
                    stdout=sub.PIPE,
                    stderr=sub.PIPE)


# Delay startup for x seconds
try:
    time.sleep(0)
    system_tray()
except Exception as error:
    # Save error log
    MAIN_INI_FILE.report_error(error)