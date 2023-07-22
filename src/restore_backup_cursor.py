from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de

somethingToRestoreInCursor=[]

async def restore_backup_cursor():
    MAININIFILE=UPDATEINIFILE()

    print("Restoring cursor...")
    try:
        # Check for cursor to be restored
        for cursor in os.listdir(f"{MAININIFILE.cursor_main_folder()}/"):
            somethingToRestoreInCursor.append(cursor)

        if somethingToRestoreInCursor:
            if get_user_de() != 'kde': 
                try:
                    os.listdir(f"/usr/share/icons/{MAININIFILE.ini_info_cursor()}")
                    sub.run(f"{SET_USER_CURSOR_CMD} {MAININIFILE.ini_info_cursor()}",shell=True)
                except:
                    try:
                        os.listdir(f"{HOME_USER}/.local/share/icons/{MAININIFILE.ini_info_cursor()}")
                        sub.run(f"{SET_USER_CURSOR_CMD} {MAININIFILE.ini_info_cursor()}",shell=True)
                    except:
                        os.listdir(f"{HOME_USER}/.icons/{MAININIFILE.ini_info_cursor()}")
                        sub.run(f"{SET_USER_CURSOR_CMD} {MAININIFILE.ini_info_cursor()}",shell=True)
    except:
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass
