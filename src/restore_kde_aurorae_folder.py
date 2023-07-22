from setup import *
from read_ini_file import UPDATEINIFILE

somethingToRestoreInKDEAurorae=[]

async def restore_kde_aurorae_folder():
    MAININIFILE=UPDATEINIFILE()

    print("Restoring Kde Aurorae folder...")

    try:
        for aurorae in os.listdir(f"{MAININIFILE.aurorae_main_folder()}/"):
            somethingToRestoreInKDEAurorae.append(aurorae)
       
        # If has something to KDEAurorae:
            if not os.path.exists(f"{HOME_USER}/.local/share/aurorae/"):
                sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/aurorae", shell=True)   

            sub.run(f"{COPY_RSYNC_CMD} {MAININIFILE.plasma_main_folder()}/ {HOME_USER}/.local/share/aurorae/", shell=True)
    except:         
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass