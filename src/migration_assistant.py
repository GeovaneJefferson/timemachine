#! /usr/bin/python3
from setup import *

# QTimer
timer = QtCore.QTimer()

################################################################
# Window management
################################################################
windowXSize = 900
windowYSize = 600

################################################################################
# Read INI file
################Box################################################################
config = configparser.ConfigParser()
config.read(src_user_config)


class WELCOMESCREEN(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.widgets()

    def widgets(self):
        # Title layout
        self.titlelLayout = QVBoxLayout()
        self.titlelLayout.setSpacing(20)
        self.titlelLayout.setContentsMargins(20, 20, 20, 20)
        
        # Image       
        image = QLabel()
        image.setFixedSize(128, 128)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_backup_icon});"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")
        
        # Welcome
        self.title = QLabel()
        self.title.setFont(QFont("Ubuntu", 34))
        self.title.setText("Migration Assistant")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

       # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont("Ubuntu", 11))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText("Use Migration Assistant to transfer information such as "
            "(Apps, Data, Files and Folders) to this PC.") 

        ################################################################################
        # Buttons
        ################################################################################
        # Continue button
        self.continueButton = QPushButton(self)
        self.continueButton.setText("Continue")
        self.continueButton.setFont(QFont("Ubuntu", 10))
        self.continueButton.adjustSize()
        self.continueButton.move(800, 555)
        self.continueButton.clicked.connect(lambda: widget.setCurrentIndex(widget.currentIndex()+1))

        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        self.titlelLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.titlelLayout.addWidget(image, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titlelLayout.addWidget(self.moreDescription, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.setLayout(self.titlelLayout)

class CHOOSEDEVICE(QWidget):
    def __init__(self):
        super().__init__()
        self.foundInMedia = None
        self.outputBox = ()
        self.captureDevices = []

        self.read_ini_file()

    def read_ini_file(self):
        ################################################################################
        # Read file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Read INI file
        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniHDName = config['EXTERNAL']['name']
        self.iniApplicationsPackages = config['RESTORE']['applications_packages']
        self.iniApplicationData = config['RESTORE']['applications_data']
        self.iniFilesAndsFolders = config['RESTORE']['files_and_folders']

        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        # Title
        self.title = QLabel()
        self.title.setFont(QFont("Ubuntu Bold", 28))
        self.title.setText("Transfer information to this pc")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        # Description
        self.description = QLabel()
        self.description.setFont(QFont("Ubuntu", 11))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Select a {appName} " 
            "disk to transfer it's information to this PC.")

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont("Ubuntu", 11))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText(f"Make sure that your External device " 
            f"with a {appName} backup is connected to this PC.")

        ################################################################################
        # Devices Area
        ################################################################################
        self.devicesAreadWidget = QWidget()
        self.devicesAreadWidget.setFixedSize(700, 200)

        # Device layout
        self.devicesAreaLayout = QHBoxLayout(self.devicesAreadWidget)
        
        ################################################################################
        # Buttons
        ################################################################################
        # Back button
        self.backButton = QPushButton(self)
        self.backButton.setText("Back")
        self.backButton.setFont(QFont("Ubuntu", 10))
        self.backButton.adjustSize()
        self.backButton.move(700, 555)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))
        
        # Continue button
        self.continueButton = QPushButton(self)
        self.continueButton.setText("Continue")
        self.continueButton.setFont(QFont("Ubuntu", 10))
        self.continueButton.adjustSize()
        self.continueButton.move(800, 555)
        self.continueButton.setEnabled(False)
        self.continueButton.clicked.connect(self.on_continue_clicked)
        
        # Update
        timer.timeout.connect(self.check_connection)
        timer.start(2000) # Update every x seconds
        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside media
        ################################################################################
        try:
            if os.listdir(f'{media}/{userName}'):
                self.foundInMedia = True
                self.show_on_screen(media)

            else:
                for i in range(len(self.captureDevices)):
                    item = self.devicesAreaLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1
                
        except FileNotFoundError:
            try:
                if os.listdir(f'{run}/{userName}'):
                    self.foundInMedia = False
                    self.show_on_screen(run)
                else:
                    for i in range(len(self.captureDevices)):
                        item = self.devicesAreaLayout.itemAt(i)
                        widget = item.widget()
                        widget.deleteLater()
                        i -= 1
                    
            except Exception:
                print("No device found...")
                pass

        self.show_on_screen(None)

    def show_on_screen(self, location):
        ################################################################################
        # Check source
        ################################################################################
        if self.foundInMedia:
            self.foundWhere = media
        else:
            self.foundWhere = run

        ################################################################################
        # Show available files
        ################################################################################
        try:
            count = 0
            for output in os.listdir(f"{location}/{userName}/"):
                # Only show disk the have baseFolderName inside
                if baseFolderName in os.listdir(f"{location}/{userName}/{output}/"):
                    if output not in self.captureDevices:
                        # If device is in list, display to user just on time per device
                        self.captureDevices.append(output)

                        self.availableDevices = QPushButton(self.devicesAreadWidget)
                        self.availableDevices.setCheckable(True)
                        self.availableDevices.setAutoExclusive(True)
                        self.availableDevices.setFixedSize(180, 180)
                        self.availableDevices.setText(output)
                        self.availableDevices.adjustSize()
                        self.availableDevices.clicked.connect(lambda *args, output=output: self.on_device_clicked(output))
                        self.availableDevices.setFont(QFont("Ubuntu", 11))
                        self.availableDevices.setStyleSheet(
                            "QPushButton"
                            "{"
                            "text-align: bottom;"
                            "padding-bottom: 25px;"
                            "}")
                        
                        # Image
                        image = QLabel(self.availableDevices)
                        image.setFixedSize(96, 96)
                        image.move(40, 35)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({src_restore_icon});"
                            "background-repeat: no-repeat;"
                            "background-color: transparent;"
                            "}")

                        self.devicesAreaLayout.addWidget(self.availableDevices)
            
                    # If x device is removed or unmounted, remove from screen
                    for output in self.captureDevices:
                        if output not in os.listdir(f'{location}/{userName}'):
                            # Current output index
                            index = self.captureDevices.index(output)
                            # Remove from list
                            self.captureDevices.remove(output)             
                            # Delete from screen
                            item = self.devicesAreaLayout.itemAt(index)
                            widget = item.widget()
                            widget.deleteLater()
                            index -= 1

        except Exception:
            pass

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addWidget(self.devicesAreadWidget, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.moreDescription, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.setLayout(self.verticalLayout)

    def on_continue_clicked(self):
        # Enable continue button
        self.continueButton.setEnabled(True)
        # Adapt external name is it has space in the name
        if " " in self.outputBox:
            self.outputBox = str(self.outputBox.replace(" ", "\ "))

        ################################################################################
        # Update INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        with open(src_user_config, 'w') as configfile:
            config.set(f'EXTERNAL', 'hd', f'{self.foundWhere}/{userName}/{self.outputBox}')
            config.set('EXTERNAL', 'name', f'{self.outputBox}')
            config.write(configfile)

        # Go to next window 
        widget.setCurrentIndex(widget.currentIndex()+1)

    def on_device_clicked(self, output):
        # If user has clicked on one device
        if self.availableDevices.isChecked():
            self.outputBox = output
            # Enable use disk button
            self.continueButton.setEnabled(True)
        else:
            # If deselected, empty self.outputBox
            self.outputBox = ""
            # Disable use disk button
            self.continueButton.setEnabled(False)

class OPTIONS(QWidget):
    def __init__(self):
        super().__init__()
        self.outputBox = ()
        self.initUI()

    def initUI(self):
        ################################################################################
        # Layouts
        ################################################################################
        # Vertical layout
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Grid layout
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(20)
        self.gridLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # Title
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
        self.restoreOption = QPushButton()
        self.restoreOption.setText(
            "Restore\n"
            f"from {appName}")
        self.restoreOption.setFont(QFont("Ubuntu", 11))
        self.restoreOption.setCheckable(True)
        self.restoreOption.setAutoExclusive(True)
        self.restoreOption.setFixedSize(200, 200)
        self.restoreOption.clicked.connect(lambda *args: self.on_device_clicked("restore"))
        
        # Set up as new
        self.startAsNew = QPushButton()
        self.startAsNew.setFont(QFont("Ubuntu", 11))
        self.startAsNew.setText("Set Up as New")
        self.startAsNew.setCheckable(True)
        self.startAsNew.setAutoExclusive(True)
        self.startAsNew.setFixedSize(200, 200)
        self.startAsNew.clicked.connect(lambda *args: self.on_device_clicked("new"))
       
        ################################################################################
        # Buttons
        ################################################################################
        # Back button
        self.backButton = QPushButton(self)
        self.backButton.setText("Back")
        self.backButton.setFont(QFont("Ubuntu", 10))
        self.backButton.adjustSize()
        self.backButton.move(700, 555)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))

        # Continue button
        self.continueButton = QPushButton(self)
        self.continueButton.setText("Continue")
        self.continueButton.setFont(QFont("Ubuntu", 10))
        self.continueButton.adjustSize()
        self.continueButton.move(800, 555)
        self.continueButton.setEnabled(False)
        self.continueButton.clicked.connect(self.on_continue_clicked)

        ################################################################################
        # Add layout and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.question, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.description, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Grid layout
        self.gridLayout.addWidget(self.restoreOption, 1, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.startAsNew, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout, 0)
        
        self.setLayout(self.verticalLayout)

    def on_continue_clicked(self):
        # If user clicked on restore from...
        if self.outputBox == "restore":
            widget.setCurrentIndex(widget.currentIndex()+1)

        # If user do not want to restore
        else:
            exit()

    def on_device_clicked(self, output):
        # Add output to self.outputBox
        self.outputBox = output
        # Enable or disable continue button
        if self.restoreOption.isChecked() or self.startAsNew.isChecked():
            # Enable continue
            self.continueButton.setEnabled(True)
        else:
            # Clean self.ouputBox
            self.outputBox = ""
            # Disable continue
            self.continueButton.setEnabled(False)

