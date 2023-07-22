from setup import *
from read_ini_file import UPDATEINIFILE


async def restore_backup_flatpaks_applications():
    MAININIFILE=UPDATEINIFILE()

    print("Installing flatpaks apps...")
    # Restore flatpak apps
    with open(f"{MAININIFILE.flatpak_txt_location()}", "r") as read_file:
        read_file=read_file.readlines()

        for output in read_file:
            output=output.strip()
            
            config=configparser.ConfigParser()
            config.read(SRC_USER_CONFIG) 
            with open(SRC_USER_CONFIG, 'w') as configfile:
                config.set('INFO', 'current_backing_up', f"{output}")
                config.write(configfile)

            sub.run(f"{FLATPAK_INSTALL_CMD} {output}", shell=True)
    
    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass