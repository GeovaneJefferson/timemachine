from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_kde_local_share():
    try:
        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.kde_local_share_main_folder()}/ {HOME_USER}/.local/share/", shell=True)
    except Exception as e:
        print(e)         
        pass

    return "Task completed: restore kde local share"


if __name__ == '__main__':
    pass

