from setup import *


def is_connected(ini_hd_name):
    # External availability
    try:
        os.listdir(f"{ini_hd_name}")  
        return True
    # No conenctio to backup device
    except FileNotFoundError:
        return False


if __name__ == '__main__':
    pass