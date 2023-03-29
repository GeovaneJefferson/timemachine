from setup import *


def device_location():
    ################################################################################
    # Search external inside media
    ################################################################################
    try:
        if len(os.listdir(f'{media}/{userName}')) != 0:
            print(f"Devices found inside {media}")
            return True

    except FileNotFoundError:
        try:
            if len(os.listdir(f'{run}/{userName}')) != 0:
                print(f"Devices found inside {run}")
                return False
        
        except:
            return None
