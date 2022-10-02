#! /usr/bin/python3
from logging import exception
from setup import *
# TODO
# Error when external is full
# Maybe error occours when app check space needed for the backup

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
            self.alreadyClearTrash = False
            
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

            self.create_base_folders()

        except KeyError as error:
            print(error)
            exit()

    def create_base_folders(self):
        # Set backup now to True
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', "true")
            config.write(configfile)
            
        try:
            ################################################################################
            # Create TMB (Base)
            ################################################################################
            if not os.path.exists(self.createBaseFolder):
                sub.run(f"{createCMDFolder} {self.createBaseFolder}", shell=True)

            ################################################################################
            # Create backup folder
            ################################################################################
            if not os.path.exists(self.createBackupFolder):
                print("TMB folder inside external, was created.")
                sub.run(f"{createCMDFolder} {self.createBackupFolder}", shell=True)

            ################################################################################
            # Create Application folder
            ################################################################################
            if not os.path.exists(self.applicationMainFolder):
                print("Application folder inside external, was created.")
                sub.run(f"{createCMDFolder} {self.applicationMainFolder}", shell=True)

            ################################################################################
            # Create Icon folder
            ################################################################################
            if not os.path.exists(self.iconsMainFolder):
                print("Icon folder inside external, was created.")
                sub.run(f"{createCMDFolder} {self.iconsMainFolder}", shell=True)

            ################################################################################
            # Create Cursor folder
            ################################################################################
            if not os.path.exists(self.cursorMainFolder):
                print("Cursor folder inside external, was created.")
                sub.run(f"{createCMDFolder} {self.cursorMainFolder}", shell=True)
            
            ################################################################################
            # Create Theme folder
            ################################################################################
            if not os.path.exists(self.themeMainFolder):
                print("Theme folder inside external, was created.")
                sub.run(f"{createCMDFolder} {self.themeMainFolder}", shell=True)

            ################################################################################
            # Create RPM folder (Folder to manual place rpms apps)
            ################################################################################
            if not os.path.exists(self.rpmMainFolder):
                sub.run(f"{createCMDFolder} {self.rpmMainFolder}", shell=True)   
            
            ################################################################################
            # Create Deb folder (Folder to manual place deb apps)
            ################################################################################
            if not os.path.exists(self.debMainFolder):
                sub.run(f"{createCMDFolder} {self.debMainFolder}", shell=True)   

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        self.get_system_settings_size()
    
    def get_system_settings_size(self):
        self.iconInside = False
        self.themeInside = False

        print("Checking size of System Settings...")
     
        self.systemSettingsFolderToBackupSizeList=[]
     
        # Get current use icon by user
        userCurrentIcon = os.popen(getUserIcon)
        userCurrentIcon = userCurrentIcon.read().strip()
        userCurrentIcon = userCurrentIcon.replace("'", "")

        ################################################################################
        # Get icon folders size
        ################################################################################
        # Try to find the current icon inside /usr/share/icons
        try:
            # Get folder size fomr /usr/share/icons
            getIconSize = os.popen(f"du -s /usr/share/icons/{userCurrentIcon}")
            getIconSize = getIconSize.read().strip("\t").strip("\n").replace(f"/usr/share/icons/{userCurrentIcon}", "").replace("\t", "")
            getIconSize = int(getIconSize)
            self.iconInside = True

        except:
            try:
                # If can not be found inside /usr/share/icons, try .icons in Home
                # Get folder size
                getIconSize = os.popen(f"du -s {homeUser}/.icons/{userCurrentIcon}")
                getIconSize = getIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.icons/{userCurrentIcon}", "").replace("\t", "")
                getIconSize = int(getIconSize)
                self.iconInside = True

            except:
                pass

        ################################################################################
        # Get theme folders size
        ################################################################################
        # Get current use theme by user
        userCurrentTheme = os.popen(getUserTheme)
        userCurrentTheme = userCurrentTheme.read().strip()
        userCurrentTheme = userCurrentTheme.replace("'", "")

        # Try to find the current icon inside /usr/share/icons
        try:
            # Get folder size fomr /usr/share/icons
            getThemeSize = os.popen(f"du -s /usr/share/themes/{userCurrentTheme}")
            getThemeSize = getThemeSize.read().strip("\t").strip("\n").replace(f"/usr/share/themes/{userCurrentTheme}", "").replace("\t", "")
            getThemeSize = int(getThemeSize)
            self.themeInside = True

        except:
            try:
                # If can not be found inside /usr/share/icons, try .icons in Home
                # Get folder size
                getThemeSize = os.popen(f"du -s {homeUser}/.themes/{userCurrentTheme}")
                getThemeSize = getThemeSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.themes/{userCurrentTheme}", "").replace("\t", "")
                getThemeSize = int(getThemeSize)
                self.themeInside = True

            except:
                pass

        
        # Check if Time Machine found icon and/or theme to be backup
        if self.iconInside:
            # Add icon size to list
            self.systemSettingsFolderToBackupSizeList.append(getIconSize)
        
        if self.themeInside:
            # Add theme size to list
            self.systemSettingsFolderToBackupSizeList.append(getThemeSize)

        if self.iconInside or self.themeInside:
            # Sum of system settings
            self.totalSystemSettingsFolderToBackupSize = int(sum(self.systemSettingsFolderToBackupSizeList))
        
        self.get_home_folders_size()

    def get_home_folders_size(self):
        print("Checking size of Home folders...")
        ################################################################################
        # Get folders size
        ################################################################################
        self.homeFolderToBackupSizeList=[]
        self.homeFolderToBeBackup=[]
        for output in self.iniFolders:  # Get folders size before back up to external
            # Capitalize first letter
            output = output.capitalize()
            # Can output be found inside Users Home?
            try:
                os.listdir(f"{homeUser}/{output}")
            except:
                # Lower output first letter
                output = output.lower() # Lower output first letter
            # Get folder size
            getSize = os.popen(f"du -s {homeUser}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{homeUser}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            # Add to list
            self.homeFolderToBackupSizeList.append(getSize)
            # Add output inside self.homeFolderToBeBackup
            self.homeFolderToBeBackup.append(output)

        self.calculate_home_folders()

    def calculate_home_folders(self):
        print("Calculating Home folders...")
        ################################################################################
        # Get external maximum size
        ################################################################################
        self.externalMaxSize = os.popen(f"df --output=size {self.iniExternalLocation}")
        self.externalMaxSize = self.externalMaxSize.read().strip().replace("1K-blocks", "").replace("Size", "").replace(
            "\n", "").replace(" ", "")
        self.externalMaxSize = int(self.externalMaxSize)

        ################################################################################
        # Get external used space
        ################################################################################
        self.usedSpace = os.popen(f"df --output=used {self.iniExternalLocation}")
        self.usedSpace = self.usedSpace.read().strip().replace("1K-blocks", "").replace("Used", "").replace(
            "\n", "").replace(" ", "")
        self.usedSpace = int(self.usedSpace)

        ################################################################################
        # Calculattions
        ################################################################################
        # Sum of all folders (from INI file) to be backup
        self.totalHomeFoldersToBackupSize = sum(self.homeFolderToBackupSizeList)
        # Calculate free space
        self.freeSpace = int(self.externalMaxSize - self.usedSpace)

        # If user allowed backup Flatpak Data, calculate flatpaks folders size
        # Backup Flatpaks Data will auto enable "allow Flatpaks names".
        if self.iniAllowFlatpakData == "false":
            self.condition_to_continue()
        else:
          self.calculate_flatpak_folders()

    def calculate_flatpak_folders(self):
        print("Checking size of folders (Flatpak)...")
        try:
            ################################################################################
            # Get flatpak (var/app) folders size
            ################################################################################
            self.flatpakVarSizeList=[]
            self.flatpakLocalSizeList=[]
            self.flatpakVarToBeBackup=[]
            self.flatpakLocaloBeBackup=[]
            for output in os.listdir(src_flatpak_var_location):  # Get folders size before back up to external
                # Get size of flatpak folder inside var/app/
                print(f"du -s {src_flatpak_var_location}/{output}")

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
                self.flatpakVarToBeBackup.append(f"{src_flatpak_var_location}/{output}")

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
                self.flatpakLocaloBeBackup.append(f"{src_flatpak_local_location}/{output}")

        except ValueError as error:
            print(error)
            exit()

        self.condition_to_continue()
    
    def condition_to_continue(self):
        # This will check if Home + Flatpaks folders to backup has enough space to continue
        # with the backup process.
        print("Checking folders conditions (size)...")
        while True:
            ################################################################################
            # Home conditions to continue with the backup
            ################################################################################
            # Home + Icon + Theme
            if self.totalHomeFoldersToBackupSize + self.totalSystemSettingsFolderToBackupSize >= self.freeSpace:
                print("Not enough space for new backup")
                print("Old folders will be deleted, to make space for the new ones.")
                print("Please wait...")

                ################################################################################
                # First try to clean .Trash inside the external device
                ################################################################################
                if not self.alreadyClearTrash:
                    print(f"Deleting .trash...")
                    sub.run(f"rm -rf {self.iniExternalLocation}/.Trash-1000", shell=True)
                    # set AlreadyClearTrash to True
                    self.alreadyClearTrash = True
                    # TODO
                    # Return to calculate all folders to be backup
                    self.get_system_settings_size()
                
                ################################################################################
                # Get available dates inside TMB
                # Delete based in Dates
                ################################################################################
                try:
                    dateFolders = []
                    for output in os.listdir(self.checkDateInsideBackupFolder):
                        if not "." in output:
                            dateFolders.append(output)
                            dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

                    ################################################################################
                    # Delete oldest folders
                    ################################################################################
                    # Only deletes if exist more than one date folder inside
                    # Will return to the top, if free space is not enought, so app can delete more old folders
                    if len(dateFolders) > 1:
                        ################################################################################
                        # Write to INI file
                        ################################################################################
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_add_info', "Deleting old backups...")
                            config.write(configfile)

                        # Action
                        print(f"Deleting {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{dateFolders[-1]}...")
                        sub.run(f"rm -rf {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{dateFolders[-1]}", shell=True)
                        # TODO
                        # Return to calculate all folders to be backup
                        self.get_system_settings_size()
                
                    else:
                        # Set notification_id to 2
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_id', "2")
                            # Turn backup now OFF
                            config.set('BACKUP', 'backup_now', 'false')
                            config.set('INFO', 'notification_add_info', "Please, manual delete file(s)/folder(s) inside "
                                    f"your backup device, to make space for {appName}'s backup!")
                            config.write(configfile)

                        print(f"Please, manual delete file(s)/folder(s) inside your backup device, to make space for {appName}'s "
                        "backup!")
                        exit()

                except FileNotFoundError as error:
                    print("Error trying to delete old backups!")
                    print(error)
                    exit()

            else:
                if self.iniAllowFlatpakData == "true":
                    print("AllowFlatpakData is enabled!")
                    ################################################################################
                    # Flatpaks conditions to continue with the backup
                    ################################################################################
                    # Sum Home folder + Flapatk var/app/ + Flapatk .local/share/flatpak
                    homePlusSystemSettingsPlusFlatpakToBackupSize = sum(
                        self.homeFolderToBackupSizeList + 
                        self.systemSettingsFolderToBackupSizeList +
                        self.flatpakVarSizeList + 
                        self.flatpakLocalSizeList)

                    ################################################################################
                    # Condition
                    ################################################################################
                    # Total fodlers to backup: HOme + flatpak(var/app) + flatpak + (.local/share/flatpak)
                    # FreSpace = External device free space

                    if homePlusSystemSettingsPlusFlatpakToBackupSize >= self.freeSpace:
                        # If Home folders to backup is good to continue, then check flatpaks folders
                        print("External has space enough to backup Home folders,")
                        # External devices has not space enough to backup FLatpaks folders
                        print(f"but not Flatpaks folders.")

                        # Calculate KBytes to MB or GB
                        spaceNeeded = homePlusSystemSettingsPlusFlatpakToBackupSize
                        # Condition
                        if len(str(spaceNeeded)) <= 6:
                            spaceNeeded = spaceNeeded / 1000 # Convert to MB
                            print(f"Total Space (Home + Flatpaks) needed: {(spaceNeeded):.1f} MB")
                            addToNotificationInfo = f"{(spaceNeeded):.1f} MB"

                        elif len(str(spaceNeeded)) > 6:
                            spaceNeeded = spaceNeeded / 1000000 # Convert to GB
                            print(f"Total Space (Home + Flatpaks) needed: {(spaceNeeded):.1f} GB")
                            addToNotificationInfo = f"{(spaceNeeded):.1f} GB"

                        else:
                            print(f"Total Space (Home + Flatpaks) needed: {spaceNeeded} KB")
                            addToNotificationInfo = f"{spaceNeeded} KB"

                        # Send notification to user telling the error
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_id', "2")
                            config.set('INFO', 'notification_add_info', f"Space needed: {addToNotificationInfo}")
                            config.write(configfile)

                        # Signal
                        signal_exit()

                    else:
                        break

                else:
                    print("External has space enough to backup Home + Flatpaks installed names.")
                    print("External has space enough to continue.")
                    self.create_pre_folders_inside_external()

        self.create_pre_folders_inside_external()

    def create_pre_folders_inside_external(self):
        print("Creating pre folders...")
        try:
            ################################################################################
            # Create folder with DATE
            ################################################################################
            print("Creating folder with date...")
            if not os.path.exists(self.dateFolder):
                sub.run(f"{createCMDFolder} {self.dateFolder}", shell=True)  # Create folder with date

            ################################################################################
            # Create folder with TIME
            ################################################################################
            print("Creating folder with time...")
            if not os.path.exists(self.timeFolder):
                sub.run(f"{createCMDFolder} {self.timeFolder}", shell=True)

            ################################################################################
            # Create application folder
            ################################################################################
            if self.iniAllowFlatpakData == "true":
                # Create inside external "Var" Folder
                if not os.path.exists(self.applicationVarFolder):
                    sub.run(f"{createCMDFolder} {self.applicationVarFolder}", shell=True)  

                # Create inside external "Local" Folder
                if not os.path.exists(self.applicationLocalFolder):
                    sub.run(f"{createCMDFolder} {self.applicationLocalFolder}", shell=True)  

            ################################################################################
            # Create flatpak text
            ################################################################################
            if not os.path.exists(self.flatpakTxtFile):
                print("Flatpak file was created.")
                sub.run(f"{createCMDFile} {self.flatpakTxtFile}", shell=True)   

            ################################################################################
            # Create wallpaper folder
            ################################################################################
            if not os.path.exists(self.wallpaperMainFolder):
                sub.run(f"{createCMDFolder} {self.wallpaperMainFolder}", shell=True)   

        except FileNotFoundError as error:
            # Call error function 
            error_trying_to_backup(error)

        self.get_user_background()

    def get_user_background(self):
        ################################################################################
        # Detect color scheme
        ################################################################################
        getColorScheme = os.popen(detectThemeMode)
        getColorScheme = getColorScheme.read().strip().replace("'", "")
            
        # Check if user DE is in the supported list
        count = 0
        for _ in supported:
            if supported[count] == self.iniUserOS:
                # Light theme
                if getColorScheme == "prefer-light":
                    # Get current wallpaper
                    self.getWallpaper = os.popen(getGnomeWallpaper)
                    self.getWallpaper = self.getWallpaper.read().strip().replace("file://", "").replace("'", "")
                
                else:
                    # Get current wallpaper (Dark)
                    self.getWallpaper = os.popen(getGnomeWallpaperDark)
                    self.getWallpaper = self.getWallpaper.read().strip().replace("file://", "").replace("'", "")
            
                # If it has comma
                if "," in self.getWallpaper:
                    self.getWallpaper = str(self.getWallpaper.replace(",", "\, "))
                
                # Remove spaces if exist
                if " " in self.getWallpaper:
                    self.getWallpaper = str(self.getWallpaper.replace(" ", "\ "))
                
                # Remove / at the end if exist
                if self.getWallpaper.endswith("/"):
                    self.getWallpaper = str(self.getWallpaper.rsplit("/", 1))
                    self.getWallpaper = "".join(str(self.getWallpaper))
                    self.getWallpaper = str(self.getWallpaper.strip().replace("[", "").replace("'", ""))
                    self.getWallpaper = str(self.getWallpaper.replace("]", "").replace(",", ""))
                
                # After one supported item was found, continue
                continue

            else:
                print("No supported DE found to back up the wallpaper.")
                self.write_flatpak_file()
            count += 1

        self.backup_user_wallpaper()

    def backup_user_wallpaper(self):
        # Replace wallpaper inside the folder, only allow 1
        # If is not empty
        insideWallpaperFolder = os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/")
        # If it has image inside the folder
        if insideWallpaperFolder:
            # Delete all image inside wallpaper folder
            for image in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/"):
                print(f"Deleting {self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/{image}...")
                sub.run(f"rm -rf {self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/{image}", shell=True)
        
        print(f"{copyCPCMD} {self.getWallpaper} {self.wallpaperMainFolder}/")
        sub.run(f"{copyCPCMD} {self.getWallpaper} {self.wallpaperMainFolder}/", shell=True) 
        
        # Set zoom mode
        sub.run(f"{zoomGnomeWallpaper}", shell=True) 
       
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
            for output in self.homeFolderToBeBackup:
                ###############################################################################
                # Write current save file name to INI file
                # so it can be show on main window (mainwindow.py)
                # This way, user will have a feedback to what
                # is happening.
                # Write current folder been backup to INI file
                ###############################################################################
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"Backing up: {output}")
                    config.write(configfile)

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
            for output in self.flatpakVarToBeBackup: # For folders inside self.flatpakVarToBeBackup
                ###############################################################################
                # Write current save file name to INI file
                # so it can be show on main window (gui.py)
                # This way, user will have a feedback to what
                # is happening.
                # Write current folder been backup to INI file
                ###############################################################################
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"Backing up: {output}")
                    config.write(configfile)

                ###############################################################################
                # Copy the Flatpak var/app folders
                ###############################################################################
                print(f"{copyCPCMD} {(self.flatpakVarToBeBackup[count])} {self.applicationVarFolder}")
                sub.run(f"{copyCPCMD} {(self.flatpakVarToBeBackup[count])} {self.applicationVarFolder}", shell=True)
                
                # print(f"{copyRsyncCMD} {(self.flatpakVarToBeBackup[count])} {self.applicationVarFolder}")
                # sub.run(f"{copyRsyncCMD} {(self.flatpakVarToBeBackup[count])} {self.applicationVarFolder}", shell=True)
                ###############################################################################
                # Copy the Flatpak var/app folders
                ###############################################################################
                count += 1

            ################################################################################
            # Start Flatpak (.local/share/flatpak) backup
            ################################################################################
            count = 0
            for output in self.flatpakLocaloBeBackup: # For folders inside self.flatpakLocalToBeBackup
                ###############################################################################
                # Write current save file name to INI file
                # so it can be show on main window (gui.py)
                # This way, user will have a feedback to what
                # is happening.
                # Write current folder been backup to INI file
                ###############################################################################
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'feedback_status', f"Backing up: {output}")
                    config.write(configfile)

                ###############################################################################
                # Copy the Flatpak var/app folders
                ###############################################################################
                print(f"{copyRsyncCMD} {(self.flatpakLocaloBeBackup[count])} {self.applicationLocalFolder}")
                sub.run(f"{copyRsyncCMD} {(self.flatpakLocaloBeBackup[count])} {self.applicationLocalFolder}", shell=True)
                ###############################################################################
                # Copy the Flatpak var/app folders
                ###############################################################################
                count += 1

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        self.backup_icons()

    def backup_icons(self):
        ################################################################################
        # Get current use icon by user
        ################################################################################
        userCurrentIcon = os.popen(getUserIcon)
        userCurrentIcon = userCurrentIcon.read().strip()
        userCurrentIcon = userCurrentIcon.replace("'", "")

        ################################################################################
        # Only one icon inside the backup folder
        ################################################################################
        insideIconFolder = os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{iconFolderName}/")
        if insideIconFolder:
            # Delete all image inside wallpaper folder
            for icon in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{iconFolderName}/"):
                # If is not the same name, remove it, and backup the new one
                if icon != userCurrentIcon:
                    print(f"Deleting {self.iniExternalLocation}/{baseFolderName}/{iconFolderName}/{icon}...")
                    sub.run(f"rm -rf {self.iniExternalLocation}/{baseFolderName}/{iconFolderName}/{icon}", shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            # Save icon information
            config.set('INFO', 'icon', f"{userCurrentIcon}")
            config.set('INFO', 'feedback_status', f"Backing up: icons")
            config.write(configfile)

        # Get users /usr/share/icons
        # Try to find the current icon inside /usr/share/icons
        # If folder is empty, use CP to copy
        if not insideIconFolder:
            try:
                # USR/SHARE
                os.listdir(f"/usr/share/icons/{userCurrentIcon}")
                sub.run(f"{copyCPCMD} /usr/share/icons/{userCurrentIcon} {self.iconsMainFolder}", shell=True)
            except:
                # .THEMES
                sub.run(f"{copyCPCMD} {homeUser}/.icons/{userCurrentIcon} {self.iconsMainFolder}", shell=True)
            else:
                pass

        else:
            try:
                # USR/SHARE
                os.listdir(f"/usr/share/icons/{userCurrentIcon}")
                sub.run(f"{copyRsyncCMD} /usr/share/icons/{userCurrentIcon} {self.iconsMainFolder}", shell=True)
            except: 
                # Try to find the current icon inside /home/user/.icons
                sub.run(f"{copyRsyncCMD} {homeUser}/.icons/{userCurrentIcon} {self.iconsMainFolder}", shell=True)
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
            config.set('INFO', 'feedback_status', f"Backing up: cursor")
            config.write(configfile)

        # Get users /usr/share/icons
        # Try to find the current cursor inside /usr/share/icons
        # If folder is empty, use CP to copy
        if not insidecursorFolder:
            try:
                # USR/SHARE
                # Try to find
                os.listdir(f"/usr/share/icons/{userCurrentcursor}/")
                sub.run(f"{copyCPCMD} /usr/share/icons/{userCurrentcursor} {self.cursorMainFolder}", shell=True)

            except:
                try:
                    # .Icons
                    # Try to find
                    sub.run(f"{copyCPCMD} {homeUser}/.icons/{userCurrentcursor} {self.cursorMainFolder}", shell=True)

                except:
                    pass
        else:
            try:
                # USR/SHARE/ICONS
                # Try to find
                os.listdir(f"{homeUser}/.icons/{userCurrentcursor}/")
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
            config.set('INFO', 'feedback_status', f"Backing up: theme")
            config.write(configfile)

        ################################################################################
        # Try to find the current theme inside /home/user/.theme
        ################################################################################
        # Create gnome-shell inside theme current theme folder
        ################################################################################
        if not os.path.exists(f"{self.iniExternalLocation}/{baseFolderName}/"
            f"{themeFolderName}/{userCurrentTheme}/{gnomeShellFolder}"):

            print("Gnome-shell folder inside external, was created.")
            sub.run(f"{createCMDFolder} {self.iniExternalLocation}/{baseFolderName}/"
                f"{themeFolderName}/{userCurrentTheme}/{gnomeShellFolder}", shell=True)
    
        # Get users /usr/share/theme
        # Try to find the current theme inside /usr/share/theme
        # If folder is empty, use CP to copy
        if not insideThemeFolder:
            try:
                # USR/SHARE
                os.listdir(f"/usr/share/themes/{userCurrentTheme}/")
                sub.run(f"{copyCPCMD} /usr/share/themes/{userCurrentTheme} {self.themeMainFolder}", shell=True)
            except:
                # .THEMES
                sub.run(f"{copyCPCMD} {homeUser}/.themes/{userCurrentTheme} {self.themeMainFolder}", shell=True)
            else:
                pass

        else:
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
            # Update last backup time
            config.set('INFO', 'latest', f'{self.dayName}, {self.currentHour}:{self.currentMinute}')
            # Change system tray color to white (Normal)
            config.set('INFO', 'notification_id', "0")
            # Reset Main Window information
            config.set('INFO', 'notification_add_info', "")
            # Clean current back up folder from Main Window
            config.set('INFO', 'feedback_status', "")
            # Set checker runner to False
            config.set('BACKUP', 'checker_running', "true")
            config.write(configfile)

        ################################################################################
        # After backup is done
        ################################################################################
        print("Backup is done!")
        print("Sleeping for 60 seconds...")
        time.sleep(60)  # Wait x, so if finish fast, won't repeat the backup :D
        exit()


main = BACKUP()

