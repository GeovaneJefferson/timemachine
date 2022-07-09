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
        icon = QIcon(src_system_bar_icon)
        self.tray.setIcon(icon)

        ################################################################################
        # Check ini
        ################################################################################
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

        self.app.exec()

    def updates(self):
        print(f"{appName} system tray is running...")
        try:
            ################################################################################
            # Read ini file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            # INI notification
            self.iniNotification = config['INFO']['notification_id']
            # INI backup now
            self.iniBackupNow = config['BACKUP']['backup_now']
            # INI HD Name
            self.iniHDName = config['EXTERNAL']['name']
            # INI system tray
            self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
            # INI last backup
            self.iniLastBackup = config['INFO']['latest']

            # TEST
            self.iniFolders = config.options('FOLDER')

        except KeyError as error:
            print(error)
            print("Error trying to read user.ini!")
            exit()

        self.condition()

    def condition(self):
        # INI information
        self.iniLastBackupInformation.setText(f"Last backup: {self.iniLastBackup}")

        if self.iniHDName != "None":
            # If iniNotification is 1 (backing up...)
            if self.iniNotification == "0":
                icon = QIcon(src_system_bar_icon)
                self.backupNowButton.setEnabled(True)
            # 0, white color
            elif self.iniNotification == "1":
                icon = QIcon(src_system_bar_run_icon)
                self.backupNowButton.setEnabled(False)
            # 2 or 3, Red color
            elif self.iniNotification == "2" or "3":
                icon = QIcon(src_system_bar_error_icon)
                self.backupNowButton.setEnabled(False)
            # 4, Yellow color
            elif self.iniNotification == "4":
                icon = QIcon(src_system_bar_restore_icon)
                self.backupNowButton.setEnabled(False)

            # Add the icon modifications to system tray icon
            self.tray.setIcon(icon)

            ################################################################################
            # External availability
            ################################################################################
            try:
                os.listdir(f"{media}/{userName}/{self.iniHDName}")  # Opensuse, external is inside "/run"

            except FileNotFoundError:
                try:
                    os.listdir(f"{run}/{userName}/{self.iniHDName}")  # Opensuse, external is inside "/run"

                except FileNotFoundError:
                    # Hide backup now button
                    self.backupNowButton.setEnabled(False)

        # No external found
        else:
            # Disable backup now button
            self.backupNowButton.setEnabled(False)
            # Disable enter in time machine button
            self.enterTimeMachineButton.setEnabled(False)
            
        ################################################################################
        # System Tray
        ################################################################################
        if self.iniSystemTray == "false":
            print("Exit system tray...")
            ################################################################################
            # Write ini file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:  # Set auto backup to true
                config.set('SYSTEMTRAY', 'system_tray', 'false')
                config.write(configfile)
                exit()

        time.sleep(1)

    def backup_now(self):
        ################################################################################
        # Write to ini file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:  # Set auto backup to true
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        sub.Popen(f"python3 {src_backup_now}", shell=True)
        print("Menu bar was successfully enabled!")


main = APP()
