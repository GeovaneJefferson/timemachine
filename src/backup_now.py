from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class CLI:
    def __init__(self):
        # Read ini file
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Terminal commands
        self.copyCmd = "rsync -avzh "
        self.createCmd = "mkdir "

        # Get hour, minute
        self.dateTime = datetime.now()
        self.dayName = self.dateTime.strftime("%a")
        self.dateDay = self.dateTime.strftime("%d")
        self.dateMonth = self.dateTime.strftime("%m")
        self.dateYear = self.dateTime.strftime("%y")
        self.currentHour = self.dateTime.strftime("%H")
        self.currentMinute = self.dateTime.strftime("%M")

        # Get user.ini
        self.getIniFolders = config.options('FOLDER')
        self.getExternalLocation = config['EXTERNAL']['hd']
        self.backupNowChecker = config['BACKUP']['backup_now']

        # Create tmb folder
        self.createTMB = self.getExternalLocation + "/TMB"
        self.dateFolder = self.createTMB + "/" + self.dateDay + "-" + self.dateMonth + "-" + self.dateYear

        self.backup_now_pressed()

    def backup_now_pressed(self):
        # Backup now True
        if self.backupNowChecker == "true":  # Read user.ini (setup.py)
            try:
                # TMB folders
                if os.path.exists(self.createTMB):
                    print("TMB folders inside external, already exist.")
                    pass
                else:
                    print("TMB folder inside external, was created.")
                    os.system(self.createCmd + self.createTMB)
            except:
                print("Error trying to create TMB folder")
                exit()

            try:
                # Put date folder
                if os.path.exists(self.dateFolder):
                    pass
                else:
                    os.system(self.createCmd + self.dateFolder)
            except:
                print("Error trying to create TMB folder with date")
                exit()

            # Backup all (user.ini true folders)
            try:
                for items in self.getIniFolders:
                    output = items.title()  # Capitalize first letter. ex: '/Desktop'
                    dst_loc = self.dateFolder + '/' + output
                    print(output)
                    os.system(self.copyCmd + home_user + '/' + output + '/ ' + dst_loc)

            except FileExistsError:
                pass

            # After backup is done
            done_backup_notification()  # Call done notification (setup.py)

            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', 'false')
                config.set('INFO', 'latest', self.dayName + ', ' + self.currentHour + ':' + self.currentMinute)
                config.write(configfile)
                exit()

            # except FileNotFoundError:
            #     not_available_notification()


main = CLI()
main.__init__()
