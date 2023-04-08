#! /usr/bin/python3
from setup import *
from check_connection import *
from get_time import *
from get_backup_date import get_backup_date
from get_system_language import system_language
from languages import determine_days_language
from read_ini_file import UPDATEINIFILE

################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class CLI:
    def __init__(self):
        # Variables
        self.isSystemTrayActivated = None

        # Auto Packages
        self.downloadLoc = f"{homeUser}/Downloads"

        # Auto Packages List
        self.detectedPackagesDebList = []
        self.detectedPackagesRPMList = []
 
        self.debMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{debFolderName}"        
        self.rpmMainFolder = f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{rpmFolderName}"        


    def updates(self):
        try:
            print("Updating...")
            # get date folders inside backup device
            get_backup_date()

        except KeyError as error:
            print(error)
            print("Backup checker KeyError!")
            exit()

        self.is_system_tray_running()

    def is_system_tray_running(self):
        ################################################################################
        # Prevent multiples system tray running
        ################################################################################
        if str(mainIniFile.ini_system_tray()) == "true":
            if self.isSystemTrayActivated != None:
                sub.Popen(f"python3 {src_system_tray_py}", shell=True)
                self.isSystemTrayActivated = True

        self.check_connection()

    def check_connection(self):
        if is_connected(str(mainIniFile.ini_hd_name())):
            # Activate Auto Packages
            self.search_downloads()

    ################################################################################
    # Auto Packages
    ################################################################################
    def search_downloads(self):
        print("Searching new packages to be backup...")
        try:
            # Read Downloads folder for .deb
            for debs in os.listdir(self.debMainFolder):
                self.detectedPackagesDebList.append(debs)
        except:
            pass
        
        try:
            # Read Downloads folder for .rpm
            for rpms in os.listdir(self.rpmMainFolder):
                self.detectedPackagesRPMList.append(rpms)
        except:
            pass

        for output in os.listdir(self.downloadLoc):
            if output.endswith(".deb"):
                # Check if has not been already back up
                if output not in self.detectedPackagesDebList:
                    # Back up DEB
                    sub.run(f"{copyRsyncCMD} {self.downloadLoc}/{output} {self.debMainFolder}", shell=True)
                else:
                    print(f"{output} is already back up.")

            elif output.endswith(".rpm"):
                # Check if has not been already back up
                if output not in self.detectedPackagesRPMList:
                    # Back up DEB
                    sub.run(f"{copyRsyncCMD} {self.downloadLoc}/{output} {self.rpmMainFolder}", shell=True)
                else:
                    print(f"{output} is already back up.")
            else:
                print("No package to be backup...")

        # Clean list
        self.detectedPackagesDebList.clear()
        self.detectedPackagesRPMList.clear()
        
        self.check_the_date()

    def check_the_date(self):
        print("Checking dates...")
        # Is Multiple time per day enabled?
        if str(mainIniFile.ini_multiple_time_mode()) == "true":
            self.check_the_mode()

        else:
            if str(mainIniFile.day_name()).lower() in determine_days_language((system_language()))[0] and str(mainIniFile.ini_next_backup_sun()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()).lower() in determine_days_language((system_language()))[1] and str(mainIniFile.ini_next_backup_mon()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()).lower() in determine_days_language((system_language()))[2] and str(mainIniFile.ini_next_backup_tue()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()).lower() in determine_days_language((system_language()))[3] and str(mainIniFile.ini_next_backup_wed()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()).lower() in determine_days_language((system_language()))[4] and str(mainIniFile.ini_next_backup_thu()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()).lower() in determine_days_language((system_language()))[5] and str(mainIniFile.ini_next_backup_fri()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()).lower() in determine_days_language((system_language()))[6] and str(mainIniFile.ini_next_backup_sat()) == "true":
                self.check_the_mode()

            else:
                print("No back up for today.")

    def check_the_mode(self):
        print("Checking mode...")
        firstLetter = []
  
        # One time per day
        if str(mainIniFile.ini_one_time_mode()) == "true":
            # If current time is higher than time to backup
            if int(mainIniFile.current_time()) > int(mainIniFile.backup_time()):
                # If todays date can not be found inside the backup device's folders, backup was not made today.

                if today_date() not in get_backup_date():
                    # Call backup now
                    self.call_backup_now()

                else:
                    print(f"{appName} has already made a backup for today.")
                    
                    # Reset time left
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w') as configfile:
                        config.set('SCHEDULE', 'time_left', 'None')
                        config.write(configfile)

            elif int(mainIniFile.current_time()) == int(mainIniFile.backup_time()):
                self.call_backup_now()

            else:
                print("Waiting for the right time to backup...")
                # Calculate tine left to backup and so it on the main window as info
                calculateTimeLeft = int(mainIniFile.backup_time()) - int(mainIniFile.current_time()) + 60
                # Add to list and get first number str() to remove it after
                firstLetter.append(str(calculateTimeLeft))
                # Remove First Number str()
                if firstLetter[0][0] == "1":
                    calculateTimeLeft = str(calculateTimeLeft).removeprefix(firstLetter[0][0])
                    # Minutes calculation
                    if int(calculateTimeLeft) < 59:
                        # Write time left, so main window can get it
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('SCHEDULE', 'time_left', f'in {calculateTimeLeft} minutes...')
                            config.write(configfile)
                
                # Pass changing time left
                else:
                    # Write time left, so main window can get it
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w') as configfile:
                        config.set('SCHEDULE', 'time_left', 'None')
                        config.write(configfile)

                # Clean list
                firstLetter.clear()
        else:
            # Multiple time per day
            if str(mainIniFile.everytime()) == '60' and str(mainIniFile.current_time()) in timeModeHours60:
                if str(mainIniFile.ini_backup_now()) == "false":
                    self.call_backup_now()

            elif str(mainIniFile.everytime()) == '120' and str(mainIniFile.current_time()) in timeModeHours120:
                if str(mainIniFile.ini_backup_now()) == "false":
                    self.call_backup_now()

            elif str(mainIniFile.everytime()) == '240' and str(mainIniFile.current_time()) in timeModeHours240:
                if str(mainIniFile.ini_backup_now()) == "false":
                    self.call_backup_now()

            else:
                print("Waiting for the right time to backup...")

    def call_backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.set('SCHEDULE', 'time_left', 'Backing up...')
            config.write(configfile)

        sub.run(f"python3 {src_prepare_backup_py}", shell=True)

    def no_backup(self):
        print("No backup for today.")
        print("Updating INI file...")
        print("Exiting...")


mainIniFile = UPDATEINIFILE()
main = CLI()
# Exit program if auto_backup is false
while True:
    time.sleep(5)
    main.updates()

    ################################################################################
    # Prevent multiples backup checker running
    ################################################################################
    try:
        if str(mainIniFile.ini_automatically_backup()) == "false":
            print("Exiting backup checker...")
            # Turn backup now to OFF
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', 'false')
                config.write(configfile)

            break

    except Exception as error:
        print(error)
        break
    
exit()

