#! /usr/bin/python3
from setup import *
from check_connection import *
from get_time import *

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

    def updates(self):
        try:
            print("Updating...")
            config = configparser.ConfigParser()
            config.read(src_user_config)

            # INI file
            self.iniHDName = config['EXTERNAL']['name']
            self.iniExternalLocation = config['EXTERNAL']['hd']
            self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
            self.iniLatestDate = config['INFO']['latest']

            # Dates
            self.iniScheduleSun = config['SCHEDULE']['sun']
            self.iniScheduleMon = config['SCHEDULE']['mon']
            self.iniScheduleTue = config['SCHEDULE']['tue']
            self.iniScheduleWed = config['SCHEDULE']['wed']
            self.iniScheduleThu = config['SCHEDULE']['thu']
            self.iniScheduleFri = config['SCHEDULE']['fri']
            self.iniScheduleSat = config['SCHEDULE']['sat']

            self.iniBackupNow = config['BACKUP']['backup_now']
            self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
            self.iniOneTimePerDay = config['MODE']['one_time_mode']
            self.iniMultipleTimePerDay = config['MODE']['more_time_mode']
            self.iniEverytime = config['SCHEDULE']['everytime']
            self.iniNextHour = config['SCHEDULE']['hours']
            self.ininextMinute = config['SCHEDULE']['minutes']

            # Day
            self.dayName = datetime.now()
            self.dayName = self.dayName.strftime("%a")

            # Time
            now = datetime.now()
            self.currentHour = now.strftime("%H")
            self.currentMinute = now.strftime("%M")
            self.totalCurrentTime = self.currentHour + self.currentMinute
            self.totalNextTime = self.iniNextHour + self.ininextMinute

            # Check date inside backup folder
            self.checkDateInsideBackupFolder = f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"

        except KeyError as error:
            print(error)
            print("Backup checker KeyError!")
            # Wait x seconds and try again
            time.sleep(5)
            self.updates()

        self.is_system_tray_running()

    def is_system_tray_running(self):
        ################################################################################
        # Prevent multiples system tray running
        ################################################################################
        if self.iniSystemTray == "true":
            if self.isSystemTrayActivated != None:
                # Call system tray
                sub.Popen(f"python3 {src_system_tray}", shell=True)
                # Set sysmtem activated to True
                self.isSystemTrayActivated = True

        self.check_connection()

    def check_connection(self):
        is_connected(self.iniHDName)

        if is_connected(self.iniHDName):
            self.check_the_date()

    def check_the_date(self):
        print("Checking dates...")
        # Is Multiple time per day enabled?
        if self.iniMultipleTimePerDay == "true":
            self.check_the_mode()

        else:
            if self.dayName == "Sun" and self.iniScheduleSun == "true":
                self.check_the_mode()

            elif self.dayName == "Mon" and self.iniScheduleMon == "true":
                self.check_the_mode()

            elif self.dayName == "Tue" and self.iniScheduleTue == "true":
                self.check_the_mode()

            elif self.dayName == "Wed" and self.iniScheduleWed == "true":
                self.check_the_mode()

            elif self.dayName == "Thu" and self.iniScheduleThu == "true":
                self.check_the_mode()

            elif self.dayName == "Fri" and self.iniScheduleFri == "true":
                self.check_the_mode()

            elif self.dayName == "Sat" and self.iniScheduleSat == "true":
                self.check_the_mode()

            else:
                print("No back up for today.")

    def check_the_mode(self):
        print("Checking mode...")
        dateFolders = []
        for output in os.listdir(self.checkDateInsideBackupFolder):
            dateFolders.append(output)
            dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        # One time per day
        if self.iniOneTimePerDay == "true":
            # If current time is higher than time to backup
            if self.totalCurrentTime > self.totalNextTime:
                # If todays date can not be found inside the backup device's folders, backup was not made today.
                if today_date() not in dateFolders:
                    # Call backup now
                    self.call_backup_now()

                else:
                    print(f"{appName} has already made a backup for today.")
                    print("Time to back up has passed")

            elif self.totalCurrentTime == self.totalNextTime:
                self.call_backup_now()

            else:
                print("Waiting for the right time to backup...")

        else:
            print("Multiple time per day")

            if self.iniEverytime == '60' and self.totalCurrentTime in timeModeHours60:
                if self.iniBackupNow == "false":
                    self.call_backup_now()

            elif self.iniEverytime == '120' and self.totalCurrentTime in timeModeHours120:
                if self.iniBackupNow == "false":
                    self.call_backup_now()

            elif self.iniEverytime == '240' and self.totalCurrentTime in timeModeHours240:
                if self.iniBackupNow == "false":
                    self.call_backup_now()

            else:
                print("Waiting for the right time to backup...")

    def call_backup_now(self):
        print("Back up will start shortly...")

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        # Call backup now
        sub.run(f"python3 {src_backup_now}", shell=True)

    def no_backup(self):
        print("No backup for today.")
        print("Updating INI file...")
        print("Exiting...")


main = CLI()
# Exit program if auto_backup is false
while True:
    time.sleep(5)
    main.updates()

    ################################################################################
    # Prevent multiples backup checker running
    ################################################################################
    try:
        if main.iniAutomaticallyBackup == "false":
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

