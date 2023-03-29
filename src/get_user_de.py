from setup import *


def get_user_de():
    userDE = os.popen(getUserDE).read().strip().lower()
    return userDE        