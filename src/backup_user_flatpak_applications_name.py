from setup import *
from read_ini_file import UPDATEINIFILE


def backup_flatpak_applications_name():
    mainIniFile = UPDATEINIFILE()
    
    try:
        count = 0
        dummyList = []

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(str(mainIniFile.flatpak_txt_location()), 'w') as configfile:  
            for output in os.popen(getFlatpaks):
                dummyList.append(output)
                # Write USER installed flatpak to flatpak.txt inside external device
                configfile.write(dummyList[count])
                count += 1

    except OSError as error:
        print(error)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            # Change system tray color to red (Error)
            config.set('INFO', 'notification_id', "2")
            # Reset Main Window information
            config.set('INFO', 'notification_add_info', f"Read-only, {error}")
