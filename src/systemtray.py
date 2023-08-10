#! /usr/bin/python3
from setup import *
from stylesheet import *
from check_connection import *
from get_backup_time import *
from get_backup_date import *
from get_time import *
from get_latest_backup_date import latest_backup_date_label
from calculate_time_left_to_backup import calculate_time_left_to_backup
from read_ini_file import UPDATEINIFILE


DELAY_TO_UPDATE=2000


class APP:
    def __init__(self):
        self.color = str()
        self.iniUI()

    def iniUI(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationDisplayName(APP_NAME)
        self.app.setApplicationName(APP_NAME)

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if self.app.palette().windowText().color().getRgb()[0] < 55:
            self.system_bar_icon_stylesheet_detector = src_system_bar_icon
        else:
            self.system_bar_icon_stylesheet_detector = src_system_bar_white_icon

        self.widget()

    def widget(self):
        # Tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(self.system_bar_icon_stylesheet_detector))
        self.tray.setVisible(True)
        self.tray.activated.connect(self.tray_icon_clicked)

        # Create a menu
        self.menu = QMenu()

        # Ini last backup information
        self.iniLastBackupInformation = QAction()
        self.iniLastBackupInformation.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.iniLastBackupInformation.setEnabled(False)
        
        self.iniLastBackupInformation2 = QAction()
        self.iniLastBackupInformation2.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.iniLastBackupInformation2.setEnabled(False)

        # Backup now button
        self.backupNowButton = QAction("Back Up Now")
        self.backupNowButton.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.backupNowButton.triggered.connect(self.backup_now)

        # Browse Time Machine Backups button
        self.browseTimeMachineBackupsButton = QAction("Browse Time Machine Backups")
        self.browseTimeMachineBackupsButton.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.browseTimeMachineBackupsButton.triggered.connect(
            lambda: sub.Popen(f"python3 {src_enter_time_machine_test_py}", shell=True))

        # Open Time Machine button
        self.openTimeMachine = QAction(f"Open {APP_NAME}")
        self.openTimeMachine.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.openTimeMachine.triggered.connect(
            lambda: sub.Popen(f"python3 {SRC_MAIN_WINDOW_PY}",shell=True))

        # Add all to menu
        # self.menu.addAction(self.dummyLine)
        self.menu.addAction(self.iniLastBackupInformation)
        self.menu.addAction(self.iniLastBackupInformation2)
        self.menu.addSeparator()

        self.menu.addAction(self.backupNowButton)
        self.menu.addAction(self.browseTimeMachineBackupsButton)
        self.menu.addSeparator()
        
        self.menu.addAction(self.openTimeMachine)
        self.menu.addSeparator()
        
        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)
        
        timer.timeout.connect(self.should_be_running)
        timer.start(DELAY_TO_UPDATE) 
        self.should_be_running()

        self.app.exec()
    
    def should_be_running(self):
        print("System tray is running...")
        
        # Check if ini file is locked or not 
        if not MAIN_INI_FILE.ini_system_tray():
            # Quit 
            self.exit()

        self.has_connection()
        
    def has_connection(self):
        try:
            # User has registered a device name
            if MAIN_INI_FILE.ini_hd_name() != "None":
                # Can device be found?
                if is_connected(MAIN_INI_FILE.ini_hd_name()):
                    # Is backup now running? (chech if file exists)
                    self.status_on()
                else:
                    self.status_off()
                
            # No backup device registered
            else:
                self.iniLastBackupInformation.setText('First, select a backup device.')
                self.iniLastBackupInformation2.setText('')
                
                # Backup now button to False
                self.backupNowButton.setEnabled(False)
                
                # Browser Time Machine button to False 
                self.browseTimeMachineBackupsButton.setEnabled(False)
        
        except Exception:
            self.exit()

    def status_on(self):
        # Backing up right now False
        if not MAIN_INI_FILE.ini_backing_up_now():
            self.change_color("White")
            self.backupNowButton.setEnabled(True)
            self.browseTimeMachineBackupsButton.setEnabled(True)

            if calculate_time_left_to_backup() is not None:
                self.iniLastBackupInformation.setText(f'Next Backup to "{MAIN_INI_FILE.ini_hd_name()}":')
                self.iniLastBackupInformation2.setText(f'{calculate_time_left_to_backup()}\n')
            else:
                self.iniLastBackupInformation.setText(f'Latest Backup to "{MAIN_INI_FILE.ini_hd_name()}":')
                self.iniLastBackupInformation2.setText(f'{str(latest_backup_date_label())}\n')
    
        else:
            # Change color to Blue
            self.change_color("Blue")

            # Notification information
            self.iniLastBackupInformation.setText(f"{MAIN_INI_FILE.ini_current_backup_information()}")
            self.iniLastBackupInformation2.setText('')
        
            self.backupNowButton.setEnabled(False)
            self.browseTimeMachineBackupsButton.setEnabled(False)
   
    def status_off(self):
        if MAIN_INI_FILE.ini_automatically_backup():
            self.change_color("Red")
            self.backupNowButton.setEnabled(False)
            self.browseTimeMachineBackupsButton.setEnabled(False)
            
            # if self.iniNotificationID != " ":
            #     # Clean notification add info, because auto backup is not enabled
            #     config=configparser.ConfigParser()
            #     config.read(src_user_config)
            #     with open(src_user_config, 'w', encoding='utf8') as configfile:
            #         config.set('INFO', 'notification_add_info', ' ')
            #         config.write(configfile)

    def is_current_restoring(self):
        if not MAIN_INI_FILE.ini_automatically_backup():
            if MAIN_INI_FILE.ini_is_restoring():
                self.change_color("Yellow")
                self.backupNowButton.setEnabled(False)
                self.browseTimeMachineBackupsButton.setEnabled(False)

    def backup_now(self):
        sub.Popen(f"python3 {src_prepare_backup_py}", shell=True)

    def change_color(self,color):
        try:
            if self.color != color:
                if color == "Blue":
                    self.color=color
                    self.tray.setIcon(QIcon(SRC_SYSTEM_BAR_RUN_ICON))

                elif color == "White":
                    self.color=color
                    self.tray.setIcon(QIcon(self.system_bar_icon_stylesheet_detector))

                elif color == "Red":
                    self.color=color
                    self.tray.setIcon(QIcon(src_system_bar_error_icon))

                elif color == "Yellow":
                    self.color=color
                    self.tray.setIcon(QIcon(src_system_bar_restore_icon))

        except Exception as e:
            self.exit()

    def exit(self):
        config=configparser.ConfigParser()
        config.read(SRC_USER_CONFIG)
        with open(SRC_USER_CONFIG, 'w') as configfile:
            config.set('SYSTEMTRAY', 'system_tray', 'False')
            config.write(configfile)

        self.tray.hide()
        QtWidgets. cation.exit()
    
    def tray_icon_clicked(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            self.tray.contextMenu().exec(QCursor.pos())
    

if __name__ == '__main__':
    MAIN_INI_FILE=UPDATEINIFILE()
    main=APP()