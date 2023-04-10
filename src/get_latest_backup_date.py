from setup import *
from read_ini_file import UPDATEINIFILE

lastestList = []

def latest_backup_date_label():
    from get_backup_time import get_latest_backup_time
    mainIniFile = UPDATEINIFILE()
    x = str(get_latest_backup_time()[0]).replace("-",":")
            
    try:
        lastestList.clear()

        for dateList in os.listdir(str(mainIniFile.backup_folder_name())):
            if dateList not in lastestList:
                lastestList.append(dateList)

        lastestList.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
        
        if lastestList[0] == f"{mainIniFile.current_date()}-{mainIniFile.current_month()}-{mainIniFile.current_year()}": 
            return f"Today, {x}"
        else:
            # Check todays date, if last backup was Yesterday, return Yesterday
            if int(mainIniFile.current_date()) - int(lastestList[0][:2]) == 1:
                return f"Yesterday, {x}"
            else:
                return lastestList[0]

    except:
        pass

def latest_backup_date():
    mainIniFile = UPDATEINIFILE()

    try:
        lastestList.clear()

        for dateList in os.listdir(str(mainIniFile.backup_folder_name())):
            if dateList not in lastestList:
                lastestList.append(dateList)

        lastestList.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
        return lastestList[0]

    except:
        pass
if __name__ == '__main__':
    print(latest_backup_date_label())
    pass