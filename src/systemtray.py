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


DELAY_TO_UPDATE = 2000


class APP:
    def __init__(self):
        self.color = str()
        self.iniUI()

    def iniUI(self):
        self.app = QApplication([], stdout=sub.PIPE, stderr=sub.PIPE)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationDisplayName(APP_NAME)
        self.app.setApplicationName(APP_NAME)

        self.widget()

    def widget(self):
        # Tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(self.get_system_color()))
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
        self.browse_time_machine_backups = QAction("Browse Time Machine Backups")
        self.browse_time_machine_backups.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        enter_in_time_machine_command = src_enter_time_machine_test_py
        self.browse_time_machine_backups.triggered.connect(
            lambda: sub.Popen(["python3", enter_in_time_machine_command], stdout=sub.PIPE, stderr=sub.PIPE))
        
        # Open Time Machine button
        self.open_Time_machine = QAction(f"Open {APP_NAME}")
        self.open_Time_machine.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        command = SRC_MAIN_WINDOW_PY
        self.open_Time_machine.triggered.connect(
            lambda: sub.Popen(["python3", command], stdout=sub.PIPE, stderr=sub.PIPE))

        # Add all to menu
        # self.menu.addAction(self.dummyLine)
        self.menu.addAction(self.iniLastBackupInformation)
        self.menu.addAction(self.iniLastBackupInformation2)
        self.menu.addSeparator()

        self.menu.addAction(self.backupNowButton)
        self.menu.addAction(self.browse_time_machine_backups)
        self.menu.addSeparator()
        
        self.menu.addAction(self.open_Time_machine)
        self.menu.addSeparator()
        
        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)
        
        timer.timeout.connect(self.should_be_running)
        timer.start(DELAY_TO_UPDATE) 

        # CHeck if system tray should be running
        self.should_be_running()

        self.app.exec()
    
    def should_be_running(self):
        print("System tray is running...")
        
        # Check if ini file is locked or not 
        if not MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
            self.exit()

        self.has_connection()
        
    def has_connection(self):
        # User has registered a device name
        if MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd') != "None":
            # Can device be found?
            if is_connected(MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')):
                # Is backup now running? (chech if file exists)
                self.status_on()
            else:
                if MAIN_INI_FILE.get_database_value("STATUS", "automatically_backup"):
                    self.status_off()
            
        # No backup device registered
        else:
            self.iniLastBackupInformation.setText('First, select a backup device.')
            self.iniLastBackupInformation2.setText('')
            
            # Backup now button to False
            self.backupNowButton.setEnabled(False)
            
            # Browser Time Machine button to False 
            self.browse_time_machine_backups.setEnabled(False)

    def status_on(self):
        # Backing up right now False
        if not MAIN_INI_FILE.get_database_value('STATUS', 'backing_up_now'):
            # Change color to White
            self.change_color("White")

            self.backupNowButton.setEnabled(True)
            self.browse_time_machine_backups.setEnabled(True)

            if calculate_time_left_to_backup() is not None:
                self.iniLastBackupInformation.setText(
                    f'Next Backup to "{MAIN_INI_FILE.get_database_value("EXTERNAL", "name")}":')
                self.iniLastBackupInformation2.setText(f'{calculate_time_left_to_backup()}\n')
            else:
                self.iniLastBackupInformation.setText(
                    f'Latest Backup to "{MAIN_INI_FILE.get_database_value("EXTERNAL", "name")}":')
                self.iniLastBackupInformation2.setText(f'{str(latest_backup_date_label())}\n')
    
        else:
            # Change color to Blue
            self.change_color("Blue")

            # Notification information
            self.iniLastBackupInformation.setText(f"{MAIN_INI_FILE.get_database_value('INFO', 'current_backing_up')}")
            self.iniLastBackupInformation2.setText('')
        
            self.backupNowButton.setEnabled(False)
            self.browse_time_machine_backups.setEnabled(False)
   
    def status_off(self):
        # Change color to Red
        self.change_color("Red")
        
        self.backupNowButton.setEnabled(False)
        self.browse_time_machine_backups.setEnabled(False)
        
        # if self.iniNotificationID != " ":
        #     # Clean notification add info, because auto backup is not enabled
        #     config=configparser.ConfigParser()
        #     config.read(src_user_config)
        #     with open(src_user_config, 'w', encoding='utf8') as configfile:
        #         config.set('INFO', 'notification_add_info', ' ')
        #         config.write(configfile)

    def is_current_restoring(self):
        if not MAIN_INI_FILE.get_database_value("STATUS", "automatically_backup"):
            if MAIN_INI_FILE.get_database_value("STATUS", "is_restoring"):
                self.change_color("Yellow")
                self.backupNowButton.setEnabled(False)
                self.browse_time_machine_backups.setEnabled(False)

    def backup_now(self):
        command = src_prepare_backup_py
        sub.run(["python3", command], stdout=sub.PIPE, stderr=sub.PIPE)

    def change_color(self,color):
        try:
            if self.color != color:
                if color == "Blue":
                    self.color=color
                    self.tray.setIcon(QIcon(SRC_SYSTEM_BAR_RUN_ICON))

                elif color == "White":
                    self.color=color
                    self.tray.setIcon(QIcon(self.get_system_color()))

                elif color == "Red":
                    self.color=color
                    self.tray.setIcon(QIcon(src_system_bar_error_icon))

                elif color == "Yellow":
                    self.color=color
                    self.tray.setIcon(QIcon(src_system_bar_restore_icon))

        except Exception:
            self.exit()

    def exit(self):
        MAIN_INI_FILE.set_database_value("SYSTEMTRAY", "system_tray", 'False')
        
        self.tray.hide()
        exit()
    
    def tray_icon_clicked(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            self.tray.contextMenu().exec(QCursor.pos())

    def get_system_color(self):
        # Detect dark theme
        if self.app.palette().windowText().color().getRgb()[0] < 55:
            self.system_bar_icon_stylesheet_detector = src_system_bar_icon
        else:
            self.system_bar_icon_stylesheet_detector = src_system_bar_white_icon
        
        return self.system_bar_icon_stylesheet_detector


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    main = APP()