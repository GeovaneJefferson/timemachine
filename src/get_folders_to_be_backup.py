from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def get_folders():
    FOLDERS_LIST = []

    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()

    # Query all keys from the specified table
    cursor.execute(f"SELECT key FROM FOLDER")
    keys = [row[0] for row in cursor.fetchall()]

    # Close the connection
    conn.close()

    for key in keys:
        FOLDERS_LIST.append(key)

    # Get Backup Folders
    for folder in FOLDERS_LIST:  
        # Capitalize first letter
        folder = folder.capitalize()

        try:
            # Backup folder was capitalize
            os.listdir(f"{HOME_USER}/{folder}")
        except:
            # Backup folder was not capitalize
            folder = folder.lower() 

        # Add folder inside home_folder_to_beBackup
        FOLDERS_LIST.append(folder)

        # Sort them
        FOLDERS_LIST.sort()
    
    return FOLDERS_LIST 

def home_folders_size():
    home_folder_to_backup_size_list = []

    for folder in get_folders():
        # Get folder size
        get_size = os.popen(f"du -s {HOME_USER}/{folder}")
        get_size = int(get_size.read().strip("\t").strip("\n").replace(f"{HOME_USER}/{folder}", "").replace("\t", ""))

        # Add to list
        home_folder_to_backup_size_list.append(get_size)

    return sum(home_folder_to_backup_size_list)


if __name__ == '__main__':
    pass