from setup import *


def package_manager():
    user_package_manager = os.popen(GET_USER_PACKAGE_MANAGER).read().strip().lower()
    
    # Distros
    if "ubuntu" in user_package_manager:
        return "deb"
    elif "debian" in user_package_manager:
        return "deb"
    elif "fedora" in user_package_manager:
        return "rpm"
    elif "opensuse" in user_package_manager:
        return "rpm"
    elif "arch" in user_package_manager:
        return "pacman"
    else:
        return "None"