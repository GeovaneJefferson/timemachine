from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def restore_kde_local_share():
    try:
        src = MAIN_INI_FILE.kde_local_share_main_folder() + '/'
        dst = os.path.join(HOME_USER, '.local/share/')
        shutil.copy2(src, dst)
    except Exception:
        pass


if __name__ == '__main__':
    pass
