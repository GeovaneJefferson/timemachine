from setup import *
from get_backup_date import *
from read_ini_file import UPDATEINIFILE
from get_latest_backup_date import latest_backup_date


TIME_FOLDER = []
MAIN_INI_FILE = UPDATEINIFILE()

def get_latest_backup_time():

    try:
        TIME_FOLDER.clear()
        for output in os.listdir(f"{MAIN_INI_FILE.backup_folder_name()}/{latest_backup_date()}/"):
            TIME_FOLDER.append(output)
            TIME_FOLDER.sort(reverse=True)
        return TIME_FOLDER

    except Exception as error:
        print(error)
        pass

if __name__ == '__main__':
    pass