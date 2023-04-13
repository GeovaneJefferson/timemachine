from setup import *
from read_ini_file import UPDATEINIFILE

def backup_kde_kwinrc():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.config/kwinrc")
        sub.run(f"{copyRsyncCMD} {homeUser}/.config/kwinrc {str(mainIniFile.kde_kwinrc_main_folder())}",shell=True)
    except FileNotFoundError as error:
        print(error)
        pass