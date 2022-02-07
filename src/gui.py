from setup import *


# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        loadUi(src_ui, self)
        self.setWindowTitle(app_name)
        app_icon = QIcon(src_restore_icon)
        self.setWindowIcon(app_icon)
        self.setFixedHeight(450)
        self.setFixedWidth(700)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)

        # Connections
        self.auto_checkbox.clicked.connect(self.automatically_backup)
        self.btn_external.clicked.connect(self.external_clicked)
        self.btn_options.clicked.connect(self.options_clicked)
        self.btn_donate.clicked.connect(self.donate_clicked)

        # Backup now btn
        self.btn_backup_now = QPushButton("Back Up Now", self)
        self.btn_backup_now.setGeometry(452, 158, 120, 33)
        self.btn_backup_now.clicked.connect(self.backup_now_clicked)

        # Timer
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

    def updates(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Get current hour, minutes
        now = datetime.now()
        day_name = now.strftime("%a")
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")

        # Get user.ini
        get_auto_backup = config['BACKUP']['auto_backup']
        get_last_backup = config['INFO']['latest']
        get_next_backup = config['INFO']['next']
        get_hd_name = config['EXTERNAL']['name']
        more_time_mode = config['MODE']['more_time_mode']
        everytime = config['SCHEDULE']['everytime']

        next_day = "None"
        get_next_hour = config['SCHEDULE']['hours']
        get_next_minute = config['SCHEDULE']['minutes']
        get_next_backup_sun = config['SCHEDULE']['sun']
        get_next_backup_mon = config['SCHEDULE']['mon']
        get_next_backup_tue = config['SCHEDULE']['tue']
        get_next_backup_wed = config['SCHEDULE']['wed']
        get_next_backup_thu = config['SCHEDULE']['thu']
        get_next_backup_fri = config['SCHEDULE']['fri']
        get_next_backup_sat = config['SCHEDULE']['sat']

        total_current_time = current_hour + current_minute
        total_next_time = get_next_hour + get_next_minute

        # Auto backup
        if get_auto_backup == "true":
            self.auto_checkbox.setChecked(True)

        # Set external name
        self.set_external_name.setText(get_hd_name)
        self.set_external_name.setFont(QFont('Arial', 18))

        try:
            os.listdir("/media/" + user_name + "/" + get_hd_name)  # Check if external can be found

            if get_hd_name != "":  # External name and status
                self.set_external_name.setText(get_hd_name)
                self.set_external_name.setFont(QFont('Arial', 18))
                self.btn_backup_now.show()  # Show backup button

                # Set external name and status
                self.status_external.setText("External HD: Connected")
                self.status_external.setFont(QFont('Arial', 10))
                self.status_external.setStyleSheet('color: green')
            else:
                self.btn_backup_now.hide()  # Hide backup now button

        except FileNotFoundError:
            self.btn_backup_now.hide()  # Hide backup now button

            # Set external name and status
            self.status_external.setText("External HD: Disconnected")
            self.status_external.setFont(QFont('Arial', 10))
            self.status_external.setStyleSheet('color: red')

        # Last backup label
        if get_last_backup == "":
            self.label_last_backup.setText("Last Backup: None")
            self.label_last_backup.setFont(QFont('Arial', 10))
        else:
            self.label_last_backup.setText("Last Backup: " + get_last_backup)
            self.label_last_backup.setFont(QFont('Arial', 10))

        # Next backup label
        if get_next_backup == "":
            self.label_next_backup.setText("Next Backup: None")
            self.label_next_backup.setFont(QFont('Arial', 10))
        else:
            self.label_next_backup.setText("Next Backup: " + get_next_backup)
            self.label_next_backup.setFont(QFont('Arial', 10))

        # Next backup label(everytime)
        if more_time_mode == "true" and everytime == "15":
            self.label_next_backup.setText("Next Backup: Every 15 minutes")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "30":
            self.label_next_backup.setText("Next Backup: Every 30 minutes")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "60":
            self.label_next_backup.setText("Next Backup: Every 1 hour")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "120":
            self.label_next_backup.setText("Next Backup: Every 2 hours")
            self.label_next_backup.setFont(QFont('Arial', 10))

        if more_time_mode == "true" and everytime == "240":
            self.label_next_backup.setText("Next Backup: Every 4 hours")
            self.label_next_backup.setFont(QFont('Arial', 10))

        # Print current time and day
        print("Current time:" + current_hour + ":" + current_minute)
        print("Day:" + day_name)

        if day_name == "Sun":
            if get_next_backup_sun == "true" and current_hour <= get_next_hour and current_minute <= get_next_minute:
                next_day = "Today"
            else:
                if get_next_backup_mon == "true":
                    next_day = "Mon"
                elif get_next_backup_tue == "true":
                    next_day = "Tue"
                elif get_next_backup_wed == "true":
                    next_day = "Wed"
                elif get_next_backup_thu == "true":
                    next_day = "Thu"
                elif get_next_backup_fri == "true":
                    next_day = "Fri"
                elif get_next_backup_sat == "true":
                    next_day = "Sat"
                elif get_next_backup_sun == "true":
                    next_day = "Sun"

        if day_name == "Mon":
            if get_next_backup_mon == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if get_next_backup_tue == "true":
                    next_day = "Tue"
                elif get_next_backup_wed == "true":
                    next_day = "Wed"
                elif get_next_backup_thu == "true":
                    next_day = "Thu"
                elif get_next_backup_fri == "true":
                    next_day = "Fri"
                elif get_next_backup_sat == "true":
                    next_day = "Sat"
                elif get_next_backup_sun == "true":
                    next_day = "Sun"
                elif get_next_backup_mon == "true":
                    next_day = "Mon"

        if day_name == "Tue":
            if get_next_backup_tue == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if get_next_backup_wed == "true":
                    next_day = "Wed"
                elif get_next_backup_thu == "true":
                    next_day = "Thu"
                elif get_next_backup_fri == "true":
                    next_day = "Fri"
                elif get_next_backup_sat == "true":
                    next_day = "Sat"
                elif get_next_backup_sun == "true":
                    next_day = "Sun"
                elif get_next_backup_mon == "true":
                    next_day = "Mon"
                elif get_next_backup_tue == "true":
                    next_day = "Tue"

        if day_name == "Wed":
            if get_next_backup_wed == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if get_next_backup_thu == "true":
                    next_day = "Thu"
                elif get_next_backup_fri == "true":
                    next_day = "Fri"
                elif get_next_backup_sat == "true":
                    next_day = "Sat"
                elif get_next_backup_sun == "true":
                    next_day = "Sun"
                elif get_next_backup_mon == "true":
                    next_day = "Mon"
                elif get_next_backup_tue == "true":
                    next_day = "Tue"
                elif get_next_backup_wed == "true":
                    next_day = "Wed"

        if day_name == "Thu":
            if get_next_backup_thu == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if get_next_backup_fri == "true":
                    next_day = "Fri"
                elif get_next_backup_sat == "true":
                    next_day = "Sat"
                elif get_next_backup_sun == "true":
                    next_day = "Sun"
                elif get_next_backup_mon == "true":
                    next_day = "Mon"
                elif get_next_backup_tue == "true":
                    next_day = "Tue"
                elif get_next_backup_wed == "true":
                    next_day = "Wed"
                elif get_next_backup_thu == "true":
                    next_day = "Thu"

        if day_name == "Fri":
            if get_next_backup_fri == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if get_next_backup_sat == "true":
                    next_day = "Sat"
                elif get_next_backup_sun == "true":
                    next_day = "Sun"
                elif get_next_backup_mon == "true":
                    next_day = "Mon"
                elif get_next_backup_tue == "true":
                    next_day = "Tue"
                elif get_next_backup_wed == "true":
                    next_day = "Wed"
                elif get_next_backup_thu == "true":
                    next_day = "Thu"
                elif get_next_backup_fri == "true":
                    next_day = "Fri"

        if day_name == "Sat":
            if get_next_backup_sat == "true" and total_current_time < total_next_time:
                next_day = "Today"
            else:
                if get_next_backup_sun == "true":
                    next_day = "Sun"
                elif get_next_backup_mon == "true":
                    next_day = "Mon"
                elif get_next_backup_tue == "true":
                    next_day = "Tue"
                elif get_next_backup_wed == "true":
                    next_day = "Wed"
                elif get_next_backup_thu == "true":
                    next_day = "Thu"
                elif get_next_backup_fri == "true":
                    next_day = "Fri"
                elif get_next_backup_sat == "true":
                    next_day = "Sat"

        # Save next backup to user.ini
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'next', next_day + ', ' + get_next_hour + ':' + get_next_minute)
            config.write(configfile)

    def automatically_backup(self):
        # Automatically back up selected
        if self.auto_checkbox.isChecked():
            if os.path.exists(src_backup_check_desktop):
                pass
            else:
                shutil.copy(src_backup_check, src_backup_check_desktop)  # Copy src .desktop to dst .desktop
                auto_backup_notification()  # Call auto backup notification

                with open(src_user_config, 'w') as configfile:  # Set auto backup to true
                    config.set('BACKUP', 'auto_backup', 'true')
                    config.write(configfile)

                print("Auto backup was successfully activated!")
        else:
            auto_backup_off_notification()  # Call auto backup off notification
            sub.Popen("rm " + src_backup_check_desktop, shell=True)     # Remove .desktop from dst

            # Set auto backup to false
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'auto_backup', 'false')
                config.write(configfile)

            print("Auto backup was successfully deactivated!")

        # Call backup check py
        sub.Popen("python3 " + src_backup_check_py, shell=True)

    @staticmethod
    def external_clicked():
        # Choose external hd
        sub.call("python3 " + src_where_py, shell=True)

    @staticmethod
    def backup_now_clicked():
        config = configparser.ConfigParser()
        config.read(src_user_config)
        # Set backup now to true
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

            # Call backup now py
            sub.Popen("python3 " + src_backup_now, shell=True)

    @staticmethod
    def options_clicked():
        # Call schedule
        sub.call("python3 " + src_options_py, shell=True)

    @staticmethod
    def donate_clicked():
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)


app = QApplication(sys.argv)
main = UI()
main.show()
app.exit(app.exec())