class PREBACKUP(QWidget):
    def __init__(self):
        super().__init__()
        self.outputBox = []
        self.read_ini_file()

    def read_ini_file(self):
        ################################################################################
        # Read file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        # Read INI file
        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniApplicationsPackages = config['RESTORE']['applications_packages']
        self.iniApplicationData = config['RESTORE']['applications_data']
        self.iniFilesAndsFolders = config['RESTORE']['files_and_folders']
        # INFO
        self.packageManager = config['INFO']['packageManager']
        # Flatpak txt file
        self.flatpakTxtFile = f"{self.iniExternalLocation}/{baseFolderName}/{flatpakTxt}"

        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        # Restore widget
        self.optionskWidget = QWidget()
        self.optionskWidget.setFixedSize(300, 300)

        # Vertical base layout
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        # Vertical options layout
        self.verticalLayoutForOptions = QVBoxLayout(self.optionskWidget)
        self.verticalLayoutForOptions.setSpacing(5)
        self.verticalLayoutForOptions.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignTop)
        self.verticalLayoutForOptions.setContentsMargins(20, 20, 20, 20)

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
        # Wallpaper checkbox
        ################################################################################
        self.wallpaperCheckBox = QCheckBox()
        self.wallpaperCheckBox.setText(" Wallpaper")
        self.wallpaperCheckBox.setFont(QFont("Ubuntu", 11))
        self.wallpaperCheckBox.adjustSize()
        self.wallpaperCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/timemachine/src/icons/folder.png"))
        self.wallpaperCheckBox.setIconSize(QtCore.QSize(28, 28))
        self.wallpaperCheckBox.clicked.connect(self.on_wallpaper_clicked)
        
        ################################################################################
        # Application checkbox (Apps inside manual folder)
        ################################################################################
        # Get folder size
        if self.packageManager == "rpm":
            self.applicationSize = os.popen(f"du -hs {self.iniExternalLocation}/"
                f"{baseFolderName}/{applicationFolderName}/{rpmFolderName}")
            self.applicationSize = self.applicationSize.read().strip("\t")
            self.applicationSize = self.applicationSize.strip("\n")
            self.applicationSize = self.applicationSize.replace(f"{self.iniExternalLocation}"
                f"/{baseFolderName}/{applicationFolderName}/{rpmFolderName}", "").replace("\t", "")
        
        elif self.packageManager == "deb":
            self.applicationSize = os.popen(f"du -hs {self.iniExternalLocation}/"
                f"{baseFolderName}/{applicationFolderName}/{debFolderName}")
            self.applicationSize = self.applicationSize.read().strip("\t")
            self.applicationSize = self.applicationSize.strip("\n")
            self.applicationSize = self.applicationSize.replace(f"{self.iniExternalLocation}"
                f"/{baseFolderName}/{applicationFolderName}/{debFolderName}", "").replace("\t", "")

        ################################################################################
        # Application checkbox
        ################################################################################
        self.applicationPackagesCheckBox = QCheckBox()
        self.applicationPackagesCheckBox.setText(f" Applications "
            f"              {self.applicationSize}")
        self.applicationPackagesCheckBox.setFont(QFont("Ubuntu", 11))
        self.applicationPackagesCheckBox.adjustSize()
        self.applicationPackagesCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/timemachine/src/icons/folder.png"))
        self.applicationPackagesCheckBox.setIconSize(QtCore.QSize(28, 28))
        self.applicationPackagesCheckBox.clicked.connect(self.on_application_clicked)

        # Application size information
        self.applicationSizeInformation = QLabel()
        # If M inside self.applicationsSizeInformation, add B = MB
        if "M" in self.applicationSize:
            self.applicationSizeInformation.setText(f"{self.applicationSize}B")
        else:
            self.applicationSizeInformation.setText(f"{self.applicationSize}")
        self.applicationSizeInformation.setFont(QFont("Ubuntu", 10))
        self.applicationSizeInformation.adjustSize()
        self.applicationSizeInformation.setAlignment(QtCore.Qt.AlignRight)
        
        ################################################################################
        # Application checkbox (names)
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(self.flatpakTxtFile, "r") as read_file:
            flatpaksToBeInstalled = len(read_file.readlines())

            self.flatpakCheckBox = QCheckBox()
            self.flatpakCheckBox.setText(f" Flatpak "
                f"                   {flatpaksToBeInstalled} Apps")
            self.flatpakCheckBox.setFont(QFont("Ubuntu", 11))
            self.flatpakCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/timemachine/src/icons/folder.png"))
            self.flatpakCheckBox.setIconSize(QtCore.QSize(28, 28))
            self.flatpakCheckBox.clicked.connect(self.on_flatpak_clicked)
            
        ################################################################################
        # Application checkbox (DATA)
        ################################################################################
        self.flatpakDataCheckBox = QCheckBox()
        self.flatpakDataCheckBox.setText(" Flatpak (Data)")
        self.flatpakDataCheckBox.setFont(QFont("Ubuntu", 11))
        self.flatpakDataCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/timemachine/src/icons/folder.png"))
        self.flatpakDataCheckBox.setIconSize(QtCore.QSize(28, 28))
        self.flatpakDataCheckBox.clicked.connect(self.on_applications_data_clicked)

        # Get folder size
        self.flatpakDataSize = os.popen(f"du -hs {self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}")
        self.flatpakDataSize = self.flatpakDataSize.read().strip("\t").strip("\n").replace(f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}", "").replace("\t", "")
    
        # Application size information
        self.applicationSizeInformation = QLabel()
        # If M inside self.applicationsSizeInformation, add B = MB
        if "M" in self.flatpakDataSize:
            self.applicationSizeInformation.setText(f"{self.flatpakDataSize}B")
        else:
            self.applicationSizeInformation.setText(f"{self.flatpakDataSize}")
        self.applicationSizeInformation.setFont(QFont("Ubuntu", 10))
        self.applicationSizeInformation.adjustSize()

        ################################################################################
        # Files & Folders checkbox
        ################################################################################
        # Get available dates inside TMB
        dateFolders = []
        for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
            f"{backupFolderName}"):
            if not "." in output:
                dateFolders.append(output)
                dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        # Get time inside date
        timeFolder = []
        for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
            f"{backupFolderName}/{dateFolders[0]}/"):
            timeFolder.append(output)
            timeFolder.sort(reverse=True)

        # Get folder size
        self.fileAndFoldersFolderSize = os.popen(f"du -hs {self.iniExternalLocation}/"
            f"{baseFolderName}/{backupFolderName}/{dateFolders[0]}/{timeFolder[0]}")
        self.fileAndFoldersFolderSize = self.fileAndFoldersFolderSize.read().strip("\t")
        self.fileAndFoldersFolderSize = self.fileAndFoldersFolderSize.strip("\n")
        self.fileAndFoldersFolderSize = self.fileAndFoldersFolderSize.replace(f"{self.iniExternalLocation}"
            f"/{baseFolderName}/{backupFolderName}/{dateFolders[0]}/{timeFolder[0]}", "").replace("\t", "")

        # Files and Folders checkbox        
        self.fileAndFoldersCheckBox = QCheckBox()
        self.fileAndFoldersCheckBox.setText(" File and Folders"
            f"       {self.fileAndFoldersFolderSize}")
        self.fileAndFoldersCheckBox.setFont(QFont("Ubuntu", 11))
        self.fileAndFoldersCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/timemachine/src/icons/folder.png"))
        self.fileAndFoldersCheckBox.setIconSize(QtCore.QSize(28, 28))
        self.fileAndFoldersCheckBox.clicked.connect(self.on_files_and_folders_clicked)


        # self.fileAndFoldersFolderInformation = QLabel()
        # # If K inside self.applicationsSizeInformation, add K = KB
        # if "K" in self.fileAndFoldersFolderSize:
        #     self.fileAndFoldersFolderInformation.setText(f"{self.fileAndFoldersFolderSize}B")
        # else:
        #     self.fileAndFoldersFolderInformation.setText(f"{self.fileAndFoldersFolderSize}")
            
        # self.fileAndFoldersFolderInformation.setFont(QFont("Ubuntu", 10))
        # self.fileAndFoldersFolderInformation.adjustSize()
        # self.fileAndFoldersFolderInformation.setAlignment(QtCore.Qt.AlignRight)

        ################################################################################
        # User information
        ################################################################################
        self.userSizeInformation = QLabel()
        self.userSizeInformation.setFont(QFont("Ubuntu", 10))
        self.userSizeInformation.adjustSize()
        self.userSizeInformation.setAlignment(QtCore.Qt.AlignRight)

        ################################################################################
        # Buttons
        ################################################################################
        # Back button
        self.backButton = QPushButton(self)
        self.backButton.setText("Back")
        self.backButton.setFont(QFont("Ubuntu", 10))
        self.backButton.adjustSize()
        self.backButton.move(700, 555)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))

        # Continue button
        self.continueButton = QPushButton(self)
        self.continueButton.setText("Continue")
        self.continueButton.setFont(QFont("Ubuntu", 10))
        self.continueButton.adjustSize()
        self.continueButton.move(800, 555)
        self.continueButton.setEnabled(False)
        self.continueButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()+1))

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)

        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.optionskWidget, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayoutForOptions.addWidget(self.wallpaperCheckBox)
        self.verticalLayoutForOptions.addWidget(self.applicationPackagesCheckBox)
        self.verticalLayoutForOptions.addWidget(self.flatpakCheckBox)
        self.verticalLayoutForOptions.addWidget(self.flatpakDataCheckBox)
        self.verticalLayoutForOptions.addWidget(self.fileAndFoldersCheckBox)
        self.verticalLayout.addStretch()

        self.setLayout(self.verticalLayout)

        self.find_flatpak_txt()

    def find_flatpak_txt(self):
        ################################################################################
        # Something inside?
        ################################################################################
        try:
            # Look for flatpakTxt inside external device
            with open(f"{self.iniExternalLocation}/{userName}"
                f"{baseFolderName}/{flatpakTxt}", 'r') as output:
                output = output.read()
                # If is  not empty, enable these boxes
                if output != "":
                    self.flatpakCheckBox.setEnabled(True)

                else:
                    # Disable these boxes
                    self.flatpakCheckBox.setEnabled(False)  

        except FileNotFoundError:
            pass

        self.find_applications()

    def find_applications(self):
        ################################################################################
        # Check inside backup flatpak data (var)
        # There is not need to check (share) inside External
        # If Var is empty, just pass this options
        ################################################################################
        try:
            dummyList = []
            if self.packageManager == "rpm":
                for output in os.listdir(f"{self.iniExternalLocation}/"
                    f"{baseFolderName}/{applicationFolderName}/{rpmFolderName}"):
                    dummyList.append(output)

            elif self.packageManager == "deb":
                for output in os.listdir(f"{self.iniExternalLocation}/"
                    f"{baseFolderName}/{applicationFolderName}/{debFolderName}"):
                    dummyList.append(output)
        except:
            pass

        if dummyList:
            self.applicationPackagesCheckBox.setEnabled(True)

        else:
            self.applicationPackagesCheckBox.setEnabled(False)  

        # Empty list
        dummyList.clear()

        self.find_applications_data()

    def find_applications_data(self):
        ################################################################################
        # Check inside backup flatpak data (var)
        # There is not need to check (share) inside External
        # If Var is empty, just pass this options
        ################################################################################
        try:
            dummyList = []
            for output in os.listdir(f"{self.iniExternalLocation}/"
                f"{baseFolderName}/{applicationFolderName}/{varFolderName}/"):
                dummyList.append(output)
        except:
            pass

        if dummyList:
            self.flatpakDataCheckBox.setEnabled(True)

        else:
            self.flatpakDataCheckBox.setEnabled(False)  

        # Empty list
        dummyList.clear()
        
        self.find_files_and_folders()

    def find_files_and_folders(self):
        ################################################################################
        try:
            dummyList = []
            # Check inside backup folder 
            for output in os.listdir(f"{self.iniExternalLocation}/"
                f"{baseFolderName}/{backupFolderName}/"):
                dummyList.append(output)
        except:
            pass

        if dummyList:
            self.fileAndFoldersCheckBox.setEnabled(True)

        else:
            self.fileAndFoldersCheckBox.setEnabled(False)  

        # Clean list
        dummyList.clear()
        
        self.find_wallpaper()

    def find_wallpaper(self):
        try:
            dummyList = []
            # Find user's DE type
            userDE = os.popen(getUserPackageManager)
            userDE = userDE.read().strip().lower()
            # Get current user's background
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/"
                f"{wallpaperFolderName}/"):
                dummyList.append(output)
        except:
            pass

        if dummyList:
            # Activate wallpaper option
            if "gnome" in userDE:
                self.wallpaperCheckBox.setEnabled(True)

        else:
            self.wallpaperCheckBox.setEnabled(False)  

        # Empty list
        dummyList.clear()

    def on_application_clicked(self):
        # Restore packages applications
        with open(src_user_config, 'w') as configfile:
            if self.applicationPackagesCheckBox.isChecked():
                config.set('RESTORE', 'applications_packages', 'true')

                # Activate data checkbox
                self.applicationPackagesCheckBox.setChecked(True)
                # Enable continue button
                self.continueButton.setEnabled(True)
                # Add names to list
                self.outputBox.append("packages")

            else:
                config.set('RESTORE', 'applications_packages', 'false')

                # Disable names
                if "packages" in self.outputBox:
                    self.outputBox.remove("packages")
      
            # Write to INI file
            config.write(configfile)

            # Allow continue?
            self.allow_to_continue()
  
    def on_flatpak_clicked(self):
        ################################################################################
        # Write to INI file
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            if self.flatpakCheckBox.isChecked():
                config.set('RESTORE', 'applications_flatpak_names', 'true')
                
                # Activate flatpak checkbox
                self.flatpakCheckBox.setChecked(True)
                # Enable continue button
                self.continueButton.setEnabled(True)
                # Add names to list if not already there
                if "flatpak" not in self.outputBox:
                    self.outputBox.append("flatpak")
            else:
                config.set('RESTORE', 'applications_flatpak_names', 'false')
                # Disable data checkbox
                self.flatpakCheckBox.setChecked(False)
                # Disable flatpak if in list
                if "flatpak" in self.outputBox:
                    self.outputBox.remove("flatpak")

            # Write to INI file
            config.write(configfile)
            
            # Allow continue?
            self.allow_to_continue()

    def on_applications_data_clicked(self):
        # If user allow app to back up data, auto activate
        # backup flatpaks name too.
        with open(src_user_config, 'w') as configfile:
            if self.flatpakDataCheckBox.isChecked():
                config.set('RESTORE', 'applications_flatpak_names', 'true')
                config.set('RESTORE', 'applications_data', 'true')

                # Activate data checkbox
                self.flatpakDataCheckBox.setChecked(True)
                # Enable continue button
                self.continueButton.setEnabled(True)
                # Add data to list if not already there
                if "data" not in self.outputBox:
                    self.outputBox.append("data")
                # Auto enable flatpak to list
                self.outputBox.append("flatpak")
              
            else:
                config.set('RESTORE', 'applications_data', 'false')
                # Disable data checkbox
                self.flatpakDataCheckBox.setChecked(False)
                # Disable data if in list
                if "data" in self.outputBox:
                    self.outputBox.remove("data")

            # Write to INI file
            config.write(configfile)

            # Allow continue?
            self.allow_to_continue()
  
    def on_files_and_folders_clicked(self):
        ################################################################################
        # Write to INI file
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            if self.fileAndFoldersCheckBox.isChecked():
                config.set('RESTORE', 'files_and_folders', 'true')

                # Enable continue button
                self.continueButton.setEnabled(True)
                # Add files to list
                self.outputBox.append("files")
              
            else:
                config.set('RESTORE', 'files_and_folders', 'false')

                # Disable continue button
                self.continueButton.setEnabled(False)
                if "files" in self.outputBox:
                    self.outputBox.remove("files")

            # Write to INI file
            config.write(configfile)

            # Allow continue?
            self.allow_to_continue()
  
    def on_wallpaper_clicked(self):
        ################################################################################
        # Write to INI file
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            if self.wallpaperCheckBox.isChecked():
                config.set('RESTORE', 'wallpaper', 'true')

                # Enable continue button
                self.continueButton.setEnabled(True)
                # Add wallpaper to list
                self.outputBox.append("wallpaper")
              
            else:
                config.set('RESTORE', 'wallpaper', 'false')

                # Disable continue button
                self.continueButton.setEnabled(False)
                if "wallpaper" in self.outputBox:
                    self.outputBox.remove("wallpaper")

            # Write to INI file
            config.write(configfile)
            
            # Allow continue?
            self.allow_to_continue()

    def allow_to_continue(self):
        # If self.outputBox is not empty, allow it
        if len(self.outputBox) > 0:
            # Enable continue button
            self.continueButton.setEnabled(True)
        else:
            # Disable continue button
            self.continueButton.setEnabled(False)

