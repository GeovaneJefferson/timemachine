from setup import *
from get_backup_dates import *

config = configparser.ConfigParser()
config.read(src_user_config)
iniExternalLocation = config['EXTERNAL']['hd']

timeFolder = []
def get_backup_time():
    try:
        for output in os.listdir(f"{iniExternalLocation}/{baseFolderName}/"
                f"{backupFolderName}/{get_backup_date()[0]}/"):
            timeFolder.append(output)
            timeFolder.sort(reverse=True)
        return timeFolder

    except:
        print("Error trying to get backup times!")
        pass