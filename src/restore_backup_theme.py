from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de

somethingToRestoreInTheme=[]

async def restore_backup_theme():
    MAININIFILE=UPDATEINIFILE()

    print("Restoring theme...")
    try:
        # Check for theme to be restored
        for theme in os.listdir(f"{MAININIFILE.gtk_theme_main_folder()}/"):
            somethingToRestoreInTheme.append(theme)

        # If has something to restore
        if somethingToRestoreInTheme:
            ################################################################################
            # Create .themes inside home user
            ################################################################################
            if not os.path.exists(f"{HOME_USER}/.local/share/themes"):
                sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/themes", shell=True)   

            sub.run(f"{COPY_RSYNC_CMD} {MAININIFILE.gtk_theme_main_folder()}/ {HOME_USER}/.local/share/themes", shell=True)

            if get_user_de() != 'kde': 
                try:
                    os.listdir(f"/usr/share/themes/{MAININIFILE.ini_info_gtktheme()}")
                    sub.run(f"{SET_USER_THEME_CMD} {MAININIFILE.ini_info_gtktheme()}", shell=True)
                except:
                    # try:
                    os.listdir(f"{HOME_USER}/.local/share/themes/{MAININIFILE.ini_info_gtktheme()}")
                    sub.run(f"{SET_USER_THEME_CMD} {MAININIFILE.ini_info_gtktheme()}", shell=True)
                    # except:
                    #     os.listdir(f"{homeUser}/.themes/{MAININIFILE.ini_info_gtktheme()}")
                    #     sub.run(f"{setUserThemeCMD} {MAININIFILE.ini_info_gtktheme()}", shell=True)
    except:     
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass