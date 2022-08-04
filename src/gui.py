#! /usr/bin/python3
from setup import *

# QTimer
timer = QtCore.QTimer()


class MAIN(QMainWindow):
    def __init__(self):
        super(MAIN, self).__init__()

        self.iniUI()

    def iniUI(self):
        # self.setWindowTitle(appName)
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
        # border-right: 1px solid rgb(68, 69, 70);
        self.leftWidget.setStyleSheet("""
            border-right: 1px solid rgb(198, 198, 198);
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
        self.backupNowButton.adjustSize()
        self.backupNowButton.move(420, 159)
        self.backupNowButton.clicked.connect(self.backup_now_clicked)
        self.backupNowButton.setEnabled(False)        

        ################################################################################
        # Description
        ################################################################################
        self.descriptionWidget = QWidget(self)
        self.descriptionWidget.setGeometry(240, 200, 440, 160)
        self.descriptionWidget.setStyleSheet("""
            border-top: 1px solid rgb(198, 198, 198);
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
        self.optionsButton.clicked.connect(self.on_options_clicked)

        # Help button
        self.helpButton = QPushButton()
        self.helpButton.setText("?")
        self.helpButton.setFont(QFont("Ubuntu", 10))
        self.helpButton.setFixedSize(24, 24)
        self.helpButton.clicked.connect(
            lambda: sub.Popen(f"xdg-open {githubHome}", shell=True))
        
        # Show system tray
        self.showInSystemTrayCheckBox = QCheckBox(self)
        self.showInSystemTrayCheckBox.setFont(item)
        self.showInSystemTrayCheckBox.setText(f"Show {appName} in menu bar")
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
        self.optionsLayout.addStretch()
        self.optionsLayout.addWidget(self.optionsButton, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.optionsLayout.addWidget(self.helpButton, 0, Qt.AlignRight | Qt.AlignVCenter)

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
            pass
            
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
        
        # try:
        #     # Clean notification info
        #     config = configparser.ConfigParser()
        #     config.read(src_user_config)
        #     with open(src_user_config, 'w') as configfile:
        #         config.set('INFO', 'notification_add_info', ' ')
        #         config.write(configfile)

        # except Exception as error:
        #     print(Exception)
        #     print("Main Window error!")
        #     exit()

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
        self.setEnabled(False)
        # mainDevices = EXTERNAL()
        mainDevices.show()

    def backup_now_clicked(self):
        sub.Popen(f"python3 {src_backup_now}", shell=True)

    def on_options_clicked(self):
        # self.setMinimumSize(800, 550)
        widget.setCurrentWidget(mainOpitions)
        # sub.run(f"python3 {src_options_py}", shell=True)

class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        self.foundInMedia = None
        self.chooseDevice = ()
        self.captureDevices = []

        self.iniUI()

    def iniUI(self):
        windowXSize = 500
        windowYSize = 380

        self.setWindowIcon(QIcon(src_backup_icon))
        self.setFixedSize(windowXSize, windowYSize)
        # self.setFixedSize(windowXSize, windowYSize)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft().x(), fg.topLeft().y())

        self.read_ini_file()

    def read_ini_file(self):
        # Read INI file
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniHDName = config['EXTERNAL']['name']

        self.widgets()

    def widgets(self):
        ################################################################################
        # Frame
        ################################################################################
        self.whereFrame = QFrame()
        self.whereFrame.setFixedSize(440, 280)
        self.whereFrame.move(20, 40)

        # Scroll
        self.scroll = QScrollArea(self)
        self.scroll.setFixedSize(460, 280)
        self.scroll.move(20, 40)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.whereFrame)

        # Vertical layout V
        self.verticalLayout = QVBoxLayout(self.whereFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        
        # Cancel button
        self.cancelButton = QPushButton(self)
        self.cancelButton.setFont(item)
        self.cancelButton.setText("Cancel")
        self.cancelButton.adjustSize()
        self.cancelButton.move(300, 340)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        # Use this device
        self.useDiskButton = QPushButton(self)
        self.useDiskButton.setFont(item)
        self.useDiskButton.setText("Use Disk")
        self.useDiskButton.adjustSize()
        # self.useDiskButton.setFixedSize(80, 28)
        self.useDiskButton.move(400, 340)
        self.useDiskButton.setEnabled(False)
        self.useDiskButton.clicked.connect(self.on_use_disk_clicked)

        # Update
        timer.timeout.connect(self.check_connection)
        timer.start(2000) # Update every x seconds
        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside media
        ################################################################################
        print("Searching for backup devices...")
        try:
            if len(os.listdir(f'{media}/{userName}')) != 0:
                print("Found device(s) inside Run")
                self.foundInMedia = True
                self.where(media)

            else:
                for i in range(len(self.captureDevices)):
                    item = self.verticalLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1

        except FileNotFoundError:
            if len(os.listdir(f'{run}/{userName}')) != 0:
                print("Found device(s) inside Run")
                self.foundInMedia = False
                self.where(run)

            else:
                try:
                    print(self.captureDevices)
                    print(len(self.captureDevices))
                    for i in range(len(self.captureDevices)):
                        item = self.verticalLayout.itemAt(i)
                        widget = item.widget()
                        widget.deleteLater()
                        i -= 1

                except:
                    self.captureDevices.clear()
                    pass

    def where(self, location):
        # Gettíng devices locations
        if self.foundInMedia:
            self.foundWhere = media
        else:
            self.foundWhere = run

        self.show_on_screen(location)

    def show_on_screen(self, location):
        print("Showing available devices")

        ################################################################################
        # Add buttons and images for each external
        ################################################################################
        # If not already in list, add
        for output in os.listdir(f'{location}/{userName}'):
            if output not in self.captureDevices:
                # If device is in list, display to user just on time per device
                self.captureDevices.append(output)

                # Avaliables external  devices
                self.availableDevices = QPushButton(self.whereFrame)
                self.availableDevices.setFont(QFont('Ubuntu', 12))
                self.availableDevices.setText(output)
                self.availableDevices.setFixedSize(444, 60)
                self.availableDevices.setCheckable(True)
                text = self.availableDevices.text()
                self.availableDevices.clicked.connect(lambda *args, text=text: self.on_device_clicked(text))

                # Image
                image = QLabel(self.availableDevices)
                image.setFixedSize(46, 46)
                image.move(6, 6)
                image.setStyleSheet(
                    "QLabel"
                    "{"
                    f"background-image: url({src_restore_small_icon});"
                    "background-repeat: no-repeat;"
                    "background-position: center;"
                    "}")

                ################################################################################
                # Auto checked this choosed external device
                ################################################################################
                if text == self.iniHDName:
                    self.availableDevices.setChecked(True)

                ################################################################################
                # Add widgets and Layouts
                ################################################################################
                # Vertical layout
                self.verticalLayout.addWidget(self.availableDevices, 0, QtCore.Qt.AlignHCenter)

            # If x device is removed or unmounted, remove from screen
            for output in self.captureDevices:
                if output not in os.listdir(f'{location}/{userName}'):
                    # Current output index
                    index = self.captureDevices.index(output)
                    # Remove from list
                    self.captureDevices.remove(output)             
                    # Delete from screen
                    item = self.verticalLayout.itemAt(index)
                    widget = item.widget()
                    widget.deleteLater()
                    index -= 1

    def on_use_disk_clicked(self):
        print(self.chooseDevice)
        ################################################################################
        # Adapt external name is it has space in the name
        ################################################################################
        if " " in self.chooseDevice:
            self.chooseDevice = str(self.chooseDevice.replace(" ", "\ "))

        ################################################################################
        # Update INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set(f'EXTERNAL', 'hd', f'{self.foundWhere}/{userName}/{self.chooseDevice}')
            config.set('EXTERNAL', 'name', f'{self.chooseDevice}')
            config.write(configfile)

        main.setEnabled(True)
        self.close()

    def on_device_clicked(self, output):
        if self.availableDevices.isChecked():
            self.chooseDevice = output
            # Enable use disk
            self.useDiskButton.setEnabled(True)
        else:
            self.chooseDevice = ""
            # Disable use disk
            self.useDiskButton.setEnabled(False)

    def on_button_cancel_clicked(self):
        mainDevices.close()
        main.setEnabled(True)

class OPTION(QMainWindow):
    def __init__(self):
        super(OPTION, self).__init__()

        self.iniUI()

    def iniUI(self):
        self.setWindowIcon(QIcon(src_backup_icon))

        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.widgets()

    def widgets(self):
        # Apps version
        version = QLabel(self)
        version.setFont(QFont("Ubuntu", 10))
        version.setText(appVersion)
        version.setFixedSize(80, 20)
        version.move(270, 505)

        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 240, 405)
   
        # Scroll
        self.scroll = QScrollArea(self)
        self.scroll.setFixedSize(240, 405)
        self.scroll.move(20, 20)
        self.scroll.setWidgetResizable(True)
        # self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.leftWidget)

        # Left layout
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setContentsMargins(10, 10, 10, 10)

        # Left title
        self.leftTitle = QLabel()
        self.leftTitle.setFont(QFont("Ubuntu", 11))
        self.leftTitle.setText("Available folders to be\nback up:")
        self.leftTitle.adjustSize()

        # Frame
        self.leftFrame = QFrame()
        self.leftFrame.adjustSize()
   
        ################################################################################
        # Days to run widget
        ################################################################################
        self.daysToRunWidget = QWidget(self)
        self.daysToRunWidget.setGeometry(280, 20, 390, 80)
        self.daysToRunWidget.setStyleSheet("""
            border-top: 1px solid rgb(198, 198, 198);
        """)

        # Days to run layout V
        self.daysToRunLayoutV = QVBoxLayout(self.daysToRunWidget)
        self.daysToRunLayoutV.setSpacing(10)

        # Days to run layout H
        self.daysToRunLayoutH = QHBoxLayout()
        self.daysToRunLayoutH.setSpacing(10)

        # Days to run title
        self.daysToRunTitle = QLabel()
        self.daysToRunTitle.setFont(QFont("Ubuntu", 11))
        self.daysToRunTitle.setText("Days to run:")
        self.daysToRunTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.daysToRunTitle.setFixedSize(180, 30)
        self.daysToRunTitle.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Checkboxes
        ################################################################################
        self.sunCheckBox = QCheckBox()
        self.sunCheckBox.setFont(QFont("Ubuntu", 10))
        self.sunCheckBox.setText("Sun")
        self.sunCheckBox.clicked.connect(self.on_check_sun_clicked)
        self.sunCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.monCheckBox = QCheckBox()
        self.monCheckBox.setFont(QFont("Ubuntu", 10))
        self.monCheckBox.setText("Mon")
        self.monCheckBox.clicked.connect(self.on_check_mon_clicked)
        self.monCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.tueCheckBox = QCheckBox()
        self.tueCheckBox.setFont(QFont("Ubuntu", 10))
        self.tueCheckBox.setText("Tue")
        self.tueCheckBox.clicked.connect(self.on_check_tue_clicked)
        self.tueCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.wedCheckBox = QCheckBox()
        self.wedCheckBox.setFont(QFont("Ubuntu", 10))
        self.wedCheckBox.setText("Wed")
        self.wedCheckBox.clicked.connect(self.on_check_wed_clicked)
        self.wedCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.thuCheckBox = QCheckBox()
        self.thuCheckBox.setFont(QFont("Ubuntu", 10))
        self.thuCheckBox.setText("Thu")
        self.thuCheckBox.clicked.connect(self.on_check_thu_clicked)
        self.thuCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.friCheckBox = QCheckBox()
        self.friCheckBox.setFont(QFont("Ubuntu", 10))
        self.friCheckBox.setText("Fri")
        self.friCheckBox.clicked.connect(self.on_check_fri_clicked)
        self.friCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.satCheckBox = QCheckBox()
        self.satCheckBox.setFont(QFont("Ubuntu", 10))
        self.satCheckBox.setText("Sat")
        self.satCheckBox.clicked.connect(self.on_check_sat_clicked)
        self.satCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Time to run widget
        ################################################################################
        self.timeToRunWidget = QWidget(self)
        self.timeToRunWidget.setGeometry(280, 100, 390, 140)
        self.timeToRunWidget.setStyleSheet("""
            border-top: 1px solid rgb(198, 198, 198);
            border-bottom: 1px solid rgb(198, 198, 198);
        """)

        # Time to run title
        self.timeToRunTitle = QLabel(self.timeToRunWidget)
        self.timeToRunTitle.setFont(QFont("Ubuntu", 11))
        self.timeToRunTitle.setText("Time to run:")
        self.timeToRunTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.timeToRunTitle.setFixedSize(180, 30)
        self.timeToRunTitle.setStyleSheet("""
            border: transparent;
        """)

        # Time to run layout
        self.timeToRunLayout = QGridLayout(self.timeToRunWidget)

        # Time settings
        self.timesGridLayout = QGridLayout()

        # Radio buttons
        self.oneTimePerDayRadio = QRadioButton()
        self.oneTimePerDayRadio.setFont(QFont("Ubuntu", 10))
        self.oneTimePerDayRadio.setText("One time per day")
        self.oneTimePerDayRadio.setToolTip("One single back up will be execute every selected day(s) and time.")
        self.oneTimePerDayRadio.adjustSize()
        self.oneTimePerDayRadio.setStyleSheet(
        "QRadioButton"
           "{"
            "border: 0px solid transparent;"
            "border-radius: 5px;"
           "}")
        self.oneTimePerDayRadio.clicked.connect(self.on_frequency_clicked)

        self.moreTimePerDayRadio = QRadioButton()
        self.moreTimePerDayRadio.setFont(QFont("Ubuntu", 10))
        self.moreTimePerDayRadio.setToolTip(
            "Back up will be execute every x hours.\n"
            "This will produce a time folder inside your backup device.\n"
            "Fx: 12-12-12/10-00\n"
            "10-00, is the time of the back up (10:00).")

        self.moreTimePerDayRadio.setText("Multiple times per day")
        self.moreTimePerDayRadio.adjustSize()
        self.moreTimePerDayRadio.setStyleSheet("""
            border-color: transparent;
        """)
        self.moreTimePerDayRadio.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.hoursSpinBox = QSpinBox()
        self.hoursSpinBox.setFont(QFont("Ubuntu", 14))
        self.hoursSpinBox.setFixedSize(50, 30)
        self.hoursSpinBox.setFrame(False)
        self.hoursSpinBox.setMinimum(0)
        self.hoursSpinBox.setSingleStep(1)
        self.hoursSpinBox.setMaximum(23)
        self.hoursSpinBox.valueChanged.connect(self.label_hours_changed)
        self.hoursSpinBox.setStyleSheet("""
            border-color: transparent;
            """)

        # : between hours and minutes
        self.betweenHoursAndMinutesLabel = QLabel()
        self.betweenHoursAndMinutesLabel.setFont(QFont("Ubuntu", 18))
        self.betweenHoursAndMinutesLabel.setText(":")
        self.betweenHoursAndMinutesLabel.setStyleSheet("""
            border-color: transparent;
        """)

        # Hours title
        self.hoursTitle = QLabel()
        self.hoursTitle.setFont(QFont("Ubuntu", 10))
        self.hoursTitle.setText("Hours")
        self.hoursTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.hoursTitle.setStyleSheet("""
            border-color: transparent;
            border-radius: 5px;
        """)

        # Minutes title
        self.minutesTitle = QLabel()
        self.minutesTitle.setFont(QFont("Ubuntu", 10))
        self.minutesTitle.setText("Minutes")
        self.minutesTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.minutesTitle.setStyleSheet("""
            border-color: transparent;
        """)

        # Spinbox Hours
        self.minutesSpinBox = QSpinBox()
        self.minutesSpinBox.setFont(QFont("Ubuntu", 14))
        self.minutesSpinBox.setFixedSize(50, 30)
        self.minutesSpinBox.setFrame(False)
        self.minutesSpinBox.setStyleSheet(
        "QSpinBox"
            "{"
                "border: 0px solid transparent;"
            "}")

        self.minutesSpinBox.setMinimum(0)
        self.minutesSpinBox.setSingleStep(1)
        self.minutesSpinBox.setMaximum(59)
        self.minutesSpinBox.valueChanged.connect(self.label_minutes_changed)

        # Multiple time per day combobox
        self.multipleTimePerDayComboBox = QComboBox()
        self.multipleTimePerDayComboBox.setFrame(True)
        self.multipleTimePerDayComboBox.setFixedSize(132, 28)
        self.multipleTimePerDayComboBox.setFont(QFont("Ubuntu", 10))
        self.multipleTimePerDayComboBox.setStyleSheet(
        "QComboBox"
            "{"
                "border: 0px solid transparent;"
            "}")

        multipleTimerPerDayComboBoxList = [
            "Every 1 hour",
            "Every 2 hours",
            "Every 4 hours"]
        self.multipleTimePerDayComboBox.addItems(multipleTimerPerDayComboBoxList)
        self.multipleTimePerDayComboBox.currentIndexChanged.connect(self.on_every_combox_changed)

        ################################################################################
        # Flatpak settings
        ################################################################################
        self.flatpakWidget = QWidget(self)
        self.flatpakWidget.setGeometry(280, 240, 390, 80)
        self.flatpakWidget.setStyleSheet(
        "QWidget"
        "{"
        "border-bottom: 1px solid rgb(198, 198, 198);"
        "}")

        # Notification layout
        self.flatpakLayout = QVBoxLayout(self.flatpakWidget)
        self.flatpakLayout.setSpacing(5)

        # Notification title
        self.flatpakTitle = QLabel()
        self.flatpakTitle.setFont(QFont("Ubuntu", 11))
        self.flatpakTitle.setText("Flatpak Settings:")
        self.flatpakTitle.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.flatpakTitle.setFixedSize(200, 30)
        self.flatpakTitle.setStyleSheet("""
            border: transparent;
        """)

        # Flatpak Name checkbox
        self.allowFlatpakNamesCheckBox = QCheckBox()
        self.allowFlatpakNamesCheckBox.setFont(QFont("Ubuntu", 10))
        self.allowFlatpakNamesCheckBox.setText(f"Back up Flatpaks apps names")
        self.allowFlatpakNamesCheckBox.adjustSize()
        self.allowFlatpakNamesCheckBox.setStyleSheet("""
            border: transparent;
        """)
        self.allowFlatpakNamesCheckBox.clicked.connect(self.on_allow__flatpak_names_clicked)
        
        # Flatpak Data checkbox
        self.allowFlatpakDataCheckBox = QCheckBox()
        self.allowFlatpakDataCheckBox.setFont(QFont("Ubuntu", 10))
        self.allowFlatpakDataCheckBox.setText(f"Back up Flatpaks data " 
            "(Flatpak names is necessary)")
        self.allowFlatpakDataCheckBox.adjustSize()
        self.allowFlatpakDataCheckBox.setStyleSheet("""
            border: transparent;
        """)
        self.allowFlatpakDataCheckBox.clicked.connect(self.on_allow__flatpak_data_clicked)

        ################################################################################
        # Reset widget
        ################################################################################
        self.resetWidget = QWidget(self)
        self.resetWidget.setGeometry(280, 320, 390, 90)
 
        # Reset layout
        self.resetLayout = QVBoxLayout(self.resetWidget)
        self.resetLayout.setSpacing(0)

        # Reset title
        self.resetTitle = QLabel()
        self.resetTitle.setFont(QFont("Ubuntu", 11))
        self.resetTitle.setText("Reset:")
        self.resetTitle.adjustSize()
        self.resetTitle.setAlignment(QtCore.Qt.AlignLeft)

        # Reset label text
        self.resetText = QLabel()
        self.resetText.setFont(QFont("Ubuntu", 10))
        self.resetText.setText('If something seems broken, click on "Reset", to reset settings.')
        self.resetText.adjustSize()

        ################################################################################
        # Fix button
        ################################################################################
        self.fixButton = QPushButton()
        self.fixButton.setFont(QFont("Ubuntu", 10))
        self.fixButton.setText("Reset")
        self.fixButton.adjustSize()
        self.fixButton.clicked.connect(self.on_button_fix_clicked)

        ################################################################################
        # Donate, Update and Save buttons
        ################################################################################
        self.donateAndBackWidget = QWidget(self)
        self.donateAndBackWidget.setGeometry(478, 390, 220, 60)

        # Donate and Settings widget
        self.donateAndBackLayout = QHBoxLayout(self.donateAndBackWidget)
        self.donateAndBackLayout.setSpacing(10)

        # Donate buton
        self.donateButton = QPushButton()
        self.donateButton.setText("Donate")
        self.donateButton.setFont(QFont("Ubuntu", 10))
        self.donateButton.adjustSize()
        self.donateButton.clicked.connect(self.donate_clicked)

        ################################################################################
        # Save button
        ################################################################################
        self.saveButton = QPushButton()
        self.saveButton.adjustSize()
        self.saveButton.setFont(QFont("Ubuntu", 10))
        self.saveButton.setText("Back")
        self.saveButton.clicked.connect(self.on_save_button_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left layout
        self.leftLayout.addWidget(self.leftTitle, 0, Qt.AlignLeft | Qt.AlignTop)
        self.leftLayout.addWidget(self.leftFrame, 0, Qt.AlignLeft | Qt.AlignTop)

        # Days to run layout V
        self.daysToRunLayoutV.addWidget(self.daysToRunTitle, 0, Qt.AlignTop | Qt.AlignLeft)
        self.daysToRunLayoutV.addLayout(self.daysToRunLayoutH)

        # Days to run layout H
        self.daysToRunLayoutH.addWidget(self.sunCheckBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.monCheckBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.tueCheckBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.wedCheckBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.thuCheckBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.friCheckBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.satCheckBox, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Time to run layout
        self.timeToRunLayout.addWidget(self.timeToRunTitle, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.oneTimePerDayRadio, 1, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.moreTimePerDayRadio, 2, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.multipleTimePerDayComboBox, 2, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addLayout(self.timesGridLayout, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

        # Time grid layout
        self.timesGridLayout.addWidget(self.hoursSpinBox, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.timesGridLayout.addWidget(self.betweenHoursAndMinutesLabel, 0, 2, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGridLayout.addWidget(self.minutesSpinBox, 0, 3, Qt.AlignTop | Qt.AlignLeft)
        self.timesGridLayout.addWidget(self.hoursTitle, 1, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGridLayout.addWidget(self.minutesTitle, 1, 3, Qt.AlignVCenter | Qt.AlignHCenter)

        # Flaptak settings
        self.flatpakLayout.addWidget(self.flatpakTitle, Qt.AlignTop | Qt.AlignLeft)
        self.flatpakLayout.addWidget(self.allowFlatpakNamesCheckBox)
        self.flatpakLayout.addWidget(self.allowFlatpakDataCheckBox)

        # Reset layout
        self.resetLayout.addWidget(self.resetTitle, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.resetText, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.fixButton, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Donate layout
        self.donateAndBackLayout.addStretch()
        self.donateAndBackLayout.addWidget(self.donateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndBackLayout.addWidget(self.saveButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)

        self.setLayout(self.leftLayout)

        self.get_folders()

    def get_folders(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        getIniFolders = config.options('FOLDER')

        # Get USER home folders
        for folder in getHomeFolders:
            # Hide hidden folder
            if not "." in folder:    
                # Checkboxes
                self.foldersCheckbox = QCheckBox(self.leftFrame)
                self.foldersCheckbox.setText(folder)
                self.foldersCheckbox.adjustSize()
                self.foldersCheckbox.setIcon(QIcon(f"{homeUser}/.local/share/timemachine/src/icons/folder.png"))
                self.foldersCheckbox.setStyleSheet(
                    "QCheckBox"
                    "{"
                    "border-color: transparent;"
                    "}")
                # self.foldersCheckbox.setFixedSize(150, 22)
                self.foldersCheckbox.clicked.connect(lambda *args, folder=folder: self.on_folder_clicked(folder))
                
                # Activate checkboxes in user.ini
                if folder.lower() in getIniFolders:
                    self.foldersCheckbox.setChecked(True)

                # Add to layout self.leftLayout
                self.leftLayout.addWidget(self.foldersCheckbox, 0, QtCore.Qt.AlignTop)

        self.dates()

    def dates(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        ################################################################################
        # Read INI file
        ################################################################################
        sun = config['SCHEDULE']['sun']
        mon = config['SCHEDULE']['mon']
        tue = config['SCHEDULE']['tue']
        wed = config['SCHEDULE']['wed']
        thu = config['SCHEDULE']['thu']
        fri = config['SCHEDULE']['fri']
        sat = config['SCHEDULE']['sat']

        ################################################################################
        # Dates
        # Check each dates
        ################################################################################
        if sun == "true":
            self.sunCheckBox.setChecked(True)

        if mon == "true":
            self.monCheckBox.setChecked(True)

        if tue == "true":
            self.tueCheckBox.setChecked(True)

        if wed == "true":
            self.wedCheckBox.setChecked(True)

        if thu == "true":
            self.thuCheckBox.setChecked(True)

        if fri == "true":
            self.friCheckBox.setChecked(True)

        if sat == "true":
            self.satCheckBox.setChecked(True)

        self.time_to_run()

    def time_to_run(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        # Time
        iniEverytime = config['SCHEDULE']['everytime']
        # Mode
        iniOneTimePerDay = config['MODE']['one_time_mode']
        iniMultipleTimePerDay = config['MODE']['more_time_mode']

        ################################################################################
        # One time per day
        ################################################################################
        # Hours
        hrs = int(config['SCHEDULE']['hours'])
        self.hoursSpinBox.setValue(hrs)

        # Minutes
        min = int(config['SCHEDULE']['minutes'])
        self.minutesSpinBox.setValue(min)

        ################################################################################
        # Get info from INI file
        # One time per day
        ################################################################################
        if iniOneTimePerDay == "true":
            self.multipleTimePerDayComboBox.setEnabled(False)
            self.hoursSpinBox.setEnabled(True)
            self.minutesSpinBox.setEnabled(True)
            self.oneTimePerDayRadio.setChecked(True)
            
            # Enable all days
            self.sunCheckBox.setEnabled(True)
            self.monCheckBox.setEnabled(True)
            self.tueCheckBox.setEnabled(True)
            self.wedCheckBox.setEnabled(True)
            self.thuCheckBox.setEnabled(True)
            self.friCheckBox.setEnabled(True)
            self.satCheckBox.setEnabled(True)
        
        # Multiple time per day
        elif iniMultipleTimePerDay == "true":
            self.hoursSpinBox.setEnabled(False)
            self.minutesSpinBox.setEnabled(False)
            self.multipleTimePerDayComboBox.setEnabled(True)
            self.moreTimePerDayRadio.setChecked(True)
        
            # Disable all days
            self.sunCheckBox.setEnabled(False)
            self.monCheckBox.setEnabled(False)
            self.tueCheckBox.setEnabled(False)
            self.wedCheckBox.setEnabled(False)
            self.thuCheckBox.setEnabled(False)
            self.friCheckBox.setEnabled(False)
            self.satCheckBox.setEnabled(False)

        ################################################################################
        # Multiple time per day
        ################################################################################
        if iniEverytime == "60":
            self.multipleTimePerDayComboBox.setCurrentIndex(0)

        elif iniEverytime == "120":
            self.multipleTimePerDayComboBox.setCurrentIndex(1)

        elif iniEverytime == "240":
            self.multipleTimePerDayComboBox.setCurrentIndex(2)

        self.flatpak_settings()

    def flatpak_settings(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniAllowFlatpakNames = config['BACKUP']['allow_flatpak_names']
        self.iniAllowFlatpakData = config['BACKUP']['allow_flatpak_data']

        ################################################################################
        # Flatpak settings
        ################################################################################
        # Flatpak names
        if self.iniAllowFlatpakNames == "true":
            self.allowFlatpakNamesCheckBox.setChecked(True)

        # Flatpak data
        if self.iniAllowFlatpakData == "true":
            self.allowFlatpakDataCheckBox.setChecked(True)

    def on_folder_clicked(self, output):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if config.has_option('FOLDER', output):
                config.remove_option('FOLDER', output)
            else:
                config.set('FOLDER', output, 'true')

            # Write to INI file
            config.write(configfile)

    def on_every_combox_changed(self):
        chooseMultipleTimePerDayCombox = self.multipleTimePerDayComboBox.currentIndex()
        
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if chooseMultipleTimePerDayCombox == 0:
                config.set('SCHEDULE', 'everytime', '60')

            elif chooseMultipleTimePerDayCombox == 1:
                config.set('SCHEDULE', 'everytime', '120')

            elif chooseMultipleTimePerDayCombox == 2:
                config.set('SCHEDULE', 'everytime', '240')

            # Write to INI file
            config.write(configfile)

    def on_check_sun_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.sunCheckBox.isChecked():
                config.set('SCHEDULE', 'sun', 'true')
                print("Sun")
            else:
                config.set('SCHEDULE', 'sun', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_mon_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.monCheckBox.isChecked():
                config.set('SCHEDULE', 'mon', 'true')
                print("Mon")
            else:
                config.set('SCHEDULE', 'mon', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_tue_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.tueCheckBox.isChecked():
                config.set('SCHEDULE', 'tue', 'true')
                print("Tue")
            else:
                config.set('SCHEDULE', 'tue', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_wed_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.wedCheckBox.isChecked():
                config.set('SCHEDULE', 'wed', 'true')
                print("Wed")
            else:
                config.set('SCHEDULE', 'wed', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_thu_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.thuCheckBox.isChecked():
                config.set('SCHEDULE', 'thu', 'true')
                print("Thu")
            else:
                config.set('SCHEDULE', 'thu', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_fri_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.friCheckBox.isChecked():
                config.set('SCHEDULE', 'fri', 'true')
                print("Fri")
            else:
                config.set('SCHEDULE', 'fri', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_sat_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.satCheckBox.isChecked():
                config.set('SCHEDULE', 'sat', 'true')
                print("Sat")
            else:
                config.set('SCHEDULE', 'sat', 'false')

            # Write to INI file
            config.write(configfile)

    def label_hours_changed(self):
        hours = str(self.hoursSpinBox.value())

        # Save hours
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w+') as configfile:
            config.set('SCHEDULE', 'hours', hours)
            if hours in fixMinutes:
                config.set('SCHEDULE', 'hours', '0' + hours)

            # Write to INI file
            config.write(configfile)

    def label_minutes_changed(self):
        minutes = str(self.minutesSpinBox.value())

        # Save minutes
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w+') as configfile:
            config.set('SCHEDULE', 'minutes', minutes)
            if minutes in fixMinutes:
                config.set('SCHEDULE', 'minutes', '0' + minutes)

            # Write to INI file
            config.write(configfile)

    def on_frequency_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w+') as configfile:
            if self.oneTimePerDayRadio.isChecked():
                config.set('MODE', 'one_time_mode', 'true')
                print("One time per day selected")
                # DISABLE MORE TIME MODE
                config.set('MODE', 'more_time_mode', 'false')

                self.multipleTimePerDayComboBox.setEnabled(False)
                self.hoursSpinBox.setEnabled(True)
                self.minutesSpinBox.setEnabled(True)
                self.oneTimePerDayRadio.setChecked(True)
                
                # Enable all days
                self.sunCheckBox.setEnabled(True)
                self.monCheckBox.setEnabled(True)
                self.tueCheckBox.setEnabled(True)
                self.wedCheckBox.setEnabled(True)
                self.thuCheckBox.setEnabled(True)
                self.friCheckBox.setEnabled(True)
                self.satCheckBox.setEnabled(True)

            elif self.moreTimePerDayRadio.isChecked():
                config.set('MODE', 'more_time_mode', 'true')
                print("Multiple time per day selected")
                # DISABLE ONE TIME MODE
                config.set('MODE', 'one_time_mode', 'false')

                self.hoursSpinBox.setEnabled(False)
                self.minutesSpinBox.setEnabled(False)
                self.multipleTimePerDayComboBox.setEnabled(True)
                self.moreTimePerDayRadio.setChecked(True)
        
                # Disable all days
                self.sunCheckBox.setEnabled(False)
                self.monCheckBox.setEnabled(False)
                self.tueCheckBox.setEnabled(False)
                self.wedCheckBox.setEnabled(False)
                self.thuCheckBox.setEnabled(False)
                self.friCheckBox.setEnabled(False)
                self.satCheckBox.setEnabled(False)

            # Write to INI file
            config.write(configfile)

    def on_allow__flatpak_names_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.allowFlatpakNamesCheckBox.isChecked():
                config.set('BACKUP', 'allow_flatpak_names', 'true')
                print("Allow flatpaks installed names")
            else:
                config.set('BACKUP', 'allow_flatpak_names', 'false')
                config.set('BACKUP', 'allow_flatpak_data', 'false')
                self.allowFlatpakDataCheckBox.setChecked(False)

            # Write to INI file
            config.write(configfile)

    def on_allow__flatpak_data_clicked(self):
        # If user allow app to back up data, auto activate
        # backup flatpaks name too.
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.allowFlatpakDataCheckBox.isChecked():
                config.set('BACKUP', 'allow_flatpak_names', 'true')
                config.set('BACKUP', 'allow_flatpak_data', 'true')
                print("Allow flatpaks installed names + data")

                # Activate names checkbox
                self.allowFlatpakNamesCheckBox.setChecked(True)

            else:
                config.set('BACKUP', 'allow_flatpak_data', 'false')

            # Write to INI file
            config.write(configfile)

    def on_button_fix_clicked(self):
        resetConfirmation = QMessageBox.question(self, 'Reset', 
            'Are you sure you want to reset settings?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resetConfirmation == QMessageBox.Yes:
            # Reset settings
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                # Backup section
                config.set('BACKUP', 'first_startup', 'false')
                config.set('BACKUP', 'auto_backup', 'false')
                config.set('BACKUP', 'backup_now', 'false')
                config.set('BACKUP', 'checker_running', 'false')
                config.set('BACKUP', 'allow_flatpak_names', 'true')
                config.set('BACKUP', 'allow_flatpak_data', 'false')

                # External section
                config.set('EXTERNAL', 'hd', 'None')
                config.set('EXTERNAL', 'name', 'None')

                # Mode section
                config.set('MODE', 'one_time_mode', 'false')
                config.set('MODE', 'more_time_mode', 'true')

                # System tray  section
                config.set('SYSTEMTRAY', 'system_tray', 'false')

                # Schedule section
                config.set('SCHEDULE', 'sun', 'false')
                config.set('SCHEDULE', 'mon', 'true')
                config.set('SCHEDULE', 'tue', 'true')
                config.set('SCHEDULE', 'wed', 'true')
                config.set('SCHEDULE', 'thu', 'true')
                config.set('SCHEDULE', 'fri', 'true')
                config.set('SCHEDULE', 'sat', 'false')
                config.set('SCHEDULE', 'hours', '10')
                config.set('SCHEDULE', 'minutes', '00')
                config.set('SCHEDULE', 'everytime', '60')

                # Info section
                config.set('INFO', 'latest', 'None')
                config.set('INFO', 'next', 'None')
                config.set('INFO', 'notification_id', '0')
                config.set('INFO', 'feedback_status', ' ')

                # Folders section
                config.set('FOLDER', 'pictures', 'true')
                config.set('FOLDER', 'documents', 'true')
                config.set('FOLDER', 'music', 'true')
                config.set('FOLDER', 'videos', 'true')
                config.set('FOLDER', 'desktop', 'true')

                # Restore section
                config.set('RESTORE', 'is_restore_running', 'false')
                config.set('RESTORE', 'applications_packages', 'true')
                config.set('RESTORE', 'applications_flatpak_names', 'true')
                config.set('RESTORE', 'applications_data', 'false')
                config.set('RESTORE', 'files_and_folders', 'false')

                # Write to INI file
                config.write(configfile)

            print("All settings was reset!")

        else:
            QMessageBox.Close

    def donate_clicked(self):
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)

    def on_save_button_clicked(self):
        widget.setCurrentWidget(main)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    #app.setStyle("Fusion")
    #dark_palette = QPalette()
    #dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    #dark_palette.setColor(QPalette.WindowText, Qt.white)
    #dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    #dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    #dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    #dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    #dark_palette.setColor(QPalette.Text, Qt.white)
    #dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    #dark_palette.setColor(QPalette.ButtonText, Qt.white)
    #dark_palette.setColor(QPalette.BrightText, Qt.red)
    #dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    #dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    #dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    #app.setPalette(dark_palette)
    #app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    ####################
    main = MAIN()
    mainDevices = EXTERNAL()
    mainOpitions = OPTION()
    ####################
    widget = QStackedWidget()
    widget.addWidget(main)   
    widget.addWidget(mainOpitions) 
    widget.setCurrentWidget(main)   
    widget.show()
    # Window title name
    widget.setWindowTitle(appName)

    app.exit(app.exec())
        
        
