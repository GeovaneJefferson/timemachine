from setup import *
from read_ini_file import UPDATEINIFILE

home_folder_to_be_backup=[]
home_folder_to_backup_size_list=[]


def get_folders():
    MAININIFILE=UPDATEINIFILE()

    # Get Backup Folders
    for folder in MAININIFILE.ini_folders():  
        # Capitalize first letter
        folder=folder.capitalize()

        try:
            # Backup folder was capitalize
            os.listdir(f"{HOME_USER}/{folder}")

        except:
            # Backup folder was not capitalize
            folder=folder.lower() 

        # Add folder inside home_folder_to_beBackup
        home_folder_to_be_backup.append(folder)

        # Sort them
        home_folder_to_be_backup.sort()
    
    return home_folder_to_be_backup 


def home_folders_size():
    for folder in get_folders():
        # Get folder size
        get_size=os.popen(f"du -s {HOME_USER}/{folder}")
        get_size=int(get_size.read().strip("\t").strip("\n").replace(f"{HOME_USER}/{folder}", "").replace("\t", ""))

        # Add to list
        home_folder_to_backup_size_list.append(get_size)

    return sum(home_folder_to_backup_size_list)


if __name__ == '__main__':
    pass