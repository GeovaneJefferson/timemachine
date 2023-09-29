from setup import *
from read_ini_file import UPDATEINIFILE
from check_connection import is_connected
from backup_flatpak import backup_flatpak
from backup_wallpaper import backup_wallpaper
from prepare_backup import PREPAREBACKUP

# Handle signal
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)

# Download folder location
DOWNLOADS_FOLDER_LOCATION = f"{HOME_USER}/Downloads"

# Found packages list
list_of_found_deb_pakages = []
list_of_found_rpm_packages = []

# # Check for previus interrupted backup
# def continue_interrupted_backup():
#     # Resume interrupted backup
#     sub.run(
#         ['python3', SRC_BACKUP_NOW_PY], stdout=sub.PIPE, stderr=sub.PIPE)

def call_analyses():
    # Call prepare backup
    print("Calling analyses...")
    
    sub.Popen(
        ['python3', SRC_ANALYSE_PY], 
            stdout=sub.PIPE, 
            stderr=sub.PIPE)

# Check for new .deb, .rpm etc. inside Downloads folder and back up
def check_for_new_packages():
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
                            sub.run(["rm", "-rf", dst], 
                                stdout=sub.PIPE, 
                                stderr=sub.PIPE)

                    # backup the found package
                    src = DOWNLOADS_FOLDER_LOCATION + "/" + package
                    dst = MAIN_INI_FILE.deb_main_folder()
                    sub.run(['cp', '-rvf', src, dst], 
                        stdout=sub.PIPE, 
                        stderr=sub.PIPE)

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
                            sub.run(["rm", "-rf", src, dst], 
                                stdout=sub.PIPE, 
                                stderr=sub.PIPE)

                    # backup the found package
                    src = DOWNLOADS_FOLDER_LOCATION + "/" + package
                    dst = MAIN_INI_FILE.rpm_main_folder()
                    sub.run(['cp', '-rvf', src, dst], 
                        stdout=sub.PIPE, 
                        stderr=sub.PIPE)

def check_backup():
    # Get the current time
    current_time = str(MAIN_INI_FILE.current_time()) 
    # current_hour = int(MAIN_INI_FILE.current_hour())
    # short_last_backup_time = int(MAIN_INI_FILE.latest_checked_backup_time()[:2]) 

    print('Current time:', current_time)
    print(MILITARY_TIME_OPTION)
    print()

    # Time to backup
    if current_time in MILITARY_TIME_OPTION:
        # Time to backup
        time_to_backup(current_time)
    
    # # Compare the first 2 digits of current and latest backup to main hour
    # # Fx. 1200 -> 12
    # elif MAIN_INI_FILE.latest_checked_backup_time() != 'None':
    #     if current_hour - short_last_backup_time >= 1:
    #         # Time to backup
    #         time_to_backup(current_time)

def time_to_backup(current_time):
    # Save current time of check
    MAIN_INI_FILE.set_database_value(
        'INFO', 'latest_backup_time_check', current_time) 

    # Backup flatpak
    backup_flatpak()
    
    # Backup wallpaper
    backup_wallpaper()
    
    # Start backup analyses
    call_analyses()


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    MAIN_PREPARE = PREPAREBACKUP()
    
    # Create the main backup folder
    if not os.path.exists(MAIN_INI_FILE.main_backup_folder()):
        if MAIN_PREPARE.prepare_the_backup():
            # Backup now
            sub.Popen(
                ['python3', SRC_BACKUP_NOW_PY], 
                    stdout=sub.PIPE, 
                    stderr=sub.PIPE)

    while True:
        # Not current backing up
        if not MAIN_INI_FILE.current_backing_up():
            print('Backup checker: ON')

            # Turn on/off backup checker
            if not MAIN_INI_FILE.automatically_backup():
                print("Automatically backup is OFF.")
                exit()
            
            # Has connection
            if is_connected(MAIN_INI_FILE.hd_hd()):
                # backup new packages
                # check_for_new_packages()

                # Check for a new backup
                check_backup()

        else:
            print('Backup checker: PAUSED')
        
        time.sleep(5)