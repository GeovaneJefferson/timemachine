from setup import *

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setWindowTitle(app_name)
        app_icon = QIcon(src_restore_icon)
        self.setWindowIcon(app_icon)
        self.setFixedSize(700, 450)

        self.widgets()

    def widgets(self):
        ################################################################################
        ## Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 200, 180)

        # Left widget
        self.baseVLeftLayout = QVBoxLayout(self.leftWidget)
        self.baseVLeftLayout.setSpacing(20)

        # Backup images
        self.backupImage = QLabel()
        self.backupImage.setFixedSize(128, 128)
        self.backupImage.setStyleSheet(
            "QLabel"
            "{"
                f"background-image: url({src_backup_icon});"
            "}"
        )

        # Auto checkbox
        self.auto_checkbox = QCheckBox()
        self.auto_checkbox.setFont(QFont("Ubuntu", 10))
        self.auto_checkbox.setText("Back Up Automatically")
        self.auto_checkbox.setFixedSize(160, 20)
        self.auto_checkbox.clicked.connect(self.automatically_clicked)

        ################################################################################
        ## Right Widget
        ################################################################################
        self.rightWidget = QWidget(self)
        self.rightWidget.setGeometry(260, 40, 160, 154)
        # self.rightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right widget
        self.baseVRightLayout = QVBoxLayout(self.rightWidget)
        self.baseVRightLayout.setSpacing(20)

        # Restore images
        self.restoreImage = QLabel()
        self.restoreImage.setFixedSize(96, 96)
        self.restoreImage.setStyleSheet(
            "QLabel"
            "{"
                f"background-image: url({src_restore_icon});"
                "background-repeat: no-repeat;"
            "}")

        # Select disk button
        self.btn_external = QPushButton(self)
        self.btn_external.setFont(QFont("Ubuntu", 10))
        self.btn_external.setText("Select Backup Disk...")
        self.btn_external.setFixedSize(140, 34)
        self.btn_external.clicked.connect(self.external_clicked)

        ################################################################################
        ## Far right Widget
        ################################################################################
        self.farRightWidget = QWidget(self)
        self.farRightWidget.setContentsMargins(0, 0, 0, 0)
        self.farRightWidget.setGeometry(425, 40, 250, 153)
        # self.farRightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right widget
        self.baseVFarRightLayout = QVBoxLayout(self.farRightWidget)
        self.baseVFarRightLayout.setSpacing(0)

        # Set external name
        self.set_external_name = QLabel()

        # Label last backup
        self.label_last_backup = QLabel()
        self.label_last_backup.setFont(QFont("Ubuntu", 10))
        self.label_last_backup.setText("Last Backup:")
        self.label_last_backup.setFixedSize(200, 18)

        # Label last backup
        self.label_next_backup = QLabel()
        self.label_next_backup.setFont(QFont("Ubuntu", 10))
        self.label_next_backup.setText("Next Backup:")
        self.label_next_backup.setFixedSize(250, 18)

        # Status external hd
        self.status_external = QLabel()
        self.status_external.setFont(QFont("Ubuntu", 10))
        self.status_external.setText("External HD:")
        self.status_external.setFixedSize(200, 18)

        # Backup now btn
        self.btn_backup_now = QPushButton("Back Up Now", self)
        self.btn_backup_now.setFixedSize(100, 34)
        self.btn_backup_now.clicked.connect(self.backup_now_clicked)
        self.btn_backup_now.hide()

        ################################################################################
        ## Ui description
        ################################################################################
        self.uiTextWidget = QWidget(self)
        self.uiTextWidget.setGeometry(260, 200, 380, 120)
        # self.uiTextWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # UiText widget
        self.baseVUiTextLayout = QVBoxLayout(self.uiTextWidget)

        self.uiText = QLabel()
        self.uiText.setFont(QFont("Ubuntu", 10))
        self.uiText.setFixedSize(400, 120)
        self.uiText.setText(
            "Time Machine is able to:\n\n"
            "* Keep local snapshots as space permits\n"
            "* Schedule backups\n\n"
            "Delete the oldest backups when your disk becomes full.\n")

        ################################################################################
        ## Donate and Settings buttons
        ################################################################################
        self.donateAndSettingsWidget = QWidget(self)
        self.donateAndSettingsWidget.setGeometry(480, 370, 200, 80)
        # self.donateAndSettingsWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Donate and Settings widget
        self.donateAndSettingsLayout = QHBoxLayout(self.donateAndSettingsWidget)
        self.donateAndSettingsLayout.setSpacing(20)

        # Donate buton
        self.btn_donate = QPushButton()
        self.btn_donate.setText("Donate")
        self.btn_donate.setFont(QFont("Ubuntu", 10))
        self.btn_donate.setFixedSize(80, 34)
        self.btn_donate.clicked.connect(self.donate_clicked)

        # Settings buton
        self.btn_options = QPushButton()
        self.btn_options.setText("Options")
        self.btn_options.setFont(QFont("Ubuntu", 10))
        self.btn_options.setFixedSize(80, 34)
        self.btn_options.clicked.connect(self.options_clicked)

        ################################################################################
        ## Add widgets and Layouts
        ################################################################################
        # BaseVLeftlayout
        self.baseVLeftLayout.addWidget(self.backupImage, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.baseVLeftLayout.addWidget(self.auto_checkbox, 0, Qt.AlignVCenter | Qt.AlignHCenter)

        #  baseVRight layout
        self.baseVRightLayout.addWidget(self.restoreImage, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.baseVRightLayout.addWidget(self.btn_external, 1, Qt.AlignVCenter | Qt.AlignHCenter)

        #  baseVFarRight layout
        self.baseVFarRightLayout.addWidget(self.set_external_name, 0, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addWidget(self.label_last_backup, 1, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addWidget(self.label_next_backup, 2, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addWidget(self.status_external, 3, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addStretch(5)
        self.baseVFarRightLayout.addWidget(self.btn_backup_now, 4, Qt.AlignLeft | Qt.AlignVCenter)

        #  baseVUiText layout
        self.baseVUiTextLayout.addWidget(self.uiText, 0, Qt.AlignVCenter | Qt.AlignLeft)

        #  Donate and Settings layout
        self.donateAndSettingsLayout.addWidget(self.btn_donate, 0, Qt.AlignHCenter | Qt.AlignVCenter)
        self.donateAndSettingsLayout.addWidget(self.btn_options, 1, Qt.AlignHCenter | Qt.AlignVCenter)

        self.setLayout(self.baseVLeftLayout)

        # # Center window
        # frameGm = self.frameGeometry()
        # screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        # centerPoint = QApplication.desktop().screenGeometry(screen).center()
        # frameGm.moveCenter(centerPoint)
        # self.move(frameGm.topLeft())



        # Timer
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

    def updates(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Get current hour, minutes
        now = datetime.now()
        self.day_name = now.strftime("%a")
        self.current_hour = now.strftime("%H")
        self.current_minute = now.strftime("%M")

        try:
            # Get user.ini
            self.get_backup_now = config['BACKUP']['backup_now']
            self.get_auto_backup = config['BACKUP']['auto_backup']
            self.get_last_backup = config['INFO']['latest']
            self.get_next_backup = config['INFO']['next']
            self.getHDName = config['EXTERNAL']['name']
            self.more_time_mode = config['MODE']['more_time_mode']
            self.everytime = config['SCHEDULE']['everytime']

            self.next_day = "None"
            self.get_next_hour = config['SCHEDULE']['hours']
            self.get_next_minute = config['SCHEDULE']['minutes']
            self.get_next_backup_sun = config['SCHEDULE']['sun']
            self.get_next_backup_mon = config['SCHEDULE']['mon']
            self.get_next_backup_tue = config['SCHEDULE']['tue']
            self.get_next_backup_wed = config['SCHEDULE']['wed']
            self.get_next_backup_thu = config['SCHEDULE']['thu']
            self.get_next_backup_fri = config['SCHEDULE']['fri']
            self.get_next_backup_sat = config['SCHEDULE']['sat']

        except KeyError:
            print("Error trying to read user.ini!")
            exit()

        self.total_current_time = self.current_hour + self.current_minute
        self.total_next_time = self.get_next_hour + self.get_next_minute

        self.check_connection_media()

    def check_connection_media(self):
        # External availability
        try:
            os.listdir(f"/media/{user_name}/{self.getHDName}")  # Check if external can be found
            self.connected()

        except FileNotFoundError:
            self.check_connection_run()

    def check_connection_run(self):
        try:
            os.listdir(f"/run/media/{user_name}/{self.getHDName}")  # Opensuse, external is inside "/run"
            self.connected()

        except FileNotFoundError:
            self.btn_backup_now.hide()  # Hide backup now button

            # External status
            self.status_external.setText("External HD: Disconnected")
            self.status_external.setFont(QFont('Ubuntu', 10))
            self.status_external.setStyleSheet('color: red')

        self.ui_settings()

    def connected(self):
        if self.getHDName != "None":  # If location can be found
            if self.get_backup_now == "false":   # If is not back up right now
                # External status
                self.status_external.setText("External HD: Connected")
                self.status_external.setFont(QFont('Ubuntu', 10))
                self.status_external.setStyleSheet('color: green')

                self.btn_backup_now.setText("Back Up Now")  # Show backup now button
                self.btn_backup_now.setEnabled(True)  # Disable backup now button
                self.btn_backup_now.setFixedSize(120, 34)  # Resize backup button
                self.btn_backup_now.show()

            else:
                self.btn_backup_now.setText("Your files are being back up...")
                self.btn_backup_now.setEnabled(False)  # Disable backup now button
                self.btn_backup_now.setFixedSize(180, 34)  # Resize backup button
        else:
            self.btn_backup_now.hide()

        self.ui_settings()

    def ui_settings(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        ################################################################################
        ## Auto backup
        ################################################################################
        if self.get_auto_backup == "true":
            self.auto_checkbox.setChecked(True)
            self.set_external_name.setText(self.getHDName)    # Set external name
            self.set_external_name.setFont(QFont('Ubuntu', 18))

        ################################################################################
        ## External name
        ################################################################################
        if self.getHDName != "None":
            self.set_external_name.setText(self.getHDName)
            self.set_external_name.setFont(QFont('Ubuntu', 18))

        ################################################################################
        ## Last backup label
        ################################################################################
        if self.get_last_backup == "":
            self.label_last_backup.setText("Last Backup: ")
            self.label_last_backup.setFont(QFont('Ubuntu', 10))
        else:
            self.label_last_backup.setText(f"Last Backup: {self.get_last_backup}")
            self.label_last_backup.setFont(QFont('Ubuntu', 10))

        ################################################################################
        ## Next backup label
        ################################################################################
        if self.get_next_backup == "":
            self.label_next_backup.setText("Next Backup: None")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        if not self.auto_checkbox.isChecked():
            self.label_next_backup.setText("Next Backup: Automatic backups off")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        else:
            self.label_next_backup.setText(f"Next Backup: {self.get_next_backup}")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        ################################################################################
        ## Next backup label everytime
        ################################################################################
        if self.more_time_mode == "true" and self.everytime == "15":
            self.label_next_backup.setText("Next Backup: Every 15 minutes")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        if self.more_time_mode == "true" and self.everytime == "30":
            self.label_next_backup.setText("Next Backup: Every 30 minutes")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        if self.more_time_mode == "true" and self.everytime == "60":
            self.label_next_backup.setText("Next Backup: Every 1 hour")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        if self.more_time_mode == "true" and self.everytime == "120":
            self.label_next_backup.setText("Next Backup: Every 2 hours")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        if self.more_time_mode == "true" and self.everytime == "240":
            self.label_next_backup.setText("Next Backup: Every 4 hours")
            self.label_next_backup.setFont(QFont('Ubuntu', 10))

        if self.day_name == "Sun":
            if self.get_next_backup_sun == "true" and self.current_hour <= self.get_next_hour and self.current_minute <= self.get_next_minute:
                self.next_day = "Today"
            else:
                if self.get_next_backup_mon == "true":
                    self.next_day = "Mon"
                elif self.get_next_backup_tue == "true":
                    self.next_day = "Tue"
                elif self.get_next_backup_wed == "true":
                    self.next_day = "Wed"
                elif self.get_next_backup_thu == "true":
                    self.next_day = "Thu"
                elif self.get_next_backup_fri == "true":
                    self.next_day = "Fri"
                elif self.get_next_backup_sat == "true":
                    self.next_day = "Sat"
                elif self.get_next_backup_sun == "true":
                    self.next_day = "Sun"

        if self.day_name == "Mon":
            if self.get_next_backup_mon == "true" and self.total_current_time < self.total_next_time:
                self.next_day = "Today"
            else:
                if self.get_next_backup_tue == "true":
                    self.next_day = "Tue"
                elif self.get_next_backup_wed == "true":
                    self.next_day = "Wed"
                elif self.get_next_backup_thu == "true":
                    self.next_day = "Thu"
                elif self.get_next_backup_fri == "true":
                    self.next_day = "Fri"
                elif self.get_next_backup_sat == "true":
                    self.next_day = "Sat"
                elif self.get_next_backup_sun == "true":
                    self.next_day = "Sun"
                elif self.get_next_backup_mon == "true":
                    self.next_day = "Mon"

        if self.day_name == "Tue":
            if self.get_next_backup_tue == "true" and self.total_current_time < self.total_next_time:
                self.next_day = "Today"
            else:
                if self.get_next_backup_wed == "true":
                    self.next_day = "Wed"
                elif self.get_next_backup_thu == "true":
                    self.next_day = "Thu"
                elif self.get_next_backup_fri == "true":
                    self.next_day = "Fri"
                elif self.get_next_backup_sat == "true":
                    self.next_day = "Sat"
                elif self.get_next_backup_sun == "true":
                    self.next_day = "Sun"
                elif self.get_next_backup_mon == "true":
                    self.next_day = "Mon"
                elif self.get_next_backup_tue == "true":
                    self.next_day = "Tue"

        if self.day_name == "Wed":
            if self.get_next_backup_wed == "true" and self.total_current_time < self.total_next_time:
                self.next_day = "Today"
            else:
                if self.get_next_backup_thu == "true":
                    self.next_day = "Thu"
                elif self.get_next_backup_fri == "true":
                    self.next_day = "Fri"
                elif self.get_next_backup_sat == "true":
                    self.next_day = "Sat"
                elif self.get_next_backup_sun == "true":
                    self.next_day = "Sun"
                elif self.get_next_backup_mon == "true":
                    self.next_day = "Mon"
                elif self.get_next_backup_tue == "true":
                    self.next_day = "Tue"
                elif self.get_next_backup_wed == "true":
                    self.next_day = "Wed"

        if self.day_name == "Thu":
            if self.get_next_backup_thu == "true" and self.total_current_time < self.total_next_time:
                self.next_day = "Today"
            else:
                if self.get_next_backup_fri == "true":
                    self.next_day = "Fri"
                elif self.get_next_backup_sat == "true":
                    self.next_day = "Sat"
                elif self.get_next_backup_sun == "true":
                    self.next_day = "Sun"
                elif self.get_next_backup_mon == "true":
                    self.next_day = "Mon"
                elif self.get_next_backup_tue == "true":
                    self.next_day = "Tue"
                elif self.get_next_backup_wed == "true":
                    self.next_day = "Wed"
                elif self.get_next_backup_thu == "true":
                    self.next_day = "Thu"

        if self.day_name == "Fri":
            if self.get_next_backup_fri == "true" and self.total_current_time < self.total_next_time:
                self.next_day = "Today"
            else:
                if self.get_next_backup_sat == "true":
                    self.next_day = "Sat"
                elif self.get_next_backup_sun == "true":
                    self.next_day = "Sun"
                elif self.get_next_backup_mon == "true":
                    self.next_day = "Mon"
                elif self.get_next_backup_tue == "true":
                    self.next_day = "Tue"
                elif self.get_next_backup_wed == "true":
                    self.next_day = "Wed"
                elif self.get_next_backup_thu == "true":
                    self.next_day = "Thu"
                elif self.get_next_backup_fri == "true":
                    self.next_day = "Fri"

        if self.day_name == "Sat":
            if self.get_next_backup_sat == "true" and self.total_current_time < self.total_next_time:
                self.next_day = "Today"
            else:
                if self.get_next_backup_sun == "true":
                    self.next_day = "Sun"
                elif self.get_next_backup_mon == "true":
                    self.next_day = "Mon"
                elif self.get_next_backup_tue == "true":
                    self.next_day = "Tue"
                elif self.get_next_backup_wed == "true":
                    self.next_day = "Wed"
                elif self.get_next_backup_thu == "true":
                    self.next_day = "Thu"
                elif self.get_next_backup_fri == "true":
                    self.next_day = "Fri"
                elif self.get_next_backup_sat == "true":
                    self.next_day = "Sat"

        ################################################################################
        ## Save next backup to user.ini
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'next', f'{self.next_day}, {self.get_next_hour}:{self.get_next_minute}')
            config.write(configfile)

        ################################################################################
        ## Print current time and day
        ################################################################################
        print("")
        print(f"Current time: {self.current_hour}:{self.current_minute}")
        print(f"Today is: {self.day_name}")
        print("")

    def automatically_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

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
            sub.Popen(f"rm {src_backup_check_desktop}", shell=True)  # Remove .desktop from dst

            # Set auto backup to false
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'auto_backup', 'false')
                config.write(configfile)

            print("Auto backup was successfully deactivated!")

        # Call backup check py
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)

    def external_clicked(self):
        # Choose external hd
        self.setEnabled(False)
        externalMain.show()     # Show external screen

    def backup_now_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Set backup now to true
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

            # Call backup now py
            sub.Popen(f"python3 {src_backup_now}", shell=True)

    def options_clicked(self):
        # Call schedule
        sub.call(f"python3 {src_options_py}", shell=True)

    def donate_clicked(self):
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)


# External Screen
class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        appIcon = QIcon(src_restore_icon)
        self.setWindowIcon(appIcon)
        self.setWindowTitle("External Screen")
        self.setFixedSize(400, 325)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        ################################################################################
        ## Media location
        ################################################################################
        self.foundInMedia = None
        self.media = "/media"
        self.run = "/run/media"

        # Read ini
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.getHDName = config['EXTERNAL']['name']

        self.widgets()

    def widgets(self):
        ################################################################################
        ## Frame
        ################################################################################
        self.where_frame = QFrame(self)
        self.where_frame.setFixedSize(360, 250)
        self.where_frame.move(20, 20)
        # self.where_frame.setStyleSheet("""
        #      border: 1px solid red;
        # """)

        ################################################################################
        ## Cancel button
        ################################################################################
        self.widget = QWidget(self)
        self.widget.setGeometry(290, 260, 150, 60)
        # self.widget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Left widget
        self.baseVCancelLayout = QVBoxLayout(self.widget)
        self.baseVCancelLayout.setSpacing(20)

        # Backup images
        self.button_where_cancel = QPushButton()
        self.button_where_cancel.setFont(QFont("Ubuntu", 10))
        self.button_where_cancel.setText("Cancel")
        self.button_where_cancel.setFixedSize(80, 34)
        self.button_where_cancel.clicked.connect(self.on_button_cancel_clicked)

        ################################################################################
        ## Add widgets and Layouts
        ################################################################################
        self.baseVCancelLayout.addWidget(self.button_where_cancel)

        self.check_connection_media()

    def check_connection_media(self):
        ################################################################################
        ## Search external inside media
        ################################################################################
        try:
            os.listdir(f'{self.media}/{user_name}')
            self.foundInMedia = True
            self.connected()

        except FileNotFoundError:
            self.check_connection_run()

    def check_connection_run(self):
        ################################################################################
        ## Search external inside run/media
        ################################################################################
        try:
            os.listdir(f'{self.run}/{user_name}')  # Opensuse, external is inside "/run"
            self.foundInMedia = False
            self.connected()

        except FileNotFoundError:
            print("No external devices mounted or available...")
            pass

    def connected(self):
        ################################################################################
        ## Add buttons and images for each external
        ################################################################################
        vertical = 20
        vertical_img = 32
        if self.foundInMedia:
            for output in os.listdir(f'{self.media}/{user_name}'):
                label_image = QLabel(self)
                pixmap = QPixmap(src_restore_small_icon)
                label_image.setPixmap(pixmap)
                label_image.setFixedSize(48, 48)
                label_image.move(30, vertical_img)
                vertical_img += 50

                # Button
                button = QPushButton(output, self.where_frame)
                button.setFixedSize(280, 30)
                button.move(60, vertical)
                vertical += 50
                text = button.text()
                button.show()
                button.clicked.connect(lambda ch: self.on_button_clicked(text))
        else:
            # Add buttons and images for each external
            for output in os.listdir(f'{self.run}/{user_name}'):
                label_image = QLabel(self)
                pixmap = QPixmap(src_restore_small_icon)
                label_image.setPixmap(pixmap)
                label_image.setFixedSize(48, 48)
                label_image.move(30, vertical_img)
                vertical_img += 50

                # Button
                button = QPushButton(output, self.where_frame)
                button.setFixedSize(280, 30)
                button.move(60, vertical)
                vertical += 50
                text = button.text()
                button.show()
                button.clicked.connect(lambda ch: self.on_button_clicked(text))

    def on_button_clicked(self, get):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Read/Load user.config (backup automatically)
        with open(src_user_config, 'w') as configfile:
            if self.foundInMedia:
                config.set(f'EXTERNAL', 'hd', f'{self.media}/{user_name}/{get}')

            else:
                config.set(f'EXTERNAL', 'hd', f'{self.run}/{user_name}/{get}')

            ################################################################################
            ## Write changes to ini
            ################################################################################
            config.set('EXTERNAL', 'name', get)
            config.write(configfile)

            self.close()
            main.setEnabled(True)

    def on_button_cancel_clicked(self):
        externalMain.close()
        main.setEnabled(True)


app = QApplication(sys.argv)
tic = time.time()
main = UI()
main.show()
externalMain = EXTERNAL()
toc = time.time()
print(f'Time Machine {(toc - tic):.4f} seconds')
app.exit(app.exec())
