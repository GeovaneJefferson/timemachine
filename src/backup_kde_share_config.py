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

def backup_kde_share_config():
    mainIniFile = UPDATEINIFILE()

    try:
        for folders in os.listdir(f"{homeUser}/.kde/share/"):
            foldersList.append(folders)
            try:
                print(folders)
                # sub.run(f"{copyRsyncCMD} {homeUser}/.kde/share/{folders} {str(mainIniFile.kde_share_config_main_folder())}",shell=True)
            except:
                pass
            
        
    except FileNotFoundError as error:
        print(error)
        pass

if __name__ == '__main__':
    pass