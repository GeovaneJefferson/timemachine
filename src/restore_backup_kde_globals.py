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

def restore_backup_kde_globals():
    mainIniFile = UPDATEINIFILE()

    print("Restoring KDE Globals...")
    try:
        for kdeGlobals in os.listdir(f"{mainIniFile.kde_globals_main_folder()}/"):
            somethingToRestoreInKdeGlobals.append(kdeGlobals)
       
        # # If has something to restore
        if somethingToRestoreInKdeGlobals:
            ################################################################################
            # Create .config inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.config"):
                sub.run(f"{createCMDFolder} {homeUser}/.config", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.kde_globals_main_folder()}/ {homeUser}/.config", shell=True)
    except:         
        pass