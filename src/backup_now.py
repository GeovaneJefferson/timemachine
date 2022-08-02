#! /usr/bin/python3
from setup import *

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

            # TMB folder
            self.createTMBFolder = f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
            # RPM main folder
            self.rpmMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{rpmFolderName}"
            # Wallpaper main folder
            self.wallpaperMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}"
            # Application main folder
            self.applicationMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}"
            # Application main Var folder
            self.applicationVarFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{varFolderName}"
            # Application main Local folder
            self.applicationLocalFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{localFolderName}"
            # Date folder
            self.dateFolder = f"{self.createTMBFolder}/{self.dateDay}-{self.dateMonth}-{self.dateYear}"
            # Time folder
            self.timeFolder = f"{self.createTMBFolder}/{self.dateDay}-{self.dateMonth}-{self.dateYear}/{self.currentHour}-{self.currentMinute}"

            # Flatpak txt file
            self.flatpakTxtFile = f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}"

            self.create_TMB()

        except KeyError as error:
            print(error)
            exit()

    def create_TMB(self):
        # Set backup now to True
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', "true")
            config.write(configfile)
            
        try:
            ################################################################################
            # Create TMB
            ################################################################################
            if not os.path.exists(self.createTMBFolder):
                sub.run(f"{createCMDFolder} {self.iniExternalLocation}/{baseFolderName}", shell=True)

            # Create {self.secondsFolderName}
            if not os.path.exists(self.createTMBFolder):
                print("TMB folder inside external, was created.")
                sub.run(f"{createCMDFolder} {self.createTMBFolder}", shell=True)

        except FileNotFoundError as error:
            error_trying_to_backup(error)

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

        ################################################################################
        print("All folders size sum : ", self.totalHomeFoldersToBackupSize)
        print("External maximum size:   ", self.externalMaxSize)
        print(f"External used space:   ", self.usedSpace)
        print("External free size:   ", self.freeSpace)

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
            print("Still checking...")
            ################################################################################
            # Home conditions to continue with the backup
            ################################################################################
            if self.totalHomeFoldersToBackupSize >= self.freeSpace:
                print("Not enough space for new backup")
                print("Old folders will be deleted, to make space for the new ones.")
                print("Please wait...")

                ################################################################################
                # Get available dates inside TMB
                ################################################################################
                try:
                    dateFolders = []
                    for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"):
                        if not "." in output:
                            print(output)
                            dateFolders.append(output)
                            dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

                    print(f"Date available: {dateFolders}")
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

                    else:
                        # Set notification_id to 2
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_id', "2")
                            # Turn backup now OFF
                            config.set('BACKUP', 'backup_now', 'false')
                            config.set('INFO', 'notification_add_info', "Please, manual delete file(s)/folder(s) inside "
                                "your backup device, to make space for Time Machine's backup!")
                            config.write(configfile)

                        print("Please, manual delete file(s)/folder(s) inside your backup device, to make space for Time "
                        "Machine's backup!")
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
                    homePlusFlatpakToBackupSize = sum(self.homeFolderToBackupSizeList + self.flatpakVarSizeList + self.flatpakLocalSizeList)

                    ################################################################################
                    # Condition
                    ################################################################################
                    # Total fodlers to backup: HOme + flatpak(var/app) + flatpak + (.local/share/flatpak)
                    # FreSpace = External device free space

                    if homePlusFlatpakToBackupSize >= self.freeSpace:
                        # If Home folders to backup is good to continue, then check flatpaks folders
                        print("External has space enough to backup Home folders,")
                        # External devices has not space enough to backup FLatpaks folders
                        print(f"but not Flatpaks folders.")

                        # Calculate KBytes to MB or GB
                        spaceNeeded = homePlusFlatpakToBackupSize
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
                    print("External has space enough to backup Home + Flatpaks folders.")
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
                # Create inside base "application" folder
                if not os.path.exists(self.applicationMainFolder):
                    sub.run(f"{createCMDFolder} {self.applicationMainFolder}", shell=True)  

                self.applicationMainFolder
                # Create inside external "Var" Folder
                if not os.path.exists(self.applicationVarFolder):
                    sub.run(f"{createCMDFolder} {self.applicationVarFolder}", shell=True)  

                # Create inside external "Local" Folder
                if not os.path.exists(self.applicationLocalFolder):
                    sub.run(f"{createCMDFolder} {self.applicationLocalFolder}", shell=True)  

            ################################################################################
            # Create application folder
            ################################################################################
            if not os.path.exists(self.flatpakTxtFile):
                print("Flatpak file was created.")
                sub.run(f"{createCMDFile} {self.flatpakTxtFile}", shell=True)   

            ################################################################################
            # Create wallpaper folder
            ################################################################################
            if not os.path.exists(self.wallpaperMainFolder):
                sub.run(f"{createCMDFolder} {self.wallpaperMainFolder}", shell=True)   

            ################################################################################
            # Create RPM folder (Folder to manual place rpms apps)
            ################################################################################
            if not os.path.exists(self.self.rpmMainFolder):
                sub.run(f"{createCMDFolder} {self.self.rpmMainFolder}", shell=True)   

        except FileNotFoundError as error:
            # Call error function 
            error_trying_to_backup(error)

        self.get_user_background()

    def get_user_background(self):
        # Get current user's background (Gnome)
        self.userDE = os.popen(getUserDE)
        self.userDE = self.userDE.read().strip().lower()

        # Get current wallpaper
        if "gnome" in self.userDE:
            self.getWallpaper = os.popen(getGnomeWallpaper)
            self.getWallpaper = self.getWallpaper.read().strip().replace("file://", "").replace("'", "")
            # Remove spaces if exist
            if " " in self.getWallpaper:
                self.getWallpaper = str(self.getWallpaper.replace(" ", "\ "))

            self.backup_user_wallpaper()

        else:
            self.write_flatpak_file()

    def backup_user_wallpaper(self):
        print("Backing up current wallpaper...")
        # Replace wallpaper inside the folder, only allow 1
        # If is not empty
        insideWallpaperFolder = os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/")
        # If it has image inside the folder
        if insideWallpaperFolder:
            # Delete all image inside wallpaper folder
            for image in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/"):
                print(f"Deleting {self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/{image}...")
                sub.run(f"rm -rf {self.iniExternalLocation}/{baseFolderName}/{wallpaperFolderName}/{image}", shell=True)
        
        sub.run(f"{copyRsyncCMD} {self.getWallpaper} {self.wallpaperMainFolder}/", shell=True) 
                
        # Condition
        ################################################################################
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
            with open(self.flatpakTxtFile, 'w') as configfile:  # Set auto backup to true
                for output in os.popen("flatpak list --columns=app --app"):
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
                # Copy the Home files/folders
                ###############################################################################
                print(f"{copyRsyncCMD} {homeUser}/{output} {self.timeFolder}")
                sub.run(f"{copyRsyncCMD} {homeUser}/{output} {self.timeFolder}", shell=True)
                ###############################################################################
                # Copy the Home files/folders
                ###############################################################################

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        if self.iniAllowFlatpakData == "true":
            self.backup_flatpak()
        else:
            self.end_backup()

    def backup_flatpak(self):
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
                print(f"{copyRsyncCMD} {(self.flatpakVarToBeBackup[count])} {self.applicationVarFolder}")
                sub.run(f"{copyRsyncCMD} {(self.flatpakVarToBeBackup[count])} {self.applicationVarFolder}", shell=True)
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
                sub.run(f"{copyRsyncCMD} {(self.flatpakLocaloBeBackup[count])} {self.applicationLocalFolder}"
                    , shell=True)
                ###############################################################################
                # Copy the Flatpak var/app folders
                ###############################################################################
                count += 1

        except FileNotFoundError as error:
            error_trying_to_backup(error)

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
        # sub.Popen(f"python3 {src_backup_check_py}", shell=True)
        exit()


main = BACKUP()

