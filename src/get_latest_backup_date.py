from setup import *
from read_ini_file import UPDATEINIFILE

MAININIFILE = UPDATEINIFILE()
LATEST_LIST = []

def latest_backup_date_label():
    from get_backup_time import get_latest_backup_time
            
    LATEST_LIST.clear()
    try:
        for dateList in os.listdir(str(MAININIFILE.backup_folder_name())):
            if dateList not in LATEST_LIST:
                LATEST_LIST.append(dateList)

        LATEST_LIST.sort(reverse = True, key = lambda date: datetime.strptime(date, "%d-%m-%y"))
        latest_backup = str(get_latest_backup_time()[0]).replace("-",":")
        if LATEST_LIST[0] == f"{MAININIFILE.current_date()}-{MAININIFILE.current_month()}-{MAININIFILE.current_year()}": 
            return f"Today, {latest_backup}"
        else:
            # Check todays date, if last backup was Yesterday, return Yesterday
            if int(MAININIFILE.current_date()) - int(LATEST_LIST[0][:2]) == 1:
                return f"Yesterday, {latest_backup}"
            else:
                return LATEST_LIST[0]
    except:
        pass

def latest_backup_date():
    LATEST_LIST.clear()
    try:
        for dateList in os.listdir(str(MAININIFILE.backup_folder_name())):
            if dateList not in LATEST_LIST:
                LATEST_LIST.append(dateList)

        LATEST_LIST.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
        return LATEST_LIST[0]
    except:
        pass

if __name__ == '__main__':
    print(latest_backup_date_label())
    pass