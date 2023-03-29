from setup import *
from get_backup_dates import *
from read_ini_file import UPDATEINIFILE


timeFolder = []
def get_latest_backup_time():
    mainIniFile = UPDATEINIFILE()
    try:
        for output in os.listdir(f"{str(mainIniFile.create_backup_folder())}/{get_backup_date()[0]}/"):
            timeFolder.append(output)
            timeFolder.sort(reverse=True)
        return timeFolder

    except:
        print("Error trying to get backup times!")
        pass
