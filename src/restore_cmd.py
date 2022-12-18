#! /usr/bin/python3
from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class RESTORE:
    def __init__(self):
        # Set restore is running to True
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            # Restore
            config.set('RESTORE', 'is_restore_running', "true")
            config.write(configfile)

        self.read_ini_file()

    def read_ini_file(self):
        # Read file
        config = configparser.ConfigParser()
        config.read(src_user_config)

        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniFolder = config.options('FOLDER')
        # Restore
        self.iniFlatpakApplications = config['RESTORE']['applications_flatpak_names']
        self.iniApplicationsPackages = config['RESTORE']['applications_packages']
        self.iniApplicationData = config['RESTORE']['applications_data']
        self.iniFilesAndsFolders = config['RESTORE']['files_and_folders']
        self.iniSystemSettings = config['RESTORE']['system_settings']

        # INFO
        self.packageManager = config['INFO']['packageManager']
        self.iniUserOS = config['INFO']['os']
        self.iniAutoReboot = config['INFO']['auto_reboot']
        # Icon
        self.iniIcon = config['INFO']['icon']
        # Theme
        self.iniTheme = config['INFO']['theme']
        # Cursor
        self.iniCursor = config['INFO']['cursor']

        # Wallpaper users folder
        self.wallpaperMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}"        # Icons users folder
        # Icons users folder
        self.iconsMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{iconFolderName}"
        # Themes users folder
        self.themeMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{themeFolderName}"
        # Cursor users folder
        self.cursorMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{cursorFolderName}"
        # Flatpak txt file
        self.flatpakTxtFile = f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}"

        self.get_home_backup_folders()

    def get_home_backup_folders(self):
        self.iniFoldersList = []
        # Get available folders from INI file
        for output in self.iniFolder:
            output = output.capitalize()
            self.iniFoldersList.append(output)

        self.get_latest_date_home()

    def get_latest_date_home(self):
        try:
            self.latestDateFolder = []
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"):
                if not "." in output:
                    self.latestDateFolder.append(output)
                    self.latestDateFolder.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        except FileNotFoundError as error:
                print("Error trying to delete old backups!")
                print(error)
                exit()

        self.get_latest_time_date_home()

    def get_latest_time_date_home(self):
        try:
            ################################################################################
            # Get available times inside {folderName}
            ################################################################################
            self.latestTimeFolder = []
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{self.latestDateFolder[0]}/"):
                self.latestTimeFolder.append(output)
                self.latestTimeFolder.sort(reverse=True)

        except FileNotFoundError as error:
            print(error)
            pass
        
        self.get_home_folders_size()

    def get_home_folders_size(self):
        try:
            print("Checking size of folders...")
            ################################################################################
            # Get folders size
            ################################################################################
            self.homeFolderToRestoreSizeList=[]
            self.homeFolderToBeRestore=[]
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/"):  # Get folders size before back up to external
                 # Capitalize first letter
                output = output.capitalize() 
                # Can output be found inside Users Home?
                try:
                    os.listdir(f"{homeUser}/{output}")
                except:
                    # Lower output first letter
                    output = output.lower() # Lower output first letter
                # Get folder size
                getSize = os.popen(f"du -s {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                        f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/")
                getSize = getSize.read().strip("\t").strip("\n").replace(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                        f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/", "").replace("\t", "")
                getSize = int(getSize)

                # Add to list
                self.homeFolderToRestoreSizeList.append(getSize)
                # Add output inside self.homeFolderToBeRestore
                self.homeFolderToBeRestore.append(output)

        except:
            pass

        self.get_flatpak_data_size()

    def get_flatpak_data_size(self):
        try:
            print("Checking size of flatpak (var)...")
            ################################################################################
            # Get folders size
            ################################################################################
            self.flatpakVarSizeList=[]
            self.flatpakLocalSizeList=[]
            self.flatpakVarToBeRestore=[]
            self.flatpakLocaloBeRestore=[]
            
            for output in os.listdir(src_flatpak_var_location): 
                getSize = os.popen(f"du -s {src_flatpak_var_location}/{output}")
                getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_var_location}/{output}", "").replace("\t", "")
                getSize = int(getSize)

                ################################################################################
                # Add to list
                # If current folder (output inside var/app) is not higher than X MB
                # Add to list to be backup
                ################################################################################
                # Add to self.flatpakVarSizeList KBytes size of the current output (folder inside var/app)
                # inside external device
                self.flatpakVarSizeList.append(getSize)
                # Add current output (folder inside var/app) to be backup later
                self.flatpakVarToBeRestore.append(f"{src_flatpak_var_location}/{output}")
            
            ################################################################################
            # Get flatpak (.local/share/flatpak) folders size
            ################################################################################
            for output in os.listdir(src_flatpak_local_location):  # Get .local/share/flatpak size before back up to external
                # Get size of flatpak folder inside var/app/
                getSize = os.popen(f"du -s {src_flatpak_local_location}/{output}")
                getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_local_location}/{output}", "").replace("\t", "")
                getSize = int(getSize)

                # Add to list to be backup
                self.flatpakVarSizeList.append(getSize)
                # Add current output (folder inside var/app) to be backup later
                self.flatpakLocaloBeRestore.append(f"{src_flatpak_local_location}/{output}")
                self.flatpakLocaloBeRestore=[]

        except:
            pass

        self.apply_users_saved_wallpaper()

    def apply_users_saved_wallpaper(self):
        dummyList = []
        try:
            # Find user's DE type
            self.userPackageManager = os.popen(getUserDE)
            self.userPackageManager = self.userPackageManager.read().strip().lower()

            # Check if a wallpaper can be found
            for wallpaper in os.listdir(f"{self.wallpaperMainFolder}/"):
                dummyList.append(wallpaper)
            
            # If has a wallpaper to restore and self.iniSystemSettings == "true":
            if dummyList and self.iniSystemSettings == "true":
                # Check if user DE is in the supported list
                ################################################################
                for count in supported:
                    # Activate wallpaper option
                    if supported[count] in self.userPackageManager:
                        # Detect color scheme
                        getColorScheme = os.popen(detectThemeMode)
                        getColorScheme = getColorScheme.read().strip().replace("'", "")

                        print("Restoring wallpaper...")
                        for image in os.listdir(f"{self.iniExternalLocation}/"
                            f"{baseFolderName}/{wallpaperFolderName}/"):
                            # Copy the wallpaper to the user's Pictures
                            sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/"
                                f"{wallpaperFolderName}/{image} {homeUser}/Pictures", shell=True)

                            # Remove spaces if exist
                            if "," in image:
                                image = str(image.replace(", ", "\, "))
                                
                            # Add \ if it has space
                            if " " in image:
                                image = str(image.replace(" ", "\ "))
                    
                            # Light or Dark wallpaper
                            if getColorScheme == "prefer-light" or getColorScheme == "default":
                                # Light theme o default
                                print(f"{setGnomeWallpaper} {homeUser}/Pictures/{image}")
                                sub.run(f"{setGnomeWallpaper} {homeUser}/Pictures/{image}", shell=True)

                            else:
                                # Dark theme
                                print(f"{setGnomeWallpaperDark} {homeUser}/Pictures/{image}")
                                sub.run(f"{setGnomeWallpaperDark} {homeUser}/Pictures/{image}", shell=True)

                            # Set wallpaper to Zoom
                            sub.run(f"{zoomGnomeWallpaper}", shell=True)
                            ################################################################
                        
                # Restore icon
                self.restore_icons()

            # Restore applications packages
            self.restore_applications_packages()

        except:
            pass

    def restore_icons(self):
        print("Restoring icon...")

        try:
            self.somethingToRestoreInIcon = []
            # Check for icon to be restored
            for icon in os.listdir(f"{self.iconsMainFolder}/"):
                self.somethingToRestoreInIcon.append(icon)
            
            # If has something to restore
            if self.somethingToRestoreInIcon:
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    # Write to INI file saved icon name
                    config.set('INFO', 'icon', f'{self.somethingToRestoreInIcon[0]}')
                    config.write(configfile)

                ################################################################################
                # Create .icons inside home user
                ################################################################################
                if not os.path.exists(f"{homeUser}/.icons"):
                    print("Creating .icons inside home user...")
                    print(f"{createCMDFolder} {homeUser}/.icons")
                    sub.run(f"{createCMDFolder} {homeUser}/.icons", shell=True)   

                # Copy icon from the backup to .icon folder
                sub.run(f"{copyRsyncCMD} {self.iconsMainFolder}/ {homeUser}/.icons/", shell=True)
                
                # Check if user DE is in the supported list
                ################################################################
                for count in supported:
                    # Activate wallpaper option
                    if supported[count] in self.userPackageManager:
                        # Apply icon
                        print(f"Applying {setUserIcon} {self.iniIcon}")
                        sub.run(f"{setUserIcon} {self.iniIcon}", shell=True)

        except:
            print("No icon to restore.")
            pass

        self.restore_cursor()

    def restore_cursor(self):
        print("Restoring cursor...")

        try:        
            self.somethingToRestoreInCursor = []
            # Check for cursor to be restored
            for cursor in os.listdir(f"{self.cursorMainFolder}/"):
                self.somethingToRestoreInCursor.append(cursor)

            # If has something to restore
            if self.somethingToRestoreInCursor:
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    # Write to INI file saved icon name
                    config.set('INFO', 'cursor', f'{self.somethingToRestoreInCursor[0]}')
                    config.write(configfile)
                    
                # Copy icon from the backup to .icon folder
                sub.run(f"{copyRsyncCMD} {self.cursorMainFolder}/ {homeUser}/.icons/", shell=True)

                # Check if user DE is in the supported list
                ################################################################
                for count in supported:
                    # Activate wallpaper option
                    if supported[count] in self.userPackageManager:
                        # Apply cursor
                        print(f"Applying {setUserCursor} {self.iniCursor}")
                        sub.run(f"{setUserCursor} {self.iniCursor}", shell=True)

        except:
            pass

        self.restore_theme()

    def restore_theme(self):
        print("Restoring theme...")

        try:
            self.somethingToRestoreInTheme = []
            # Check for theme to be restored
            for theme in os.listdir(f"{self.themeMainFolder}/"):
                self.somethingToRestoreInTheme.append(theme)

            # If has something to restore
            if self.somethingToRestoreInTheme:
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    # Write to INI file saved theme name
                    config.set('INFO', 'theme', f'{self.somethingToRestoreInTheme[0]}')
                    config.write(configfile)

                ################################################################################
                # Create .themes inside home user
                ################################################################################
                if not os.path.exists(f"{homeUser}/.themes"):
                    print("Creating .themes inside home user...")
                    sub.run(f"{createCMDFolder} {homeUser}/.themes", shell=True)   

                # Copy theme from the backup to .theme folder
                sub.run(f"{copyRsyncCMD} {self.themeMainFolder}/ {homeUser}/.themes/", shell=True)
                               # Check if user DE is in the supported list
                ################################################################
                for count in supported:
                    # Activate wallpaper option
                    if supported[count] in self.userPackageManager:
                        # Apply theme
                        print(f"Applying {setUserTheme} {self.iniTheme}")
                        sub.run(f"{setUserTheme} {self.iniTheme}", shell=True)
        
        except:
            print("No theme to restore.")
            pass

        if self.iniApplicationsPackages == "true":
            self.restore_applications_packages()

        else:
            self.restore_flatpaks()

    def restore_applications_packages(self):
        print("Installing applications packages...")
        try:             
            if self.packageManager == "rpm":
                ################################################################################
                # Restore RPMS
                ################################################################################
                for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
                    f"{applicationFolderName}/{rpmFolderName}"):
                    print(f"{installRPM} {self.iniExternalLocation}/{baseFolderName}/"
                        f"{applicationFolderName}/{rpmFolderName}/{output}")

                    # Install rpms applications
                    sub.run(f"{installRPM} {self.iniExternalLocation}/{baseFolderName}/"
                        f"{applicationFolderName}/{rpmFolderName}/{output}", shell=True)
            
            elif self.packageManager == "deb":
                ################################################################################
                # Restore DEBS
                ################################################################################
                for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
                    f"{applicationFolderName}/{debFolderName}"):
                    print(f"{installRPM} {self.iniExternalLocation}/{baseFolderName}/"
                        f"{applicationFolderName}/{debFolderName}/{output}")
                        
                    # Install debs applications
                    sub.run(f"{installDEB} {self.iniExternalLocation}/{baseFolderName}/"
                        f"{applicationFolderName}/{debFolderName}/{output}", shell=True)

                # Fix packages installation
                sub.run("sudo apt install -y -f", shell=True)

            # Add flathub repository
            sub.run("sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo", shell=True)
        
        except:
            print("Error trying to install packages...")
            pass
        
        self.restore_flatpaks()

    def restore_flatpaks(self):
        if self.iniFlatpakApplications == "true":
            print("Installing flatpaks apps...")
            try: 
                # Restore flatpak apps
                with open(self.flatpakTxtFile, "r") as read_file:
                    read_file = read_file.readlines()

                    for output in read_file:
                        output = output.strip()
                        ###############################################################################
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'feedback_status', f"{output}")
                            config.write(configfile)

                        ###############################################################################
                        sub.run(f"flatpak install --system --noninteractive --assumeyes --or-update {output}", shell=True)
                        ###############################################################################
                
                # Got to flatpak DATA
                self.restore_flatpak_data()

            except:
                pass

        else:
            if self.iniFilesAndsFolders == "true":
                self.restore_home()

            else:
                self.end_backup()

    def restore_flatpak_data(self):
        print("Restoring flatpaks data...")
        try:
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/"
                f"{varFolderName}/"):
                ###############################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"{output}")
                    config.write(configfile)

                ################################################################################
                # Restore flatpak data (var) folders from external device
                ################################################################################
                sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                    f"{applicationFolderName}/{varFolderName}/{output} {src_flatpak_var_location}", shell=True)
                
        except:
            pass
        
        self.restore_flatpak_data_local()
        
    def restore_flatpak_data_local(self):
        print("Restoring flatpaks data (local)...")
        try:
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
                f"{applicationFolderName}/{localFolderName}/"):

                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"{output}")
                    config.write(configfile)

                ################################################################################
                # Restore flatpak data (var) folders from external device
                ################################################################################
                sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                    f"{applicationFolderName}/{localFolderName}/{output} {src_flatpak_local_location}", shell=True)

        except:
            pass

        if self.iniFilesAndsFolders == "true":
            self.restore_home()

        else:
            self.end_backup()

    def restore_home(self):
        try:
            print("Restoring Home folders...")
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                    f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/"):

                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"{output}")
                    config.write(configfile)
                
                ###############################################################################
                # If output folder do not exist, create it
                ###############################################################################
                if not os.path.exists(f"{homeUser}/{output}/"):
                    print(f"This {output} do not exist inside {homeUser}/ Home")
                    sub.run(f"{createCMDFolder} {homeUser}/{output}", shell=True)
                
                ###############################################################################
                # Restore Home folders
                ###############################################################################
                sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/"
                    f"{backupFolderName}/{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/"
                    f"{output}/ {homeUser}/{output}/", shell=True)

        except:
            pass

        self.end_backup()

    def end_backup(self):
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
            # Restore settings
            config.set('RESTORE', 'is_restore_running', "false")
            config.set('RESTORE', 'applications_packages', "false")
            config.set('RESTORE', 'applications_flatpak_names', "false")
            config.set('RESTORE', 'applications_data', "false")
            config.set('RESTORE', 'files_and_folders', "false")
            config.set('RESTORE', 'system_settings', "false")
            config.write(configfile)

        ################################################################################
        # After backup is done
        ################################################################################
        print("Restoring is done!")
        # Reboot

        if self.iniAutoReboot == "true":
            ###############################################################################
            # Update INI file
            ###############################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                # Set auto rebooting to false
                config.set('INFO', 'auto_reboot', "false")
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

main = RESTORE()