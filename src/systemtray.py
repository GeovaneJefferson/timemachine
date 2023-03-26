#! /usr/bin/python3
from setup import *
from check_connection import *
from get_backup_times import *
from get_backup_dates import *
from get_time import *
from read_ini_file import UPDATEINIFILE

# QTimer
timer = QtCore.QTimer()


class APP:
    def __init__(self):
        self.color = str()
        self.iniUI()

    def iniUI(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationDisplayName(appName)
        self.app.setApplicationName(appName)
    
        self.widget()

    def widget(self):
        ################################################################################
        # Add icon
        ################################################################################
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(src_system_bar_icon))
        self.tray.setVisible(True)

        # Create a menu
        self.menu = QMenu()

        # Ini last backup information
        self.iniLastBackupInformation = QAction()
        self.iniLastBackupInformation.setFont(QFont(item))
        self.iniLastBackupInformation.setEnabled(False)

        # Line
        self.dummyLine = QAction("――――――――――――――")
        self.dummyLine.setEnabled(False)
      
        # Line2
        self.dummyLine2 = QAction("――――――――――――――")
        self.dummyLine2.setEnabled(False)

        # Line3
        self.dummyLine3 = QAction("――――――――――――――")
        self.dummyLine3.setEnabled(False)

        # Backup now button
        self.backupNowButton = QAction("Back Up Now")
        self.backupNowButton.setFont(QFont(item))
        self.backupNowButton.triggered.connect(self.backup_now)

        # Browse Time Machine Backups button
        self.browseTimeMachineBackupsButton = QAction("Browse Time Machine Backups")
        self.browseTimeMachineBackupsButton.setFont(QFont(item))
        self.browseTimeMachineBackupsButton.triggered.connect(
            lambda: sub.Popen(f"python3 {src_enter_time_machine_py}", shell=True))

        # Open Time Machine button
        self.openTimeMachine = QAction(f"Open {appName}")
        self.openTimeMachine.setFont(QFont(item))
        self.openTimeMachine.triggered.connect(
            lambda: sub.Popen(f"python3 {src_main_window_py}", shell=True))

        # Add all to menu
        self.menu.addAction(self.dummyLine)
        self.menu.addAction(self.iniLastBackupInformation)

        self.menu.addAction(self.dummyLine2)
        # self.menu.addAction(self.skipThisBackup)

        self.menu.addAction(self.backupNowButton)
        self.menu.addAction(self.browseTimeMachineBackupsButton)
        
        self.menu.addAction(self.dummyLine3)
        self.menu.addAction(self.openTimeMachine)
        
        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)

        ################################################################################
        # Read Ini File
        ################################################################################
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every x second
        self.updates()
        
        self.app.exec()
    
    def updates(self):
        print("System tray is running...")
        
        self.system_tray_manager()

    def system_tray_manager(self):
        try:
            if str(mainIniFile.ini_system_tray()) == "false":
                print("Exiting system tray...")
                exit()
                
        except KeyError as error:
            print(error)
            print("System Tray (136) KeyError!")
            pass

        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Check Connection 
        ################################################################################
        # User has registered a device name
        if str(mainIniFile.ini_hd_name()) != "None":
            if is_connected(str(mainIniFile.ini_hd_name())):
                if str(mainIniFile.ini_backup_now()) == "false":
                    self.change_color("White")
                    # # White color
                    # self.tray.setIcon(QIcon(src_system_bar_icon))
                    # Show backup now button
                    self.backupNowButton.setEnabled(True)
                    # Enable enter in time machine button
                    self.browseTimeMachineBackupsButton.setEnabled(True)
                    # try:
                    #     # search inside backup folder, if today date inside, wirte Today
                    #     if get_backup_date()[0] == today_date():
                    #         # Update last backup information
                    #         self.iniLastBackupInformation.setText(f'Latest Backup to "{str(mainIniFile.ini_hd_name())}":\n'
                    #             f'Today, {str(get_latest_backup_time()[0]).replace("-",":")}')
                    #     else:
                    #         # Update last backup information
                    #         self.iniLastBackupInformation.setText(f'Latest Backup to "{str(mainIniFile.ini_hd_name())}":\n'
                    #             f'{str(mainIniFile.ini_lastest_backup())}')
                    # except:
                    #     pass
                    
                    # Update last backup information
                    self.iniLastBackupInformation.setText(f'Latest Backup to "{str(mainIniFile.ini_hd_name())}":\n'
                        f'{str(mainIniFile.ini_lastest_backup())}')

                else:
                    self.change_color("Blue")
                    # # Blue color
                    # self.tray.setIcon(QIcon(src_system_bar_run_icon))
                    self.iniLastBackupInformation.setText(f"{str(mainIniFile.ini_current_backup_information())}")
        
            else:
                self.change_color("Red")
                # Red color
                # self.tray.setIcon(QIcon(src_system_bar_error_icon))
                # Hide backup now button
                self.backupNowButton.setEnabled(False)
                # Hide Enter In Time Machine
                self.browseTimeMachineBackupsButton.setEnabled(False)

                # If backup device is not connected and automatically if ON
                if str(mainIniFile.ini_automatically_backup()) == "true":
                    self.change_color("Red")
                    # # Change system tray red color
                    # self.tray.setIcon(QIcon(src_system_bar_error_icon))

                else:
                    # Read ini file befora write
                    if self.iniNotificationID != " ":
                        # Clean notification add info, because auto backup is not enabled
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w', encoding='utf8') as configfile:
                            config.set('INFO', 'notification_add_info', ' ')
                            config.write(configfile)
            
                        self.change_color("White")
                        # # Change system tray white color
                        # self.tray.setIcon(QIcon(src_system_bar_icon))

        else:
            # Update last backup information
            self.iniLastBackupInformation.setText('First, select a backup device.')
            # Disable backup now button
            self.backupNowButton.setEnabled(False)
            # Disable enter in time machine button
            self.browseTimeMachineBackupsButton.setEnabled(False)

    def backup_now(self):
        sub.Popen(f"python3 {src_prepare_backup_py}", shell=True)

    def change_color(self,color):
        if self.color != color:
            print("Changing color")
            if color == "Blue":
                self.color = "Blue"
                self.tray.setIcon(QIcon(src_system_bar_run_icon))
            elif color == "White":
                self.color = "White"
                self.tray.setIcon(QIcon(src_system_bar_icon))
            elif color == "Red":
                self.color = "Red"
                self.tray.setIcon(QIcon(src_system_bar_error_icon))

if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    main = APP()