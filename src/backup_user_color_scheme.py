from setup import *
from read_ini_file import UPDATEINIFILE
from get_kde_color_scheme import get_kde_color_scheme
from delete_old_settings_settings import delete_old_settings


def backup_user_color_scheme():
    mainIniFile = UPDATEINIFILE()
    
    delete_old_settings("Color-Scheme")

    try:
        os.listdir(f"/usr/share/color-schemes/{get_kde_color_scheme()}")
        sub.run(f"{copyRsyncCMD} /usr/share/color-schemes/{get_kde_color_scheme()} {str(mainIniFile.icon_main_folder())}",shell=True)
    except: 
        sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/color-schemes/{get_kde_color_scheme()} {str(mainIniFile.icon_main_folder())}",shell=True)
    else:
        pass