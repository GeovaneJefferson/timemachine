from setup import *
# Read ini file
from read_ini_file import UPDATEINIFILE
# Languages
from languages import determine_days_language
from get_system_language import system_language
# Connection
from check_connection import is_connected
# Calculation
from calculate_time_left_to_backup import calculate_time_left_to_backup
# Time
from get_time import today_date
# Date
from get_backup_date import get_backup_date


# Handle signal
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


# Download folder location
DOWNLOADS_FOLDER_LOCATION=f"{HOME_USER}/Downloads"
# Found packages list
FOUND_DEB_PACKAGES_LIST=[]
FOUND_RPM_PACKAGES_LIST=[]


class CHECKER:
    def __init__(self):
        pass

    # Check for previus interrupted backup
    def continue_interrupted_backup(self):
        # Call backup now .py
        sub.run(f"python3 {src_backup_now_py}", shell=True)

    # Check for new .deb, .rpm etc. inside Downloads folder and back up
    def check_for_new_packages(self):
        print("Searching new packages inside Downloads folder...")

        # Search for .deb packages inside Downloads folder
        for package in os.listdir(DOWNLOADS_FOLDER_LOCATION):
            if package.endswith(".deb"):
                # Check if the found .deb is has not alredy been back up
                if package.split("_")[0] in (f"{MAIN_INI_FILE.deb_main_folder()}/{(package).split('_')[0]}"):
                    # Add to list, so it wont back up every time the same file
                    if package not in FOUND_DEB_PACKAGES_LIST:
                        FOUND_DEB_PACKAGES_LIST.append(package)

                        # Delete the old version before back up
                        for old_package in os.listdir(MAIN_INI_FILE.deb_main_folder()):
                            if old_package.startswith(f"{package.split('_')[0]}"):
                                # Delete old package
                                sub.run(f"rm -f {MAIN_INI_FILE.deb_main_folder()}/{old_package}",shell=True)

                        # backup the found package
                        sub.run(f"{COPY_RSYNC_CMD} {DOWNLOADS_FOLDER_LOCATION}/{package} {MAIN_INI_FILE.deb_main_folder()}", shell=True)

            # Search for .rpm packages inside Downloads folder
            if package.endswith(".rpm"):
                # Check if the found .rpm is has not alredy been back up
                if package.split("_")[0] in (f"{MAIN_INI_FILE.rpm_main_folder()}/{(package).split('_')[0]}"):
                    # Add to list, so it wont back up every time the same file
                    if package not in FOUND_RPM_PACKAGES_LIST:
                        FOUND_RPM_PACKAGES_LIST.append(package)

                        # Delete the old version before back up
                        for deleteOutput in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
                            if deleteOutput.startswith(f"{package.split('_')[0]}"):
                                # Delete old package
                                sub.run(f"rm -f {MAIN_INI_FILE.rpm_main_folder()}/{deleteOutput}",shell=True)

                        # backup the found package
                        sub.run(f"{COPY_RSYNC_CMD} {DOWNLOADS_FOLDER_LOCATION}/{package} {MAIN_INI_FILE.rpm_main_folder()}", shell=True)

    # Check the dates for backup, one or multiple times per day
    def check_the_dates(self):
        # One time per day
        if MAIN_INI_FILE.ini_one_time_mode():
            if str(MAIN_INI_FILE.day_name()) in determine_days_language((system_language()))[0] and str(MAIN_INI_FILE.ini_next_backup_sun()):
                self.take_action(True)

            elif str(MAIN_INI_FILE.day_name()) in determine_days_language((system_language()))[1] and str(MAIN_INI_FILE.ini_next_backup_mon()):
                self.take_action(True)

            elif str(MAIN_INI_FILE.day_name()) in determine_days_language((system_language()))[2] and str(MAIN_INI_FILE.ini_next_backup_tue()):
                self.take_action(True)

            elif str(MAIN_INI_FILE.day_name()) in determine_days_language((system_language()))[3] and str(MAIN_INI_FILE.ini_next_backup_wed()):
                self.take_action(True)

            elif str(MAIN_INI_FILE.day_name()) in determine_days_language((system_language()))[4] and str(MAIN_INI_FILE.ini_next_backup_thu()):
                self.take_action(True)

            elif str(MAIN_INI_FILE.day_name()) in determine_days_language((system_language()))[5] and str(MAIN_INI_FILE.ini_next_backup_fri()):
                self.take_action(True)

            elif str(MAIN_INI_FILE.day_name()) in determine_days_language((system_language()))[6] and str(MAIN_INI_FILE.ini_next_backup_sat()):
                self.take_action(True)

        # Multiple time per day
        else:
            self.take_action(False)

    # Take actions after check the date
    def take_action(self, one_time_per_day):
        # if not MAININIFILE.ini_unfinished_backup():
        # only one time per day
        if one_time_per_day:
            # If current time i higher or iqual to the 'saved' backup time to backup
            if MAIN_INI_FILE.current_time() >= MAIN_INI_FILE.backup_time_military():
                # If todays date can not be found inside backup device
                if today_date() not in get_backup_date():
                    # Prepare backup
                    self.call_prepare_backup()

            # Calculate time left to backup
            else:
                calculate_time_left_to_backup()

        # Multiple time per day
        else:
            # 60 minutes
            if MAIN_INI_FILE.ini_everytime() == f'{TIME1}' and str(MAIN_INI_FILE.current_time()) in MULTIPLE_TIME_OPTION1:
                self.call_prepare_backup()

            # 120 minutes
            elif MAIN_INI_FILE.ini_everytime() == f'{TIME2}' and str(MAIN_INI_FILE.current_time()) in MULTIPLE_TIME_OPTION2:
                self.call_prepare_backup()

            # 240 minutes
            elif MAIN_INI_FILE.ini_everytime() == f'{TIME3}' and str(MAIN_INI_FILE.current_time()) in MULTIPLE_TIME_OPTION3:
                self.call_prepare_backup()

    def call_prepare_backup(self):
        # TODO
        # Check if ini file is not locked, than write to it
        # Set time left to None
        # Set backup now to True, or create a file that shows that
        config=configparser.ConfigParser()
        config.read(SRC_USER_CONFIG)
        with open(SRC_USER_CONFIG, 'w') as configfile:
            config.set('STATUS', 'backing_up_now', 'true')
            config.set('SCHEDULE', 'time_left', 'None')
            config.write(configfile)

        # Call prepare backup
        print("Preparing the backup...")
        sub.run(f"python3 {src_prepare_backup_py}", shell=True)


if __name__ == '__main__':
    # Objects
    MAIN=CHECKER()
    MAIN_INI_FILE=UPDATEINIFILE()

    while True:
        try:
            if MAIN_INI_FILE.ini_automatically_backup():
                print("Backup checker is running...")

                # Get backup devices name and check connection
                if is_connected(MAIN_INI_FILE.ini_hd_name()):
                    # If previus backup is unfinished
                    if MAIN_INI_FILE.ini_unfinished_backup():
                        MAIN.continue_interrupted_backup()

                    # Thread to check new packages at Downloads folders
                    # Search for new packages
                    MAIN.check_for_new_packages()

                    # Check dates
                    MAIN.check_the_dates()

                # Wait
                time.sleep(5)

            else:
                break

        except Exception as e:
            print("Backup Checker ERROR:", e)
            break

# Quit
exit()
