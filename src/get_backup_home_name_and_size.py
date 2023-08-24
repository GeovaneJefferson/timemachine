from setup import *
from read_ini_file import UPDATEINIFILE
from get_latest_backup_date import latest_backup_date
from get_backup_time import get_latest_backup_time
from handle_spaces import handle_spaces


MAIN_INI_FILE = UPDATEINIFILE()


list_home_folder_to_restore = []
list_home_folder_size_to_restore = []
list_home_folder_size_to_restore_pretty = []

def get_backup_home_folders_name():
    print("Getting folders name...")

    for folder in os.listdir(f"{MAIN_INI_FILE.get_backup_home_folders()}"):
        folder = folder.capitalize() 

        # Check folder isUpper or not
        if not os.path.exists(f"{HOME_USER}/{folder}"):
            folder = folder.lower() 

        # Add to the list after handle spaces
        list_home_folder_to_restore.append(handle_spaces(folder))

        try:
            get_size = os.popen(f"du -s {MAIN_INI_FILE.backup_folder_name()}/{latest_backup_date()}/{(get_latest_backup_time()[0])}/")
            get_size = get_size.read().strip("\t").strip("\n").replace(f"{MAIN_INI_FILE.backup_folder_name()}/"
                    f"{latest_backup_date()}/{(get_latest_backup_time()[0])}/", "").replace("\t", "")
            
            # Add to the list
            list_home_folder_size_to_restore.append(int(get_size))
        except:
            pass
        
        try:
            get_size = os.popen(f"du -hs {MAIN_INI_FILE.backup_folder_name()}/{latest_backup_date()}/{(get_latest_backup_time()[0])}/")
            get_size = get_size.read().strip("\t").strip("\n").replace(f"{MAIN_INI_FILE.backup_folder_name()}/"
                    f"{latest_backup_date()}/{(get_latest_backup_time()[0])}/", "").replace("\t", "")
            
            # Add to the list
            list_home_folder_size_to_restore_pretty.append(int(get_size))
        except:
            pass

    # Return all sizes
    return list_home_folder_to_restore

def get_backup_folders_size():
    get_backup_home_folders_name()
    
    # Return first size from list
    return list_home_folder_size_to_restore[0]

def get_backup_folders_size_pretty():
    get_backup_home_folders_name()

    try:
        # Return first size from list, pretty way
        return list_home_folder_size_to_restore_pretty[0]
    except IndexError:
        return None
    
    
if __name__ == '__main__':
    pass