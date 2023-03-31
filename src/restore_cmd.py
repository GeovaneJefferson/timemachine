#! /usr/bin/python3
from setup import *
from get_user_de import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)

################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


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
        print("read")
        # Read file
        config = configparser.ConfigParser()
        config.read(src_user_config)

        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniFolder = config.options('FOLDER')
        # Restore
        self.iniFlatpakApplications = config['RESTORE']['applications_flatpak_names']
        self.iniApplicationsPackages = config['RESTORE']['applications_packages']
        self.iniFlatpakApplicationData = config['RESTORE']['applications_data']
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

        # Proceed to home
        if self.iniFilesAndsFolders == "true":
            self.get_home_backup_folders()

        # Proceed to application
        elif self.iniApplicationsPackages == "true":
            self.restore_applications_packages()

        # Proceed to flatpak files (Local and Data)
        elif self.iniFlatpakApplicationData == "true":
            self.get_flatpak_data_size()
        
        # Proceed to wallpaper
        elif self.iniSystemSettings == "true":
            self.apply_users_saved_wallpaper()

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
        print("Restoring users wallpaper...")
        dummyList = []
        try:
            ################################################################################
            # Get users Package Manager
            ################################################################################
            get_user_de()

            # Check if a wallpaper can be found
            for wallpaper in os.listdir(f"{self.wallpaperMainFolder}/"):
                dummyList.append(wallpaper)
            
            # If has a wallpaper to restore and self.iniSystemSettings == "true":
            if self.iniSystemSettings == "true":
                if dummyList: 
                    # Retore users wallpaper to Pictures
                    for image in os.listdir(f"{self.iniExternalLocation}/"
                        f"{baseFolderName}/{wallpaperFolderName}/"):
                        # Copy the wallpaper to the user's Pictures
                        sub.run(f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/"
                            f"{wallpaperFolderName}/{image} {homeUser}/Pictures", shell=True)

                    # Check if user DE is in the supported list to Automatically apply
                    ################################################################
                    count = 0
                    for _ in supportedOS:
                        # Activate wallpaper option
                        if supportedOS[count] in str(get_user_de):
                            # Detect color scheme
                            getColorScheme = os.popen(detectThemeMode)
                            getColorScheme = getColorScheme.read().strip().replace("'", "")
                            
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

                        elif str(get_user_de) == "kde":
                            print("Restoring users wallpaper (KDE)...")
                            # Apply to KDE desktop
                            os.popen("""
                                    dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
                                var Desktops = desktops();
                                for (i=0;i<Desktops.length;i++) {
                                        d = Desktops[i];
                                        d.wallpaperPlugin = "org.kde.image";
                                        d.currentConfigGroup = Array("Wallpaper",
                                                                    "org.kde.image",
                                                                    "General");
                                        d.writeConfig("Image", "file://%s/Pictures/%s");
                                }'
                                    """ % (homeUser, image))
                        else:
                            pass

                    # Restore icon
                    self.restore_icons()

                else:
                    # Restore icon
                    self.restore_icons()

            else:
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
            
            # # If has something to restore
            if self.somethingToRestoreInIcon:
                ################################################################################
                # Create .local/share/.icons inside home user
                ################################################################################
                if not os.path.exists(f"{homeUser}/.local/share/icons"):
                    print("Creating .local/share/icons inside home user...")
                    print(f"{createCMDFolder} {homeUser}.local/share/icons")
                    sub.run(f"{createCMDFolder} {homeUser}.local/share/icons", shell=True)   

                # Copy icon from the backup to local/share/icons folder
                sub.run(f"{copyRsyncCMD} {self.iconsMainFolder}/ {homeUser}.local/share/icons", shell=True)
                
                # Check if user DE is in the supported list
                ################################################################
                count = 0
                for _ in supportedOS:
                    # Activate wallpaper option
                    if supportedOS[count] in str(get_user_de):
                        # Continue only if has a theme inside to restore
                        # Apply icon
                        print(f"Applying {setUserIconCMD} {icon}")
                        try:
                            # USR/SHARE
                            os.listdir(f"/usr/share/icons/{icon}/")
                            sub.run(f"{setUserIconCMD} {icon}", shell=True)
                        except:
                            # .icons
                            sub.run(f"{setUserIconCMD} {icon}", shell=True)
                        else:
                            pass

        except:
            print("No icon to restore.")
            pass

        self.restore_cursor()

    def restore_cursor(self):
        print("Restoring cursor...")

        self.somethingToRestoreInCursor = []
        # Check for cursor to be restored
        for cursor in os.listdir(f"{self.cursorMainFolder}/"):
            self.somethingToRestoreInCursor.append(cursor)
            print(cursor)

        # If has something to restore
        if self.somethingToRestoreInCursor:
            # Copy icon from the backup to .icon folder
            sub.run(f"{copyRsyncCMD} {self.cursorMainFolder}/ {homeUser}.local/share/icons", shell=True)

            # Check if user DE is in the supported list
            count = 0
            for _ in supportedOS:
                # Activate wallpaper option
                if supportedOS[count] in str(get_user_de):
                    # Continue only if has a theme inside to restore
                    # Apply cursor
                    print(f"Applying {setUserCursorCMD} {cursor}")
                    try:
                        # USR/SHARE
                        os.listdir(f"/usr/share/icons/{cursor}/")
                        sub.run(f"{setUserCursorCMD} {cursor}", shell=True)
                    except:
                        try:
                            # .cursor
                            sub.run(f"{setUserCursorCMD} {cursor}", shell=True)
                        except:
                            pass

        self.restore_theme()

    def restore_theme(self):
        print("Restoring theme...")

        self.somethingToRestoreInTheme = []
        # Check for theme to be restored
        for theme in os.listdir(f"{self.themeMainFolder}/"):
            self.somethingToRestoreInTheme.append(theme)
            print(theme)

        # If has something to restore
        if self.somethingToRestoreInTheme:
            ################################################################################
            # Create .themes inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.themes"):
                print("Creating .local/share/themes inside home user...")
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/themes", shell=True)   

            # Copy theme from the backup to .theme folder
            sub.run(f"{copyRsyncCMD} {self.themeMainFolder}/ {homeUser}/.local/share/themes", shell=True)
            # Check if user DE is in the supported list
            """
            lookandfeeltool -a theme name or location (KDE)
            """
            count = 0
            for _ in supportedOS:
                # Activate wallpaper option
                if supportedOS[count] in str(get_user_de):
                    # Continue only if has a theme inside to restore
                    # Apply theme
                    print(f"Applying {setUserThemeCMD} {theme}")
                    try:
                        # USR/SHARE
                        os.listdir(f"/usr/share/themes/{theme}/")
                        sub.run(f"{setUserThemeCMD} {theme}", shell=True)
                    except:
                        # .cursor
                        sub.run(f"{setUserThemeCMD} {theme}", shell=True)
                    else:
                        pass

        
        if self.iniApplicationsPackages == "true":
            self.restore_applications_packages()

        else:
            self.restore_flatpaks()

    def restore_applications_packages(self):
        # Dummy Exclude applications list
        dummyExcludeAppsList = []

        # Exclude application location
        self.excludeAppsLoc = (f"{self.iniExternalLocation}/{baseFolderName}/"
                f"{applicationFolderName}/{src_exclude_applications}")

        # Read exclude applications from .exclude-application.txt
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(self.excludeAppsLoc, 'r') as readExclude:
            readExclude = readExclude.read().split("\n")
            dummyExcludeAppsList.append(f"{readExclude}")

        print("Installing applications packages...")
        try:             
            if self.packageManager == f"{rpmFolderName}":
                ################################################################################
                # Restore RPMS
                ################################################################################
                for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
                    f"{applicationFolderName}/{rpmFolderName}"):
                    print(f"{installRPM} {self.iniExternalLocation}/{baseFolderName}/"
                        f"{applicationFolderName}/{rpmFolderName}/{output}")

                    # Install only if output if not in the exclude app list
                    if output not in str(dummyExcludeAppsList):
                        # Install rpms applications
                        sub.run(f"{installRPM} {self.iniExternalLocation}/{baseFolderName}/"
                            f"{applicationFolderName}/{rpmFolderName}/{output}", shell=True)
            
            elif self.packageManager == f"{debFolderName}":
                ################################################################################
                # Restore DEBS
                ################################################################################
                for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
                        f"{applicationFolderName}/{debFolderName}"):

                    # Install only if output if not in the exclude app list
                    if output not in str(dummyExcludeAppsList):
                        print(f"{installDEB} {self.iniExternalLocation}/{baseFolderName}/"
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
                        sub.run(f"{flatpakInstallCommand} {output}", shell=True)
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