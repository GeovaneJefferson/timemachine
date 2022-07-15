#! /usr/bin/python3
from setup import *

# QTimer
timer = QtCore.QTimer()


class APP:
    def __init__(self):
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
        self.iniLastBackupInformation.setEnabled(False)

        # Backup now button
        self.backupNowButton = QAction("Back Up Now")
        self.backupNowButton.setFont(QFont(item))
        self.backupNowButton.triggered.connect(self.backup_now)

        # Enter time machine button
        self.enterTimeMachineButton = QAction("Enter Time Machine")
        self.enterTimeMachineButton.setFont(QFont(item))
        self.enterTimeMachineButton.triggered.connect(lambda: sub.run(f"python3 {src_enter_time_machine_py}", shell=True))

        # Open settings button
        self.openSettingsButton = QAction("Open Time Machine Preferences...")
        self.openSettingsButton.setFont(QFont(item))
        self.openSettingsButton.triggered.connect(lambda: sub.run(f"python3 {src_options_py}", shell=True))

        # Add all to menu
        self.menu.addAction(self.iniLastBackupInformation)
        self.menu.addAction(self.backupNowButton)
        self.menu.addAction(self.enterTimeMachineButton)
        self.menu.addAction(self.openSettingsButton)

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)

        # Tray
        self.icon = QIcon(src_system_bar_icon)
        self.tray.setIcon(self.icon)

        ################################################################################
        # Check ini
        ################################################################################
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every x second
        self.updates()

        self.app.exec()

    def updates(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # Backup now
            self.iniBackupNow = config['BACKUP']['backup_now']
            # INI notification
            self.iniNotification = config['INFO']['notification_id']
            # INI HD Name
            self.iniHDName = config['EXTERNAL']['name']
            # INI system tray
            self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
            # INI last backup
            self.iniLastBackup = config['INFO']['latest']

        except KeyError as error:
            print(error)
            print("System Tray KeyError!")
            exit()

        self.load_system_tray()
    
    def load_system_tray(self):
        if self.iniSystemTray == "false":
            print("Exiting system tray...")
            # Write ini file
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:  
                config.set('SYSTEMTRAY', 'system_tray', 'false')
                config.write(configfile)

            exit()

        self.conditions()

    def conditions(self):
        # INI information
        self.iniLastBackupInformation.setText(f"Last backup: {self.iniLastBackup}")

        if self.iniHDName != "None":
            # TODO
            if self.iniBackupNow == "false":
                # White color
                self.icon = QIcon(src_system_bar_icon)
                # Enable backup now button
                self.backupNowButton.setEnabled(True)
                # Enable enter in time machine button
                self.enterTimeMachineButton.setEnabled(True)

            else:
                # Blue color
                self.icon = QIcon(src_system_bar_run_icon)
                self.backupNowButton.setEnabled(False)

            # Add the icon modifications to system tray
            self.tray.setIcon(self.icon)
            # TODO

        else:
            # Disable backup now button
            self.backupNowButton.setEnabled(False)
            # Disable enter in time machine button
            self.enterTimeMachineButton.setEnabled(False)
        
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

            except FileNotFoundError:
                try:
                    os.listdir(f"{run}/{userName}/{self.iniHDName}") 

                    # If usb is connected, change notification id to 0 (White color)
                    config = configparser.ConfigParser()
                    config.read(src_user_config)
                    with open(src_user_config, 'w') as configfile: 
                        config.set('INFO', 'notification_id', '0')
                        config.write(configfile)

                except FileNotFoundError:
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

    def backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:  
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        sub.Popen(f"python3 {src_backup_now}", shell=True)


main = APP()
