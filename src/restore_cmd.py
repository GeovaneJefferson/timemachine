#! /usr/bin/python3
from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class RESTORE:
    def __init__(self):
        # Update INI file
        with open(src_user_config, 'w') as configfile:
            # Restore
            config.set('RESTORE', 'is_restore_running', "true")
            config.write(configfile)

        self.read_ini_file()

    def read_ini_file(self):
        # Read file
        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniFolder = config.options('FOLDER')
        # Restore
        self.iniApplicationNames = config['RESTORE']['applications_name']
        self.iniApplicationData = config['RESTORE']['application_data']
        self.iniFilesAndsFolders = config['RESTORE']['files_and_folders']

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
                print(output)
                if not "." in output:
                    print(output)
                    self.latestDateFolder.append(output)
                    self.latestDateFolder.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        except FileNotFoundError as error:
                ################################################################################
                # Set notification_id to 6
                ################################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'notification_id', "6")
                    config.write(configfile)

                print("Error trying to delete old backups!")
                print(error)
                sub.run(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification
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
        
        if self.iniFilesAndsFolders == "true":
            self.get_home_folders_size()
        # If flatpak names is true, flatpak data is also true
        elif self.iniApplicationNames == "true":
            self.get_flatpak_data_size()

    def get_home_folders_size(self):
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

        if self.iniApplicationData == "true":
            self.get_flatpak_data_size()
        else:
            self.restore_home()

    def get_flatpak_data_size(self):
        print("Checking size of flatpak (var)...")
        ################################################################################
        # Get folders size
        ################################################################################
        self.flatpakVarSizeList=[]
        self.flatpakLocalSizeList=[]
        self.flatpakVarToBeRestore=[]
        self.flatpakLocaloBeRestore=[]
        
        for output in os.listdir(src_flatpak_var_location): 
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

        if self.iniFilesAndsFolders == "true":
            self.restore_home()
        else:
            # If allow flatpak names is true; flatpak data is also true
            self.restore_flatpak_apps(countForRuleOf3=1)

    def restore_home(self, countForRuleOf3=1):
        try:
            if self.iniFilesAndsFolders == "true":
                ################################################################################
                # self.Percent100 for the "Rule of 3" calculation
                ################################################################################
                # Home folders + Flatpak data (var/app) + .local/share/flatpak
                if self.iniApplicationData == "true": 
                    self.percent100 = len(self.homeFolderToBeRestore) + len(self.flatpakLocaloBeRestore) + len(self.flatpakVarToBeRestore)
                # Only Home folders 
                else:
                    self.percent100 = len(self.homeFolderToBeRestore)
   
                print("Restoring Home folders...")
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
                    print(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/{output}/ {homeUser}/{output}/")
                    sub.run(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/{output}/ {homeUser}/{output}/", shell=True)
                    ###############################################################################
                    
                    # Calculate percent of the process ("rule of 3")
                    calculateRuleOf3 = ((self.percent100 - countForRuleOf3) * 100 / self.percent100)
                    calculateRuleOf3 = int(100 - calculateRuleOf3)
                    
                    # Update the current percent of the process INI file
                    with open(src_user_config, 'w') as configfile:
                        config.set('INFO', 'current_percent', f"{(calculateRuleOf3):.0f}")
                        config.write(configfile)
                    
                    ###############################################################################
                    # Add 1 to self.countForRuleOf3
                    countForRuleOf3 += 1
        except:
            pass

        self.restore_flatpak_apps(countForRuleOf3)

    def restore_flatpak_apps(self, countForRuleOf3):
        if self.iniApplicationNames == "true":
            print("Installing flatpaks apps...")
            try: 
                # Restore flatpak apps
                with open(f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}", "r") as read_file:
                    read_file = read_file.readlines()

                    for output in read_file:
                        output = output.strip()
                        
                        # Add to list
                        self.percent100 = len(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                            f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/") 
                        
                        ###############################################################################
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'feedback_status', f"{output}")
                            config.write(configfile)

                        ###############################################################################
                        print(f"flatpak install -y --user --noninteractive {output}")
                        sub.run(f"flatpak install -y --user --noninteractive {output}", shell=True)
                        ###############################################################################
                        
                        # Calculate percent of the process ("rule of 3")
                        calculateRuleOf3 = ((self.percent100 - countForRuleOf3) * 100 / self.percent100)
                        calculateRuleOf3 = int(100 - calculateRuleOf3)
                        
                        # Update the current percent of the process INI file
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'current_percent', f"{(calculateRuleOf3):.0f}")
                            config.write(configfile)
                        
                        ###############################################################################
                        # Add 1 to self.countForRuleOf3
                        countForRuleOf3 += 1
            except:
                pass

        self.restore_flatpak_data(countForRuleOf3)

    def restore_flatpak_data(self, countForRuleOf3):
        if self.iniApplicationData == "true":
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
                    print(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{varFolderName}/{output} {src_flatpak_var_location}")
                    sub.run(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{varFolderName}/{output} {src_flatpak_var_location}", shell=True)
                    
                    ###############################################################################
                    # Calculate percent of the process ("rule of 3")
                    calculateRuleOf3 = ((self.percent100 - countForRuleOf3) * 100 / self.percent100)
                    calculateRuleOf3 = int(100 - calculateRuleOf3)

                    ###############################################################################
                    # Update the current percent of the process INI file
                    ###############################################################################
                    with open(src_user_config, 'w') as configfile:
                        config.set('INFO', 'current_percent', f"{(calculateRuleOf3):.0f}")
                        config.write(configfile)

                    ###############################################################################
                    # Add 1 to countForRuleOf3
                    countForRuleOf3 += 1

            except:
                pass
            
            self.restore_flatpak_data_local(countForRuleOf3)
        
        self.end_backup()

    def restore_flatpak_data_local(self, countForRuleOf3):
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
                print(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{localFolderName}/{output} {src_flatpak_local_location}")
                sub.run(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{localFolderName}/{output} {src_flatpak_local_location}", shell=True)
                ###############################################################################
                # Calculate percent of the process ("rule of 3")
                calculateRuleOf3 = ((self.percent100 - countForRuleOf3) * 100 / self.percent100)
                calculateRuleOf3 = int(100 - calculateRuleOf3)

                ###############################################################################
                # Update the current percent of the process INI file
                ###############################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'current_percent', f"{(calculateRuleOf3):.0f}")
                    config.write(configfile)

                ###############################################################################
                # Add 1 to countForRuleOf3
                countForRuleOf3 += 1

        except:
            pass

        self.end_backup()
            
    def end_backup(self):
        print("Ending restoring...")
        ###############################################################################
        # After all done, feedback_status = "" and set current_percent = 0
        ###############################################################################
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'notification_id', "2")
            config.set('INFO', 'notification_add_info', "")
            config.set('INFO', 'feedback_status', "")
            config.set('INFO', 'current_percent', "0")
            # Restore
            config.set('RESTORE', 'is_restore_running', "false")
            config.write(configfile)

        ################################################################################
        # After backup is done
        ################################################################################
        sub.Popen(f"python3 {src_notification}", shell=True)
        print("Restoring is done!")
        exit()

main = RESTORE()