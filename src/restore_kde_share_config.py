from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def restore_kde_share_config():
    try:
        src = MAIN_INI_FILE.kde_share_config_main_folder()
        dst = os.path.join(HOME_USER, '.kde/share/')

        print('-----[.KDE/SHARE]-----')
        print('From:', src)
        print('To:', dst)

        shutil.copytree(src, dst, dirs_exist_ok= True)
    except Exception as error:
        print(error)
        # Save error log
        MAIN_INI_FILE.report_error(error)


if __name__ == '__main__':
    pass
