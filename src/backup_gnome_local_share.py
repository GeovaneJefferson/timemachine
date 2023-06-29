from setup import *
from read_ini_file import UPDATEINIFILE

foldersList = []
filesList = []
includeList = [
    "gnome_shell"
    ]

def backup_gnome_local_share():
    mainIniFile = UPDATEINIFILE()

    try:

        # .local/share/gnome-shell
        for folder in os.listdir(f"{homeUser}/.config/"):
            foldersList.append(folder)

            try:
                if folder in includeList:
                    sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/{folder} {str(mainIniFile.gnome_local_share_main_folder())}",shell=True)
            except:
                pass
    except:
        pass

if __name__ == '__main__':
    pass