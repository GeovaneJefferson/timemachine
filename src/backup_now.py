from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class BACKUP:
    def __init__(self):
        ################################################################################
        ## Commands
        ################################################################################
        self.createCmd = "mkdir"
        self.createFile = "touch"

        try:
            ################################################################################
            ## Get hour, minute
            ################################################################################
            dateTime = datetime.now()
            dateDay = dateTime.strftime("%d")
            dateMonth = dateTime.strftime("%m")
            dateYear = dateTime.strftime("%y")
            self.dayName = dateTime.strftime("%a")
            self.currentHour = dateTime.strftime("%H")
            self.currentMinute = dateTime.strftime("%M")

            ################################################################################
            ## Get user.ini
            ################################################################################
            self.getExternalLocation = config['EXTERNAL']['hd']
            self.getHDName = config['EXTERNAL']['name']
            self.getIniFolders = config.options('FOLDER')
            self.backupNowChecker = config['BACKUP']['backup_now']
            self.oneTimeMode = config['MODE']['one_time_mode']

            ################################################################################
            ## Create folders
            ################################################################################
            self.createTMB = f"{self.getExternalLocation}/{folderName}"
            self.dateFolder = f"{self.createTMB}/{dateDay}-{dateMonth}-{dateYear}"
            self.timeFolder = f"{self.createTMB}/{dateDay}-{dateMonth}-{dateYear}/{self.currentHour}-{self.currentMinute}"

            ################################################################################
            ## Apt txt file
            ################################################################################
            self.apt_txt = f"{self.getExternalLocation}/{folderName}/apt.txt"

            ################################################################################
            ## Flatpak txt file
            ################################################################################
            self.flatpak_txt = f"{self.getExternalLocation}/{folderName}/flatpak.txt"

            self.create_TMB()

        except KeyError:
            print("Error trying to read user.ini!")
            error_reading()
            exit()

    def create_TMB(self):
        ################################################################################
        ## Create TMB
        ################################################################################
        if self.backupNowChecker == "true":  # Read user.ini
            try:
                if os.path.exists(self.createTMB):
                    print("TMB folders inside external, already exist.")
                else:
                    print("TMB folder inside external, was created.")
                    sub.run(f"{self.createCmd} {self.createTMB}", shell=True)

            except FileNotFoundError:
                print("Error trying to create TMB...")
                error_backup()
                exit()
        else:
            print("Nothing to do right now...")
            exit()

        self.create_apt_file()

    def create_apt_file(self):
        ################################################################################
        ## Create file txt
        ################################################################################
        try:
            if os.path.exists(self.apt_txt):
                print("Apt file already exist.")
            else:
                print("Apt file was created.")
                sub.run(f"{self.createFile} {self.apt_txt}", shell=True)    # Create tmb folder

        except FileNotFoundError:
            print("Error trying to create Apt file...")
            error_backup()  # Notification
            exit()

        self.create_flatpak_file()

    def create_flatpak_file(self):
        ################################################################################
        ## Create file txt
        ################################################################################
        try:
            # TMB folders
            if os.path.exists(self.flatpak_txt):
                print("Flatpak file already exist.")
            else:
                print("Flatpak file was created.")
                sub.run(f"{self.createFile} {self.flatpak_txt}", shell=True)    # Create tmb folder

        except FileNotFoundError:
            print("Error trying to create Flatpak file...")
            error_backup()  # Notification
            exit()

        self.save_apt_file()

    def save_apt_file(self):
        ################################################################################
        ## Commands
        ################################################################################
        x = os.popen("apt-mark showmanual")

        ################################################################################
        ## Save to file
        ################################################################################
        list = []
        for _ in x:
            list.append(x.readline())

        try:
            with open(f"{self.getExternalLocation}/{folderName}/apt.txt", "w") as write_file:
                for i in list:
                    if not i.startswith(exclude):
                        write_file.write(i)

            ################################################################################
            ## Read to file
            ################################################################################
            with open(f"{self.getExternalLocation}/{folderName}/apt.txt", "r") as read_file:
                try:
                    for i in read_file:
                        print(i.strip())
                except:
                    pass  # Add do error list to install
        except:
            print("Error tying to save apt list of apps to the file!")
            exit()

        self.save_flatpak_file()

    def save_flatpak_file(self):
        ################################################################################
        ## Commands
        ################################################################################
        x = os.popen("flatpak list -a --columns=application --app")

        ################################################################################
        ## Save to file
        ################################################################################
        list = []
        for _ in x:
            list.append(x.readline())

        try:
            with open(f"{self.getExternalLocation}/{folderName}/flatpak.txt", "w") as write_file:
                for i in list:
                    if not i.startswith(exclude):
                        write_file.write(i)

            ################################################################################
            ## Read to file
            ################################################################################
            with open(f"{self.getExternalLocation}/{folderName}/flatpak.txt", "r") as read_file:
                try:
                    for i in read_file:
                        print(i.strip())
                except:
                    pass  # Add do error list to install
        except:
            print("Error trying to save flatpak list of apps to the file!")
            exit()

        self.check_size()

    def check_size(self):
        ################################################################################
        ## Get current size
        ################################################################################
        usedSpace = os.popen(f"du -s {self.getExternalLocation}")
        usedSpace = usedSpace.read().strip("\t").strip("\n").replace(self.getExternalLocation, "").replace("\t", "")
        usedSpace = int(usedSpace)

        ################################################################################
        ## Get total size
        ################################################################################
        outputMaximum = os.popen(f"df --output=size {self.getExternalLocation}")
        outputMaximum = outputMaximum.read().strip().replace("1K-blocks", "").replace(" ", "")
        outputMaximum = int(outputMaximum)

        # Local variables
        freeSpace = int(outputMaximum - usedSpace)
        limit = int(outputMaximum * 0.99)   # 20% limit space

        print(f"USB used space:   ", usedSpace)
        print("USB maximum size:   ", outputMaximum)
        print("USB free size:   ", freeSpace)
        print("USB limit space:   ", limit)

        ################################################################################
        ## Condition
        ################################################################################
        if usedSpace >= limit:
            print("External is almost full!")
            print("Old files will be deleted, to make room for the new ones.")
            print("Please wait...")

            ################################################################################
            ## Get available dates inside TMB
            ################################################################################
            try:
                dateFolders = []
                for output in os.listdir(f"{self.getExternalLocation}/{folderName}"):
                    dateFolders.append(output)
                    dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

                print(dateFolders)
                ################################################################################
                ## Delete old folders
                ################################################################################
                sub.run(f"rm -rf {self.getExternalLocation}/{folderName}/{dateFolders[-1]}", shell=True)
                print(f"Deleting {self.getExternalLocation}/{folderName}/{dateFolders[-1]}...")

                self.create_folder_date()

            except FileNotFoundError:
                print("Error trying to delete old backups!")
                error_delete()
                exit()

            print("Date available: ", self.dateFolders)
        else:
            self.create_folder_date()

    def create_folder_date(self):
        ################################################################################
        ## Create folder with date
        ################################################################################
        try:
            if os.path.exists(self.dateFolder):
                pass
            else:
                sub.run(f"{self.createCmd} {self.dateFolder}", shell=True)   # Create folder with date

        except FileNotFoundError:
            print("Error trying to create date folder...")
            error_backup()
            exit()

        self.create_folder_time()

    def create_folder_time(self):
        ################################################################################
        ## Create folder with time
        ################################################################################
        try:
            if os.path.exists(self.timeFolder):
                pass
            else:
                sub.run(f"{self.createCmd} {self.timeFolder}", shell=True)

        except FileNotFoundError:
            print("Error trying to create date folder...")
            error_backup()  # Notification
            exit()

        self.start_backup()

    def start_backup(self):
        ################################################################################
        ## Start with the backup
        ################################################################################
        try:
            if self.oneTimeMode == "true":
                print("One mode activated!")

                for output in self.getIniFolders:    # Backup all (user.ini true folders)
                    output = output.title()  # Capitalize first letter. ex: '/Desktop'
                    print(f"Back up: {output}")
                    sub.run(f"{copyCmd} {home_user}/{output} {self.timeFolder}", shell=True) #Ex: TMB/date/Desktop

            else:
                print("More mode activated!")
                sub.run(f"{self.createCmd} {self.timeFolder}", shell=True) # Create folder with date and time

                for output in self.getIniFolders:    # Backup all (user.ini true folders)
                    output = output.title()  # Capitalize first letter. ex: '/Desktop'
                    print(f"Back up: {output}")
                    sub.run(f"{copyCmd} {home_user}/{output} {self.timeFolder}", shell=True) #Ex: TMB/date/time/Desktop
                    print("")

        except FileNotFoundError:
            print("Error trying to back up folders to external location...")
            error_backup()
            exit()

        self.end_backup()

    def end_backup(self):
        ################################################################################
        ## Update "last backup" and set backup_now to "false"
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            config.set('INFO', 'latest', f'{self.dayName}, {self.currentHour}:{self.currentMinute}')
            config.write(configfile)

        ################################################################################
        ## After backup is done
        ################################################################################
        done_backup_notification()
        time.sleep(60) # Wait 60, so if it finish fast, wont repeat the backup :D
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)
        exit()


main = BACKUP()
