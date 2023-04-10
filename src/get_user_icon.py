from setup import *
from get_user_de import get_user_de
from get_kde_icon_name import get_kde_icon_name

def users_icon_name():
    if get_user_de() == 'kde':
        return get_kde_icon_name()

    else:
        userIconName = os.popen(getUserIconCMD)
        userIconName = userIconName.read().strip()
        userIconName = userIconName.replace("'", "")

    return userIconName