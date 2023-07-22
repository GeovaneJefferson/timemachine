from setup import *
from get_backup_date import *
from read_ini_file import UPDATEINIFILE
from get_latest_backup_date import latest_backup_date


timeFolder=[]
timeAllFolder=[]

def get_latest_backup_time():
    MAININIFILE=UPDATEINIFILE()

    try:
        timeFolder.clear()
        for output in os.listdir(f"{str(MAININIFILE.backup_folder_name())}/{latest_backup_date()}/"):
            timeFolder.append(output)
            timeFolder.sort(reverse=True)
        return timeFolder

    except Exception as error:
        print(error)
        print("Error trying to get backup times!")
        pass

if __name__ == '__main__':
    pass