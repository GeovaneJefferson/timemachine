from setup import *
from get_users_de import get_user_de
from read_ini_file import UPDATEINIFILE
from restore_backup_wallpaper import restore_backup_wallpaper
from restore_backup_home import restore_backup_home
from restore_backup_flatpaks_applications import restore_backup_flatpaks_applications
from restore_backup_package_applications import restore_backup_package_applications
from restore_backup_flatpaks_data import restore_backup_flatpaks_data
# from restart_kde_session import restart_kde_session
from restore_kde_share_config import restore_kde_share_config
from restore_kde_config import restore_kde_config
from restore_kde_local_share import restore_kde_local_share
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

is_a_test = False


# Define a function to convert the date string to a datetime object
def convert_to_datetime(date_str):
    return datetime.strptime(date_str, '%y-%m-%d')


class RESTORE:
    def __init__(self):
        # Update DB
        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'True')

        # Length of item to restore
        self.item_to_restore = 0 

        #  Get length of the restore list
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_packages'):
            self.item_to_restore += 1
        
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_names'):
            self.item_to_restore += 1
        
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_data'):
            self.item_to_restore += 1
        
        if MAIN_INI_FILE.get_database_value('RESTORE', 'files_and_folders'):
            self.item_to_restore += 1
        
        if MAIN_INI_FILE.get_database_value('RESTORE', 'system_settings'):
            self.item_to_restore += 1

        if not is_a_test:
            # Only one item inside restore list
            if self.item_to_restore == 1:
                # Show 99%
                self.progress_increment = 99 / self.item_to_restore

            else:
                self.progress_increment = 100 / self.item_to_restore

        # Start restoring
        asyncio.run(self.start_restoring())
        
    async def start_restoring(self):
        # First change the wallpaper
        if MAIN_INI_FILE.get_database_value('RESTORE', 'system_settings'):
            self.update_progressbar_db()
            print('Restoring wallpaper...')
            await restore_backup_wallpaper()
        
        # Restore home folder
        if MAIN_INI_FILE.get_database_value('RESTORE', 'files_and_folders'):
            self.update_progressbar_db()
            print('Restoring HOME...')
            await restore_backup_home()

        # Restore applications packages
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_packages'):
            self.update_progressbar_db()
            print('Restoring Applications Packages...')
            await restore_backup_package_applications()
       
        # Restore flatpaks
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_names'):
            self.update_progressbar_db()
            print('Restoring Flatpak Applications...')
            await restore_backup_flatpaks_applications()
        
        # Restore flatpaks data
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_data'):
            self.update_progressbar_db()
            print('Restoring Flatpak Data...')
            await restore_backup_flatpaks_data()
        
        # # Restore system settings
        if MAIN_INI_FILE.get_database_value('RESTORE', 'system_settings'):
            # Only for kde
            if get_user_de() == 'kde':
                self.update_progressbar_db()
                print('Restoring KDE .local/share...')
                await restore_kde_local_share()

                self.update_progressbar_db()
                print('Restoring KDE .config...')
                await restore_kde_config()

                self.update_progressbar_db()
                print('Restoring KDE .share/config...')
                await restore_kde_share_config()
                
                # # Restart KDE session
                # sub.run(
                #     ['kquitapp5', 'plasmashell'],
                #     stdout=sub.PIPE,
                #     stderr=sub.PIPE)
            
                # sub.run(
                #     ['kstart5', 'plasmashell'],
                #     stdout=sub.PIPE,
                #     stderr=sub.PIPE)
        
        # Restore updates file to HOME
        asyncio.run(self.restore_backup_home_updates())
        # self.restore_backup_home_updates()
            
    # For updated HOME files
    # async def restore_backup_home_updates(self):
    def restore_backup_home_updates(self):
        date_list = []
        added_list = []
        dst_loc = MAIN_INI_FILE.backup_dates_location()

        # Add all dates to the list
        for date in os.listdir(dst_loc):
            # Eclude hidden files/folders
            if not date.startswith('.'):
                date_list.append(date)

        # Sort the dates in descending order using the converted datetime objects
        sorted_date = sorted(date_list,
                    key=convert_to_datetime,
                    reverse=True)

        # Loop through each date folder
        for i in range(len(sorted_date)):
            # Get date path
            date_path = f'{dst_loc}/{sorted_date[i]}'
        
            # Get latest file update and add to the 'Added list' 
            for root, _, files in os.walk(date_path):
                if files:
                    for i in range(len(files)):
                        if files[i] not in added_list:
                            destination_location = root.replace(date_path, '')
                            destination_location =  os.path.join(
                                    HOME_USER, '/'.join(
                                    destination_location.split(
                                    '/')[2:])) 
                            
                            source = os.path.join(root, files[i])
                            # print('Restoring:', files[i])
                            # print('Source:', source)
                            # print('Destination:', os.path.join(destination_location, files[i]))

                            # Restore lastest file update
                            print(f'Restoring {source} to: {destination_location}')
                            
                            # Log
                            # with open('', 'a') as file:
                            #     file.write(f'Restoring {source} to: {destination_location}\n')
                            #     file.write('\n')

                            # shutil.copy(
                            #     source,
                            #     destination_location)

                            # Add to 'Added list'
                            added_list.append(files[i])

        self.end_restoring()

    def end_restoring(self):
        print("Restoring is done!")

        # Update DB
        MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_data', 'False')
        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'restore_progress_bar', '0')
        
        notification_message_current_backing_up('')
        
        exit()

    def update_progressbar_db(self):
        if not is_a_test:
            new_value = self.progress_increment + \
                int(MAIN_INI_FILE.get_database_value(
                    'RESTORE', 'restore_progress_bar').split('.')[0])
            
            MAIN_INI_FILE.set_database_value(
                'RESTORE', 'restore_progress_bar', f'{str(new_value)}')


if __name__ == '__main__':
    MAIN = RESTORE()