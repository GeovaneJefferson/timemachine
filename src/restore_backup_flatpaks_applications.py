from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_backup_flatpaks_applications():
    print("Installing flatpaks apps...")
    # Restore flatpak apps
    with open(f"{MAIN_INI_FILE.flatpak_txt_location()}", "r") as read_file:
        read_file=read_file.readlines()

        for output in read_file:
            output = output.strip()
            MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', f'{output}')
            
            sub.run(f"{FLATPAK_INSTALL_CMD} {output}", shell=True)
    
    return "Task completed: Wallpaper"


if __name__ == '__main__':
    pass