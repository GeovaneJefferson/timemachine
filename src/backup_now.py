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
from backup_user_fonts import backup_user_fonts
from get_kde_gtk_cursor_name import users_kde_gtk_cursor_name
from get_kde_gtk_icon_name import get_kde_gtk_icon_name
from get_user_wallpaper import user_wallpaper
from backup_user_flatpak_applications_name import backup_flatpak_applications_name
from get_kde_font import FONT
from get_user_font import get_user_font
from add_backup_now_file import can_backup_now_file_be_found, remove_backup_now_file
from backup_kde_config import backup_kde_config
from backup_local_share import backup_local_share
from backup_kde_share_config import backup_kde_share_config
from update_notification_status import update_notification_status


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
        # try:
        #     config = configparser.ConfigParser()
        #     config.read(src_user_config)
        #     with open(src_user_config, 'w') as configfile:
        #         config.set('BACKUP', 'backup_now', "true")
        #         config.write(configfile)
                
        # except KeyError as error:
        #     print(error)
        #     exit()

        self.start_backup()

    def start_backup(self):
        update_notification_status("Backing up: Wallpaper...")
        backup_user_wallpaper()
        
        if str(mainIniFile.ini_allow_flatpak_names()) == "true":
            update_notification_status("Backing up: Flatpak Applications ...")
            backup_flatpak_applications_name()

        if str(mainIniFile.ini_multiple_time_mode()) == "true":
            try:
                sub.run(f"{createCMDFolder} {str(mainIniFile.time_folder_format())}", shell=True)  
            except FileNotFoundError as error:
                error_trying_to_backup(error)

        update_notification_status("Backing up: Home ...")
        backup_user_home()

        if str(mainIniFile.ini_allow_flatpak_data()) == "true":
            update_notification_status("Backing up: Flatpak Data ...")
            backup_user_flatpak_data()
      
        # For both Gnome and Kde
        update_notification_status("Backing up: Icon ...")
        backup_user_icons()
        update_notification_status("Backing up: Fonts ...")
        backup_user_fonts()
        update_notification_status("Backing up: Themes ...")
        backup_user_theme()
        
        # Only for Kde
        if get_user_de() == 'kde':
            update_notification_status("Backing up: .local/share ...")
            backup_local_share()
            update_notification_status("Backing up: .config ...")
            backup_kde_config()
            update_notification_status("Backing up: .kde/share/...")
            backup_kde_share_config()
            
        self.end_backup()

    def end_backup(self):
        print("Ending backup...")
        
        if can_backup_now_file_be_found():
            remove_backup_now_file()

        update_notification_status("")

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
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
                config.set('INFO', 'font', f'{mainFont.get_kde_font()}, {mainFont.get_kde_font_size()}')
                config.set('INFO', 'gtktheme', f'{users_theme_name()}')
                config.set('INFO', 'theme', f'None')
            else:
                config.set('INFO', 'icon', f'{users_icon_name()}')
                config.set('INFO', 'cursor', f'{users_cursor_name()}')
                config.set('INFO', 'font', f'{get_user_font()}')
                config.set('INFO', 'gtktheme', f'{users_theme_name()}')
                config.set('INFO', 'theme', f'None')
                config.set('INFO', 'colortheme', f'None')

            config.write(configfile)
        
        backup_ini_file(False)

        print("Backup is done!")
        print("Sleeping for 60 seconds...")
        time.sleep(60)  # Wait x, so if it finish fast, won't repeat the backup
        exit()


if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    mainFont = FONT()
    main = BACKUP()
