from setup import *
from read_ini_file import *


MAIN_INI_FILE = UPDATEINIFILE()


def oldest_backup_date():
    try:
        for date in os.listdir(str(MAIN_INI_FILE.backup_folder_name())):
            # Only date folders
            if '-' in date:
                return date
            
            else:
                # Return latest backup to main folder
                return MAIN_INI_FILE.get_database_value(
                        'INFO', 'latest_backup_to_main')
        
    except:
        pass
    

if __name__ == '__main__':
    pass
