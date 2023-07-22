from setup import *


def package_manager():
    userPackageManager=os.popen(GET_USER_PACKAGE_MANAGER).read().strip().lower()
    
    # Distros
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