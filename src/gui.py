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

        # Center window
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        # Connections
        self.auto_checkbox.clicked.connect(self.automatically_backup)
        self.btn_external.clicked.connect(self.external_clicked)
        self.btn_options.clicked.connect(self.options_clicked)
        self.btn_donate.clicked.connect(self.donate_clicked)

        # Backup now btn
        self.btn_backup_now = QPushButton("Back Up Now", self)
        self.btn_backup_now.resize(120, 34)
        self.btn_backup_now.move(452, 157)
        self.btn_backup_now.clicked.connect(self.backup_now_clicked)

        # Timer
        timer.timeout.connect(self.updates)
        timer.start(500)  # update every second
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
        get_backup_now = config['BACKUP']['backup_now']
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
            try:
                os.listdir("/media/" + user_name + "/" + get_hd_name)  # Check if external can be found
            except:
                os.listdir("/run/media/" + user_name + "/" + get_hd_name)  # Opensuse, external is inside "/run"

            if get_hd_name != "":  # External name and status
                self.set_external_name.setText(get_hd_name)
                self.set_external_name.setFont(QFont('Arial', 18))
                if get_backup_now == "false":
                    # Backup now settings changed
                    self.btn_backup_now.setText("Back Up Now")
                    self.btn_backup_now.setEnabled(True)  # Disable backup now button
                    self.btn_backup_now.resize(120, 34)  # Resize backup button
                    self.btn_backup_now.show()
                else:
                    # Backup now settings changed
                    self.btn_backup_now.setText("Your files are being back up...")
                    self.btn_backup_now.setEnabled(False)  # Disable backup now button
                    self.btn_backup_now.resize(200, 34)  # Resize backup button

                # Set external name and status
                self.status_external.setText("External HD: Connected")
                self.status_external.setFont(QFont('Arial', 10))
                self.status_external.setStyleSheet('color: green')
            else:
                self.btn_backup_now.hide()  # Hide backup now button

        except:
            self.btn_backup_now.hide()  # Hide backup now button

            # Set external name and status
            self.status_external.setText("External HD: Disconnected")
            self.status_external.setFont(QFont('Arial', 10))
            self.status_external.setStyleSheet('color: red')

        # Last backup label
        if get_last_backup == "":
            self.label_last_backup.setText("Last Backup: ")
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
            sub.Popen("rm " + src_backup_check_desktop, shell=True)  # Remove .desktop from dst

            # Set auto backup to false
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'auto_backup', 'false')
                config.write(configfile)

            print("Auto backup was successfully deactivated!")

        # Call backup check py
        sub.Popen("python3 " + src_backup_check_py, shell=True)

    def external_clicked(self):
        # Choose external hd
        self.setEnabled(False)
        EXTERNAL.__init__(externalMain)     # Call external screen
        externalMain.show()     # Show external screen

    def backup_now_clicked(self):

        config = configparser.ConfigParser()
        config.read(src_user_config)
        # Set backup now to true
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

            # Call backup now py
            sub.Popen("python3 " + src_backup_now, shell=True)

    def options_clicked(self):
        # Call schedule
        sub.call("python3 " + src_options_py, shell=True)

    def donate_clicked(self):
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)


# External Screen
class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        loadUi(src_ui_where, self)
        self.setWindowTitle("External Screen")
        appIcon = QIcon(src_restore_icon)
        self.setWindowIcon(appIcon)
        # self.baseHeight = 50
        # self.extendedHeight = 325
        self.setFixedHeight(325)
        self.setFixedWidth(400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.currentHeight = self.height()

        # Center widget
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        self.usedMedia = False
        self.usedRun = False
        self.media = "/media/"
        self.run = "/run/media/"

        # Connections
        self.button_where_cancel.clicked.connect(self.btn_cancel_clicked)

        self.external()

    def external(self):
        try:
            try:
                # Get local media
                local_media = os.listdir(self.media + user_name + "/")
                print(local_media)
                self.usedMedia = True
            except:
                local_media = os.listdir(self.run + user_name + "/")  # Opensuse, external is inside "/run"
                print(local_media)
                self.usedRun = True

            # Add buttons and images for each external
            vertical = 20
            vertical_img = 32
            for self.storage in local_media:
                print("Available external:")
                print(self.storage)
                label_image = QLabel(self)
                pixmap = QPixmap(src_restore_small_icon)
                label_image.setPixmap(pixmap)
                label_image.setFixedSize(48, 48)
                label_image.move(30, vertical_img)
                vertical_img = vertical_img + 50

                # Button
                button = QPushButton(self.storage, self.where_frame)
                button.setFixedSize(280, 30)
                button.move(60, vertical)
                vertical = vertical + 50
                text = button.text()
                button.show()
                button.clicked.connect(lambda ch: self.on_button_clicked(text))

        except:
            none_external = QLabel("No external devices mounted or available...", self.where_frame)
            none_external.move(55, 100)
            none_external.setFixedSize(300, 50)
            none_external.setFont(QFont('Arial', 10))
            none_external.setStyleSheet('color: red')

            print("No external devices mounted or available...")

    def on_button_clicked(self, get):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Read/Load user.config (backup automatically)
        with open(src_user_config, 'w') as configfile:
            if self.usedMedia:
                config.set('EXTERNAL', 'hd', self.media + user_name + '/' + get)
            else:
                config.set('EXTERNAL', 'hd', self.run + user_name + '/' + get)

            config.set('EXTERNAL', 'name', get)
            config.write(configfile)

            self.close()
            main.setEnabled(True)

    def btn_cancel_clicked(self):
        externalMain.close()
        main.setEnabled(True)


app = QApplication(sys.argv)
main = UI()
externalMain = EXTERNAL()

main.show()
app.exit(app.exec())
