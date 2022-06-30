#! /usr/bin/python3
from setup import *

################################################################
# Window management
################################################################
windowXSize = 900
windowYSize = 600

################################################################################
# Read INI file
################################################################################
config = configparser.ConfigParser()
config.read(src_user_config)


class WELCOME(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.widgets()

    def widgets(self):
        # Layout V
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        # Welcome
        self.title = QLabel()
        self.title.setFont(QFont("Ubuntu", 34))
        self.title.setText(
        "Welcome to your\n"
        f"Personal OS")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        # # Image
        # self.image = QLabel()
        # self.image.setFixedSize(89, 89)
        # self.image.setStyleSheet(
        #     "QLabel"
        #         "{"
        #             f"background-image: url({src_restore_icon});"
        #             "background-position: center;"
        #         "}")

        ################################################################################
        # Buttons
        ################################################################################
        # Buttons layout
        self.horizontalLayoutWidget = QWidget()
        self.horizontalLayoutWidget.setFixedSize(140, 40)

        # Continue button
        self.continueButton = QPushButton(self.horizontalLayoutWidget)
        self.continueButton.setText("Continue")
        self.continueButton.setFont(QFont("Ubuntu", 11))
        self.continueButton.setFixedSize(120, 34)
        self.continueButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()+1))
        self.continueButton.setStyleSheet(
            "QPushButton"
            "{"
            "color: white;"
            "background-color: rgba(20, 110, 255, 1);"
            "border-radius: 10px;"
            "border: 0px"
            "}"
            "QPushButton:hover"
            "{"
            "background-color: rgba(162, 167, 175, 1);"
            "}")

         # Add stuff

        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.verticalLayout.addWidget(self.image, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.horizontalLayoutWidget, 1, QtCore.Qt.AlignRight)

        self.setLayout(self.verticalLayout)


