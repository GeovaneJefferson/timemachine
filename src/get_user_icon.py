from setup import *

def users_icon_name():
    userIconName = os.popen(getUserIconCMD)
    userIconName = userIconName.read().strip()
    userIconName = userIconName.replace("'", "")

    return userIconName
