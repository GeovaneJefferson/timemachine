from setup import *


def device_location():
    ################################################################################
    # Search external inside media
    ################################################################################
    try:
        print(f"Searching inside {media}")
        if len(os.listdir(f'{media}/{userName}')) != 0:
            print(f"Devices found inside {media}")
            return f"{media}"

    except FileNotFoundError:
        try:
            print(f"Searching inside {run}")
            if len(os.listdir(f'{run}/{userName}')) != 0:
                print(f"Devices found inside {run}")
                return f"{run}"
        
        except:
            return None
