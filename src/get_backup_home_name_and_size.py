from setup import *
from read_ini_file import UPDATEINIFILE
from get_latest_backup_date import latest_backup_date
from get_backup_time import get_latest_backup_time


MAIN_INI_FILE = UPDATEINIFILE()
home_folder_to_be_restore = []
home_folder_to_restore_size_list = []
home_Folder_to_restore_size_list_pretty = []

def get_backup_home_folders_name():
    print("Getting folders name...")
    for output in os.listdir(f"{MAIN_INI_FILE.get_backup_home_folders()}"):
        output=output.capitalize() 

        try:
            os.listdir(f"{HOME_USER}/{output}")
        except:
            # Lower output first letter
            output=output.lower() 

        home_folder_to_be_restore.append(output)

        try:
            getSize = os.popen(f"du -s {MAIN_INI_FILE.backup_folder_name()}/{latest_backup_date()}/{(get_latest_backup_time()[0])}/")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{MAIN_INI_FILE.backup_folder_name()}/"
                    f"{latest_backup_date()}/{(get_latest_backup_time()[0])}/", "").replace("\t", "")
            getSize = int(getSize)
            
            home_folder_to_restore_size_list.append(getSize)
        except:
            pass
        
        try:
            getSize=os.popen(f"du -hs {MAIN_INI_FILE.backup_folder_name()}/{latest_backup_date()}/{(get_latest_backup_time()[0])}/")
            getSize=getSize.read().strip("\t").strip("\n").replace(f"{MAIN_INI_FILE.backup_folder_name()}/"
                    f"{latest_backup_date()}/{(get_latest_backup_time()[0])}/", "").replace("\t", "")
            
            home_Folder_to_restore_size_list_pretty.append(getSize)
        except:
            pass

    return home_folder_to_be_restore

def get_backup_folders_size():
    get_backup_home_folders_name()
    
    return home_folder_to_restore_size_list[0]

def get_backup_folders_size_pretty():
    get_backup_home_folders_name()

    try:
        return home_Folder_to_restore_size_list_pretty[0]
    except IndexError as e:
        print(e)
        return None
    
    
if __name__ == '__main__':
    pass