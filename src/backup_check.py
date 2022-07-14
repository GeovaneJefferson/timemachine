#! /usr/bin/python3
from setup import *


class CLI:
    def __init__(self):
        # Variables
        self.isSystemTrayActivated = None
        # Signal
        signal.signal(signal.SIGINT, self.signal_exit)
        signal.signal(signal.SIGTERM, self.signal_exit)

    def updates(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        ################################################################################
        # INI file
        ##############
        self.iniHDName = config['EXTERNAL']['name']
        self.iniBackupNowChecker = config['BACKUP']['backup_now']
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
        # 
        self.iniFirstStartup = config['BACKUP']['first_startup']
        self.iniBackupNowChecker = config['BACKUP']['backup_now']
        self.iniAutoBackup = config['BACKUP']['auto_backup']
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

    def is_system_tray_running(self):
        ################################################################################
        # Prevent multiples system tray App
        ################################################################################
        if self.iniSystemTray == "true" and self.isSystemTrayActivated != None and self.iniFirstStartup == "false":
            self.isSystemTrayActivated = True
            # Call system tray
            sub.Popen(f"python3 {src_system_tray}", shell=True)

    def check_connection(self):  
        ################################################################################
        # Check for external in media/
        ################################################################################
        try:
            # Check for user backup device inside Media
            os.listdir(f'{media}/{userName}/{self.iniHDName}')
            print(f'Devices found inside {media}/{self.iniHDName}')
            self.check_the_date()

        except FileNotFoundError:
            ################################################################################
            # Check for external in run/
            ################################################################################
            try:
                # Check for user backup device inside Run
                os.listdir(f'{run}/{userName}/{self.iniHDName}')
                print(f"Devices found inside {run}")
                self.check_the_date()

            except FileNotFoundError as error:
                print(error)
                ################################################################################
                # No saved backup device was found inside Media or Run
                # Write error to INI File
                ################################################################################
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'notification_id', "3")
                    config.set('INFO', 'notification_add_info', f"{error}")
                    config.write(configfile)

                print("No external device found.")
                print(f"Please, connect the external device, so next time, {appName} will be able to backup.")
                pass

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
                self.no_backup()

    def check_the_mode(self):
        print("Checking mode...")
        # One time per day
        if self.iniOneTimePerDay == "true":
            print("One time per day found")
            if self.totalCurrentTime > self.totalNextTime:
                ################################################################################
                # ! Every time user turn off pc, firstStartup inside INI file is update to true
                # Only backup if:
                #  * App was unable to backup because PC was off
                #  * Make sure that App had not already made a backup today after time has passed
                # by check the latest backup date "self.iniLatestDate" inside INI file.
                ################################################################################
                if self.iniFirstStartup == "true" and self.dayName not in self.iniLatestDate: 
                    ################################################################################
                    # Set startup to False and Continue to back up
                    ################################################################################
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w') as configfile:
                        config.set('BACKUP', 'first_startup', 'false')
                        config.write(configfile)
                        
                    # Call backup now
                    self.call_backup_now()

                else: 
                    print(f"{appName} has alredy made a backup for today.")
                    print("Time to back up has passed")
                    self.no_backup()

            elif self.totalCurrentTime == self.totalNextTime:
                self.call_backup_now()

            else:
                print("Waiting for the right time to backup...")
                ################################################################################
                # Set startup to False, so wont backup twice after passed time :D
                ################################################################################
                ################################################################################
                # Write to  INI file
                ################################################################################
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('BACKUP', 'first_startup', 'false')
                    config.write(configfile)

        else: 
            print("Multiple time per day")
            if self.iniEverytime == '60' and self.totalCurrentTime in timeModeHours60:
                if self.iniBackupNowChecker == "false":
                    self.call_backup_now()

            elif self.iniEverytime == '120' and self.totalCurrentTime in timeModeHours120:
                if self.iniBackupNowChecker == "false":
                    self.call_backup_now()

            elif self.iniEverytime == '240' and self.totalCurrentTime in timeModeHours240:
                if self.iniBackupNowChecker == "false":
                    self.call_backup_now()

            else:
                print("Waiting for the right time to backup...")

    def call_backup_now(self):
        print("Back up will start shortly...")
        ################################################################################
        # Set notification_id to 1
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.set('INFO', 'notification_id', '1')  # Backup will start shortly...
            config.write(configfile)

        # Call backup now
        sub.Popen(f"python3 {src_backup_now}", shell=True)  # Call backup now
        exit()

    def no_backup(self):
        print("No backup... Updating INI file...")
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'checker_running', 'false')
            config.write(configfile)

        exit()

    def signal_exit(self, *args):
        print("Change INI settings... Exiting...")
        self.no_backup()

main = CLI()
while True:
    main.updates()
    main.is_system_tray_running()
    main.check_connection()

    print("Updating...")
    # Exit program if automatically backup is false
    if main.iniBackupNowChecker == "true":
        print("Exiting backup checker...")
        break

    # Exit program if auto_backup is false
    if main.iniAutoBackup == "false":
        print("Exiting backup checker...")
        break

    time.sleep(2)

main.no_backup()




