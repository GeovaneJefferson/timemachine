from setup import *
from read_ini_file import UPDATEINIFILE
from check_connection import is_connected
from backup_flatpak import backup_flatpak
from backup_wallpaper import backup_wallpaper
from prepare_backup import PREPAREBACKUP
# import error_catcher

# # Handle signal
# signal.signal(signal.SIGINT, error_catcher.signal_exit)
# signal.signal(signal.SIGTERM, error_catcher.signal_exit)

MAIN_INI_FILE = UPDATEINIFILE()
MAIN_PREPARE = PREPAREBACKUP()
DOWNLOADS_FOLDER_LOCATION = f"{HOME_USER}/Downloads"


def check_backup():
    # Get the current time
    current_time = str(MAIN_INI_FILE.current_time()) 

    print('Current time:', current_time)
    print()

    # Time to backup
    if current_time in MILITARY_TIME_OPTION:
        # Time to backup
        time_to_backup(current_time)
    
def time_to_backup(current_time):
    # Start backup analyses
    print("Calling analyses...")
    
    # Save current time of check
    MAIN_INI_FILE.set_database_value(
        'INFO', 'latest_backup_time_check', current_time) 

    # Backup flatpak
    backup_flatpak()
    
    # Backup wallpaper
    backup_wallpaper()

    sub.Popen(
        ['python3', SRC_ANALYSE_PY], 
        stdout=sub.PIPE, 
        stderr=sub.PIPE)
    
    exit()

if __name__ == '__main__':
    # Has connection to the backup device
    if is_connected(MAIN_INI_FILE.hd_hd()):
        # Create the main backup folder
        if not os.path.exists(MAIN_INI_FILE.main_backup_folder()):
            if MAIN_PREPARE.prepare_the_backup():
                # Set backup now to True
                MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'True') 

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
                print('Backup checker   : ON')

                # Turn on/off backup checker
                if not MAIN_INI_FILE.automatically_backup():
                    print("Automatically backup is OFF.")
                    break
                
                # Has connection to the backup device
                if is_connected(MAIN_INI_FILE.hd_hd()):
                    print('Backup connection: ON')

                    # Check for a new backup
                    check_backup()

                else:
                    print('Backup connection: OFF')

            else:
                print('Backup checker: PAUSED')
            
            print()
            time.sleep(5)

        except Exception as e:
            pass