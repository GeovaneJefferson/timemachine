from setup import *
from read_ini_file import UPDATEINIFILE
from package_manager import package_manager
from get_users_de import get_user_de
from device_location import device_location


MAIN_INI_FILE = UPDATEINIFILE()

def save_info(device):
    # .deb
    if "deb" in package_manager():
        MAIN_INI_FILE.set_database_value('INFO', 'packageManager', f'{DEB_FOLDER_NAME}')
    # .rpm
    elif "rpm" in package_manager():
        MAIN_INI_FILE.set_database_value('INFO', 'packageManager', f'{RPM_FOLDER_NAME}')

    # Users OS
    MAIN_INI_FILE.set_database_value('INFO', 'os', f'{get_user_de()}')

    # Users OS language
    # config.set('INFO', 'language',  f'{str(system_language())}')

    # Device location
    if device_location():
        MAIN_INI_FILE.set_database_value('EXTERNAL', 'hd', f'{MEDIA}/{USERNAME}/{device}')

    elif not device_location():
        MAIN_INI_FILE.set_database_value('EXTERNAL', 'hd', f'{RUN}/{USERNAME}/{device}')

    # External name
    MAIN_INI_FILE.set_database_value('EXTERNAL', 'name', f'{device}')
            
            
if __name__ == '__main__':
    pass