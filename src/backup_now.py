from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class CLI:
    def __init__(self):
        # Terminal commands
        self.copy_cmd = "rsync -avzh "
        self.create_cmd = "mkdir "

        # Get hour, minute
        self.date_time = datetime.now()
        self.day_name = (self.date_time.strftime("%a"))
        self.date_day = (self.date_time.strftime("%d"))
        self.date_month = (self.date_time.strftime("%m"))
        self.date_year = (self.date_time.strftime("%y"))
        self.current_hour = self.date_time.strftime("%H")
        self.current_minute = self.date_time.strftime("%M")

        # Get user.ini
        self.get_ini_folders = config.options('FOLDER')
        self.get_hd_loc = config['EXTERNAL']['hd']
        self.backup_now_checker = config['BACKUP']['backup_now']

        # Create tmb folder
        self.create_tmb = self.get_hd_loc + "/TMB"
        self.date_folder = self.create_tmb + "/" + self.date_day + "-" + self.date_month + "-" + self.date_year

        self.backup_now_pressed()

    def backup_now_pressed(self):
        # Backup now True
        if self.backup_now_checker == "true":  # Read user.ini (setup.py)
            try:
                # TMB folders
                if os.path.exists(self.create_tmb):
                    print("TMB folders inside external, already exist.")
                    pass
                else:
                    print("TMB folder inside external, was created.")
                    os.system(self.create_cmd + self.create_tmb)

            except:
                print("Error trying to create TMB folder")
                exit()

            try:
                # Put date folder
                if os.path.exists(self.date_folder):
                    pass
                else:
                    os.system(self.create_cmd + self.date_folder)
            except:
                print("Error trying to create TMB folder with date")
                exit()

            # Backup all (user.ini true folders)
            try:
                for itens in self.get_ini_folders:
                    output = itens.title()  # Capitalize self.get_ini_folders. ex: '/Desktop'
                    dst_loc = self.date_folder + '/' + output
                    print(output)
                    os.system(self.copy_cmd + home_user + '/' + output + '/ ' + dst_loc)

            except FileExistsError:
                pass

            # After backup is done
            done_backup_notification()  # Call done notification (setup.py)

            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', 'false')
                config.set('INFO', 'latest', self.day_name + ', ' + self.current_hour + ':' + self.current_minute)
                config.write(configfile)
                exit()

            # except FileNotFoundError:
            #     not_available_notification()


app = CLI()
app.__init__()
