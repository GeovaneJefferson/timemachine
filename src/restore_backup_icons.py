from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

somethingToRestoreInIcon = []

def restore_backup_icons():
    mainIniFile = UPDATEINIFILE()

    print("Restoring icon...")
    try:
        # Check for icon to be restored
        for icon in os.listdir(f"{mainIniFile.icon_main_folder()}/"):
            somethingToRestoreInIcon.append(icon)
        
        # # If has something to restore
        if somethingToRestoreInIcon:
            ################################################################################
            # Create .local/share/icons inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.local/share/icons"):
                sub.run(f"{createCMDFolder} {homeUser}.local/share/icons", shell=True)   

            # Copy icon from the backup to local/share/icons folder
            sub.run(f"{copyRsyncCMD} {mainIniFile.icon_main_folder()}/ {homeUser}.local/share/icons", shell=True)
            
            # Check if user DE is in the supported list
            for count in range(len(supportedOS)):
                if supportedOS[count] in str(get_user_de()):
                    print(f"Applying {setUserIconCMD} {icon}")

                    try:
                        os.listdir(f"/usr/share/icons/{icon}/")
                        sub.run(f"{setUserIconCMD} {icon}", shell=True)
                    except:
                        sub.run(f"{setUserIconCMD} {icon}", shell=True)
                    else:
                        pass
    except:
        pass
