from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        loadUi(src_ui_options, self)
        self.setWindowTitle("Options Screen")
        appIcon = QIcon(src_restore_icon)
        self.setWindowIcon(appIcon)
        self.setFixedHeight(550)
        self.setFixedWidth(800)

        # Connections
        self.label_hours.valueChanged.connect(self.label_hours_changed)
        self.label_minutes.valueChanged.connect(self.label_minutes_changed)
        self.one_time_mode.clicked.connect(self.on_frequency_clicked)
        self.more_time_mode.clicked.connect(self.on_frequency_clicked)
        self.every_combox.currentIndexChanged.connect(self.on_every_combox_changed)
        self.btn_save.clicked.connect(self.on_buttons_save_clicked)
        self.btn_fix.clicked.connect(self.on_button_fix_clicked)

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
                # # Get folder size
                # size = sub.check_output(['du','-sh', home_user + "/" + files]).split()[0].decode('utf-8')
                # if size == "0":
                #     size = ""
                #     print(size)
                
                print(files)
                # Folders text
                label_text = QLabel(files, self.folders_frame)
                label_text.setFixedSize(200, 22)
                label_text.move(40, vert_space_label)
                vert_space_label += 25  # Position

                # Checkboxes
                self.folders_checkbox = QCheckBox(self.folders_frame)
                self.folders_checkbox.setFixedSize(200, 22)
                self.folders_checkbox.move(15, vert_space_checkbox)
                vert_space_checkbox += 25
                text = label_text.text().lower()  # Lowercase
                self.folders_checkbox.show()
                self.folders_checkbox.clicked.connect(lambda ch, text=text: self.folders(text))

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
