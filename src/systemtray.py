from setup import *

# QTimer
timer = QtCore.QTimer()

class APP:
    def __init__(self):
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)
        app.setApplicationDisplayName(appName)

        # ################################################################################
        # ## Add icon
        # ################################################################################
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(src_system_bar_icon))
        self.tray.setVisible(True)

        # Creating the options
        self.menu = QMenu()

        ################################################################################
        ## Add item on the menu bar
        ################################################################################
        self.iniInformation = QAction()
        self.iniInformation.setEnabled(False)

        self.backupNow = QAction("Back Up Now")
        self.backupNow.setFont(QFont(item))
        self.backupNow.triggered.connect(self.backup_now)

        self.enterTimeMachine = QAction("Enter Time Machine (alpha)")
        self.enterTimeMachine.setFont(QFont(item))
        self.enterTimeMachine.triggered.connect(lambda: sub.run(f"python3 {src_restore_py}", shell=True))
        # self.enterTimeMachine.setEnabled(False)

        self.openSettings = QAction("Open Time Machine Preferences...")
        self.openSettings.setFont(QFont(item))
        self.openSettings.triggered.connect(lambda: sub.run(f"python3 {src_options_py}", shell=True))


        self.menu.addAction(self.iniInformation)
        self.menu.addAction(self.backupNow)
        self.menu.addAction(self.enterTimeMachine)
        self.menu.addAction(self.openSettings)

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)

        ################################################################################
        ## Check ini
        ################################################################################
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

        app.exec()

    def updates(self):
        try:
            ################################################################################
            ## Read ini file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            getBackupNow = config['BACKUP']['backup_now']
            getSystemTray = config['SYSTEMTRAY']['system_tray']
            getLastBackup = config['INFO']['latest']

        except:
            error_reading() # Error trying to read INI file
            exit()

        ################################################################################
        ## INI information
        ################################################################################
        self.iniInformation.setText(f"Last backup: {getLastBackup}")

        ################################################################################
        ## Add icon
        ################################################################################
        if getBackupNow == "true":
            icon = QIcon(src_system_bar_run_icon)
            self.backupNow.setEnabled(False)
        
        elif getBackupNow == "false":
            icon = QIcon(src_system_bar_icon)
            self.backupNow.setEnabled(True)

        else:
            icon = QIcon(src_system_bar_icon)

        self.tray.setIcon(icon)

        print(f"{appName} system tray is running...")

        ################################################################################
        ## System Tray
        ################################################################################
        if getSystemTray == "false":
            print("Exit system tray...")
            ################################################################################
            ## Write ini file
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
        ## Write to ini file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:  # Set auto backup to true
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        sub.Popen(f"python3 {src_backup_now}", shell=True)
        print("Menu bar was successfully enabled!")


main = APP()
