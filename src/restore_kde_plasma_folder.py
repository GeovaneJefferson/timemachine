from setup import *
from read_ini_file import UPDATEINIFILE

somethingToRestoreInKDEPlasmaFolder = []

async def restore_kde_plasma_folder():
    mainIniFile = UPDATEINIFILE()

    print("Restoring Kde Plasma folder...")

    try:
        for plasma in os.listdir(f"{mainIniFile.plasma_main_folder()}/"):
            somethingToRestoreInKDEPlasmaFolder.append(plasma)
       
        # If has something to KDEPlasmaFolder:
            ################################################################################
            # Create .config inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.local/share/plasma/"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/plasma", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.plasma_main_folder()}/ {homeUser}/.local/share/plasma/", shell=True)
    except:         
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass

