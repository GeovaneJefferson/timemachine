from setup import *
from read_ini_file import UPDATEINIFILE

foldersList = []
filesList = []
includeList = [
    # "icons",
    "gtk-3.0",
    "gtk-4.0",
    "kdedefaults",
    "dconf",
    "fontconfig",
    "xsettingsd",
    "dolphinrc",
    "gtkrc",
    "gtkrc-2.0",
    "kdeglobals",
    "kwinrc",
    "plasmarc",
    "plasmarshellrc",
    "kglobalshortcutsrc",
    "khotkeysrc",
               ]

def backup_kde_config():
    mainIniFile = UPDATEINIFILE()

    try:
        for folders in os.listdir(f"{homeUser}/.config/"):
            foldersList.append(folders)
            try:
                if folders in includeList:
                    sub.run(f"{copyRsyncCMD} {homeUser}/.config/{folders} {str(mainIniFile.config_main_folder())}",shell=True)
            except:
                pass
            
        
    except:
        pass

if __name__ == '__main__':
    pass