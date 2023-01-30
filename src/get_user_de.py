from setup import *


def get_user_de():
    ################################################################################
    # Get users DE
    ################################################################################
    userDE = os.popen(getUserDE).read().strip().lower()
    return userDE        