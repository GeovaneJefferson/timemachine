#! /usr/bin/python3
from setup import *
from get_backup_folders import *
from get_time import *
from get_user_wallpaper import *

################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class PREPAREBACKUP:
    def __init__(self):
        print("Preparing the backup...")
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

            # Time folder
            self.timeFolder = f"{self.createBackupFolder}/{str(get_date_time())}"
            # Date folder
            self.dateFolder = f"{self.createBackupFolder}/{str(get_date())}"
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

        self.create_base_folders()

    def create_base_folders(self):
        try:
            ################################################################################
            # Create TMB (Base)
            ################################################################################
            if not os.path.exists(self.createBaseFolder):
                print(f"{createCMDFolder} {self.createBaseFolder}")
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

        self.has_icon_inside()
    
    def has_icon_inside(self):
        print("Checking icons...")
        self.iconInside = False

        # Get current use icon by user
        userCurrentGnomeIcon = os.popen(getUserIcon)
        userCurrentGnomeIcon = userCurrentGnomeIcon.read().strip()
        userCurrentGnomeIcon = userCurrentGnomeIcon.replace("'", "")

        ################################################################################
        # Get icon folders size
        ################################################################################
        # Try to find the current icon inside /usr/share/icons
        try:
            # Get folder size fomr /usr/share/icons
            self.getIconSize = os.popen(f"du -s /usr/share/icons/{userCurrentGnomeIcon}")
            self.getIconSize = self.getIconSize.read().strip("\t").strip("\n").replace(f"/usr/share/icons/{userCurrentGnomeIcon}", "").replace("\t", "")
            self.getIconSize = int(self.getIconSize)
            print("Icon found inside usr/share/icons")
            self.iconInside = True

        except :
            try:
                # If can not be found inside /usr/share/icons, try .icons in Home
                # Get folder size
                self.getIconSize = os.popen(f"du -s {homeUser}/.icons/{userCurrentGnomeIcon}")
                self.getIconSize = self.getIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.icons/{userCurrentGnomeIcon}", "").replace("\t", "")
                self.getIconSize = int(self.getIconSize)
                print("Icon found inside .icons")
                self.iconInside = True

            except:
                pass

        self.has_theme_inside()

    def has_theme_inside(self):
        self.themeInside = False
        print("Checking themes...")
        try:
            ################################################################################
            # Get theme folders size
            ################################################################################
            # Get current use theme by user
            userCurrentTheme = os.popen(getUserTheme)
            userCurrentTheme = userCurrentTheme.read().strip()
            userCurrentTheme = userCurrentTheme.replace("'", "")

            # Try to find the current icon inside /usr/share/icons
            # Get folder size fomr /usr/share/icons
            self.getThemeSize = os.popen(f"du -s /usr/share/themes/{userCurrentTheme}")
            self.getThemeSize = self.getThemeSize.read().strip("\t").strip("\n").replace(f"/usr/share/themes/{userCurrentTheme}", "").replace("\t", "")
            self.getThemeSize = int(self.getThemeSize)
            self.themeInside = True
        except:
            try:
                # If can not be found inside /usr/share/icons, try .icons in Home
                # Get folder size
                self.getThemeSize = os.popen(f"du -s {homeUser}/.themes/{userCurrentTheme}")
                self.getThemeSize = self.getThemeSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.themes/{userCurrentTheme}", "").replace("\t", "")
                self.getThemeSize = int(self.getThemeSize)
                self.themeInside = True

            except:
                pass
        
        self.add_to_backup_list()

    def add_to_backup_list(self):
        self.systemSettingsFolderToBackupSizeList=[]
        # Check if Time Machine found icon and/or theme to be backup
        if self.iconInside:
            # Add icon size to list
            self.systemSettingsFolderToBackupSizeList.append(self.getIconSize)
        
        if self.themeInside:
            # Add theme size to list
            self.systemSettingsFolderToBackupSizeList.append(self.getThemeSize)

        if self.iconInside or self.themeInside:
            # Sum of system settings
            self.totalSystemSettingsFolderToBackupSize = int(sum(self.systemSettingsFolderToBackupSizeList))
   
        self.calculate_home_folders()

    def calculate_home_folders(self):
        print("Checking size of Home folders and size...")

        if self.iniAllowFlatpakData == "true":
            self.calculate_flatpak_folders()
        else:
            self.condition_to_continue()

    def calculate_flatpak_folders(self):
        print("Checking size of folders (Flatpak)...")

        self.condition_to_continue()
    
    def condition_to_continue(self):
        # This will check if Home + Flatpaks folders to backup has enough space to continue
        # with the backup process.
        print("Checking folders conditions (size)...")
        while True:
            ################################################################################
            # Home conditions to continue with the backup
            ################################################################################
            # Home + Icon + Theme + aditional number, just for safety
            if (int(total_home_folders_to_backup()) + 
                self.totalSystemSettingsFolderToBackupSize + 1500000 >= 
                int(free_space_home_folders())):

                print("Not enough space for new backup")
                print("Old folders will be deleted, to make space for the new ones.")
                print("Please wait...")

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
                        
                        # First try to clean .Trash inside the external device
                        # print(f"Deleting .trash too...")
                        # sub.run(f"rm -rf {self.iniExternalLocation}/.Trash-1000", shell=True)

                        # Return to calculate all folders to be backup
                        self.calculate_home_folders()
                
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
                print("enough space to continue...")
                if self.iniAllowFlatpakData == "true":
                    ################################################################################
                    # Flatpaks conditions to continue with the backup
                    ################################################################################
                    # Sum Home folder + Flapatk var/app/ + Flapatk .local/share/flatpak
                    homePlusSystemSettingsPlusFlatpakToBackupSize = sum(
                        int(home_folders_size()) + 
                        int(flatpak_var_size()) + 
                        int(flatpak_local_size()) +
                        self.systemSettingsFolderToBackupSizeList)

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

        # Run prepare_backup first
        sub.Popen(f"python3 {src_backup_now}",shell=True)
        exit()


if __name__ == '__main__':
    main = PREPAREBACKUP()

