from setup import *
from read_ini_file import UPDATEINIFILE

def backup_kde_scripts_folder():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.local/share/kwin/scripts/")
        sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/kwin/scripts/ {str(mainIniFile.kde_scripts_main_folder())}",shell=True)
    except FileNotFoundError as error:
        print(error)
        pass

if __name__ == '__main__':
    pass