from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de


MAIN_INI_FILE=UPDATEINIFILE()
something_to_restore_in_icon = []

async def restore_backup_icons():
    print("Restoring icon...")
    for icon in os.listdir(f"{MAIN_INI_FILE.icon_main_folder()}/"):
        something_to_restore_in_icon.append(icon)
    
    # # If has something to restore
    if something_to_restore_in_icon:
        ################################################################################
        # Create .local/share/icons inside home user
        ################################################################################
        if not os.path.exists(f"{HOME_USER}/.local/share/icons"):
            sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/icons", shell=True)   

        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.icon_main_folder()}/ {HOME_USER}/.local/share/icons", shell=True)
        
        if get_user_de() != 'kde': 
            try:
                os.listdir(f"/usr/share/icons/{MAIN_INI_FILE.ini_info_icon()}/")
                sub.run(f"{SET_USER_ICON_CMD} {MAIN_INI_FILE.ini_info_icon()}", shell=True)
            except:
                # try:
                os.listdir(f"{HOME_USER}/.local/share/icons/{MAIN_INI_FILE.ini_info_icon()}")
                sub.run(f"{SET_USER_ICON_CMD} {MAIN_INI_FILE.ini_info_icon()}", shell=True)
                # except:
                #     os.listdir(f"{homeUser}/.icons/{MAIN_INI_FILE.ini_info_icon()}")
                #     sub.run(f"{setUserIconCMD} {MAIN_INI_FILE.ini_info_icon()}", shell=True)

    return "Task completed: Wallpaper"


if __name__ == '__main__':
    pass