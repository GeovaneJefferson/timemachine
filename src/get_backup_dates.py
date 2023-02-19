from setup import *
config = configparser.ConfigParser()
config.read(src_user_config)
iniExternalLocation = config['EXTERNAL']['hd']

dateFolders = []
def get_backup_date():
    try:
        for output in os.listdir(f"{iniExternalLocation}/"
                f"{baseFolderName}/{backupFolderName}"):
            # Hide hidden outputs
            if "." not in output:
                dateFolders.append(output)
                dateFolders.sort(
                    reverse=True, 
                    key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        return dateFolders

    except:
        print("Error trying to get backup dates!")
        pass
