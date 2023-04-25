from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de
'''
This changes:
- Color Scheme
- Fonts
- Icons
- Single Click 
- Other small folders configurations

Missing:
- Plasma Style
- Window Decoration
- Cursor

'''
somethingToRestoreInKdeGlobals = []

async def restore_kde_kwinrc():
    mainIniFile = UPDATEINIFILE()

    print("Restoring KDE kwinrc...")
    try:
        for kdeKwinRc in os.listdir(f"{mainIniFile.kde_kwinrc_main_folder()}/"):
            somethingToRestoreInKdeGlobals.append(kdeKwinRc)
       
        # # If has something to restore
        if somethingToRestoreInKdeGlobals:
            ################################################################################
            # Create .config inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.config"):
                sub.run(f"{createCMDFolder} {homeUser}/.config", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.kde_kwinrc_main_folder()}/ {homeUser}/.config", shell=True)
    except:         
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass