from setup import *
from read_ini_file import UPDATEINIFILE


def backup_user_fonts():
    MAININIFILE=UPDATEINIFILE()

    try:
        os.listdir(f"{HOME_USER}/.fonts")
        sub.run(f"{COPY_RSYNC_CMD} {HOME_USER}/.fonts/ {str(MAININIFILE.fonts_main_folder())}",shell=True)
    except:
        pass

    try:
        os.listdir(f"{HOME_USER}/.local/share/fonts")
        sub.run(f"{COPY_RSYNC_CMD} {HOME_USER}/.local/share/fonts/ {str(MAININIFILE.fonts_main_folder())}",shell=True)
    except:
        pass

if __name__ == '__main__':
    pass