class START(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ################################################################################
        # Layout
        ################################################################################
        # V layout
        self.baseVlayout = QVBoxLayout()
        self.baseVlayout.setSpacing(20)
        self.baseVlayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Grid layout
        self.baseGridlayout = QGridLayout()
        self.baseGridlayout.setSpacing(20)
        self.baseGridlayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # Apps and Data
        self.title = QLabel()
        self.title.setFont(QFont("Ubuntu", 18))
        self.title.setText("Apps & Data")
        self.title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # Question
        self.question = QLabel()
        self.question.setFont(QFont("Ubuntu", 24))
        self.question.setAlignment(QtCore.Qt.AlignHCenter)
        self.question.setText("What are you planning to do?")

        # Description
        self.description = QLabel()
        self.description.setFont(QFont("Ubuntu", 11))
        self.description.setAlignment(QtCore.Qt.AlignHCenter)
        self.description.setText(
            f"If you already have back up with {appName}\n"
            "You can use the restore option.")

        # Restore from
        self.restoreFrom = QPushButton()
        self.restoreFrom.setText(
            "Restore\n"
            f"from {appName}")
        self.restoreFrom.setFont(QFont("Ubuntu", 12))
        self.restoreFrom.setFixedSize(250, 250)
        self.restoreFrom.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()+1))
        self.restoreFrom.setStyleSheet(
            "QPushButton"
                "{"
                    "color: white;"
                    "background-color: rgb(36, 37, 38);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(58, 59, 60);"
                "}"
            "QPushButton::checked"
                "{"
                    "background-color: rgb(24, 25, 26);"
                    "border: 1px solid white;"
                    "border-radius: 5px;"
                "}")

        # Set up as new
        self.startAsNew = QPushButton()
        self.startAsNew.setFont(QFont("Ubuntu", 12))
        self.startAsNew.setText("Set Up as New")
        # self.startAsNew.setCheckable(True)
        # self.startAsNew.setAutoExclusive(True)
        self.startAsNew.setFixedSize(250, 250)
        self.startAsNew.clicked.connect(lambda: exit())
        self.startAsNew.setStyleSheet(
            "QPushButton"
                "{"
                    "color: white;"
                    "background-color: rgb(36, 37, 38);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(58, 59, 60);"
                "}"
            "QPushButton::checked"
                "{"
                    "background-color: rgb(24, 25, 26);"
                    "border: 1px solid white;"
                    "border-radius: 5px;"
                "}")

        ################################################################################
        # Add layout and widgets
        ################################################################################
        self.baseVlayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.baseVlayout.addWidget(self.question, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.baseVlayout.addWidget(self.description, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Grid layout
        self.baseGridlayout.addWidget(self.restoreFrom, 1, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.baseGridlayout.addWidget(self.startAsNew, 1, 1)
        self.baseVlayout.addLayout(self.baseGridlayout, 0)
        self.setLayout(self.baseVlayout)


class RESTORE(QWidget):
    def __init__(self):
        super().__init__()
        self.read_ini_file()

    def read_ini_file(self):
        ################################################################################
        # Read file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniExternalLocation = config['EXTERNAL']['hd']

        self.iniApplicationNames = config['RESTORE']['applications_name']
        self.iniApplicationData = config['RESTORE']['application_data']
        self.iniFilesAndsFolders = config['RESTORE']['files_and_folders']

        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        # Buttons layout
        self.horizontalLayoutWidget = QWidget()
        self.horizontalLayoutWidget.setFixedSize(240, 50)
        self.horizontalLayoutWidget.setContentsMargins(0, 0, 20, 20)
 
        self.horizontalButtonLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalButtonLayout.setSpacing(20)

        # Title
        self.title = QLabel()
        self.title.setFont(QFont("Ubuntu", 24))
        self.title.setText("Select the information to restore")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        # Description
        self.description = QLabel()
        self.description.setFont(QFont("Ubuntu", 11))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText("Choose which information you´d like to restore to this pc")

        ################################################################################
        # Restore
        ################################################################################
        # Restore widget
        self.restorekWidget = QWidget()
        self.restorekWidget.setFixedSize(400, 250)
        self.restorekWidget.setStyleSheet(
            "QWidget"
            "{"
            "border-radius: 5px;"
            "background-color: rgb(56, 57, 58);"
            "}")
        
        ################################################################################
        # Application checkbox (Installed names)
        ################################################################################
        self.applicationNamesCheckBox = QCheckBox(self.restorekWidget)
        self.applicationNamesCheckBox.setText(" Applications")
        self.applicationNamesCheckBox.setFont(QFont("Ubuntu", 11))
        self.applicationNamesCheckBox.move(20, 10)
        self.applicationNamesCheckBox.clicked.connect(self.on_application_names_clicked)
        self.applicationNamesCheckBox.setStyleSheet(
            "QCheckBox"
            "{"
            "color: white;"
            "}")

        # Get folder size
        self.applicationNamesSize = os.popen(f"du -hs {self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}")
        self.applicationNamesSize = self.applicationNamesSize.read().strip("\t").strip("\n").replace(f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}", "").replace("\t", "")

        # Application size information
        self.applicationSizeInformation = QLabel(self.restorekWidget)
        if "M" in self.applicationNamesSize:
            self.applicationSizeInformation.setText(f"{self.applicationNamesSize}B")
        else:
            self.applicationSizeInformation.setText(f"{self.applicationNamesSize}")
        
        self.applicationSizeInformation.setFont(QFont("Ubuntu", 10))
        self.applicationSizeInformation.adjustSize()
        self.applicationSizeInformation.move(320, 12)
        self.applicationSizeInformation.setStyleSheet(
            "QLabel"
            "{"
            "color: white;"
            "}")
        
        ################################################################################
        # Application checkbox (DATA)
        ################################################################################
        self.applicationDataCheckBox = QCheckBox(self.restorekWidget)
        self.applicationDataCheckBox.setText(" Applications (Data)")
        self.applicationDataCheckBox.setFont(QFont("Ubuntu", 11))
        self.applicationDataCheckBox.move(20, 40)
        self.applicationDataCheckBox.clicked.connect(self.on_application_data_clicked)
        self.applicationDataCheckBox.setStyleSheet(
            "QCheckBox"
            "{"
            "color: white;"
            "}")

        # Get folder size
        self.applicationDataSize = os.popen(f"du -hs {self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}")
        self.applicationDataSize = self.applicationDataSize.read().strip("\t").strip("\n").replace(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}", "").replace("\t", "")
 
        # Application size information
        self.applicationSizeInformation = QLabel(self.restorekWidget)
        if "M" in self.applicationDataSize:
            self.applicationSizeInformation.setText(f"{self.applicationDataSize}B")
        else:
            self.applicationSizeInformation.setText(f"{self.applicationDataSize}")
        
        self.applicationSizeInformation.setFont(QFont("Ubuntu", 10))
        self.applicationSizeInformation.adjustSize()
        self.applicationSizeInformation.move(320, 42)
        self.applicationSizeInformation.setStyleSheet(
            "QLabel"
            "{"
            "color: white;"
            "}")
        
        ################################################################################
        # Files & Folders checkbox
        ################################################################################
        self.fileAndFoldersCheckBox = QCheckBox(self.restorekWidget)
        self.fileAndFoldersCheckBox.setText(" File and Folders")
        self.fileAndFoldersCheckBox.setFont(QFont("Ubuntu", 11))
        self.fileAndFoldersCheckBox.move(20, 70)
        self.fileAndFoldersCheckBox.setStyleSheet(
            "QCheckBox"
            "{"
            "color: white;"
            "}")
        self.fileAndFoldersCheckBox.clicked.connect(self.on_files_and_folders_clicked)

        # Get folder size
        self.fileAndFoldersFolderSize = os.popen(f"du -hs {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/")
        self.fileAndFoldersFolderSize = self.fileAndFoldersFolderSize.read().strip("\t").strip("\n").replace(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/", "").replace("\t", "")
        
        self.fileAndFoldersFolder = QLabel(self.restorekWidget)
        if "K" in self.fileAndFoldersFolderSize:
            self.fileAndFoldersFolder.setText(f"{self.fileAndFoldersFolderSize}B")
        else:
            self.fileAndFoldersFolder.setText(f"{self.fileAndFoldersFolderSize}")
            
        self.fileAndFoldersFolder.setFont(QFont("Ubuntu", 10))
        self.fileAndFoldersFolder.adjustSize()
        self.fileAndFoldersFolder.move(320, 72)
        self.fileAndFoldersFolder.setStyleSheet(
            "QLabel"
            "{"
            "color: white;"
            "}")

        ################################################################################
        # User information
        ################################################################################
        self.userSizeInformation = QLabel(self.restorekWidget)
        self.userSizeInformation.setFont(QFont("Ubuntu", 10))
        self.userSizeInformation.adjustSize()
        self.userSizeInformation.move(320, 102)
        self.userSizeInformation.setStyleSheet(
            "QLabel"
            "{"
            "color: white;"
            "}")
        
        ################################################################################
        # Wallpaper checkbox
        ################################################################################
        self.wallpaperCheckBox = QCheckBox(self.restorekWidget)
        self.wallpaperCheckBox.setText(" Wallpaper")
        self.wallpaperCheckBox.setFont(QFont("Ubuntu", 11))
        self.wallpaperCheckBox.move(20, 100)
        self.wallpaperCheckBox.setStyleSheet(
            "QCheckBox"
            "{"
            "color: white;"
            "}")

        # Application size information
        self.wallpaperSizeInformation = QLabel(self.restorekWidget)
        self.wallpaperSizeInformation.setText("32 KB")
        self.wallpaperSizeInformation.setFont(QFont("Ubuntu", 10))
        self.wallpaperSizeInformation.adjustSize()
        self.wallpaperSizeInformation.move(320, 102)
        self.wallpaperSizeInformation.setStyleSheet(
            "QLabel"
            "{"
            "color: white;"
            "}")

        ################################################################################
        # Texts
        ################################################################################
        # Back button
        self.backButton = QPushButton()
        self.backButton.setText("Back")
        self.backButton.setFont(QFont("Ubuntu", 11))
        self.backButton.setFixedSize(80, 34)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))
        self.backButton.setStyleSheet(
            "QPushButton"
            "{"
            "color: white;"
            "background-color: gray;"
            "border-radius: 10px;"
            "border: 0px"
            "}"
            "QPushButton:hover"
            "{"
            "background-color: rgba(162, 167, 175, 1);"
            "}")

        # Continue button
        self.continueButton = QPushButton()
        self.continueButton.setText("Continue")
        self.continueButton.setFont(QFont("Ubuntu", 11))
        self.continueButton.setFixedSize(120, 34)
        self.continueButton.clicked.connect(self.restore_data)
        self.continueButton.setStyleSheet(
            "QPushButton"
            "{"
            "color: white;"
            "background-color: rgba(20, 110, 255, 1);"
            "border-radius: 10px;"
            "border: 0px"
            "}"
            "QPushButton:hover"
            "{"
            "background-color: rgba(162, 167, 175, 1);"
            "}")
        
        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addStretch()

        # horizontalLayout
        self.verticalLayout.addWidget(self.restorekWidget, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addStretch()
        self.horizontalButtonLayout.addWidget(self.backButton, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)
        self.horizontalButtonLayout.addWidget(self.continueButton, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)

        self.verticalLayout.addWidget(self.horizontalLayoutWidget, 1, QtCore.Qt.AlignRight)
        self.setLayout(self.verticalLayout)

        self.conditions()

    def conditions(self):
        ################################################################################
        # Something inside?
        ################################################################################
        try:
            # Check flatpak names to install
            with open(f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}", 'r') as output:
                output = output.read()
                # If is empty, disable this option
                if output != "":
                    self.applicationNamesCheckBox.setEnabled(True)
                    self.applicationNamesCheckBox.setChecked(True)
                    self.applicationNamesCheckBox.setStyleSheet(
                        "QCheckBox"
                        "{"
                        "color: white;"
                        "}")

                    with open(src_user_config, 'w') as configfile:
                        config.set('RESTORE', 'applications_name', 'true')
                        config.write(configfile)

                else:
                    self.applicationNamesCheckBox.setEnabled(False)  
                    self.applicationNamesCheckBox.setChecked(False)
                    self.applicationNamesCheckBox.setStyleSheet(
                        "QCheckBox"
                        "{"
                        "color: gray;"
                        "}")
                
                    with open(src_user_config, 'w') as configfile:
                        config.set('RESTORE', 'applications_name', 'false')
                        config.write(configfile)
        except:
            pass

        ################################################################################
        # Check inside backup flatpak data (var)
        # There is not need to check (share) inside External
        # If Var is empty, just pass this options
        try:
            dummyList = []
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{varFolderName}/"):
                dummyList.append(output)
        except:
            pass

        if dummyList:
            self.applicationDataCheckBox.setEnabled(True)
            self.applicationDataCheckBox.setChecked(True)
            self.applicationDataCheckBox.setStyleSheet(
                "QCheckBox"
                "{"
                "color: white;"
                "}")
                
            with open(src_user_config, 'w') as configfile:
                config.set('RESTORE', 'application_data', 'true')
                config.write(configfile)

        else:
            print("Empty application data")
            self.applicationDataCheckBox.setEnabled(False)  
            self.applicationDataCheckBox.setChecked(False)
            self.applicationDataCheckBox.setStyleSheet(
                "QCheckBox"
                "{"
                "color: gray;"
                "}")
        
            with open(src_user_config, 'w') as configfile:
                config.set('RESTORE', 'application_data', 'false')
                config.write(configfile)

        # Empty list
        dummyList.clear()
        
        ################################################################################
        try:
            # Check inside backup folder 
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"):
                dummyList.append(output)
        except:
            pass

        if dummyList:
            self.fileAndFoldersCheckBox.setEnabled(True)
            self.fileAndFoldersCheckBox.setChecked(True)
            self.fileAndFoldersCheckBox.setStyleSheet(
                "QCheckBox"
                "{"
                "color: White;"
                "}")    

            with open(src_user_config, 'w') as configfile:
                if self.fileAndFoldersCheckBox.isChecked():
                    config.set('RESTORE', 'files_and_folders', 'true')
                    config.write(configfile)

        else:
            self.fileAndFoldersCheckBox.setEnabled(False)  
            self.fileAndFoldersCheckBox.setChecked(False)
            self.fileAndFoldersCheckBox.setStyleSheet(
                "QCheckBox"
                "{"
                "color: Gray;"
                "}")
            
            with open(src_user_config, 'w') as configfile:
                config.set('RESTORE', 'files_and_folders', 'false')
                config.write(configfile)

        # Empty list
        dummyList.clear()
        
        # self.flatpak()

    def flatpak(self):
        # Flatpak list
        try:
            count = 10
            with open(f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}", "r") as write_file:
                for item in write_file:
                    print(f"{(item.strip())}")
                    output = QLabel(self.restorekWidget)
                    output.setText(item)
                    output.setFont(QFont("Ubuntu", 11))
                    output.setFixedSize(200, 34)
                    output.move(20, count)
                    output.setAlignment(QtCore.Qt.AlignVCenter)
                    output.setStyleSheet(
                        "QLabel"
                        "{"
                        "color: white;"
                        "}")
                    count += 20

        except FileNotFoundError:
            print("No flatpak file found")
            pass

    def restore_data(self):
        sub.Popen(f"python3 {homeUser}/.local/share/timemachine/src/welcome_screen_cmd.py", shell=True)
        exit()

    ################################################################################
    # Write to INI file
    ################################################################################
    def on_application_names_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.applicationNamesCheckBox.isChecked():
                config.set('RESTORE', 'applications_name', 'true')
            else:
                config.set('RESTORE', 'applications_name', 'false')

            config.write(configfile)

    def on_application_data_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.applicationDataCheckBox.isChecked():
                config.set('RESTORE', 'application_data', 'true')
            else:
                config.set('RESTORE', 'application_data', 'false')

            config.write(configfile)

    def on_files_and_folders_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.fileAndFoldersCheckBox.isChecked():
                config.set('RESTORE', 'files_and_folders', 'true')
            else:
                config.set('RESTORE', 'files_and_folders', 'false')

            config.write(configfile)


app = QApplication(sys.argv)
main = WELCOME()
main2 = START()
main3 = RESTORE()

widget = QStackedWidget()
widget.addWidget(main)   # create an instance of the first page class and add it to stackedwidget
widget.addWidget(main2)   # adding second page
widget.addWidget(main3)   # adding second page
widget.setCurrentWidget(main)   # setting the page that you want to load when application starts up. you can also use setCurrentIndex(int)

widget.setWindowTitle(appName)
widget.setWindowIcon(QIcon(src_restore_icon))
widget.setFixedSize(windowXSize, windowYSize)

widget.show()

app.exit(app.exec())
