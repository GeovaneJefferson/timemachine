from setup import *

# QTimer
timer = QtCore.QTimer()


class CLI:
    def __init__(self):
        self.time = 2

        ################################################################################
        ## Variables
        ################################################################################
        self.systemTrayActivated = None
        signal.signal(signal.SIGINT, self.signal_exit)
        signal.signal(signal.SIGTERM, self.signal_exit)

        # # Timer
        # timer.timeout.connect(self.updates)
        # timer.start(1000)  # update every second
        # self.updates()

    def updates(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        self.getHDName = config['EXTERNAL']['name']
        self.backupNowChecker = config['BACKUP']['backup_now']
        self.getSystemTray = config['SYSTEMTRAY']['system_tray']
        # self.getCheckerRunning = config['BACKUP']['checker_running']

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
        self.dayName = self.dayName.lower()

        # Time
        now = datetime.now()
        self.currentHour = now.strftime("%H")
        self.currentMinute = now.strftime("%M")

        # Read INI file
        self.backupNowChecker = config['BACKUP']['backup_now']
        self.getAutoBackup = config['BACKUP']['auto_backup']
        self.oneTimeMode = config['MODE']['one_time_mode']
        self.everytime = config['SCHEDULE']['everytime']
        self.nextHour = config['SCHEDULE']['hours']
        self.nextMinute = config['SCHEDULE']['minutes']

        self.totalCurrentTime = self.currentHour + self.currentMinute
        self.totalNextTime = self.nextHour + self.nextMinute

        self.is_system_tray_running()

    def is_system_tray_running(self):
        if self.getSystemTray == "true" and self.systemTrayActivated != None:
            self.systemTrayActivated = True

            ################################################################################
            ## Call system tray
            ################################################################################
            sub.Popen(f"python3 {src_system_tray}", shell=True)

        self.can_external_name_be_found()

    def can_external_name_be_found(self):
        if self.getHDName != "":
            self.check_for_external_media()

        else:
            no_external_info()
            self.no_backup()

    def check_for_external_media(self):  # Check for external in media/
        try:
            for output in os.listdir("/media/" + user_name):
                if not output.startswith('.'):
                    if self.getHDName in output:  # If user.ini has external hd name
                        print("External found in /media.")
                        self.check_the_date()

        except FileNotFoundError:
            self.check_for_external_run()

    def check_for_external_run(self):  # Or check for external in run/
        try:
            for output in os.listdir("/run/media/" + user_name):  # Try other folder (fx. Opensuse)
                if not output.startswith('.'):
                    if self.getHDName in output:  # If user.ini has external hd name
                        print("External found in /run/media.")
                        self.check_the_date()

        except FileNotFoundError:
            print("No external devices mounted or available...")
            not_available_notification()  # Call not available notification
            self.no_backup()

    def check_the_date(self):
        print("Checking dates...")

        if self.dayName == "sun" and self.getScheduleSun == "true":
            self.check_the_mode()

        elif self.dayName == "mon" and self.getScheduleMon == "true":
            self.check_the_mode()

        elif self.dayName == "tue" and self.getScheduleTue == "true":
            self.check_the_mode()

        elif self.dayName == "wed" and self.getScheduleWed == "true":
            self.check_the_mode()

        elif self.dayName == "thu" and self.getScheduleThu == "true":
            self.check_the_mode()

        elif self.dayName == "fri" and self.getScheduleFri == "true":
            self.check_the_mode()

        elif self.dayName == "sat" and self.getScheduleSat == "true":
            self.check_the_mode()

        else:
            print("No back up for today.")
            self.no_backup()

    def check_the_mode(self):
        print("Checking mode...")

        if self.oneTimeMode == "true":  # one time mode
            print("One Time Mode found")
            if self.totalCurrentTime > self.totalNextTime:
                print("Time to back up has passed")
                self.no_backup()

            elif self.totalCurrentTime == self.totalNextTime:
                self.call_backup_now()

            else:
                print("Waiting for the right time to backup...")
                # time.sleep(self.time)

        else:  # More time mode
            print("More Time Mode found")

            if self.everytime == '15':
                if self.currentMinute in time_mode_minutes_15:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

            elif self.everytime == '30':
                if self.currentMinute in time_mode_minutes_30:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

            elif self.everytime == '60':
                if self.currentHour in time_mode_hours_60:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

            elif self.everytime == '120':
                if self.currentHour in time_mode_hours_120:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

            elif self.everytime == '240':
                if self.currentHour in time_mode_hours_240:
                    if self.backupNowChecker == "false":
                        self.call_backup_now()

    def call_backup_now(self):
        print("Starting back up...")

        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

            sub.Popen(f"python3 {src_backup_now}", shell=True)  # Call backup checker
            exit()

    def no_backup(self):
        print("No backup... Updating INI file...")
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            # config.set('BACKUP', 'auto_backup', 'false')
            config.set('BACKUP', 'checker_running', 'false')
            config.write(configfile)

        exit()

    def signal_exit(self, *args):
        print("Change INI settings... Exiting...")
        self.no_backup()

main = CLI()
while True:
    main.updates()
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

    ###############################################################################
    # Do not allow more than 1 backup_checker at the same time
    ###############################################################################
    # if main.getCheckerRunning == 'false':
    #     print("Break checker running")
    #     pass

    time.sleep(main.time)

main.no_backup()



