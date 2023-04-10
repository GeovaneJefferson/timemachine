from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

somethingToRestoreInIcon = []

def restore_backup_icons():
    mainIniFile = UPDATEINIFILE()

    print("Restoring icon...")
    try:
        for icon in os.listdir(f"{mainIniFile.icon_main_folder()}/"):
            somethingToRestoreInIcon.append(icon)
       
        # # If has something to restore
        if somethingToRestoreInIcon:
            ################################################################################
            # Create .local/share/icons inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.local/share/icons"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/icons", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.icon_main_folder()}/ {homeUser}/.local/share/icons", shell=True)
            
            if get_user_de() != 'kde': 
                try:
                    os.listdir(f"/usr/share/icons/{mainIniFile.ini_info_icon()}/")
                    sub.run(f"{setUserIconCMD} {mainIniFile.ini_info_icon()}", shell=True)
                except:
                    try:
                        os.listdir(f"{homeUser}/.local/share/icons/{mainIniFile.ini_info_icon()}")
                        sub.run(f"{setUserIconCMD} {mainIniFile.ini_info_icon()}", shell=True)
                    except:
                        os.listdir(f"{homeUser}/.icons/{mainIniFile.ini_info_icon()}")
                        sub.run(f"{setUserIconCMD} {mainIniFile.ini_info_icon()}", shell=True)
    except:         
        pass