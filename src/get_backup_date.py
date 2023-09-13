from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def get_backup_date():
    backup_date_list = []

    try:
        for date_folder in os.listdir(f"{str(MAIN_INI_FILE.backup_folder_name())}"):
            # Only date folders
            if '-' in date_folder:
                backup_date_list.append(date_folder)
                backup_date_list.sort(
                    reverse = True, 
                    key = lambda date: datetime.strptime(date, "%d-%m-%y"))
        
        # Has date in list
        if backup_date_list:
            return backup_date_list

        else:
            return None
        
    except:
        pass

def last_backup_date():
    # Grab last date folder
    return get_backup_date()[0]

def last_backup_time():
    loc = MAIN_INI_FILE.backup_dates_location()
    search = loc + '/' + last_backup_date()

    # Grab last time folder
    for time_folder in os.listdir(search):
        # Exclude hidden files/folder
        if '.' not in time_folder:
            break

    # Time folder found
    if time_folder:
        return time_folder

def has_backup_dates():
    # Last date/time folder
    for has_date_folder in os.listdir(MAIN_INI_FILE.backup_dates_location()):
        # Exlude hidden files/folders
        if '.' not in has_date_folder:
            break

    return bool(has_date_folder)


if __name__ == '__main__':
    print(last_backup_time())
    pass