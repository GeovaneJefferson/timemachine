#! /usr/bin/python3
from setup import *
from prepare_backup import *
from get_user_wallpaper import *
from update import backup_ini_file
from read_ini_file import UPDATEINIFILE
from get_user_icon import users_icon_name
from get_users_cursor_name import users_cursor_name
from get_user_theme import users_theme_name
from get_user_de import get_user_de
from backup_user_wallpaper import backup_user_wallpaper
from backup_user_home import backup_user_home
from backup_user_flatpak_data import backup_user_flatpak_data
from backup_user_icons import backup_user_icons
from backup_user_theme import backup_user_theme
from get_kde_gtk_cursor_name import users_kde_gtk_cursor_name
from get_kde_gtk_icon_name import get_kde_gtk_icon_name
from get_user_wallpaper import user_wallpaper
from backup_user_flatpak_applications_name import backup_flatpak_applications_name
from backup_kde_globals_file import backup_kde_globals_file
from backup_kde_kglobal_shortcuts_src import backup_kde_kglobal_shortcuts_src
from backup_kde_kwinrc import backup_kde_kwinrc


################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class BACKUP:
    def __init__(self):
        self.begin_settings()

    def begin_settings(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', "true")
                config.write(configfile)
                
        except KeyError as error:
            print(error)
            exit()

        self.start_backup()

    def start_backup(self):
        backup_user_wallpaper()
        
        if str(mainIniFile.ini_allow_flatpak_names()) == "true":
            backup_flatpak_applications_name()

        if str(mainIniFile.ini_multiple_time_mode()) == "true":
            try:
                sub.run(f"{createCMDFolder} {str(mainIniFile.time_folder_format())}", shell=True)  
            except FileNotFoundError as error:
                error_trying_to_backup(error)

        backup_user_home()

        if str(mainIniFile.ini_allow_flatpak_data()) == "true":
            backup_user_flatpak_data()
      
        # For both Gnome and Kde
        backup_user_icons()
        backup_user_theme()
        
        # Only for Kde
        if get_user_de() == 'kde':
            backup_kde_globals_file()
            backup_kde_kglobal_shortcuts_src()
            backup_kde_kwinrc()

        self.end_backup()

    def end_backup(self):
        print("Ending backup...")

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            # Change system tray color to white (Normal)
            config.set('INFO', 'notification_id', "0")
            config.set('INFO', 'notification_add_info', "")
            config.set('BACKUP', 'checker_running', "true")
            config.set('SCHEDULE', 'time_left', 'None')
            config.write(configfile)
        
        config = configparser.ConfigParser()
        config.read(f"{mainIniFile.restore_settings_location()}")
        with open(f"{mainIniFile.restore_settings_location()}", 'w') as configfile:
            if not config.has_section('INFO'):
                config.add_section('INFO')

            config.set('INFO', 'wallpaper', f'{user_wallpaper().split("/")[-1]}')
            if get_user_de() == 'kde':
                config.set('INFO', 'icon', f'{get_kde_gtk_icon_name()}')
                config.set('INFO', 'cursor', f'{users_kde_gtk_cursor_name()}')
                config.set('INFO', 'gtktheme', f'{users_theme_name()}')
                config.set('INFO', 'theme', f'None')
            else:
                config.set('INFO', 'icon', f'{users_icon_name()}')
                config.set('INFO', 'cursor', f'{users_cursor_name()}')
                config.set('INFO', 'gtktheme', f'{users_theme_name()}')
                config.set('INFO', 'theme', f'None')
                config.set('INFO', 'colortheme', f'None')

            config.write(configfile)
        
        # self.update_feedback_status("")
        backup_ini_file(False)

        print("Backup is done!")
        print("Sleeping for 60 seconds...")
        time.sleep(60)  # Wait x, so if it finish fast, won't repeat the backup
        exit()

    def update_feedback_status(self,output):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            # Save theme information
            if output == "":
                config.set('INFO', 'feedback_status', "")
            else:
                config.set('INFO', 'feedback_status', f"Backing up: {output}")
            config.write(configfile)

if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    main = BACKUP()
