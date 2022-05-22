from setup import *

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setWindowTitle(appName)
        app_icon = QIcon(src_restore_icon)
        self.setWindowIcon(app_icon)
        self.setFixedSize(700, 450)

        ################################################################################
        ## Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.widgets()

    def widgets(self):
        ################################################################################
        ## Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 200, 410)
        self.leftWidget.setStyleSheet("""
            border-right: 1px solid rgb(68, 69, 70);
        """)

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
            "border-color: transparent;"
            "}")

        # Auto checkbox
        self.autoCheckbox = QCheckBox()
        self.autoCheckbox.setFont(item)
        self.autoCheckbox.setText("Back Up Automatically")
        self.autoCheckbox.setFixedSize(175, 20)
        self.autoCheckbox.setStyleSheet("""
            border-color: transparent;
        """)
        self.autoCheckbox.clicked.connect(self.automatically_clicked)

        ################################################################################
        ## Right Widget
        ################################################################################
        self.rightWidget = QWidget(self)
        self.rightWidget.setGeometry(240, 40, 170, 154)
        # self.rightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right widget
        self.baseVRightLayout = QVBoxLayout(self.rightWidget)
        self.baseVRightLayout.setSpacing(20)

        # Restore images
        self.restoreImage = QLabel()
        self.restoreImage.setFixedSize(84, 84)
        self.restoreImage.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_restore_icon});"
            "background-repeat: no-repeat;"
            "}")

        # Select disk button
        self.externalButton = QPushButton(self)
        self.externalButton.setFont(item)
        self.externalButton.setText("Select Backup Disk...")
        self.externalButton.setFixedSize(150, 28)
        self.externalButton.clicked.connect(self.external_clicked)

        ################################################################################
        ## Far right Widget
        ################################################################################
        self.farRightWidget = QWidget(self)
        self.farRightWidget.setContentsMargins(0, 0, 0, 0)
        self.farRightWidget.setGeometry(412, 40, 280, 120)
        # self.farRightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right widget
        self.baseVFarRightLayout = QVBoxLayout(self.farRightWidget)
        self.baseVFarRightLayout.setSpacing(0)

        ################################################################################
        ## Set external name
        ################################################################################
        self.setExternalName = QLabel()
        self.setExternalName.setFont(bigTitle)
        self.setExternalName.setAlignment(QtCore.Qt.AlignLeft)

        ################################################################################
        ## Get external size
        ################################################################################
        self.showExternalSize = QLabel()
        self.showExternalSize.setFont(item)
        self.showExternalSize.setFixedSize(200, 18)

        ################################################################################
        ## Label last backup
        ################################################################################
        self.lastBackupLabel = QLabel()
        self.lastBackupLabel.setFont(item)
        self.lastBackupLabel.setText("Last Backup:")
        self.lastBackupLabel.setFixedSize(200, 18)

        # Label last backup
        self.nextBackupLabel = QLabel()
        self.nextBackupLabel.setFont(item)
        self.nextBackupLabel.setText("Next Backup:")
        self.nextBackupLabel.setFixedSize(250, 18)

        # Status external hd
        self.externalStatus = QLabel()
        self.externalStatus.setFont(item)
        self.externalStatus.setText("External HD:")
        self.externalStatus.setFixedSize(200, 18)

        ################################################################################
        ## Preparing backup
        ################################################################################
        self.gif = QLabel(self)
        self.gif.move(420, 154)
        self.gif.setStyleSheet(
            "QLabel"
            "{"
            "background-color: transparent;"
            "border: 0px;"
            "}")

        # set qmovie as gif
        self.movie = QMovie(src_loadingGif)
        self.movie.setScaledSize(QSize().scaled(22, 22, Qt.KeepAspectRatio))
        self.gif.setMovie(self.movie)

        ################################################################################
        ## Backup now button
        ################################################################################
        self.backupNowButton = QPushButton("Back Up Now", self)
        self.backupNowButton.setFixedSize(100, 28)
        self.backupNowButton.move(420, 155)
        self.backupNowButton.clicked.connect(self.backup_now_clicked)
        self.backupNowButton.hide()

        ################################################################################
        ## Ui description
        ################################################################################
        self.uiTextWidget = QWidget(self)
        self.uiTextWidget.setGeometry(240, 200, 440, 140)
        self.uiTextWidget.setStyleSheet("""
            border-top: 1px solid rgb(68, 69, 70);
        """)

        # uiInfoTitle widget
        self.baseVUiTextLayout = QVBoxLayout(self.uiTextWidget)

        self.uiInfoTitle = QLabel()
        self.uiInfoTitle.setFont(topicTitle)
        self.uiInfoTitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.uiInfoTitle.setFixedSize(420, 24)
        self.uiInfoTitle.setStyleSheet("""
            border-color: transparent;

        """)
        self.uiInfoTitle.setText(
            f"{appName} is able to:\n\n")

        # uiInfoText
        self.uiInfoText = QLabel()
        self.uiInfoText.setFont(item)
        self.uiInfoText.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.uiInfoText.setFixedSize(420, 120)
        self.uiInfoText.setStyleSheet("""
            border-color: transparent;
        """)
        self.uiInfoText.setText(
            "* Keep local snapshots as space permits\n"
            "* Schedule backups (Minutely, Hourly or Daily)\n"
            f"* Automatically back up at first PC boot, if backup time\n   has passed.\n\n"
            "Delete the oldest backups when your disk becomes full.\n")

        ################################################################################
        ## Donate and Settings buttons
        ################################################################################
        self.optionsWidget = QWidget(self)
        self.optionsWidget.setGeometry(340, 380, 350, 80)
        # self.optionsWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Options layout
        self.optionsLayout = QHBoxLayout(self.optionsWidget)
        self.optionsLayout.setSpacing(10)

        # Settings buton
        self.optionsButton = QPushButton()
        self.optionsButton.setText("Options...")
        self.optionsButton.setFont(item)
        self.optionsButton.setFixedSize(80, 28)
        self.optionsButton.clicked.connect(self.options_clicked)

        # Auto checkbox
        self.showInSystemTray = QCheckBox(self)
        self.showInSystemTray.setFont(item)
        self.showInSystemTray.setText(f"Show {appName} in system tray (alpha)")
        self.showInSystemTray.setFixedSize(280, 20)
        self.showInSystemTray.move(240, 410)
        self.showInSystemTray.setStyleSheet("""
            border-color: transparent;
        """)
        self.showInSystemTray.clicked.connect(self.menu_bar_clicked)

        ################################################################################
        ## Add widgets and Layouts
        ################################################################################
        # BaseVLeftlayout
        self.baseVLeftLayout.addWidget(self.backupImage, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.baseVLeftLayout.addWidget(self.autoCheckbox, 1, Qt.AlignHCenter | Qt.AlignTop)

        #  baseVRight layout
        self.baseVRightLayout.addWidget(self.restoreImage, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.baseVRightLayout.addWidget(self.externalButton, 1, Qt.AlignVCenter | Qt.AlignHCenter)

        #  baseVFarRight layout
        self.baseVFarRightLayout.addWidget(self.setExternalName, 0, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addWidget(self.showExternalSize, 0, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addWidget(self.lastBackupLabel, 1, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addWidget(self.nextBackupLabel, 2, Qt.AlignLeft | Qt.AlignTop)
        self.baseVFarRightLayout.addWidget(self.externalStatus, 3, Qt.AlignLeft | Qt.AlignTop)

        #  baseVUiText layout
        self.baseVUiTextLayout.addWidget(self.uiInfoTitle, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseVUiTextLayout.addWidget(self.uiInfoText, 0, Qt.AlignVCenter | Qt.AlignLeft)

        #  Options layout
        self.optionsLayout.addWidget(self.optionsButton, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.setLayout(self.baseVLeftLayout)

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
            self.getExternalLocation = config['EXTERNAL']['hd']
            self.get_backup_now = config['BACKUP']['backup_now']
            self.getCheckerRunning = config['BACKUP']['checker_running']
            self.getAutoBackup = config['BACKUP']['auto_backup']
            self.getSystemTray = config['SYSTEMTRAY']['system_tray']
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
            os.listdir(f"/media/{userName}/{self.getHDName}")  # Check if external can be found
            self.connected()

        except FileNotFoundError:
            self.check_connection_run()

    def check_connection_run(self):
        try:
            os.listdir(f"/run/media/{userName}/{self.getHDName}")  # Opensuse, external is inside "/run"

            self.connected()

        except FileNotFoundError:
            self.backupNowButton.hide()  # Hide backup now button

            # External status
            self.externalStatus.setText("External HD: Disconnected")
            self.externalStatus.setFont(QFont('DejaVu Sans', 10))
            self.externalStatus.setStyleSheet('color: red')
            self.externalStatus.setAlignment(QtCore.Qt.AlignTop)

            ################################################################################
            ## External size
            ################################################################################
            self.showExternalSize.setText("No information available")

        self.ui_settings()

    def connected(self):
        ################################################################################
        ## External status
        ################################################################################
        self.externalStatus.setText("External HD: Connected")
        self.externalStatus.setFont(QFont('DejaVu Sans', 10))
        self.externalStatus.setStyleSheet('color: green')

        ################################################################################
        ## Get external size values
        ################################################################################
        try:
            externalMaxSize = os.popen(f"df --output=size -h {self.getExternalLocation}")
            externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace("Size", "").replace(
                "\n", "").replace(" ", "")
            externalMaxSize = str(externalMaxSize)

            usedSpace = os.popen(f"df --output=used -h {self.getExternalLocation}")
            usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace("Used", "").replace(
                "\n", "").replace(" ", "")
            usedSpace = str(usedSpace)

            self.showExternalSize.setText(f"{usedSpace} of {externalMaxSize} available")

        except:
            self.showExternalSize.setText("No information available")

        ################################################################################
        ## Condition
        ################################################################################
        if self.getHDName != "None":  # If location can be found
            if self.get_backup_now == "false":  # If is not backing up right now
                ################################################################################
                ## Hide loading gif
                ################################################################################
                self.movie.stop()

                ################################################################################
                ## Backup Now
                ################################################################################
                self.backupNowButton.setEnabled(True)  # Disable backup now button
                self.backupNowButton.setFixedSize(120, 28)  # Resize backup button
                self.backupNowButton.show()

            else:
                ################################################################################
                ## Show loading gif
                ################################################################################
                self.movie.start()

                ################################################################################
                ## Hide backup now button
                ################################################################################
                self.backupNowButton.hide()

        else:
            ################################################################################
            ## Hide backup now button
            ################################################################################
            self.backupNowButton.hide()

        self.ui_settings()

    def ui_settings(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        ################################################################################
        ## Set None if user has not choose a external device yet
        ################################################################################
        self.setExternalName.setText(self.getHDName)  # Set external name
        self.setExternalName.setFont(QFont('DejaVu Sans', 18))

        ################################################################################
        ## External name
        ################################################################################
        if self.getHDName != "None":
            self.setExternalName.setText(self.getHDName)

        ################################################################################
        ## Last backup label
        ################################################################################
        if self.get_last_backup == "":
            self.lastBackupLabel.setText("Last Backup: ")
        else:
            self.lastBackupLabel.setText(f"Last Backup: {self.get_last_backup}")

        ################################################################################
        ## Next backup label
        ################################################################################
        if self.get_next_backup == "":
            self.nextBackupLabel.setText("Next Backup: None")

        ################################################################################
        ## Auto backup
        ################################################################################
        if self.getAutoBackup == "true":
            self.autoCheckbox.setChecked(True)

        else:
            self.autoCheckbox.setChecked(False)

        if not self.autoCheckbox.isChecked():
            self.nextBackupLabel.setText("Next Backup: Automatic backups off")

        else:
            self.nextBackupLabel.setText(f"Next Backup: {self.get_next_backup}")

        ################################################################################
        ## System tray
        ################################################################################
        if self.getSystemTray == "true":
            self.showInSystemTray.setChecked(True)

        else:
            self.showInSystemTray.setChecked(False)

        ################################################################################
        ## Next backup label everytime
        ################################################################################
        if self.more_time_mode == "true" and self.everytime == "15":
            self.nextBackupLabel.setText("Next Backup: Every 15 minutes")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        if self.more_time_mode == "true" and self.everytime == "30":
            self.nextBackupLabel.setText("Next Backup: Every 30 minutes")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        if self.more_time_mode == "true" and self.everytime == "60":
            self.nextBackupLabel.setText("Next Backup: Every 1 hour")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        if self.more_time_mode == "true" and self.everytime == "120":
            self.nextBackupLabel.setText("Next Backup: Every 2 hours")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        if self.more_time_mode == "true" and self.everytime == "240":
            self.nextBackupLabel.setText("Next Backup: Every 4 hours")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

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
        ################################################################################
        ## If automatically is selected
        ################################################################################
        if self.autoCheckbox.isChecked():
            if os.path.exists(src_backup_check_desktop):
                pass

            else:
                shutil.copy(src_backup_check, src_backup_check_desktop)  # Copy to /home/#USER/.config/autostart

            ################################################################################
            ## Set auto backup to true
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            with open(src_user_config, 'w') as configfile:  # Set auto backup to true
                config.set('BACKUP', 'auto_backup', 'true')
                config.set('BACKUP', 'checker_running', 'true')
                config.write(configfile)

                print("Auto backup was successfully activated!")

        else:
            config = configparser.ConfigParser()
            config.read(src_user_config)

            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'auto_backup', 'false')
                config.set('BACKUP', 'checker_running', 'false')
                config.write(configfile)

                print("Auto backup was successfully deactivated!")

        ################################################################################
        ## Call backup check py
        ################################################################################
        sub.Popen(f"python3 {src_backup_check_py}", shell=True)

    def menu_bar_clicked(self):
        ################################################################################
        ## Menu bar selected
        ################################################################################
        if self.showInSystemTray.isChecked():
            ################################################################################
            ## Write to ini file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            with open(src_user_config, 'w') as configfile:  # Set auto backup to true
                config.set('SYSTEMTRAY', 'system_tray', 'true')
                config.write(configfile)

                print("System tray was successfully enabled!")

        else:
            ################################################################################
            ## Write to ini file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            with open(src_user_config, 'w') as configfile:
                config.set('SYSTEMTRAY', 'system_tray', 'false')
                config.write(configfile)

                print("Menu bar was successfully disabled!")

        ################################################################################
        ## Call backup check py
        ################################################################################
        sub.Popen(f"python3 {src_system_tray}", shell=True)

    def external_clicked(self):
        # Choose external hd
        self.setEnabled(False)
        externalMain.show()  # Show Choose external:

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
        sub.run(f"python3 {src_options_py}", shell=True)


################################################################################
## Show external option to back up
################################################################################
class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        appIcon = QIcon(src_restore_icon)
        self.setWindowIcon(appIcon)
        self.setWindowTitle("Choose external:")
        self.setFixedSize(500, 380)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        ################################################################################
        ## Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        ################################################################################
        ## Media location
        ################################################################################
        self.foundInMedia = None
        self.media = "/media"
        self.run = "/run/media"

        ################################################################################
        ## Read ini
        ################################################################################
        # config = configparser.ConfigParser()
        # config.read(src_user_config)
        # self.getHDName = config['EXTERNAL']['name']
        # self.getMode = config['EXTERNAL']['mode']

        ################################################################################
        ## FileBrowser
        ################################################################################
        # self.dirpath = QDir.currentPath()

        # self.label = QLabel(self)
        # # self.label.setText(title)
        # self.label.setFixedWidth(65)
        # self.label.setFont(QFont("Arial",10))
        # self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.widgets()

    def widgets(self):
        ################################################################################
        ## Frame
        ################################################################################
        self.whereFrame = QFrame(self)
        self.whereFrame.setFixedSize(460, 280)
        self.whereFrame.move(20, 40)
        self.whereFrame.setStyleSheet("""
            background-color: rgb(48, 49, 50);
        """)

        # ################################################################################
        # ## Radio local
        # ################################################################################
        # self.local = QRadioButton(self)
        # self.local.setFont(item)
        # self.local.setText("Local storage")
        # self.local.setToolTip("Use this options if you plan to back up to a: USB/HD/SSD,\n"
        #                       "that is directly connected to your pc")
        # self.local.setFixedSize(150, 24)
        # self.local.move(20, 10)
        # self.local.setEnabled(False)
        # self.local.autoExclusive()
        # self.local.setStyleSheet("""
        #      border: 1px solid red;
        # """)

        ################################################################################
        ## Radio network
        ################################################################################
        # self.network = QRadioButton(self)
        # self.network.setFont(item)
        # self.network.setText("Remote storage")
        # self.network.setToolTip("Use this options if you plan to back up via network (LAN)")
        # self.network.setFixedSize(150, 24)
        # self.network.move(20, 305)
        # self.network.setEnabled(False)
        # self.network.autoExclusive()
        # self.network.setStyleSheet("""
        #      border: 1px solid red;
        # """)

        ###############################################################################
        ## Radio network
        ################################################################################
        # self.lineEdit = QLineEdit(self)
        # self.lineEdit.setFont(item)
        # self.lineEdit.setPlaceholderText("Example: ssh USER@xx.xxx.xxx.xx")
        # self.lineEdit.setFixedWidth(210)
        # self.lineEdit.move(180, 305)
        # self.lineEdit.setEnabled(False)
        # self.lineEdit.setStyleSheet("""
        #     color: gray;
        # """)

        ################################################################################
        ## Choose button
        ################################################################################
        # self.connectTo = QPushButton(self)
        # self.connectTo.setFont(item)
        # self.connectTo.setText("Connect")
        # self.connectTo.setEnabled(False)
        # self.connectTo.setFixedSize(80, 28)
        # self.connectTo.move(400, 300)
        # self.connectTo.setStyleSheet(
        #     "QPushButton::hover"
        #     "{"
        #     "background-color: red;"
        #     "}")
        # # self.connectTo.clicked.connect(self.on_choose_button_clicked)
        # self.connectTo.clicked.connect(lambda *args: print("Clicked"))

        ################################################################################
        ## Cancel button
        ################################################################################
        # self.widget = QWidget(self)
        # self.widget.setGeometry(290, 260, 150, 110)
        # self.widget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Backup images
        self.cancelButton = QPushButton(self)
        self.cancelButton.setFont(item)
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFixedSize(80, 28)
        self.cancelButton.move(400, 340)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        self.check_connection_media()

    def check_connection_media(self):
        ################################################################################
        ## Search external inside media
        ################################################################################
        try:
            os.listdir(f'{self.media}/{userName}')
            self.foundInMedia = True
            self.show_one_screen()

        except FileNotFoundError:
            self.check_connection_run()

    def check_connection_run(self):
        ################################################################################
        ## Search external inside run/media
        ################################################################################
        try:
            os.listdir(f'{self.run}/{userName}')  # Opensuse, external is inside "/run"
            self.foundInMedia = False
            self.show_one_screen()

        except FileNotFoundError:
            print("No external devices mounted or available...")
            pass

    def show_one_screen(self):
        ################################################################################
        ## Check source
        ################################################################################
        if self.foundInMedia:
            self.foundWhere = self.media
        else:
            self.foundWhere = self.run

        ################################################################################
        ## Add buttons and images for each external
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        vertical = 20
        verticalImg = 52
        for output in os.listdir(f'{self.foundWhere}/{userName}'):
            image = QLabel(self)
            pixmap = QPixmap(src_restore_small_icon)
            image.setPixmap(pixmap)
            image.setFixedSize(48, 48)
            image.move(30, verticalImg)
            verticalImg += 50

            # Button
            button = QPushButton(output, self.whereFrame)
            button.setFixedSize(380, 30)
            button.move(60, vertical)
            button.setFont(item)
            button.setCheckable(True)
            text = button.text()
            button.setStyleSheet("""
                color: white;
            """)

            ################################################################################
            ## Auto checked this choosed external device
            ################################################################################
            if text == main.getHDName:
                button.setChecked(True)

            vertical += 50
            button.show()
            button.clicked.connect(lambda *args, text=text: self.on_button_clicked(text))

    def on_button_clicked(self, get):
        ################################################################################
        ## Check for spaces inside output and sort them
        ################################################################################
        if " " in get:
            get = str(get)
            get = get.replace(" ", "\ ")
            print("Remove spaces: " + get)

        ################################################################################
        ## Write changes to ini
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set(f'EXTERNAL', 'hd', f'{self.foundWhere}/{userName}/{get}')
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
print(f'{appName} {(toc - tic):.4f} seconds')
app.exit(app.exec())
