#! /usr/bin/python3
from setup import *

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle(appName)
        self.setWindowIcon(QIcon(src_backup_icon))
        self.setFixedSize(700, 450)

        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.widgets()

    def widgets(self):
        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 200, 410)
        self.leftWidget.setStyleSheet("""
            border-right: 1px solid rgb(68, 69, 70);
        """)

        # Left layout
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(20)
        self.leftLayout.setContentsMargins(0, 0, 10, 0)

        # Backup images
        self.backupImageLabel = QLabel()
        self.backupImageLabel.setFixedSize(128, 128)
        self.backupImageLabel.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_backup_icon});"
            "border-color: transparent;"
            "background-repeat: no-repeat;"
            "}")

        # Automatically checkbox
        self.automaticallyCheckBox = QCheckBox()
        self.automaticallyCheckBox.setFont(QFont("Ubuntu", 10))
        self.automaticallyCheckBox.setText("Back Up Automatically")
        self.automaticallyCheckBox.adjustSize()
        self.automaticallyCheckBox.setStyleSheet("""
            border-color: transparent;
        """)
        self.automaticallyCheckBox.clicked.connect(self.automatically_clicked)

        ################################################################################
        # Right Widget
        ################################################################################
        self.rightWidget = QWidget(self)
        self.rightWidget.setGeometry(240, 40, 170, 154)
        # self.rightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right layout
        self.rightLayout = QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(20)

        # Restore images
        self.restoreImageLabel = QLabel()
        self.restoreImageLabel.setFixedSize(128, 128)
        self.restoreImageLabel.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_restore_icon});"
            "background-repeat: no-repeat;"
            "background-position: top;"
            "}")

        # Select disk button
        self.selectDiskButton = QPushButton(self)
        self.selectDiskButton.setFont(QFont("Ubuntu", 10))
        self.selectDiskButton.setText("Select Backup Disk...")
        self.selectDiskButton.adjustSize()
        self.selectDiskButton.clicked.connect(self.select_external_clicked)

        ################################################################################
        # Far right Widget
        ################################################################################
        self.farRightWidget = QWidget(self)
        self.farRightWidget.setContentsMargins(0, 0, 0, 0)
        self.farRightWidget.setGeometry(412, 40, 280, 120)
        # self.farRightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right widget
        self.farRightLayout = QVBoxLayout(self.farRightWidget)
        self.farRightLayout.setSpacing(0)

        ################################################################################
        # Set external name
        ################################################################################
        self.externalNameLabel = QLabel()
        self.externalNameLabel.setFont(bigTitle)
        self.externalNameLabel.setFixedSize(350, 80)
        self.externalNameLabel.setAlignment(QtCore.Qt.AlignLeft)

        ################################################################################
        # Get external size
        ################################################################################
        self.externalSizeLabel = QLabel()
        self.externalSizeLabel.setFont(item)
        self.externalSizeLabel.setFixedSize(200, 18)

        ################################################################################
        # Label last backup
        ################################################################################
        self.lastBackupLabel = QLabel()
        self.lastBackupLabel.setFont(item)
        self.lastBackupLabel.setText("Last Backup: None")
        self.lastBackupLabel.setFixedSize(200, 18)

        # Label last backup
        self.nextBackupLabel = QLabel()
        self.nextBackupLabel.setFont(item)
        self.nextBackupLabel.setText("Next Backup: None")
        self.nextBackupLabel.setFixedSize(250, 18)

        # Status Status
        self.externalStatusLabel = QLabel()
        self.externalStatusLabel.setFont(QFont('DejaVu Sans', 10))
        self.externalStatusLabel.setText("Status:")
        self.externalStatusLabel.setFixedSize(200, 18)

        ################################################################################
        # Extra information about an error
        ################################################################################
        self.extraInformationLabel = QLabel(self)
        self.extraInformationLabel.setFont(item)
        
        ################################################################################
        # Current backup label information
        ################################################################################
        self.currentBackUpLabel = QLabel(self)
        self.currentBackUpLabel.setFont(item)
        
        ################################################################################
        # Backup now button
        ################################################################################
        self.backupNowButton = QPushButton(self)
        self.backupNowButton.setText("Back Up Now")
        self.backupNowButton.setFont(QFont("Ubuntu", 10))
        # self.backupNowButton.setFixedSize(100, 28)
        self.backupNowButton.adjustSize()
        self.backupNowButton.move(420, 162)
        self.backupNowButton.clicked.connect(self.backup_now_clicked)
        self.backupNowButton.setEnabled(False)        

        ################################################################################
        # Description
        ################################################################################
        self.descriptionWidget = QWidget(self)
        self.descriptionWidget.setGeometry(240, 200, 440, 160)
        self.descriptionWidget.setStyleSheet("""
            border-top: 1px solid rgb(68, 69, 70);
        """)

        # Description Layout
        self.descriptionLayout = QVBoxLayout(self.descriptionWidget)

        # Description Title
        self.descriptionTitle = QLabel()
        self.descriptionTitle.setFont(topicTitle)
        self.descriptionTitle.setText(f"{appName} is able to:\n\n")
        self.descriptionTitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.descriptionTitle.setFixedSize(420, 24)
        self.descriptionTitle.setStyleSheet("""
            border-color: transparent;
            color: gray;
        """)

        # Description Text
        self.descriptionText = QLabel()
        self.descriptionText.setFont(item)
        self.descriptionText.setText(
            "* Keep local snapshots of your personal files as space permits\n"
            "* Keep Flatpaks Data and/or only Flatpaks installed names\n"
            "* Schedule backups Hourly or Daily\n"
            "* Will automatically back up at first boot, if time to do so\n   has passed.\n"
            "Delete the oldest backups when your disk becomes full.\n")
        self.descriptionText.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.descriptionText.adjustSize()
        self.descriptionText.setStyleSheet("""
            border-color: transparent;
            color: gray;
        """)

        ################################################################################
        # Donate and Settings buttons
        ################################################################################
        self.optionsWidget = QWidget(self)
        self.optionsWidget.setGeometry(340, 380, 350, 80)

        # Options Layout
        self.optionsLayout = QHBoxLayout(self.optionsWidget)
        self.optionsLayout.setSpacing(10)

        # Options button
        self.optionsButton = QPushButton()
        self.optionsButton.setText("Options...")
        self.optionsButton.setFont(QFont("Ubuntu", 10))
        # self.optionsButton.setFixedSize(80, 28)
        self.optionsButton.adjustSize()
        self.optionsButton.clicked.connect(self.options_clicked)

        # Show system tray
        self.showInSystemTrayCheckBox = QCheckBox(self)
        self.showInSystemTrayCheckBox.setFont(item)
        self.showInSystemTrayCheckBox.setText(f"Show {appName} in system tray")
        self.showInSystemTrayCheckBox.setFixedSize(280, 20)
        self.showInSystemTrayCheckBox.move(240, 410)
        self.showInSystemTrayCheckBox.setStyleSheet("""
            border-color: transparent;
        """)
        self.showInSystemTrayCheckBox.clicked.connect(self.system_tray_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left Layout
        self.leftLayout.addWidget(self.backupImageLabel, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.leftLayout.addWidget(self.automaticallyCheckBox, 1, Qt.AlignHCenter | Qt.AlignTop)

        #  Right Layout
        self.rightLayout.addWidget(self.restoreImageLabel, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.rightLayout.addWidget(self.selectDiskButton, 1, Qt.AlignVCenter | Qt.AlignHCenter)

        #  Far Right Layout
        self.farRightLayout.addWidget(self.externalNameLabel, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.externalSizeLabel, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.lastBackupLabel, 1, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.nextBackupLabel, 2, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.externalStatusLabel, 3, Qt.AlignLeft | Qt.AlignTop)

        # Description Layout
        self.descriptionLayout.addWidget(self.descriptionTitle, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.descriptionLayout.addWidget(self.descriptionText, 0, Qt.AlignVCenter | Qt.AlignLeft)

        #  Options layout
        self.optionsLayout.addWidget(self.optionsButton, 0, Qt.AlignRight | Qt.AlignVCenter)

        # Set Layouts
        self.setLayout(self.leftLayout)

        # Update
        timer.timeout.connect(self.read_ini_file)
        timer.start(1000) # Update every x seconds
        self.read_ini_file()

    def read_ini_file(self):
        print("Main window is running...")
        try:
            ################################################################################
            # Read INI file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            # Get current hour, minutes
            now = datetime.now()
            self.dayName = now.strftime("%a")
            self.currentHour = now.strftime("%H")
            self.currentMinute = now.strftime("%M")

            # INI file
            self.iniHDName = config['EXTERNAL']['name']
            self.iniExternalLocation = config['EXTERNAL']['hd']
            self.iniBackupNow = config['BACKUP']['backup_now']
            self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
            # self.iniBackupIsRunning = config['BACKUP']['checker_running']
            self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
            self.iniLastBackup = config['INFO']['latest']
            self.iniNextBackup = config['INFO']['next']

            # Mode
            self.oneTimeMode = config['MODE']['one_time_mode']

            # Dates
            self.nextDay = "None"
            self.iniNextHour = config['SCHEDULE']['hours']
            self.iniNextMinute = config['SCHEDULE']['minutes']
            self.iniNextBackupSun = config['SCHEDULE']['sun']
            self.iniNextBackupMon = config['SCHEDULE']['mon']
            self.iniNextBackupTue = config['SCHEDULE']['tue']
            self.iniNextBackupWed = config['SCHEDULE']['wed']
            self.iniNextBackupThu = config['SCHEDULE']['thu']
            self.iniNextBackupFri = config['SCHEDULE']['fri']
            self.iniNextBackupSat = config['SCHEDULE']['sat']
            self.everytime = config['SCHEDULE']['everytime']

            # Times
            self.currentTime = self.currentHour + self.currentMinute
            self.backupTime = self.iniNextHour + self.iniNextMinute

            # Current information about an error
            self.iniExtraInformation = config['INFO']['notification_add_info']
            
            # Current backup information
            self.iniCurrentBackupInfo = config['INFO']['feedback_status']
            
        except KeyError as keyError:
            print(keyError)
            print("Main window KeyError!")
            exit()

        self.check_connection()

    def check_connection(self):
         ################################################################################
        # External availability
        ################################################################################
        try:
            os.listdir(f"{media}/{userName}/{self.iniHDName}")  # Check if external can be found
            self.connected_connection()

        except FileNotFoundError:
            try:
                os.listdir(f"{run}/{userName}/{self.iniHDName}") 
                self.connected_connection()

            except FileNotFoundError:
                # Disable backup now button
                self.backupNowButton.setEnabled(False)    
                # Disconnected     
                self.externalStatusLabel.setText("Status: Disconnected")
                self.externalStatusLabel.setStyleSheet('color: red')
                self.externalStatusLabel.setAlignment(QtCore.Qt.AlignTop)
                self.externalSizeLabel.setText("No information available")

        self.set_external_name()

    def connected_connection(self):
        ################################################################################
        # External status
        ################################################################################
        self.externalStatusLabel.setText("Status: Connected")
        self.externalStatusLabel.setStyleSheet('color: green')
        
        try:
            # Clean notification info
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:  
                config.set('INFO', 'notification_add_info', ' ')
                config.write(configfile)

        except Exception as error:
            print(Exception)
            print("Main Window error!")
            exit()

        self.get_size_informations()

    def get_size_informations(self):
        ################################################################################
        # Get external size values
        ################################################################################
        try:
            # Get external max size
            externalMaxSize = os.popen(f"df --output=size -h {self.iniExternalLocation}")
            externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace(
                "Size", "").replace("\n", "").replace(" ", "")
            externalMaxSize = str(externalMaxSize)

            # Get external usded size
            usedSpace = os.popen(f"df --output=used -h {self.iniExternalLocation}")
            usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace(
                "Used", "").replace("\n", "").replace(" ", "")
            usedSpace = str(usedSpace)

            self.externalSizeLabel.setText(f"{usedSpace} of {externalMaxSize} available")

        except:
            self.externalSizeLabel.setText("No information available")

        self.condition()

    def condition(self):
        # User has select a backup device
        if self.iniHDName != "None":  
            # Show backup button if no back up is been made
            if self.iniBackupNow == "false":
                # Enable backup now button
                self.backupNowButton.setEnabled(True)

            else:
                # Disable backup now button
                self.backupNowButton.setEnabled(False)

        else:
            # Set external name
            self.externalNameLabel.setText("None")
            self.backupNowButton.setEnabled(False)

        self.set_external_name()

    def set_external_name(self):
        self.externalNameLabel.setText(self.iniHDName)

        self.set_external_last_backup()

    def set_external_last_backup(self):
        ################################################################################
        # Last backup label
        ################################################################################
        if self.iniLastBackup != "":
            self.lastBackupLabel.setText(f"Last Backup: {self.iniLastBackup}")

        self.load_time_backup()

    def load_time_backup(self):
        ################################################################################
        # Status for automaticallyCheckBox
        ################################################################################
        # if self.iniNextBackup != "":
        #     self.nextBackupLabel.setText(f"Next Backup: {self.iniNextBackup}")
        if self.automaticallyCheckBox.isChecked():
            if self.oneTimeMode == "true":
                self.nextBackupLabel.setText(f"Next Backup: {self.iniNextBackup}")
            else:
                if self.everytime == "60":
                    self.nextBackupLabel.setText("Next Backup: Every 1 hour")
                    self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

                elif self.everytime == "120":
                    self.nextBackupLabel.setText("Next Backup: Every 2 hours")
                    self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

                elif self.everytime == "240":
                    self.nextBackupLabel.setText("Next Backup: Every 4 hours")
                    self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))
        else:
            self.nextBackupLabel.setText("Next Backup: Automatic backups off")

        self.load_dates()

    def load_dates(self):
        # Days to run
        if self.dayName == "Sun":
            if self.iniNextBackupSun == "true" and self.currentHour <= self.iniNextHour and self.currentMinute <= self.iniNextMinute:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"

        if self.dayName == "Mon":
            if self.iniNextBackupMon == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"

        if self.dayName == "Tue":
            if self.iniNextBackupTue == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"

        if self.dayName == "Wed":
            if self.iniNextBackupWed == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"

        if self.dayName == "Thu":
            if self.iniNextBackupThu == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"

        if self.dayName == "Fri":
            if self.iniNextBackupFri == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"

        if self.dayName == "Sat":
            if self.iniNextBackupSat == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"

        # Save next backup to user.ini
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'next', f'{self.nextDay}, {self.iniNextHour}:{self.iniNextMinute}')
            config.write(configfile)

        self.load_current_backup_folder()

    def load_current_backup_folder(self):
        # Current backup folder been backup
        self.currentBackUpLabel.setText(self.iniCurrentBackupInfo)
        # Auto adjustSize for current backup folder
        self.currentBackUpLabel.adjustSize()

        self.load_extra_information()

    def load_extra_information(self):
        if self.iniExtraInformation != "":
            # Information about an error message
            self.extraInformationLabel.setText(self.iniExtraInformation)
            # Auto adjustSize label
            self.extraInformationLabel.adjustSize()
            # Show label
            self.extraInformationLabel.setEnabled(True)
        else:
            self.extraInformationLabel.setEnabled(False)

        self.load_automacically_backup()

    def load_automacically_backup(self):
        ################################################################################
        # Auto backup
        ################################################################################
        if self.iniHDName == "None":
            # Disable automatically backup checkbox
            self.automaticallyCheckBox.setEnabled(False)
        else:
            # Enable automatically backup checkbox
            self.automaticallyCheckBox.setEnabled(True)

        if self.iniAutomaticallyBackup == "true":
            self.automaticallyCheckBox.setChecked(True)
        else:
            self.automaticallyCheckBox.setChecked(False)
        
        self.load_system_tray()

    def load_system_tray(self):
        ################################################################################
        # System tray
        ################################################################################
        if self.iniSystemTray == "true":
            self.showInSystemTrayCheckBox.setChecked(True)

        else:
            self.showInSystemTrayCheckBox.setChecked(False)

    def automatically_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:  
            if self.automaticallyCheckBox.isChecked():
                if not os.path.exists(src_backup_check_desktop):
                    # Copy .desktop to user folder (Autostart .desktop)
                    shutil.copy(src_backup_check, src_backup_check_desktop)  

                config.set('BACKUP', 'auto_backup', 'true')
                config.write(configfile)

                # Backup checker
                sub.Popen(f"python3 {src_backup_check_py}", shell=True)
                # Set checker running to true
                with open(src_user_config, 'w') as configfile:
                    config.set('BACKUP', 'checker_running', "true")
                    config.write(configfile)

                print("Auto backup was successfully activated!")
     
            else:
                config.set('BACKUP', 'auto_backup', 'false')
                config.write(configfile)    
                
                # Set checker running to false
                with open(src_user_config, 'w') as configfile:
                    config.set('BACKUP', 'checker_running', "false")
                    config.write(configfile)

                print("Auto backup was successfully deactivated!")

    def system_tray_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.showInSystemTrayCheckBox.isChecked():
                config.set('SYSTEMTRAY', 'system_tray', 'true')
                config.write(configfile)

                print("System tray was successfully enabled!")

            else:
                config.set('SYSTEMTRAY', 'system_tray', 'false')
                config.write(configfile)

                print("System tray was successfully disabled!")

        ################################################################################
        # Call system tray
        # System tray can check if is not already runnnig
        ################################################################################
        sub.Popen(f"python3 {src_system_tray}", shell=True)

    def select_external_clicked(self):
        sub.run(f"python3 {src_search_for_devices}", shell=True)

    def backup_now_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile: # Set backup now to true
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        sub.Popen(f"python3 {src_backup_now}", shell=True)

    def options_clicked(self):
        sub.run(f"python3 {src_options_py}", shell=True)


app = QApplication(sys.argv)
main = UI()
main.show()
app.exit(app.exec())
