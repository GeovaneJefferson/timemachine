from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class CLI:
    def __init__(self):
        # Terminal commands
        self.copyCmd = "rsync -avzh "
        self.createCmd = "mkdir "

        self.create_folders()

    def create_folders(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            
            # Get hour, minute
            self.dateTime = datetime.now()
            self.dayName = self.dateTime.strftime("%a")
            self.dateDay = self.dateTime.strftime("%d")
            self.dateMonth = self.dateTime.strftime("%m")
            self.dateYear = self.dateTime.strftime("%y")
            self.currentHour = self.dateTime.strftime("%H")
            self.currentMinute = self.dateTime.strftime("%M")

            # Get user.ini
            self.getExternalLocation = config['EXTERNAL']['hd']
            self.getHDName = config['EXTERNAL']['name']
            self.getIniFolders = config.options('FOLDER')
            self.backupNowChecker = config['BACKUP']['backup_now']

            # Create tmb folder
            self.createTMB = self.getExternalLocation + "/TMB"
            self.dateFolder = self.createTMB + "/" + self.dateDay + "-" + self.dateMonth + "-" + self.dateYear
            
            self.create_TMB()   # If everything goes well, continue
        
        except KeyError:
            print("Error trying to read user.ini!")
            error_reading()
            exit()

    def create_TMB(self):
        # Backup now True
        if self.backupNowChecker == "true":  # Read user.ini (setup.py)
            try:
                # TMB folders
                if os.path.exists(self.createTMB):
                    print("TMB folders inside external, already exist.")
                else:
                    print("TMB folder inside external, was created.")
                    sub.run(self.createCmd + self.createTMB, shell=True)

            except FileNotFoundError:
                print("Error trying to create TMB...")
                error_backup()      # Notification
                exit()
        else:
            print("Nothing to do right now...")
            exit()

        self.create_date_folder()  # Move on

    def create_date_folder(self):
        try:
            if os.path.exists(self.dateFolder):     # Put date folder
                pass
            else:
                sub.run(self.createCmd + self.dateFolder, shell=True)

        except FileNotFoundError:
            print("Error trying to create date folder...")
            error_backup()      # Notification
            exit()

        self.start_backup()

    def start_backup(self):
        try:
            for items in self.getIniFolders:    # Backup all (user.ini true folders)
                output = items.title()  # Capitalize first letter. ex: '/Desktop'
                dst_loc = self.dateFolder + '/' + output
                print(output)
                sub.run(self.copyCmd + home_user + '/' + output + '/ ' + dst_loc, shell=True)

        except FileNotFoundError:
            print("Error trying to back up folders...")
            error_backup()      # Notification
            exit()

        self.end_backup()

    def end_backup(self):
        # Read ini file
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            config.set('INFO', 'latest', self.dayName + ', ' + self.currentHour + ':' + self.currentMinute)
            config.write(configfile)

        # After backup is done
        done_backup_notification()  # Notification
        time.sleep(60)    
        sub.Popen("python3 " + src_backup_check_py, shell=True)    # Call backup checker
        exit()


main = CLI()
