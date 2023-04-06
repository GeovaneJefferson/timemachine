from setup import *
from get_backup_date import *
from get_latest_backup_date import latest_backup_date
from read_ini_file import UPDATEINIFILE


timeFolder = []
timeAllFolder = []

def get_latest_backup_time():
    mainIniFile = UPDATEINIFILE()
    try:
        timeFolder.clear()
        for output in os.listdir(f"{str(mainIniFile.backup_folder_name())}/{latest_backup_date()}/"):
            timeFolder.append(output)
            timeFolder.sort(reverse=True)
        return timeFolder

    except:
        print("Error trying to get backup times!")
        pass