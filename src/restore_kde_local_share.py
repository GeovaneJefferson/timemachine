from setup import *
from read_ini_file import UPDATEINIFILE

async def restore_kde_local_share():
    MAININIFILE=UPDATEINIFILE()

    try:
        sub.run(f"{COPY_RSYNC_CMD} {MAININIFILE.kde_local_share_main_folder()}/ {HOME_USER}/.local/share/", shell=True)
    except:         
        pass

    return "Task completed: restore kde local share"


if __name__ == '__main__':
    pass

