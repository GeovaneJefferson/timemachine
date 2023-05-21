from setup import *
from read_ini_file import UPDATEINIFILE

foldersList = []
filesList = []
includeList = [
    # "icons",
    "kwin",
    "plasma_notes",
    "plasma",
    "aurorae",
    "color-schemes",
    "fonts",
    "kate",
    "kxmlgui5"
    "icons"
    "themes"
               ]

def backup_local_share():
    mainIniFile = UPDATEINIFILE()

    try:
        for folders in os.listdir(f"{homeUser}/.local/share/"):
            foldersList.append(folders)

            # .local/share
            try:
                if folders in includeList:
                    sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/{folders} {str(mainIniFile.local_share_main_folder())}",shell=True)
            
            except:
                pass
                    
    except:
        pass

if __name__ == '__main__':
    pass