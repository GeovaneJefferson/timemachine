#! /usr/bin/python3
from setup import *
from prepare_backup import *
from get_user_wallpaper import *
from update import backup_ini_file
from read_ini_file import UPDATEINIFILE
from get_user_icon import users_icon_name
from get_user_cursor import users_cursor_name
from get_theme_cursor import users_theme_name
from delete_old_settings_settings import delete_old_settings_settings

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

        self.backup_user_wallpaper()

    def backup_user_wallpaper(self):
        # Replace wallpaper inside the folder, only allow 1
        if os.listdir(f"{str(mainIniFile.wallpaper_main_folder())}"):
            # Delete all image inside wallpaper folder
            for image in os.listdir(f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}/"):
                print(f"Deleting {str(mainIniFile.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}/{image}...")
                sub.run(f"rm -rf {str(mainIniFile.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}/{image}", shell=True)
        
        print(f"{copyCPCMD} {user_wallpaper()} {str(mainIniFile.wallpaper_main_folder())}/")
        sub.run(f"{copyCPCMD} {user_wallpaper()} {str(mainIniFile.wallpaper_main_folder())}/", shell=True) 
       
        if str(mainIniFile.ini_allow_flatpak_names()) == "true":
            self.write_flatpak_file()
        else:
            self.getMode()
    
    def write_flatpak_file(self):
        try:
            count = 0
            dummyList = []

            # Get user installed flatpaks
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(str(mainIniFile.flatpak_txt_location()), 'w') as configfile:  
                for output in os.popen(getFlatpaks):
                    dummyList.append(output)
                    # Write USER installed flatpak to flatpak.txt inside external device
                    configfile.write(dummyList[count])
                    count += 1

        except OSError as error:
            print(error)

            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', 'false')
                # Change system tray color to red (Error)
                config.set('INFO', 'notification_id', "2")
                # Reset Main Window information
                config.set('INFO', 'notification_add_info', f"Read-only, {error}")
            exit()

        self.getMode()

    def getMode(self):
        print("Getting mode...")
        try:
            if str(mainIniFile.ini_multiple_time_mode()) == "true":
                # Create folder with date and time
                sub.run(f"{createCMDFolder} {str(mainIniFile.time_folder_format())}", shell=True)  

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        self.backup_home()

    def backup_home(self):
        print("Backing up Home folders...")
        try:
            # Backup all (user.ini true folders)
            for output in get_folders():
                # Write current stastus
                self.update_feedback_status(output)

                # Copy the Home files/folders
                print(f"{copyCPCMD} {homeUser}/{output} {str(mainIniFile.time_folder_format())}")
                sub.run(f"{copyCPCMD} {homeUser}/{output} {str(mainIniFile.time_folder_format())}",shell=True)

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        if str(mainIniFile.ini_allow_flatpak_data()) == "true":
            self.backup_flatpak_data()
        else:
            self.backup_icons()

    def backup_flatpak_data(self):
        print("Backing up Flatpak folders...")
        try:
            ################################################################################
            # Start Flatpak (var/app) backup
            ################################################################################
            count = 0
            for output in flatpak_var_list():
                # Write current stastus
                self.update_feedback_status(output)

                # Copy the Flatpak var/app folders
                print(f"{copyCPCMD} {flatpak_var_list()[count]} {str(mainIniFile.application_var_folder())}")
                sub.run(f"{copyCPCMD} {flatpak_var_list()[count]} {str(mainIniFile.application_var_folder())}", shell=True)
                count += 1

            ################################################################################
            # Start Flatpak (.local/share/flatpak) backup
            ################################################################################
            count = 0
            for output in flatpak_local_list():
                # Write current stastus
                self.update_feedback_status(output)

                # Copy the Flatpak var/app folders
                print(f"{copyRsyncCMD} {flatpak_local_list()[count]} {str(mainIniFile.application_local_folder())}")
                sub.run(f"{copyRsyncCMD} {flatpak_local_list()[count]} {str(mainIniFile.application_local_folder())}", shell=True)
                count += 1

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        self.backup_icons()

    def backup_icons(self):
        delete_old_settings_settings("Icon")
        self.update_feedback_status(users_icon_name())

        try:
            os.listdir(f"/usr/share/icons/{users_icon_name()}")
            sub.run(f"{copyRsyncCMD} /usr/share/icons/{users_icon_name()} {str(mainIniFile.icon_main_folder())}", shell=True)
        except: 
            sub.run(f"{copyRsyncCMD} {homeUser}/.icons/{users_icon_name()} {str(mainIniFile.icon_main_folder())}", shell=True)
        else:
            sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/icons/{users_icon_name()} {str(mainIniFile.icon_main_folder())}", shell=True)

        self.backup_cursor()

    def backup_cursor(self):
        delete_old_settings_settings("Cursor")
        self.update_feedback_status(userCurrentcursor)

        try:
            os.listdir(f"/usr/share/icons/{users_cursor_name()}")
            sub.run(f"{copyRsyncCMD} /usr/share/icons/{users_cursor_name()} {str(mainIniFile.cursor_main_folder())}", shell=True)
        except: 
            try:
                sub.run(f"{copyRsyncCMD} {homeUser}/.icons/{users_cursor_name()} {str(mainIniFile.cursor_main_folder())}", shell=True)
            except:
                sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/icons/{users_cursor_name()} {str(mainIniFile.cursor_main_folder())}", shell=True)

        self.backup_theme()

    def backup_theme(self):
        delete_old_settings_settings("Theme")
        self.update_feedback_status(users_theme_name())

        ################################################################################
        # Create gnome-shell inside theme current theme folder
        ################################################################################
        if not os.path.exists(f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/"
            f"{themeFolderName}/{users_theme_name()}/{gnomeShellFolder}"):
            try:
                sub.run(f"{createCMDFolder} {str(mainIniFile.ini_external_location())}/{baseFolderName}/"
                    f"{themeFolderName}/{users_theme_name()}/{gnomeShellFolder}", shell=True)
            except Exception as error:
                pass

        try:
            os.listdir(f"/usr/share/themes/{users_theme_name()}/")
            sub.run(f"{copyRsyncCMD} /usr/share/themes/{users_theme_name()} {str(mainIniFile.theme_main_folder())}", shell=True)
        except:
            sub.run(f"{copyRsyncCMD} {homeUser}/.themes/{users_theme_name()} {str(mainIniFile.theme_main_folder())}", shell=True)
        else:
            sub.run(f"{copyRsyncCMD} {homeUser}/.local/share/themes/{users_theme_name()} {str(mainIniFile.theme_main_folder())}", shell=True)

        ################################################################################
        # Get gnome-shell with the current theme name
        ################################################################################
        try:
            if os.listdir(f"/usr/share/gnome-shell/theme/{users_theme_name()}/"):
                sub.run(f"{copyRsyncCMD} /usr/share/gnome-shell/theme/{users_theme_name()}/ "
                    f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/"
                    f"{themeFolderName}/{users_theme_name()}/{gnomeShellFolder}", shell=True)
        except:
            pass

        self.end_backup()

    def end_backup(self):
        print("Ending backup...")

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            try:
                # Update last backup time
                config.set('INFO', 'latest', f'{latest_time_info()}')
            except:
                pass
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
