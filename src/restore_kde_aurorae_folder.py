from setup import *
from read_ini_file import UPDATEINIFILE

somethingToRestoreInKDEAurorae = []

async def restore_kde_aurorae_folder():
    mainIniFile = UPDATEINIFILE()

    print("Restoring Kde Aurorae folder...")

    try:
        for aurorae in os.listdir(f"{mainIniFile.aurorae_main_folder()}/"):
            somethingToRestoreInKDEAurorae.append(aurorae)
       
        # If has something to KDEAurorae:
            if not os.path.exists(f"{homeUser}/.local/share/aurorae/"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/aurorae", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.plasma_main_folder()}/ {homeUser}/.local/share/aurorae/", shell=True)
    except:         
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass