from setup import *
from read_ini_file import UPDATEINIFILE

async def restore_kde_share_config():
    mainIniFile = UPDATEINIFILE()

    try:
        sub.run(f"{copyRsyncCMD} {mainIniFile.kde_share_config_main_folder()}/ {homeUser}/.kde/share/", shell=True)
    except:         
        pass

    return "Task completed: restore kde share config"

if __name__ == '__main__':
    pass
