from setup import *

def users_cursor_name():
    userCurrentcursor = os.popen(getUserCursorCMD)
    userCurrentcursor = userCurrentcursor.read().strip()
    userCurrentcursor = userCurrentcursor.replace("'", "")

    return userCurrentcursor
