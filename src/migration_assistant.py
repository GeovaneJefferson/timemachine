#! /usr/bin/python3
from setup import *
from device_location import device_location
from package_manager import package_manager
from get_backup_date import get_backup_date
from get_backup_time import get_latest_backup_time
from restore_cmd import RESTORE
from read_ini_file import UPDATEINIFILE
from stylesheet import *


class WELCOMESCREEN(QWidget):
    def __init__(self):
        super(WELCOMESCREEN, self).__init__()
        self.widgets()

    def widgets(self):
        # Title layout
        self.titlelLayout = QVBoxLayout()
        self.titlelLayout.setSpacing(20)
        self.titlelLayout.setContentsMargins(20, 20, 20, 20)
        
        # Image       
        image = QLabel()
        image.setFixedSize(140, 140)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_migration_assistant_96px});"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")
        
        # Welcome
        self.title = QLabel()
        self.title.setFont(QFont("Arial", 34))
        self.title.setText("Migration Assistant")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        """)

       # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(fontSize11px)
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText("Use Migration Assistant to restore information such as "
            "Applications, Files, Folders and more to this PC.") 

        ################################################################################
        # Buttons
        ################################################################################
        widgetButton = QWidget(self)
        widgetButton.setFixedSize(900,60)
        widgetButton.move(0,600-widgetButton.height())
        widgetButton.setStyleSheet(separetorLine)

        widgetButtonLayout = QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)
        
        # Continue button
        self.continueButton = QPushButton()
        self.continueButton.setFixedHeight(buttonHeightSize)
        self.continueButton.setText("   Continue   ")
        self.continueButton.setFont(buttonFontSize)
        self.continueButton.adjustSize()
        self.continueButton.setStyleSheet(buttonStylesheet)
        self.continueButton.clicked.connect(self.on_continueButton_clicked)

        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        self.titlelLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.titlelLayout.addWidget(image, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titlelLayout.addWidget(self.moreDescription, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        widgetButtonLayout.addWidget(self.continueButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.setLayout(self.titlelLayout)

    def on_continueButton_clicked(self):
        main2 = CHOOSEDEVICE()
        widget.addWidget(main2) 
        widget.setCurrentIndex(widget.currentIndex()+1)

class CHOOSEDEVICE(QWidget):
    def __init__(self):
        super().__init__()
        self.foundInMedia = None
        self.outputBox = ()
        self.captureDevices = []

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
        self.title.setFont(QFont("Arial Bold", 28))
        self.title.setText("Restore information to this PC")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        """)

        # Description
        self.description = QLabel()
        self.description.setFont(fontSize11px)
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Select a {appName} " 
            "backup disk to retore it's information to this PC.")

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(fontSize11px)
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText(f"Make sure that your Backup external device " 
            f"with a {appName}'s backup is already connected to this PC.")

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
        widgetButton = QWidget(self)
        widgetButton.setFixedSize(900,60)
        widgetButton.move(0,600-widgetButton.height())
        widgetButton.setStyleSheet(separetorLine)

        widgetButtonLayout = QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)
        
        # Back button
        self.backButton = QPushButton()
        self.backButton.setText("   Back   ")
        self.backButton.setFont(buttonFontSize)
        self.backButton.setFixedHeight(buttonHeightSize)
        self.backButton.adjustSize()
        self.backButton.setStyleSheet(buttonStylesheet)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))

        # Continue button
        self.continueButton = QPushButton()
        self.continueButton.setText("   Continue  ")
        self.continueButton.setFont(buttonFontSize)
        self.continueButton.setFixedHeight(buttonHeightSize)
        self.continueButton.adjustSize()
        self.continueButton.setEnabled(False)
        self.continueButton.setStyleSheet(buttonStylesheet)
        self.continueButton.clicked.connect(self.on_continue_clicked)
        
        widgetButtonLayout.addStretch()
        widgetButtonLayout.addWidget(self.backButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        widgetButtonLayout.addWidget(self.continueButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.show_on_screen()

    def show_on_screen(self):
        ################################################################################
        # Search external inside media
        ################################################################################
        if device_location():
            location = f"{media}"
        elif not device_location():
            location = f"{run}"
        else:
            location = None

        ################################################################################
        # Show available files
        ################################################################################
        try:
            for output in os.listdir(f"{location}/{userName}/"):
                # Only show disk the have baseFolderName inside
                if baseFolderName in os.listdir(f"{location}/{userName}/{output}/"):
                    if output not in self.captureDevices:   
                        self.captureDevices.append(output)

                        self.availableDevices = QPushButton(self.devicesAreadWidget)
                        self.availableDevices.setCheckable(True)
                        self.availableDevices.setAutoExclusive(True)
                        self.availableDevices.setFixedSize(140,140)
                        self.availableDevices.setText(f"\n\n\n\n\n{output}")
                        self.availableDevices.setFont(fontSize11px)
                        self.availableDevices.adjustSize()
                        self.availableDevices.clicked.connect(
                            lambda *args, output=output: self.on_device_clicked(output))
                        self.availableDevices.setStyleSheet(buttonStylesheet)
           
                        # Image
                        image = QLabel(self.availableDevices)
                        image.setFixedSize(96, 96)
                        image.move(38,30)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                                f"background-image: url({src_monitor_icon});"
                                "background-repeat: no-repeat;"
                                "background-color: transparent;"
                            "}")

                        self.devicesAreaLayout.addWidget(self.availableDevices)

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

    def on_device_clicked(self, output):
        self.locationBackup = output
        self.continueButton.setEnabled(True)
        
    def on_continue_clicked(self):
        ################################################################################
        # Update INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if str(supportedDEBPackageManager) in package_manager():
                # Save user's os name
                config.set(f'INFO', 'packageManager', f'{debFolderName}')

            elif str(supportedRPMPackageManager) in package_manager():
                # Save user's os name
                config.set(f'INFO', 'packageManager', f'{rpmFolderName}')

            # Update INI file
            if device_location():
                config.set(f'EXTERNAL', 'hd', f'{media}/{userName}/{self.locationBackup}')

            elif not device_location():
                config.set(f'EXTERNAL', 'hd', f'{run}/{userName}/{self.locationBackup}')

            config.set('EXTERNAL', 'name', f'{self.locationBackup}')
            config.write(configfile)

        main4 = PREBACKUP()
        widget.addWidget(main4) 
        widget.setCurrentIndex(widget.currentIndex()+1)

class PREBACKUP(QWidget):
    def __init__(self):
        super().__init__()
        self.optionsAddedList = []
        self.excludeAppList = []
        self.countOfDebList = []
        self.countOfRPMList = []
        self.alreadySelectApps = False
        
        self.restoreHome = None
        self.restoreApplicationsPackages = None
        self.restoreFlatpaksPrograms = None
        self.restoreFlatpaksData = None
        self.restoreSystemSettings = None
        self.reboot = None

        self.excludeAppsLoc = (f"{mainIniFile.ini_external_location()}/{baseFolderName}/"
                f"{applicationFolderName}/{src_exclude_applications}")
        
        # Delete .exclude-applications.txt first
        if os.path.exists(self.excludeAppsLoc):
            sub.run(f"rm -rf {self.excludeAppsLoc}", shell=True)
            
        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        # Restore widget
        self.optionskWidget = QWidget()

        self.scrollOptions = QScrollArea(self)
        self.scrollOptions.setFixedSize(420,260)
        self.scrollOptions.setWidgetResizable(True)
        self.scrollOptions.setWidget(self.optionskWidget)
        self.scrollOptions.setStyleSheet(whiteBox)

        # Vertical base layout
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        # Vertical options layout
        self.verticalLayoutForOptions = QVBoxLayout(self.optionskWidget)
        self.verticalLayoutForOptions.setSpacing(5)
        self.verticalLayoutForOptions.setAlignment(QtCore.Qt.AlignTop)
        self.verticalLayoutForOptions.setContentsMargins(10, 10, 10, 10)

        # Title
        self.title = QLabel()
        self.title.setFont(fontSize24px)
        self.title.setText("Select the information to restore")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
            font-weight: Bold;
        """)

        # Description
        self.description = QLabel()
        self.description.setFont(fontSize11px)
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText("Choose which information you'd like to restore to this PC.")
        
        ################################################################################
        # Application checkbox (DATA)
        ################################################################################
        self.flatpakDataCheckBox = QCheckBox()
        self.flatpakDataCheckBox.setText(" Flatpak (Data)")
        self.flatpakDataCheckBox.setFont(fontSize11px)
        self.flatpakDataCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/application-vnd.flatpak.ref.svg"))
        self.flatpakDataCheckBox.setIconSize(QtCore.QSize(32,32))
        self.flatpakDataCheckBox.setEnabled(False)
        self.flatpakDataCheckBox.clicked.connect(self.on_applications_data_clicked)
        
        ################################################################################
        # Buttons
        ################################################################################
        widgetButton = QWidget(self)
        widgetButton.setFixedSize(900,60)
        widgetButton.move(0,self.height()+60)
        widgetButton.setStyleSheet(separetorLine)

        widgetButtonLayout = QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)
        
        # Back button
        self.backButton = QPushButton()
        self.backButton.setText("   Back   ")
        self.backButton.setFont(buttonFontSize)
        self.backButton.adjustSize()
        self.backButton.setStyleSheet(buttonStylesheet)
        self.backButton.setFixedHeight(buttonHeightSize)
        self.backButton.clicked.connect(self.on_back_button_clicked)

        # Continue button
        self.continueButton = QPushButton()
        self.continueButton.setText("   Continue   ")
        self.continueButton.setFont(buttonFontSize)
        self.continueButton.adjustSize()
        self.continueButton.setFixedHeight(buttonHeightSize)
        self.continueButton.setStyleSheet(buttonStylesheet)

        if not self.optionsAddedList:
            self.continueButton.setEnabled(False)
        self.continueButton.clicked.connect(self.on_continue_button_clicked)

        ################################################################################
        # System settings checkbox
        ################################################################################
        dummySystemSettingsSizeList = []
        
        ################################################################################
        # Application checkbox (Apps inside manual folder)
        ################################################################################
        try:
            # Get folder size
            if package_manager() == rpmFolderName:
                self.applicationSize = os.popen(f"du -hs {mainIniFile.rpm_main_folder()}/")
                self.applicationSize = self.applicationSize.read().strip("\t")
                self.applicationSize = self.applicationSize.strip("\n")
                self.applicationSize = self.applicationSize.replace(f"{mainIniFile.deb_main_folder()}", "").replace("\t", "").replace("/", "")
        
            elif package_manager() == debFolderName:
                self.applicationSize = os.popen(f"du -hs {mainIniFile.deb_main_folder()}/")
                self.applicationSize = self.applicationSize.read().strip("\t")
                self.applicationSize = self.applicationSize.strip("\n")
                self.applicationSize = self.applicationSize.replace(f"{mainIniFile.deb_main_folder()}", "").replace("\t", "").replace("/", "")

            ################################################################################
            # Application checkbox
            ################################################################################
            self.applicationPackagesCheckBox = QCheckBox()
            self.applicationPackagesCheckBox.setText(f" Applications "
                "                              "
                f"                              {self.applicationSize}")
            self.applicationPackagesCheckBox.setFont(fontSize11px)
            self.applicationPackagesCheckBox.adjustSize()
            self.applicationPackagesCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/folder-templates.svg"))
            self.applicationPackagesCheckBox.setIconSize(QtCore.QSize(32,32))
            self.applicationPackagesCheckBox.setToolTip("This will reinstall: \n"
                "* All backup's packages")
            self.applicationPackagesCheckBox.clicked.connect(self.on_application_clicked)
        except:
            pass

        try:
            # Application size information
            self.applicationSizeInformation = QLabel()
            # If M inside self.applicationsSizeInformation, add B = MB
            if "M" in self.applicationSize:
                self.applicationSizeInformation.setText(f"{self.applicationSize}B")
            else:
                self.applicationSizeInformation.setText(f"{self.applicationSize}")
            self.applicationSizeInformation.setFont(buttonFontSize)
            self.applicationSizeInformation.adjustSize()
            self.applicationSizeInformation.setAlignment(QtCore.Qt.AlignRight)
        except:
            pass

        try:
            ################################################################################
            # Flatpak checkbox (names)
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(mainIniFile.flatpak_txt_location(), "r") as read_file:
                flatpaksToBeInstalled = len(read_file.readlines())

                self.flatpakCheckBox = QCheckBox()
                self.flatpakCheckBox.setText(f" Flatpak "
                    "                                  "
                    f"                               {flatpaksToBeInstalled} Apps")
                self.flatpakCheckBox.setFont(fontSize11px)
                self.flatpakCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/application-vnd.flatpak.ref.svg"))
                self.flatpakCheckBox.setIconSize(QtCore.QSize(32,32))
                self.flatpakCheckBox.setToolTip("This will reinstall: \n"
                    "* All flatpak applications")
                self.flatpakCheckBox.clicked.connect(self.on_flatpak_clicked)
        except:
            pass
        ################################################################################
        # Flatpaks DATA checkbox
        ################################################################################
        try:
            # Get flatpak data size
            self.flatpakDataSize = os.popen(f"du -hs {mainIniFile.ini_external_location()}/{baseFolderName}/{applicationFolderName}")
            self.flatpakDataSize = self.flatpakDataSize.read().strip("\t").strip("\n").replace(f"{mainIniFile.ini_external_location()}/{baseFolderName}/{applicationFolderName}", "").replace("\t", "")
        
 
            # Application size information
            self.applicationSizeInformation = QLabel()
            # If M inside self.applicationsSizeInformation, add B = MB
            if "M" in self.flatpakDataSize:
                self.applicationSizeInformation.setText(f"{self.flatpakDataSize}B")
            else:
                self.applicationSizeInformation.setText(f"{self.flatpakDataSize}")
            self.applicationSizeInformation.setFont(buttonFontSize)
            self.applicationSizeInformation.adjustSize()
        
        except:
            pass

        ################################################################################
        # System Settings checkbox
        ################################################################################
        try:
            # Icons size
            self.systemSettingsFolderSize = os.popen(f"du -hs {mainIniFile.icon_main_folder()} 2>/dev/null")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.read().strip("\t")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.strip("\n")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.replace(f"{mainIniFile.icon_main_folder()}", "")
            dummySystemSettingsSizeList.append(self.systemSettingsFolderSize)

            # Theme size
            self.systemSettingsFolderSize = os.popen(f"du -hs {themeFolderName} 2>/dev/null")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.read().strip("\t")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.strip("\n")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.replace(f"{themeFolderName}", "")
            dummySystemSettingsSizeList.append(self.systemSettingsFolderSize)
        
            # Cursor size
            self.systemSettingsFolderSize = os.popen(f"du -hs {cursorFolderName} 2>/dev/null")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.read().strip("\t")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.strip("\n")
            self.systemSettingsFolderSize = self.systemSettingsFolderSize.replace(f"{cursorFolderName}", "")
            dummySystemSettingsSizeList.append(self.systemSettingsFolderSize)

            # Sum all values inside dummySystemSettingsSizeList
            self.systemSettingsFolderSize = sum(dummySystemSettingsSizeList)
        
        except:
            pass

        try:
            # System settings size information
            self.SystemSettingsSizeInformation = QLabel()
            # If M inside self.applicationsSizeInformation, add B = MB
            if "M" in self.systemSettingsFolderSize:
                self.SystemSettingsSizeInformation.setText(f"{self.systemSettingsFolderSize}B")
            else:
                self.SystemSettingsSizeInformation.setText(f"{self.systemSettingsFolderSize}")
            self.SystemSettingsSizeInformation.setFont(buttonFontSize)
            self.SystemSettingsSizeInformation.adjustSize()
        

            self.systemSettingsCheckBox = QCheckBox()
            self.systemSettingsCheckBox.setText(" System Settings"
                "                               "
                f"                              {self.systemSettingsFolderSize}")
            self.systemSettingsCheckBox.setFont(fontSize11px)
            self.systemSettingsCheckBox.adjustSize()
            self.systemSettingsCheckBox.setToolTip("This will restore: \n"
                "* Wallpaper\n"
                "* Theme\n"
                "   -- Icon\n"
                "   -- Cursor")

            self.systemSettingsCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/preferences-system.svg"))
            self.systemSettingsCheckBox.setIconSize(QtCore.QSize(32,32))
            self.systemSettingsCheckBox.clicked.connect(self.on_system_settings_clicked)
            
        except:
            pass

        ################################################################################
        # Files & Folders checkbox
        ################################################################################
        try:
            # Get folder size
            self.fileAndFoldersFolderSize = os.popen(f"du -hs {mainIniFile.ini_external_location()}/"
                f"{baseFolderName}/{backupFolderName}/{get_backup_date()[0]}/{get_latest_backup_time()[0]}")
            self.fileAndFoldersFolderSize = self.fileAndFoldersFolderSize.read().strip("\t")
            self.fileAndFoldersFolderSize = self.fileAndFoldersFolderSize.strip("\n")
            self.fileAndFoldersFolderSize = self.fileAndFoldersFolderSize.replace(f"{mainIniFile.ini_external_location()}"
                f"/{baseFolderName}/{backupFolderName}/{get_backup_date()[0]}/{get_latest_backup_time()[0]}", "")
        except:
            pass

        try:
            # Files and Folders checkbox        
            self.fileAndFoldersCheckBox = QCheckBox()
            self.fileAndFoldersCheckBox.setText(" Files and Folders"
                "                               "
                f"                      {self.fileAndFoldersFolderSize}")
            self.fileAndFoldersCheckBox.setFont(fontSize11px)
            self.fileAndFoldersCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/text-x-generic.svg"))
            self.fileAndFoldersCheckBox.setIconSize(QtCore.QSize(32,32))
            self.fileAndFoldersCheckBox.setToolTip("This will restore: \n"
                "* All recents back up files and folders")
            self.fileAndFoldersCheckBox.clicked.connect(self.on_files_and_folders_clicked)
        except:
            pass

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.baseAppsWidget = QWidget()

        self.scrollShowMoreApps = QScrollArea()
        self.scrollShowMoreApps.setFixedHeight(0)
        self.scrollShowMoreApps.setWidgetResizable(True)
        # self.scrollShowMoreApps.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollShowMoreApps.setWidget(self.baseAppsWidget)

        ################################################################################
        self.selectAppsLayout = QVBoxLayout(self.baseAppsWidget)
        self.selectAppsLayout.setSpacing(5)

        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.scrollOptions, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.verticalLayoutForOptions.addWidget(self.applicationPackagesCheckBox)
        self.verticalLayoutForOptions.addWidget(self.scrollShowMoreApps)
        self.verticalLayoutForOptions.addWidget(self.flatpakCheckBox)
        self.verticalLayoutForOptions.addWidget(self.flatpakDataCheckBox)
        self.verticalLayoutForOptions.addWidget(self.fileAndFoldersCheckBox)
        self.verticalLayoutForOptions.addWidget(self.systemSettingsCheckBox)
        self.verticalLayout.addStretch(10)
        
        widgetButtonLayout.addStretch()
        widgetButtonLayout.addWidget(self.backButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        widgetButtonLayout.addWidget(self.continueButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.setLayout(self.verticalLayout)


        self.find_flatpak_txt()

    def find_flatpak_txt(self):
        ################################################################################
        # Something inside?
        ################################################################################
        try:
            # Look for flatpakTxt inside external device
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(f"{mainIniFile.flatpak_txt_location()}", 'r') as output:
                output = output.read()
                # TODO
                try:
                    # If is  not empty, enable these boxes
                    if output != "":
                        self.flatpakCheckBox.setEnabled(True)

                    else:
                        # Disable these boxes
                        self.flatpakCheckBox.setEnabled(False)  
                except:
                    pass

        except FileNotFoundError:
            pass

        self.find_applications()

    def find_applications(self):
        ################################################################################
        # Check inside backup flatpak data (var)
        # There is not need to check (share) inside External
        # If Var is empty, just pass skip options
        ################################################################################
        try:
            dummyList = []
            if mainIniFile.ini_package_manager() == rpmFolderName:
                for outputRPM in os.listdir(f"{mainIniFile.rpm_main_folder()}/"):
                    dummyList.append(outputRPM)

            elif mainIniFile.ini_package_manager() == debFolderName:
                for outputDeb in os.listdir(f"{mainIniFile.deb_main_folder()}/"):
                    dummyList.append(outputDeb)
            
            # If has something inside
            if dummyList:
                self.applicationPackagesCheckBox.setEnabled(True)
            
            else:
                self.applicationPackagesCheckBox.setEnabled(False)  

            # Empty list
            dummyList.clear()
            
        except:
            pass

        self.find_applications_data()

    def find_applications_data(self):
        ################################################################################
        # Check inside backup flatpak data (var)
        # There is not need to check (share) inside External
        # If Var is empty, just pass this options
        ################################################################################
        try:
            dummyList = []
            for output in os.listdir(f"{mainIniFile.application_var_folder()}/"):
                dummyList.append(output)

            if dummyList:
                self.flatpakDataCheckBox.setEnabled(True)

            else:
                self.flatpakDataCheckBox.setEnabled(False)  
            
            # Empty list
            dummyList.clear()

        except:
            pass

        self.find_files_and_folders()

    def find_files_and_folders(self):
        ################################################################################
        try:
            dummyList = []
            # Check inside backup folder 
            for output in os.listdir(f"{mainIniFile.backup_folder_name()}/"):
                dummyList.append(output)

            if dummyList:
                self.fileAndFoldersCheckBox.setEnabled(True)

            else:
                self.fileAndFoldersCheckBox.setEnabled(False)  

            # Clean list
            dummyList.clear()

        except:
            pass

        self.enable_system_settings()

    def enable_system_settings(self):
        dummyList = []
        try:
            # Check if a wallpaper has been backup
            for output in os.listdir(f"{mainIniFile.wallpaper_main_folder()}/"):
                dummyList.append(output)

            # Check if icon has been backup
            for output in os.listdir(f"{mainIniFile.icon_main_folder()}/"):
                dummyList.append(output)

            # Check if theme has been backup
            for output in os.listdir(f"{mainIniFile.theme_main_folder()}/"):
                dummyList.append(output)
            
            # Check if cursor has been backup
            for output in os.listdir(f"{mainIniFile.cursor_main_folder()}/"):
                dummyList.append(output)

            # Check if user DE is in the supported list
            if dummyList:
                # Enable systemSettingsCheckBox
                self.systemSettingsCheckBox.setEnabled(True)
                
            else:
                self.systemSettingsCheckBox.setEnabled(False)  

            # Empty list
            dummyList.clear()

        except:
            pass

    def on_application_clicked(self):
        # Open applications checkboxes
        if not self.alreadySelectApps:
            self.scrollShowMoreApps.setFixedHeight(120)
            self.alreadySelectApps = True
        else:
            self.scrollShowMoreApps.setFixedHeight(0)
            self.alreadySelectApps = False

        # Restore packages applications
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            if self.applicationPackagesCheckBox.isChecked():
                config.set('RESTORE', 'applications_packages', 'true')
                # Activate data checkbox
                self.applicationPackagesCheckBox.setChecked(True)
                # Enable continue button
                self.continueButton.setEnabled(True)
                # Add names to list
                self.optionsAddedList.append("packages")

                # DEP
                if self.iniUserPackageManager == debFolderName:
                    for exclude in os.listdir(f"{mainIniFile.ini_external_location()}/{baseFolderName}/"
                        f"{applicationFolderName}/{debFolderName}/"):
                        # Exclude
                        # exclude = exclude.split("_")[0].split("-")[0]
                        # Checkbox
                        dummyCheckBox = QCheckBox()
                        dummyCheckBox.setText(exclude.capitalize())
                        dummyCheckBox.setChecked(True)
                        self.countOfDebList.append(exclude)
                        dummyCheckBox.clicked.connect(lambda *args, exclude=exclude: self.exclude_apps(exclude))

                        self.selectAppsLayout.addWidget(dummyCheckBox)
                # RPM
                elif self.iniUserPackageManager == rpmFolderName:
                    for exclude in os.listdir(f"{mainIniFile.ini_external_location()}/{baseFolderName}/"
                        f"{applicationFolderName}/{rpmFolderName}/"):
                        # Exclude
                        # exclude = exclude.split("_")[0].split("-")[0]
                        # Checkbox
                        dummyCheckBox = QCheckBox()
                        dummyCheckBox.setText(exclude.capitalize())
                        dummyCheckBox.setChecked(True)
                        self.countOfDebList.append(exclude)
                        dummyCheckBox.clicked.connect(lambda *args, exclude=exclude: self.exclude_apps(exclude))

                        self.selectAppsLayout.addWidget(dummyCheckBox)
                else:
                    pass

            else:
                config.set('RESTORE', 'applications_packages', 'false')
                # Disable names
                # if "packages" in self.optionsAddedList:
                self.optionsAddedList.remove("packages")
                # Clean exclude lsit
                self.excludeAppList.clear()
                # Remove applications checkboxes
                for i in range(self.selectAppsLayout.count()):
                    item = self.selectAppsLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1

            # Write to INI file
            config.write(configfile)
            # Allow continue?
            self.allow_to_continue()

    def on_flatpak_clicked(self):

        if self.flatpakCheckBox.isChecked():
            self.restoreFlatpaksPrograms = True
            # Activate flatpak checkbox
            self.flatpakCheckBox.setChecked(True)
            # Enable continue button
            self.continueButton.setEnabled(True)
            # Add names to list if not already there
            self.optionsAddedList.append("flatpak")

        else:
            self.restoreFlatpaksPrograms = False
            # Disable data checkbox
            self.flatpakCheckBox.setChecked(False)
            # Disable flatpak if in list
            self.optionsAddedList.remove("flatpak")

        self.allow_to_continue()

    def on_applications_data_clicked(self):
        if self.flatpakDataCheckBox.isChecked():
            self.restoreFlatpaksPrograms = True
            self.restoreFlatpaksData = True
            # Activate flatpak DATA checkbox
            self.flatpakDataCheckBox.setChecked(True)
            # Enable continue button
            self.continueButton.setEnabled(True)
            # Add data to list if not already there
            # if "data" not in self.optionsAddedList:
            self.optionsAddedList.append("data")
            # Auto enable flatpak to list
            self.optionsAddedList.append("flatpak")
        else:
            self.restoreFlatpaksPrograms = False
            self.restoreFlatpaksData = False
            # Disable flatpak DATA checkbox
            self.flatpakDataCheckBox.setChecked(False)
            # Disable data if in list
            # if "data" in self.optionsAddedList:
            self.optionsAddedList.remove("data")

        self.allow_to_continue()

    def on_files_and_folders_clicked(self):
        if self.fileAndFoldersCheckBox.isChecked():
            self.restoreHome = True
            # Enable continue button
            self.continueButton.setEnabled(True)
            # Add files to list
            self.optionsAddedList.append("files")
        else:
            self.restoreHome = False
            # Disable continue button
            self.continueButton.setEnabled(False)
            # if "files" in self.optionsAddedList:
            self.optionsAddedList.remove("files")

        self.allow_to_continue()
  
    def on_system_settings_clicked(self):
        if self.systemSettingsCheckBox.isChecked():
            self.restoreSystemSettings = True
            # Enable continue button
            self.continueButton.setEnabled(True)
            # Add system_settings to list
            self.optionsAddedList.append("system_settings")
        else:
            self.restoreSystemSettings = False
            # Disable continue button
            self.continueButton.setEnabled(False)
            if "system_settings" in self.optionsAddedList:
                self.optionsAddedList.remove("system_settings")

        self.allow_to_continue()

    def allow_to_continue(self):
        # If self.optionsAddedList is not empty, allow it
        if len(self.optionsAddedList) > 0:
            # Enable continue button
            self.continueButton.setEnabled(True)
        else:
            # Disable continue button
            self.continueButton.setEnabled(False)

    def on_back_button_clicked(self):
       widget.setCurrentIndex(widget.currentIndex()-1)

       self.alreadySelectApps = False

    def on_continue_button_clicked(self):
        if self.applicationPackagesCheckBox.isChecked() == True:
            # Write applications exclude list .exclude-application.txt
            # Create a .exclude-applications
            if not os.path.exists(self.excludeAppsLoc):
                    sub.run(f"{createCMDFile} {self.excludeAppsLoc}", shell=True)

            else:
                # Delete before continue
                sub.run(f"rm -rf {self.excludeAppsLoc}", shell=True)
                # Create again
                sub.run(f"{createCMDFile} {self.excludeAppsLoc}", shell=True)

            if self.excludeAppList:
                # Get user installed flatpaks
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(self.excludeAppsLoc, 'w') as configfile:
                    for apps in self.excludeAppList:  
                        configfile.write(f"{apps}\n")
            
        main5 = BACKUPSCREEN()
        widget.addWidget(main5)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def exclude_apps(self, exclude):
        # Only add to exclude, if it not already there
        if exclude not in self.excludeAppList:
            self.excludeAppList.append(exclude)
        else:
            self.excludeAppList.remove(exclude)
        
        # if user deselect all app, application check to False
        if len(self.excludeAppList) == len(self.countOfDebList) or len(self.excludeAppList) == len(self.countOfRPMList):
            self.applicationPackagesCheckBox.setChecked(False)
            # Clean optionsAddedList
            self.optionsAddedList.clear()
            # Disable continue button
            self.continueButton.setEnabled(False)
        else:
            self.applicationPackagesCheckBox.setChecked(True)
            # Enable continue button
            self.continueButton.setEnabled(True)

class BACKUPSCREEN(QWidget):
    def __init__(self):
        super().__init__()
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
        self.title.setFont(QFont("Arial", 28))
        self.title.setText("Transferring Your information")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        """)

        # Description
        self.description = QLabel()
        self.description.setFont(fontSize11px)
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Backup from {appName} " 
            "will been transferred to this PC.")

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont("Arial", 6))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText('<h1>Click on "Restore" to begin.</h1>') 
        
        # Automatically reboot
        self.autoReboot = QCheckBox()
        self.autoReboot.setFont(buttonFontSize)
        self.autoReboot.setText('Automatically reboot after restoring is done. (Recommended)') 
        self.autoReboot.clicked.connect(self.auto_reboot_clicked)

        # Restoring description
        self.whileRestoringDescription = QLabel()
        self.whileRestoringDescription.setFont(fontSize11px)
        self.whileRestoringDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        ################################################################################
        # Images
        ################################################################################
        # Image 1       
        image = QLabel()
        image.setFixedSize(68, 68)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({homeUser}/.local/share/{appNameClose}/src/icons/restore_64px.svg);"
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
            f"background-image: url({homeUser}/.local/share/{appNameClose}/src/icons/arrow.png);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        # Image 3       
        image3 = QLabel()
        image3.setFixedSize(96, 96)
        image3.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({homeUser}/.local/share/{appNameClose}/src/icons/applications-system.svg);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        ################################################################################
        # External device name
        ################################################################################
        widgetDeviceName = QWidget(self)
        widgetDeviceName.setFixedSize(185, 40)
        widgetDeviceName.move(232, 265)

        # Widget device layout
        widgetDeviceLayout = QHBoxLayout(widgetDeviceName)

        # External device name
        self.externalDeviceName = QLabel()
        self.externalDeviceName.setFont(QFont("Arial", 14))
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            # Add userName 
            self.externalDeviceName.setText(mainIniFile.ini_hd_name())
            self.externalDeviceName.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.externalDeviceName.adjustSize()
        
        except:
            pass

        ################################################################################
        # This pc label
        ################################################################################
        widgetThisPCName = QWidget(self)
        widgetThisPCName.setFixedSize(170, 40)
        widgetThisPCName.move(488, 265)

        # This pc name layout
        widgetLayout = QHBoxLayout(widgetThisPCName)
        self.thisPCName = QLabel()
        self.thisPCName.setFont(QFont("Arial", 14))
        self.thisPCName.setText(f"{(userName).capitalize()}")
        self.thisPCName.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.thisPCName.adjustSize()

        ################################################################################
        # Buttons
        ################################################################################
        # Back button
        self.backButton = QPushButton(self)
        self.backButton.setText("Back")
        self.backButton.setFont(buttonFontSize)
        self.backButton.adjustSize()
        self.backButton.move(700, 555)
        self.backButton.setStyleSheet(buttonStylesheet)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))

        # Continue button
        self.startRestoreButton = QPushButton(self)
        self.startRestoreButton.setText("Restore")
        self.startRestoreButton.setFont(buttonFontSize)
        self.startRestoreButton.adjustSize()
        self.startRestoreButton.move(800, 555)
        self.startRestoreButton.setEnabled(True)
        self.startRestoreButton.clicked.connect(self.change_screen)

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addWidget(self.devicesAreadWidget, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.moreDescription, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.whileRestoringDescription, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.autoReboot, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Widget device layouts
        self.imagesLayout.addWidget(image, 1, QtCore.Qt.AlignHCenter)
        self.imagesLayout.addWidget(image2, 0, QtCore.Qt.AlignHCenter)
        self.imagesLayout.addWidget(image3, 1, QtCore.Qt.AlignHCenter)
        widgetDeviceLayout.addWidget(self.externalDeviceName)
        widgetLayout.addWidget(self.thisPCName)

        # Add userName self.set
        self.setLayout(self.verticalLayout)

        self.read_ini_file()

    def read_ini_file(self):
        try:
            self.externalDeviceName.setText(mainIniFile.ini_hd_name())

            ################################################################################
            # Update widgets
            ################################################################################
            # if restoring is running
            if mainIniFile.ini_restoring_is_running() == "true":
                # Show restoring description
                self.whileRestoringDescription.setText(f'Transferring '
                    f"{mainIniFile.ini_current_backup_information()} to the user {userName}...") 
                # Hide more description
                self.moreDescription.hide()
                # Show restoring description
                self.whileRestoringDescription.show()

        except:
            pass

    def change_screen(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w', encoding='utf8') as configfile:  
            config.set('RESTORE', 'is_restore_running', 'true')
            config.write(configfile)

        main6 = START_RESTORING()
        widget.addWidget(main6)

        # Call restore python
        mainRestore = RESTORE()
        mainRestore.begin_settings(
            self.restoreHome,
            self.restoreApplicationsPackages,
            self.restoreFlatpaksPrograms,
            self.restoreFlatpaksData,
            self.restoreSystemSettings,
            self.reboot)
        
        widget.showFullScreen()
        widget.setCurrentIndex(widget.currentIndex()+1)

    def auto_reboot_clicked(self):
        if self.autoReboot.isChecked():
            self.reboot = True
        else:
            self.reboot = False

class START_RESTORING(QWidget):
    def __init__(self):
        super().__init__()
        self.widgets()
            
    def widgets(self):
        # Title layout
        self.titlelLayout = QVBoxLayout()
        self.titlelLayout.setSpacing(20)
        self.titlelLayout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome
        self.title = QLabel()
        self.title.setFont(QFont("Arial", 28))
        self.title.setText("This may take a few minutes...")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        """)

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(fontSize11px)
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText(
            "Don't turn off your PC.\n"
            "This window will automatically close after restoring is done.") 
        self.moreDescription.setStyleSheet("""
        color: gray;
        """)

        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        self.titlelLayout.addStretch()
        self.titlelLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titlelLayout.addWidget(self.moreDescription, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titlelLayout.addStretch()
        self.setLayout(self.titlelLayout)

        # Update
        timer.timeout.connect(self.read_ini_file)
        timer.start(1000) # Update every x seconds
        self.read_ini_file()

    def read_ini_file(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.isRestoreRunning = config['RESTORE']['is_restore_running']

        if self.isRestoreRunning == "false":
            ###############################################################################
            # Update INI file
            ###############################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                # Set auto rebooting to false
                config.set('RESTORE', 'is_restore_running', 'none')
                config.write(configfile)

            exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    mainIniFile = UPDATEINIFILE()
    main = WELCOMESCREEN()
    # main2 = CHOOSEDEVICE()
    main4 = PREBACKUP()
    # main5 = BACKUPSCREEN()
    # main6 = START_RESTORING()

    widget.addWidget(main4)   
    widget.setCurrentWidget(main4)   

    widget.setWindowTitle("Migration Assistant")
    widget.setWindowIcon(QIcon(src_migration_assistant_96px)) 
    widget.setFixedSize(900,600)
    widget.show()

    app.exit(app.exec())