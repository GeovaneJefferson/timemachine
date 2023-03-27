from setup import *


def get_package_manager():
    userPackageManager = os.popen(getUserPackageManager).read().strip().lower()
    if "ubuntu" in userPackageManager:
        return "deb"
    elif "debian" in userPackageManager:
        return "deb"
    elif "fedora" in userPackageManager:
        return "rpm"
    elif "opensuse" in userPackageManager:
        return "rpm"
    elif "arch" in userPackageManager:
        return "pacman"
    else:
        return "None"
    