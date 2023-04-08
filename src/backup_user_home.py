from setup import *
from read_ini_file import UPDATEINIFILE
from get_backup_folders import get_folders

def backup_user_home():
    mainIniFile = UPDATEINIFILE()

    try:
        # Backup all (user.ini true folders)
        for output in get_folders():
            print(f"{copyCPCMD} {homeUser}/{output} {str(mainIniFile.time_folder_format())}")
            sub.run(f"{copyCPCMD} {homeUser}/{output} {str(mainIniFile.time_folder_format())}",shell=True)

    except FileNotFoundError as error:
        error_trying_to_backup(error)
