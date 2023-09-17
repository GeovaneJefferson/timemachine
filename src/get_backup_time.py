from setup import *
from get_backup_date import *
from read_ini_file import UPDATEINIFILE
from get_latest_backup_date import latest_backup_date


MAIN_INI_FILE = UPDATEINIFILE()



def get_latest_backup_time():
    list_of_time_folder = []

    try:
        for output in os.listdir(f"{MAIN_INI_FILE.backup_folder_name()}/{latest_backup_date()}/"):
            list_of_time_folder.append(output)

        # Sort list
        list_of_time_folder.sort(reverse=True)
        #  Return list
        return list_of_time_folder
    except Exception:
        pass


if __name__ == '__main__':
    pass