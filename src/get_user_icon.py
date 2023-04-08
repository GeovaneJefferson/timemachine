from setup import *
from get_user_de import get_user_de

def users_icon_name():
    if get_user_de() == 'kde':
        config = configparser.ConfigParser()
        config.read(f"{homeUser}/.config/kdedefaults/kdeglobals")
        userIconName = config['Icons']['Theme']
        
    else:
        userIconName = os.popen(getUserIconCMD)
        userIconName = userIconName.read().strip()
        userIconName = userIconName.replace("'", "")

    return userIconName