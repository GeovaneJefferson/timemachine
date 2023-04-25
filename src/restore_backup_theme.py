from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

somethingToRestoreInTheme = []

async def restore_backup_theme():
    mainIniFile = UPDATEINIFILE()

    print("Restoring theme...")
    try:
        # Check for theme to be restored
        for theme in os.listdir(f"{mainIniFile.gtk_theme_main_folder()}/"):
            somethingToRestoreInTheme.append(theme)

        # If has something to restore
        if somethingToRestoreInTheme:
            ################################################################################
            # Create .themes inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.local/share/themes"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/themes", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.gtk_theme_main_folder()}/ {homeUser}/.local/share/themes", shell=True)

            if get_user_de() != 'kde': 
                try:
                    os.listdir(f"/usr/share/themes/{mainIniFile.ini_info_gtktheme()}")
                    sub.run(f"{setUserThemeCMD} {mainIniFile.ini_info_gtktheme()}", shell=True)
                except:
                    # try:
                    os.listdir(f"{homeUser}/.local/share/themes/{mainIniFile.ini_info_gtktheme()}")
                    sub.run(f"{setUserThemeCMD} {mainIniFile.ini_info_gtktheme()}", shell=True)
                    # except:
                    #     os.listdir(f"{homeUser}/.themes/{mainIniFile.ini_info_gtktheme()}")
                    #     sub.run(f"{setUserThemeCMD} {mainIniFile.ini_info_gtktheme()}", shell=True)
    except:     
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass