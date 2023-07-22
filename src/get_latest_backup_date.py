from setup import *
from read_ini_file import UPDATEINIFILE

lastestList=[]

def latest_backup_date_label():
    from get_backup_time import get_latest_backup_time
    MAININIFILE=UPDATEINIFILE()
            
    try:
        lastestList.clear()

        for dateList in os.listdir(str(MAININIFILE.backup_folder_name())):
            if dateList not in lastestList:
                lastestList.append(dateList)

        lastestList.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        if lastestList[0] == f"{MAININIFILE.current_date()}-{MAININIFILE.current_month()}-{MAININIFILE.current_year()}": 
            x=str(get_latest_backup_time()[0]).replace("-",":")
            return f"Today, {x}"
        else:
            # Check todays date, if last backup was Yesterday, return Yesterday
            if int(MAININIFILE.current_date()) - int(lastestList[0][:2]) == 1:
                x=str(get_latest_backup_time()[0]).replace("-",":")
                return f"Yesterday, {x}"
            else:
                return lastestList[0]

    except:
        pass

def latest_backup_date():
    MAININIFILE=UPDATEINIFILE()

    try:
        lastestList.clear()

        for dateList in os.listdir(str(MAININIFILE.backup_folder_name())):
            if dateList not in lastestList:
                lastestList.append(dateList)

        lastestList.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
        return lastestList[0]

    except:
        pass

if __name__ == '__main__':
    pass