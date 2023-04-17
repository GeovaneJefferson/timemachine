from setup import *
from read_ini_file import UPDATEINIFILE

def backup_kde_plasma_folder():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.local/share/plasma/")
        sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/plasma/ {str(mainIniFile.plasma_main_folder())}",shell=True)
    except FileNotFoundError as error:
        print(error)
        pass

if __name__ == '__main__':
    pass