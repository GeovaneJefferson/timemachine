from setup import *
from read_ini_file import UPDATEINIFILE
from get_days_name import get_days_name
from check_connection import is_connected
from calculate_time_left_to_backup import calculate_time_left_to_backup
from backup_was_already_made import backup_was_already_made


# Handle signal
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


# Download folder location
DOWNLOADS_FOLDER_LOCATION = f"{HOME_USER}/Downloads"
# Found packages list
FOUND_DEB_PACKAGES_LIST = []
FOUND_RPM_PACKAGES_LIST = []


class CHECKER:
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
        if MAIN_INI_FILE.get_database_value('MODE', 'one_time_mode'):
            if MAIN_INI_FILE.day_name() == get_days_name() and MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
                self.take_action(True)

            elif MAIN_INI_FILE.day_name() == get_days_name() and MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
                self.take_action(True)

            elif MAIN_INI_FILE.day_name() == get_days_name() and MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
                self.take_action(True)

            elif MAIN_INI_FILE.day_name() == get_days_name() and MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
                self.take_action(True)

            elif MAIN_INI_FILE.day_name() == get_days_name() and MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
                self.take_action(True)

            elif MAIN_INI_FILE.day_name() == get_days_name() and MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
                self.take_action(True)

            elif MAIN_INI_FILE.day_name() == get_days_name() and MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
                self.take_action(True)
        # Multiple time per day
        else:
            self.take_action(False)

    # Take actions after check the date
    def take_action(self, one_time_per_day):
        # if not MAIN_INI_FILE.ini_unfinished_backup():
        # only one time per day
        if one_time_per_day:
            # If current time i higher or iqual to the 'saved' backup time to backup
            if MAIN_INI_FILE.current_time() >= MAIN_INI_FILE.backup_time_military():
                # If todays date can not be found inside backup device
                if not backup_was_already_made():
                    # Prepare backup
                    self.call_prepare_backup()
                else:
                    print("A backup was already made today.")

            # Calculate time left to backup
            else:
                calculate_time_left_to_backup()

        # Multiple time per day
        else:
            # 60 minutes
            if MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime') == f'{TIME1}' and str(MAIN_INI_FILE.current_time()) in MULTIPLE_TIME_OPTION1:
                self.call_prepare_backup()

            # 120 minutes
            elif MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime') == f'{TIME2}' and str(MAIN_INI_FILE.current_time()) in MULTIPLE_TIME_OPTION2:
                self.call_prepare_backup()

            # 240 minutes
            elif MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime') == f'{TIME3}' and str(MAIN_INI_FILE.current_time()) in MULTIPLE_TIME_OPTION3:
                self.call_prepare_backup()

    def call_prepare_backup(self):
        # TODO
        # Check if ini file is not locked, than write to it
        # Set time left to None
        # Set backup now to True, or create a file that shows that
        MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'True')
        MAIN_INI_FILE.set_database_value('SCHEDULE', 'time_left', 'None')

        # Call prepare backup
        print("Preparing the backup...")
        sub.run(f"python3 {src_prepare_backup_py}", shell=True)


if __name__ == '__main__':
    # Objects
    MAIN = CHECKER()
    MAIN_INI_FILE = UPDATEINIFILE()

    while True:
        try:
            if MAIN_INI_FILE.get_database_value('STATUS', 'automatically_backup'):
                if not MAIN_INI_FILE.get_database_value('STATUS', 'backing_up_now'):
                    print("Backup checker is running...")

                    # Get backup devices name and check connection
                    if is_connected(MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')):
                        # If previus backup is unfinished
                        if MAIN_INI_FILE.get_database_value('STATUS', 'unfinished_backup'):
                            MAIN.continue_interrupted_backup()

                        # Thread to check new packages at Downloads folders
                        # Search for new packages
                        MAIN.check_for_new_packages()

                        # Check dates
                        MAIN.check_the_dates()

                    else:
                        print("Backup device is not connected...")

                time.sleep(5)

            else:
                break

        except Exception:
            break

print("Automatically backup is OFF.")
exit()
