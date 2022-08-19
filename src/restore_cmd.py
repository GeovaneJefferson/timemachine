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
                print(f"du -s {src_flatpak_local_location}/{output}")

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
        if self.iniSystemSettings == "true":
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
                if getColorScheme == "prefer-light" or "default":
                    # Light theme o default
                    sub.run(f"{setGnomeWallpaper} {homeUser}/Pictures/{image}/", shell=True)

                else:
                    # Dark theme
                    sub.run(f"{setGnomeWallpaperDark} {homeUser}/Pictures/{image}/", shell=True)

                # Set wallpaper to Zoom
                sub.run(f"{zoomGnomeWallpaper}", shell=True)

        # Restore icon
        self.restore_icons()

    def restore_icons(self):
        if self.iniSystemSettings == "true":
            print("Restoring icon...")

            dummyList = []
            # Get current icon
            for icon in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{iconFolderName}/"):
                dummyList.append(icon)

            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                # Write to INI file saved icon name
                config.set('INFO', 'icon', f'{dummyList[0]}')
                config.write(configfile)
                
        try:
            ################################################################################
            # Create .icons inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.icons"):
                print("Creating .icons inside home user...")
                print(f"{createCMDFolder} {homeUser}/.icons")
                sub.run(f"{createCMDFolder} {homeUser}/.icons", shell=True)   

            # Copy icon from the backup to .icon folder
            sub.run(f"{copyRsyncCMD} {self.iconsMainFolder}/ {homeUser}/.icons/", shell=True)
            
            ################################################################################
            # Read file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # Icon
            iniIcon = config['INFO']['icon']
        
            # Apply the icon
            print(f"Applying {setUserIcon} {iniIcon}")
            sub.run(f"{setUserIcon} {iniIcon}", shell=True)

        except:
            pass

        self.restore_cursor()

    def restore_cursor(self):
        if self.iniSystemSettings == "true":
            print("Restoring cursor...")

            dummyList = []
            # Get current cursor
            for cursor in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{cursorFolderName}/"):
                dummyList.append(cursor)

            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                    # Write to INI file saved icon name
                    config.set('INFO', 'cursor', f'{dummyList[0]}')
                    config.write(configfile)
                
        try:
            # Copy icon from the backup to .icon folder
            sub.run(f"{copyRsyncCMD} {self.cursorMainFolder}/ {homeUser}/.icons/", shell=True)
            
            ################################################################################
            # Read file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # Cursor
            iniCursor = config['INFO']['cursor']
        
            # Apply cursor
            print(f"Applying {setUserCursor} {iniCursor}")
            sub.run(f"{setUserCursor} {iniCursor}", shell=True)

        except:
            pass

        self.restore_theme()

    def restore_theme(self):
        if self.iniSystemSettings == "true":
            print("Restoring theme...")

            dummyList = []
            # Get current theme
            for theme in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{themeFolderName}/"):
                dummyList.append(theme)

            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                # Write to INI file saved theme name
                config.set('INFO', 'theme', f'{dummyList[0]}')
                config.write(configfile)

        try:
            ################################################################################
            # Create .themes inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.themes"):
                print("Creating .themes inside home user...")
                sub.run(f"{createCMDFolder} {homeUser}/.themes", shell=True)   

            # Copy theme from the backup to .theme folder
            sub.run(f"{copyRsyncCMD} {self.themeMainFolder}/ {homeUser}/.themes/", shell=True)
            
            ################################################################################
            # Read file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # Theme
            iniTheme = config['INFO']['theme']

            # Apply theme
            print(f"Applying {setUserTheme} {iniTheme}")
            sub.run(f"{setUserTheme} {iniTheme}", shell=True)

        except:
            pass

        if self.iniApplicationsPackages == "true":
            self.restore_applications_packages()

        else:
            self.restore_flatpaks()

    def restore_applications_packages(self):
        print("Installing applications packages...")
        try:             
            if self.packageManager == "rpm":
                # Distros like Fedora already has flatpak installed
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
                # First install flatphub if necessary
                ################################################################################
                # Install flatpak
                sub.run("sudo apt install -y flatpak", shell=True)
                # Install gnome software plugin flatpak
                sub.run("sudo apt install -y gnome-software-plugin-flatpak", shell=True)

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
                        print(f"flatpak install --system --noninteractive --assumeyes --or-update {output}")
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
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{varFolderName}/"):
                ###############################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"{output}")
                    config.write(configfile)

                ################################################################################
                # Restore flatpak data (var) folders from external device
                ################################################################################
                print(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{varFolderName}/{output} {src_flatpak_var_location}")
                sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{varFolderName}/{output} {src_flatpak_var_location}", shell=True)
                
        except:
            pass
        
        self.restore_flatpak_data_local()
        
    def restore_flatpak_data_local(self):
        print("Restoring flatpaks data (local)...")
        try:
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{localFolderName}/"):
                ###############################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"{output}")
                    config.write(configfile)

                ################################################################################
                # Restore flatpak data (var) folders from external device
                ################################################################################
                print(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{localFolderName}/{output} {src_flatpak_local_location}")
                sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{localFolderName}/{output} {src_flatpak_local_location}", shell=True)

        except:
            pass

        if self.iniFilesAndsFolders == "true":
            self.restore_home()

        else:
            self.end_backup()

    def restore_home(self):
        try:
            print("Restoring Home folders...")
            print(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                    f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/")
                    
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                    f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/"):

                ###############################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"{output}")
                    config.write(configfile)
                
                ###############################################################################
                # If output folder do not exist, create it
                if not os.path.exists(f"{homeUser}/{output}/"):
                    print(f"This {output} do not exist inside {homeUser}/ Home")
                    sub.run(f"{createCMDFolder} {homeUser}/{output}", shell=True)
                
                ###############################################################################
                # Restore Home folders
                print(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/"
                    f"{backupFolderName}/{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/"
                    f"{output}/ {homeUser}/{output}/")

                sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/"
                    f"{backupFolderName}/{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/"
                    f"{output}/ {homeUser}/{output}/", shell=True)
                ###############################################################################

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
        exit()

main = RESTORE()