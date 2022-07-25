#! /usr/bin/python3
from setup import *


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("Options Screen")
        self.setWindowIcon(QIcon(src_backup_icon))
        self.setFixedSize(800, 550)

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
        self.leftWidget.setGeometry(20, 20, 240, 505)
        self.leftWidget.setStyleSheet(
        "QWidget"
        "{"
            "border-right: 1px solid rgb(198, 198, 198);"
        "}")

        # Left layout
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setContentsMargins(20, 20, 20, 20)

        # Left title
        self.leftTitle = QLabel()
        self.leftTitle.setFont(QFont("Ubuntu", 11))
        self.leftTitle.setText("Available folders to be\nback up:")
        self.leftTitle.adjustSize()

        # Frame
        self.leftFrame = QFrame()
        self.leftFrame.adjustSize()
        # self.leftFrame.setStyleSheet(
        #     "QFrame"
        #     "{"
        #         "background-color: rgb(36, 37, 38);"
        #     "}")

        ################################################################################
        # Days to run widget
        ################################################################################
        self.daysToRunWidget = QWidget(self)
        self.daysToRunWidget.setGeometry(280, 20, 490, 80)
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
        self.timeToRunWidget.setGeometry(280, 100, 490, 160)
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
        self.oneTimePerDayRadio.setFixedSize(180, 30)
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
        self.moreTimePerDayRadio.setFixedSize(180, 30)
        self.moreTimePerDayRadio.setStyleSheet("""
            border-color: transparent;
        """)
        self.moreTimePerDayRadio.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.hoursSpinBox = QSpinBox()
        self.hoursSpinBox.setFont(QFont("Ubuntu", 14))
        self.hoursSpinBox.setFixedSize(60, 40)
        self.hoursSpinBox.setFrame(True)
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
        self.hoursTitle.setFont(QFont("Ubuntu", 11))
        self.hoursTitle.setText("Hours")
        self.hoursTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.hoursTitle.setStyleSheet("""
            border-color: transparent;
            border-radius: 5px;
        """)

        # Minutes title
        self.minutesTitle = QLabel()
        self.minutesTitle.setFont(QFont("Ubuntu", 11))
        self.minutesTitle.setText("Minutes")
        self.minutesTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.minutesTitle.setStyleSheet("""
            border-color: transparent;
        """)

        # Spinbox Hours
        self.minutesSpinBox = QSpinBox()
        self.minutesSpinBox.setFont(QFont("DejaVu Sans", 14))
        self.minutesSpinBox.setFixedSize(60, 40)
        self.minutesSpinBox.setFrame(True)
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
        self.multipleTimePerDayComboBox.setFixedSize(150, 28)
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
        self.flatpakWidget.setGeometry(280, 260, 490, 80)
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
            "(Back up flatpak names is necessary)")
        self.allowFlatpakDataCheckBox.adjustSize()
        self.allowFlatpakDataCheckBox.setStyleSheet("""
            border: transparent;
        """)
        self.allowFlatpakDataCheckBox.clicked.connect(self.on_allow__flatpak_data_clicked)

        ################################################################################
        # Reset widget
        ################################################################################
        self.resetWidget = QWidget(self)
        self.resetWidget.setGeometry(280, 340, 490, 90)
 
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
        # self.fixButton.setFixedSize(80, 28)
        self.fixButton.adjustSize()
        self.fixButton.clicked.connect(self.on_button_fix_clicked)

        ################################################################################
        # Donate, Update and Save buttons
        ################################################################################
        self.donateAndSaveWidget = QWidget(self)
        self.donateAndSaveWidget.setGeometry(568, 490, 220, 60)

        # Donate and Settings widget
        self.donateAndSaveLayout = QHBoxLayout(self.donateAndSaveWidget)
        self.donateAndSaveLayout.setSpacing(10)

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
        self.saveButton.setText("Save and Close")
        self.saveButton.clicked.connect(self.on_save_button_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left layout
        self.leftLayout.addWidget(self.leftTitle, 0, Qt.AlignLeft | Qt.AlignTop)
        self.leftLayout.addWidget(self.leftFrame, 0, Qt.AlignLeft | Qt.AlignTop)

        # Days to run layout V
        self.daysToRunLayoutV.addWidget(self.daysToRunTitle, 0, Qt.AlignVCenter | Qt.AlignLeft)
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
        self.timeToRunLayout.addWidget(self.timeToRunTitle, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.oneTimePerDayRadio, 1, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.moreTimePerDayRadio, 2, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.multipleTimePerDayComboBox, 2, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addLayout(self.timesGridLayout, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

        # Time grid layout
        self.timesGridLayout.addWidget(self.hoursSpinBox, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timesGridLayout.addWidget(self.betweenHoursAndMinutesLabel, 0, 2, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGridLayout.addWidget(self.minutesSpinBox, 0, 3, Qt.AlignVCenter | Qt.AlignLeft)
        self.timesGridLayout.addWidget(self.hoursTitle, 1, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGridLayout.addWidget(self.minutesTitle, 1, 3, Qt.AlignVCenter | Qt.AlignHCenter)

        # Flaptak settings
        self.flatpakLayout.addWidget(self.flatpakTitle)
        self.flatpakLayout.addWidget(self.allowFlatpakNamesCheckBox)
        self.flatpakLayout.addWidget(self.allowFlatpakDataCheckBox)

        # Reset layout
        self.resetLayout.addWidget(self.resetTitle, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.resetText, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.fixButton, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Save layout
        self.donateAndSaveLayout.addWidget(self.donateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndSaveLayout.addWidget(self.saveButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)

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
                config.set('RESTORE', 'applications_name', 'true')
                config.set('RESTORE', 'application_data', 'false')
                config.set('RESTORE', 'files_and_folders', 'false')

                # Write to INI file
                config.write(configfile)

            print("All settings was reset!")
            exit()

        else:
            QMessageBox.Close

    def donate_clicked(self):
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)

    def on_save_button_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
        self.iniBackupIsRunning = config['BACKUP']['checker_running']
        
        # Is is checker is not running and auto is enabled
        if self.iniAutomaticallyBackup == "true":
            # If backup chcker is already running, do nothing
            if self.iniBackupIsRunning == "false":
                # Call backup check py
                sub.Popen(f"python3 {src_backup_check_py}", shell=True)

                # Set checker running to true
                with open(src_user_config, 'w') as configfile:
                    config.set('BACKUP', 'checker_running', "true")
                    config.write(configfile)
            else:
                print("Backup checker is already running.")
                print("Exiting...")

        exit()


app = QApplication(sys.argv)
tic = time.time()
main = UI()
main.show()
toc = time.time()
print(f'Options {(toc-tic):.4f} seconds')
sys.exit(app.exec())


