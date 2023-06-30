#! /usr/bin/python3
from setup import *
from get_user_de import *
from read_ini_file import UPDATEINIFILE
from restore_backup_wallpaper import restore_backup_wallpaper
from restore_backup_home import restore_backup_home
from restore_backup_flatpaks_applications import restore_backup_flatpaks_applications
from restore_backup_package_applications import restore_backup_package_applications
from restore_backup_flatpaks_data import restore_backup_flatpaks_data
from restore_backup_icons import restore_backup_icons
from restore_backup_cursor import restore_backup_cursor
from restore_backup_theme import restore_backup_theme
from restart_kde_session import restart_kde_session
from restore_backup_fonts import restore_backup_fonts
from restore_kde_share_config import restore_kde_share_config
from restore_kde_config import restore_kde_config
from restore_kde_local_share import restore_kde_local_share
from restore_settings import restore_settings


################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class RESTORE:
    def __init__(self):
        self.auto_reboot = False

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('RESTORE', 'is_restore_running', "true")
            config.write(configfile)

        asyncio.run(self.start_restoring())

    async def start_restoring(self):
        # First change the wallpaper
        if restore_settings.restore_system_settings:
            await restore_backup_wallpaper()
        
        # Restore home folder
        if restore_settings.restore_home:
            await restore_backup_home()

        # Restore applications packages (.deb, .rpm etc.)
        if restore_settings.restore_applications_packages:
            await restore_backup_package_applications()
       
        # Restore flatpaks
        if restore_settings.restore_flatpaks_programs:
            await restore_backup_flatpaks_applications()
        
        # Restore flatpaks data
        if restore_settings.restore_flatpaks_data:
            await restore_backup_flatpaks_data()
        
        # Restore system settings
        if restore_settings.restore_system_settings:
            print("")
            # Restore cursor
            # await restore_backup_cursor()
            
            # # Restore font
            # await restore_backup_fonts()

            # # Restore icons
            # await restore_backup_icons()
            
            # # Restore theme
            # await restore_backup_theme()

            # Only for kde
            if get_user_de() == 'kde':
                # Restore kde local share
                await restore_kde_local_share()
                
                # Restore kde config
                await restore_kde_config()
                
                # Restore kde share config
                await restore_kde_share_config()
                
                # Restart KDE session
                restart_kde_session()
        
        self.end_restoring()

    def end_restoring(self):
        print("Ending restoring...")

        # Update INI file
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'notification_message', "0")
            config.set('INFO', 'notification_add_info', "")
            config.set('INFO', 'current_backing_up', "")

            config.set('RESTORE', 'is_restore_running', "false")
            config.set('RESTORE', 'files_and_folders', "false")
            config.set('RESTORE', 'applications_packages', "false")
            config.set('RESTORE', 'applications_flatpak_names', "false")
            config.set('RESTORE', 'applications_data', "false")
            config.set('RESTORE', 'system_settings', "false")
            config.set('RESTORE', 'is_restore_running', "false")

            config.write(configfile)

        # After backup is done
        print("Restoring is done!")

        if self.auto_reboot:
            # Update INI file
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('RESTORE', 'is_restore_running', 'false')
                config.write(configfile)

            sub.run("sudo reboot", shell=True)

        else:
            print("Closing window...")
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('RESTORE', 'is_restore_running', 'false')
                config.write(configfile)

            exit()

if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    main = RESTORE()