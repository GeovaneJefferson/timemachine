from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_kde_share_config():
    try:
        src = MAIN_INI_FILE.kde_share_config_main_folder() + '/'
        dst = os.path.join(HOME_USER, '.kde/share/')
        shutil.copy2(src, dst)
    except Exception as error:
        print(error)
        pass


if __name__ == '__main__':
    pass
