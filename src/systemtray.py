from setup import *

# QTimer
timer = QtCore.QTimer()

class APP:
    def start(self):
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)
        app.setApplicationDisplayName(app_name)
        
        # ################################################################################
        # ## Add icon
        # ################################################################################
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(src_system_bar_icon))
        self.tray.setVisible(True)

        ################################################################################
        ## Add item on the menu bar
        ################################################################################
        # Creating the options
        menu = QMenu()

        self.iniInformation = QAction()
        self.iniInformation.setEnabled(False)

        openSettings = QAction("Open Time Machine Preferences...")
        openSettings.setFont(QFont(item))
        openSettings.triggered.connect(lambda: sub.run(f"python3 {src_options_py}", shell=True))

        enterTimeMachine = QAction("'Enter Time Machine' Coming soon...")
        enterTimeMachine.setFont(QFont(item))
        enterTimeMachine.triggered.connect(lambda: sub.run(f"python3 {src_restore_py}", shell=True))
        enterTimeMachine.setEnabled(False)

        backupNow = QAction("Back Up Now")
        backupNow.setFont(QFont(item))
        backupNow.triggered.connect(self.backup_now)

        menu.addAction(self.iniInformation)
        menu.addAction(openSettings)
        menu.addAction(enterTimeMachine)
        menu.addAction(backupNow)

        # # To quit the app
        # quit = QAction("Quit")
        # quit.triggered.connect(app.quit)
        # menu.addAction(quit)

        # Adding options to the System Tray
        self.tray.setContextMenu(menu)

        ################################################################################
        ## Check ini
        ################################################################################
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every second
        self.updates()

        app.exec()

    def updates(self):
        ################################################################################
        ## Read ini file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        getBackupNow = config['BACKUP']['backup_now']
        getSystemTray = config['SYSTEMTRAY']['system_tray']
        getLastBackup = config['INFO']['latest']

        ################################################################################
        ## INI information
        ################################################################################
        self.iniInformation.setText(f"Last backup: {getLastBackup}")

        ################################################################################
        ## Add icon
        ################################################################################
        if getBackupNow == "true":
            icon = QIcon(src_system_bar_run_icon)
        
        elif getBackupNow == "false":
            icon = QIcon(src_system_bar_icon)

        else:
            icon = QIcon(src_system_bar_icon)

        self.tray.setIcon(icon)

        print(f"{app_name} system tray is running...")

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

        sub.run(f"python3 {src_backup_now}", shell=True)

        print("Menu bar was successfully enabled!")


main = APP()
main.start()
