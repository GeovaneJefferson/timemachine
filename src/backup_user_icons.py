from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_icon import users_icon_name

def backup_user_icons():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"/usr/share/icons/{users_icon_name()}")
        sub.run(f"{copyRsyncCMD} /usr/share/icons/ {str(mainIniFile.icon_main_folder())}",shell=True)
    except: 
        try:
            os.listdir(f"{homeUser}/icons/{users_icon_name()}")
            sub.run(f"{copyRsyncCMD} {homeUser}/.icons/ {str(mainIniFile.icon_main_folder())}",shell=True)
        except FileNotFoundError:
            sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/icons/ {str(mainIniFile.icon_main_folder())}",shell=True)
