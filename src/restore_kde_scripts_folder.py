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
somethingToRestoreInKdescripts = []

def restore_kde_scripts_folder():
    mainIniFile = UPDATEINIFILE()

    print("Restoring KDE Scripts...")
    try:
        for kdeScripts in os.listdir(f"{mainIniFile.kde_scripts_main_folder()}/"):
            somethingToRestoreInKdescripts.append(kdeScripts)
       
        # # If has something to restore
        if somethingToRestoreInKdescripts:
            ################################################################################
            # Create .config inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.local/share/kwin/scripts/"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/kwin/scripts", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.kde_scripts_main_folder()}/ {homeUser}/.local/share/kwin/scripts/", shell=True)
    except:         
        pass