from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_kde_config():
    try:
        src = MAIN_INI_FILE.kde_config_main_folder() + '/'
        dst = HOME_USER + '/.config/'
        shutil.copy2(src, dst)
    except Exception as error:
        print(error)
        pass


if __name__ == '__main__':
    pass
