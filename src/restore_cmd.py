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


################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class RESTORE:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('RESTORE', 'is_restore_running', "true")
            config.write(configfile)

        # self.begin_settings()
        asyncio.run(self.begin_settings())

    async def begin_settings(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # isRunning = config['RESTORE']['is_restore_running']
        restoreHome = config['RESTORE']['files_and_folders']
        restoreApplicationsPackages = config['RESTORE']['applications_packages']
        restoreFlatpaksPrograms = config['RESTORE']['applications_flatpak_names']
        restoreFlatpaksData = config['RESTORE']['applications_data']
        restoreSystemSettings = config['RESTORE']['system_settings']
        reboot = config['INFO']['auto_reboot']

        # First change the wallpaper
        if restoreSystemSettings == 'true':
            await restore_backup_wallpaper()
        
        if restoreHome == 'true':
            await restore_backup_home()

        if restoreApplicationsPackages == 'true':
            await restore_backup_package_applications()
       
        if restoreFlatpaksPrograms == 'true':
            await restore_backup_flatpaks_applications()
        
        if restoreFlatpaksData == 'true':
            await restore_backup_flatpaks_data()
        
        if restoreSystemSettings == 'true':
            await restore_backup_cursor()
            await restore_backup_fonts()
            await restore_backup_icons()
            await restore_backup_theme()

            # Only for kde
            if get_user_de() == 'kde':
                await restore_kde_local_share()
                await restore_kde_config()
                await restore_kde_share_config()
                
                # Restart KDE session
                restart_kde_session()
        
        self.end_backup(reboot)

    def end_backup(self,reboot):
        print("Ending restoring...")
        ###############################################################################
        # Update INI file
        ###############################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'notification_id', "0")
            config.set('INFO', 'notification_add_info', "")
            config.set('INFO', 'feedback_status', "")

            config.set('RESTORE', 'is_restore_running', "false")
            config.set('RESTORE', 'files_and_folders', "false")
            config.set('RESTORE', 'applications_packages', "false")
            config.set('RESTORE', 'applications_flatpak_names', "false")
            config.set('RESTORE', 'applications_data', "false")
            config.set('RESTORE', 'system_settings', "false")
            config.set('RESTORE', 'is_restore_running', "false")

            config.write(configfile)

        ################################################################################
        # After backup is done
        ################################################################################
        print("Restoring is done!")

        if reboot == 'true':
            ###############################################################################
            # Update INI file
            ###############################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('RESTORE', 'is_restore_running', 'false')
                config.set('INFO', 'auto_reboot', 'false')
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