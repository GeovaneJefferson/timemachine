from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_kde_share_config():
    try:
        src = MAIN_INI_FILE.kde_share_config_main_folder() + "/"
        dst = HOME_USER + "/.kde/share/"
        sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)

        notification_message_current_backing_up(f'Restoring: {MAIN_INI_FILE.kde_share_config_main_folder()}...')

    except Exception:
        pass


if __name__ == '__main__':
    pass
