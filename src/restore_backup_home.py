from setup import *
from read_ini_file import UPDATEINIFILE
from get_backup_date import get_backup_date
from get_backup_time import get_latest_backup_time


async def restore_backup_home():
    mainIniFile = UPDATEINIFILE()

    print("Restoring Home folders...")
    for output in os.listdir(f"{mainIniFile.backup_folder_name()}/{get_backup_date()}/{get_latest_backup_time()}/"):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'current_backing_up', f"{output}")
            config.write(configfile)
        
        # If output folder do not exist, create it
        if not os.path.exists(f"{homeUser}/{output}/"):
            sub.run(f"{createCMDFolder} {homeUser}/{output}", shell=True)
        
        # Restore Home folders
        sub.run(f"{copyRsyncCMD} {mainIniFile.backup_folder_name()}/{get_backup_date()}/{get_latest_backup_time()}/"
            f"{output}/ {homeUser}/{output}/", shell=True)
    
    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass
