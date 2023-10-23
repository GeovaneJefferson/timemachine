from setup import *


def device_location():
    # Search external inside media
    try:
        if len(os.listdir(f'{MEDIA}/{USERNAME}')) != 0:
            return True
        
    except FileNotFoundError:
        try:
            if len(os.listdir(f'{RUN}/{USERNAME}')) != 0:
                return False
            
        except:
            print(f"No devices found.")
            return None


if __name__=='__main__':
    pass
