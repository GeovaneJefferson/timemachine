#! /usr/bin/python3
from setup import *
from prepare_backup import *
from get_user_wallpaper import *
from update import backup_ini_file

################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class BACKUP:
    def __init__(self):
        self.read_ini_file()

    def read_ini_file(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)

            # Get hour, minute
            self.dateTime = datetime.now()
            self.dateDay = self.dateTime.strftime("%d")
            self.dateMonth = self.dateTime.strftime("%m")
            self.dateYear = self.dateTime.strftime("%y")
            self.dayName = self.dateTime.strftime("%a")
            self.currentHour = self.dateTime.strftime("%H")
            self.currentMinute = self.dateTime.strftime("%M")

            ################################################################################
            # Get user.ini
            ################################################################################
            self.iniExternalLocation = config['EXTERNAL']['hd']
            self.iniFolders = config.options('FOLDER')
            self.iniBackupNow = config['BACKUP']['backup_now']
            self.iniOneTimePerDay = config['MODE']['one_time_mode']
            self.iniAllowFlatpakNames = config['BACKUP']['allow_flatpak_names']
            self.iniAllowFlatpakData = config['BACKUP']['allow_flatpak_data']
            self.iniUserOS = config['INFO']['os']

            # Base folder
            self.createBaseFolder = f"{self.iniExternalLocation}/{baseFolderName}"
            # Backup folder
            self.createBackupFolder = f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
            # Wallpaper main folder
            self.wallpaperMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}"
            # Application main folder
            self.applicationMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}"
            # Application main Var folder
            self.applicationVarFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{varFolderName}"
            # Application main Local folder
            self.applicationLocalFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{localFolderName}"
            # Check date inside backup folder
            self.checkDateInsideBackupFolder = f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
            # Icons users folder
            self.iconsMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{iconFolderName}"
            # Cursor users folder
            self.cursorMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{cursorFolderName}"
            # Themes users folder
            self.themeMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{themeFolderName}"
            # Gnome-shell users folder
            self.gnomeShellMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{themeFolderName}/{gnomeShellFolder}"
            
            # PACKAGES
            # RPM main folder
            self.rpmMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{rpmFolderName}"
            # DEB main folder
            self.debMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{debFolderName}"

            # Date folder
            self.dateFolder = f"{self.createBackupFolder}/{self.dateDay}-{self.dateMonth}-{self.dateYear}"
            # Time folder
            self.timeFolder = f"{self.createBackupFolder}/{self.dateDay}-{self.dateMonth}-{self.dateYear}/{self.currentHour}-{self.currentMinute}"
            # Flatpak txt file
            self.flatpakTxtFile = f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}"
            
            # Set backup now to True
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', "true")
                config.write(configfile)
                
        except KeyError as error:
            print(error)
            exit()

        # Continue
        self.backup_user_wallpaper()

    def backup_user_wallpaper(self):
        # Replace wallpaper inside the folder, only allow 1
        # If is not empty
        insideWallpaperFolder = os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/")
        # If it has image inside the folder
        if insideWallpaperFolder:
            print("Image(s) found inside.")
            # Delete all image inside wallpaper folder
            for image in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/"):
                print(f"Deleting {self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/{image}...")
                sub.run(f"rm -rf {self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/{image}", shell=True)
        
        print("Backing up wallpaper...")
        # Get Wallaper
        print(f"{copyCPCMD} {user_wallpaper()} {self.wallpaperMainFolder}/")
        sub.run(f"{copyCPCMD} {user_wallpaper()} {self.wallpaperMainFolder}/", shell=True) 
       
        # Condition
        if self.iniAllowFlatpakNames == "true":
            self.write_flatpak_file()
        
        else:
            self.getMode()
    
    def write_flatpak_file(self):
        try:
            # Add flatpak name to the list
            count = 0
            dummyList = []
            # Get user installed flatpaks
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(self.flatpakTxtFile, 'w') as configfile:  
                for output in os.popen(getFlatpaks):
                    dummyList.append(output)
                    # Write USER installed flatpak to flatpak.txt inside external device
                    configfile.write(dummyList[count])
                    count += 1

        # If read only error    
        except OSError as error:
            print(error)
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                # Set backup now to False
                config.set('BACKUP', 'backup_now', 'false')
                # Change system tray color to red (Error)
                config.set('INFO', 'notification_id', "2")
                # Reset Main Window information
                config.set('INFO', 'notification_add_info', f"Read-only, {error}")
            exit()

        self.getMode()

    def getMode(self):
        print("Getting mode...")
        ################################################################################
        # Type of backup (One or Multiple times per day)
        ################################################################################
        try:
            # One time per day
            if self.iniOneTimePerDay == "true":
                print("Mode: One time per day")

            # Multiple time per day
            else:
                print("Mode: Multiple time per day")
                sub.run(f"{createCMDFolder} {self.timeFolder}", shell=True)  # Create folder with date and time

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        self.backup_home()

    def backup_home(self):
        print("Backing up Home folders...")
        try:
            ################################################################################
            # Start Home backup
            ################################################################################
            # Backup all (user.ini true folders)
            for output in get_folders():
                """
                Write current save file name to INI file
                so it can be show on main window (mainwindow.py)
                This way, user will have a feedback to what
                is happening.
                Write current folder been backup to INI file
                """
                ###############################################################################
                self.update_feedback_status(output)
                # config = configparser.ConfigParser()
                # config.read(src_user_config)
                # with open(src_user_config, 'w') as configfile:
                #     config.set('INFO', 'feedback_status', f"Backing up: {output}")
                #     config.write(configfile)

                ###############################################################################
                # Copy the Home files/folders
                ###############################################################################
                print(f"{copyCPCMD} {homeUser}/{output} {self.timeFolder}")
                sub.run(f"{copyCPCMD} {homeUser}/{output} {self.timeFolder}", shell=True)

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        if self.iniAllowFlatpakData == "true":
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
                ###############################################################################
                # Write current save file name to INI file
                # so it can be show on main window (gui.py)
                # This way, user will have a feedback to what
                # is happening.
                # Write current folder been backup to INI file
                ###############################################################################
                self.update_feedback_status(output)
                # config = configparser.ConfigParser()
                # config.read(src_user_config)
                # with open(src_user_config, 'w') as configfile:
                #     config.set('INFO', 'feedback_status', f"Backing up: {output}")
                #     config.write(configfile)

                ###############################################################################
                # Copy the Flatpak var/app folders
                ###############################################################################
                print(f"{copyCPCMD} {flatpak_var_list()[count]} {self.applicationVarFolder}")
                sub.run(f"{copyCPCMD} {flatpak_var_list()[count]} {self.applicationVarFolder}", shell=True)

                count += 1

            ################################################################################
            # Start Flatpak (.local/share/flatpak) backup
            ################################################################################
            count = 0
            for output in flatpak_local_list():
                ###############################################################################
                # Write current save file name to INI file
                # so it can be show on main window (gui.py)
                # This way, user will have a feedback to what
                # is happening.
                # Write current folder been backup to INI file
                ###############################################################################
                self.update_feedback_status(output)
                # config = configparser.ConfigParser()
                # config.read(src_user_config)
                # with open(src_user_config, 'w') as configfile:
                #     config.set('INFO', 'feedback_status', f"Backing up: {output}")
                #     config.write(configfile)

                ###############################################################################
                # Copy the Flatpak var/app folders
                ###############################################################################
                print(f"{copyRsyncCMD} {flatpak_local_list()[count]} {self.applicationLocalFolder}")
                sub.run(f"{copyRsyncCMD} {flatpak_local_list()[count]} {self.applicationLocalFolder}", shell=True)

                count += 1

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        self.backup_icons()

    def backup_icons(self):
        ################################################################################
        # Get current use icon by user
        ################################################################################
        userCurrentGnomeIcon = os.popen(getUserIcon)
        userCurrentGnomeIcon = userCurrentGnomeIcon.read().strip()
        userCurrentGnomeIcon = userCurrentGnomeIcon.replace("'", "")

        ################################################################################
        # Only one icon inside the backup folder
        ################################################################################
        insideIconFolder = os.listdir(f"{self.iconsMainFolder}/")
        # Delete all image inside .icons folder
        if insideIconFolder:
            for icon in os.listdir(f"{self.iconsMainFolder}/"):
                # If is not the same name, remove it, and backup the new one
                if icon != userCurrentGnomeIcon:
                    print(f"Deleting {self.iconsMainFolder}/{icon}...")
                    sub.run(f"rm -rf {self.iconsMainFolder}/{icon}", shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            # Save icon information
            config.set('INFO', 'icon', f"{userCurrentGnomeIcon}")
            # config.set('INFO', 'feedback_status', f"Backing up: icons")
            config.write(configfile)

        self.update_feedback_status(userCurrentGnomeIcon)

        try:
            # USR/SHARE
            os.listdir(f"/usr/share/icons/{userCurrentGnomeIcon}")
            sub.run(f"{copyRsyncCMD} /usr/share/icons/{userCurrentGnomeIcon} {self.iconsMainFolder}", shell=True)
       
        except: 
            # Try to find the current icon inside /home/user/.icons
            sub.run(f"{copyRsyncCMD} {homeUser}/.icons/{userCurrentGnomeIcon} {self.iconsMainFolder}", shell=True)
      
        else:
            pass

        self.backup_cursor()

    def backup_cursor(self):
        ################################################################################
        # Get current use cursor by user
        ################################################################################
        userCurrentcursor = os.popen(getUserCursor)
        userCurrentcursor = userCurrentcursor.read().strip()
        userCurrentcursor = userCurrentcursor.replace("'", "")

        ################################################################################
        # Only one cursor inside the backup folder
        ################################################################################
        insidecursorFolder = os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{cursorFolderName}/")
        if insidecursorFolder:
            # Delete all cursors inside wallpaper folder
            for cursor in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{cursorFolderName}/"):
                # If is not the same name, remove it, and backup the new one
                if cursor != userCurrentcursor:
                    print(f"Deleting {self.iniExternalLocation}/{baseFolderName}/{cursorFolderName}/{cursor}...")
                    sub.run(f"rm -rf {self.iniExternalLocation}/{baseFolderName}/{cursorFolderName}/{cursor}", shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            # Save cursor information
            config.set('INFO', 'cursor', f"{userCurrentcursor}")
            # config.set('INFO', 'feedback_status', f"Backing up: cursor")
            config.write(configfile)

        self.update_feedback_status(userCurrentcursor)

        try:
            # USR/SHARE/ICONS
            # Try to find
            os.listdir(f"/usr/share/icons/{userCurrentcursor}")
            sub.run(f"{copyRsyncCMD} /usr/share/icons/{userCurrentcursor} {self.cursorMainFolder}", shell=True)

        except: 
            try:
                # Try to find the current cursor inside /home/user/.icons
                sub.run(f"{copyRsyncCMD} {homeUser}/.icons/{userCurrentcursor} {self.cursorMainFolder}", shell=True)

            except:
                pass

        self.backup_theme()

    def backup_theme(self):
        ################################################################################
        # Get current use icon by user
        ################################################################################
        userCurrentTheme = os.popen(getUserTheme)
        userCurrentTheme = userCurrentTheme.read().strip()
        userCurrentTheme = userCurrentTheme.replace("'", "")

        ################################################################################
        # Only one icon inside the backup folder
        ################################################################################
        insideThemeFolder = os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{themeFolderName}/")
        if insideThemeFolder:
            # Delete all theme inside wallpaper folder
            for theme in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{themeFolderName}/"):
                # If is not the same name, remove it, and backup the new one
                if theme != userCurrentTheme:
                    print(f"Deleting {self.iniExternalLocation}/{baseFolderName}/{themeFolderName}/{theme}...")
                    sub.run(f"rm -rf {self.iniExternalLocation}/{baseFolderName}/{themeFolderName}/{theme}", shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            # Save theme information
            config.set('INFO', 'theme', f"{userCurrentTheme}")
            # config.set('INFO', 'feedback_status', f"Backing up: theme")
            config.write(configfile)
        
        self.update_feedback_status(userCurrentTheme)

        ################################################################################
        # Try to find the current theme inside /home/user/.theme
        ################################################################################
        # Create gnome-shell inside theme current theme folder
        ################################################################################
        if not os.path.exists(f"{self.iniExternalLocation}/{baseFolderName}/"
            f"{themeFolderName}/{userCurrentTheme}/{gnomeShellFolder}"):
            try:
                sub.run(f"{createCMDFolder} {self.iniExternalLocation}/{baseFolderName}/"
                    f"{themeFolderName}/{userCurrentTheme}/{gnomeShellFolder}", shell=True)
            
            except Exception as error:
                pass

        try:
            # USR/SHARE
            os.listdir(f"/usr/share/themes/{userCurrentTheme}/")
            sub.run(f"{copyRsyncCMD} /usr/share/themes/{userCurrentTheme} {self.themeMainFolder}", shell=True)
        
        except:
            # .THEMES
            sub.run(f"{copyRsyncCMD} {homeUser}/.themes/{userCurrentTheme} {self.themeMainFolder}", shell=True)
        else:
            pass

        ################################################################################
        # Get gnome-shell with the current theme name
        ################################################################################
        try:
            insideGnomeShellThemeFolder = os.listdir(f"/usr/share/gnome-shell/theme/{userCurrentTheme}/")
            if insideGnomeShellThemeFolder:
                print("Backing up theme gnome-shell...")
                sub.run(f"{copyRsyncCMD} /usr/share/gnome-shell/theme/{userCurrentTheme}/ "
                    f"{self.iniExternalLocation}/{baseFolderName}/"
                    f"{themeFolderName}/{userCurrentTheme}/{gnomeShellFolder}", shell=True)
        
        except:
            pass

        self.end_backup()

    def end_backup(self):
        # try:
        #     # Get oldest backup info
        #     oldestList = []
        #     for oldestOutput in os.listdir(f"{self.createBackupFolder}"):
        #         oldestList.append(oldestOutput)
        # except:
        #     pass

        print("Ending backup...")
        ################################################################################
        # Set backup_now to "false", backup_running to "false" and Update "last backup"
        # After all done, feedback_status = "" 
        ###############################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            # Set backup now to False
            config.set('BACKUP', 'backup_now', 'false')
            # try:
            #     # Update oldest backup time
            #     config.set('INFO', 'oldest', f'{oldestList[0]}')
            # except:
            #     pass
            try:
                # Update last backup time
                config.set('INFO', 'latest', f'{latest_time_info()}')
            except:
                pass
            # Change system tray color to white (Normal)
            config.set('INFO', 'notification_id', "0")
            # Reset Main Window information
            config.set('INFO', 'notification_add_info', "")
            # Clean current back up folder from Main Window
            # config.set('INFO', 'feedback_status', "")
            # Set checker runner to False
            config.set('BACKUP', 'checker_running', "true")
            # Time left to None
            config.set('SCHEDULE', 'time_left', 'None')
            config.write(configfile)
        
        # Clean current back up folder from Main Window
        self.update_feedback_status("")
        ################################################################################
        # Backup Ini File
        ################################################################################
        print("Backing up user.ini file...")
        backup_ini_file(False)
        ################################################################################
        # After backup is done
        ################################################################################
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
    main = BACKUP()
