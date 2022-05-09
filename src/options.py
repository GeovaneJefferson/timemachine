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
        self.folders_frame = QFrame()
        self.folders_frame.setFixedSize(250, 500)
        # self.folders_frame.setStyleSheet(
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
        self.check_sun = QCheckBox()
        self.check_sun.setFont(item)
        self.check_sun.setText("Sun")
        self.check_sun.clicked.connect(self.on_check_sun_clicked)
        self.check_sun.setStyleSheet("""
            border-color: transparent;
        """)

        self.check_mon = QCheckBox()
        self.check_mon.setFont(item)
        self.check_mon.setText("Mon")
        self.check_mon.clicked.connect(self.on_check_mon_clicked)
        self.check_mon.setStyleSheet("""
            border-color: transparent;
        """)

        self.check_tue = QCheckBox()
        self.check_tue.setFont(item)
        self.check_tue.setText("Tue")
        self.check_tue.clicked.connect(self.on_check_tue_clicked)
        self.check_tue.setStyleSheet("""
            border-color: transparent;
        """)

        self.check_wed = QCheckBox()
        self.check_wed.setFont(item)
        self.check_wed.setText("Wed")
        self.check_wed.clicked.connect(self.on_check_wed_clicked)
        self.check_wed.setStyleSheet("""
            border-color: transparent;
        """)

        self.check_thu = QCheckBox()
        self.check_thu.setFont(item)
        self.check_thu.setText("Thu")
        self.check_thu.clicked.connect(self.on_check_thu_clicked)
        self.check_thu.setStyleSheet("""
            border-color: transparent;
        """)

        self.check_fri = QCheckBox()
        self.check_fri.setFont(item)
        self.check_fri.setText("Fri")
        self.check_fri.clicked.connect(self.on_check_fri_clicked)
        self.check_fri.setStyleSheet("""
            border-color: transparent;
        """)

        self.check_sat = QCheckBox()
        self.check_sat.setFont(item)
        self.check_sat.setText("Sat")
        self.check_sat.clicked.connect(self.on_check_sat_clicked)
        self.check_sat.setStyleSheet("""
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
            "This will produce a time folder inside the chose external location.\n"
            "Fx: 12-12-12/10-15\n"
            "10-15, is the time of the back up (10:15).")

        self.moreTimeMode.setText("Multiple times per day")
        self.moreTimeMode.setFixedSize(180, 30)
        self.moreTimeMode.setStyleSheet("""
            border-color: transparent;
        """)
        self.moreTimeMode.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.label_hours = QSpinBox()
        self.label_hours.setFont(QFont("DejaVu Sans", 14))
        self.label_hours.setFixedSize(60, 40)
        self.label_hours.setFrame(True)
        self.label_hours.setMinimum(0)
        self.label_hours.setSingleStep(1)
        self.label_hours.setMaximum(23)
        self.label_hours.valueChanged.connect(self.label_hours_changed)
        self.label_hours.setStyleSheet(
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
        self.label_minutes = QSpinBox()
        self.label_minutes.setFont(QFont("DejaVu Sans", 14))
        self.label_minutes.setFixedSize(60, 40)
        self.label_minutes.setFrame(True)
        self.label_minutes.setStyleSheet(
        "QSpinBox"
            "{"
                "border: 0px solid transparent;"
                "border-radius: 5px;"
            "}")

        self.label_minutes.setMinimum(0)
        self.label_minutes.setSingleStep(1)
        self.label_minutes.setMaximum(59)
        self.label_minutes.valueChanged.connect(self.label_minutes_changed)

        # Combo box
        self.every_combox = QComboBox()
        self.every_combox.setFrame(True)
        self.every_combox.setFixedSize(155, 28)
        self.every_combox.setFont(item)
        self.every_combox.setStyleSheet(
        "QComboBox"
            "{"
                "border: 0px solid transparent;"
                "border-radius: 5px;"
            "}")

        every_combox_list = ["Every 15 minutes", "Every 30 minutes", "Every 1 hour", "Every 2 hours", "Every 4 hours"]
        self.every_combox.addItems(every_combox_list)
        self.every_combox.currentIndexChanged.connect(self.on_every_combox_changed)

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
        self.donateAndSaveWidget.setGeometry(390, 485, 400, 60)
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
        updateButton = QPushButton()
        updateButton.setText("Check for updates")
        updateButton.setFont(item)
        updateButton.setFixedSize(140, 28)
        updateButton.clicked.connect(self.check_for_updates)

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
        self.baseVLeftLayout.addWidget(self.folders_frame, 0, Qt.AlignHCenter | Qt.AlignTop)

        # BaseVDaysToRun layout
        self.baseVDaysToRunLayout.addWidget(self.labelDaysToRun, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseVDaysToRunLayout.addLayout(self.baseHDaysToRunLayout)

        # BaseVDaysToRun layout
        self.baseHDaysToRunLayout.addWidget(self.check_sun, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.check_mon, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.check_tue, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.check_wed, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.check_thu, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.check_fri, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHDaysToRunLayout.addWidget(self.check_sat, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # BaseGridTimeToRun layout
        self.baseHTimeToRunLayout.addWidget(self.labelTimeToRun, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addWidget(self.oneTimeMode, 1, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addWidget(self.moreTimeMode, 2, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addWidget(self.every_combox, 2, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addLayout(self.timesGrid, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

        # TimeGrid
        self.timesGrid.addWidget(self.label_hours, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timesGrid.addWidget(self.timeLabel, 0, 2, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGrid.addWidget(self.label_minutes, 0, 3, Qt.AlignVCenter | Qt.AlignLeft)
        self.timesGrid.addWidget(self.hoursLabel, 1, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGrid.addWidget(self.minutesLabel, 1, 3, Qt.AlignVCenter | Qt.AlignHCenter)

        # Reset layout
        self.baseVResetLayout.addWidget(self.labelReset, 0, Qt.AlignLeft | Qt.AlignTop)
        self.baseVResetLayout.addWidget(self.labelResetText, 0, Qt.AlignLeft | Qt.AlignTop)
        self.baseVResetLayout.addWidget(fixButton, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Save layout
        self.donateAndSaveLayout.addWidget(updateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndSaveLayout.addWidget(donateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndSaveLayout.addWidget(saveButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)

        self.setLayout(self.baseVLeftLayout)

        self.get_folders()

    def get_folders(self):
    #     # Backup images
    #     self.backupImage = QLabel()
    #     self.backupImage.setFixedSize(128, 128)
    #     self.backupImage.setStyleSheet(
    #         "QLabel"
    #         "{"
    #             f"background-image: url({src_backup_icon});"
    #         "}"
    #     )

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
        self.label_hours.setValue(hrs)

        # Minutes
        min = int(config['SCHEDULE']['minutes'])
        self.label_minutes.setValue(min)

        # More folders
        vert_space_label = 10
        vert_space_checkbox = vert_space_label  # Same value as vertical space
        for files in get_home_folders:
            if not "." in files:
                # Folders text
                label_text = QLabel(files, self.folders_frame)
                label_text.setFont(item)
                label_text.setFixedSize(150, 22)
                label_text.move(30, vert_space_label)
                vert_space_label += 25  # Position

                # Checkboxes
                self.foldersCheckbox = QCheckBox(self.folders_frame)
                self.foldersCheckbox.setStyleSheet("""
                    border-color: transparent;
                """)

                self.foldersCheckbox.setFixedSize(150, 22)
                self.foldersCheckbox.move(5, vert_space_checkbox)
                vert_space_checkbox += 25
                text = label_text.text().lower()  # Lowercase
                self.foldersCheckbox.show()
                self.foldersCheckbox.clicked.connect(lambda *args, text=text: self.folders(text))

                # Activate checkboxes in user.ini
                if text in getIniFolders:
                    self.foldersCheckbox.setChecked(True)

        if sun == "true":
            self.check_sun.setChecked(True)

        if mon == "true":
            self.check_mon.setChecked(True)

        if tue == "true":
            self.check_tue.setChecked(True)

        if wed == "true":
            self.check_wed.setChecked(True)

        if thu == "true":
            self.check_thu.setChecked(True)

        if fri == "true":
            self.check_fri.setChecked(True)

        if sat == "true":
            self.check_sat.setChecked(True)

        # Everytime
        if getEverytime == "15":
            self.every_combox.setCurrentIndex(0)

        elif getEverytime == "30":
            self.every_combox.setCurrentIndex(1)

        elif getEverytime == "60":
            self.every_combox.setCurrentIndex(2)

        elif getEverytime == "120":
            self.every_combox.setCurrentIndex(3)

        elif getEverytime == "240":
            self.every_combox.setCurrentIndex(4)

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
        more_time_mode = config['MODE']['more_time_mode']

        if oneTimeMode == "true":
            self.every_combox.setEnabled(False)
            self.label_hours.setEnabled(True)
            self.label_minutes.setEnabled(True)
            self.oneTimeMode.setChecked(True)

        elif more_time_mode == "true":
            self.label_hours.setEnabled(False)
            self.label_minutes.setEnabled(False)
            self.every_combox.setEnabled(True)
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
        choose_every_combox = self.every_combox.currentIndex()
        with open(src_user_config, 'w') as configfile:
            if choose_every_combox == 0:
                config.set('SCHEDULE', 'everytime', '15')
                config.write(configfile)

            elif choose_every_combox == 1:
                config.set('SCHEDULE', 'everytime', '30')
                config.write(configfile)

            elif choose_every_combox == 2:
                config.set('SCHEDULE', 'everytime', '60')
                config.write(configfile)

            elif choose_every_combox == 3:
                config.set('SCHEDULE', 'everytime', '120')
                config.write(configfile)

            elif choose_every_combox == 4:
                config.set('SCHEDULE', 'everytime', '240')
                config.write(configfile)

    def on_check_sun_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_sun.isChecked():
                config.set('SCHEDULE', 'sun', 'true')
                config.write(configfile)
                print("Sun")
            else:
                config.set('SCHEDULE', 'sun', 'false')
                config.write(configfile)

    def on_check_mon_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_mon.isChecked():
                config.set('SCHEDULE', 'mon', 'true')
                config.write(configfile)
                print("Mon")
            else:
                config.set('SCHEDULE', 'mon', 'false')
                config.write(configfile)

    def on_check_tue_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_tue.isChecked():
                config.set('SCHEDULE', 'tue', 'true')
                config.write(configfile)
                print("Tue")
            else:
                config.set('SCHEDULE', 'tue', 'false')
                config.write(configfile)

    def on_check_wed_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_wed.isChecked():
                config.set('SCHEDULE', 'wed', 'true')
                config.write(configfile)
                print("Wed")
            else:
                config.set('SCHEDULE', 'wed', 'false')
                config.write(configfile)

    def on_check_thu_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_thu.isChecked():
                config.set('SCHEDULE', 'thu', 'true')
                config.write(configfile)
                print("Thu")
            else:
                config.set('SCHEDULE', 'thu', 'false')
                config.write(configfile)

    def on_check_fri_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_fri.isChecked():
                config.set('SCHEDULE', 'fri', 'true')
                config.write(configfile)
                print("Fri")
            else:
                config.set('SCHEDULE', 'fri', 'false')
                config.write(configfile)

    def on_check_sat_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_sat.isChecked():
                config.set('SCHEDULE', 'sat', 'true')
                config.write(configfile)
                print("Sat")
            else:
                config.set('SCHEDULE', 'sat', 'false')
                config.write(configfile)

    def label_hours_changed(self):
        hours = self.label_hours.value()
        hours = str(hours)

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'hours', hours)
            if hours in min_fix:
                config.set('SCHEDULE', 'hours', '0' + hours)

            config.write(configfile)

    def label_minutes_changed(self):
        minutes = self.label_minutes.value()
        minutes = str(minutes)

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'minutes', minutes)
            if minutes in min_fix:
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

                # Folders section
                config.set('FOLDER', 'documents', 'true')
                config.set('FOLDER', 'music', 'true')
                config.set('FOLDER', 'videos', 'true')
                config.set('FOLDER', 'pictures', 'true')

                config.write(configfile)
                exit()
        else:
            QMessageBox.Close

    def check_for_updates(self):
        ################################################################################
        ## MessabeBox
        ################################################################################
        updateConfirmation = QMessageBox.question(self, 'Update Software',
        f'You are about to grab the latest version of {app_name} from GitHub.'
        '\nDo you want to continue?',
        QMessageBox.Yes | QMessageBox.No)

        if updateConfirmation == QMessageBox.Yes:
            output = sub.call(f"cd {home_user}/.local/share/{app_name}/ && git stash && git pull --no-edit && git stash drop", shell=True)
            print(output)

            ################################################################################
            ## MessabeBox information
            ################################################################################
            QMessageBox.information(self, "Update Software", f"Now, you are using the latest version of {app_name}.\nYou can check the version under Options.")

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
