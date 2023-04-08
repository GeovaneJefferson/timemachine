from setup import *
from get_user_de import get_user_de

def users_icon_name():
    userIconName = os.popen(getUserIconCMD)
    userIconName = userIconName.read().strip()
    userIconName = userIconName.replace("'", "")

    return userIconName