from setup import *


def is_connected(ini_hd_name):
    # External availability
    try:
        os.listdir(ini_hd_name)  
        return True
    
    # No connection to backup device
    except FileNotFoundError:
        return False


if __name__ == '__main__':
    pass