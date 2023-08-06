from setup import *
from read_ini_file import UPDATEINIFILE
from package_manager import package_manager
from get_users_de import get_user_de
from device_location import device_location

MAININIFILE=UPDATEINIFILE()

def save_info(chooseDevice):
    config=configparser.ConfigParser()
    config.read(SRC_USER_CONFIG)
    with open(SRC_USER_CONFIG, 'w', encoding='utf8') as configfile:
        # .deb
        if "deb" in package_manager():
            config.set('INFO', 'packageManager', f'{DEB_FOLDER_NAME}')

        # .rpm
        elif "rpm" in package_manager():
            config.set('INFO', 'packageManager', f'{RPM_FOLDER_NAME}')
        
        # Users OS
        config.set('INFO', 'os',  f'{get_user_de()}')
        # Users OS language
        # config.set('INFO', 'language',  f'{str(system_language())}')

        # Device location
        if device_location():
            config.set(f'EXTERNAL', 'hd', f'{MEDIA}/{USERNAME}/{chooseDevice}')

        elif not device_location():
            config.set(f'EXTERNAL', 'hd', f'{RUN}/{USERNAME}/{chooseDevice}')
        
        # External name
        config.set('EXTERNAL', 'name', f'{chooseDevice}')
        # Write to file
        config.write(configfile)
            
if __name__ == '__main__':
    pass