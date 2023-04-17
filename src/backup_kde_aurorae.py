from setup import *
from read_ini_file import UPDATEINIFILE

def backup_kde_aurorae():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.local/share/aurorae/")
        sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/aurorae/ {str(mainIniFile.aurorae_main_folder())}",shell=True)
    except FileNotFoundError as error:
        print(error)
        pass

if __name__ == '__main__':
    pass