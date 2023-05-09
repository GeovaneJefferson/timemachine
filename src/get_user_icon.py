from setup import *
from get_user_de import get_user_de
from get_kde_gtk_icon_name import get_kde_gtk_icon_name

def users_icon_name():
    if get_user_de() == 'kde':
        return get_kde_gtk_icon_name()

    else:
        userIconName = os.popen(getUserIconCMD)
        userIconName = userIconName.read().strip()
        userIconName = userIconName.replace("'", "")

    return userIconName 

def users_icon_size():
    try:
        userIconSize = os.popen(f"du -s {homeUser}/.icons/{users_icon_name()}")
        userIconSize = userIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.icons/{users_icon_name()}", "").replace("\t", "")
        userIconSize = int(userIconSize)
    except ValueError:
        try:
            userIconSize = os.popen(f"du -s {homeUser}/.local/share/icons/{users_icon_name()}")
            userIconSize = userIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.local/share/icons/{users_icon_name()}", "").replace("\t", "")
            userIconSize = int(userIconSize)
        except ValueError:
            try:
                userIconSize = os.popen(f"du -s /usr/share/icons/{users_icon_name()}")
                userIconSize = userIconSize.read().strip("\t").strip("\n").replace(f"/usr/share/icons/{users_icon_name()}", "").replace("\t", "")
                userIconSize = int(userIconSize)
            except ValueError:
                return None

    return userIconSize 

if __name__ == '__main__':
    pass