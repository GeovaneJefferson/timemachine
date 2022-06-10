from setup import *


class CLI:
    def __init__(self):
        ################################################################################
        ## Variables
        ################################################################################
        self.systemTrayActivated = None

        ################################################################################
        ## Signal
        ################################################################################
        signal.signal(signal.SIGINT, self.signal_exit)
        signal.signal(signal.SIGTERM, self.signal_exit)

    def updates(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Informations
        self.getHDName = config['EXTERNAL']['name']
        self.backupNowChecker = config['BACKUP']['backup_now']
        self.getSystemTray = config['SYSTEMTRAY']['system_tray']
        self.getLatestDate = config['INFO']['latest']

        # Dates
        self.getScheduleSun = config['SCHEDULE']['sun']
        self.getScheduleMon = config['SCHEDULE']['mon']
        self.getScheduleTue = config['SCHEDULE']['tue']
        self.getScheduleWed = config['SCHEDULE']['wed']
        self.getScheduleThu = config['SCHEDULE']['thu']
        self.getScheduleFri = config['SCHEDULE']['fri']
        self.getScheduleSat = config['SCHEDULE']['sat']

        self.dayName = datetime.now()
        self.dayName = self.dayName.strftime("%a")

        # Time
        now = datetime.now()
        self.currentHour = now.strftime("%H")
        self.currentMinute = now.strftime("%M")

        # Read INI file
        self.firstStartup = config['BACKUP']['first_startup']
        self.backupNowChecker = config['BACKUP']['backup_now']
        self.getAutoBackup = config['BACKUP']['auto_backup']
        self.oneTimeMode = config['MODE']['one_time_mode']
        self.everytime = config['SCHEDULE']['everytime']
        self.nextHour = config['SCHEDULE']['hours']
        self.nextMinute = config['SCHEDULE']['minutes']

        self.totalCurrentTime = self.currentHour + self.currentMinute
        self.totalNextTime = self.nextHour + self.nextMinute

        # self.is_system_tray_running()

    def is_system_tray_running(self):
        ################################################################################
        ## Prevent multiples system tray App
        ################################################################################
        if self.getSystemTray == "true" and self.systemTrayActivated != None and self.firstStartup == "false":
            self.systemTrayActivated = True

            ################################################################################
            ## Call system tray
            ################################################################################
            sub.Popen(f"python3 {src_system_tray}", shell=True)

        # self.can_external_name_be_found()

    def can_external_name_be_found(self):
        if self.getHDName != "":
            print("Device name found in INI file...")
            self.check_for_external_media()

        else:
            ################################################################################
            ## Set notification_id to 8
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "8")
                config.write(configfile)

            sub.Popen(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification

            self.no_backup()

    def check_for_external_media(self):  # Check for external in media/
        print("Checking external under /media... ")
        try:
            for output in os.listdir("/media/" + userName):
                if not output.startswith('.'):
                    if self.getHDName in output:  # If user.ini has external hd name
                        print("External found in /media.")
                        self.check_the_date()
                    
                    else:
                        self.check_for_external_run()

        except FileNotFoundError:
            self.check_for_external_run()

    def check_for_external_run(self):  # Or check for external in run/
        print("Checking external under /run/media... ")
        try:
            for output in os.listdir("/run/media/" + userName):  # Try other folder (fx. Opensuse)
                if not output.startswith('.'):
                    if self.getHDName in output:  # If user.ini has external hd name
                        print("External found in /run/media.")
                        self.check_the_date()

                    ################################################################################
                    ## If external can not be found, exit the App.
                    ################################################################################
                    else:
                        ################################################################################
                        ## Set notification_id to 3
                        ################################################################################
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_id', "3")
                            config.write(configfile)

                        print("External not mounted or available...")
                        sub.Popen(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification

        except FileNotFoundError:
            ################################################################################
            ## Set notification_id to 3
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "3")
                config.write(configfile)

            print("External not mounted or available...")
            sub.Popen(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification
            self.no_backup()

    def check_the_date(self):
        print("Checking dates...")

        if self.dayName == "Sun" and self.getScheduleSun == "true":
            self.check_the_mode()

        elif self.dayName == "Mon" and self.getScheduleMon == "true":
            self.check_the_mode()

        elif self.dayName == "Tue" and self.getScheduleTue == "true":
            self.check_the_mode()

        elif self.dayName == "Wed" and self.getScheduleWed == "true":
            self.check_the_mode()

        elif self.dayName == "Thu" and self.getScheduleThu == "true":
            self.check_the_mode()

        elif self.dayName == "Fri" and self.getScheduleFri == "true":
            self.check_the_mode()

        elif self.dayName == "Sat" and self.getScheduleSat == "true":
            self.check_the_mode()

        else:
            print("No back up for today.")
            self.no_backup()

    def check_the_mode(self):
        print("Checking mode...")
        ################################################################################
        ## One Time Mode
        ################################################################################
        if self.oneTimeMode == "true":
            print("One Time Mode found")
            if self.totalCurrentTime > self.totalNextTime:
                ################################################################################
                ## ! Every time user turn off pc, firstStartup inside INI file is update to true
                ## Only backup if:
                ##  * App was unable to backup because PC was off
                ##  * Make sure that App had not already made a backup today after time has passed
                ## by check the latest backup date "self.getLatestDate" inside INI file.
                ################################################################################
                if self.firstStartup == "true" and self.dayName not in self.getLatestDate: 
                    ################################################################################
                    ## Set startup to False and Continue to back up
                    ################################################################################
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w') as configfile:
                        config.set('BACKUP', 'first_startup', 'false')
                        config.write(configfile)

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
                ## Set startup to False, so wont backup twice after passed time :D
                ################################################################################
                ################################################################################
                ## Write to  INI file
                ################################################################################
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('BACKUP', 'first_startup', 'false')
                    config.write(configfile)

        else:  # More time mode
            print("More Time Mode found")

            if self.everytime == '30':
                if self.currentMinute in timeModeMinutes30:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

            elif self.everytime == '60':
                if self.currentHour in timeModeHours60:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

            elif self.everytime == '120':
                if self.currentHour in timeModeHours120:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

            elif self.everytime == '240':
                if self.currentHour in timeModeHours240:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

    def call_backup_now(self):
        print("Back up will start shortly...")

        ################################################################################
        ## Call notification and wait x seconds
        ################################################################################
        sub.Popen(f"python3 {src_notification}", shell=True)  # Call notification
        time.sleep(5)

        ################################################################################
        ## Set notification_id to 3
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.set('INFO', 'notification_id', '1')  # Backup will start shortly...
            config.write(configfile)

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
    main.can_external_name_be_found()
    # main.check_for_external_media()
    # main.check_for_external_run()
    # main.check_the_date()


    print("Updating...")
    ################################################################################
    ## Exit program if auto_backup is false
    ################################################################################
    if main.backupNowChecker == "true":
        print("Break backupchecker")
        break

    ################################################################################
    ## Exit program if auto_backup is false
    ################################################################################
    if main.getAutoBackup == "false":
        print("Break autobackup")
        break

    time.sleep(2)

main.no_backup()



