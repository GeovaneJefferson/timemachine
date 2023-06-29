from setup import *
from read_ini_file import UPDATEINIFILE

async def restore_kde_config():
    mainIniFile = UPDATEINIFILE()

    try:
        sub.run(f"{copyRsyncCMD} {mainIniFile.kde_config_main_folder()}/ {homeUser}/.config/", shell=True)
    except:         
        pass

    return "Task completed: restore kde config"

if __name__ == '__main__':
    pass
