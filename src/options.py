#! /usr/bin/env python3
from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setWindowTitle("Options Screen")
        appIcon = QIcon(src_restore_icon)
        self.setWindowIcon(appIcon)
        self.setFixedSize(800, 550)

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
        ## Apps version
        ################################################################################
        version = QLabel(self)
        version.setFont(item)
        version.setText(appVersion)
        version.setFixedSize(80, 20)
        version.move(270, 505)

        ################################################################################
        ## Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 240, 500)
        self.leftWidget.setStyleSheet(
        "QWidget"
        "{"
            "border-right: 1px solid rgb(68, 69, 70);"
        "}")

        # Left widget
        self.baseVLeftLayout = QVBoxLayout(self.leftWidget)
        self.baseVLeftLayout.setSpacing(10)
        self.baseVLeftLayout.setContentsMargins(20, 0, 20, 20)

        # Label
        self.label = QLabel()
        self.label.setFont(topicTitle)
        self.label.setText("Available folders to be\nback up:")
        self.label.setFixedSize(250, 40)

        # Frame
        self.foldersFrame = QFrame()
        self.foldersFrame.setFixedSize(250, 500)
        # self.foldersFrame.setStyleSheet(
        #     "QFrame"
        #     "{"
        #         "background-color: rgb(36, 37, 38);"
        #     "}")

        ################################################################################
        ## Days to run widget
        ################################################################################
        self.daysToRunWidget = QWidget(self)
        self.daysToRunWidget.setGeometry(280, 20, 500, 80)
        self.daysToRunWidget.setStyleSheet("""
            border-top: 1px solid rgb(68, 69, 70);
        """)

        # BaseH layout
        self.baseVDaysToRunLayout = QVBoxLayout(self.daysToRunWidget)
        self.baseVDaysToRunLayout.setSpacing(10)
        # self.baseVDaysToRunLayout.setContentsMargins(20, 0, 20, 20)

        # BaseV layout
        self.baseHDaysToRunLayout = QHBoxLayout()
        self.baseHDaysToRunLayout.setSpacing(10)
        # self.baseVDaysToRunLayout.setContentsMargins(20, 0, 20, 20)

        # Label
        self.labelDaysToRun = QLabel()
        self.labelDaysToRun.setFont(topicTitle)
        self.labelDaysToRun.setText("Days to run:")
        self.labelDaysToRun.setAlignment(QtCore.Qt.AlignLeft)
        self.labelDaysToRun.setFixedSize(200, 30)
        self.labelDaysToRun.setStyleSheet("""
            border-color: transparent;
        """)

        # Checkboxes
        self.checkSun = QCheckBox()
        self.checkSun.setFont(item)
        self.checkSun.setText("Sun")
        self.checkSun.clicked.connect(self.on_check_sun_clicked)
        self.checkSun.setStyleSheet("""
            border-color: transparent;
        """)

        self.checkMon = QCheckBox()
        self.checkMon.setFont(item)
        self.checkMon.setText("Mon")
        self.checkMon.clicked.connect(self.on_check_mon_clicked)
        self.checkMon.setStyleSheet("""
            border-color: transparent;
        """)

        self.checkTue = QCheckBox()
        self.checkTue.setFont(item)
        self.checkTue.setText("Tue")
        self.checkTue.clicked.connect(self.on_check_tue_clicked)
        self.checkTue.setStyleSheet("""
            border-color: transparent;
        """)

        self.checkWed = QCheckBox()
        self.checkWed.setFont(item)
        self.checkWed.setText("Wed")
        self.checkWed.clicked.connect(self.on_check_wed_clicked)
        self.checkWed.setStyleSheet("""
            border-color: transparent;
        """)

        self.checkThu = QCheckBox()
        self.checkThu.setFont(item)
        self.checkThu.setText("Thu")
        self.checkThu.clicked.connect(self.on_check_thu_clicked)
        self.checkThu.setStyleSheet("""
            border-color: transparent;
        """)

        self.checkFri = QCheckBox()
        self.checkFri.setFont(item)
        self.checkFri.setText("Fri")
        self.checkFri.clicked.connect(self.on_check_fri_clicked)
        self.checkFri.setStyleSheet("""
            border-color: transparent;
        """)

        self.checkSat = QCheckBox()
        self.checkSat.setFont(item)
        self.checkSat.setText("Sat")
        self.checkSat.clicked.connect(self.on_check_sat_clicked)
        self.checkSat.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        ## Time to run widget
        ################################################################################
        self.timeToRunWidget = QWidget(self)
        self.timeToRunWidget.setGeometry(280, 100, 500, 180)
        self.timeToRunWidget.setStyleSheet("""
            border-top: 1px solid rgb(68, 69, 70);
            border-bottom: 1px solid rgb(68, 69, 70);
        """)

        # Label
        self.labelTimeToRun = QLabel(self.timeToRunWidget)
        self.labelTimeToRun.setFont(topicTitle)
        self.labelTimeToRun.setText("Time to run:")
        self.labelTimeToRun.setAlignment(QtCore.Qt.AlignLeft)
        self.labelTimeToRun.setFixedSize(180, 30)
        self.labelTimeToRun.setStyleSheet("""
            border: transparent;
        """)

        # BaseGrid layout
        self.baseHTimeToRunLayout = QGridLayout(self.timeToRunWidget)

        self.timesGrid = QGridLayout()

        # Radio buttons
        self.oneTimeMode = QRadioButton()
        self.oneTimeMode.setFont(item)
        self.oneTimeMode.setText("One time per day")
        self.oneTimeMode.setToolTip("One single back up will be execute every selected day(s) and time.")
        self.oneTimeMode.setFixedSize(180, 30)
        self.oneTimeMode.setStyleSheet(
        "QRadioButton"
           "{"
            "border: 0px solid transparent;"
            "border-radius: 5px;"
           "}")
        self.oneTimeMode.clicked.connect(self.on_frequency_clicked)

        self.moreTimeMode = QRadioButton()
        self.moreTimeMode.setFont(item)
        self.moreTimeMode.setToolTip(
            "Back up will be execute every x minutes/hours.\n"
            "This will produce a time folder inside the choose external location.\n"
            "Fx: 12-12-12/10-30\n"
            "10-30, is the time of the back up (10:30).")

        self.moreTimeMode.setText("Multiple times per day")
        self.moreTimeMode.setFixedSize(180, 30)
        self.moreTimeMode.setStyleSheet("""
            border-color: transparent;
        """)
        self.moreTimeMode.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.labelHours = QSpinBox()
        self.labelHours.setFont(QFont("DejaVu Sans", 14))
        self.labelHours.setFixedSize(60, 40)
        self.labelHours.setFrame(True)
        self.labelHours.setMinimum(0)
        self.labelHours.setSingleStep(1)
        self.labelHours.setMaximum(23)
        self.labelHours.valueChanged.connect(self.label_hours_changed)
        self.labelHours.setStyleSheet(
        "QSpinBox"
           "{"
            "border: 0px solid transparent;"
            "border-radius: 5px;"
           "}")

        # Label
        self.timeLabel = QLabel()
        self.timeLabel.setFont(QFont("DejaVu Sans", 18))
        self.timeLabel.setText(":")
        self.timeLabel.setStyleSheet("""
            border-color: transparent;
        """)

        # Label hours
        self.hoursLabel = QLabel()
        self.hoursLabel.setFont(QFont("DejaVu Sans", 12))
        self.hoursLabel.setText("Hours")
        self.hoursLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.hoursLabel.setStyleSheet("""
            border-color: transparent;
            border-radius: 5px;
        """)

        # Label minutes
        self.minutesLabel = QLabel()
        self.minutesLabel.setFont(QFont("DejaVu Sans", 12))
        self.minutesLabel.setText("Minutes")
        self.minutesLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.minutesLabel.setStyleSheet("""
            border-color: transparent;
        """)

        # Spinbox Hours
        self.labelMinutes = QSpinBox()
        self.labelMinutes.setFont(QFont("DejaVu Sans", 14))
        self.labelMinutes.setFixedSize(60, 40)
        self.labelMinutes.setFrame(True)
        self.labelMinutes.setStyleSheet(
        "QSpinBox"
            "{"
                "border: 0px solid transparent;"
                "border-radius: 5px;"
            "}")

        self.labelMinutes.setMinimum(0)
        self.labelMinutes.setSingleStep(1)
        self.labelMinutes.setMaximum(59)
        self.labelMinutes.valueChanged.connect(self.label_minutes_changed)

        # Combo box
        self.everyCombox = QComboBox()
        self.everyCombox.setFrame(True)
        self.everyCombox.setFixedSize(155, 28)
        self.everyCombox.setFont(item)
        self.everyCombox.setStyleSheet(
        "QComboBox"
            "{"
                "border: 0px solid transparent;"
                "border-radius: 5px;"
            "}")

        everyComboxList = ["Every 30 minutes", "Every 1 hour", "Every 2 hours", "Every 4 hours"]  # "Every 15 minutes"
        self.everyCombox.addItems(everyComboxList)
        self.everyCombox.currentIndexChanged.connect(self.on_every_combox_changed)

        ################################################################################
        ## Reset widget
        ################################################################################
        self.resetWidget = QWidget(self)
        self.resetWidget.setGeometry(280, 280, 500, 100)

        # BaseV layout
        self.baseVResetLayout = QVBoxLayout(self.resetWidget)
        self.baseVResetLayout.setSpacing(5)
        # self.baseVDaysToRunLayout.setContentsMargins(20, 0, 20, 20)

        # Reset label
        self.labelReset = QLabel()
        self.labelReset.setFont(topicTitle)
        self.labelReset.setText("Reset:")
        self.labelReset.setAlignment(QtCore.Qt.AlignLeft)
        self.labelReset.setFixedSize(200, 30)   # If something seems broken, click on "Reset", to reset settings.

        # Reset label text
        self.labelResetText = QLabel()
        self.labelResetText.setFont(item)
        self.labelResetText.setText('If something seems broken, click on "Reset", to reset settings.')
        self.labelResetText.setFixedSize(400, 30)

        # Reset button
        fixButton = QPushButton()
        fixButton.setFont(item)
        fixButton.setText("Reset")
        fixButton.setFixedSize(80, 28)
        fixButton.clicked.connect(self.on_button_fix_clicked)

        ################################################################################
        ## Donate, Update and Save buttons
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
        donateButton = QPushButton()
        donateButton.setText("Donate")
        donateButton.setFont(item)
        donateButton.setFixedSize(80, 28)
        donateButton.clicked.connect(self.donate_clicked)

        # Update button (Git pull)
        # updateButton = QPushButton()
        # updateButton.setText("Check for updates")
        # updateButton.setFont(item)
        # updateButton.setFixedSize(140, 28)
        # updateButton.clicked.connect(self.check_for_updates)

        ################################################################################
        ## Save button
        ################################################################################
        saveButton = QPushButton()
        saveButton.setFixedSize(120, 28)
        saveButton.setFont(item)
        saveButton.setText("Save and Close")
        saveButton.clicked.connect(self.on_save_button_clicked)

        ################################################################################
        ## Add widgets and Layouts
        ################################################################################
        # BaseVLeft layout
        self.baseVLeftLayout.addWidget(self.label)
        self.baseVLeftLayout.addWidget(self.foldersFrame, 0, Qt.AlignHCenter | Qt.AlignTop)

        # BaseVDaysToRun layout
        self.baseVDaysToRunLayout.addWidget(self.labelDaysToRun, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseVDaysToRunLayout.addLayout(self.baseHDaysToRunLayout)

        # BaseVDaysToRun layout
        self.baseHDaysToRunLayout.addWidget(self.checkSun, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.checkMon, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.checkTue, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.checkWed, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.checkThu, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.checkFri, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.checkSat, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # BaseGridTimeToRun layout
        self.baseHTimeToRunLayout.addWidget(self.labelTimeToRun, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addWidget(self.oneTimeMode, 1, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addWidget(self.moreTimeMode, 2, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addWidget(self.everyCombox, 2, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addLayout(self.timesGrid, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

        # TimeGrid
        self.timesGrid.addWidget(self.labelHours, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timesGrid.addWidget(self.timeLabel, 0, 2, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGrid.addWidget(self.labelMinutes, 0, 3, Qt.AlignVCenter | Qt.AlignLeft)
        self.timesGrid.addWidget(self.hoursLabel, 1, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGrid.addWidget(self.minutesLabel, 1, 3, Qt.AlignVCenter | Qt.AlignHCenter)

        # Reset layout
        self.baseVResetLayout.addWidget(self.labelReset, 0, Qt.AlignLeft | Qt.AlignTop)
        self.baseVResetLayout.addWidget(self.labelResetText, 0, Qt.AlignLeft | Qt.AlignTop)
        self.baseVResetLayout.addWidget(fixButton, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Save layout
        # self.donateAndSaveLayout.addWidget(updateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndSaveLayout.addWidget(donateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndSaveLayout.addWidget(saveButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)

        self.setLayout(self.baseVLeftLayout)

        self.get_folders()

    def get_folders(self):
        # Get user.ini
        sun = config['SCHEDULE']['sun']
        mon = config['SCHEDULE']['mon']
        tue = config['SCHEDULE']['tue']
        wed = config['SCHEDULE']['wed']
        thu = config['SCHEDULE']['thu']
        fri = config['SCHEDULE']['fri']
        sat = config['SCHEDULE']['sat']
        getEverytime = config['SCHEDULE']['everytime']
        getIniFolders = config.options('FOLDER')

        # Schedule options
        # Hours
        hrs = int(config['SCHEDULE']['hours'])
        self.labelHours.setValue(hrs)

        # Minutes
        min = int(config['SCHEDULE']['minutes'])
        self.labelMinutes.setValue(min)

        # More folders
        verticalSpaceLabel = 10
        verticalSpaceCheckbox = verticalSpaceLabel  # Same value as vertical space
        for files in getHomeFolders:
            if not "." in files:
                # Folders text
                label_text = QLabel(files, self.foldersFrame)
                label_text.setFont(item)
                label_text.setFixedSize(150, 22)
                label_text.move(30, verticalSpaceLabel)
                verticalSpaceLabel += 25  # Position

                # Checkboxes
                self.foldersCheckbox = QCheckBox(self.foldersFrame)
                self.foldersCheckbox.setStyleSheet("""
                    border-color: transparent;
                """)

                self.foldersCheckbox.setFixedSize(150, 22)
                self.foldersCheckbox.move(5, verticalSpaceCheckbox)
                verticalSpaceCheckbox += 25
                text = label_text.text().lower()  # Lowercase
                self.foldersCheckbox.show()
                self.foldersCheckbox.clicked.connect(lambda *args, text=text: self.folders(text))

                # Activate checkboxes in user.ini
                if text in getIniFolders:
                    self.foldersCheckbox.setChecked(True)

        if sun == "true":
            self.checkSun.setChecked(True)

        if mon == "true":
            self.checkMon.setChecked(True)

        if tue == "true":
            self.checkTue.setChecked(True)

        if wed == "true":
            self.checkWed.setChecked(True)

        if thu == "true":
            self.checkThu.setChecked(True)

        if fri == "true":
            self.checkFri.setChecked(True)

        if sat == "true":
            self.checkSat.setChecked(True)

        # Everytime
        # if getEverytime == "15":
        #     self.everyCombox.setCurrentIndex(0)

        if getEverytime == "30":
            self.everyCombox.setCurrentIndex(0)

        elif getEverytime == "60":
            self.everyCombox.setCurrentIndex(1)

        elif getEverytime == "120":
            self.everyCombox.setCurrentIndex(2)

        elif getEverytime == "240":
            self.everyCombox.setCurrentIndex(3)

        # Timer
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

    def updates(self):
        # Configparser
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Read user.ini
        oneTimeMode = config['MODE']['one_time_mode']
        moreTimeMode = config['MODE']['more_time_mode']

        if oneTimeMode == "true":
            self.everyCombox.setEnabled(False)
            self.labelHours.setEnabled(True)
            self.labelMinutes.setEnabled(True)
            self.oneTimeMode.setChecked(True)

        elif moreTimeMode == "true":
            self.labelHours.setEnabled(False)
            self.labelMinutes.setEnabled(False)
            self.everyCombox.setEnabled(True)
            self.moreTimeMode.setChecked(True)

    def folders(self, get):
        print(get)
        with open(src_user_config, 'w+') as configfile:
            if config.has_option('FOLDER', get):
                config.remove_option('FOLDER', get)
            else:
                config.set('FOLDER', get, 'true')

            config.write(configfile)

    def on_every_combox_changed(self):
        chooseEveryCombox = self.everyCombox.currentIndex()
        with open(src_user_config, 'w') as configfile:
            if chooseEveryCombox == 0:
                config.set('SCHEDULE', 'everytime', '15')
                config.write(configfile)

            elif chooseEveryCombox == 1:
                config.set('SCHEDULE', 'everytime', '30')
                config.write(configfile)

            elif chooseEveryCombox == 2:
                config.set('SCHEDULE', 'everytime', '60')
                config.write(configfile)

            elif chooseEveryCombox == 3:
                config.set('SCHEDULE', 'everytime', '120')
                config.write(configfile)

            elif chooseEveryCombox == 4:
                config.set('SCHEDULE', 'everytime', '240')
                config.write(configfile)

    def on_check_sun_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.checkSun.isChecked():
                config.set('SCHEDULE', 'sun', 'true')
                config.write(configfile)
                print("Sun")
            else:
                config.set('SCHEDULE', 'sun', 'false')
                config.write(configfile)

    def on_check_mon_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.checkMon.isChecked():
                config.set('SCHEDULE', 'mon', 'true')
                config.write(configfile)
                print("Mon")
            else:
                config.set('SCHEDULE', 'mon', 'false')
                config.write(configfile)

    def on_check_tue_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.checkTue.isChecked():
                config.set('SCHEDULE', 'tue', 'true')
                config.write(configfile)
                print("Tue")
            else:
                config.set('SCHEDULE', 'tue', 'false')
                config.write(configfile)

    def on_check_wed_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.checkWed.isChecked():
                config.set('SCHEDULE', 'wed', 'true')
                config.write(configfile)
                print("Wed")
            else:
                config.set('SCHEDULE', 'wed', 'false')
                config.write(configfile)

    def on_check_thu_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.checkThu.isChecked():
                config.set('SCHEDULE', 'thu', 'true')
                config.write(configfile)
                print("Thu")
            else:
                config.set('SCHEDULE', 'thu', 'false')
                config.write(configfile)

    def on_check_fri_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.checkFri.isChecked():
                config.set('SCHEDULE', 'fri', 'true')
                config.write(configfile)
                print("Fri")
            else:
                config.set('SCHEDULE', 'fri', 'false')
                config.write(configfile)

    def on_check_sat_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.checkSat.isChecked():
                config.set('SCHEDULE', 'sat', 'true')
                config.write(configfile)
                print("Sat")
            else:
                config.set('SCHEDULE', 'sat', 'false')
                config.write(configfile)

    def label_hours_changed(self):
        hours = self.labelHours.value()
        hours = str(hours)

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'hours', hours)
            if hours in minFix:
                config.set('SCHEDULE', 'hours', '0' + hours)

            config.write(configfile)

    def label_minutes_changed(self):
        minutes = self.labelMinutes.value()
        minutes = str(minutes)

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'minutes', minutes)
            if minutes in minFix:
                config.set('SCHEDULE', 'minutes', '0' + minutes)

            config.write(configfile)

    def on_frequency_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.oneTimeMode.isChecked():
                config.set('MODE', 'one_time_mode', 'true')
                print("One time mode selected")

                # DISABLE MORE TIME MODE
                config.set('MODE', 'more_time_mode', 'false')
                config.write(configfile)

            elif self.moreTimeMode.isChecked():
                config.set('MODE', 'more_time_mode', 'true')
                print("Multiple time mode selected")

                # DISABLE ONE TIME MODE
                config.set('MODE', 'one_time_mode', 'false')
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
                config.set('INFO', 'notification_id', '0')

                # Folders section
                config.set('FOLDER', 'documents', 'true')
                config.set('FOLDER', 'music', 'true')
                config.set('FOLDER', 'videos', 'true')
                config.set('FOLDER', 'pictures', 'true')

                config.write(configfile)
            
            print("All settings was reset!")
            sub.Popen(f"python3 {src_notification}", shell=True)  # Call notification

            exit()

        else:
            QMessageBox.Close

    def check_for_updates(self):
        ################################################################################
        ## MessabeBox
        ################################################################################
        updateConfirmation = QMessageBox.question(self, 'Update Software',
        f'You are about to grab the latest version of {appName} from GitHub.'
        '\nDo you want to continue?',
        QMessageBox.Yes | QMessageBox.No)

        if updateConfirmation == QMessageBox.Yes:
            output = sub.call(f"cd {homeUser}/.local/share/{appNameClose}/ && git stash && git reset --hard && git pull --no-edit && git stash drop", shell=True)
            print(output)

            ################################################################################
            ## MessabeBox information
            ################################################################################
            QMessageBox.information(self, "Update Software", f"Now, you are using the latest version of {appName}.\nYou can check the version under Options.")

        else:
            QMessageBox.Close

    def donate_clicked(self):
        sub.Popen("xdg-open https://www.paypal.com/paypalme/geovanejeff", shell=True)

    def on_save_button_clicked(self):
        ################################################################################
        ## Read INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.getAutoBackup = config['BACKUP']['auto_backup']
        self.getCheckerRunning = config['BACKUP']['checker_running']

        if self.getAutoBackup == "true" and self.getCheckerRunning == "true":
            exit()

        else:
            ################################################################################
            ## Call backup check py
            ################################################################################
            sub.Popen(f"python3 {src_backup_check_py}", shell=True)

            ################################################################################
            ## After call backup checker, set checker_running to true
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
