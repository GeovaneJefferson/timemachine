from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class BACKUP:
    def __init__(self):
        # Terminal commands
        self.copyCmd = "rsync -avruzh "
        self.createCmd = "mkdir "

        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            
            # Get hour, minute
            dateTime = datetime.now()
            dateDay = dateTime.strftime("%d")
            dateMonth = dateTime.strftime("%m")
            dateYear = dateTime.strftime("%y")
            self.dayName = dateTime.strftime("%a")

            self.currentHour = dateTime.strftime("%H")
            self.currentMinute = dateTime.strftime("%M")

            # Get user.ini
            self.getExternalLocation = config['EXTERNAL']['hd']
            self.getHDName = config['EXTERNAL']['name']
            self.getIniFolders = config.options('FOLDER')
            self.backupNowChecker = config['BACKUP']['backup_now']
            self.oneTimeMode = config['MODE']['one_time_mode']

            self.createTMB = self.getExternalLocation + "/TMB" 
            self.dateFolder = f"{self.createTMB}/{dateDay}-{dateMonth}-{dateYear}" 
            self.timeFolder = f"{self.createTMB}/{dateDay}-{dateMonth}-{dateYear}/{self.currentHour}-{self.currentMinute}"

            self.create_TMB()   # If everything goes well, continue
        
        except KeyError:
            print("Error trying to read user.ini!")
            error_reading()
            exit()

    def create_TMB(self):
        # Backup now True
        if self.backupNowChecker == "true":  # Read user.ini
            try:
                # TMB folders
                if os.path.exists(self.createTMB):
                    print("TMB folders inside external, already exist.")
                else:
                    print("TMB folder inside external, was created.")
                    sub.run(self.createCmd + self.createTMB, shell=True)    # Create tmb folder

            except FileNotFoundError:
                print("Error trying to create TMB...")
                error_backup()  # Notification
                exit()
        else:
            print("Nothing to do right now...")
            exit()

        self.create_folder_date()  # Move on

    def create_folder_date(self):
        try:
            if os.path.exists(self.dateFolder): 
                pass
            else:
                sub.run(self.createCmd + self.dateFolder, shell=True)   # Create folder with date

        except FileNotFoundError:
            print("Error trying to create date folder...")
            error_backup()  # Notification
            exit()

        self.create_folder_time()

    def create_folder_time(self):
        try:
            if os.path.exists(self.timeFolder): 
                pass
            else:
                sub.run(self.createCmd + self.timeFolder, shell=True)   # Create folder with date

        except FileNotFoundError:
            print("Error trying to create date folder...")
            error_backup()  # Notification
            exit()

        self.start_backup()

    def start_backup(self):
        try:
            if self.oneTimeMode == "true":
                print("One mode activated!")
                
                for output in self.getIniFolders:    # Backup all (user.ini true folders)
                    output = output.title()  # Capitalize first letter. ex: '/Desktop'
                    print(f"Back up: {output}")
                    sub.run(f"{self.copyCmd}{home_user}/{output} {self.timeFolder}", shell=True) #Ex: TMB/date/Desktop
            else:
                print("More mode activated!")
                sub.run(self.createCmd + self.timeFolder, shell=True) # Create folder with date and time
                
                for output in self.getIniFolders:    # Backup all (user.ini true folders)
                    output = output.title()  # Capitalize first letter. ex: '/Desktop'
                    print(f"Back up: {output}")
                    sub.run(f"{self.copyCmd}{home_user}/{output} {self.timeFolder}", shell=True) #Ex: TMB/date/time/Desktop
                    print("")

        except FileNotFoundError:
            print("Error trying to back up folders to external location...")
            error_backup()  # Notification
            exit()

        self.end_backup()

    def end_backup(self):
        # Read ini file
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            config.set('INFO', 'latest', f'{self.dayName}, {self.currentHour}:{self.currentMinute}')
            config.write(configfile)

        # After backup is done
        done_backup_notification()  # Notification
        time.sleep(60)    
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)    # Call backup checker
        exit()


main = BACKUP()
