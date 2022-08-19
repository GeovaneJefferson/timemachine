#! /usr/bin/python3
from setup import *

# QTimer
timer = QtCore.QTimer()


class APP:
    def __init__(self):
        self.connected = None
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

        ################################################################################
        # Add item on the menu bar
        ################################################################################
        # Create a menu
        self.menu = QMenu()

        # Ini last backup information
        self.iniLastBackupInformation = QAction()
        self.iniLastBackupInformation.setFont(QFont(item))
        self.iniLastBackupInformation.setEnabled(False)

        # Line
        self.dummyLine = QAction("――――――――――――")
        self.dummyLine.setFont(QFont(item))
        self.dummyLine.setEnabled(False)
      
        # Line2
        self.dummyLine2 = QAction("――――――――――――")
        self.dummyLine2.setFont(QFont(item))
        self.dummyLine2.setEnabled(False)
      
        # Backup now button
        self.backupNowButton = QAction("Back Up Now")
        self.backupNowButton.setFont(QFont(item))
        self.backupNowButton.triggered.connect(self.backup_now)

        # Skip this backup
        self.skipThisBackup = QAction("Skip This Backup")
        self.skipThisBackup.setFont(QFont(item))
        # self.skipThisBackup.triggered.connect(self.backup_now)

        # Enter time machine button
        self.enterTimeMachineButton = QAction("Enter Time Machine")
        self.enterTimeMachineButton.setFont(QFont(item))
        self.enterTimeMachineButton.triggered.connect(
            lambda: sub.Popen(f"python3 {src_enter_time_machine_py}", shell=True))

        # Open Time Machine button
        self.openTimeMachine = QAction(f"Open {appName}")
        self.openTimeMachine.setFont(QFont(item))
        self.openTimeMachine.triggered.connect(
            lambda: sub.Popen(f"python3 {src_main_window_py}", shell=True))

        # Add all to menu
        self.menu.addAction(self.iniLastBackupInformation)
        self.menu.addAction(self.dummyLine)
        self.menu.addAction(self.enterTimeMachineButton)
        self.menu.addAction(self.backupNowButton)
        self.menu.addAction(self.dummyLine2)
        self.menu.addAction(self.openTimeMachine)

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)

        # Tray
        self.icon = QIcon(src_system_bar_icon)
        self.tray.setIcon(self.icon)

        ################################################################################
        # Check ini
        ################################################################################
        timer.timeout.connect(self.updates)
        timer.start(2000)  # update every x second
        self.updates()
        
        # App exec
        self.app.exec()
    
    def updates(self):
        print("System tray is running...")
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # Backup now
            self.iniBackupNow = config['BACKUP']['backup_now']
            # Automatically backup
            self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
            # INI notification
            self.iniNotification = config['INFO']['notification_id']
            # INI HD Name
            self.iniHDName = config['EXTERNAL']['name']
            # INI system tray
            self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
            # INI last backup
            self.iniLastBackup = config['INFO']['latest']
            # Current backup information
            self.iniCurrentBackupInfo = config['INFO']['feedback_status']

        except KeyError as error:
            print(error)
            print("System Tray KeyError!")
            exit()

        self.system_tray_manager()

    def system_tray_manager(self):
        if self.iniSystemTray == "false":
            print("Exiting system tray...")

            try:
                # Write ini file
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('SYSTEMTRAY', 'system_tray', 'false')
                    config.write(configfile)

            except KeyError as error:
                print(error)
                print("System Tray (136) KeyError!")
                
            exit()

        self.check_connection()

    def check_connection(self):
        ################################################################################
        # External availability
        ################################################################################
        if self.iniBackupNow == "false":
            try:
                os.listdir(f"{media}/{userName}/{self.iniHDName}")
                # If usb is connected, change notification id to 0 (White color)
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'notification_id', '0')
                    config.write(configfile)

                # Devices was found
                self.connected = True

            except FileNotFoundError:
                try:
                    os.listdir(f"{run}/{userName}/{self.iniHDName}")

                    # If usb is connected, change notification id to 0 (White color)
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w') as configfile:
                        config.set('INFO', 'notification_id', '0')
                        config.write(configfile)

                    # Devices was found
                    self.connected = True

                except FileNotFoundError:
                    try:
                        # Hide backup now button
                        self.backupNowButton.setEnabled(False)
                        # Hide Enter In Time Machine
                        self.enterTimeMachineButton.setEnabled(False)

                        # Change system tray color to red, because not backup device was found or mounted
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_id', '2')
                            config.write(configfile)

                        # Devices was not found
                        self.connected = False

                    except Exception as error:
                        print(error)
                        print("(242)")
                        exit()

        # Condition
        self.conditions()

    def conditions(self):
        # If backup device is registered
        if self.iniHDName != "None":
            # If backup device is connected
            if self.connected:
                # Is not backing up now
                if self.iniBackupNow == "false":
                    # White color
                    self.icon = QIcon(src_system_bar_icon)
                    # Enable backup now button
                    self.backupNowButton.setEnabled(True)
                    # Enable enter in time machine button
                    self.enterTimeMachineButton.setEnabled(True)
                    # Update last backup information
                    self.iniLastBackupInformation.setText(f'Latest Backup to "{(self.iniHDName)}":\n'
                        f'{self.iniLastBackup}')
                    # Add the icon modifications to system tray
                    self.tray.setIcon(self.icon)

                else:
                    # Blue color
                    self.icon = QIcon(src_system_bar_run_icon)
                    # Disable backup now button
                    self.backupNowButton.setEnabled(False)
                    # Update last backup information
                    self.iniLastBackupInformation.setText(f"{(self.iniCurrentBackupInfo)}")
                    # Add the icon modifications to system tray
                    self.tray.setIcon(self.icon)
        
            else:
                # Disable backup now button
                self.backupNowButton.setEnabled(False)
                # Enable enter in time machine button
                # self.enterTimeMachineButton.setEnabled(True)
    
                # If backup device is not connected and automatically if ON
                if self.iniAutomaticallyBackup == "true":
                    # Change system tray red color
                    self.icon = QIcon(src_system_bar_error_icon)
                    # Add the icon modifications to system tray
                    self.tray.setIcon(self.icon)

                else:
                    # Clean notification add info, because auto backup is not enabled
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w') as configfile:
                        config.set('INFO', 'notification_add_info', ' ')
                        config.write(configfile)

                    # Change system tray red color
                    self.icon = QIcon(src_system_bar_icon)
                    # Add the icon modifications to system tray
                    self.tray.setIcon(self.icon)

        else:
            # Update last backup information
            self.iniLastBackupInformation.setText('First, select a backup device.')
            # If backup device is not registered
            # Disable backup now button
            self.backupNowButton.setEnabled(False)
            # Disable enter in time machine button
            self.enterTimeMachineButton.setEnabled(False)

    def backup_now(self):
        sub.Popen(f"python3 {src_backup_now}", shell=True)


main = APP()
