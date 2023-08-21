from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_kde_share_config():
    try:
        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.kde_share_config_main_folder()}/ {HOME_USER}/.kde/share/", shell=True)
    except Exception:
        pass

    return "Task completed: restore kde share config"


if __name__ == '__main__':
    pass
