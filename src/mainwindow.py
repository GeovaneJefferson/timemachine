from setup import *
from stylesheet import *
from check_connection import is_connected
from device_location import device_location
from get_home_folders import get_home_folders
from get_flatpaks_folders_size import (
    get_external_device_used_size, get_external_device_max_size,
    get_all_used_backup_device_space, get_all_max_backup_device_space)
from read_ini_file import UPDATEINIFILE
from get_oldest_backup_date import oldest_backup_date
from get_latest_backup_date import latest_backup_date_label
from update import backup_ini_file
from calculate_time_left_to_backup import calculate_time_left_to_backup
from determine_next_backup import get_next_backup
from save_info import save_info
from create_backup_checker_desktop import create_backup_checker_desktop
from notification_massage import notification_message
from detect_theme_color import detect_theme_color


CHOOSE_DEVICE = []
CAPTURE_DEVICE = []


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ini_ui()

    def ini_ui(self):
        ################################################################################
        # Center window
        ################################################################################
        centerPoint=QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg=self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if detect_theme_color(APP):
            # Left background
            self.leftBackgroundColorDetector=leftBackgroundColorStylesheetDark
            # Button
            self.buttonStylesheetDetector=buttonStylesheetDark
            # External window
            self.externalWindowbackgroundDetector=externalWindowbackgroundStylesheetDark
            # Available devices
            self.availableDeviceButtonDetector=availableDeviceButtonStylesheetDark
            # Separator
            self.separatorstylesheetDetector=separetorLineDark
            # Separator left background
            self.separatorLeftBackgroundStylesheetDetector=separetorLineLeftbackgroundDark

        else:
            # Left background
            self.leftBackgroundColorDetector=leftBackgroundColorStylesheet
            # Button
            self.buttonStylesheetDetector=buttonStylesheet
            # External window
            self.externalWindowbackgroundDetector=externalWindowbackgroundStylesheet
            # Available devices
            self.availableDeviceButtonDetector=availableDeviceButtonStylesheet
            # Separator
            self.separatorstylesheetDetector=separetorLine
            # Separator left background
            self.separatorLeftBackgroundStylesheetDetector=separetorLineLeftbackground

        leftBackgroundColor=QWidget(self)
        leftBackgroundColor.setGeometry(0,0,220,self.height())
        leftBackgroundColor.setStyleSheet(self.leftBackgroundColorDetector)

        self.widgets()

    def widgets(self):
        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget=QWidget(self)
        self.leftWidget.setGeometry(20, 20, 200, 410)
        self.leftWidget.setStyleSheet(self.separatorLeftBackgroundStylesheetDetector)

        # Left layout
        self.leftLayout=QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(20)
        self.leftLayout.setContentsMargins(0, 0, 10, 0)

        # Backup images
        self.backup_image_label = QLabel()
        self.backup_image_label.setFixedSize(128, 128)
        self.backup_image_label.setStyleSheet(
            "QLabel"
            "{"
                f"background-image: url({SRC_BACKUP_ICON});"
                "border-color: transparent;"
                "background-repeat: no-repeat;"
            "}")

        # App name
        self.APPNAME=QLabel()
        self.APPNAME.setFont(QFont(MAIN_FONT,SMALL_FONT_SIZE))
        self.APPNAME.setText(f"<h1>{APP_NAME}</h1>")
        self.APPNAME.adjustSize()

        # Automatically checkbox
        self.automatically_check_box=QCheckBox()
        self.automatically_check_box.setFont(QFont(MAIN_FONT, NORMAL_FONT_SIZE))
        self.automatically_check_box.setText("Back Up Automatically")
        self.automatically_check_box.adjustSize()
        self.automatically_check_box.setStyleSheet("""
            border-color: transparent;
        """)
        self.automatically_check_box.clicked.connect(self.automatically_clicked)

        ################################################################################
        # Right Widget
        ################################################################################
        self.rightWidget=QWidget(self)
        self.rightWidget.setGeometry(240, 40, 120, 154)

        # Right layout
        self.rightLayout=QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(20)

        # Restore images
        self.restore_image_label = QLabel()
        self.restore_image_label.setFixedSize(74, 74)
        self.restore_image_label.setStyleSheet(
            "QLabel"
            "{"
                f"background-image: url({SRC_RESTORE_ICON});"
                "background-repeat: no-repeat;"
                "background-position: top;"
            "}")

        # Select disk button
        self.select_disk_button = QPushButton(self)
        self.select_disk_button.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.select_disk_button.setText("   Select Disk...   ")
        self.select_disk_button.adjustSize()
        self.select_disk_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.select_disk_button.setStyleSheet(self.buttonStylesheetDetector)
        self.select_disk_button.clicked.connect(self.external_open_animation)

        ################################################################################
        # Far right Widget
        ################################################################################
        self.farRightWidget=QWidget(self)
        self.farRightWidget.setContentsMargins(0, 0, 0, 0)
        self.farRightWidget.setGeometry(360, 40, 280, 154)

        # Right WIDGET
        self.farRightLayout=QVBoxLayout(self.farRightWidget)
        self.farRightLayout.setSpacing(0)
        # self.farRightWidget.setStyleSheet("""
        #     border: 1px solid red;
        #     """)

        ################################################################################
        # Set external name
        ################################################################################
        self.external_name_label=QLabel()
        self.external_name_label.setFont(QFont(MAIN_FONT, 6))
        self.external_name_label.setAlignment(Qt.AlignLeft)

        ################################################################################
        # Get external size
        ################################################################################
        self.external_size_label=QLabel()
        self.external_size_label.setFont(ITEM)
        self.external_size_label.setFixedSize(200, 18)
        self.external_size_label.setStyleSheet("""
            color: gray;
            """)

        ################################################################################
        # Label UI backup
        ################################################################################
        self.oldest_backup_label=QLabel()
        self.oldest_backup_label.setFont(ITEM)
        self.oldest_backup_label.setText("Oldest Backup: None")
        self.oldest_backup_label.setFixedSize(200, 18)
        self.oldest_backup_label.setStyleSheet("""
            color: gray;
            """)

        self.latest_backup_label=QLabel()
        self.latest_backup_label.setFont(ITEM)
        self.latest_backup_label.setText("Lastest Backup: None")
        self.latest_backup_label.setFixedSize(200, 18)
        self.latest_backup_label.setStyleSheet("""
            color: gray;
            """)

        # Label last backup
        self.next_backup_label=QLabel()
        self.next_backup_label.setFont(ITEM)
        self.next_backup_label.setText("Next Backup: None")
        self.next_backup_label.setFixedSize(250, 18)
        self.next_backup_label.setStyleSheet("""
            color: gray;
            """)

        # Status Status
        self.external_status_label=QLabel()
        self.external_status_label.setFont(ITEM)
        self.external_status_label.setText("Status: None")
        self.external_status_label.setFixedSize(200, 18)
        self.external_status_label.setStyleSheet("""
            color: gray;
            """)

        ################################################################################
        # Backup now button
        ################################################################################
        self.backup_now_button=QPushButton(self)
        self.backup_now_button.setText("   Back Up Now   ")
        self.backup_now_button.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.backup_now_button.adjustSize()
        self.backup_now_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.backup_now_button.setStyleSheet(self.buttonStylesheetDetector)
        self.backup_now_button.clicked.connect(self.backup_now_clicked)
        self.backup_now_button.setEnabled(False)

        ################################################################################
        # Top line WIDGET
        ################################################################################
        topLineWidget=QWidget(self)
        topLineWidget.setGeometry(240,30,440,1)
        topLineWidget.setStyleSheet(self.separatorstylesheetDetector)
        ################################################################################
        # Description
        ################################################################################
        self.descriptionWidget=QWidget(self)
        self.descriptionWidget.setGeometry(240, 200, 440, 160)
        self.descriptionWidget.setStyleSheet(self.separatorstylesheetDetector)

        # Description Layout
        self.descriptionLayout=QVBoxLayout(self.descriptionWidget)

        # Description Title
        self.descriptionTitle=QLabel()
        self.descriptionTitle.setFont(TOP_TITLE)
        self.descriptionTitle.setText(f"How {APP_NAME} works:")
        self.descriptionTitle.adjustSize()
        self.descriptionTitle.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        # self.descriptionTitle.setFixedSize(420, 24)
        self.descriptionTitle.setStyleSheet("""
            border-color: transparent;
            color: gray;
        """)

        # Description Text
        self.descriptionText=QLabel()
        self.descriptionText.setFont(ITEM)
        self.descriptionText.setText(
            "• Choose which folders to back up from HOME.\n"
            "• Hourly, Daily or Weekly backups, depending on your preference.\n"
            "• Packages such as .DEB, and .RPM that are stored\n"
            "  in the Downloads folder, are backed up.\n"
            "• Installed flatpaks and their data are also backed up.\n"
            "The oldest backups are deleted when your disk becomes full.\n\n")
        self.descriptionText.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.descriptionText.adjustSize()
        self.descriptionText.setStyleSheet("""
            border-color: transparent;
            color: gray;
        """)

        ################################################################################
        # Donate and Settings buttons
        ################################################################################
        self.optionsWidget=QWidget(self)
        self.optionsWidget.setGeometry(340, 380, 350, 80)

        # Options Layout
        self.optionsLayout=QHBoxLayout(self.optionsWidget)
        self.optionsLayout.setSpacing(10)

        # Options button
        self.optionsButton=QPushButton()
        self.optionsButton.setText("   Options...   ")
        self.optionsButton.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.optionsButton.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.optionsButton.adjustSize()
        self.optionsButton.setStyleSheet(self.buttonStylesheetDetector)
        self.optionsButton.clicked.connect(self.on_options_clicked)

        # Help button
        self.helpButton=QPushButton()
        self.helpButton.setText("?")
        self.helpButton.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.helpButton.setFixedSize(24,24)
        self.helpButton.setToolTip("Help")
        self.helpButton.setStyleSheet(self.buttonStylesheetDetector)
        self.helpButton.clicked.connect(
            lambda: sub.Popen([f"xdg-open", {GITHUB_HOME}]))
        

        # Show system tray
        self.showInSystemTrayCheckBox=QCheckBox(self)
        self.showInSystemTrayCheckBox.setFont(ITEM)
        self.showInSystemTrayCheckBox.setText(f"Show {APP_NAME} in menu bar")
        self.showInSystemTrayCheckBox.setFixedSize(280, 20)
        self.showInSystemTrayCheckBox.move(240, 410)
        self.showInSystemTrayCheckBox.setStyleSheet("""
            border-color: transparent;
        """)
        self.showInSystemTrayCheckBox.clicked.connect(self.system_tray_clicked)

        ################################################################################
        # External Window
        ################################################################################
        self.externalBackgroundShadow=QWidget(self)
        self.externalBackgroundShadow.setFixedSize(700,self.height())
        self.externalBackgroundShadow.move(0,0)
        self.externalBackgroundShadow.setVisible(False)
        self.externalBackgroundShadow.setStyleSheet(
        "QWidget"
            "{"
                "background-color:rgba(14,14,14,0.6);"
            "}")

        self.externalWindow=QWidget(self)
        self.externalWindow.setFixedSize(400,280)
        self.externalWindow.move(self.width()/4,-300)
        self.externalWindow.show()
        self.externalWindow.setStyleSheet(self.externalWindowbackgroundDetector)

        # Frame
        self.where_frame=QFrame(self.externalWindow)
        self.where_frame.setFixedSize(self.externalWindow.width()-60,self.externalWindow.height())
        self.where_frame.move(20,40)
        self.where_frame.setStyleSheet(self.externalWindowbackgroundDetector)

        # Scroll
        self.scroll=QScrollArea(self.externalWindow)
        self.scroll.resize(360,180)
        self.scroll.move(20,40)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.where_frame)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setStyleSheet(self.externalWindowbackgroundDetector)

        # Vertical layout V
        self.verticalLayout=QVBoxLayout(self.where_frame)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        # Info
        self.notAllowed=QLabel(self.externalWindow)
        self.notAllowed.setText("Devices with space(s) and/or special characters will be hidden.")
        self.notAllowed.setFont(ITEM)
        self.notAllowed.move(20,20)
        self.notAllowed.setStyleSheet(transparentBackground)

        ################################################################################
        # Buttons
        ################################################################################
        widgetButton=QWidget(self.externalWindow)
        widgetButton.setFixedSize((self.externalWindow.width() - 10), 58)
        widgetButton.move(5,220)
        widgetButton.setStyleSheet("""border:0px;""")

        widgetButtonLayout=QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)

        # Cancel button
        self.cancelButton=QPushButton()
        self.cancelButton.setFont(ITEM)
        self.cancelButton.setText("   Cancel   ")
        self.cancelButton.adjustSize()
        self.cancelButton.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.cancelButton.setStyleSheet(self.buttonStylesheetDetector)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        # Use this device
        self.useDiskButton=QPushButton()
        self.useDiskButton.setFont(ITEM)
        self.useDiskButton.setText("   Use Disk   ")
        self.useDiskButton.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.useDiskButton.adjustSize()
        self.useDiskButton.setEnabled(False)
        self.useDiskButton.setStyleSheet(useDiskButtonStylesheet)
        self.useDiskButton.clicked.connect(self.on_use_disk_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left Layout
        self.leftLayout.addWidget(self.backup_image_label, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.leftLayout.addWidget(self.APPNAME, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.leftLayout.addWidget(self.automatically_check_box, 1, Qt.AlignHCenter | Qt.AlignTop)

        #  Right Layout
        self.rightLayout.addStretch(10)
        self.rightLayout.addWidget(self.restore_image_label, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.rightLayout.addWidget(self.select_disk_button, 1, Qt.AlignVCenter | Qt.AlignHCenter)

        #  Far Right Layout
        self.farRightLayout.addWidget(self.external_name_label, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.external_size_label, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.oldest_backup_label, 1, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.latest_backup_label, 1, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.next_backup_label, 2, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.external_status_label, 3, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addStretch(10)
        self.farRightLayout.addWidget(self.backup_now_button, 4, Qt.AlignLeft | Qt.AlignTop)

        # Description Layout
        self.descriptionLayout.addWidget(self.descriptionTitle, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.descriptionLayout.addWidget(self.descriptionText, 0, Qt.AlignVCenter | Qt.AlignLeft)

        #  Options layout
        self.optionsLayout.addStretch()
        self.optionsLayout.addWidget(self.optionsButton, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.optionsLayout.addWidget(self.helpButton, 0, Qt.AlignRight | Qt.AlignVCenter)

        widgetButtonLayout.addStretch()
        widgetButtonLayout.addWidget(self.cancelButton,0, Qt.AlignVCenter | Qt.AlignRight)
        widgetButtonLayout.addWidget(self.useDiskButton,0, Qt.AlignVCenter | Qt.AlignRight)

        self.setLayout(self.leftLayout)

        # Startup checking
        self.startup_check()

        # Check for update
        self.check_for_updates()

        timer.timeout.connect(self.running)
        timer.start(2000)
        self.running()

    def running(self):
        print(f"Main Windows ({APP_NAME_CLOSE}) is running...")

        # Check if a backup device was registered
        if self.device_registered():
            # Check connection to it
            if is_connected(MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')):
                ################################################
                # Connection
                ################################################
                # Set external status label to Connected
                self.external_status_label.setText("Status: Connected")
                # Set external status label to color Green
                self.external_status_label.setStyleSheet('color: green')

                ################################################
                # Clean notification massage
                ################################################
                notification_message("")

                ################################################
                # Get backup devices size informations
                ################################################
                try:
                    self.external_size_label.setText(
                        f"{get_external_device_used_size()} of "
                        f"{get_external_device_max_size()} available")

                except:
                    self.external_size_label.setText("No information available")

                ################################################
                # Check if is current busy doing something
                ################################################
                # If is backing up right now
                if MAIN_INI_FILE.get_database_value('STATUS', 'backing_up_now'):
                    # Disable backup now
                    self.backup_now_button.setEnabled(False)
                    # Disable select disk
                    self.select_disk_button.setEnabled(False)
                    # Disable automatically backup
                    self.automatically_check_box.setEnabled(False)

                else:
                    # Enable backup now
                    self.backup_now_button.setEnabled(True)
                    # Enable select disk
                    self.select_disk_button.setEnabled(True)
                    # Enable automatically backup
                    self.automatically_check_box.setEnabled(True)

                ################################################
                # One time per day
                ################################################
                if MAIN_INI_FILE.get_database_value('MODE', 'one_time_mode'):
                        ################################################
                        # Automatically backup
                        ################################################
                        if MAIN_INI_FILE.get_database_value('STATUS', 'automatically_backup'):
                            ################################################
                            # Time left calculation
                            ################################################
                            if calculate_time_left_to_backup() is not None:
                                self.next_backup_label.setText(
                                    f"Next Backup: {calculate_time_left_to_backup()}")
                            else:
                                self.next_backup_label.setText(
                                    f"Next Backup: {get_next_backup().capitalize()}, "
                                    f"{MAIN_INI_FILE.get_database_value('SCHEDULE', 'hours')}:{MAIN_INI_FILE.get_database_value('SCHEDULE', 'minutes')}")
                        else:
                            self.next_backup_label.setText("Next Backup: Automatic backups off")
                else:
                    ################################################
                    # Automatically backup
                    ################################################
                    if MAIN_INI_FILE.get_database_value('STATUS', 'automatically_backup'):
                        ################################################
                        # Multiple times per day
                        ################################################
                        if MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime') == f'{TIME1}':
                            self.next_backup_label.setText(f'Next Backup: Every 1 hour')
                            self.next_backup_label.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))

                        elif MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime') == f'{TIME2}':
                            self.next_backup_label.setText(f'Next Backup: Every 2 hours')
                            self.next_backup_label.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))

                        elif MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime') == f'{TIME3}':
                            self.next_backup_label.setText(f'Next Backup: Every 4 hours')
                            self.next_backup_label.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))

                    else:
                        self.next_backup_label.setText("Next Backup: Automatic backups off")

            ################################################
            # Has no connection to it
            ################################################
            else:
                # Disable backup now
                self.backup_now_button.setEnabled(False)
                # Set external status label to Disconencted
                self.external_status_label.setText("Status: Disconnected")
                # Set external status label to color Red
                self.external_status_label.setStyleSheet('color: red')
                # Set external size label to No information
                self.external_size_label.setText("No information available")

        ################################################
        # No device was registered yet
        ################################################
        else:
            # Set external size label to No information
            self.external_size_label.setText("No information available")
            # Set external name label to None
            self.external_name_label.setText("<h1>None</h1>")
            # Set external status label to None
            self.external_status_label.setText("Status: None")
            # Set external status label to color Gray
            self.external_status_label.setStyleSheet('color: gray')
            # Set backup now to False
            self.backup_now_button.setEnabled(False)

    def device_registered(self):
        # Check if a backup device was registered
        if MAIN_INI_FILE.get_database_value('EXTERNAL', 'name') != "None":
            # Show devices name
            self.external_name_label.setText(f"<h1>{MAIN_INI_FILE.get_database_value('EXTERNAL', 'name')}</h1>")
            # Show oldest backup label
            self.oldest_backup_label.setText(f"Oldest Backup: {oldest_backup_date()}")
            # Show latest backup label
            self.latest_backup_label.setText(f"Lastest Backup: {latest_backup_date_label()}")

            # Return True
            return True
        else:
            self.external_name_label.setText(f"asd asd ")


    ################################################################################
    # STATIC
    ################################################################################
    def startup_check(self):
        if MAIN_INI_FILE.get_database_value('STATUS', 'automatically_backup'):
            self.automatically_check_box.setChecked(True)
        else:
            self.automatically_check_box.setChecked(False)

        if MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
            self.showInSystemTrayCheckBox.setChecked(True)
        else:
            self.showInSystemTrayCheckBox.setChecked(False)

    def automatically_clicked(self):
        if self.automatically_check_box.isChecked():
            # Create backup checker .desktop and move it to the destination
            create_backup_checker_desktop()

            # Copy backup_check.desktop
            shutil.copy(DST_BACKUP_CHECK_DESKTOP, dst_autostart_location)

            MAIN_INI_FILE.set_database_value('STATUS', 'automatically_backup', 'True')

            # call backup check
            sub.Popen(["python3", SRC_BACKUP_CHECKER_PY])

            print("Auto backup was successfully activated!")

        else:
            # Remove autostart.desktop
            sub.run(f"rm -f {dst_autostart_location}",shell=True)

            MAIN_INI_FILE.set_database_value('STATUS', 'automatically_backup', 'False')

            print("Auto backup was successfully deactivated!")

    # TODO
    def system_tray_clicked(self):
        if self.showInSystemTrayCheckBox.isChecked():
            MAIN_INI_FILE.set_database_value('SYSTEMTRAY', 'system_tray', 'True')

            # Call system tray
            sub.Popen(["python3", src_system_tray_py])

            print("System tray was successfully enabled!")

        else:
            MAIN_INI_FILE.set_database_value('SYSTEMTRAY', 'system_tray', 'False')

            print("System tray was successfully disabled!")

    def connected_action_to_take(self):
        self.select_disk_button.setEnabled(True)
        self.backup_now_button.setEnabled(True)
        self.automatically_check_box.setEnabled(True)
        self.showInSystemTrayCheckBox.setEnabled(True)

    def not_connected_action_to_take(self):
        self.select_disk_button.setEnabled(False)
        self.backup_now_button.setEnabled(False)
        self.automatically_check_box.setEnabled(False)
        self.showInSystemTrayCheckBox.setEnabled(False)

    def not_registered_action_to_take(self):
        self.external_name_label.setText("<h1>None</h1>")
        self.backup_now_button.setEnabled(False)

    def backup_now_clicked(self):
        sub.Popen(["python3", src_prepare_backup_py])

    def on_options_clicked(self):
        WIDGET.setCurrentWidget(MAIN_OPTIONS)

    def check_for_updates(self):
        # Check for git updates
        gitUpdateCommand = os.popen("git remote update && git status -uno").read()

        # Updates found
        if "Your branch is behind" in str(gitUpdateCommand):
            updateAvailable = QPushButton()
            updateAvailable.setText("   Update Available   ")
            updateAvailable.adjustSize()
            updateAvailable.setStyleSheet(self.buttonStylesheetDetector)
            updateAvailable.clicked.connect(self.on_update_button_clicked)

            # Show button on screen
            self.leftLayout.addWidget(updateAvailable, 0, Qt.AlignHCenter | Qt.AlignBottom)
        else:
            print("No new updates available...")

    def on_update_button_clicked(self):
        # # Disable system tray
        # if os.path.isfile(f"{DST_FOLDER_INSTALL}/src/system_tray_is_running.txt"):
        #     sub.run(f"rm {DST_FOLDER_INSTALL}/src/system_tray_is_running.txt",shell=True)

        # Call update and Exit
        backup_ini_file(True)

    ################################################################################
    # EXTERNAL
    ################################################################################
    def external_open_animation(self):
        self.anim=QPropertyAnimation(self.externalWindow, b"pos")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setEndValue(QPoint(160,0))
        self.anim.setDuration(500)
        self.anim.start()

        self.externalBackgroundShadow.setVisible(True)

        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside /Media
        ################################################################################
        if device_location():
            try:
                # Add buttons and images for each external
                for backup_device in os.listdir(f'{MEDIA}/{USERNAME}'):
                    # No spaces and special characters allowed
                    if backup_device not in CAPTURE_DEVICE and "'" not in backup_device and " " not in backup_device:
                        print("     Devices:",backup_device)
                        CAPTURE_DEVICE.append(backup_device)

                        # Avaliables external  devices
                        self.available_devices=QPushButton(self.where_frame)
                        self.available_devices.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
                        self.available_devices.setText(backup_device)
                        self.available_devices.setFixedSize(self.where_frame.width()-20,50)
                        self.available_devices.setCheckable(True)

                        if MAIN_INI_FILE.get_database_value('EXTERNAL', 'name') != "None":
                            self.available_devices.setAutoExclusive(True)

                        self.available_devices.setStyleSheet(self.availableDeviceButtonDetector)

                        text=self.available_devices.text()
                        self.available_devices.clicked.connect(lambda *args, text=text: self.on_device_clicked(text))

                        # Image
                        icon=QLabel(self.available_devices)
                        image=QPixmap(f"{SRC_RESTORE_ICON}")
                        image=image.scaled(36,36,Qt.KeepAspectRatio)
                        icon.move(7,7)
                        icon.setStyleSheet(transparentBackground)
                        icon.setPixmap(image)

                        # Free Space Label
                        free_space_label=QLabel(self.available_devices)
                        free_space_label.setText(f'{get_all_used_backup_device_space(backup_device)} / {get_all_max_backup_device_space(backup_device)}')
                        free_space_label.setFont(QFont(MAIN_FONT, 8))
                        free_space_label.setAlignment(Qt.AlignRight)
                        free_space_label.move(self.available_devices.width()-80, 30)

                        # Auto checked the choosed backup device
                        if text == MAIN_INI_FILE.get_database_value('EXTERNAL', 'name'):
                            self.available_devices.setChecked(True)

                        ################################################################################
                        # Add widgets and Layouts
                        ################################################################################
                        # Vertical layout
                        self.verticalLayout.addWidget(self.available_devices, 0, Qt.AlignHCenter)

            except FileNotFoundError:
                pass

        # If backup devices found inside /Run
        else:
            try:
                # If x device is removed or unmounted, remove from screen
                for backup_device in os.listdir(f'{RUN}/{USERNAME}'):
                    # No spaces and special characters allowed
                    if backup_device not in CAPTURE_DEVICE and "'" not in backup_device and " " not in backup_device:
                        print("     Devices:",backup_device)
                        CAPTURE_DEVICE.append(backup_device)

                        # Avaliables external  devices
                        self.available_devices=QPushButton(self.where_frame)
                        self.available_devices.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
                        self.available_devices.setText(backup_device)
                        self.available_devices.setFixedSize(self.where_frame.width()-20,60)
                        self.available_devices.setCheckable(True)
                        self.available_devices.setAutoExclusive(True)
                        self.available_devices.setStyleSheet(availableDeviceButtonStylesheet)
                        device=self.available_devices.text()

                        # Connect the device
                        self.available_devices.clicked.connect(lambda *args, device=device: self.on_device_clicked(device))


                        # Image
                        icon=QLabel(self.available_devices)
                        image=QPixmap(f"{SRC_RESTORE_ICON}")
                        image=image.scaled(46, 46, Qt.KeepAspectRatio)
                        icon.move(7, 7)
                        icon.setPixmap(image)

                        # Free Space Label
                        free_space_label=QLabel(self.available_devices)
                        free_space_label.setText(f'{get_all_used_backup_device_space(backup_device)} / {get_all_max_backup_device_space(backup_device)}')
                        free_space_label.setFont(QFont(MAIN_FONT, 8))
                        free_space_label.setAlignment(Qt.AlignRight)
                        free_space_label.move(self.available_devices.width()-80, 30)

                        ################################################################################
                        # Auto checked this choosed external device
                        ################################################################################
                        if device == MAIN_INI_FILE.get_database_value('EXTERNAL', 'name'):
                            self.available_devices.setChecked(True)

                        ################################################################################
                        # Add widgets and Layouts
                        ################################################################################
                        # Vertical layout
                        self.verticalLayout.addWidget(self.available_devices, 0, Qt.AlignHCenter)

            except FileNotFoundError:
                pass

    def on_use_disk_clicked(self):
        # Update INI file
        save_info(CHOOSE_DEVICE[-1])

        try:
            # Backup Ini File
            # backup_ini_file(False)

            self.external_close_animation()

        except:
            pass

    def on_device_clicked(self, device):
        # Add to the list
        if device not in CHOOSE_DEVICE:
            # Add to choosed device list
            CHOOSE_DEVICE.append(device)

            # Enable use disk
            self.useDiskButton.setEnabled(True)

        # Remove from the list
        else:
            # CHOOSEDEVICE.clear()
            CHOOSE_DEVICE.remove(device)

            # Disable use disk
            self.useDiskButton.setEnabled(False)

        # Limit if list is higher than 1
        if len(CHOOSE_DEVICE) > 1:
            self.useDiskButton.setEnabled(False)

        else:
            self.useDiskButton.setEnabled(True)

        if len(CHOOSE_DEVICE) == 0:
            self.useDiskButton.setEnabled(False)


        print(CHOOSE_DEVICE)

    def on_button_cancel_clicked(self):
        self.external_close_animation()

    def external_close_animation(self):
        self.anim=QPropertyAnimation(self.externalWindow, b"pos")
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
        # Set window icon
        self.setWindowIcon(QIcon(SRC_BACKUP_ICON))

        ################################################################################
        # Center window
        ################################################################################
        centerPoint=QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg=self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if detect_theme_color(APP):
            self.buttonStylesheetDetector=buttonStylesheetDark
        else:
            self.buttonStylesheetDetector=buttonStylesheet

        self.widgets()

    def widgets(self):
        # Apps version
        version=QLabel(self)
        version.setFont(QFont(MAIN_FONT, 4))
        version.setText(f"<h1>{APP_VERSION}</h1>")
        version.adjustSize()
        # version.setFixedSize(80, 20)
        version.move(290, 410)

        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget=QWidget()
        self.leftWidget.setGeometry(20, 20, 240, 405)

        # Scroll
        self.scroll=QScrollArea(self)
        self.scroll.setFixedSize(240, 405)
        self.scroll.move(20, 20)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.leftWidget)

        # Left layout
        self.leftLayout=QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setContentsMargins(10, 10, 10, 10)

        ################################################################################
        # Left title
        self.leftTitle=QLabel()
        self.leftTitle.setFont(QFont(MAIN_FONT,SMALL_FONT_SIZE))
        self.leftTitle.setText("<h1>Folders to be back up:</h1>")
        self.leftTitle.adjustSize()

        # Frame
        self.leftFrame=QFrame()
        self.leftFrame.setGeometry(20, 20, 240, 405)

        ################################################################################
        # Days to run WIDGET
        ################################################################################
        self.daysToRunWidget=QWidget(self)
        self.daysToRunWidget.setGeometry(285, 20, 390, 80)
        self.daysToRunWidget.setStyleSheet("""
            border-top: 0px;
            border-left: 0px;
            border-right: 0px;
        """)

        # Days to run layout V
        self.daysToRunLayoutV=QVBoxLayout(self.daysToRunWidget)
        self.daysToRunLayoutV.setSpacing(10)

        # Days to run layout H
        self.daysToRunLayoutH=QHBoxLayout()
        self.daysToRunLayoutH.setSpacing(10)

        # Days to run title
        self.daysToRunTitle=QLabel()
        self.daysToRunTitle.setFont(QFont(MAIN_FONT,SMALL_FONT_SIZE))
        self.daysToRunTitle.setText("<h1>Days to run:</h1>")
        self.daysToRunTitle.setAlignment(Qt.AlignLeft)
        self.daysToRunTitle.adjustSize()
        self.daysToRunTitle.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Checkboxes
        ################################################################################
        self.sun_checkbox=QCheckBox()
        self.sun_checkbox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.sun_checkbox.setText("Sun")
        self.sun_checkbox.clicked.connect(self.on_check_sun_clicked)
        self.sun_checkbox.setStyleSheet("""
            border-color: transparent;
        """)

        self.mon_checkBox=QCheckBox()
        self.mon_checkBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.mon_checkBox.setText("Mon")
        self.mon_checkBox.clicked.connect(self.on_check_mon_clicked)
        self.mon_checkBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.tue_checkBox=QCheckBox()
        self.tue_checkBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.tue_checkBox.setText("Tue")
        self.tue_checkBox.clicked.connect(self.on_check_tue_clicked)
        self.tue_checkBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.wed_checkBox=QCheckBox()
        self.wed_checkBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.wed_checkBox.setText("Wed")
        self.wed_checkBox.clicked.connect(self.on_check_wed_clicked)
        self.wed_checkBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.thu_checkBox=QCheckBox()
        self.thu_checkBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.thu_checkBox.setText("Thu")
        self.thu_checkBox.clicked.connect(self.on_check_thu_clicked)
        self.thu_checkBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.fri_checkBox=QCheckBox()
        self.fri_checkBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.fri_checkBox.setText("Fri")
        self.fri_checkBox.clicked.connect(self.on_check_fri_clicked)
        self.fri_checkBox.setStyleSheet("""
            border-color: transparent;
        """)

        self.sat_checkBox=QCheckBox()
        self.sat_checkBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.sat_checkBox.setText("Sat")
        self.sat_checkBox.clicked.connect(self.on_check_sat_clicked)
        self.sat_checkBox.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Time to run WIDGET
        ################################################################################
        self.timeToRunWidget=QWidget(self)
        self.timeToRunWidget.setGeometry(285, 100, 390, 140)
        self.timeToRunWidget.setStyleSheet("""
            border-top: 0px;
            border-bottom: 0px;
            border-left: 0px;
            border-right: 0px;
        """)

        # Time to run title
        self.timeToRunTitle=QLabel(self.timeToRunWidget)
        self.timeToRunTitle.setFont(QFont(MAIN_FONT,SMALL_FONT_SIZE))
        self.timeToRunTitle.setText("<h1>Time to run:</h1>")
        self.timeToRunTitle.setAlignment(Qt.AlignLeft)
        self.timeToRunTitle.adjustSize()
        self.timeToRunTitle.setStyleSheet("""
            border: transparent;
        """)

        # Time to run layout
        self.timeToRunLayout=QGridLayout(self.timeToRunWidget)

        # Time settings
        self.timesGridLayout=QGridLayout()

        # Radio buttons
        self.one_time_per_day_radio=QRadioButton()
        self.one_time_per_day_radio.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.one_time_per_day_radio.setText("At:")
        self.one_time_per_day_radio.setToolTip("One single back up will be execute every selected day(s) and time.")
        self.one_time_per_day_radio.adjustSize()
        self.one_time_per_day_radio.setStyleSheet(
        "QRadioButton"
           "{"
            "border: 0px solid transparent;"
            "border-radius: 5px;"
           "}")
        self.one_time_per_day_radio.clicked.connect(self.on_frequency_clicked)

        self.more_time_per_day_radio=QRadioButton()
        self.more_time_per_day_radio.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.more_time_per_day_radio.setToolTip(
            "Back up will be execute every x hours.\n"
            "This will produce a time folder inside your backup device.\n"
            "Fx: 12-12-12/10-00\n"
            "10-00, is the time of the back up (10:00).")

        self.more_time_per_day_radio.setText("Every:")
        self.more_time_per_day_radio.adjustSize()
        self.more_time_per_day_radio.setStyleSheet("""
            border-color: transparent;
        """)
        self.more_time_per_day_radio.clicked.connect(self.on_frequency_clicked)

        # Spinbox Hours
        self.hours_spinbox=QSpinBox()
        self.hours_spinbox.setFont(QFont(MAIN_FONT, 14))
        self.hours_spinbox.setFixedSize(50, 30)
        self.hours_spinbox.setFrame(False)
        self.hours_spinbox.setMinimum(0)
        self.hours_spinbox.setSingleStep(1)
        self.hours_spinbox.setMaximum(23)
        self.hours_spinbox.valueChanged.connect(self.label_hours_changed)
        self.hours_spinbox.setStyleSheet(timeBox)

        # : between hours and minutes
        self.betweenHoursAndMinutesLabel=QLabel()
        self.betweenHoursAndMinutesLabel.setFont(QFont(MAIN_FONT, 18))
        self.betweenHoursAndMinutesLabel.setText(":")
        self.betweenHoursAndMinutesLabel.setStyleSheet("""
            border-color: transparent;
        """)

        # Hours title
        self.hoursTitle=QLabel()
        self.hoursTitle.setFont(QFont(MAIN_FONT, 4))
        self.hoursTitle.setText("<h1>Hours</h1>")
        self.hoursTitle.setAlignment(Qt.AlignHCenter)
        self.hoursTitle.setStyleSheet("""
            border-color: transparent;
            border-radius: 5px;
        """)

        # Minutes title
        self.minutesTitle=QLabel()
        self.minutesTitle.setFont(QFont(MAIN_FONT, 4))
        self.minutesTitle.setText("<h1>Minutes</h1>")
        self.minutesTitle.setAlignment(Qt.AlignHCenter)
        self.minutesTitle.setStyleSheet("""
            border-color: transparent;
        """)

        # Spinbox Hours
        self.minutes_spinBox=QSpinBox()
        self.minutes_spinBox.setFont(QFont(MAIN_FONT, 14))
        self.minutes_spinBox.setFixedSize(50, 30)
        self.minutes_spinBox.setFrame(False)
        self.minutes_spinBox.setStyleSheet(timeBox)

        self.minutes_spinBox.setMinimum(0)
        self.minutes_spinBox.setSingleStep(1)
        self.minutes_spinBox.setMaximum(59)
        self.minutes_spinBox.valueChanged.connect(self.label_minutes_changed)

        # Multiple time per day combobox
        self.multiple_time_per_day_comboBox=QComboBox()
        self.multiple_time_per_day_comboBox.setFrame(True)
        self.multiple_time_per_day_comboBox.setFixedSize(132, 28)
        self.multiple_time_per_day_comboBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.multiple_time_per_day_comboBox.setStyleSheet(timeBox)

        multipleTimerPerDayComboBoxList=[
            "Every 1 hour",
            "Every 2 hours",
            "Every 4 hours"]
        self.multiple_time_per_day_comboBox.addItems(multipleTimerPerDayComboBoxList)
        self.multiple_time_per_day_comboBox.currentIndexChanged.connect(self.on_every_combox_changed)

        ################################################################################
        # Flatpak settings
        ################################################################################
        self.flatpakWidget=QWidget(self)
        self.flatpakWidget.setGeometry(285, 240, 390, 80)
        self.flatpakWidget.setStyleSheet(
        "QWidget"
        "{"
        "border-bottom: 0px;"
        "border-left: 0px;"
        "border-right: 0px;"
        "}")

        # Notification layout
        self.flatpakLayout=QVBoxLayout(self.flatpakWidget)
        self.flatpakLayout.setSpacing(5)

        # Notification title
        self.flatpakTitle=QLabel()
        self.flatpakTitle.setFont(QFont(MAIN_FONT,SMALL_FONT_SIZE))
        self.flatpakTitle.setText("<h1>Flatpak Settings:</h1>")
        self.flatpakTitle.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.flatpakTitle.setFixedSize(200, 30)
        self.flatpakTitle.setStyleSheet("""
            border: transparent;
        """)

        # # Flatpak Name checkbox
        # self.allowFlatpakNamesCheckBox=QCheckBox()
        # self.allowFlatpakNamesCheckBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        # self.allowFlatpakNamesCheckBox.setText(f"Back up Flatpaks")
        # self.allowFlatpakNamesCheckBox.adjustSize()
        # self.allowFlatpakNamesCheckBox.setStyleSheet("""
        #     border: transparent;
        # """)
        # self.allowFlatpakNamesCheckBox.clicked.connect(self.on_allow__flatpak_names_clicked)

        # Flatpak Data checkbox
        self.allowFlatpakDataCheckBox=QCheckBox()
        self.allowFlatpakDataCheckBox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.allowFlatpakDataCheckBox.setText(f"Back up Flatpaks Data (.var/app) and (.local/share/flatpak)"
            "")
        self.allowFlatpakDataCheckBox.adjustSize()
        self.allowFlatpakDataCheckBox.setStyleSheet("""
            border: transparent;
        """)
        self.allowFlatpakDataCheckBox.clicked.connect(self.on_allow__flatpak_data_clicked)

        ################################################################################
        # Reset WIDGET
        ################################################################################
        self.resetWidget=QWidget(self)
        self.resetWidget.setGeometry(285, 320, 390, 90)

        # Reset layout
        self.resetLayout=QVBoxLayout(self.resetWidget)
        self.resetLayout.setSpacing(0)

        # Reset title
        self.resetTitle=QLabel()
        self.resetTitle.setFont(QFont(MAIN_FONT,SMALL_FONT_SIZE))
        self.resetTitle.setText("<h1>Reset:</h1>")
        self.resetTitle.adjustSize()
        self.resetTitle.setAlignment(Qt.AlignLeft)

        # Reset label text
        self.resetText=QLabel()
        self.resetText.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.resetText.setText('If something seems broken, click on "Reset", to reset settings.')
        self.resetText.adjustSize()

        ################################################################################
        # Fix button
        ################################################################################
        self.fixButton=QPushButton()
        self.fixButton.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.fixButton.setText("   Reset   ")
        self.fixButton.adjustSize()
        self.fixButton.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.fixButton.setStyleSheet(self.buttonStylesheetDetector)
        self.fixButton.clicked.connect(self.on_button_fix_clicked)

        ################################################################################
        # Donate, Update and Save buttons
        ################################################################################
        self.donateAndBackWidget=QWidget(self)
        self.donateAndBackWidget.setGeometry(310, 390, 380, 60)

        # Donate and Settings WIDGET
        self.donateAndBackLayout=QHBoxLayout(self.donateAndBackWidget)
        self.donateAndBackLayout.setSpacing(10)

        # Donate buton
        self.donateButton=QPushButton()
        self.donateButton.setText("   Donate   ")
        self.donateButton.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.donateButton.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.donateButton.setStyleSheet(self.buttonStylesheetDetector)
        self.donateButton.clicked.connect(self.donate_clicked)

        ################################################################################
        # Button
        ################################################################################
        # self.applyButton=QPushButton()
        # self.applyButton.setFont(QFont(mainFont,normalFontSize))
        # self.applyButton.setText("   Apply   ")
        # self.applyButton.adjustSize()
        # self.applyButton.setFixedHeight(buttonHeightSize)
        # self.applyButton.setStyleSheet(self.buttonStylesheetDetector)
        # self.applyButton.clicked.connect(self.on_save_button_clicked)

        self.backButton=QPushButton()
        self.backButton.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
        self.backButton.setText("   Back   ")
        self.backButton.adjustSize()
        self.backButton.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.backButton.setStyleSheet(self.buttonStylesheetDetector)
        self.backButton.clicked.connect(self.on_back_button_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left layout
        self.leftLayout.addWidget(self.leftTitle, 0, Qt.AlignLeft | Qt.AlignTop)

        # Days to run layout V
        self.daysToRunLayoutV.addWidget(self.daysToRunTitle, 0, Qt.AlignTop | Qt.AlignLeft)
        self.daysToRunLayoutV.addLayout(self.daysToRunLayoutH)

        # Days to run layout H
        self.daysToRunLayoutH.addWidget(self.sun_checkbox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.mon_checkBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.tue_checkBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.wed_checkBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.thu_checkBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.fri_checkBox, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.daysToRunLayoutH.addWidget(self.sat_checkBox, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Time to run layout
        self.timeToRunLayout.addWidget(self.timeToRunTitle, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.one_time_per_day_radio, 1, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.more_time_per_day_radio, 2, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addWidget(self.multiple_time_per_day_comboBox, 2, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.timeToRunLayout.addLayout(self.timesGridLayout, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

        # Time grid layout
        self.timesGridLayout.addWidget(self.hours_spinbox, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.timesGridLayout.addWidget(self.betweenHoursAndMinutesLabel, 0, 2, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGridLayout.addWidget(self.minutes_spinBox, 0, 3, Qt.AlignTop | Qt.AlignLeft)
        self.timesGridLayout.addWidget(self.hoursTitle, 1, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.timesGridLayout.addWidget(self.minutesTitle, 1, 3, Qt.AlignVCenter | Qt.AlignHCenter)

        # Flaptak settings
        self.flatpakLayout.addWidget(self.flatpakTitle, Qt.AlignTop | Qt.AlignLeft)
        # self.flatpakLayout.addWidget(self.allowFlatpakNamesCheckBox)
        self.flatpakLayout.addWidget(self.allowFlatpakDataCheckBox)

        # Reset layout
        self.resetLayout.addWidget(self.resetTitle, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.resetText, 0, Qt.AlignLeft | Qt.AlignTop)
        self.resetLayout.addWidget(self.fixButton, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # Donate layout
        self.donateAndBackLayout.addStretch()
        self.donateAndBackLayout.addWidget(self.donateButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.donateAndBackLayout.addWidget(self.backButton, 0, Qt.AlignVCenter | Qt.AlignHCenter)

        self.setLayout(self.leftLayout)

        self.get_folders()

    def get_folders(self):
        FOLDERS_LIST = []

        # Connect to the SQLite database
        conn = sqlite3.connect(SRC_USER_CONFIG_DB)
        cursor = conn.cursor()

        # Query all keys from the specified table
        cursor.execute(f"SELECT key FROM FOLDER")
        keys = [row[0] for row in cursor.fetchall()]

        # Close the connection
        conn.close()

        for key in keys:
            FOLDERS_LIST.append(key)

        ################################################################################
        # Get Home Folders and Sort them alphabetically
        # Add On Screen
        ################################################################################
        for folder in get_home_folders():
            # Hide hidden folder
            if not "." in folder:
                # Checkboxes
                self.foldersCheckbox=QCheckBox(self.leftFrame)
                self.foldersCheckbox.setText(folder)
                self.foldersCheckbox.setFont(QFont(MAIN_FONT,NORMAL_FONT_SIZE))
                self.foldersCheckbox.adjustSize()
                # self.foldersCheckbox.setIcon(QIcon(f"{homeUser}/.local/share/{APPNAMEClose}/src/icons/folder.png"))
                self.foldersCheckbox.setStyleSheet(
                    "QCheckBox"
                    "{"
                    "border-color: transparent;"
                    "}")
                self.foldersCheckbox.clicked.connect(lambda *args, folder = folder: self.on_folder_clicked(folder))

                # Activate checkboxes in user.ini
                if folder.lower() in FOLDERS_LIST:
                    self.foldersCheckbox.setChecked(True)

                # Add to layout self.leftLayout
                self.leftLayout.addWidget(self.foldersCheckbox, 0, Qt.AlignTop)

        self.dates()

    def dates(self):
        if MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
            self.sun_checkbox.setChecked(True)

        if MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
            self.mon_checkBox.setChecked(True)

        if MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
            self.tue_checkBox.setChecked(True)

        if MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
            self.wed_checkBox.setChecked(True)

        if MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
            self.thu_checkBox.setChecked(True)

        if MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
            self.fri_checkBox.setChecked(True)

        if MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
            self.sat_checkBox.setChecked(True)

        self.time_to_run()

    def time_to_run(self):
        self.hours_spinbox.setValue(int(MAIN_INI_FILE.get_database_value('SCHEDULE', 'hours')))
        self.minutes_spinBox.setValue(int(MAIN_INI_FILE.get_database_value('SCHEDULE', 'minutes')))

        ################################################################################
        # Get info from INI file
        # One time per day
        ################################################################################
        if MAIN_INI_FILE.get_database_value('MODE', 'one_time_mode'):
            self.multiple_time_per_day_comboBox.setEnabled(False)
            self.hours_spinbox.setEnabled(True)
            self.minutes_spinBox.setEnabled(True)
            self.one_time_per_day_radio.setChecked(True)

            # Enable all days
            self.sun_checkbox.setEnabled(True)
            self.mon_checkBox.setEnabled(True)
            self.tue_checkBox.setEnabled(True)
            self.wed_checkBox.setEnabled(True)
            self.thu_checkBox.setEnabled(True)
            self.fri_checkBox.setEnabled(True)
            self.sat_checkBox.setEnabled(True)

        # Multiple time per day
        elif MAIN_INI_FILE.get_database_value('MODE', 'more_time_mode'):
            self.hours_spinbox.setEnabled(False)
            self.minutes_spinBox.setEnabled(False)
            self.multiple_time_per_day_comboBox.setEnabled(True)
            self.more_time_per_day_radio.setChecked(True)

            # Disable all days
            self.sun_checkbox.setEnabled(False)
            self.mon_checkBox.setEnabled(False)
            self.tue_checkBox.setEnabled(False)
            self.wed_checkBox.setEnabled(False)
            self.thu_checkBox.setEnabled(False)
            self.fri_checkBox.setEnabled(False)
            self.sat_checkBox.setEnabled(False)

        ################################################################################
        # Multiple time per day
        ################################################################################
        if str(MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime')) == "60":
            self.multiple_time_per_day_comboBox.setCurrentIndex(0)

        elif str(MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime')) == "120":
            self.multiple_time_per_day_comboBox.setCurrentIndex(1)

        elif str(MAIN_INI_FILE.get_database_value('SCHEDULE', 'everytime')) == "240":
            self.multiple_time_per_day_comboBox.setCurrentIndex(2)

        self.flatpak_settings()

    def flatpak_settings(self):
        ################################################################################
        # Flatpak data
        ################################################################################
        # Flatpak data
        if MAIN_INI_FILE.get_database_value('STATUS', 'allow_flatpak_data'):
            self.allowFlatpakDataCheckBox.setChecked(True)

    def on_folder_clicked(self, output):
        if MAIN_INI_FILE.get_database_value('FOLDER', f'{output.lower()}'):
            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Delete the key-value pair from the 'STATUS' table
            cursor.execute(f'DELETE FROM FOLDER WHERE key = ?', (f'{output.lower()}',))
            conn.commit()
        else:
            MAIN_INI_FILE.set_database_value('FOLDER', f'{output.lower()}', 'True')

    def on_every_combox_changed(self):
        chooseMultipleTimePerDayCombox = self.multiple_time_per_day_comboBox.currentIndex()

        if chooseMultipleTimePerDayCombox == 0:
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'everytime', f'{TIME1}')

        elif chooseMultipleTimePerDayCombox == 1:
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'everytime', f'{TIME2}')

        elif chooseMultipleTimePerDayCombox == 2:
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'everytime', f'{TIME3}')

    def on_check_sun_clicked(self):
        if self.sun_checkbox.isChecked():
            MAIN_INI_FILE.set_database_value('DAYS', 'sun', 'True')
        else:
            MAIN_INI_FILE.set_database_value('DAYS', 'sun', 'False')

    def on_check_mon_clicked(self):
        if self.mon_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('DAYS', 'mon', 'True')
        else:
            MAIN_INI_FILE.set_database_value('DAYS', 'mon', 'False')

    def on_check_tue_clicked(self):
        if self.tue_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('DAYS', 'tue', 'True')
        else:
            MAIN_INI_FILE.set_database_value('DAYS', 'tue', 'False')

    def on_check_wed_clicked(self):
        if self.wed_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('DAYS', 'wed', 'True')
        else:
            MAIN_INI_FILE.set_database_value('DAYS', 'wed', 'False')

    def on_check_thu_clicked(self):
        if self.thu_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('DAYS', 'thu', 'True')
        else:
            MAIN_INI_FILE.set_database_value('DAYS', 'thu', 'False')

    def on_check_fri_clicked(self):
        if self.fri_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('DAYS', 'fri', 'True')
        else:
            MAIN_INI_FILE.set_database_value('DAYS', 'fri', 'False')

    def on_check_sat_clicked(self):
        if self.sat_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('DAYS', 'sat', 'True')
        else:
            MAIN_INI_FILE.set_database_value('DAYS', 'sat', 'False')

    def label_hours_changed(self): 
        hours = str(self.hours_spinbox.value())

        MAIN_INI_FILE.set_database_value('SCHEDULE', 'hours', hours)

    def label_minutes_changed(self):
        minutes = str(self.minutes_spinBox.value())
        
        if minutes in FIX_MINUTES:
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'minutes', f'0{minutes}')
        else:
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'minutes', f'{minutes}')
       
        print("GET", MAIN_INI_FILE.get_database_value('SCHEDULE', 'minutes'))
        
    def on_frequency_clicked(self):
        if self.one_time_per_day_radio.isChecked():
            MAIN_INI_FILE.set_database_value('MODE', 'one_time_mode', 'True')
            MAIN_INI_FILE.set_database_value('MODE', 'more_time_mode', 'False')

            self.multiple_time_per_day_comboBox.setEnabled(False)
            self.hours_spinbox.setEnabled(True)
            self.minutes_spinBox.setEnabled(True)
            self.one_time_per_day_radio.setChecked(True)

            # Enable all days
            self.sun_checkbox.setEnabled(True)
            self.mon_checkBox.setEnabled(True)
            self.tue_checkBox.setEnabled(True)
            self.wed_checkBox.setEnabled(True)
            self.thu_checkBox.setEnabled(True)
            self.fri_checkBox.setEnabled(True)
            self.sat_checkBox.setEnabled(True)

        elif self.more_time_per_day_radio.isChecked():
            MAIN_INI_FILE.set_database_value('MODE', 'more_time_mode', 'True')
            MAIN_INI_FILE.set_database_value('MODE', 'one_time_mode', 'False')

            self.hours_spinbox.setEnabled(False)
            self.minutes_spinBox.setEnabled(False)
            self.multiple_time_per_day_comboBox.setEnabled(True)
            self.more_time_per_day_radio.setChecked(True)

            # Disable all days
            self.sun_checkbox.setEnabled(False)
            self.mon_checkBox.setEnabled(False)
            self.tue_checkBox.setEnabled(False)
            self.wed_checkBox.setEnabled(False)
            self.thu_checkBox.setEnabled(False)
            self.fri_checkBox.setEnabled(False)
            self.sat_checkBox.setEnabled(False)

    def on_allow__flatpak_data_clicked(self):
        if self.allowFlatpakDataCheckBox.isChecked():
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'True')
            print("Allow flatpaks data to be backup.")
        else:
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'False')

    def on_button_fix_clicked(self):
        reset_confirmation=QMessageBox.question(
            self,
            'Reset',
            'Are you sure you want to reset settings?',QMessageBox.Yes | QMessageBox.No)

        if reset_confirmation == QMessageBox.Yes:
            MAIN.latest_backup_label.setText("Latest Backup: None")
            MAIN.oldest_backup_label.setText("Oldest Backup: None")
            
            # Reset settings
            # Backup section
            MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'No')
            MAIN_INI_FILE.set_database_value('STATUS', 'automatically_backup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'first_startup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_names', 'True')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')
            
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'hd', 'None')
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'name', 'None')
            
            MAIN_INI_FILE.set_database_value('MODE', 'one_time_mode', 'True')
            MAIN_INI_FILE.set_database_value('MODE', 'more_time_mode', 'False')
            
            MAIN_INI_FILE.set_database_value('SYSTEMTRAY', 'system_tray', 'False')
            
            MAIN_INI_FILE.set_database_value('DAYS', 'sun', 'True')
            MAIN_INI_FILE.set_database_value('DAYS', 'mon', 'True')
            MAIN_INI_FILE.set_database_value('DAYS', 'tue', 'True')
            MAIN_INI_FILE.set_database_value('DAYS', 'wed', 'True')
            MAIN_INI_FILE.set_database_value('DAYS', 'thu', 'True')
            MAIN_INI_FILE.set_database_value('DAYS', 'fri', 'True')
            MAIN_INI_FILE.set_database_value('DAYS', 'sat', 'True')
            
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'hours', '10')
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'minutes', '00')
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'everytime', '60')
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'time_left', 'None')
            MAIN_INI_FILE.set_database_value('SCHEDULE', 'time_left', 'None')
            
            MAIN_INI_FILE.set_database_value('INFO', 'language', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'os', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'packageManager', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'theme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'icon', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'cursor', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'colortheme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', 'None')
            
            MAIN_INI_FILE.set_database_value('FOLDER', 'pictures', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'documents', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'music', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'videos', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'desktop', 'True')

            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_data', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'is_restore_running', 'False')

            print("All settings was reset!")

            # Re-open Main Windows
            sub.Popen(["python3", SRC_MAIN_WINDOW_PY])

            # Quit
            exit()

        else:
            QMessageBox.Close

    def donate_clicked(self):
        sub.Popen([f"xdg-open", "https://ko-fi.com/geovanejeff"])

    def on_back_button_clicked(self):
        WIDGET.setCurrentWidget(MAIN)


if __name__ == '__main__':
    APP = QApplication(sys.argv)

    MAIN_INI_FILE = UPDATEINIFILE()
    MAIN = MainWindow()
    MAIN_OPTIONS=OPTION()

    WIDGET = QStackedWidget()
    WIDGET.addWidget(MAIN)
    WIDGET.addWidget(MAIN_OPTIONS)
    WIDGET.setCurrentWidget(MAIN)
    WIDGET.show()

    WIDGET.setWindowTitle(APP_NAME)
    WIDGET.setWindowIcon(QIcon(SRC_BACKUP_ICON))
    WIDGET.setFixedSize(700,450)

    APP.exit(APP.exec())
