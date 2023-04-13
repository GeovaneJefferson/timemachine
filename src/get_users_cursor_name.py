from setup import *
from get_user_de import get_user_de
from get_kde_gtk_cursor_name import users_kde_gtk_cursor_name

def users_cursor_name():
    if get_user_de() == 'kde':
        return users_kde_gtk_cursor_name()

    else:
        userCursorName = os.popen(getUserCursorCMD)
        userCursorName = userCursorName.read().strip()
        userCursorName = userCursorName.replace("'", "")

    return userCursorName
