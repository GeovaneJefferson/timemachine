from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()


def latest_backup_date_label():
    from get_backup_time import get_latest_backup_time

    latest_backup_list = []
            
    # Get all dates folders
    for date in os.listdir(str(MAIN_INI_FILE.backup_folder_name())):
        # Only date folders
        if '-' in date:
            latest_backup_list.append(date)

    # Date/time backup folders
    if latest_backup_list:
        # Sort list
        latest_backup_list.sort(
            reverse = True, 
            key = lambda date:
            datetime.strptime(date, "%d-%m-%y"))
        
        latest_backup = str(
            get_latest_backup_time()[0]).replace("-",":")
        
        # Today
        if latest_backup_list[0] == (
            f'{MAIN_INI_FILE.current_date()}-{MAIN_INI_FILE.current_month()}-{MAIN_INI_FILE.current_year()}'): 
            return f"Today, {latest_backup}"
        
        # Yesterday
        else:
            # Check todays date, if last backup was Yesterday, return Yesterday
            if int(
                MAIN_INI_FILE.current_date()) - int(latest_backup_list[0][:2]) == 1:
                return f"Yesterday, {latest_backup}"
            
            else:
                return latest_backup_list[0]

    else:
        # Return latest backup to main folder
        return MAIN_INI_FILE.latest_backup_date()


def latest_backup_date():
    latest_backup_list = []

    try:
        for date in os.listdir(str(MAIN_INI_FILE.backup_folder_name())):
            # Only date folders
            if '-' in date:
                latest_backup_list.append(date)

        # Sort list
        latest_backup_list.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
        
        # No date/time folders found
        if not latest_backup_list:
            # Return latest 'checked' backup date
            '''
            This will return last time a new file was backup to main.
            No date/time folder was created yet.
            '''
            
            # Return latest backup to main folder
            return MAIN_INI_FILE.latest_backup_date()

        else:
            return latest_backup_list[0]
    
    except:
        pass


if __name__ == '__main__':
    pass