from setup import *

# Read/Load user.config
config = configparser.ConfigParser()
config.read(src_user_config)


class CLI:
    def __init__(self):
        self.time = 5
        self.getHDName = config['EXTERNAL']['name']
        self.get_hd_name = config['EXTERNAL']['name']

        self.check_user_settings()

    def check_user_settings(self):
        if self.get_hd_name != "":
            self.check_for_external_media()
        else:
            no_external_info()
            exit()
        
    def check_for_external_media(self): # Check for external in media/
        try:
            for output in os.listdir("/media/" + user_name):
                if not output.startswith('.'):
                    if self.getHDName in output:  # If user.ini has external hd name
                        print("External found in /media")
                        self.check_the_date()
        except FileNotFoundError:  
            self.check_for_external_run()

    def check_for_external_run(self):   # Or check for external in run/
        try:
            for output in os.listdir("/run/media/" + user_name):   # Try other folder (fx. Opensuse)
                if not output.startswith('.'):
                    if self.getHDName in output:  # If user.ini has external hd name
                        print("External found in /run/media")
                        self.check_the_date()
        except FileNotFoundError:
            print("No external devices mounted or available...")
            not_available_notification()  # Call not available notification
            exit()

    def check_the_date(self):
        print("Backup checker is running...")

        while True:
            # Read/Load user.config (backup automatically)
            config = configparser.ConfigParser()
            config.read(src_user_config)
            
            getScheduleSun = config['SCHEDULE']['sun']
            getScheduleMon = config['SCHEDULE']['mon']
            getScheduleTue = config['SCHEDULE']['tue']
            getScheduleWed = config['SCHEDULE']['wed']
            getScheduleThu = config['SCHEDULE']['thu']
            getScheduleFri = config['SCHEDULE']['fri']
            getScheduleSat = config['SCHEDULE']['sat']

            # Get date
            dayName = datetime.now()
            dayName = dayName.strftime("%a")
            dayName = dayName.lower()

            if dayName == "sun" and getScheduleSun == "true":
                break

            elif dayName == "mon" and getScheduleMon == "true":
                break

            elif dayName == "tue" and getScheduleTue == "true":
                break

            elif dayName == "wed" and getScheduleWed == "true":
                break

            elif dayName == "thu" and getScheduleThu == "true":
                break

            elif dayName == "fri" and getScheduleFri == "true":
                break

            elif dayName == "sat" and getScheduleSat == "true":
                break
            
            else:
                print("No back up for today.")
                exit()

        self.check_the_mode()

    def check_the_mode(self):
        print("Checking the mode...")
        while True:
            # Read/Load user.config
            config = configparser.ConfigParser()
            config.read(src_user_config)

            now = datetime.now()
            currentHour = now.strftime("%H")
            currentMinute = now.strftime("%M")

            backupNowChecker = config['BACKUP']['backup_now']
            oneTimeMode = config['MODE']['one_time_mode']
            everytime = config['SCHEDULE']['everytime']
            nextHour = config['SCHEDULE']['hours']
            nextMinute = config['SCHEDULE']['minutes']

            totalCurrentTime = currentHour + currentMinute
            totalNextTime = nextHour + nextMinute

            if oneTimeMode == "true":   # one time mode
                if totalCurrentTime > totalNextTime:
                    print("Time to back up has passed")
                    exit()

                elif totalCurrentTime == totalNextTime:
                    break
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(self.time)

            else:   # More time mode
                if everytime == '15':
                    if currentMinute in time_mode_minutes_15:
                        if backupNowChecker == "false":
                            break

                elif everytime == '30':
                    if currentMinute in time_mode_minutes_30:
                        if backupNowChecker == "false":
                            break

                elif everytime == '60':
                    if currentHour in time_mode_hours_60:
                        if backupNowChecker == "false":
                            break

                elif everytime == '120':
                    if currentHour in time_mode_hours_120:
                        if backupNowChecker == "false":
                            break

                elif everytime == '240':
                    if currentHour in time_mode_hours_240:
                        if backupNowChecker == "false":
                            break
                        
                print("")
                print("Backup time  : " + nextHour + ":" + nextMinute + " One Time Mode")
                print("Backup time every : " + everytime)
                print("Waiting for the right time to backup...")
                print("")
                time.sleep(self.time)

        self.call_backup_now()

    def call_backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)
            
            sub.Popen("python3 " + src_backup_now, shell=True)    # Call backup checker


main = CLI()
