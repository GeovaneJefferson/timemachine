from setup import *
from read_ini_file import UPDATEINIFILE
from get_backup_date import get_backup_date
from get_backup_time import get_latest_backup_time
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_backup_home():
    print("Restoring Home folders...")

    for output in os.listdir(f"{MAIN_INI_FILE.backup_folder_name()}/{get_backup_date()[0]}/{get_latest_backup_time()[0]}/"):
        # If output folder do not exist, create it
        if not os.path.exists(f"{HOME_USER}/{output}/"):
            sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/{output}", shell=True)
        
        # Restore Home folders
        # Restore the latest backup
        sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.backup_folder_name()}/{get_backup_date()[0]}/{get_latest_backup_time()[0]}/"
            f"{output}/ {HOME_USER}/{output}/", shell=True)

        notification_message_current_backing_up(f'Restoring: {HOME_USER}/{output}...')
    
    return "Task completed: Wallpaper"


if __name__ == '__main__':
    pass
