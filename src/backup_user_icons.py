from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_icon import users_icon_name

def backup_user_icons():
    MAININIFILE=UPDATEINIFILE()

    try:
        os.listdir(f"/usr/share/icons/{users_icon_name()}")
        sub.run(f"{COPY_RSYNC_CMD} /usr/share/icons/ {str(MAININIFILE.icon_main_folder())}",shell=True)
    
    except: 
        try:
            os.listdir(f"{HOME_USER}/icons/{users_icon_name()}")
            sub.run(f"{COPY_RSYNC_CMD} {HOME_USER}/.icons/ {str(MAININIFILE.icon_main_folder())}",shell=True)
        
        except FileNotFoundError:
            sub.run(f"{COPY_RSYNC_CMD} {HOME_USER}/.local/share/icons/ {str(MAININIFILE.icon_main_folder())}",shell=True)
