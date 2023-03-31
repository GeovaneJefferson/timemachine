from setup import *

def users_icon_name():
    userCurrentGnomeIcon = os.popen(getUserIconCMD)
    userCurrentGnomeIcon = userCurrentGnomeIcon.read().strip()
    userCurrentGnomeIcon = userCurrentGnomeIcon.replace("'", "")

    return userCurrentGnomeIcon
