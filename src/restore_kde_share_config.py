from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_kde_share_config():
    try:
        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.kde_share_config_main_folder()}/ {HOME_USER}/.kde/share/", shell=True)
        notification_message_current_backing_up(f'Restoring: {MAIN_INI_FILE.kde_share_config_main_folder()}...')
    except Exception:
        pass

    return "Task completed: restore kde share config"


if __name__ == '__main__':
    pass
