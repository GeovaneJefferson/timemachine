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
        self.setFixedHeight(550)
        self.setFixedWidth(800)
        self.widgets()

    def widgets(self):
        ################################################################################
        ## Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 240, 500)
        # self.leftWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)
        # Left widget
        self.baseVLeftLayout = QVBoxLayout(self.leftWidget)
        self.baseVLeftLayout.setSpacing(10)
        self.baseVLeftLayout.setContentsMargins(20, 0, 20, 20)

        # Label
        self.label = QLabel()
        self.label.setFont(QFont("Arial Black", 10))
        self.label.setText("These folders will be back up:")
        self.label.setFixedSize(200, 30)

        # Frame
        self.folders_frame = QFrame()
        self.folders_frame.setFixedSize(200, 440)
        # self.folders_frame.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        ################################################################################
        ## Days to run widget
        ################################################################################
        self.daysToRunWidget = QWidget(self)
        self.daysToRunWidget.setGeometry(280, 20, 500, 80)
        # self.daysToRunWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

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
        self.labelDaysToRun.setFont(QFont("Arial Black", 10))
        self.labelDaysToRun.setText("Days to run:")
        self.labelDaysToRun.setFixedSize(200, 30)

        # Checkboxes
        self.check_sun = QCheckBox()
        self.check_sun.setFont(QFont("Ubuntu", 10))
        self.check_sun.setText("Sun")

        self.check_mon = QCheckBox()
        self.check_mon.setFont(QFont("Ubuntu", 10))
        self.check_mon.setText("Mon")

        self.check_tue = QCheckBox()
        self.check_tue.setFont(QFont("Ubuntu", 10))
        self.check_tue.setText("Tue")

        self.check_wed = QCheckBox()
        self.check_wed.setFont(QFont("Ubuntu", 10))
        self.check_wed.setText("Wed")

        self.check_thu = QCheckBox()
        self.check_thu.setFont(QFont("Ubuntu", 10))
        self.check_thu.setText("Thu")

        self.check_fri = QCheckBox()
        self.check_fri.setFont(QFont("Ubuntu", 10))
        self.check_fri.setText("Fri")

        self.check_sat = QCheckBox()
        self.check_sat.setFont(QFont("Ubuntu", 10))
        self.check_sat.setText("Sat")

        ################################################################################
        ## Time to run widget
        ################################################################################
        self.timeToRunWidget = QWidget(self)
        self.timeToRunWidget.setGeometry(280, 100, 500, 200)
        # self.timeToRunWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Label
        self.labelTimeToRun = QLabel()
        self.labelTimeToRun.setFont(QFont("Arial Black", 10))
        self.labelTimeToRun.setText("Time to run:")
        self.labelTimeToRun.setFixedSize(180, 30)

        # BaseGrid layout
        self.baseHTimeToRunLayout = QGridLayout(self.timeToRunWidget)

        self.timesGrid = QGridLayout()

        # Radio buttons
        self.one_time_mode = QRadioButton()
        self.one_time_mode.setFont(QFont("Ubuntu", 10))
        self.one_time_mode.setText("One time per day")
        self.one_time_mode.setToolTip("One single back up will be excute every selected day(s) and time.")
        self.one_time_mode.setFixedSize(180, 30)
        self.one_time_mode.clicked.connect(self.on_frequency_clicked)

        self.more_time_mode = QRadioButton()
        self.more_time_mode.setFont(QFont("Ubuntu", 10))
        self.more_time_mode.setToolTip(
            "Back up will be execute every x minutes/hours.\n"
            "This will produce a time folder inside the chose external location.\n"
            "Fx: 12-12-12/10-15\n"
            "10-15, is the time of the back up (10:15)."
        )
        self.more_time_mode.setText("Multiple times per day")
        self.more_time_mode.setFixedSize(180, 30)
        self.more_time_mode.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.label_hours = QSpinBox()
        self.label_hours.setFont(QFont("Ubuntu", 14))
        self.label_hours.setFixedSize(60, 40)
        self.label_hours.setFrame(True)
        self.label_hours.setMinimum(0)
        self.label_hours.setSingleStep(1)
        self.label_hours.setMaximum(23)
        self.label_hours.valueChanged.connect(self.label_hours_changed)

        # Label
        self.timeLabel = QLabel()
        self.timeLabel.setFont(QFont("Ubuntu", 18))
        self.timeLabel.setText(":")

        # Label hours
        self.hoursLabel = QLabel()
        self.hoursLabel.setFont(QFont("Ubuntu", 12))
        self.hoursLabel.setText("Hours")

        # Label minutes
        self.minutesLabel = QLabel()
        self.minutesLabel.setFont(QFont("Ubuntu", 12))
        self.minutesLabel.setText("Minutes")

        # Spinbox Hours
        self.label_minutes = QSpinBox()
        self.label_minutes.setFont(QFont("Ubuntu", 14))
        self.label_minutes.setFixedSize(60, 40)
        self.label_minutes.setFrame(True)
        self.label_minutes.setMinimum(0)
        self.label_minutes.setSingleStep(1)
        self.label_minutes.setMaximum(59)
        self.label_minutes.valueChanged.connect(self.label_minutes_changed)

        # Combo box
        self.every_combox = QComboBox()
        self.every_combox.setFrame(True)
        self.every_combox.setFixedSize(140, 34)
        self.every_combox.setFont(QFont("Ubuntu", 10))
        every_combox_list = ["Every 15 minutes", "Every 30 minutes", "Every 1 hour", "Every 2 hours", "Every 4 hour"]
        self.every_combox.addItems(every_combox_list)
        self.every_combox.currentIndexChanged.connect(self.on_every_combox_changed)

        ################################################################################
        ## Reset widget
        ################################################################################
        self.resetWidget = QWidget(self)
        self.resetWidget.setGeometry(280, 300, 500, 160)
        # self.resetWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # BaseV layout
        self.baseVResetLayout = QVBoxLayout(self.resetWidget)
        self.baseVResetLayout.setSpacing(5)
        # self.baseVDaysToRunLayout.setContentsMargins(20, 0, 20, 20)

        # Reset label
        self.labelReset = QLabel()
        self.labelReset.setFont(QFont("Arial Black", 10))
        self.labelReset.setText("Reset:")
        self.labelReset.setFixedSize(200, 30)   # If something seems broken, click on "Reset", to reset settings.

        # Reset label text
        self.labelResetText = QLabel()
        self.labelResetText.setFont(QFont("Ubuntu", 10))
        self.labelResetText.setText('If something seems broken, click on "Reset", to reset settings.')
        self.labelResetText.setFixedSize(400, 30)

        # Reset button
        self.btn_fix = QPushButton()
        self.btn_fix.setFont(QFont("Ubuntu", 10))
        self.btn_fix.setText("Reset")
        self.btn_fix.setFixedSize(80, 34)
        self.btn_fix.clicked.connect(self.on_button_fix_clicked)

        ################################################################################
        ## Save button
        ################################################################################
        self.saveWidget = QWidget(self)
        self.saveWidget.setGeometry(620, 480, 180, 60)
        # self.saveWidget.setStyleSheet("""
        #      border: 1px solid red;
        #  """)

        # Save layout
        self.saveLayout = QVBoxLayout(self.saveWidget)

        # Save button
        self.btn_save = QPushButton()
        self.btn_save.setFixedSize(120, 34)
        self.btn_save.setFont(QFont("Ubuntu", 10))
        self.btn_save.setText("Save and Close")
        self.btn_save.clicked.connect(self.on_buttons_save_clicked)

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
        self.baseHTimeToRunLayout.addWidget(self.one_time_mode, 1, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseHTimeToRunLayout.addWidget(self.more_time_mode, 2, 0, Qt.AlignVCenter | Qt.AlignLeft)
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
        self.baseVResetLayout.addStretch()
        self.baseVResetLayout.addWidget(self.btn_fix, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.baseVResetLayout.addStretch()

        # Save layout
        self.saveLayout.addWidget(self.btn_save, 0, Qt.AlignVCenter | Qt.AlignHCenter)

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
        get_ini_folders = config.options('FOLDER')

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
            if not files.startswith("."):
                print(files)

                # Folders text
                label_text = QLabel(files, self.folders_frame)
                label_text.setFont(QFont("Ubuntu", 10))
                label_text.setFixedSize(150, 22)
                label_text.move(30, vert_space_label)
                vert_space_label += 25  # Position

                # Checkboxes
                self.folders_checkbox = QCheckBox(self.folders_frame)
                self.folders_checkbox.setFixedSize(150, 22)
                self.folders_checkbox.move(5, vert_space_checkbox)
                vert_space_checkbox += 25
                text = label_text.text().lower()  # Lowercase
                self.folders_checkbox.show()
                self.folders_checkbox.clicked.connect(lambda *args, text=text: self.folders(text))

                # Activate checkboxes in user.ini
                if text in get_ini_folders:
                    self.folders_checkbox.setChecked(True)

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
            self.one_time_mode.setChecked(True)

        elif more_time_mode == "true":
            self.label_hours.setEnabled(False)
            self.label_minutes.setEnabled(False)
            self.every_combox.setEnabled(True)
            self.more_time_mode.setChecked(True)

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
    #
    def on_frequency_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.one_time_mode.isChecked():
                config.set('MODE', 'one_time_mode', 'true')
                print("One time mode selected")

                # DISABLE MORE TIME MODE
                config.set('MODE', 'more_time_mode', 'false')
                config.write(configfile)

            elif self.more_time_mode.isChecked():
                config.set('MODE', 'more_time_mode', 'true')
                print("Multiple time mode selected")

                # DISABLE ONE TIME MODE
                config.set('MODE', 'one_time_mode', 'false')
                config.write(configfile)

    def on_button_fix_clicked(self, event):
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

                    # External section
                    config.set('EXTERNAL', 'hd', 'None')
                    config.set('EXTERNAL', 'name', 'None')

                    # Mode section
                    config.set('MODE', 'one_time_mode', 'true')
                    config.set('MODE', 'more_time_mode', 'false')

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

    def on_buttons_save_clicked(self):
        sub.Popen("python3 " + src_backup_py, shell=True)  # Call backup py
        exit()


app = QApplication(sys.argv)
tic = time.time()
main = UI()
main.show()
toc = time.time()

print(f'Options {(toc-tic):.4f} seconds')
sys.exit(app.exec())
