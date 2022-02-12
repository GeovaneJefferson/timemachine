from setup import *

# Read/Load user.config
config = configparser.ConfigParser()
config.read(src_user_config)


class CLI:
    def __init__(self):
        self.getHDName = config['EXTERNAL']['name']
        self.time = 5

        self.check_for_external()

    def check_for_external(self):
        try:
            for storage in os.listdir("/media/" + user_name):
                if not storage.startswith('.'):
                    if self.getHDName in storage:  # If user.ini has external hd name
                        self.check_the_date()

        except FileNotFoundError:
            for storage in os.listdir("/run/media/" + user_name):   # Try other folder (fx. Opensuse)
                if not storage.startswith('.'):
                    if self.getHDName in storage:  # If user.ini has external hd name
                        self.check_the_date()

        else:
            print("No external devices mounted or available...")
            not_available_notification()  # Call not available notification
            exit()

    def check_the_date(self):
        print("Backup checker is running...")
        print("HD found!")

        while True:
            # Read/Load user.config (backup automatically)
            config = configparser.ConfigParser()
            config.read(src_user_config)
            
            get_schedule_sun = config['SCHEDULE']['sun']
            get_schedule_mon = config['SCHEDULE']['mon']
            get_schedule_tue = config['SCHEDULE']['tue']
            get_schedule_wed = config['SCHEDULE']['wed']
            get_schedule_thu = config['SCHEDULE']['thu']
            get_schedule_fri = config['SCHEDULE']['fri']
            get_schedule_sat = config['SCHEDULE']['sat']

            # Get date
            day_name = datetime.now()
            day_name = day_name.strftime("%a")
            day_name = day_name.lower()

            if day_name == "sun" and get_schedule_sun == "true":
                break

            elif day_name == "mon" and get_schedule_mon == "true":
                break

            elif day_name == "tue" and get_schedule_tue == "true":
                break

            elif day_name == "wed" and get_schedule_wed == "true":
                break

            elif day_name == "thu" and get_schedule_thu == "true":
                break

            elif day_name == "fri" and get_schedule_fri == "true":
                break

            elif day_name == "sat" and get_schedule_sat == "true":
                break
            
            else:
                print("No back up for today.")
                exit()

        self.check_the_mode()

    def check_the_mode(self):
        while True:
            # Read/Load user.config
            config = configparser.ConfigParser()
            config.read(src_user_config)
            now = datetime.now()
            currentHour = now.strftime("%H")
            currentMinute = now.strftime("%M")

            # backupNowChecker = config['BACKUP']['backup_now']
            oneTimeMode = config['MODE']['one_time_mode']
            # moreTimeMode = config['MODE']['more_time_mode']
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
                    with open(src_user_config, 'w') as configfile:
                        config.set('BACKUP', 'backup_now', 'true')
                        config.write(configfile)

                        sub.run("python3 " + src_backup_now, shell=True)    # Open backup now
                        exit()
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(self.time)

            else:   # More time mode
                if everytime == '15':
                    if currentMinute in time_mode_minutes_15:
                        break

                elif everytime == '30':
                    if currentMinute in time_mode_minutes_30:
                        break

                elif everytime == '60':
                    if currentHour in time_mode_hours_60:
                        break

                elif everytime == '120':
                    if currentHour in time_mode_hours_120:
                        break

                elif everytime == '240':
                    if currentHour in time_mode_hours_240:
                        break

                print("Current time: " + currentHour + ":" + currentMinute)
                print("Backup time: " + nextHour + ":" + nextMinute)
                print("Waiting for the right time to backup...")
                time.sleep(self.time)

        self.call_backup_now()

    def call_backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)
            
            sub.run("python3 " + src_backup_now, shell=True)    # Call backup checker


main = CLI()
