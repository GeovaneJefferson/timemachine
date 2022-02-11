from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class CLI:
    def __init__(self):
        self.storage = []
        self.getHDName = config['EXTERNAL']['name']
        self.t = 5

        self.check_for_external()

    def check_for_external(self):
        try:
            for self.storage in os.listdir("/media/" + user_name + "/"):
                if not self.storage.startswith('.'):
                    print("Local media        : ", self.storage)
                    print("Saved external name: ", self.getHDName)

            if self.getHDName in self.storage:  # If user.ini has external hd name
                print("HD found!")
                self.check_the_date()
            else:
                not_available_notification()  # Call not available notification (setup.py)

        except FileNotFoundError:
            print("No external devices mounted or available...")
            exit()

    def check_the_date(self):
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
            print("Backup checker is running...")

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

            print("No back up for today.")
            exit()

        self.check_the_mode()

    def check_the_mode(self):
        # Read/Load user.config
        config = configparser.ConfigParser()
        config.read(src_user_config)

        next_hour = config['SCHEDULE']['hours']
        next_minute = config['SCHEDULE']['minutes']

        # Frequency check
        one_time_mode = config['MODE']['one_time_mode']

        if one_time_mode == "true":
            while True:
                now = datetime.now()
                current_hour = now.strftime("%H")
                current_minute = now.strftime("%M")

                total_current_time = current_hour + current_minute
                total_next_time = next_hour + next_minute

                print(total_current_time)
                print(total_next_time)

                time.sleep(self.t)

                if total_current_time > total_next_time:
                    print("Time to back up has passed")
                    exit()

                if total_current_time == total_next_time:
                    break
                else:
                    print("Waiting for the right time to backup...")
                    time.sleep(self.t)

            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', 'true')
                config.write(configfile)

                # Open backup checker
                sub.Popen("python3 " + src_backup_now, shell=True)
                exit()

        else:
            while True:
                # ----Read/Load user.config (backup automatically)----#
                config = configparser.ConfigParser()
                config.read(src_user_config)

                # User.ini
                backupNowChecker = config['BACKUP']['backup_now']
                moreTimeMode = config['MODE']['more_time_mode']
                everytime = config['SCHEDULE']['everytime']

                now = datetime.now()
                current_hour = now.strftime("%H")
                current_minute = now.strftime("%M")

                print("Current time: " + current_hour + ":" + current_minute)
                time.sleep(self.t)

                if everytime == '15':
                    print('everytime: ' + everytime)
                    if current_minute in time_mode_minutes_15:
                        with open(src_user_config, 'w') as configfile:
                            config.set('BACKUP', 'backup_now', 'true')
                            config.write(configfile)
                            break
                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(self.t)

                if everytime == '30':
                    print('everytime: ' + everytime)
                    if current_minute in time_mode_minutes_30:
                        with open(src_user_config, 'w') as configfile:
                            config.set('BACKUP', 'backup_now', 'true')
                            config.write(configfile)
                            break
                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(self.t)

                if everytime == '60':
                    print('everytime: ' + everytime)
                    if current_hour in time_mode_hours_60:
                        with open(src_user_config, 'w') as configfile:
                            config.set('BACKUP', 'backup_now', 'true')
                            config.write(configfile)
                            break

                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(self.t)

                if everytime == '120':
                    print('everytime: ' + everytime)
                    if current_hour in time_mode_hours_120:
                        with open(src_user_config, 'w') as configfile:
                            config.set('BACKUP', 'backup_now', 'true')
                            config.write(configfile)
                            break

                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(self.t)

                if everytime == '240':
                    print('everytime: ' + everytime)
                    if current_hour in time_mode_hours_240:
                        with open(src_user_config, 'w') as configfile:
                            config.set('BACKUP', 'backup_now', 'true')
                            config.write(configfile)
                            break

                    else:
                        print("Waiting for the right time to backup...")
                        time.sleep(self.t)

                if moreTimeMode == "false":
                    break

            # Call backup checker
            sub.call("python3 " + src_backup_now, shell=True)
            self.__init__()


app = CLI()
