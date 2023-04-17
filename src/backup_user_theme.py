from setup import *
from read_ini_file import UPDATEINIFILE
from delete_old_settings_settings import delete_old_settings
from get_user_theme import users_theme_name

def backup_user_theme():
    mainIniFile = UPDATEINIFILE()

    # delete_old_settings("Theme")

    ################################################################################
    # Create gnome-shell inside theme current theme folder
    ################################################################################
    if not os.path.exists(f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/"
        f"{gtkThemeFolderName}/{users_theme_name()}/{gnomeShellFolder}"):
        try:
            sub.run(f"{createCMDFolder} {str(mainIniFile.ini_external_location())}/{baseFolderName}/"
                f"{gtkThemeFolderName}/{users_theme_name()}/{gnomeShellFolder}",shell=True)
        except Exception as error:
            print("Error" + error)
            pass

    try:
        os.listdir(f"/usr/share/themes/{users_theme_name()}/")
        sub.run(f"{copyRsyncCMD} /usr/share/themes/ {str(mainIniFile.gtk_theme_main_folder())}",shell=True)
    except:
        try:
            os.listdir(f"{homeUser}/.themes/{users_theme_name()}")
            sub.run(f"{copyRsyncCMD} {homeUser}/.themes/ {str(mainIniFile.gtk_theme_main_folder())}",shell=True)
        except:
            sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/themes/ {str(mainIniFile.gtk_theme_main_folder())}",shell=True)

    ################################################################################
    # Get gnome-shell with the current theme name
    ################################################################################
    try:
        if os.listdir(f"/usr/share/gnome-shell/theme/{users_theme_name()}/"):
            sub.run(f"{copyRsyncCMD} /usr/share/gnome-shell/theme/{users_theme_name()}/ "
                f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/"
                f"{gtkThemeFolderName}/{users_theme_name()}/{gnomeShellFolder}",shell=True)
    except:
        pass

if __name__ == '__main__':
    pass