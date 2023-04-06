from setup import *
from read_ini_file import *

lastestList = []

def latest_backup_date_label():
    try:
        mainIniFile = UPDATEINIFILE()
        lastestList.clear()

        for dateList in os.listdir(str(mainIniFile.backup_folder_name())):
            if dateList not in lastestList:
                lastestList.append(dateList)

        lastestList.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        if lastestList[0] == f"{mainIniFile.current_date()}-{mainIniFile.current_month()}-{mainIniFile.current_year()}": 
            return "Today"
        else:
            return lastestList[0]

    except:
        pass

def latest_backup_date():
    try:
        mainIniFile = UPDATEINIFILE()
        lastestList.clear()

        for dateList in os.listdir(str(mainIniFile.backup_folder_name())):
            if dateList not in lastestList:
                lastestList.append(dateList)

        lastestList.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
        return lastestList[0]

    except:
        pass