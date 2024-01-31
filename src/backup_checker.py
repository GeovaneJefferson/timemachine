from setup import *
from read_ini_file import UPDATEINIFILE
from check_connection import is_connected
from backup_flatpak import backup_flatpak
from backup_pip_packages import backup_pip_packages
from backup_wallpaper import backup_wallpaper
from prepare_backup import PREPAREBACKUP

# Found packages list
list_of_found_deb_pakages = []
list_of_found_rpm_packages = []

MAIN_INI_FILE = UPDATEINIFILE()
MAIN_PREPARE = PREPAREBACKUP()
DOWNLOADS_FOLDER_LOCATION = f"{HOME_USER}/Downloads"

# Check for new .deb, .rpm etc. inside Downloads folder and back up
def check_for_new_packages():
    print("Searching new packages inside Downloads folder...")

    # Search for .deb packages inside Downloads folder
    for package in os.listdir(DOWNLOADS_FOLDER_LOCATION):
        if package.endswith(".deb"):
            # Check if the found .deb is has not alredy been back up
            if package.split("_")[0] in (
                f"{MAIN_INI_FILE.deb_main_folder()}/{(package).split('_')[0]}"):
                # Add to list, so it wont back up every time the same file
                if package not in list_of_found_deb_pakages:
                    list_of_found_deb_pakages.append(package)

                    # Delete the old version before back up
                    for old_package in os.listdir(MAIN_INI_FILE.deb_main_folder()):
                        if old_package.startswith(f"{package.split('_')[0]}"):
                            # Delete old package
                            dst = MAIN_INI_FILE.deb_main_folder() + "/" + old_package
                            sub.run(
                                ["rm", "-rf", dst], 
                                stdout=sub.PIPE, 
                                stderr=sub.PIPE)

                    # backup the found package
                    src = DOWNLOADS_FOLDER_LOCATION + "/" + package
                    dst = MAIN_INI_FILE.deb_main_folder()
                    sub.run(
                        ['cp', '-rvf', src, dst], 
                        stdout=sub.PIPE, 
                        stderr=sub.PIPE)

        # Search for .rpm packages inside Downloads folder
        if package.endswith(".rpm"):
            # Check if the found .rpm is has not alredy been back up
            if package.split("_")[0] in (
                f"{MAIN_INI_FILE.rpm_main_folder()}/{(package).split('_')[0]}"):
                # Add to list, so it wont back up every time the same file
                if package not in list_of_found_rpm_packages:
                    list_of_found_rpm_packages.append(package)

                    # Delete the old version before back up
                    for deleteOutput in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
                        if deleteOutput.startswith(f"{package.split('_')[0]}"):
                            # Delete old package
                            dst = MAIN_INI_FILE.rpm_main_folder() + "/" + old_package
                            sub.run(
                                ["rm", "-rf", src, dst], 
                                stdout=sub.PIPE, 
                                stderr=sub.PIPE)

                    # backup the found package
                    src = DOWNLOADS_FOLDER_LOCATION + "/" + package
                    dst = MAIN_INI_FILE.rpm_main_folder()
                    sub.run(
                        ['cp', '-rvf', src, dst], 
                        stdout=sub.PIPE, 
                        stderr=sub.PIPE)

def time_to_backup(current_time):
    
    # Save current time of check
    MAIN_INI_FILE.set_database_value(
        'INFO', 'latest_backup_time_check', current_time) 

    print("Calling analyses...")

    try:
        x = sub.Popen(
            ['python3', SRC_ANALYSE_PY], 
            stdout=sub.PIPE, 
            stderr=sub.PIPE)
        
        output, error = x.communicate()

            # Check the return code
        if x.returncode == 0:
            print(f"Backup process completed successfully. Output: {output}")
        else:
            print(f"Error in backup process. Output: {output}, Error: {error}")
    except Exception as e:
        # Save error log
        MAIN_INI_FILE.report_error(e)

    exit()

        # x = sub.Popen(
        #     ['python3', SRC_ANALYSE_PY],
        #         stdout=sub.PIPE,
        #         stderr=sub.PIPE)
        
        # output, error = x.communicate()

        #     # Check the return code
        # if x.returncode == 0:
        #     print(f"Backup process completed successfully. Output: {output}")
        # else:
        #     print(f"Error in backup process. Output: {output}, Error: {error}")
    

# if __name__ == '__main__':
# Has connection to the backup device

# Set the process name
setproctitle.setproctitle("Time Machine - Backup Checker")

if is_connected(MAIN_INI_FILE.hd_hd()):
    # Create the main backup folder
    if not os.path.exists(MAIN_INI_FILE.create_base_folder()):
        if MAIN_PREPARE.prepare_the_backup():
            # Set backup now to True
            MAIN_INI_FILE.set_database_value(
                'STATUS', 'backing_up_now', 'True') 

            # Backup now
            sub.Popen(
                ['python3', SRC_BACKUP_NOW_PY], 
                    stdout=sub.PIPE, 
                    stderr=sub.PIPE)

            # Exit
            exit()

while True:
    try:
        # Not current backing up
        if not MAIN_INI_FILE.current_backing_up():

            # Turn on/off backup checker
            if not MAIN_INI_FILE.automatically_backup():
                print("Automatically backup is OFF.")
                break
            
            print('Backup checker   : ON')
            
            # Has connection to the backup device
            if is_connected(MAIN_INI_FILE.hd_hd()):
                print('Backup connection: ON')

                # Check for a new backup
                # Get the current time
                current_time = str(MAIN_INI_FILE.current_time()) 

                print('Current time:', current_time)
                print('Backup time:', MILITARY_TIME_OPTION)
                print()

                # Time to backup
                if current_time in MILITARY_TIME_OPTION:
                    # Time to backup
                    time_to_backup(current_time)
                

                # Check for new packages to backup
                check_for_new_packages()

            else:
                print('Backup connection: OFF')

        else:
            print('Backup checker: PAUSED')
        
        time.sleep(5)

    except Exception as e:
        # Save error log
        # MAIN_INI_FILE.report_error(e)
        pass