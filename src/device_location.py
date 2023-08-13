from setup import *


def device_location():
    # Search external inside media
    try:
        if len(os.listdir(f'{MEDIA}/{USERNAME}')) != 0:
            print(f"Devices found inside {MEDIA}")
            return True
    except FileNotFoundError:
        try:
            if len(os.listdir(f'{RUN}/{USERNAME}')) != 0:
                print(f"Devices found inside {RUN}")
                return False
        except:
            return None


if __name__=='__main__':
    pass
