from setup import *


def get_user_de():
    userDE = os.popen(getUserDE).read().strip().lower()
    if ":" in userDE:
        return userDE.split(":")[1]
    else:
        return userDE        