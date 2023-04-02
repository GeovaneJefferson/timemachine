from setup import *

def users_cursor_name():
    getUserCursorCMD = os.popen(getUserCursorCMD)
    getUserCursorCMD = getUserCursorCMD.read().strip()
    getUserCursorCMD = getUserCursorCMD.replace("'", "")

    return getUserCursorCMD
