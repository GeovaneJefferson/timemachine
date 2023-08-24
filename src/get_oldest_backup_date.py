from setup import *
from read_ini_file import *


MAIN_INI_FILE = UPDATEINIFILE()


OLDEST_BACKUP_DATE = []

def oldest_backup_date():
    try:
        for dateList in os.listdir(str(MAIN_INI_FILE.backup_folder_name())):
            if dateList not in OLDEST_BACKUP_DATE:
                OLDEST_BACKUP_DATE.append(dateList)
                break
                
        return OLDEST_BACKUP_DATE[0]

    except:
        pass
    

if __name__ == '__main__':
    pass