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

def may_create_date_time_folder():
    # Read the include file and process each item's information
    with open(MAIN_INI_FILE.include_to_backup(), "r") as f:
        lines = f.readlines()
        
        for i in range(0, len(lines), 5):
            try:
                filename = lines[i + 0].split(':')[-1].strip()
                size_string = lines[i + 1].split(':')[-1].strip()
                # size = int(size_string.split()[0])
                location = lines[i + 2].split(':')[-1].strip()
                status = lines[i + 3].split(':')[-1].strip()
                
                ##########################################################
                # .MAIN BACKUP
                ##########################################################
                if status == 'UPDATED':
                    # Latest date/time with only close file location
                    # Remove home name
                    remove_home_name = location.replace(f'{HOME_USER}', ' ').strip()

                    # Fx. /Desktop/test.txt
                    destination_location = f'{MAIN_INI_FILE.time_folder_format()}{remove_home_name}'
                    
                    # One is necessary to create date/time folder 
                    return True
            
            except IndexError:
                pass

        return False

# def may_create_date_time_folder():
#     # Read the include file and process each item's information
#     with open(MAIN_INI_FILE.include_to_backup(), "r") as f:
#         lines = f.readlines()
        
#         for i in range(0, len(lines), 5):
#             try:
#                 filename = lines[i + 0].split(':')[-1].strip()
#                 size_string = lines[i + 1].split(':')[-1].strip()
#                 # size = int(size_string.split()[0])
#                 location = lines[i + 2].split(':')[-1].strip()
#                 status = lines[i + 3].split(':')[-1].strip()
                
#                 ##########################################################
#                 # .MAIN BACKUP
#                 ##########################################################
#                 if status == 'NEW':
#                     # Remove home name
#                     remove_backup_name = location.replace(f'{HOME_USER}', ' ').strip()

#                     # Fx. /Desktop/test.txt
#                     destination_location = f'{MAIN_INI_FILE.main_backup_folder()}{remove_backup_name}'
                        
#                     # One is necessary to create date/time folder 
#                     return True
            
#             except IndexError:
#                 pass
                
#         return False


if __name__ == '__main__':
    pass