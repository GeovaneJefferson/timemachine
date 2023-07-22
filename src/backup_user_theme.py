from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_theme import users_theme_name

def backup_user_theme():
    MAININIFILE=UPDATEINIFILE()

    ################################################################################
    # Create gnome-shell inside theme current theme folder
    ################################################################################
    if not os.path.exists(f"{str(MAININIFILE.ini_external_location())}/{BASE_FOLDER_NAME}/"
        f"{GTK_THEME_FOLDER_NAME}/{users_theme_name()}/{GNOME_SHELL_FOLDER_NAME}"):
        try:
            sub.run(f"{CREATE_CMD_FOLDER} {str(MAININIFILE.ini_external_location())}/{BASE_FOLDER_NAME}/"
                f"{GTK_THEME_FOLDER_NAME}/{users_theme_name()}/{GNOME_SHELL_FOLDER_NAME}",shell=True)
        except Exception as error:
            print("Error" + error)
            pass

    try:
        os.listdir(f"/usr/share/themes/{users_theme_name()}/")
        sub.run(f"{COPY_RSYNC_CMD} /usr/share/themes/ {str(MAININIFILE.gtk_theme_main_folder())}",shell=True)
    except:
        try:
            os.listdir(f"{HOME_USER}/.themes/{users_theme_name()}")
            sub.run(f"{COPY_RSYNC_CMD} {HOME_USER}/.themes/ {str(MAININIFILE.gtk_theme_main_folder())}",shell=True)
        except:
            sub.run(f"{COPY_RSYNC_CMD} {HOME_USER}/.local/share/themes/ {str(MAININIFILE.gtk_theme_main_folder())}",shell=True)

    ################################################################################
    # Get gnome-shell with the current theme name
    ################################################################################
    try:
        if os.listdir(f"/usr/share/gnome-shell/theme/{users_theme_name()}/"):
            sub.run(f"{COPY_RSYNC_CMD} /usr/share/gnome-shell/theme/{users_theme_name()}/ "
                f"{str(MAININIFILE.ini_external_location())}/{BASE_FOLDER_NAME}/"
                f"{GTK_THEME_FOLDER_NAME}/{users_theme_name()}/{GNOME_SHELL_FOLDER_NAME}",shell=True)
    except:
        pass

if __name__ == '__main__':
    pass