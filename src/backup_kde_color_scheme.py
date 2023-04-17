from setup import *
from read_ini_file import UPDATEINIFILE

def backup_kde_color_scheme():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.local/share/color-schemes/")
        sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/color-schemes/ {str(mainIniFile.color_scheme_main_folder())}",shell=True)
    except FileNotFoundError as error:
        print(error)
        pass

if __name__ == '__main__':
    pass