from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def get_folders():
    list_of_folders = []
    list_of_folders_to_return = []
    
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()

    # Query all keys from the specified table
    cursor.execute(f"SELECT key FROM FOLDER")
    keys = [row[0] for row in cursor.fetchall()]

    # Close the connection
    conn.close()

    for key in keys:
        list_of_folders.append(key)

    # Get Backup Folders
    for folder in list_of_folders:  
        folder = str(folder).capitalize()

        # Check folder isUpper or not
        if not os.path.exists(f"{HOME_USER}/{folder}"):
            folder = folder.lower() 
        
        list_of_folders_to_return.append(folder)
        list_of_folders_to_return.sort()
    
    return list_of_folders_to_return 

def home_folders_size():
    home_folder_to_backup_size_list = []

    for folder in get_folders():
        try:
            # Get folder size
            get_size = os.popen(f"du -s {HOME_USER}/{folder}")
            get_size = int(get_size.read().strip("\t").strip("\n").replace(
                f"{HOME_USER}/{folder}", "").replace("\t", ""))

            # Add to list
            home_folder_to_backup_size_list.append(get_size)
        except Exception:
            pass

    return sum(home_folder_to_backup_size_list)


if __name__ == '__main__':
    pass