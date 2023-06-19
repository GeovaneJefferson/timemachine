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
from add_backup_now_file import add_backup_now_file, can_backup_now_file_be_found
from add_system_tray_file import can_system_tray_file_be_found, remove_system_tray_file
from add_backup_now_file import can_backup_now_file_be_found, remove_backup_now_file
from update_notification_status import update_notification_status

class APP:
    def __init__(self):
        self.color = str()
        self.iniUI()

    def iniUI(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationDisplayName(appName)
        self.app.setApplicationName(appName)
        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if self.app.palette().windowText().color().getRgb()[0] < 55:
            self.systemBarIconStylesheetDetector = src_system_bar_white_icon
        else:
            self.systemBarIconStylesheetDetector = src_system_bar_icon

        self.widget()

    def widget(self):
        ################################################################################
        # Add icon
        ################################################################################
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(self.systemBarIconStylesheetDetector))
        self.tray.setVisible(True)
        self.tray.activated.connect(self.tray_icon_clicked)

        # Create a menu
        self.menu = QMenu()

        # Ini last backup information
        self.iniLastBackupInformation = QAction()
        self.iniLastBackupInformation.setFont(QFont(mainFont,buttonFontSize))
        self.iniLastBackupInformation.setEnabled(False)
        
        self.iniLastBackupInformation2 = QAction()
        self.iniLastBackupInformation2.setFont(QFont(mainFont,buttonFontSize))
        self.iniLastBackupInformation2.setEnabled(False)

        # Backup now button
        self.backupNowButton = QAction("Back Up Now")
        self.backupNowButton.setFont(QFont(mainFont,buttonFontSize))
        self.backupNowButton.triggered.connect(self.backup_now)

        # Browse Time Machine Backups button
        self.browseTimeMachineBackupsButton = QAction("Browse Time Machine Backups")
        self.browseTimeMachineBackupsButton.setFont(QFont(mainFont,buttonFontSize))
        self.browseTimeMachineBackupsButton.triggered.connect(
            lambda: sub.Popen(f"python3 {src_enter_time_machine_py}", shell=True))

        # Open Time Machine button
        self.openTimeMachine = QAction(f"Open {appName}")
        self.openTimeMachine.setFont(QFont(mainFont,buttonFontSize))
        self.openTimeMachine.triggered.connect(
            lambda: sub.Popen(f"python3 {src_main_window_py}",shell=True))

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
        timer.start(2000) 
        self.should_be_running()

        self.app.exec()
    
    def should_be_running(self):
        print("System tray is running...")
        
        if not can_system_tray_file_be_found():
            self.exit()

        self.has_connection()
        
    def has_connection(self):
        try:
            # User has registered a device name
            if str(mainIniFile.ini_hd_name()) != "None":
                # Can device be found?
                if is_connected(str(mainIniFile.ini_hd_name())):
                    # Is backup now running? (chech if file exists)
                    self.set_status_on()
                else:
                    self.set_status_off()
                
            else:
                self.iniLastBackupInformation.setText('First, select a backup device.')
                self.iniLastBackupInformation2.setText('')
                self.backupNowButton.setEnabled(False)
                self.browseTimeMachineBackupsButton.setEnabled(False)
        
        except Exception as error:
            print(error)
            self.exit()

    def set_status_on(self):
        # Not backing up right now
        if not can_backup_now_file_be_found():
            self.change_color("White")
            self.backupNowButton.setEnabled(True)
            self.browseTimeMachineBackupsButton.setEnabled(True)

            if calculate_time_left_to_backup() != None:
                self.iniLastBackupInformation.setText(f'Next Backup to "{str(mainIniFile.ini_hd_name())}":')
                self.iniLastBackupInformation2.setText(f'{calculate_time_left_to_backup()}\n')
            else:
                self.iniLastBackupInformation.setText(f'Latest Backup to "{str(mainIniFile.ini_hd_name())}":')
                self.iniLastBackupInformation2.setText(f'{str(latest_backup_date_label())}\n')
    
        else:
            self.change_color("Blue")
            # self.iniLastBackupInformation.setText("Backing up...")
            self.iniLastBackupInformation.setText(f"{str(mainIniFile.ini_current_backup_information())}")
            self.iniLastBackupInformation2.setText('')
            
            self.backupNowButton.setEnabled(False)
            self.browseTimeMachineBackupsButton.setEnabled(False)
   
    def set_status_off(self):
        if str(mainIniFile.ini_automatically_backup()) == "true":
            self.change_color("Red")
            self.backupNowButton.setEnabled(False)
            self.browseTimeMachineBackupsButton.setEnabled(False)
            
            # if self.iniNotificationID != " ":
            #     # Clean notification add info, because auto backup is not enabled
            #     config = configparser.ConfigParser()
            #     config.read(src_user_config)
            #     with open(src_user_config, 'w', encoding='utf8') as configfile:
            #         config.set('INFO', 'notification_add_info', ' ')
            #         config.write(configfile)

    def backup_now(self):
        sub.Popen(f"python3 {src_prepare_backup_py}", shell=True)

    def change_color(self,color):
        try:
            if self.color != color:
                if color == "Blue":
                    self.color = color
                    self.tray.setIcon(QIcon(src_system_bar_run_icon))

                elif color == "White":
                    self.color = color
                    self.tray.setIcon(QIcon(self.systemBarIconStylesheetDetector))

                elif color == "Red":
                    self.color = color
                    self.tray.setIcon(QIcon(src_system_bar_error_icon))

        except Exception as error:
            print(error)
            self.exit()

    def exit(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('SYSTEMTRAY', 'system_tray', 'false')
            config.write(configfile)

        if can_system_tray_file_be_found():
            remove_system_tray_file()
        
        if can_backup_now_file_be_found():
            remove_backup_now_file()
            
        self.tray.hide()
        QtWidgets.QApplication.exit()
    
    def tray_icon_clicked(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            self.tray.contextMenu().exec(QCursor.pos())

if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    main = APP()