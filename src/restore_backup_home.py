from setup import *
from read_ini_file import UPDATEINIFILE
from get_backup_date import get_backup_date
from get_backup_time import get_latest_backup_time
from notification_massage import notification_message_current_backing_up
from handle_spaces import handle_spaces


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_backup_home():
    print("Restoring Home folders...")

    for folder in os.listdir(f"{MAIN_INI_FILE.backup_folder_name()}/{get_backup_date()[0]}/{get_latest_backup_time()[0]}/"):
        # Handle spaces
        folder = handle_spaces(folder)
    
        notification_message_current_backing_up(f'Restoring: {HOME_USER}/{folder}...')
    
        # If folder folder do not exist, create it
        if not os.path.exists(f"{HOME_USER}/{folder}/"):
            dst = HOME_USER + "/" + folder 
            sub.run(["mkdir", dst], stdout=sub.PIPE, stderr=sub.PIPE)
            
        # Restore Home folders
        # Restore the latest backup
        src = MAIN_INI_FILE.backup_folder_name() + "/" + get_backup_date()[0] + "/" + get_latest_backup_time()[0] + "/" + folder + "/"
        dst = HOME_USER + "/" + folder + "/"
        sub.run(['cp', '-rvf', src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
            

if __name__ == '__main__':
    pass
