from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_kde_local_share():
    try:
        sub.run(f"{"rsync", "-avr"} {MAIN_INI_FILE.kde_local_share_main_folder()}/ {HOME_USER}/.local/share/", shell=True)
        notification_message_current_backing_up(f'Restoring: {MAIN_INI_FILE.kde_local_share_main_folder()}...')
    except Exception:
        pass

    return "Task completed: restore kde local share"


if __name__ == '__main__':
    pass

