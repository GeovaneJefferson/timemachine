from setup import *
from read_ini_file import UPDATEINIFILE

folderList = []
filesList = []
includeList = [
    "dconf"
        ]

def backup_gnome_config():
    mainIniFile = UPDATEINIFILE()

    try:
        # Backup .config/
        for folder in os.listdir(f"{homeUser}/.config/"):
            folderList.append(folder)

            try:
                if folder in includeList:
                    sub.run(f"{copyRsyncCMD} {homeUser}/.config/{folder} {str(mainIniFile.gnome_config_main_folder())}",shell=True)
            
            except:
                pass
        
    except:
        pass

if __name__ == '__main__':
    pass