from setup import *
from read_ini_file import *

oldestList=[]

def oldest_backup_date():
    try:
        MAININIFILE=UPDATEINIFILE()

        for dateList in os.listdir(str(MAININIFILE.backup_folder_name())):
            if dateList not in oldestList:
                oldestList.append(dateList)
                break

        return oldestList[0]

    except:
        pass
    
if __name__ == '__main__':
    pass