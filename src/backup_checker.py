from setup import *
from read_ini_file import UPDATEINIFILE
from check_connection import is_connected
from backup_flatpak import backup_flatpak
from backup_wallpaper import backup_wallpaper
from prepare_backup import PREPAREBACKUP
import error_catcher as error_catcher

# Handle signal
signal.signal(signal.SIGINT, error_catcher.signal_exit)
signal.signal(signal.SIGTERM, error_catcher.signal_exit)

MAIN_INI_FILE = UPDATEINIFILE()
MAIN_PREPARE = PREPAREBACKUP()
DOWNLOADS_FOLDER_LOCATION = f"{HOME_USER}/Downloads"

# Get the current time
current_time = str(MAIN_INI_FILE.current_time()) 

def check_backup():
    print('Current time:', current_time)
    print()

    # Time to backup
    if current_time in MILITARY_TIME_OPTION:
        # Time to backup
        time_to_backup()
    
def time_to_backup():
    # Save current time of check
    MAIN_INI_FILE.set_database_value(
        'INFO', 'latest_backup_time_check', current_time) 

    # Backup flatpak
    backup_flatpak()
    
    # Backup wallpaper
    backup_wallpaper()
    
    # Start backup analyses
    print("Calling analyses...")
    
    sub.Popen(
        ['python3', SRC_ANALYSE_PY], 
        stdout=sub.PIPE, 
        stderr=sub.PIPE)
    

if __name__ == '__main__':
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
                # Check for a new backup
                check_backup()

        else:
            print('Backup checker: PAUSED')
        
        time.sleep(5)