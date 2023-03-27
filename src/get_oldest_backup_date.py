from setup import *
from read_ini_file import *

oldestList = []

def oldest_backup_date():
    try:
        mainIniFile = UPDATEINIFILE()

        for dateList in os.listdir(str(mainIniFile.create_backup_folder())):
            if dateList not in oldestList:
                oldestList.append(dateList)
                break

        return oldestList[0]

    except:
        pass