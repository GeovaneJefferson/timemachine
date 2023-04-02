from setup import *

def users_cursor_name():
    userCursorName = os.popen(getUserCursorCMD)
    userCursorName = userCursorName.read().strip()
    userCursorName = userCursorName.replace("'", "")

    return userCursorName
