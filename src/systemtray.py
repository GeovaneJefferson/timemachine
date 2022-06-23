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
        self.enterTimeMachineButton.triggered.connect(lambda: sub.run(f"python3 {src_restore_py}", shell=True))
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
            # INI backup now
            self.iniBackupNow = config['BACKUP']['backup_now']
            # INI HD Name
            self.iniHDName = config['EXTERNAL']['name']
            # INI system tray
            self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
            # INI last backup
            self.iniLastBackup = config['INFO']['latest']

        except:
            ################################################################################
            # Set notification_id to 5
            ################################################################################
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "5")
                config.write(configfile)

            print("Error trying to read user.ini!")
            sub.Popen(f"python3 {src_notification}", shell=True)  # Call notification
            exit()

        self.condition()

    def condition(self):
        # INI information
        self.iniLastBackupInformation.setText(f"Last backup: {self.iniLastBackup}")
        # No external found
        if self.iniHDName == "None":
            self.backupNowButton.setEnabled(False)

        # Condition Backup Now and Icon
        if self.iniBackupNow == "true" and self.iniHDName != "None":
            icon = QIcon(src_system_bar_run_icon)
            self.backupNowButton.setEnabled(False)
        
        elif self.iniBackupNow == "false" and self.iniHDName != "None":
            icon = QIcon(src_system_bar_icon)
            self.backupNowButton.setEnabled(True)

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
