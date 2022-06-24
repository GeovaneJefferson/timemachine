#! /usr/bin/env python3
from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("Options Screen")
        self.setWindowIcon(QIcon(src_restore_icon))
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
        # Read version.txt file, for version numbers
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'next', f'{self.nextDay}, {self.iniNextHour}:{self.iniNextMinute}')
            config.write(configfile)

        # Apps version
        version = QLabel(self)
        version.setFont(item)
        version.setText(appVersion)
        version.setFixedSize(80, 20)
        version.move(270, 505)

        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 240, 500)
        self.leftWidget.setStyleSheet(
        "QWidget"
        "{"
            "border-right: 1px solid rgb(68, 69, 70);"
        "}")

        # Left layout
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setContentsMargins(20, 0, 20, 20)

        # Left title
        self.leftTitle = QLabel()
        self.leftTitle.setFont(topicTitle)
        self.leftTitle.setText("Available folders to be\nback up:")
        self.leftTitle.setFixedSize(250, 40)

        # Frame
        self.leftFrame = QFrame()
        self.leftFrame.setFixedSize(250, 500)
        # self.leftFrame.setStyleSheet(
        #     "QFrame"
        #     "{"
        #         "background-color: rgb(36, 37, 38);"
        #     "}")

        ################################################################################
        # Days to run widget
        ################################################################################
        self.daysToRunWidget = QWidget(self)
        self.daysToRunWidget.setGeometry(280, 20, 500, 80)
        self.daysToRunWidget.setStyleSheet("""
            border-top: 1px solid rgb(68, 69, 70);
        """)

        # Days to run layout V
        self.daysToRunLayoutV = QVBoxLayout(self.daysToRunWidget)
        self.daysToRunLayoutV.setSpacing(10)
        # self.daysToRunLayoutV.setContentsMargins(20, 0, 20, 20)

        # Days to run layout H
        self.daysToRunLayoutH = QHBoxLayout()
        self.daysToRunLayoutH.setSpacing(10)
        # self.daysToRunLayoutV.setContentsMargins(20, 0, 20, 20)

        # Days to run title
        self.daysToRunTitle = QLabel()
        self.daysToRunTitle.setFont(topicTitle)
        self.daysToRunTitle.setText("Days to run:")
        self.daysToRunTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.daysToRunTitle.setFixedSize(200, 30)
        self.daysToRunTitle.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Checkboxes
        ################################################################################
        self.sunCheckBox = QCheckBox()
        self.sunCheckBox.setFont(item)
        self.sunCheckBox.setText("Sun")
        self.sunCheckBox.clicked.connect(self.on_check_sun_clicked)
        self.sunCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.monCheckBox = QCheckBox()
        self.monCheckBox.setFont(item)
        self.monCheckBox.setText("Mon")
        self.monCheckBox.clicked.connect(self.on_check_mon_clicked)
        self.monCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.tueCheckBox = QCheckBox()
        self.tueCheckBox.setFont(item)
        self.tueCheckBox.setText("Tue")
        self.tueCheckBox.clicked.connect(self.on_check_tue_clicked)
        self.tueCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.wedCheckBox = QCheckBox()
        self.wedCheckBox.setFont(item)
        self.wedCheckBox.setText("Wed")
        self.wedCheckBox.clicked.connect(self.on_check_wed_clicked)
        self.wedCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.thuCheckBox = QCheckBox()
        self.thuCheckBox.setFont(item)
        self.thuCheckBox.setText("Thu")
        self.thuCheckBox.clicked.connect(self.on_check_thu_clicked)
        self.thuCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.friCheckBox = QCheckBox()
        self.friCheckBox.setFont(item)
        self.friCheckBox.setText("Fri")
        self.friCheckBox.clicked.connect(self.on_check_fri_clicked)
        self.friCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.satCheckBox = QCheckBox()
        self.satCheckBox.setFont(item)
        self.satCheckBox.setText("Sat")
        self.satCheckBox.clicked.connect(self.on_check_sat_clicked)
        self.satCheckBox.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Time to run widget
        ################################################################################
        self.timeToRunWidget = QWidget(self)
        self.timeToRunWidget.setGeometry(280, 100, 500, 180)
        self.timeToRunWidget.setStyleSheet("""
            border-top: 1px solid rgb(68, 69, 70);
            border-bottom: 1px solid rgb(68, 69, 70);
        """)

        # Time to run title
        self.timeToRunTitle = QLabel(self.timeToRunWidget)
        self.timeToRunTitle.setFont(topicTitle)
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
        self.oneTimePerDayRadio.setFont(item)
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
        self.moreTimePerDayRadio.setFont(item)
        self.moreTimePerDayRadio.setToolTip(
            "Back up will be execute every x minutes/hours.\n"
            "This will produce a time folder inside the choose external location.\n"
            "Fx: 12-12-12/10-30\n"
            "10-30, is the time of the back up (10:30).")

        self.moreTimePerDayRadio.setText("Multiple times per day")
        self.moreTimePerDayRadio.setFixedSize(180, 30)
        self.moreTimePerDayRadio.setStyleSheet("""
            border-color: transparent;
        """)
        self.moreTimePerDayRadio.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.hoursSpinBox = QSpinBox()
        self.hoursSpinBox.setFont(QFont("DejaVu Sans", 14))
        self.hoursSpinBox.setFixedSize(60, 40)
        self.hoursSpinBox.setFrame(True)
        self.hoursSpinBox.setMinimum(0)
        self.hoursSpinBox.setSingleStep(1)
        self.hoursSpinBox.setMaximum(23)
        self.hoursSpinBox.valueChanged.connect(self.label_hours_changed)
        self.hoursSpinBox.setStyleSheet(
        "QSpinBox"
           "{"
            "border: 0px solid transparent;"
            "border-radius: 5px;"
           "}")

        # : between hours and minutes
        self.betweenHoursAndMinutesLabel = QLabel()
        self.betweenHoursAndMinutesLabel.setFont(QFont("DejaVu Sans", 18))
        self.betweenHoursAndMinutesLabel.setText(":")
        self.betweenHoursAndMinutesLabel.setStyleSheet("""
            border-color: transparent;
        """)

        # Hours title
        self.hoursTitle = QLabel()
        self.hoursTitle.setFont(QFont("DejaVu Sans", 12))
        self.hoursTitle.setText("Hours")
        self.hoursTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.hoursTitle.setStyleSheet("""
            border-color: transparent;
            border-radius: 5px;
        """)

        # Minutes title
        self.minutesTitle = QLabel()
        self.minutesTitle.setFont(QFont("DejaVu Sans", 12))
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
                "border-radius: 5px;"
            "}")

        self.minutesSpinBox.setMinimum(0)
        self.minutesSpinBox.setSingleStep(1)
        self.minutesSpinBox.setMaximum(59)
        self.minutesSpinBox.valueChanged.connect(self.label_minutes_changed)

        # Multiple time per day combobox
        self.multipleTimePerDayComboBox = QComboBox()
        self.multipleTimePerDayComboBox.setFrame(True)
        self.multipleTimePerDayComboBox.setFixedSize(155, 28)
        self.multipleTimePerDayComboBox.setFont(item)
        self.multipleTimePerDayComboBox.setStyleSheet(
        "QComboBox"
            "{"
                "border: 0px solid transparent;"
                "border-radius: 5px;"
            "}")

        multipleTimerPerDayComboBoxList = [
            "Every 30 minutes",
            "Every 1 hour",
            "Every 2 hours",
            "Every 4 hours"]
        self.multipleTimePerDayComboBox.addItems(multipleTimerPerDayComboBoxList)
        self.multipleTimePerDayComboBox.currentIndexChanged.connect(self.on_every_combox_changed)

        ################################################################################
        # Notification settings
        ################################################################################
        self.notificationWidget = QWidget(self)
        self.notificationWidget.setGeometry(280, 280, 500, 80)
        self.notificationWidget.setStyleSheet(
        "QWidget"
        "{"
        "border-bottom: 1px solid rgb(68, 69, 70);"
        "}")

        # Notification layout
        self.notificationLayout = QVBoxLayout(self.notificationWidget)
        self.notificationLayout.setSpacing(5)

        # Notification title
        self.notificationTitle = QLabel()
        self.notificationTitle.setFont(topicTitle)
        self.notificationTitle.setText("Notification:")
        self.notificationTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.notificationTitle.setFixedSize(200, 30)
        self.notificationTitle.setStyleSheet("""
            border: transparent;
        """)

        # Notification checkbox
        self.notificationCheckBox = QCheckBox(self.notificationWidget)
        self.notificationCheckBox.setFont(item)
        self.notificationCheckBox.setText(f"Allow {appName} to send notifications ")
        self.notificationCheckBox.setStyleSheet("""
            border: transparent;
        """)
        self.notificationCheckBox.clicked.connect(self.on_allow__notifications_clicked)

        ################################################################################
        # Reset widget
        ################################################################################
        self.resetWidget = QWidget(self)
        self.resetWidget.setGeometry(280, 360, 500, 100)

        # Reset layout
        self.resetLayout = QVBoxLayout(self.resetWidget)
        self.resetLayout.setSpacing(5)
        # self.daysToRunLayoutV.setContentsMargins(20, 0, 20, 20)

        # Reset title
        self.resetTitle = QLabel()
        self.resetTitle.setFont(topicTitle)
        self.resetTitle.setText("Reset:")
        self.resetTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.resetTitle.setFixedSize(200, 30)   # If something seems broken, click on "Reset", to reset settings.

        # Reset label text
        self.resetText = QLabel()
        self.resetText.setFont(item)
        self.resetText.setText('If something seems broken, click on "Reset", to reset settings.')
        self.resetText.setFixedSize(400, 30)

        ################################################################################
        # Fix button
        ################################################################################
        self.fixButton = QPushButton()
        self.fixButton.setFont(item)
        self.fixButton.setText("Reset")
        self.fixButton.setFixedSize(80, 28)
        self.fixButton.clicked.connect(self.on_button_fix_clicked)

        ################################################################################
        # Donate, Update and Save buttons
        ################################################################################
        self.donateAndSaveWidget = QWidget(self)
        self.donateAndSaveWidget.setGeometry(550, 490, 240, 60)
        # self.donateAndSaveWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Donate and Settings widget
        self.donateAndSaveLayout = QHBoxLayout(self.donateAndSaveWidget)
        self.donateAndSaveLayout.setSpacing(10)

        # Donate buton
        self.donateButton = QPushButton()
        self.donateButton.setText("Donate")
        self.donateButton.setFont(item)
        self.donateButton.setFixedSize(80, 28)
        self.donateButton.clicked.connect(self.donate_clicked)

        ################################################################################
        # Save button
        ################################################################################
        self.saveButton = QPushButton()
        self.saveButton.setFixedSize(120, 28)
        self.saveButton.setFont(item)
        self.saveButton.setText("Save and Close")
        self.saveButton.clicked.connect(self.on_save_button_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left layout
        self.leftLayout.addWidget(self.leftTitle)
        self.leftLayout.addWidget(self.leftFrame, 0, Qt.AlignHCenter | Qt.AlignTop)

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

        # Notifications layout
        self.notificationLayout.addWidget(self.notificationTitle, 0, Qt.AlignLeft | Qt.AlignTop)
        self.notificationLayout.addWidget(self.notificationCheckBox, 0, Qt.AlignLeft | Qt.AlignTop)

        # Reset layout
        self.resetLayout.addWidget(self.resetTitle, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.resetText, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.fixButton, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Save layout
        # self.donateAndSaveLayout.addWidget(updateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndSaveLayout.addWidget(self.donateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndSaveLayout.addWidget(self.saveButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)

        self.setLayout(self.leftLayout)

        self.get_folders()

    def get_folders(self):
        ################################################################################
        # Read INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Folders to backup
        getIniFolders = config.options('FOLDER')

        # More folders
        verticalSpaceLabel = 10
        verticalSpaceCheckbox = verticalSpaceLabel  # Same value as vertical space
        for files in getHomeFolders:
            if not "." in files:    # Do not show hidden folders/files
                # Folders text
                label_text = QLabel(files, self.leftFrame)
                label_text.setFont(item)
                label_text.setFixedSize(150, 22)
                label_text.move(30, verticalSpaceLabel)
                verticalSpaceLabel += 25  # Position

                # Checkboxes
                self.foldersCheckbox = QCheckBox(self.leftFrame)
                self.foldersCheckbox.setStyleSheet("""
                    border-color: transparent;
                """)

                self.foldersCheckbox.setFixedSize(150, 22)
                self.foldersCheckbox.move(5, verticalSpaceCheckbox)
                verticalSpaceCheckbox += 25
                text = label_text.text().lower()  # Lowercase
                self.foldersCheckbox.show()
                self.foldersCheckbox.clicked.connect(lambda *args, text=text: self.on_folder_clicked(text))

                # Activate checkboxes in user.ini
                if text in getIniFolders:
                    self.foldersCheckbox.setChecked(True)

        self.dates()

    def dates(self):
        ################################################################################
        # Read INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

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
        ################################################################################
        # Read INI file
        ################################################################################
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

        # Multiple time per day
        elif iniMultipleTimePerDay == "true":
            self.hoursSpinBox.setEnabled(False)
            self.minutesSpinBox.setEnabled(False)
            self.multipleTimePerDayComboBox.setEnabled(True)
            self.moreTimePerDayRadio.setChecked(True)

        ################################################################################
        # Multiple time per day
        ################################################################################
        if iniEverytime == "30":
            self.multipleTimePerDayComboBox.setCurrentIndex(0)

        elif iniEverytime == "60":
            self.multipleTimePerDayComboBox.setCurrentIndex(1)

        elif iniEverytime == "120":
            self.multipleTimePerDayComboBox.setCurrentIndex(2)

        elif iniEverytime == "240":
            self.multipleTimePerDayComboBox.setCurrentIndex(3)

        self.notification()

    def notification(self):
        ################################################################################
        # Read INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        # Notification
        self.iniNotification = config['INFO']['notification']

        ################################################################################
        # Notifications
        ################################################################################
        if self.iniNotification == "true":
            self.notificationCheckBox.setChecked(True)

    def on_folder_clicked(self, get):
        with open(src_user_config, 'w+') as configfile:
            if config.has_option('FOLDER', get):
                config.remove_option('FOLDER', get)
            else:
                config.set('FOLDER', get, 'true')

            # Write to INI file
            config.write(configfile)

    def on_every_combox_changed(self):
        chooseMultipleTimePerDayCombox = self.multipleTimePerDayComboBox.currentIndex()
        with open(src_user_config, 'w') as configfile:
            if chooseMultipleTimePerDayCombox == 0:
                config.set('SCHEDULE', 'everytime', '30')

            elif chooseMultipleTimePerDayCombox == 1:
                config.set('SCHEDULE', 'everytime', '60')

            elif chooseMultipleTimePerDayCombox == 2:
                config.set('SCHEDULE', 'everytime', '120')

            elif chooseMultipleTimePerDayCombox == 3:
                config.set('SCHEDULE', 'everytime', '240')

            # Write to INI file
            config.write(configfile)

    def on_check_sun_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.sunCheckBox.isChecked():
                config.set('SCHEDULE', 'sun', 'true')
                print("Sun")
            else:
                config.set('SCHEDULE', 'sun', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_mon_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.monCheckBox.isChecked():
                config.set('SCHEDULE', 'mon', 'true')
                print("Mon")
            else:
                config.set('SCHEDULE', 'mon', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_tue_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.tueCheckBox.isChecked():
                config.set('SCHEDULE', 'tue', 'true')
                print("Tue")
            else:
                config.set('SCHEDULE', 'tue', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_wed_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.wedCheckBox.isChecked():
                config.set('SCHEDULE', 'wed', 'true')
                print("Wed")
            else:
                config.set('SCHEDULE', 'wed', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_thu_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.thuCheckBox.isChecked():
                config.set('SCHEDULE', 'thu', 'true')
                print("Thu")
            else:
                config.set('SCHEDULE', 'thu', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_fri_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.friCheckBox.isChecked():
                config.set('SCHEDULE', 'fri', 'true')
                print("Fri")
            else:
                config.set('SCHEDULE', 'fri', 'false')

            # Write to INI file
            config.write(configfile)

    def on_check_sat_clicked(self):
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
        with open(src_user_config, 'w+') as configfile:
            config.set('SCHEDULE', 'hours', hours)
            if hours in fixMinutes:
                config.set('SCHEDULE', 'hours', '0' + hours)

            # Write to INI file
            config.write(configfile)

    def label_minutes_changed(self):
        minutes = str(self.minutesSpinBox.value())

        # Save minutes
        with open(src_user_config, 'w+') as configfile:
            config.set('SCHEDULE', 'minutes', minutes)
            if minutes in fixMinutes:
                config.set('SCHEDULE', 'minutes', '0' + minutes)

            # Write to INI file
            config.write(configfile)

    def on_frequency_clicked(self):
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

            elif self.moreTimePerDayRadio.isChecked():
                config.set('MODE', 'more_time_mode', 'true')
                print("Multiple time per day selected")
                # DISABLE ONE TIME MODE
                config.set('MODE', 'one_time_mode', 'false')

                self.hoursSpinBox.setEnabled(False)
                self.minutesSpinBox.setEnabled(False)
                self.multipleTimePerDayComboBox.setEnabled(True)
                self.moreTimePerDayRadio.setChecked(True)

            # Write to INI file
            config.write(configfile)

    def on_allow__notifications_clicked(self):
        ################################################################################
        # Allow app to send notifications
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            if self.notificationCheckBox.isChecked():
                config.set('INFO', 'notification', 'true')

            else:
                config.set('INFO', 'notification', 'false')

            # Write to INI file
            print("Notifications enabled")
            config.write(configfile)

    def on_button_fix_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        resetConfirmation = QMessageBox.question(self, 'Reset', 'Are you sure you want to reset settings?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resetConfirmation == QMessageBox.Yes:
            # Reset settings
            with open(src_user_config, 'w') as configfile:
                # Backup section
                config.set('BACKUP', 'first_startup', 'false')
                config.set('BACKUP', 'auto_backup', 'false')
                config.set('BACKUP', 'backup_now', 'false')
                config.set('BACKUP', 'checker_running', 'false')
                # External section
                config.set('EXTERNAL', 'hd', 'None')
                config.set('EXTERNAL', 'name', 'None')
                # Mode section
                config.set('MODE', 'one_time_mode', 'true')
                config.set('MODE', 'more_time_mode', 'false')
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
                # Info section
                config.set('INFO', 'latest', 'None')
                config.set('INFO', 'next', 'None')
                config.set('INFO', 'notification', 'true')
                config.set('INFO', 'notification_id', '0')
                # Folders section
                config.set('FOLDER', 'documents', 'true')
                config.set('FOLDER', 'music', 'true')
                config.set('FOLDER', 'videos', 'true')
                config.set('FOLDER', 'pictures', 'true')
                # Write to INI file
                config.write(configfile)

            print("All settings was reset!")
            # Call notification
            sub.Popen(f"python3 {src_notification}", shell=True)
            exit()

        else:
            QMessageBox.Close

    def donate_clicked(self):
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)

    def on_save_button_clicked(self):
        ################################################################################
        # Read INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
        self.iniCheckerRunning = config['BACKUP']['checker_running']

        ################################################################################
        # Call backup checker or not?
        ################################################################################
        # TODO
        if self.iniAutomaticallyBackup == "true" and self.iniCheckerRunning == "true":
            pass

        else:
            ################################################################################
            # Call backup check py
            ################################################################################
            sub.Popen(f"python3 {src_backup_check_py}", shell=True)

            ################################################################################
            # After call backup checker, set checker_running to true
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:  # Set auto backup to true
                config.set('BACKUP', 'checker_running', 'true')
                config.write(configfile)

        exit()


app = QApplication(sys.argv)
tic = time.time()
main = UI()
main.show()
toc = time.time()
print(f'Options {(toc-tic):.4f} seconds')
sys.exit(app.exec())
