from setup import *


def get_package_manager():
    ################################################################################
    # Get user's packagemanager
    ################################################################################
    userPackageManager = os.popen(getUserPackageManager).read().strip().lower()
    return userPackageManager