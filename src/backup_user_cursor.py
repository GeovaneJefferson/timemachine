from setup import *
from read_ini_file import UPDATEINIFILE
from delete_old_settings_settings import delete_old_settings
from get_users_cursor_name import users_cursor_name

def backup_user_cursor():
    mainIniFile = UPDATEINIFILE()

    # delete_old_settings("Cursor")

    try:
        os.listdir(f"/usr/share/icons/{users_cursor_name()}")
        sub.run(f"{copyRsyncCMD} /usr/share/icons/{users_cursor_name()} {str(mainIniFile.icon_main_folder())}", shell=True)
    except: 
        try:
            os.listdir(f"{homeUser}/icons/{users_cursor_name()}")
            sub.run(f"{copyRsyncCMD} {homeUser}/.icons/ {str(mainIniFile.icon_main_folder())}", shell=True)
        except FileNotFoundError:
            sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/icons/ {str(mainIniFile.icon_main_folder())}", shell=True)
