from setup import *


def is_connected(iniHDName):
    # External availability

    try:
        # /media
        os.listdir(f"{MEDIA}/{USERNAME}/{iniHDName}")  
        return True

    except FileNotFoundError:
        # /run/media

        try:
            os.listdir(f"{RUN}/{USERNAME}/{iniHDName}") 
            return True

        except FileNotFoundError:
            pass
    
        return False


if __name__ == '__main__':
    pass