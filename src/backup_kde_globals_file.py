from setup import *
from read_ini_file import UPDATEINIFILE

def backup_kde_globals_file():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.config/kdeglobals")
        sub.run(f"{copyRsyncCMD} {homeUser}/.config/kdeglobals {str(mainIniFile.kde_globals_main_folder())}",shell=True)
    except FileNotFoundError as error:
        print(error)
        pass