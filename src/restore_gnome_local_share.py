from setup import *
from read_ini_file import UPDATEINIFILE

async def restore_gnome_local_share():
    mainIniFile = UPDATEINIFILE()

    try:
        # Back up .local/share/gnome-shell
        sub.run(f"{copyRsyncCMD} {mainIniFile.kde_local_share_main_folder()}/ {homeUser}/.local/share/gnome-shell", shell=True)
    
    except:         
        pass

    return "Task completed: restore gnome local share"

if __name__ == '__main__':
    pass

