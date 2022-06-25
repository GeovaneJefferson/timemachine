#! /usr/bin/env python3
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
        self.iniNotification = config['INFO']['notification']
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

    def check_for_external_media(self):  
        ################################################################################
        # Check for external in media/
        ################################################################################
        try:
            print("Checking external under /media... ")
            if self.iniHDName in os.listdir(f"/media/{userName}"):
                print("External found in /media.")
                self.check_the_date()

            else:
                # If device name can not be found inside /media, continue
                raise FileNotFoundError
            
        except FileNotFoundError:
            # If /media is empty, continue
            self.check_for_external_run()

    def check_for_external_run(self): 
        ################################################################################
        # Check for external in run/media/
        ################################################################################
        try:
            print("Checking external under /run/media... ")
            if self.iniHDName in os.listdir(f"/run/media/{userName}"):  # If user.ini has external hd name
                print("External found in /run/media.")
                self.check_the_date()

            else:
                # If device name can not be found inside /media, exit
                raise FileNotFoundError
        
        except FileNotFoundError:
            ################################################################################
            # If run/media is empty, exit
            # Set notification_id to 3
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "3")
                config.write(configfile)

            # If user has allow app to send notifications
            if self.iniNotification == "true":
                print("External not mounted or available...")
                sub.run(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification
            
            exit()

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

        elif self.iniMultipleTimePerDay == "true": 
            print("Multiple time per day found")
            if self.iniEverytime == '30':
                if self.currentMinute in timeModeMinutes30:
                    if self.iniBackupNowChecker == "false":
                        self.call_backup_now()

            elif self.iniEverytime == '60':
                if self.currentHour in timeModeHours60:
                    if self.iniBackupNowChecker == "false":
                        self.call_backup_now()

            elif self.iniEverytime == '120':
                if self.currentHour in timeModeHours120:
                    if self.iniBackupNowChecker == "false":
                        self.call_backup_now()

            elif self.iniEverytime == '240':
                if self.currentHour in timeModeHours240:
                    if self.iniBackupNowChecker == "false":
                        self.call_backup_now()

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
        
        # Call notification and wait x seconds
        sub.Popen(f"python3 {src_notification}", shell=True)  # Call notification
        time.sleep(5)

        # If user has allow app to send notifications
        if self.iniNotification == "true":
            sub.Popen(f"python3 {src_backup_now}", shell=True)  # Call backup now
        
        exit()

    def no_backup(self):
        print("No backup... Updating INI file...")
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'checker_running', 'false')
            config.write(configfile)

        # sub.run(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification
        exit()

    def signal_exit(self, *args):
        print("Change INI settings... Exiting...")
        self.no_backup()

main = CLI()
while True:
    main.updates()
    main.is_system_tray_running()
    main.check_for_external_media()

    print("Updating...")
    # Exit program if auto_backup is false
    if main.iniBackupNowChecker == "true":
        print("Break backupchecker")
        break
    # Exit program if auto_backup is false
    if main.iniAutoBackup == "false":
        print("Break autobackup")
        break

    time.sleep(2)

main.no_backup()



