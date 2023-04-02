from setup import *
from get_backup_dates import *
from read_ini_file import UPDATEINIFILE


timeFolder = []
timeAllFolder = []

def get_latest_backup_time():
    mainIniFile = UPDATEINIFILE()
    try:
        timeFolder.clear()
        for output in os.listdir(f"{str(mainIniFile.backup_folder_name())}/{get_backup_date()[0]}/"):
            timeFolder.append(output)
            timeFolder.sort(reverse=True)
        return timeFolder

    except:
        print("Error trying to get backup times!")
        pass