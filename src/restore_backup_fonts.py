from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de

MAIN_INI_FILE=UPDATEINIFILE()
something_to_restore_in_fonts = []

async def restore_backup_fonts():
    print("Restoring fonts...")
    for fonts in os.listdir(f"{MAIN_INI_FILE.fonts_main_folder()}/"):
        something_to_restore_in_fonts.append(fonts)
    
    # # If has something to restore
    if something_to_restore_in_fonts:
        ################################################################################
        # Create .local/share/icons inside home user
        ################################################################################
        if not os.path.exists(f"{HOME_USER}/.local/share/fonts"):
            sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/fonts", shell=True)   

        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.fonts_main_folder()}/ {HOME_USER}/.local/share/fonts", shell=True)
        
        if get_user_de() != 'kde': 
            try:
                os.listdir(f"/usr/share/fonts/{MAIN_INI_FILE.ini_info_font()}/")
                sub.run(f"{SET_USER_FONT_CMD} {MAIN_INI_FILE.ini_info_font()}", shell=True)
            except:
                os.listdir(f"{HOME_USER}/.local/share/fonts/{MAIN_INI_FILE.ini_info_font()}")
                sub.run(f"{SET_USER_FONT_CMD} {MAIN_INI_FILE.ini_info_font()}", shell=True)

    return "Task completed: Wallpaper"


if __name__ == '__main__':
    pass