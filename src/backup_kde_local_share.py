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
    # "fonts",
    "kate",
    "kxmlgui5"
               ]

def backup_kde_local_share():
    mainIniFile = UPDATEINIFILE()

    try:
        for folders in os.listdir(f"{homeUser}/.local/share/"):
            foldersList.append(folders)
            try:
                if folders in includeList:
                    # print(folders)
                    sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/{folders} {str(mainIniFile.kde_local_share_main_folder())}",shell=True)
            except:
                pass
            
        
    except FileNotFoundError as error:
        print(error)
        pass

if __name__ == '__main__':
    pass