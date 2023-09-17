from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()
all_date_folder_list = []

def has_date_folder():
    # Get all dates folders
    for date in os.listdir(str(MAIN_INI_FILE.backup_folder_name())):
        # Only date folders
        if '-' in date:
            all_date_folder_list.append(date)

    if all_date_folder_list:
        # Has date folder inside
        return True

    else:
        return False

def latest_backup_date_label():
    # Has date folder inside
    if has_date_folder():
        # Sort list to get the latest
        all_date_folder_list.sort(
            reverse = True, 
            key = lambda date:
            datetime.strptime(date, "%d-%m-%y"))
        
        # Get latest backup time
        from get_backup_time import get_latest_backup_time
        
        # has time
        if get_latest_backup_time is not None:
            latest_backup = str(
                get_latest_backup_time()[0]).replace("-",":")
        
            # Return 'Today', 'yesterday' or Nothing ''
            return date_timeframe() + latest_backup
        
    else:
        # check date timeframe

        # Return latest backup to main folder
        return date_timeframe() + MAIN_INI_FILE.latest_backup_date()


def latest_backup_date():
    # Has date folder inside
    if has_date_folder():
        # Sort list to get the latest
        all_date_folder_list.sort(
            reverse=True,
            key=lambda
            date: datetime.strptime(date, "%d-%m-%y"))
        
        # No date/time folders found
        return all_date_folder_list[0]

    else:
        # Return latest 'checked' backup date
        '''
        This will return last time a new file was backup to main.
        No date/time folder was created yet.
        '''
        
        # Return latest backup to main folder
        return MAIN_INI_FILE.latest_backup_date()

def date_timeframe():
    todays_date = (
            f'{MAIN_INI_FILE.current_date()}-{MAIN_INI_FILE.current_month()}-{MAIN_INI_FILE.current_year()}')
    
    # Date/time
    if has_date_folder():
        # Last backup date match with todays date
        if all_date_folder_list[0] == todays_date:
            return 'Today, '
        
        # Yesterday
        # Last backup date match with yesterdays date
        else:
            # Check todays date, if last backup was Yesterday, return Yesterday
            if (int(
                MAIN_INI_FILE.current_date()) - 
                int(all_date_folder_list[0][:2]) == 1):
                
                # return 'Yesterday,', latest_backup
                return 'Yesterday, '
            
    # Main
    else:
        # Latest backup to main match with todays date
        if todays_date in MAIN_INI_FILE.latest_backup_date():
            return 'Today, '
        # Check todays date, if last backup was Yesterday, return Yesterday
        elif (int(
            MAIN_INI_FILE.current_date()) - 
            int(all_date_folder_list[0][:2]) == 1):
            
            # return 'Yesterday,', latest_backup
            return 'Yesterday, '
        
        else:
            return ''

if __name__ == '__main__':
    print(latest_backup_date_label())
    pass