#! /usr/bin/python3
from setup import *
from prepare_backup import *
from get_user_wallpaper import *
from update import backup_ini_file
from read_ini_file import UPDATEINIFILE
from get_user_icon import users_icon_name
from users_cursor_name import users_cursor_name
from get_user_theme import users_theme_name
from get_user_de import get_user_de
from delete_old_settings_settings import delete_old_settings
from backup_user_wallpaper import backup_user_wallpaper
from backup_user_home import backup_user_home
from backup_user_flatpak_data import backup_user_flatpak_data
from backup_user_icons import backup_user_icons
from backup_user_cursor import backup_user_cursor
from backup_user_theme import backup_user_theme
from backup_user_color_scheme import backup_user_color_scheme
from backup_user_flatpak_applications_name import backup_flatpak_applications_name


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

        # First backup user wallpaper
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
      
        backup_user_icons()
        
        backup_user_cursor()

        backup_user_theme()

        if get_user_de() == 'kde':
            backup_user_color_scheme()

        self.end_backup()

    def end_backup(self):
        print("Ending backup...")

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            # try:
            #     # Update last backup time
            #     config.set('INFO', 'latest', f'{latest_time_info()}')
            # except:
            #     pass
            # Change system tray color to white (Normal)
            config.set('INFO', 'notification_id', "0")
            # Reset Main Window information
            config.set('INFO', 'notification_add_info', "")
            config.set('BACKUP', 'checker_running', "true")
            config.set('SCHEDULE', 'time_left', 'None')
            config.write(configfile)
        
        self.update_feedback_status("")
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
