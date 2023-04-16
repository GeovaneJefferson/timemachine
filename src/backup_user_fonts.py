from setup import *
from read_ini_file import UPDATEINIFILE


def backup_user_fonts():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.fonts")
        sub.run(f"{copyRsyncCMD} {homeUser}/.fonts/ {str(mainIniFile.fonts_main_folder())}",shell=True)
    except:
        pass

    try:
        os.listdir(f"{homeUser}/.local/share/fonts")
        sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/fonts/ {str(mainIniFile.fonts_main_folder())}",shell=True)
    except:
        pass

if __name__ == '__main__':
    pass