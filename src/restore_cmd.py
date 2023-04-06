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

        self.begin_settings()

    def begin_settings(
        self,
        restoreHome,
        restoreApplicationsPackages,
        restoreFlatpaksPrograms,
        restoreFlatpaksData,
        restoreSystemSettings,
        reboot):

        # First change the wallpaper
        if restoreSystemSettings:
            restore_backup_wallpaper()
        
        if restoreHome:
            restore_backup_home()

        if restoreApplicationsPackages:
            restore_backup_package_applications()
       
        if restoreFlatpaksPrograms:
            restore_backup_flatpaks_applications()
        
        if restoreFlatpaksData:
            restore_backup_flatpaks_data()
        
        if restoreSystemSettings:
            restore_backup_icons()
            restore_backup_cursor()
            restore_backup_theme()

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
            config.write(configfile)

        ################################################################################
        # After backup is done
        ################################################################################
        print("Restoring is done!")

        if reboot:
            ###############################################################################
            # Update INI file
            ###############################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                # Set auto rebooting to false
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