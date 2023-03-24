from setup import *


def device_location():
    ################################################################################
    # Search external inside media
    ################################################################################
    try:
        print(f"Searching inside {media}")
        if len(os.listdir(f'{media}/{userName}')) != 0:
            print(f"Devices found inside {media}")
            return True

    except FileNotFoundError:
        try:
            print(f"Searching inside {run}")
            if len(os.listdir(f'{run}/{userName}')) != 0:
                print(f"Devices found inside {run}")
                return False
        
        except:
            return None
