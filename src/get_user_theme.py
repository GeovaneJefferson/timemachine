from setup import *

def users_theme_name():
    userCurrentTheme = os.popen(getUserThemeCMD)
    userCurrentTheme = userCurrentTheme.read().strip()
    userCurrentTheme = userCurrentTheme.replace("'", "")

    return userCurrentTheme
