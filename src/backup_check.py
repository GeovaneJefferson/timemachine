#! /usr/bin/python3
from setup import *
from check_connection import *
from get_time import *
from get_backup_date import get_backup_date
from get_system_language import system_language
from languages import determine_days_language
from calculate_time_left_to_backup import calculate_time_left_to_backup
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
 
    def updates(self):
        try:
            print("Backup Checker is running...")
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
            for debs in os.listdir(mainIniFile.deb_main_folder()):
                self.detectedPackagesDebList.append(debs)
        except:
            pass
        
        try:
            # Read Downloads folder for .rpm
            for rpms in os.listdir(mainIniFile.rpm_main_folder()):
                self.detectedPackagesRPMList.append(rpms)
        except:
            pass

        for output in os.listdir(self.downloadLoc):
            if output.endswith(".deb"):
                if output.split("_")[0] in (f"{mainIniFile.deb_main_folder()}/{(output).split('_')[0]}"):
                    # Delete the old version before back up
                    for deleteOutput in os.listdir(mainIniFile.deb_main_folder()):
                        if deleteOutput.startswith(f"{output.split('_')[0]}"):
                            sub.run(f"rm -f {mainIniFile.deb_main_folder()}/{deleteOutput}",shell=True)
                    
                    # Now back up
                    sub.run(f"{copyRsyncCMD} {self.downloadLoc}/{output} {mainIniFile.deb_main_folder()}", shell=True)

            elif output.endswith(".rpm"):
                if output.split("_")[0] in (f"{mainIniFile.rpm_main_folder()}/{(output).split('_')[0]}"):
                    # Delete the old version before back up
                    for deleteOutput in os.listdir(mainIniFile.rpm_main_folder()):
                        if deleteOutput.startswith(f"{output.split('_')[0]}"):
                            sub.run(f"rm -f {mainIniFile.rpm_main_folder()}/{deleteOutput}",shell=True)
                    
                    # Now back up
                    sub.run(f"{copyRsyncCMD} {self.downloadLoc}/{output} {mainIniFile.rpm_main_folder()}", shell=True)
            else:
                print("No package to be backup...")

        # Clean list
        self.detectedPackagesDebList.clear()
        self.detectedPackagesRPMList.clear()
        
        self.check_the_date()

    def check_the_date(self):
        print("Checking dates...")
        if str(mainIniFile.ini_multiple_time_mode()) == "true":
            self.check_the_mode()

        else:
            if str(mainIniFile.day_name()) in determine_days_language((system_language()))[0] and str(mainIniFile.ini_next_backup_sun()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[1] and str(mainIniFile.ini_next_backup_mon()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[2] and str(mainIniFile.ini_next_backup_tue()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[3] and str(mainIniFile.ini_next_backup_wed()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[4] and str(mainIniFile.ini_next_backup_thu()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[5] and str(mainIniFile.ini_next_backup_fri()) == "true":
                self.check_the_mode()

            elif str(mainIniFile.day_name()) in determine_days_language((system_language()))[6] and str(mainIniFile.ini_next_backup_sat()) == "true":
                self.check_the_mode()

            else:
                print("No back up for today.")

    def check_the_mode(self):
        print("Checking mode...")
        if str(mainIniFile.ini_backup_now()) == "false":
            if str(mainIniFile.ini_one_time_mode()) == "true":
                if int(mainIniFile.current_time()) > int(mainIniFile.backup_time_military()):
                    if today_date() not in get_backup_date():
                        self.call_backup_now()
                    else:
                        print(f"{appName} has already made a backup for today.")
                        
                        # Reset time left
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('SCHEDULE', 'time_left', 'None')
                            config.write(configfile)

                elif int(mainIniFile.current_time()) == int(mainIniFile.backup_time_military()):
                    self.call_backup_now()

                else:
                    print("Waiting for the right time to backup...")
                    # TODO
                    calculate_time_left_to_backup()
                 
            else:
                # Multiple time per day
                if str(mainIniFile.everytime()) == '60' and str(mainIniFile.current_time()) in timeModeHours60:
                    self.call_backup_now()

                elif str(mainIniFile.everytime()) == '120' and str(mainIniFile.current_time()) in timeModeHours120:
                    self.call_backup_now()

                elif str(mainIniFile.everytime()) == '240' and str(mainIniFile.current_time()) in timeModeHours240:
                    self.call_backup_now()

                else:
                    print("Waiting for the right time to backup...")

    def call_backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        sub.run(f"python3 {src_prepare_backup_py}", shell=True)

    def no_backup(self):
        print("No backup for today.")
        print("Updating INI file...")
        print("Exiting...")


mainIniFile = UPDATEINIFILE()
main = CLI()

while True:
    time.sleep(5)
    main.updates()

    ################################################################################
    # Prevent multiples backup checker running
    ################################################################################
    try:
        if mainIniFile.ini_automatically_backup() == "false":
            print("Exiting backup checker...")

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

