from setup import *
from read_ini_file import UPDATEINIFILE
from get_backup_date import get_backup_date
from get_backup_time import get_latest_backup_time
from notification_massage import notification_message_current_backing_up
from handle_spaces import handle_spaces


MAIN_INI_FILE = UPDATEINIFILE()


async def restore_backup_home():
    print("Restoring Home folders...")

    # location = (f'{MAIN_INI_FILE.backup_folder_name()}/'\
    #             f'{get_backup_date()[0]}/'\
    #             f'{get_latest_backup_time()[0]}/')
    
    location = MAIN_INI_FILE.main_backup_folder()

    for folder in os.listdir(location):
        # EXclude hidden files/folder
        if not folder.startswith('.'):
            # Handle spaces
            folder = handle_spaces(folder)
         
            print('Restoring:', folder)

            notification_message_current_backing_up(
                f'Restoring: {HOME_USER}/{folder}...')
        
            # If folder folder do not exist, create it
            if not os.path.exists(f"{HOME_USER}/{folder}"):
                dst = HOME_USER + "/" + folder 
                
                sub.run(
                    ["mkdir", dst],
                    stdout=sub.PIPE,
                    stderr=sub.PIPE).wait()
                
            # Restore Home folders
            # Restore the latest backup
            # src = MAIN_INI_FILE.backup_folder_name() + "/" + get_backup_date()[0] + "/" + get_latest_backup_time()[0] + "/" + folder + "/"
            
            # Source from main backup folder
            src = location + '/' + folder + '/'
            dst = HOME_USER + '/' + folder + '/'

            print(src)
            print(dst)
            print()

            # Copy everything from src to dst folder
            for i in os.listdir(src):
                x = src + i
                
                sub.run(
                    ['cp', '-rvf', x, dst],
                    stdout=sub.PIPE,
                    stderr=sub.PIPE,
                    text=True)


if __name__ == '__main__':  
    pass