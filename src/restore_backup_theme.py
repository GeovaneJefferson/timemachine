from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de

MAIN_INI_FILE=UPDATEINIFILE()
something_to_restore_in_theme = []

async def restore_backup_theme():
    print("Restoring theme...")
    # Check for theme to be restored
    for theme in os.listdir(f"{MAIN_INI_FILE.gtk_theme_main_folder()}/"):
        something_to_restore_in_theme.append(theme)

    # If has something to restore
    if something_to_restore_in_theme:
        ################################################################################
        # Create .themes inside home user
        ################################################################################
        if not os.path.exists(f"{HOME_USER}/.local/share/themes"):
            sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/themes", shell=True)   

        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.gtk_theme_main_folder()}/ {HOME_USER}/.local/share/themes", shell=True)

        if get_user_de() != 'kde': 
            try:
                os.listdir(f"/usr/share/themes/{MAIN_INI_FILE.ini_info_gtktheme()}")
                sub.run(f"{SET_USER_THEME_CMD} {MAIN_INI_FILE.ini_info_gtktheme()}", shell=True)
            except:
                # try:
                os.listdir(f"{HOME_USER}/.local/share/themes/{MAIN_INI_FILE.ini_info_gtktheme()}")
                sub.run(f"{SET_USER_THEME_CMD} {MAIN_INI_FILE.ini_info_gtktheme()}", shell=True)
                # except:
                #     os.listdir(f"{homeUser}/.themes/{MAIN_INI_FILE.ini_info_gtktheme()}")
                #     sub.run(f"{setUserThemeCMD} {MAIN_INI_FILE.ini_info_gtktheme()}", shell=True)

    return "Task completed: Wallpaper"


if __name__ == '__main__':
    pass