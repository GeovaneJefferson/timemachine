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


class APP:
    def __init__(self):
        self.color = str()
        self.lastestBackup = str()
        self.timeLeftToBackup = str()

        self.alreadySet = False
        self.firstStartup = False

        # Try to acquire a lock for the application
        lock_file = self.acquire_lock()
        if lock_file is None:
            print('Another instance of the application is already running.')
            sys.exit(1)
        
        # create a named pipe
        if not os.path.exists(systemTrayPipeName):
            os.mkfifo(systemTrayPipeName)
        
        self.iniUI()
    
    def iniUI(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationDisplayName(appName)
        self.app.setApplicationName(appName)

        self.begin_settings()

    def begin_settings(self):
        self.firstStartup = True

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

        ################################################################################
        # Read Ini File
        ################################################################################
        timer.timeout.connect(self.updates)
        timer.start(1000)  # update every x second
        self.updates()
        
        self.app.exec()
    
    def updates(self):
        print("System tray is running...")

        if mainIniFile.ini_hd_name() != "None":
            # Only get latest backup information only once, if a new backup is started 
            if self.firstStartup:
                print("Getting latest backup information...")
                self.lastestBackup = f'{str(latest_backup_date_label())}\n'
                self.firstStartup = False

            # Calculate lastest backup 
            try:
                if mainIniFile.ini_backup_now() == 'true':
                    if not self.alreadySet:
                        self.alreadySet = True
                        print("Getting latest backup information...")
                        self.lastestBackup = f'{str(latest_backup_date_label())}\n'
                else:
                    self.alreadySet = False
            except:
                pass

            if mainIniFile.current_second() == 59:
                print("Getting time left to backup information...")
                self.timeLeftToBackup = f'{calculate_time_left_to_backup()}\n'

        self.is_connected()

    def is_connected(self):
        # User has registered a device name
        if str(mainIniFile.ini_hd_name()) != "None":
            if is_connected(str(mainIniFile.ini_hd_name())):
                pass
            #     return "Connected"
            # else:
            #     return "Not Connected"

                # if str(mainIniFile.ini_backup_now()) == "false":
                    # self.change_color("White")
                    # self.backupNowButton.setEnabled(True)
                    # self.browseTimeMachineBackupsButton.setEnabled(True)

                    # TODO
                #     # if calculate_time_left_to_backup() != None:
                #     if self.timeLeftToBackup != "":
                #         print(f'Time left to backup: {self.timeLeftToBackup}')
                #         self.iniLastBackupInformation.setText(f'Next Backup to "{str(mainIniFile.ini_hd_name())}":')
                #         self.iniLastBackupInformation2.setText(self.timeLeftToBackup)
                #     else:
                #         self.iniLastBackupInformation.setText(f'Latest Backup to "{str(mainIniFile.ini_hd_name())}":')
                #         self.iniLastBackupInformation2.setText(self.lastestBackup)
                # else:
                #     self.change_color("Blue")
                #     self.iniLastBackupInformation.setText(f"{str(mainIniFile.ini_current_backup_information())}")
                #     self.iniLastBackupInformation2.setText('')

            # else:
            #     if str(mainIniFile.ini_automatically_backup()) == "true":
            #         self.change_color("Red")
            #         self.backupNowButton.setEnabled(False)
            #         self.browseTimeMachineBackupsButton.setEnabled(False)
            #     else:
            #         self.change_color("White")
                    
                    # if self.iniNotificationID != " ":
                    #     # Clean notification add info, because auto backup is not enabled
                    #     config = configparser.ConfigParser()
                    #     config.read(src_user_config)
                    #     with open(src_user_config, 'w', encoding='utf8') as configfile:
                    #         config.set('INFO', 'notification_add_info', ' ')
                    #         config.write(configfile)
        else:
            self.iniLastBackupInformation.setText('First, select a backup device.')
            self.backupNowButton.setEnabled(False)
            self.browseTimeMachineBackupsButton.setEnabled(False)
            # return "No Device Registered"

        self.check_pipe()

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
                self.tray.setIcon(QIcon(self.systemBarIconStylesheetDetector))
            elif color == "Red":
                self.color = "Red"
                self.tray.setIcon(QIcon(src_system_bar_error_icon))

    def get_lock_file_path(self):
        if sys.platform == 'linux':
            return f'/tmp/myapp_pipe'
        elif sys.platform == 'win32':
            return os.path.join(os.environ['TEMP'], 'myapp_pipe')
        elif sys.platform == 'darwin':
            return os.path.join(os.path.expanduser('~/Library/Application Support'), 'myapp_pipe')

    def acquire_lock(self):
        try:
            lock_file_path = self.get_lock_file_path()
            lock_file = open(lock_file_path, 'w')
            fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lock_file
        except (IOError, OSError):
            return None
    
    def exit(self):
        self.tray.hide()

        # close the named pipe
        os.close("/tmp/system_tray.pipe")
        os.unlink(self.pipe_name)

        # exit the application
        exit()
    
    def tray_icon_clicked(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            self.tray.contextMenu().exec(QCursor.pos())

    def check_pipe(self):
        print("Checking pipes...")
        
        # Check backup now
        try:
            backupNowPipe = os.open("/tmp/backup_now.pipe)", os.O_RDONLY | os.O_NONBLOCK)

            if backupNowPipe:
                data = os.read(backupNowPipe, 1024)
                if data == START_BACKUP_MSG:
                    # Set the system tray icon to indicate that backup is in progress
                    self.change_color("Blue")
                   
                    self.iniLastBackupInformation.setText(f"{str(mainIniFile.ini_current_backup_information())}")
                    self.iniLastBackupInformation2.setText('')

                else:
                    # Set the system tray icon to indicate that backup is complete
                    self.change_color("White")
                    
                    self.backupNowButton.setEnabled(True)
                    self.browseTimeMachineBackupsButton.setEnabled(True)

                    # if calculate_time_left_to_backup() != None:
                    if self.timeLeftToBackup != "":
                        print(f'Time left to backup: {self.timeLeftToBackup}')
                        self.iniLastBackupInformation.setText(f'Next Backup to "{str(mainIniFile.ini_hd_name())}":')
                        self.iniLastBackupInformation2.setText(self.timeLeftToBackup)
                    else:
                        self.iniLastBackupInformation.setText(f'Latest Backup to "{str(mainIniFile.ini_hd_name())}":')
                        self.iniLastBackupInformation2.setText(self.lastestBackup)

        except (OSError, NameError):
            # Handle errors reading from the named pipe
            pass
    
        # Check system tray status
        try:
            systemTrayPipeLocation = os.open("/tmp/system_tray.pipe", os.O_RDONLY | os.O_NONBLOCK)

            if systemTrayPipeLocation:
                data = os.read(systemTrayPipeLocation, 1024)
                if data == b"exit":
                    QtWidgets.QApplication.quit()  # Exit the application
                else:
                    # Handle other messages received over the named pipe
                    pass

        except (OSError, NameError):
            # Handle errors reading from the named pipe
            pass

if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    main = APP()