class BACKUPSCREEN(QWidget):
    def __init__(self):
        super().__init__()
        self.outputBox = ()
        self.clickedOnRestore = None

        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        # Restore area widget
        self.devicesAreadWidget = QWidget()
        self.devicesAreadWidget.setFixedSize(400, 200)

        # Horizontal layout
        self.imagesLayout = QHBoxLayout(self.devicesAreadWidget)
        self.imagesLayout.setSpacing(10)

        ################################################################################
        # Texts
        ################################################################################
        # Title
        self.title = QLabel()
        self.title.setFont(QFont("Ubuntu", 28))
        self.title.setText("Transferring Your information")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        # Description
        self.description = QLabel()
        self.description.setFont(QFont("Ubuntu", 11))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Backup from {appName} " 
            "will been transferred to this PC.")

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont("Ubuntu", 14))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText('Click on "Restore" to begin.') 

        # Restoring description
        self.whileRestoringDescription = QLabel()
        self.whileRestoringDescription.setFont(QFont("Ubuntu", 11))
        self.whileRestoringDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        ################################################################################
        # Images
        ################################################################################
        # Image 1       
        image = QLabel()
        image.setFixedSize(128, 128)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/restore_128px.svg);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        # Image 2       
        image2 = QLabel()
        image2.setFixedSize(96, 96)
        image2.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/arrow.png);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        # Image 3       
        image3 = QLabel()
        image3.setFixedSize(128, 128)
        image3.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/pc_128px.svg);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        ################################################################################
        # External device name
        ################################################################################
        widgetDeviceName = QWidget(self)
        widgetDeviceName.setFixedSize(180, 40)
        widgetDeviceName.move(232, 265)

        # Widget device layout
        widgetDeviceLayout = QHBoxLayout(widgetDeviceName)

        # External device name
        self.externalDeviceName = QLabel()
        self.externalDeviceName.setFont(QFont("Ubuntu", 11))
        # Add userName 
        self.iniExternalName = config['EXTERNAL']['name']
        self.externalDeviceName.setText(self.iniExternalName)
        self.externalDeviceName.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.externalDeviceName.adjustSize()
        
        ################################################################################
        # This pc label
        ################################################################################
        widgetThisPCName = QWidget(self)
        widgetThisPCName.setFixedSize(180, 40)
        widgetThisPCName.move(488, 265)

        # This pc name layout
        widgetLayout = QHBoxLayout(widgetThisPCName)

        self.thisPCName = QLabel()
        self.thisPCName.setFont(QFont("Ubuntu", 11))
        self.thisPCName.setText(f"{userName}") # 
        self.thisPCName.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.thisPCName.adjustSize()

        ################################################################################
        # Buttons
        ################################################################################
        # Back button
        self.backButton = QPushButton(self)
        self.backButton.setText("Back")
        self.backButton.setFont(QFont("Ubuntu", 10))
        self.backButton.adjustSize()
        self.backButton.move(700, 555)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))

        # Continue button
        self.startRestoreButton = QPushButton(self)
        self.startRestoreButton.setText("Restore")
        self.startRestoreButton.setFont(QFont("Ubuntu", 10))
        self.startRestoreButton.adjustSize()
        self.startRestoreButton.move(800, 555)
        self.startRestoreButton.setEnabled(True)
        self.startRestoreButton.clicked.connect(self.start_restoring)

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addWidget(self.devicesAreadWidget, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.moreDescription, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.whileRestoringDescription, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Widget device layouts
        self.imagesLayout.addWidget(image, 1, QtCore.Qt.AlignHCenter)
        self.imagesLayout.addWidget(image2, 1, QtCore.Qt.AlignHCenter)
        self.imagesLayout.addWidget(image3, 1, QtCore.Qt.AlignHCenter)
        widgetDeviceLayout.addWidget(self.externalDeviceName)
        widgetLayout.addWidget(self.thisPCName)

        # Add userName self.set
        self.setLayout(self.verticalLayout)

        # Update
        timer.timeout.connect(self.read_ini_file)
        timer.start(2000)
        self.read_ini_file()

    def read_ini_file(self):
        try:
            ################################################################################
            # Read file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            self.iniExternalName = config['EXTERNAL']['name']
            self.iniIsRestoreRunning = config['RESTORE']['is_restore_running']
            self.iniApplicationsPackages = config['RESTORE']['applications_packages']
            self.iniApplicationData = config['RESTORE']['applications_data']
            self.iniFilesAndsFolders = config['RESTORE']['files_and_folders']
            # Current backup information
            self.iniCurrentBackupInfo = config['INFO']['feedback_status']
            # Current backup information
            self.iniCurrentPercentBackup = config['INFO']['current_percent']
            # Get current notification ID
            self.iniNotificationID = config['INFO']['notification_id']

        except:
            pass

        # Add externalDeviceName text
        self.externalDeviceName.setText(self.iniExternalName)

        ################################################################################
        # Update widgets
        ################################################################################
        # if restoring is running
        if self.iniIsRestoreRunning == "true":
            # Show restoring description
            self.whileRestoringDescription.setText(f'Transferring '
                f"{self.iniCurrentBackupInfo} to the user {userName}...") 
            # Hide more description
            self.moreDescription.hide()
            # Show restoring description
            self.whileRestoringDescription.show()
        
    def start_restoring(self):
        # Disable back button
        self.backButton.setEnabled(False)
        # Disable restore button
        self.startRestoreButton.setEnabled(False)
        # Call restore python
        sub.run(f"python3 {src_restore_cmd}", shell=True)
        # Change screen
        widget.setCurrentIndex(widget.currentIndex()+1)

class DONE(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.widgets()

    def widgets(self):
        # Title layout
        self.titlelLayout = QVBoxLayout()
        self.titlelLayout.setSpacing(20)
        self.titlelLayout.setContentsMargins(20, 20, 20, 20)
        
        # Image       
        image = QLabel()
        image.setFixedSize(128, 128)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_backup_icon});"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")
        
        # Welcome
        self.title = QLabel()
        self.title.setFont(QFont("Ubuntu", 34))
        self.title.setText("Migration Assistant")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

       # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont("Ubuntu", 14))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText("All done!") 

        ################################################################################
        # Buttons
        ################################################################################
        # Close button
        self.closeButton = QPushButton(self)
        self.closeButton.setText("Close")
        self.closeButton.setFont(QFont("Ubuntu", 10))
        self.closeButton.adjustSize()
        self.closeButton.move(800, 555)
        self.closeButton.clicked.connect(lambda: exit())

        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        self.titlelLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.titlelLayout.addWidget(image, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titlelLayout.addWidget(self.moreDescription, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.setLayout(self.titlelLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = WELCOMESCREEN()
    main2 = CHOOSEDEVICE()
    main3 = OPTIONS()
    main4 = PREBACKUP()
    main5 = BACKUPSCREEN()
    main6 = DONE()

    widget = QStackedWidget()
    widget.addWidget(main)   
    widget.addWidget(main2) 
    widget.addWidget(main3) 
    widget.addWidget(main4) 
    widget.addWidget(main5) 
    widget.addWidget(main6) 
    widget.setCurrentWidget(main)   

    # Window settings
    widget.setWindowTitle(appName)
    widget.setWindowIcon(QIcon(src_backup_icon))
    widget.setFixedSize(windowXSize, windowYSize)
    widget.show()

    app.exit(app.exec())
