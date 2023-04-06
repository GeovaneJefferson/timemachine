from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

somethingToRestoreInTheme = []

def restore_backup_theme():
    mainIniFile = UPDATEINIFILE()

    print("Restoring theme...")
    try:
        # Check for theme to be restored
        for theme in os.listdir(f"{mainIniFile.theme_main_folder()}/"):
            somethingToRestoreInTheme.append(theme)

        # If has something to restore
        if somethingToRestoreInTheme:
            ################################################################################
            # Create .themes inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.local/share/themes"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/themes", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.theme_main_folder()}/ {homeUser}/.local/share/themes", shell=True)

            for count in range(len(supportedOS)):
                if supportedOS[count] in str(get_user_de()):
                    try:
                        os.listdir(f"/usr/share/themes/{theme}/")
                        sub.run(f"{setUserThemeCMD} {theme}", shell=True)
                    except:
                        sub.run(f"{setUserThemeCMD} {theme}", shell=True)
                    else:
                        pass
    except:
        pass