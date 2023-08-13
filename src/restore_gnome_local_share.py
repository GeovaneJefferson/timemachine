from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_gnome_local_share():
    try:
        # Back up .local/share/gnome-shell
        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.kde_local_share_main_folder()}/ {HOME_USER}/.local/share/gnome-shell", shell=True)
    
    except Exception as e:
        print(e)         
        pass

    return "Task completed: restore gnome local share"


if __name__ == '__main__':
    pass

