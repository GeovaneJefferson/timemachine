from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

somethingToRestoreInCursor = []

def restore_backup_cursor():
    mainIniFile = UPDATEINIFILE()

    print("Restoring cursor...")
    try:
        # Check for cursor to be restored
        for cursor in os.listdir(f"{mainIniFile.cursor_main_folder()}/"):
            somethingToRestoreInCursor.append(cursor)

        if somethingToRestoreInCursor:
            sub.run(f"{copyRsyncCMD} {mainIniFile.cursor_main_folder()}/ {homeUser}.local/share/icons",shell=True)
            
            if get_user_de() != 'kde': 
                try:
                    os.listdir(f"/usr/share/icons/{mainIniFile.ini_info_cursor()}/")
                    sub.run(f"{setUserCursorCMD} {mainIniFile.ini_info_cursor()}",shell=True)
                except:
                    try:
                        sub.run(f"{setUserCursorCMD} {mainIniFile.ini_info_cursor()}",shell=True)
                    except:
                        pass
    except:
        pass