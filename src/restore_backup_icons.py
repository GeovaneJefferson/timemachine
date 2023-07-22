from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de

somethingToRestoreInIcon=[]

async def restore_backup_icons():
    MAININIFILE=UPDATEINIFILE()

    print("Restoring icon...")
    try:
        for icon in os.listdir(f"{MAININIFILE.icon_main_folder()}/"):
            somethingToRestoreInIcon.append(icon)
       
        # # If has something to restore
        if somethingToRestoreInIcon:
            ################################################################################
            # Create .local/share/icons inside home user
            ################################################################################
            if not os.path.exists(f"{HOME_USER}/.local/share/icons"):
                sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/icons", shell=True)   

            sub.run(f"{COPY_RSYNC_CMD} {MAININIFILE.icon_main_folder()}/ {HOME_USER}/.local/share/icons", shell=True)
            
            if get_user_de() != 'kde': 
                try:
                    os.listdir(f"/usr/share/icons/{MAININIFILE.ini_info_icon()}/")
                    sub.run(f"{SET_USER_ICON_CMD} {MAININIFILE.ini_info_icon()}", shell=True)
                except:
                    # try:
                    os.listdir(f"{HOME_USER}/.local/share/icons/{MAININIFILE.ini_info_icon()}")
                    sub.run(f"{SET_USER_ICON_CMD} {MAININIFILE.ini_info_icon()}", shell=True)
                    # except:
                    #     os.listdir(f"{homeUser}/.icons/{MAININIFILE.ini_info_icon()}")
                    #     sub.run(f"{setUserIconCMD} {MAININIFILE.ini_info_icon()}", shell=True)
    except:         
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass