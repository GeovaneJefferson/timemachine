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


################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)

MAIN_INI_FILE = UPDATEINIFILE()

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
            await restore_backup_wallpaper()
        
        # Restore home folder
        if MAIN_INI_FILE.get_database_value('RESTORE', 'files_and_folders'):
            self.update_progressbar_db()
            await restore_backup_home()

        # Restore applications packages
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_packages'):
            self.update_progressbar_db()
            await restore_backup_package_applications()
       
        # Restore flatpaks
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_names'):
            self.update_progressbar_db()
            await restore_backup_flatpaks_applications()
        
        # Restore flatpaks data
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_data'):
            self.update_progressbar_db()
            await restore_backup_flatpaks_data()
        
        # # Restore system settings
        if MAIN_INI_FILE.get_database_value('RESTORE', 'system_settings'):
            # Only for kde
            if get_user_de() == 'kde':
                self.update_progressbar_db()
                await restore_kde_local_share()

                self.update_progressbar_db()
                await restore_kde_config()

                self.update_progressbar_db()
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
        new_value = self.progress_increment + \
            int(MAIN_INI_FILE.get_database_value(
                'RESTORE', 'restore_progress_bar').split('.')[0])
        MAIN_INI_FILE.set_database_value(
            'RESTORE', 'restore_progress_bar', f'{str(new_value)}')


if __name__ == '__main__':
    main = RESTORE()
