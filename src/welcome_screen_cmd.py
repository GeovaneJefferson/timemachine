#! /usr/bin/python3
from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class RESTORE:
    def __init__(self):
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
                if not "." in output:
                    self.latestDateFolder.append(output)
                    self.latestDateFolder.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
                    # Stop at the newest date folder

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

        self.restore_home()
        
    def restore_home(self):
        if self.iniFilesAndsFolders == "true":
            print("Restoring Home folders...")
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/"):
                # Restore Home folders
                print(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                    f"{self.latestDateFolder[0]}/{self.latestTimeFolder[0]}/{output}/ {homeUser}/{output}/")

                sub.run(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/", shell=True)

        self.restore_flatpak_apps()

    def restore_flatpak_apps(self):
        if self.iniApplicationNames == "true":
            print("Installing flatpaks apps...")
            try: 
                # Restore flatpak apps
                with open(f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}", "r") as read_file:
                    read_file = read_file.readlines()

                    for output in read_file:
                        output = output.strip()
                        print(f"flatpak install -y --noninteractive {output}")
                        sub.run(f"flatpak install -y --noninteractive {output}", shell=True)
            except:
                pass

        self.restore_flatpak_data()

    def restore_flatpak_data(self):
        # ################################################################################
        # # Something inside?
        # ################################################################################
        # dummyList = []
        # # Check inside Var
        # print(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{varFolderName}/")
        # for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{varFolderName}/"):
        #     dummyList.append(output)

        # if not dummyList:
        #     print("Empty...")
        #     # Disable Application (data)
            
        if self.iniApplicationData == "true":
            print("Restoring flatpaks data...")
            try:
                ################################################################################
                # Restore flatpak data (var) folders from external device
                ################################################################################
                print(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{varFolderName}/ {src_flatpak_var_location}")
                sub.run(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{varFolderName}/ {src_flatpak_var_location}", shell=True)
                
                ################################################################################
                # Restore flatpak data (.local/share) folders from external device
                ################################################################################
                print(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{localFolderName}/ {src_flatpak_local_location}")
                sub.run(f"{copyCmd} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{applicationFolderName}/{localFolderName}/ {src_flatpak_local_location}", shell=True)
            
            except:
                pass

            exit()

            
main = RESTORE()