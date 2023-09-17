from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def all_date_folder_list():
    date_list = []
    
    # Get all dates folders
    for date in os.listdir(str(MAIN_INI_FILE.backup_folder_name())):
        # Only date folders
        if '-' in date:
            date_list.append(date)

    # Has date folder inside
    return date_list

def latest_backup_date_label():
    from get_backup_time import get_latest_backup_time

    # Has date folder inside
    if all_date_folder_list():
        # Sort list to get the latest
        all_date_folder_list().sort(
            reverse = True, 
            key = lambda date:
            datetime.strptime(date, "%d-%m-%y"))
        
        latest_backup = str(
            get_latest_backup_time()[0]).replace("-",":")

        # Date/time
        # Today
        if all_date_folder_list()[0] == (
            f'{MAIN_INI_FILE.current_date()}-{MAIN_INI_FILE.current_month()}-{MAIN_INI_FILE.current_year()}'): 
            return 'Today,', latest_backup
        
        # Yesterday
        else:
            # Check todays date, if last backup was Yesterday, return Yesterday
            if int(
                MAIN_INI_FILE.current_date()) - int(all_date_folder_list()[0][:2]) == 1:
                return 'Yesterday,', latest_backup
            
            else:
                return all_date_folder_list()[0]

    else:
        # Return latest backup to main folder
        return MAIN_INI_FILE.oldest_backup_date()


def latest_backup_date():
    # Has date folder inside
    if all_date_folder_list():
        # Sort list to get the latest
        all_date_folder_list().sort(
            reverse=True,
            key=lambda
            date: datetime.strptime(date, "%d-%m-%y"))
        
        # No date/time folders found
        return all_date_folder_list()[0]

    else:
        # Return latest 'checked' backup date
        '''
        This will return last time a new file was backup to main.
        No date/time folder was created yet.
        '''
        
        # Return latest backup to main folder
        return MAIN_INI_FILE.oldest_backup_date()


if __name__ == '__main__':
    pass