from setup import *
from read_ini_file import *


MAIN_INI_FILE = UPDATEINIFILE()


def oldest_backup_date():
    # Return latest backup to main folder
    return MAIN_INI_FILE.get_database_value(
            'INFO', 'oldest_backup_to_main')
    

if __name__ == '__main__':
    pass
