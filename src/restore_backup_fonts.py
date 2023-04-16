from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

somethingToRestoreInFonts = []

def restore_backup_fonts():
    mainIniFile = UPDATEINIFILE()

    print("Restoring fonts...")
    try:
        for fonts in os.listdir(f"{mainIniFile.fonts_main_folder()}/"):
            somethingToRestoreInFonts.append(fonts)
       
        # # If has something to restore
        if somethingToRestoreInFonts:
            ################################################################################
            # Create .local/share/icons inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.local/share/fonts"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/fonts", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.fonts_main_folder()}/ {homeUser}/.local/share/fonts", shell=True)
    except:         
        pass