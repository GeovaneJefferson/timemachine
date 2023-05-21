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
        pass