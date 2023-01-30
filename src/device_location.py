from setup import *


def device_location():
    ################################################################################
    # Search external inside media
    ################################################################################
    print("Searching for backup devices inside media...")
    try:
        if len(os.listdir(f'{media}/{userName}')) != 0:
            return True

    except FileNotFoundError:
        print("Searching for backup devices inside run...")
        try:
            if len(os.listdir(f'{run}/{userName}')) != 0:
                return False
        
        except:
            return None
