from setup import *
from read_ini_file import *


MAIN_INI_FILE = UPDATEINIFILE()
oldest_list=[]

def oldest_backup_date():
    try:

        for dateList in os.listdir(str(MAIN_INI_FILE.backup_folder_name())):
            if dateList not in oldest_list:
                oldest_list.append(dateList)
                break

        return oldest_list[0]

    except:
        pass
    

if __name__ == '__main__':
    pass