from setup import *
from read_ini_file import UPDATEINIFILE
from package_manager import package_manager
from get_user_de import get_user_de
from determine_next_backup import system_language
from device_location import device_location

mainIniFile = UPDATEINIFILE()

def save_info(chooseDevice):
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w', encoding='utf8') as configfile:
        # .deb
        if "deb" in package_manager():
            config.set('INFO', 'packageManager', f'{debFolderName}')
        
        # .rpm
        elif "rpm" in package_manager():
            config.set('INFO', 'packageManager', f'{rpmFolderName}')
        
        config.set('INFO', 'os',  f'{get_user_de()}')
        config.set('INFO', 'language',  f'{str(system_language())}')

        if device_location():
            config.set(f'EXTERNAL', 'hd', f'{media}/{userName}/{chooseDevice}')
        elif not device_location():
            config.set(f'EXTERNAL', 'hd', f'{run}/{userName}/{chooseDevice}')
        
        config.set('EXTERNAL', 'name', f'{chooseDevice}')
        config.write(configfile)
            
if __name__ == '__main__':
    pass