from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de


MAIN_INI_FILE = UPDATEINIFILE()
something_to_restore_in_cursor=[]

async def restore_backup_cursor():

    print("Restoring cursor...")
    # Check for cursor to be restored
    for cursor in os.listdir(f"{MAIN_INI_FILE.cursor_main_folder()}/"):
        something_to_restore_in_cursor.append(cursor)

    if something_to_restore_in_cursor:
        if get_user_de() != 'kde': 
            try:
                os.listdir(f"/usr/share/icons/{MAIN_INI_FILE.ini_info_cursor()}")
                sub.run(f"{SET_USER_CURSOR_CMD} {MAIN_INI_FILE.ini_info_cursor()}",shell=True)
            except:
                try:
                    os.listdir(f"{HOME_USER}/.local/share/icons/{MAIN_INI_FILE.ini_info_cursor()}")
                    sub.run(f"{SET_USER_CURSOR_CMD} {MAIN_INI_FILE.ini_info_cursor()}",shell=True)
                except:
                    os.listdir(f"{HOME_USER}/.icons/{MAIN_INI_FILE.ini_info_cursor()}")
                    sub.run(f"{SET_USER_CURSOR_CMD} {MAIN_INI_FILE.ini_info_cursor()}",shell=True)

    return "Task completed: Wallpaper"


if __name__ == '__main__':
    pass
