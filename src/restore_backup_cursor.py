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
            print(cursor)

        # If has something to restore
        if somethingToRestoreInCursor:
            sub.run(f"{copyRsyncCMD} {mainIniFile.cursor_main_folder()}/ {homeUser}.local/share/icons", shell=True)

            # Check if user DE is in the supported list
            for count in range(len(supportedOS)):
                print(count)
                if supportedOS[count] in str(get_user_de()):
                    try:
                        # USR/SHARE
                        os.listdir(f"/usr/share/icons/{cursor}/")
                        sub.run(f"{setUserCursorCMD} {cursor}", shell=True)
                    except:
                        try:
                            # .cursor
                            sub.run(f"{setUserCursorCMD} {cursor}", shell=True)
                        except:
                            pass
    except:
        pass