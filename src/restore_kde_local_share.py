from setup import *
from read_ini_file import UPDATEINIFILE

async def restore_kde_local_share():
    mainIniFile = UPDATEINIFILE()

    try:
        sub.run(f"{copyRsyncCMD} {mainIniFile.kde_local_share_main_folder()}/ {homeUser}/.local/share/", shell=True)
    except:         
        pass

    return "Task completed: restore kde local share"

if __name__ == '__main__':
    pass

