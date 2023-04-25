from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

somethingToRestoreInKdeNotes = []

async def restore_kde_notes_folder():
    mainIniFile = UPDATEINIFILE()

    print("Restoring KDE Notes...")
    try:
        for kdeNotes in os.listdir(f"{mainIniFile.kde_notes_main_folder()}/"):
            somethingToRestoreInKdeNotes.append(kdeNotes)
       
        # # If has something to restore
        if somethingToRestoreInKdeNotes:
            if not os.path.exists(f"{homeUser}/.local/share/plasma_notes/"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/plasma_notes", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.kde_notes_main_folder()}/ {homeUser}/.local/share/plasma_notes/", shell=True)
    except:         
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass