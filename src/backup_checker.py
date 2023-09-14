from setup import *
from read_ini_file import UPDATEINIFILE
# from get_days_name import get_days_name
from check_connection import is_connected
from calculate_time_left_to_backup import calculate_time_left_to_backup
# from get_time import today_date
from backup_flatpak import backup_flatpak
from backup_wallpaper import backup_wallpaper
from get_backup_date import (
    get_backup_date,
    has_backup_dates,
    last_backup_date,
    last_backup_time)


# Handle signal
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


# Download folder location
DOWNLOADS_FOLDER_LOCATION = f"{HOME_USER}/Downloads"

# Found packages list
list_of_found_deb_pakages = []
list_of_found_rpm_packages = []

# Check for new .deb, .rpm etc. inside Downloads folder and back up
async def check_for_new_packages():
    print("Searching new packages inside Downloads folder...")

    # Search for .deb packages inside Downloads folder
    for package in os.listdir(DOWNLOADS_FOLDER_LOCATION):
        if package.endswith(".deb"):
            # Check if the found .deb is has not alredy been back up
            if package.split("_")[0] in (f"{MAIN_INI_FILE.deb_main_folder()}/{(package).split('_')[0]}"):
                # Add to list, so it wont back up every time the same file
                if package not in list_of_found_deb_pakages:
                    list_of_found_deb_pakages.append(package)

                    # Delete the old version before back up
                    for old_package in os.listdir(MAIN_INI_FILE.deb_main_folder()):
                        if old_package.startswith(f"{package.split('_')[0]}"):
                            # Delete old package
                            dst = MAIN_INI_FILE.deb_main_folder() + "/" + old_package
                            sub.run(["rm", "-rf", dst], stdout=sub.PIPE, stderr=sub.PIPE)

                    # backup the found package
                    src = DOWNLOADS_FOLDER_LOCATION + "/" + package
                    dst = MAIN_INI_FILE.deb_main_folder()
                    sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)

        # Search for .rpm packages inside Downloads folder
        if package.endswith(".rpm"):
            # Check if the found .rpm is has not alredy been back up
            if package.split("_")[0] in (f"{MAIN_INI_FILE.rpm_main_folder()}/{(package).split('_')[0]}"):
                # Add to list, so it wont back up every time the same file
                if package not in list_of_found_rpm_packages:
                    list_of_found_rpm_packages.append(package)

                    # Delete the old version before back up
                    for deleteOutput in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
                        if deleteOutput.startswith(f"{package.split('_')[0]}"):
                            # Delete old package
                            dst = MAIN_INI_FILE.rpm_main_folder() + "/" + old_package
                            sub.run(["rm", "-rf", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)

                    # backup the found package
                    src = DOWNLOADS_FOLDER_LOCATION + "/" + package
                    dst = MAIN_INI_FILE.rpm_main_folder()
                    sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)

async def check_backup():
    current_time_list = []
    
    # Get the current time
    current_time = MAIN_INI_FILE.current_time()

    # Add 0 if is there only 3 strings
    for i in str(current_time):
        current_time_list.append(i)

    # Add 0 to the sring if needed
    if len(current_time_list) == 3:
        current_time_list.insert(2, '0')
        current_time = str(','.join(current_time_list).replace(',',''))

    #  has backup dates
    # if has_backup_dates():
        # current_hour = MAIN_INI_FILE.current_hour()
        # dates_loc = MAIN_INI_FILE.backup_dates_location()
        # edited_time_folde = last_backup_time()
        # '''
        # if current_hour - 1: 

        # # Check if the current time - 1 hour can not be found
        # if not os.path.exist(
        #     dates_loc
        #     + '/' + last_backup_date() 
        #     + '/' + last_backup_time()):
        
        # '''        

        # # Check if time to backup has passed
        # last_backup_time_folder = (
        #     dates_loc
        #     + '/' + last_backup_date() 
        #     + '/' + last_backup_time())

    print('Current time:', current_time)
    print('Next backup :', calculate_time_left_to_backup())
    print()

    # Check if is time to backup
    if current_time in MILITARY_TIME_OPTION:
        # Backup flatpak
        await backup_flatpak()
        
        # Backup wallpaper
        await backup_wallpaper()
        
        # Start backup analyses
        await call_analyses()

async def call_analyses():
    # Call prepare backup
    print("Calling analyses...")
    
    sub.run(
        ["python3", SRC_ANALYSE_PY], 
        stdout=sub.PIPE, 
        stderr=sub.PIPE)

# # Check for previus interrupted backup
# def continue_interrupted_backup():
#     # Resume interrupted backup
#     sub.run(
#         ["python3", SRC_BACKUP_NOW_PY], stdout=sub.PIPE, stderr=sub.PIPE)

async def main():
    # Create the main backup folder
    if not os.listdir(MAIN_INI_FILE.main_backup_folder()):
        await call_analyses()

    while True:
        try:
            # Checker status
            print('Backup Checker: Running.')

            # Turn on/off backup checker
            if not MAIN_INI_FILE.automatically_backup():
                print("Automatically backup is OFF.")
                
                # Exit
                break
            
            # No connection
            if not is_connected(MAIN_INI_FILE.hd_hd()):
                # Device is not connected
                print('Backup device is not connected.')

            else:
                # Backing up now
                if MAIN_INI_FILE.get_database_value(
                    'STATUS', 'backing_up_now'):
                    print('Closing backup checker, reason: Backing up now.')
                    
                    # Exit
                    break

                # TODO
                # # If previus backup is unfinished
                # if MAIN_INI_FILE.get_database_value(
                #     'STATUS', 'unfinished_backup'):
                #     continue_interrupted_backup()

                # backup new packages
                await check_for_new_packages()

                # Check for a new backup
                await check_backup()

            # wait 
            time.sleep(5)

        except:
            # Exit
            break

    exit()


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    asyncio.run(main())
    