from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()


async def restore_backup_flatpaks_applications():
    print("Installing flatpaks apps...")
    
    # Read flatpaks and add to exclude
    with open(f"{MAIN_INI_FILE.exclude_flatpaks_location()}", 'r') as read_exclude:
        read_exclude = read_exclude.read().split("\n")
  
    with open(f"{MAIN_INI_FILE.flatpak_txt_location()}", "r") as read_flatpak_file:
        read_flatpak_file = read_flatpak_file.readlines()
        
        for flatpak in read_flatpak_file:
            flatpak = flatpak.strip('\n')
            
            if flatpak not in read_exclude:
                # Install only if flatpak if not in the exclude app list
                try:
                    # Update DB
                    MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', f'{flatpak}')
                    # Update notification
                    notification_message_current_backing_up(f'Installing: {flatpak}...')
                    # Install it
                    sub.run(f"{FLATPAK_INSTALL_CMD} {flatpak}", shell=True)
                except:
                    pass
                
    return "Task completed: Wallpaper"


if __name__ == '__main__':
    pass