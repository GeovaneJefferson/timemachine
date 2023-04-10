#! /usr/bin/python3
from setup import *
from stylesheet import *
from check_connection import *
from device_location import *
from package_manager import *
from get_user_de import get_user_de
from get_home_folders import *
from get_system_language import system_language
# from languages import determine_days_language
from get_size import *
from read_ini_file import UPDATEINIFILE
from get_oldest_backup_date import oldest_backup_date
from get_latest_backup_date import latest_backup_date_label
from update import backup_ini_file
from calculate_time_left_to_backup import calculate_time_left_to_backup
from determine_next_backup import get_next_backup


class MAIN(QMainWindow):
    def __init__(self):
        super(MAIN, self).__init__()
        self.timeOut = 0

        self.chooseDevice = ()
        self.captureDevices = []

        self.oldestList = []
        self.lastList = []
        
        self.iniUI()

    def iniUI(self):
        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if app.palette().window().color().getRgb()[0] < 55:
            # Left background
            self.leftBackgroundColorDetector = leftBackgroundColorStylesheetDark
            # Button
            self.buttonStylesheetDetector = buttonStylesheetDark
            # External window
            self.externalWindowbackgroundDetector = externalWindowbackgroundStylesheetDark
            # Available devices
            self.availableDeviceButtonDetector = availableDeviceButtonStylesheetDark
        else:
            # Left background
            self.leftBackgroundColorDetector = leftBackgroundColorStylesheet
            # Button
            self.buttonStylesheetDetector = buttonStylesheet
            # External window
            self.externalWindowbackgroundDetector = externalWindowbackgroundStylesheet
            # Available devices
            self.availableDeviceButtonDetector = availableDeviceButtonStylesheet

        leftBackgroundColor = QWidget(self)
        leftBackgroundColor.setGeometry(0,0,220,self.height()) 
        leftBackgroundColor.setStyleSheet(self.leftBackgroundColorDetector)

        self.widgets()

    def widgets(self):
        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 200, 410) 

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

        # App name
        self.appName = QLabel()
        self.appName.setFont(QFont(mainFont,smallFontSize))
        self.appName.setText(f"<h1>{appName}</h1>")
        self.appName.adjustSize()

        # Automatically checkbox
        self.automaticallyCheckBox = QCheckBox()
        self.automaticallyCheckBox.setFont(QFont(mainFont,normalFontSize))
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
        self.rightWidget.setGeometry(240, 40, 120, 154)

        # Right layout
        self.rightLayout = QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(20)

        # Restore images
        self.restoreImageLabel = QLabel()
        self.restoreImageLabel.setFixedSize(74, 74)
        self.restoreImageLabel.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_restore_icon});"
            "background-repeat: no-repeat;"
            "background-position: top;"
            "}")

        # Select disk button
        self.selectDiskButton = QPushButton(self)
        self.selectDiskButton.setFont(QFont(mainFont,normalFontSize))
        self.selectDiskButton.setText("   Select Disk...   ")
        self.selectDiskButton.adjustSize()
        self.selectDiskButton.setFixedHeight(buttonHeightSize)
        self.selectDiskButton.setStyleSheet(self.buttonStylesheetDetector)
        self.selectDiskButton.clicked.connect(self.external_open_animation)
       
        ################################################################################
        # Far right Widget
        ################################################################################
        self.farRightWidget = QWidget(self)
        self.farRightWidget.setContentsMargins(0, 0, 0, 0)
        self.farRightWidget.setGeometry(360, 40, 280, 154)
        
        # Right widget
        self.farRightLayout = QVBoxLayout(self.farRightWidget)
        self.farRightLayout.setSpacing(0)
        # self.farRightWidget.setStyleSheet("""
        #     border: 1px solid red;
        #     """)

        ################################################################################
        # Set external name
        ################################################################################
        self.externalNameLabel = QLabel()
        self.externalNameLabel.setFont(QFont(mainFont, 6))
        # self.externalNameLabel.setFixedSize(350, 80)
        self.externalNameLabel.setAlignment(QtCore.Qt.AlignLeft)

        ################################################################################
        # Get external size
        ################################################################################
        self.externalSizeLabel = QLabel()
        self.externalSizeLabel.setFont(item)
        self.externalSizeLabel.setFixedSize(200, 18)
        self.externalSizeLabel.setStyleSheet("""
            color: gray;
            """)

        ################################################################################
        # Label UI backup
        ################################################################################
        self.oldestBackupLabel = QLabel()
        self.oldestBackupLabel.setFont(item)
        self.oldestBackupLabel.setText("Oldest Backup: None")
        self.oldestBackupLabel.setFixedSize(200, 18)
        self.oldestBackupLabel.setStyleSheet("""
            color: gray;
            """)
            
        self.lastestBackupLabel = QLabel()
        self.lastestBackupLabel.setFont(item)
        self.lastestBackupLabel.setText("Lastest Backup: None")
        self.lastestBackupLabel.setFixedSize(200, 18)
        self.lastestBackupLabel.setStyleSheet("""
            color: gray;
            """)

        # Label last backup
        self.nextBackupLabel = QLabel()
        self.nextBackupLabel.setFont(item)
        self.nextBackupLabel.setText("Next Backup: None")
        self.nextBackupLabel.setFixedSize(250, 18)
        self.nextBackupLabel.setStyleSheet("""
            color: gray;
            """)

        # Status Status
        self.externalStatusLabel = QLabel()
        self.externalStatusLabel.setFont(item)
        self.externalStatusLabel.setText("Status: None")
        self.externalStatusLabel.setFixedSize(200, 18)
        self.externalStatusLabel.setStyleSheet("""
            color: gray;
            """)

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
        self.backupNowButton.setText("   Back Up Now   ")
        self.backupNowButton.setFont(QFont(mainFont,normalFontSize))
        self.backupNowButton.adjustSize()
        self.backupNowButton.setFixedHeight(buttonHeightSize)
        self.backupNowButton.setStyleSheet(self.buttonStylesheetDetector)
        self.backupNowButton.clicked.connect(self.backup_now_clicked)
        self.backupNowButton.setEnabled(False)        

        ################################################################################
        # Top line widget
        ################################################################################
        topLineWidget = QWidget(self)
        topLineWidget.setGeometry(240,30,440,1)
        topLineWidget.setStyleSheet("""
            border-top:1px solid rgba(14,14,14,0.1);
        """)
        ################################################################################
        # Description
        ################################################################################
        self.descriptionWidget = QWidget(self)
        self.descriptionWidget.setGeometry(240, 200, 440, 160)
        self.descriptionWidget.setStyleSheet("""
            border-top:1px solid rgba(14,14,14,0.1);
        """)


        # Description Layout
        self.descriptionLayout = QVBoxLayout(self.descriptionWidget)

        # Description Title
        self.descriptionTitle = QLabel()
        self.descriptionTitle.setFont(topicTitle)
        self.descriptionTitle.setText(f"{appName} keeps:")
        self.descriptionTitle.adjustSize()
        self.descriptionTitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        # self.descriptionTitle.setFixedSize(420, 24)
        self.descriptionTitle.setStyleSheet("""
            border-color: transparent;
            color: gray;
        """)

        # Description Text
        self.descriptionText = QLabel()
        self.descriptionText.setFont(item)
        self.descriptionText.setText(
            "• Local snapshots as space permits\n"
            "• Hourly backups for the past 24 hours\n"
            "• Daily backups for the past mounths\n"
            "• Applications '.deb and .rpm' + Flatpaks\n"
            "• Wallpaper, Theme, Icon and Cursor theme\n\n"
            "The oldest backups are deleted when your disk becomes full.\n\n")
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
        self.optionsButton.setText("   Options...   ")
        self.optionsButton.setFont(QFont(mainFont,normalFontSize))
        self.optionsButton.setFixedHeight(buttonHeightSize)
        self.optionsButton.adjustSize()
        self.optionsButton.setStyleSheet(self.buttonStylesheetDetector)
        self.optionsButton.clicked.connect(self.on_options_clicked)

        # Help button
        self.helpButton = QPushButton()
        self.helpButton.setText("?")
        self.helpButton.setFont(QFont(mainFont,normalFontSize))
        self.helpButton.setFixedSize(24,24)
        self.helpButton.setToolTip("Help")
        self.helpButton.setStyleSheet(self.buttonStylesheetDetector)
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
        # External Window
        ################################################################################
        self.externalBackgroundShadow = QWidget(self)
        self.externalBackgroundShadow.setFixedSize(700,self.height())
        self.externalBackgroundShadow.move(0,0)
        self.externalBackgroundShadow.setVisible(False)
        self.externalBackgroundShadow.setStyleSheet(
        "QWidget"
            "{"
                "background-color:rgba(14,14,14,0.6);"
            "}")
        
        self.externalWindow = QWidget(self)
        self.externalWindow.setFixedSize(400,280)
        self.externalWindow.move(self.width()/4,-300)
        self.externalWindow.show()
        self.externalWindow.setStyleSheet(self.externalWindowbackgroundDetector)

        # Frame
        self.whereFrame = QFrame(self.externalWindow)
        self.whereFrame.setFixedSize(self.externalWindow.width()-60,self.externalWindow.height())
        self.whereFrame.move(20,40)
        self.whereFrame.setStyleSheet(self.externalWindowbackgroundDetector)

        # Scroll
        self.scroll = QScrollArea(self.externalWindow)
        self.scroll.resize(360,180)
        self.scroll.move(20,40)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.whereFrame)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setStyleSheet(self.externalWindowbackgroundDetector)

        # Vertical layout V
        self.verticalLayout = QVBoxLayout(self.whereFrame)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        
        # Info 
        self.notAllowed = QLabel(self.externalWindow)
        self.notAllowed.setText("Devices with space(s) and/or special characters will be hidden.")
        self.notAllowed.setFont(item)
        self.notAllowed.move(20,20)
        self.notAllowed.setStyleSheet(transparentBackground)
        
        ################################################################################
        # Buttons
        ################################################################################
        widgetButton = QWidget(self.externalWindow)
        widgetButton.setFixedSize(self.externalWindow.width()-10,58)
        widgetButton.move(5,220)
        widgetButton.setStyleSheet("""border:0px;""")

        widgetButtonLayout = QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)
        
        # Cancel button
        self.cancelButton = QPushButton()
        self.cancelButton.setFont(item)
        self.cancelButton.setText("   Cancel   ")
        self.cancelButton.adjustSize()
        self.cancelButton.setFixedHeight(buttonHeightSize)
        self.cancelButton.setStyleSheet(self.buttonStylesheetDetector)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        # Use this device
        self.useDiskButton = QPushButton()
        self.useDiskButton.setFont(item)
        self.useDiskButton.setText("   Use Disk   ")
        self.useDiskButton.setFixedHeight(buttonHeightSize)
        self.useDiskButton.adjustSize()
        self.useDiskButton.setEnabled(False)
        self.useDiskButton.setStyleSheet(useDiskButtonStylesheet)
        self.useDiskButton.clicked.connect(self.on_use_disk_clicked)
        
        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left Layout
        self.leftLayout.addWidget(self.backupImageLabel, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.leftLayout.addWidget(self.appName, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.leftLayout.addWidget(self.automaticallyCheckBox, 1, Qt.AlignHCenter | Qt.AlignTop)

        #  Right Layout
        self.rightLayout.addStretch(10)
        self.rightLayout.addWidget(self.restoreImageLabel, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.rightLayout.addWidget(self.selectDiskButton, 1, Qt.AlignVCenter | Qt.AlignHCenter)
        
        #  Far Right Layout
        self.farRightLayout.addWidget(self.externalNameLabel, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.externalSizeLabel, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.oldestBackupLabel, 1, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.lastestBackupLabel, 1, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.nextBackupLabel, 2, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.externalStatusLabel, 3, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addStretch(10)
        self.farRightLayout.addWidget(self.backupNowButton, 4, Qt.AlignLeft | Qt.AlignTop)

        # Description Layout
        self.descriptionLayout.addWidget(self.descriptionTitle, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.descriptionLayout.addWidget(self.descriptionText, 0, Qt.AlignVCenter | Qt.AlignLeft)

        #  Options layout
        self.optionsLayout.addStretch()
        self.optionsLayout.addWidget(self.optionsButton, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.optionsLayout.addWidget(self.helpButton, 0, Qt.AlignRight | Qt.AlignVCenter)
        
        widgetButtonLayout.addStretch()
        widgetButtonLayout.addWidget(self.cancelButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        widgetButtonLayout.addWidget(self.useDiskButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.setLayout(self.leftLayout)

        self.check_for_updates()

        timer.timeout.connect(self.connection)
        timer.start(2000) 
        self.connection()
        
    def connection(self):
        print("Updating...")
        # Reset timeOut
        self.timeOut = 0

        if str(mainIniFile.ini_hd_name()) != "None":
            self.externalNameLabel.setText(f"<h1>{str(mainIniFile.ini_hd_name())}</h1>")
            
            if is_connected(str(mainIniFile.ini_hd_name())):
                ################################################################################
                # External status
                ################################################################################
                self.externalStatusLabel.setText("Status: Connected")
                self.externalStatusLabel.setStyleSheet('color: green')

                try:
                    # Clean notification info
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w', encoding='utf8') as configfile:
                        config.set('INFO', 'notification_add_info', ' ')
                        config.write(configfile)

                except Exception as error:
                    print(Exception)
                    print("Main Window error!")
                    exit()

                self.get_size_informations()

            else:
                self.backupNowButton.setEnabled(False)       
                self.externalStatusLabel.setText("Status: Disconnected")
                self.externalStatusLabel.setStyleSheet('color: red')
                self.externalSizeLabel.setText("No information available")
        
        # No device registered
        else:
            self.externalSizeLabel.setText("No information available")
            
            self.externalNameLabel.setText("<h1>None</h1>")
            
            self.externalStatusLabel.setText("Status: None")
            self.externalStatusLabel.setStyleSheet('color:gray')
            
            self.backupNowButton.setEnabled(False)

    def get_size_informations(self):
        ################################################################################
        # Get external size values
        ################################################################################
        try:
            self.externalSizeLabel.setText(f"{get_disk_used_size()} of {get_disk_max_size()} available")

        except:
            self.externalSizeLabel.setText("No information available")

        self.condition()

    def condition(self):
        if str(mainIniFile.ini_hd_name()) != "None" and is_connected(str(mainIniFile.ini_hd_name())):  
            # Show backup button if no back up is been made
            if str(mainIniFile.ini_backup_now()) == "false":
                self.selectDiskButton.setEnabled(True)
                self.backupNowButton.setEnabled(True)
                self.automaticallyCheckBox.setEnabled(True)                
                self.showInSystemTrayCheckBox.setEnabled(True)
            else:
                self.selectDiskButton.setEnabled(False)
                self.backupNowButton.setEnabled(False)
                self.automaticallyCheckBox.setEnabled(False)
                self.showInSystemTrayCheckBox.setEnabled(False)
        else:
            self.externalNameLabel.setText("<h1>None</h1>")
            self.backupNowButton.setEnabled(False)
      
        self.set_external_oldest_backup()

    def set_external_oldest_backup(self):
        self.oldestBackupLabel.setText(f"Oldest Backup: {oldest_backup_date()}")
      
        self.set_external_last_backup()

    def set_external_last_backup(self):
        self.lastestBackupLabel.setText(f"Lastest Backup: {latest_backup_date_label()}")

        self.automatically_backup_checkbox()

    def automatically_backup_checkbox(self):
        if mainIniFile.ini_automatically_backup() == 'true':
            if str(mainIniFile.ini_one_time_mode()) == "true":
                if str(calculate_time_left_to_backup()) != "None":
                    self.nextBackupLabel.setText(f"Next Backup: {calculate_time_left_to_backup()}")
                else:
                    self.nextBackupLabel.setText(f"Next Backup: {get_next_backup().capitalize()}, {mainIniFile.ini_next_hour()}:{mainIniFile.ini_next_minute()}")
            else:
                if str(mainIniFile.ini_everytime()) == "60":
                    self.nextBackupLabel.setText("Next Backup: Every 1 hour")
                    self.nextBackupLabel.setFont(buttonFontSize)

                elif str(mainIniFile.ini_everytime()) == "120":
                    self.nextBackupLabel.setText("Next Backup: Every 2 hours")
                    self.nextBackupLabel.setFont(buttonFontSize)

                elif str(mainIniFile.ini_everytime()) == "240":
                    self.nextBackupLabel.setText("Next Backup: Every 4 hours")
                    self.nextBackupLabel.setFont(buttonFontSize)
        else:
            self.nextBackupLabel.setText("Next Backup: Automatic backups off")

        self.load_dates()
    
    def load_dates(self):
        try:
            info = str(get_next_backup().capitalize()) + ", " + str(mainIniFile.ini_next_hour()) + ":" + str(mainIniFile.ini_next_minute())
            # Save next backup to user.ini
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                config.set('INFO', 'next', f'{info}')
                config.write(configfile)
        except:
            pass

        self.load_current_backup_folder()

    def load_current_backup_folder(self):
        # Current backup folder been backup
        self.currentBackUpLabel.setText(str(mainIniFile.ini_current_backup_information()))
        # Auto adjustSize for current backup folder
        self.currentBackUpLabel.adjustSize()

        self.load_extra_information()

    def load_extra_information(self):
        if str(mainIniFile.ini_extra_information()) != "":
            # Information about an error message
            self.extraInformationLabel.setText(str(mainIniFile.ini_extra_information()))
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
        # if str(mainIniFile.ini_hd_name()) == "None":
        #     # Disable automatically backup checkbox
        #     self.automaticallyCheckBox.setEnabled(False)
        # else:
        #     # Enable automatically backup checkbox
        #     self.automaticallyCheckBox.setEnabled(True)

        if str(mainIniFile.ini_automatically_backup()) == "true":
            self.automaticallyCheckBox.setChecked(True)
        else:
            self.automaticallyCheckBox.setChecked(False)
        
        self.load_system_tray()

    def load_system_tray(self):
        ################################################################################
        # System tray
        ################################################################################
        if str(mainIniFile.ini_system_tray()) == "true":
            self.showInSystemTrayCheckBox.setChecked(True)

        else:
            self.showInSystemTrayCheckBox.setChecked(False)

    def automatically_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:  
                if self.automaticallyCheckBox.isChecked():
                    if not os.path.exists(src_backup_check_desktop):
                        # Copy .desktop to user folder (Autostart .desktop)
                        shutil.copy(src_backup_check_desktop, src_backup_check_desktop)  

                    config.set('BACKUP', 'auto_backup', 'true')
                    config.write(configfile)

                    # Backup checker
                    sub.Popen(f"python3 {src_backup_check_py}", shell=True)
                    # Set checker running to true
                    with open(src_user_config, 'w', encoding='utf8') as configfile:
                        config.set('BACKUP', 'checker_running', "true")
                        config.write(configfile)

                    print("Auto backup was successfully activated!")
         
                else:
                    config.set('BACKUP', 'auto_backup', 'false')
                    config.write(configfile)    
                    
                    # Set checker running to false
                    with open(src_user_config, 'w', encoding='utf8') as configfile:
                        config.set('BACKUP', 'checker_running', "false")
                        config.write(configfile)

                    print("Auto backup was successfully deactivated!")
        except:
            pass

    def system_tray_clicked(self):
        try:
            ################################################################################
            # Call system tray
            # System tray can check if is not already runnnig
            ################################################################################
            if str(mainIniFile.ini_system_tray()) == "false":
                print("Starting system tray...")
                sub.Popen(f"python3 {src_system_tray_py}", shell=True)
           
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.showInSystemTrayCheckBox.isChecked():
                    config.set('SYSTEMTRAY', 'system_tray', 'true')
                    config.write(configfile)
                    print("System tray was successfully enabled!")

                else:
                    config.set('SYSTEMTRAY', 'system_tray', 'false')
                    config.write(configfile)
                    print("System tray was successfully disabled!")

        except:
            pass

    def backup_now_clicked(self):
        sub.Popen(f"python3 {src_prepare_backup_py}",shell=True)

    def on_options_clicked(self):
        widget.setCurrentWidget(mainOpitions)

    def check_for_updates(self):
        print("Checking updates...")
        # Check for git updates
        gitUpdateCommand = os.popen("git remote update && git status -uno").read()

        # Updates found
        if "Your branch is behind" in str(gitUpdateCommand):
            updateAvailable = QPushButton()
            updateAvailable.setText("   Update Available   ")
            updateAvailable.adjustSize()
            updateAvailable.setStyleSheet(buttonStylesheet)
            updateAvailable.clicked.connect(self.on_update_button_clicked)
            
            # Show button on screen      
            self.leftLayout.addWidget(updateAvailable, 0, Qt.AlignHCenter | Qt.AlignBottom)

    def on_update_button_clicked(self):
        ################################################################################
        # Call update and Exit
        ################################################################################
        # Set to True, so it will call others function to update propely
        backup_ini_file(True)
        # exit()

    ################################################################################
    # EXTERNAL
    ################################################################################
    def external_open_animation(self):
        self.anim = QPropertyAnimation(self.externalWindow, b"pos")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setEndValue(QPoint(160,0))
        self.anim.setDuration(500)
        self.anim.start()
    
        self.externalBackgroundShadow.setVisible(True)

        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside media
        ################################################################################
        if device_location():
            try:
                # Add buttons and images for each external
                for output in os.listdir(f'{media}/{userName}'):
                    # No spaces and special characters allowed
                    if output not in self.captureDevices and "'" not in output and " " not in output:
                        self.captureDevices.append(output)

                        # Avaliables external  devices
                        self.availableDevices = QPushButton(self.whereFrame)
                        self.availableDevices.setFont(QFont(mainFont,fontSize11px))
                        self.availableDevices.setText(f"{output}")
                        self.availableDevices.setFixedSize(self.whereFrame.width()-20,50)
                        self.availableDevices.setCheckable(True)

                        if str(mainIniFile.ini_hd_name()) != "None":
                            self.availableDevices.setAutoExclusive(True)
    
                        self.availableDevices.setStyleSheet(self.availableDeviceButtonDetector)
                        text = self.availableDevices.text()
                        self.availableDevices.clicked.connect(lambda *args, text=text: self.on_device_clicked(text))
                        
                        # Image
                        icon = QLabel(self.availableDevices)
                        image = QPixmap(f"{src_restore_icon}")
                        image = image.scaled(36,36,QtCore.Qt.KeepAspectRatio)
                        icon.move(7,7)
                        icon.setStyleSheet(transparentBackground)
                        icon.setPixmap(image)
      
                        ################################################################################
                        # Auto checked this choosed external device
                        ################################################################################
                        
                        if text == str(mainIniFile.ini_hd_name()):
                            self.availableDevices.setChecked(True)

                        ################################################################################
                        # Add widgets and Layouts
                        ################################################################################
                        # Vertical layout
                        self.verticalLayout.addWidget(self.availableDevices, 0, QtCore.Qt.AlignHCenter)
           
            except FileNotFoundError:
                pass

        elif not device_location():
            try:
                # If x device is removed or unmounted, remove from screen
                for output in os.listdir(f'{run}/{userName}'):
                    # No spaces and special characters allowed
                    if "'" not in output and " " not in output:
                        self.captureDevices.append(output)

                        # Avaliables external  devices
                        self.availableDevices = QPushButton(self.whereFrame)
                        self.availableDevices.setFont(QFont(mainFont,fontSize11px))
                        self.availableDevices.setText(f"{output}")
                        self.availableDevices.setFixedSize(self.whereFrame.width()-20,60)
                        self.availableDevices.setCheckable(True)
                        self.availableDevices.setAutoExclusive(True)
                        self.availableDevices.setStyleSheet(availableDeviceButtonStylesheet)
                        text = self.availableDevices.text()
                        self.availableDevices.clicked.connect(lambda *args, text=text: self.on_device_clicked(text))
                        
                        # Image
                        icon = QLabel(self.availableDevices)
                        image = QPixmap(f"{src_restore_icon}")
                        image = image.scaled(46, 46, QtCore.Qt.KeepAspectRatio)
                        icon.move(7, 7)
                        icon.setPixmap(image)
                        
                        # Free Space Label
                        freeSpaceLabel = QLabel(self.availableDevices)
                        freeSpaceLabel.setFont(QFont(mainFont, 8))
                        freeSpaceLabel.setAlignment(QtCore.Qt.AlignRight)
                        freeSpaceLabel.move(self.availableDevices.width()-80, 40)
                        
                        if str(mainIniFile.ini_external_location()) == self.availableDevices.text():
                            freeSpaceLabel.setText(f"{get_disk_used_size()}/{get_disk_max_size()}")
                            freeSpaceLabel.adjustSize()

                        # For other devices
                        else:
                            freeSpaceLabel.setText(f"{get_available_devices_size(f'{run}/{userName}/{output}')}")
                            freeSpaceLabel.adjustSize()
                            
                        ################################################################################
                        # Auto checked this choosed external device
                        ################################################################################
                        if text == str(mainIniFile.ini_hd_name()):
                            self.availableDevices.setChecked(True)

                        ################################################################################
                        # Add widgets and Layouts
                        ################################################################################
                        # Vertical layout
                        self.verticalLayout.addWidget(self.availableDevices, 0, QtCore.Qt.AlignHCenter)
            except FileNotFoundError:
                pass

    def on_use_disk_clicked(self):
        ################################################################################
        # Update INI file
        ################################################################################
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if mainFont in package_manager():
                    config.set('INFO', 'packageManager', f'{debFolderName}')
                
                elif "fedora" in package_manager():
                    config.set('INFO', 'packageManager', f'{rpmFolderName}')

                config.set('INFO', 'os',  f'{get_user_de()}')
                config.set('INFO', 'language',  f'{str(system_language())}')
                config.write(configfile)

            ################################################################################
            # Update INI file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                # If inside media
                if device_location():
                    config.set(f'EXTERNAL', 'hd', f'{media}/{userName}/{self.chooseDevice}')
                # If inside run/media
                elif not device_location():
                    config.set(f'EXTERNAL', 'hd', f'{run}/{userName}/{self.chooseDevice}')
                
                config.set('EXTERNAL', 'name', f'{self.chooseDevice}')
                config.write(configfile)
            
            ################################################################################
            # Backup Ini File
            ################################################################################
            print("Backup user.ini file")
            backup_ini_file(False)
            # sub.run(f"{copyCPCMD} {src_user_config} {homeUser}/.local/share/{appNameClose}/src",shell=True)
            
            # Close Window
            self.external_close_animation()
            # main.setEnabled(True)
            # self.close()
        
            self.get_size_informations()


        except:
            pass

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
        self.external_close_animation()
    
    def external_close_animation(self):
        self.anim = QPropertyAnimation(self.externalWindow, b"pos")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setEndValue(QPoint(160,-300))
        self.anim.setDuration(500)
        self.anim.start()
        
        self.externalBackgroundShadow.setVisible(False)
    
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

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if app.palette().window().color().getRgb()[0] < 55:
            self.buttonStylesheetDetector = buttonStylesheetDark
        else:
            self.buttonStylesheetDetector = buttonStylesheet
        
        self.widgets()

    def widgets(self):
        # Apps version
        version = QLabel(self)
        version.setFont(QFont(mainFont, 4))
        version.setText(f"<h1>{appVersion}</h1>")
        version.adjustSize()
        # version.setFixedSize(80, 20)
        version.move(290, 410)

        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget = QWidget()
        self.leftWidget.setGeometry(20, 20, 240, 405)
   
        # Scroll
        self.scroll = QScrollArea(self)
        self.scroll.setFixedSize(240, 405)
        self.scroll.move(20, 20)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.leftWidget)

        # Left layout
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setContentsMargins(10, 10, 10, 10)
        
        ################################################################################
        # Left title
        self.leftTitle = QLabel()
        self.leftTitle.setFont(QFont(mainFont,smallFontSize))
        self.leftTitle.setText("<h1>Folders to be back up:</h1>")
        self.leftTitle.adjustSize()

        # Frame
        self.leftFrame = QFrame()
        self.leftFrame.setGeometry(20, 20, 240, 405)
   
        ################################################################################
        # Days to run widget
        ################################################################################
        self.daysToRunWidget = QWidget(self)
        self.daysToRunWidget.setGeometry(285, 20, 390, 80)
        self.daysToRunWidget.setStyleSheet("""
            border-top: 0px;
            border-left: 0px;
            border-right: 0px;
        """)

        # Days to run layout V
        self.daysToRunLayoutV = QVBoxLayout(self.daysToRunWidget)
        self.daysToRunLayoutV.setSpacing(10)

        # Days to run layout H
        self.daysToRunLayoutH = QHBoxLayout()
        self.daysToRunLayoutH.setSpacing(10)

        # Days to run title
        self.daysToRunTitle = QLabel()
        self.daysToRunTitle.setFont(QFont(mainFont,smallFontSize))
        self.daysToRunTitle.setText("<h1>Days to run:</h1>")
        self.daysToRunTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.daysToRunTitle.adjustSize()
        self.daysToRunTitle.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Checkboxes
        ################################################################################
        self.sunCheckBox = QCheckBox()
        self.sunCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.sunCheckBox.setText("Sun")
        self.sunCheckBox.clicked.connect(self.on_check_sun_clicked)
        self.sunCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.monCheckBox = QCheckBox()
        self.monCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.monCheckBox.setText("Mon")
        self.monCheckBox.clicked.connect(self.on_check_mon_clicked)
        self.monCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.tueCheckBox = QCheckBox()
        self.tueCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.tueCheckBox.setText("Tue")
        self.tueCheckBox.clicked.connect(self.on_check_tue_clicked)
        self.tueCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.wedCheckBox = QCheckBox()
        self.wedCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.wedCheckBox.setText("Wed")
        self.wedCheckBox.clicked.connect(self.on_check_wed_clicked)
        self.wedCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.thuCheckBox = QCheckBox()
        self.thuCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.thuCheckBox.setText("Thu")
        self.thuCheckBox.clicked.connect(self.on_check_thu_clicked)
        self.thuCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.friCheckBox = QCheckBox()
        self.friCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.friCheckBox.setText("Fri")
        self.friCheckBox.clicked.connect(self.on_check_fri_clicked)
        self.friCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.satCheckBox = QCheckBox()
        self.satCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.satCheckBox.setText("Sat")
        self.satCheckBox.clicked.connect(self.on_check_sat_clicked)
        self.satCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Time to run widget
        ################################################################################
        self.timeToRunWidget = QWidget(self)
        self.timeToRunWidget.setGeometry(285, 100, 390, 140)
        self.timeToRunWidget.setStyleSheet("""
            border-top: 0px;
            border-bottom: 0px;
            border-left: 0px;
            border-right: 0px;
        """)

        # Time to run title
        self.timeToRunTitle = QLabel(self.timeToRunWidget)
        self.timeToRunTitle.setFont(QFont(mainFont,smallFontSize))
        self.timeToRunTitle.setText("<h1>Time to run:</h1>")
        self.timeToRunTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.timeToRunTitle.adjustSize()
        self.timeToRunTitle.setStyleSheet("""
            border: transparent;
        """)

        # Time to run layout
        self.timeToRunLayout = QGridLayout(self.timeToRunWidget)

        # Time settings
        self.timesGridLayout = QGridLayout()

        # Radio buttons
        self.oneTimePerDayRadio = QRadioButton()
        self.oneTimePerDayRadio.setFont(QFont(mainFont,normalFontSize))
        self.oneTimePerDayRadio.setText("At:")
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
        self.moreTimePerDayRadio.setFont(QFont(mainFont,normalFontSize))
        self.moreTimePerDayRadio.setToolTip(
            "Back up will be execute every x hours.\n"
            "This will produce a time folder inside your backup device.\n"
            "Fx: 12-12-12/10-00\n"
            "10-00, is the time of the back up (10:00).")

        self.moreTimePerDayRadio.setText("Every:")
        self.moreTimePerDayRadio.adjustSize()
        self.moreTimePerDayRadio.setStyleSheet("""
            border-color: transparent;
        """)
        self.moreTimePerDayRadio.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.hoursSpinBox = QSpinBox()
        self.hoursSpinBox.setFont(QFont(mainFont, 14))
        self.hoursSpinBox.setFixedSize(50, 30)
        self.hoursSpinBox.setFrame(False)
        self.hoursSpinBox.setMinimum(0)
        self.hoursSpinBox.setSingleStep(1)
        self.hoursSpinBox.setMaximum(23)
        self.hoursSpinBox.valueChanged.connect(self.label_hours_changed)
        self.hoursSpinBox.setStyleSheet(timeBox)

        # : between hours and minutes
        self.betweenHoursAndMinutesLabel = QLabel()
        self.betweenHoursAndMinutesLabel.setFont(QFont(mainFont, 18))
        self.betweenHoursAndMinutesLabel.setText(":")
        self.betweenHoursAndMinutesLabel.setStyleSheet("""
            border-color: transparent;
        """)

        # Hours title
        self.hoursTitle = QLabel()
        self.hoursTitle.setFont(QFont(mainFont, 4))
        self.hoursTitle.setText("<h1>Hours</h1>")
        self.hoursTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.hoursTitle.setStyleSheet("""
            border-color: transparent;
            border-radius: 5px;
        """)

        # Minutes title
        self.minutesTitle = QLabel()
        self.minutesTitle.setFont(QFont(mainFont, 4))
        self.minutesTitle.setText("<h1>Minutes</h1>")
        self.minutesTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.minutesTitle.setStyleSheet("""
            border-color: transparent;
        """)

        # Spinbox Hours
        self.minutesSpinBox = QSpinBox()
        self.minutesSpinBox.setFont(QFont(mainFont, 14))
        self.minutesSpinBox.setFixedSize(50, 30)
        self.minutesSpinBox.setFrame(False)
        self.minutesSpinBox.setStyleSheet(timeBox)

        self.minutesSpinBox.setMinimum(0)
        self.minutesSpinBox.setSingleStep(1)
        self.minutesSpinBox.setMaximum(59)
        self.minutesSpinBox.valueChanged.connect(self.label_minutes_changed)

        # Multiple time per day combobox
        self.multipleTimePerDayComboBox = QComboBox()
        self.multipleTimePerDayComboBox.setFrame(True)
        self.multipleTimePerDayComboBox.setFixedSize(132, 28)
        self.multipleTimePerDayComboBox.setFont(QFont(mainFont,normalFontSize))
        self.multipleTimePerDayComboBox.setStyleSheet(timeBox)

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
        self.flatpakWidget.setGeometry(285, 240, 390, 80)
        self.flatpakWidget.setStyleSheet(
        "QWidget"
        "{"
        "border-bottom: 0px;"
        "border-left: 0px;"
        "border-right: 0px;"
        "}")

        # Notification layout
        self.flatpakLayout = QVBoxLayout(self.flatpakWidget)
        self.flatpakLayout.setSpacing(5)

        # Notification title
        self.flatpakTitle = QLabel()
        self.flatpakTitle.setFont(QFont(mainFont,smallFontSize))
        self.flatpakTitle.setText("<h1>Flatpak Settings:</h1>")
        self.flatpakTitle.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.flatpakTitle.setFixedSize(200, 30)
        self.flatpakTitle.setStyleSheet("""
            border: transparent;
        """)

        # Flatpak Name checkbox
        self.allowFlatpakNamesCheckBox = QCheckBox()
        self.allowFlatpakNamesCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.allowFlatpakNamesCheckBox.setText(f"Back up Flatpaks")
        self.allowFlatpakNamesCheckBox.adjustSize()
        self.allowFlatpakNamesCheckBox.setStyleSheet("""
            border: transparent;
        """)
        self.allowFlatpakNamesCheckBox.clicked.connect(self.on_allow__flatpak_names_clicked)
        
        # Flatpak Data checkbox
        self.allowFlatpakDataCheckBox = QCheckBox()
        self.allowFlatpakDataCheckBox.setFont(QFont(mainFont,normalFontSize))
        self.allowFlatpakDataCheckBox.setText(f"Back up Flatpaks Data " 
            "")
        self.allowFlatpakDataCheckBox.adjustSize()
        self.allowFlatpakDataCheckBox.setStyleSheet("""
            border: transparent;
        """)
        self.allowFlatpakDataCheckBox.clicked.connect(self.on_allow__flatpak_data_clicked)

        ################################################################################
        # Reset widget
        ################################################################################
        self.resetWidget = QWidget(self)
        self.resetWidget.setGeometry(285, 320, 390, 90)
         
        # Reset layout
        self.resetLayout = QVBoxLayout(self.resetWidget)
        self.resetLayout.setSpacing(0)
        
        # Reset title
        self.resetTitle = QLabel()
        self.resetTitle.setFont(QFont(mainFont,smallFontSize))
        self.resetTitle.setText("<h1>Reset:</h1>")
        self.resetTitle.adjustSize()
        self.resetTitle.setAlignment(QtCore.Qt.AlignLeft)

        # Reset label text
        self.resetText = QLabel()
        self.resetText.setFont(QFont(mainFont,normalFontSize))
        self.resetText.setText('If something seems broken, click on "Reset", to reset settings.')
        self.resetText.adjustSize()

        ################################################################################
        # Fix button
        ################################################################################
        self.fixButton = QPushButton()
        self.fixButton.setFont(QFont(mainFont,normalFontSize))
        self.fixButton.setText("   Reset   ")
        self.fixButton.adjustSize()
        self.fixButton.setFixedHeight(buttonHeightSize)
        self.fixButton.setStyleSheet(self.buttonStylesheetDetector)
        self.fixButton.clicked.connect(self.on_button_fix_clicked)

        ################################################################################
        # Donate, Update and Save buttons
        ################################################################################
        self.donateAndBackWidget = QWidget(self)
        self.donateAndBackWidget.setGeometry(310, 390, 380, 60)

        # Donate and Settings widget
        self.donateAndBackLayout = QHBoxLayout(self.donateAndBackWidget)
        self.donateAndBackLayout.setSpacing(10)

        # Donate buton
        self.donateButton = QPushButton()
        self.donateButton.setText("Donate")
        self.donateButton.setFont(QFont(mainFont,normalFontSize))
        self.donateButton.adjustSize()
        self.donateButton.clicked.connect(self.donate_clicked)

        ################################################################################
        # Save button
        ################################################################################
        self.saveButton = QPushButton()
        self.saveButton.setFont(QFont(mainFont,normalFontSize))
        self.saveButton.setText("   Back   ")
        self.saveButton.adjustSize()
        self.saveButton.setFixedHeight(buttonHeightSize)
        self.saveButton.setStyleSheet(self.buttonStylesheetDetector)
        self.saveButton.clicked.connect(self.on_save_button_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left layout
        self.leftLayout.addWidget(self.leftTitle, 0, Qt.AlignLeft | Qt.AlignTop)

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
        # self.donateAndBackLayout.addWidget(self.donateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndBackLayout.addWidget(self.saveButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        
        self.setLayout(self.leftLayout)

        self.get_folders()

    def get_folders(self):
        ################################################################################
        # Read Ini File
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        getIniFolders = config.options('FOLDER')
        ################################################################################
        # Get Home Folders and Sort them alphabetically
        # Add On Screen
        ################################################################################
        for folder in get_home_folders():
            # Hide hidden folder
            if not "." in folder:   
                # Checkboxes
                self.foldersCheckbox = QCheckBox(self.leftFrame)
                self.foldersCheckbox.setText(folder)
                self.foldersCheckbox.setFont(QFont(mainFont,normalFontSize))
                self.foldersCheckbox.adjustSize()
                # self.foldersCheckbox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/folder.png"))
                self.foldersCheckbox.setStyleSheet(
                    "QCheckBox"
                    "{"
                    "border-color: transparent;"
                    "}")
                self.foldersCheckbox.clicked.connect(lambda *args, folder=folder: self.on_folder_clicked(folder))
                
                # Activate checkboxes in user.ini
                if folder.lower() in getIniFolders:
                    self.foldersCheckbox.setChecked(True)

                # Add to layout self.leftLayout
                self.leftLayout.addWidget(self.foldersCheckbox, 0, QtCore.Qt.AlignTop)

        self.dates()

    def dates(self):
        ################################################################################
        # Dates
        # Check each dates
        ################################################################################
        if str(mainIniFile.ini_next_backup_sun()) == "true":
            self.sunCheckBox.setChecked(True)

        if str(mainIniFile.ini_next_backup_mon()) == "true":
            self.monCheckBox.setChecked(True)

        if str(mainIniFile.ini_next_backup_tue()) == "true":
            self.tueCheckBox.setChecked(True)

        if str(mainIniFile.ini_next_backup_wed()) == "true":
            self.wedCheckBox.setChecked(True)

        if str(mainIniFile.ini_next_backup_thu()) == "true":
            self.thuCheckBox.setChecked(True)

        if str(mainIniFile.ini_next_backup_fri()) == "true":
            self.friCheckBox.setChecked(True)

        if str(mainIniFile.ini_next_backup_sat()) == "true":
            self.satCheckBox.setChecked(True)

        self.time_to_run()

    def time_to_run(self):
        self.hoursSpinBox.setValue(int(mainIniFile.ini_next_hour()))
        self.minutesSpinBox.setValue(int(mainIniFile.ini_next_minute()))

        ################################################################################
        # Get info from INI file
        # One time per day
        ################################################################################
        if str(mainIniFile.ini_one_time_mode()) == "true":
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
        elif str(mainIniFile.ini_multiple_time_mode()) == "true":
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
        if str(mainIniFile.ini_everytime()) == "60":
            self.multipleTimePerDayComboBox.setCurrentIndex(0)

        elif str(mainIniFile.ini_everytime()) == "120":
            self.multipleTimePerDayComboBox.setCurrentIndex(1)

        elif str(mainIniFile.ini_everytime()) == "240":
            self.multipleTimePerDayComboBox.setCurrentIndex(2)

        self.flatpak_settings()

    def flatpak_settings(self):
        ################################################################################
        # Flatpak settings
        ################################################################################
        # Flatpak names
        if str(mainIniFile.ini_allow_flatpak_names()) == "true":
            self.allowFlatpakNamesCheckBox.setChecked(True)

        # Flatpak data
        if str(mainIniFile.ini_allow_flatpak_data()) == "true":
            self.allowFlatpakDataCheckBox.setChecked(True)

    def on_folder_clicked(self, output):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if config.has_option('FOLDER', output):
                    config.remove_option('FOLDER', output)
                else:
                    config.set('FOLDER', output, 'true')

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def on_every_combox_changed(self):
        chooseMultipleTimePerDayCombox = self.multipleTimePerDayComboBox.currentIndex()
        
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if chooseMultipleTimePerDayCombox == 0:
                    config.set('SCHEDULE', 'everytime', '60')

                elif chooseMultipleTimePerDayCombox == 1:
                    config.set('SCHEDULE', 'everytime', '120')

                elif chooseMultipleTimePerDayCombox == 2:
                    config.set('SCHEDULE', 'everytime', '240')

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def on_check_sun_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.sunCheckBox.isChecked():
                    config.set('SCHEDULE', 'sun', 'true')
                    print("Sun")
                else:
                    config.set('SCHEDULE', 'sun', 'false')

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def on_check_mon_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.monCheckBox.isChecked():
                    config.set('SCHEDULE', 'mon', 'true')
                    print("Mon")
                else:
                    config.set('SCHEDULE', 'mon', 'false')

                # Write to INI file
                config.write(configfile)
        except:
            pass

    def on_check_tue_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.tueCheckBox.isChecked():
                    config.set('SCHEDULE', 'tue', 'true')
                    print("Tue")
                else:
                    config.set('SCHEDULE', 'tue', 'false')

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def on_check_wed_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.wedCheckBox.isChecked():
                    config.set('SCHEDULE', 'wed', 'true')
                    print("Wed")
                else:
                    config.set('SCHEDULE', 'wed', 'false')

                # Write to INI file
                config.write(configfile)
        except:
            pass

    def on_check_thu_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.thuCheckBox.isChecked():
                    config.set('SCHEDULE', 'thu', 'true')
                    print("Thu")
                else:
                    config.set('SCHEDULE', 'thu', 'false')

                # Write to INI file
                config.write(configfile)
        except:
            pass

    def on_check_fri_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.friCheckBox.isChecked():
                    config.set('SCHEDULE', 'fri', 'true')
                    print("Fri")
                else:
                    config.set('SCHEDULE', 'fri', 'false')

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def on_check_sat_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.satCheckBox.isChecked():
                    config.set('SCHEDULE', 'sat', 'true')
                    print("Sat")
                else:
                    config.set('SCHEDULE', 'sat', 'false')

                # Write to INI file
                config.write(configfile)    

        except:
            pass

    def label_hours_changed(self):
        hours = str(self.hoursSpinBox.value())
        try:
            # Save hours
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # with open(src_user_config, 'w+') as configfile:
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                config.set('SCHEDULE', 'hours', hours)
                if hours in fixMinutes:
                    config.set('SCHEDULE', 'hours', '0' + hours)

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def label_minutes_changed(self):
        minutes = str(self.minutesSpinBox.value())
        try:
            # Save minutes
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # with open(src_user_config, 'w+') as configfile:
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                config.set('SCHEDULE', 'minutes', minutes)
                if minutes in fixMinutes:
                    config.set('SCHEDULE', 'minutes', '0' + minutes)

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def on_frequency_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # with open(src_user_config, 'w+') as configfile:
            with open(src_user_config, 'w', encoding='utf8') as configfile:
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
        except:
            pass

    def on_allow__flatpak_names_clicked(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
                if self.allowFlatpakNamesCheckBox.isChecked():
                    config.set('BACKUP', 'allow_flatpak_names', 'true')
                    print("Allow flatpaks installed names")
                else:
                    config.set('BACKUP', 'allow_flatpak_names', 'false')
                    config.set('BACKUP', 'allow_flatpak_data', 'false')
                    self.allowFlatpakDataCheckBox.setChecked(False)

                # Write to INI file
                config.write(configfile)

        except:
            pass

    def on_allow__flatpak_data_clicked(self):
        try:
            # If user allow app to back up data, auto activate
            # backup flatpaks name too.
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:
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

        except:
            pass

    def on_apparence_button_clicked(self):
        # Reset settings
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w', encoding='utf8') as configfile:
            # Mode section
            # True = Dark, White = False
            if main.darkMode == "true":
                print((main.darkMode))

                config.set('MODE', 'dark_mode', 'false')
            else:
                config.set('MODE', 'dark_mode', 'true')

            # Write to INI file
            config.write(configfile)

        themeChanger = QMessageBox.question(self, 'Change Theme', 
        f'Will be applied after {appName} is restarted.',
        QMessageBox.Ok)

        if themeChanger == QMessageBox.Ok:
            QMessageBox.Close

    def on_button_fix_clicked(self):
        resetConfirmation = QMessageBox.question(self, 'Reset', 
            'Are you sure you want to reset settings?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resetConfirmation == QMessageBox.Yes:
            try:
                
                main.lastestBackupLabel.setText("Latest Backup: None")
                main.oldestBackupLabel.setText("Oldest Backup: None")

                # Reset settings
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w', encoding='utf8') as configfile:
                    # Backup section
                    config.set('BACKUP', 'auto_backup', 'false')
                    config.set('BACKUP', 'backup_now', 'false')
                    config.set('BACKUP', 'checker_running', 'false')
                    config.set('BACKUP', 'allow_flatpak_names', 'true')
                    config.set('BACKUP', 'allow_flatpak_data', 'false')
                    config.set('BACKUP', 'skip_this_backup', 'false')

                    # External section
                    config.set('EXTERNAL', 'hd', 'None')
                    config.set('EXTERNAL', 'name', 'None')

                    # Mode section
                    config.set('MODE', 'one_time_mode', 'true')
                    config.set('MODE', 'more_time_mode', 'false')

                    # System tray  section
                    config.set('SYSTEMTRAY', 'system_tray', 'false')

                    # Schedule section
                    config.set('SCHEDULE', 'sun', 'true')
                    config.set('SCHEDULE', 'mon', 'true')
                    config.set('SCHEDULE', 'tue', 'true')
                    config.set('SCHEDULE', 'wed', 'true')
                    config.set('SCHEDULE', 'thu', 'true')
                    config.set('SCHEDULE', 'fri', 'true')
                    config.set('SCHEDULE', 'sat', 'true')
                    config.set('SCHEDULE', 'hours', '10')
                    config.set('SCHEDULE', 'minutes', '00')
                    config.set('SCHEDULE', 'everytime', '60')

                    # Info section
                    config.set('INFO', 'language', 'None')
                    config.set('INFO', 'os', 'None')
                    config.set('INFO', 'packageManager', 'None')
                    config.set('INFO', 'icon', 'None')
                    config.set('INFO', 'theme', 'None')
                    config.set('INFO', 'cursor', 'None')
                    config.set('INFO', 'colortheme', 'None')
                    # config.set('INFO', 'oldest', 'None')
                    # config.set('INFO', 'latest', 'None')
                    config.set('INFO', 'next', 'None')
                    config.set('INFO', 'notification_id', '0')
                    config.set('INFO', 'feedback_status', ' ')
                    config.set('INFO', 'auto_reboot', 'false')

                    # Folders section
                    config.set('FOLDER', 'pictures', 'true')
                    config.set('FOLDER', 'documents', 'true')
                    config.set('FOLDER', 'music', 'true')
                    config.set('FOLDER', 'videos', 'true')
                    config.set('FOLDER', 'desktop', 'true')

                    # Restore section
                    config.set('RESTORE', 'is_restore_running', 'none')
                    config.set('RESTORE', 'applications_packages', 'false')
                    config.set('RESTORE', 'applications_flatpak_names', 'false')
                    config.set('RESTORE', 'applications_data', 'false')
                    config.set('RESTORE', 'files_and_folders', 'false')
                    config.set('RESTORE', 'system_settings', 'false')

                    # Write to INI file
                    config.write(configfile)
            
            except:
                pass

            print("All settings was reset!")

        else:
            QMessageBox.Close

    def donate_clicked(self):
        sub.Popen("xdg-open https://ko-fi.com/geovanejeff", shell=True)

    def on_save_button_clicked(self):
        widget.setCurrentWidget(main)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ####################
    mainIniFile = UPDATEINIFILE()
    main = MAIN()
    mainOpitions = OPTION()

    widget = QStackedWidget()
    widget.addWidget(main)   
    widget.addWidget(mainOpitions) 
    widget.setCurrentWidget(main)   
    widget.show()

    widget.setWindowTitle(appName)
    widget.setWindowIcon(QIcon(src_backup_icon))
    widget.setFixedSize(700,450)

    app.exit(app.exec())
        

