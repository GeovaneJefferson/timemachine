#! /usr/bin/python3
from setup import *
from device_location import device_location
from package_manager import package_manager
from restore_cmd import RESTORE
from read_ini_file import UPDATEINIFILE
from stylesheet import *
from get_packages_size import get_packages_size
from get_system_settings_size import get_system_settings_size
from package_manager import package_manager
from get_backup_home_name_and_size import get_backup_folders_size_pretty
from save_info import save_info


class WELCOMESCREEN(QWidget):
    def __init__(self):
        super(WELCOMESCREEN, self).__init__()
        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if app.palette().window().color().getRgb()[0] < 55:
            self.leftBackgroundColorDetector = leftBackgroundColorStylesheetDark
            self.buttonStylesheetDetector = buttonStylesheetDark
            self.externalWindowbackgroundDetector = externalWindowbackgroundStylesheetDark
            self.separatorstylesheetDetector = separetorLineDark
        else:
            self.leftBackgroundColorDetector = leftBackgroundColorStylesheet
            self.buttonStylesheetDetector = buttonStylesheet
            self.externalWindowbackgroundDetector = externalWindowbackgroundStylesheet
            self.separatorstylesheetDetector = separetorLine

        self.widgets()

    def widgets(self):
        # Title layout
        self.titlelLayout = QVBoxLayout()
        self.titlelLayout.setSpacing(20)
        self.titlelLayout.setContentsMargins(20, 20, 20, 20)
        
        # Image       
        image = QLabel()
        image.setFixedSize(212,212)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_migration_assistant_icon_212px});"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")
        
        # Welcome
        self.title = QLabel()
        self.title.setFont(QFont(mainFont,migrationAssistantTitle))
        self.title.setText("Migration Assistant")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet(
        """
            font-weight: Bold;
            color:gray;
        """)

       # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont(mainFont,fontSize11px))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText("Use Migration Assistant to restore information such as "
            "Applications, Files, Folders and more to this PC.") 

        ################################################################################
        # Buttons
        ################################################################################
        widgetButton = QWidget(self)
        widgetButton.setFixedSize(900,60)
        widgetButton.move(0,600-widgetButton.height())
        widgetButton.setStyleSheet(self.separatorstylesheetDetector)

        widgetButtonLayout = QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)
        
        # Continue button
        self.continueButton = QPushButton()
        self.continueButton.setFixedHeight(buttonHeightSize)
        self.continueButton.setText("   Continue   ")
        self.continueButton.setFont(QFont(mainFont,buttonFontSize))
        self.continueButton.adjustSize()
        self.continueButton.setStyleSheet(self.buttonStylesheetDetector)
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

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if app.palette().window().color().getRgb()[0] < 55:
            self.buttonStylesheetDetector = buttonStylesheetDark
            self.separatorstylesheetDetector = separetorLineDark
            self.availableDeviceButtonDetector = availableDeviceButtonStylesheetDark
        else:
            self.buttonStylesheetDetector = buttonStylesheet
            self.separatorstylesheetDetector = separetorLine
            self.availableDeviceButtonDetector = availableDeviceButtonStylesheet

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
        self.title.setFont(QFont(mainFont,migrationAssistantTitle))
        self.title.setText("Restore Information To This PC")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        # Description
        self.description = QLabel()
        self.description.setFont(QFont(mainFont,fontSize11px))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Select a {appName} " 
            "backup disk to retore it's information to this PC.")

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont(mainFont,fontSize11px))
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
        widgetButton.setStyleSheet(self.separatorstylesheetDetector)

        widgetButtonLayout = QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)
        
        # Back button
        self.backButton = QPushButton()
        self.backButton.setText("   Back   ")
        self.backButton.setFont(QFont(mainFont,buttonFontSize))
        self.backButton.setFixedHeight(buttonHeightSize)
        self.backButton.adjustSize()
        self.backButton.setStyleSheet(self.buttonStylesheetDetector)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))

        # Continue button
        self.continueButton = QPushButton()
        self.continueButton.setText("   Continue  ")
        self.continueButton.setFont(QFont(mainFont,buttonFontSize))
        self.continueButton.setFixedHeight(buttonHeightSize)
        self.continueButton.adjustSize()
        self.continueButton.setEnabled(False)
        self.continueButton.setStyleSheet(self.buttonStylesheetDetector)
        self.continueButton.clicked.connect(self.on_continue_clicked)
        
        # Refresh button
        # self.refreshButton = QPushButton()
        # self.refreshButton.setFixedSize(28,28)
        # self.refreshButton.setIcon(QIcon())
        # self.refreshButton.setIconSize(QtCore.QSize(22,22))
        # self.refreshButton.setStyleSheet(self.buttonStylesheetDetector)
        # self.refreshButton.clicked.connect(self.show_on_screen)
        
        widgetButtonLayout.addStretch()
        widgetButtonLayout.addWidget(self.backButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        widgetButtonLayout.addWidget(self.continueButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.show_on_screen()

    def show_on_screen(self):
        print("Searching devices...")
  
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
                        self.availableDevices.setFont(QFont(mainFont,fontSize11px))
                        self.availableDevices.adjustSize()
                        self.availableDevices.clicked.connect(
                            lambda *args, output=output: self.on_device_clicked(output))
                        self.availableDevices.setStyleSheet(self.availableDeviceButtonDetector)
           
                        # Image
                        image = QLabel(self.availableDevices)
                        image.setFixedSize(96, 96)
                        image.move(42,30)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                                f"background-image: url({src_restore_icon});"
                                "background-repeat: no-repeat;"
                                "background-color: transparent;"
                                "border-radius:0px solid transparent;"
                            "}")

                        self.devicesAreaLayout.addWidget(self.availableDevices)

        except Exception:
            pass

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addWidget(self.devicesAreadWidget,0,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.verticalLayout.addWidget(self.refreshButton, 0,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.moreDescription,1,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.setLayout(self.verticalLayout)

    def on_device_clicked(self, output):
        if self.availableDevices.isChecked():
            self.chooseDevice = output
            self.continueButton.setEnabled(True)
        else:
            self.continueButton.setEnabled(False)
            
    def on_continue_clicked(self):
        ################################################################################
        # Update INI file
        ################################################################################
        save_info(self.chooseDevice)

        # config = configparser.ConfigParser()
        # config.read(src_user_config)
        # with open(src_user_config, 'w') as configfile:
        #     if str(supportedDEBPackageManager) in package_manager():
        #         # Save user's os name
        #         config.set(f'INFO', 'packageManager', f'{debFolderName}')

        #     elif str(supportedRPMPackageManager) in package_manager():
        #         # Save user's os name
        #         config.set(f'INFO', 'packageManager', f'{rpmFolderName}')

        #     # Update INI file
        #     if device_location():
        #         config.set(f'EXTERNAL', 'hd', f'{media}/{userName}/{self.chooseDevice}')

        #     elif not device_location():
        #         config.set(f'EXTERNAL', 'hd', f'{run}/{userName}/{self.chooseDevice}')

        #     config.set('EXTERNAL', 'name', f'{self.chooseDevice}')
        #     config.write(configfile)

        main3 = PREBACKUP()
        widget.addWidget(main3) 
        widget.setCurrentIndex(widget.currentIndex()+1)

class PREBACKUP(QWidget):
    def __init__(self):
        super().__init__()
        self.hasItensInsideToContinueList = []
        self.excludeAppList = []
        self.countOfDebList = []
        self.countOfRPMList = []

        self.alreadyShowingApplicationInformation = False
        self.alreadyShowingFlatpakInformation = False
        self.alreadyShowingFlatpakDataInformation = False
        self.alreadyShowingFilesAndSoldersInformation = False
        self.alreadyShowingSystemSettingsInformation = False
        
        self.restoreHome = bool()
        self.restoreApplicationsPackages = bool()
        self.restoreFlatpaksPrograms = bool()
        self.restoreFlatpaksData = bool()
        self.restoreSystemSettings = bool()
        self.reboot = bool()

        self.itensToRestore = {
            'restoreHome': bool(),
            'restoreApplicationsPackages': bool(),
            'restoreFlatpaksPrograms': bool(),
            'restoreFlatpaksData': bool(),
            'reboot': bool()}

        # Delete .exclude-applications.txt first
        if os.path.exists(mainIniFile.exclude_appsications_location()):
            sub.run(f"rm -rf {mainIniFile.exclude_appsications_location()}",shell=True)

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if app.palette().window().color().getRgb()[0] < 55:
            self.buttonStylesheetDetector = buttonStylesheetDark
            self.separatorstylesheetDetector = separetorLineDark
            self.applicationBackgroundBoxDetector = leftBackgroundColorStylesheetDark
        else:
            self.buttonStylesheetDetector = buttonStylesheet
            self.separatorstylesheetDetector = separetorLine
            self.applicationBackgroundBoxDetector = leftBackgroundColorStylesheet

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
        self.scrollOptions.setStyleSheet(self.applicationBackgroundBoxDetector)

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
        self.title.setFont(QFont(mainFont,migrationAssistantTitle))
        self.title.setText("Select The Information To Restore")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
            font-weight: Bold;
            color:gray;
        """)

        # Description
        self.description = QLabel()
        self.description.setFont(QFont(mainFont,fontSize11px))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText("Choose which information you'd like to restore to this PC.")
        
        ################################################################################
        # Application checkbox (DATA)
        ################################################################################
        self.flatpakDataCheckBox = QCheckBox()
        self.flatpakDataCheckBox.setText(" Flatpak (Data)")
        self.flatpakDataCheckBox.setFont(QFont(mainFont,fontSize11px))
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
        widgetButton.setStyleSheet(self.separatorstylesheetDetector)

        self.widgetButtonLayout = QHBoxLayout(widgetButton)
        self.widgetButtonLayout.setSpacing(10)
        
        # Back button
        self.backButton = QPushButton()
        self.backButton.setText("   Back   ")
        self.backButton.setFont(QFont(mainFont,buttonFontSize))
        self.backButton.adjustSize()
        self.backButton.setStyleSheet(self.buttonStylesheetDetector)
        self.backButton.setFixedHeight(buttonHeightSize)
        self.backButton.clicked.connect(self.on_back_button_clicked)

        # Continue button
        self.continueButton = QPushButton()
        self.continueButton.setText("   Continue   ")
        self.continueButton.setFont(QFont(mainFont,buttonFontSize))
        self.continueButton.adjustSize()
        self.continueButton.setFixedHeight(buttonHeightSize)
        self.continueButton.setStyleSheet(self.buttonStylesheetDetector)
        # No item in the list
        if not self.hasItensInsideToContinueList:
            self.continueButton.setEnabled(False)
        self.continueButton.clicked.connect(self.on_continue_button_clicked)

        self.applications_option()

    def applications_option(self):
        ################################################################################
        # Application checkbox
        ################################################################################
        self.applicationPackagesCheckBox = QCheckBox()
        self.applicationPackagesCheckBox.setText(f" Applications "
            "                              "
            f"                           {get_packages_size()}")
        self.applicationPackagesCheckBox.setFont(QFont(mainFont,fontSize11px))
        self.applicationPackagesCheckBox.adjustSize()
        self.applicationPackagesCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/folder-templates.svg"))
        self.applicationPackagesCheckBox.setIconSize(QtCore.QSize(32,32))
        self.applicationPackagesCheckBox.setToolTip(
            "This will reinstall: \n"
            "* All backup's deb packages.")
        self.applicationPackagesCheckBox.clicked.connect(self.on_application_clicked)
        
        ################################################################################
        # More informations about
        ################################################################################
        baseWidgetForMoreInformation = QWidget()

        self.showMoreApplicationInformationWidget = QScrollArea()
        self.showMoreApplicationInformationWidget.setFixedHeight(0)
        self.showMoreApplicationInformationWidget.setWidgetResizable(True)
        self.showMoreApplicationInformationWidget.setWidget(baseWidgetForMoreInformation)

        self.showMoreApplicationInformationLayout = QVBoxLayout(baseWidgetForMoreInformation)
        self.showMoreApplicationInformationLayout.setSpacing(5)

        ################################################################################
        if get_packages_size() != "None":
            # Application size information
            self.applicationSizeInformation = QLabel()
            self.applicationSizeInformation.setText(f"{get_packages_size()}")
            self.applicationSizeInformation.adjustSize()
            self.applicationSizeInformation.setFont(QFont(mainFont,buttonFontSize))
            self.applicationSizeInformation.setAlignment(QtCore.Qt.AlignRight)
    
        self.flatpak_names_option()

    def flatpak_names_option(self):
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
                self.flatpakCheckBox.setFont(QFont(mainFont,fontSize11px))
                self.flatpakCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/application-vnd.flatpak.ref.svg"))
                self.flatpakCheckBox.setIconSize(QtCore.QSize(32,32))
                self.flatpakCheckBox.setToolTip("This will reinstall: \n"
                    "* All flatpak applications")
                self.flatpakCheckBox.clicked.connect(self.on_flatpak_clicked)

            ################################################################################
            # More informations about
            ################################################################################
            baseWidgetForMoreInformation = QWidget()

            self.showMoreFlatpakInformationWidget = QScrollArea()
            self.showMoreFlatpakInformationWidget.setFixedHeight(0)
            self.showMoreFlatpakInformationWidget.setWidgetResizable(True)
            self.showMoreFlatpakInformationWidget.setWidget(baseWidgetForMoreInformation)

            self.showMoreFlatpakInformationLayout = QVBoxLayout(baseWidgetForMoreInformation)
            self.showMoreFlatpakInformationLayout.setSpacing(5)

        except:
            pass
        
        self.flatpak_data_option()

    def flatpak_data_option(self):
        ################################################################################
        # Flatpaks DATA checkbox
        ################################################################################
        try:
            # Get flatpak data size
            self.flatpakDataSize = os.popen(f"du -hs {mainIniFile.ini_external_location()}/{baseFolderName}/{applicationFolderName}")
            self.flatpakDataSize = self.flatpakDataSize.read().strip("\t").strip("\n").replace(f"{mainIniFile.ini_external_location()}/{baseFolderName}/{applicationFolderName}", "").replace("\t", "")
        
            # Application size information
            self.applicationSizeInformation = QLabel()
            self.applicationSizeInformation.setText(f"{self.flatpakDataSize}")
            self.applicationSizeInformation.setFont(QFont(mainFont,buttonFontSize))
            self.applicationSizeInformation.adjustSize()
            
            ################################################################################
            # More informations about
            ################################################################################
            baseWidgetForMoreInformation = QWidget()

            self.showMoreFlatpakDataInformationWidget = QScrollArea()
            self.showMoreFlatpakDataInformationWidget.setFixedHeight(0)
            self.showMoreFlatpakDataInformationWidget.setWidgetResizable(True)
            self.showMoreFlatpakDataInformationWidget.setWidget(baseWidgetForMoreInformation)

            self.showMoreFlatpakDataInformationLayout = QVBoxLayout(baseWidgetForMoreInformation)
            self.showMoreFlatpakDataInformationLayout.setSpacing(5)

        except:
            pass
        
        self.system_settings_option()

    def system_settings_option(self):
        ################################################################################
        # System Settings checkbox
        ################################################################################
        try:
            # System settings size information
            self.SystemSettingsSizeInformation = QLabel()
            self.SystemSettingsSizeInformation.setText(f"{str(get_system_settings_size())}")
            self.SystemSettingsSizeInformation.setFont(QFont(mainFont,buttonFontSize))
            self.SystemSettingsSizeInformation.adjustSize()
        
            self.systemSettingsCheckBox = QCheckBox()
            self.systemSettingsCheckBox.setText(" System Settings"
                "                               "
                f"                       {self.SystemSettingsSizeInformation.text()}")
            self.systemSettingsCheckBox.setFont(QFont(mainFont,fontSize11px))
            self.systemSettingsCheckBox.adjustSize()
            self.systemSettingsCheckBox.setToolTip("This will restore: \n"
                "* Wallpaper\n"
                "* Theme\n"
                "   -- Icon\n"
                "   -- Cursor")
            self.systemSettingsCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/preferences-system.svg"))
            self.systemSettingsCheckBox.setIconSize(QtCore.QSize(34,34))
            self.systemSettingsCheckBox.clicked.connect(self.on_system_settings_clicked)
            
            ################################################################################
            # More informations about
            ################################################################################
            baseWidgetForMoreInformation = QWidget()

            self.showMoreSystemSettingsInformationWidget = QScrollArea()
            self.showMoreSystemSettingsInformationWidget.setFixedHeight(0)
            self.showMoreSystemSettingsInformationWidget.setWidgetResizable(True)
            self.showMoreSystemSettingsInformationWidget.setWidget(baseWidgetForMoreInformation)

            self.showMoreSystemSettingsInformationLayout = QVBoxLayout(baseWidgetForMoreInformation)
            self.showMoreSystemSettingsInformationLayout.setSpacing(5)

        except:
            pass

        self.files_and_folders_option()

    def files_and_folders_option(self):
        ################################################################################
        # Files & Folders checkbox
        ################################################################################
        try:
            # Files and Folders checkbox        
            self.fileAndFoldersCheckBox = QCheckBox()
            if get_backup_folders_size_pretty() != None:
                self.fileAndFoldersCheckBox.setText(" Files and Folders"
                    "                               "
                    f"                      {get_backup_folders_size_pretty()}")
            else:
                self.fileAndFoldersCheckBox.setText(" Files and Folders ")
                
            self.fileAndFoldersCheckBox.setFont(QFont(mainFont,fontSize11px))
            self.fileAndFoldersCheckBox.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/text-x-generic.svg"))
            self.fileAndFoldersCheckBox.setIconSize(QtCore.QSize(32,32))
            self.fileAndFoldersCheckBox.setToolTip("This will restore: \n"
                "* All recents back up files and folders")
            self.fileAndFoldersCheckBox.clicked.connect(self.on_files_and_folders_clicked)

            ################################################################################
            # More informations about
            ################################################################################
            baseWidgetForMoreInformation = QWidget()

            self.showMoreFileAndFoldersInformationWidget = QScrollArea()
            self.showMoreFileAndFoldersInformationWidget.setFixedHeight(0)
            self.showMoreFileAndFoldersInformationWidget.setWidgetResizable(True)
            self.showMoreFileAndFoldersInformationWidget.setWidget(baseWidgetForMoreInformation)

            self.showMoreFileAndFoldersInformationLayout = QVBoxLayout(baseWidgetForMoreInformation)
            self.showMoreFileAndFoldersInformationLayout.setSpacing(5)

        except Exception as error:
            print("Files and Folders",error)
            pass
        
        ################################################################################
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.scrollOptions, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.verticalLayoutForOptions.addWidget(self.applicationPackagesCheckBox)
        self.verticalLayoutForOptions.addWidget(self.showMoreApplicationInformationWidget)

        # self.verticalLayoutForOptions.addWidget(self.flatpakCheckBox)
        # self.verticalLayoutForOptions.addWidget(self.showMoreApplicationInformationWidget)
        
        self.verticalLayoutForOptions.addWidget(self.flatpakDataCheckBox)
        self.verticalLayoutForOptions.addWidget(self.showMoreFlatpakDataInformationWidget)
        
        self.verticalLayoutForOptions.addWidget(self.fileAndFoldersCheckBox)
        self.verticalLayoutForOptions.addWidget(self.showMoreFileAndFoldersInformationWidget)
        
        self.verticalLayoutForOptions.addWidget(self.systemSettingsCheckBox)
        self.verticalLayoutForOptions.addWidget(self.showMoreSystemSettingsInformationWidget)
        self.verticalLayout.addStretch(5)
        
        self.widgetButtonLayout.addStretch()
        self.widgetButtonLayout.addWidget(self.backButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.widgetButtonLayout.addWidget(self.continueButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.setLayout(self.verticalLayout)

        self.has_flatpak_names_to_install()

    def has_flatpak_names_to_install(self):
        dummy = []
        try:
            # Look for flatpakTxt inside external device
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(f"{mainIniFile.flatpak_txt_location()}", 'r') as output:
                output = output.read().strip()
                dummy.append(output)

            if dummy:
                self.flatpakCheckBox.setEnabled(True)
            else:
                self.flatpakCheckBox.setEnabled(False)  

        except FileNotFoundError:
            pass

        self.has_applications_packages_to_install()

    def has_applications_packages_to_install(self):
        dummyList = []

        try:
            if package_manager() == rpmFolderName:
                for outputRPM in os.listdir(f"{mainIniFile.rpm_main_folder()}/"):
                    dummyList.append(outputRPM)

            elif package_manager() == debFolderName:
                for outputDeb in os.listdir(f"{mainIniFile.deb_main_folder()}/"):
                    dummyList.append(outputDeb)
            
            if dummyList:
                self.applicationPackagesCheckBox.setEnabled(True)
            else:
                self.applicationPackagesCheckBox.setEnabled(False)  

            dummyList.clear()
            
        except:
            pass

        self.find_applications_data()

    def find_applications_data(self):
        dummy = []

        try:
            for output in os.listdir(f"{mainIniFile.application_var_folder()}/"):
                dummy.append(output)

            if dummy:
                self.flatpakDataCheckBox.setEnabled(True)
            else:
                self.flatpakDataCheckBox.setEnabled(False)  
            
            dummy.clear()

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
        self.system_settings_list = []
        try:
            for output in os.listdir(f"{mainIniFile.wallpaper_main_folder()}/"):
                self.system_settings_list.append(output)

            if self.system_settings_list:
                self.activate_system_settings()

            for output in os.listdir(f"{mainIniFile.icon_main_folder()}/"):
                self.system_settings_list.append(output)

            if self.system_settings_list:
                self.activate_system_settings()

            for output in os.listdir(f"{mainIniFile.gtk_theme_main_folder()}/"):
                self.system_settings_list.append(output)
            
            if self.system_settings_list:
                self.activate_system_settings()

            for output in os.listdir(f"{mainIniFile.cursor_main_folder()}/"):
                self.system_settings_list.append(output)
            
            if self.system_settings_list:
                self.activate_system_settings()

            for output in os.listdir(f"{mainIniFile.color_scheme_main_folder()}/"):
                self.system_settings_list.append(output)

            if self.system_settings_list:
                self.activate_system_settings()

            for output in os.listdir(f"{mainIniFile.plasma_main_folder()}/"):
                self.system_settings_list.append(output)

            if self.system_settings_list:
                self.activate_system_settings()
            
            for output in os.listdir(f"{mainIniFile.aurorae_main_folder()}/"):
                self.system_settings_list.append(output)

            if self.system_settings_list:
                self.activate_system_settings()
        except:
            pass
                
    def activate_system_settings(self):
        if self.system_settings_list:
            self.systemSettingsCheckBox.setEnabled(True)
        else:
            self.systemSettingsCheckBox.setEnabled(False)  

        # Empty list
        self.system_settings_list.clear()

    def on_application_clicked(self):
        # Open applications checkboxes
        if not self.alreadyShowingApplicationInformation:
            self.showMoreApplicationInformationWidget.setFixedHeight(240)
            self.alreadyShowingApplicationInformation = True
        else:
            self.showMoreApplicationInformationWidget.setFixedHeight(0)
            self.alreadyShowingApplicationInformation = False
        
        if self.applicationPackagesCheckBox.isChecked():
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile: 
                config.set('RESTORE', 'applications_packages', 'true')
                config.write(configfile)

            self.applicationPackagesCheckBox.setChecked(True)
            self.continueButton.setEnabled(True)
            self.hasItensInsideToContinueList.append("packages")

            # DEP
            if package_manager() == debFolderName:
                for exclude in os.listdir(f"{mainIniFile.deb_main_folder()}"):
                    # Exclude
                    # exclude = exclude.split("_")[0].split("-")[0]
                    # Checkbox
                    dummyCheckBox = QCheckBox()
                    dummyCheckBox.setText(exclude.capitalize())
                    dummyCheckBox.setChecked(True)
                    self.countOfDebList.append(exclude)
                    dummyCheckBox.clicked.connect(lambda *args, exclude=exclude: self.exclude_apps(exclude))

                    self.showMoreApplicationInformationLayout.addWidget(dummyCheckBox)
            # RPM
            elif package_manager() == rpmFolderName:
                for exclude in os.listdir(f"{mainIniFile.rpm_main_folder()}"):
                    # Exclude
                    # exclude = exclude.split("_")[0].split("-")[0]
                    # Checkbox
                    dummyCheckBox = QCheckBox()
                    dummyCheckBox.setText(exclude.capitalize())
                    dummyCheckBox.setChecked(True)
                    self.countOfDebList.append(exclude)
                    dummyCheckBox.clicked.connect(lambda *args, exclude=exclude: self.exclude_apps(exclude))

                    self.showMoreApplicationInformationLayout.addWidget(dummyCheckBox)
        else:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile: 
                config.set('RESTORE', 'applications_packages', 'false')
                config.write(configfile)

            self.hasItensInsideToContinueList.remove("packages")
            self.excludeAppList.clear()

            # Remove applications checkboxes
            for i in range(self.showMoreApplicationInformationLayout.count()):
                item = self.showMoreApplicationInformationLayout.itemAt(i)
                widget = item.widget()
                widget.deleteLater()
                i -= 1

        self.allow_to_continue()

    # TODO
    def on_flatpak_clicked(self):
        # # Open flatpak checkboxes
        # if not self.alreadyShowingFlatpakInformation:
        #     self.showMoreFlatpakInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingFlatpakInformation = True
        # else:
        #     self.showMoreFlatpakInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingFlatpakInformation = False
        
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w', encoding='utf8') as configfile: 
            if self.flatpakCheckBox.isChecked():
                config.set('RESTORE', 'applications_flatpak_names', 'true')

                self.flatpakCheckBox.setChecked(True)
                self.continueButton.setEnabled(True)
                self.hasItensInsideToContinueList.append("flatpak")
            else:
                config.set('RESTORE', 'applications_flatpak_names', 'false')

                self.flatpakCheckBox.setChecked(False)
                self.hasItensInsideToContinueList.remove("flatpak")
            
            config.write(configfile)

        self.allow_to_continue()

    def on_applications_data_clicked(self):
        # # Open flatpak data checkboxes
        # if not self.alreadyShowingFlatpakDataInformation:
        #     self.showMoreFlatpakDataInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingFlatpakDataInformation = True
        # else:
        #     self.showMoreFlatpakDataInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingFlatpakDataInformation = False
        
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w', encoding='utf8') as configfile:  
            if self.flatpakDataCheckBox.isChecked():
                config.set('RESTORE', 'applications_data', 'true')

                self.flatpakDataCheckBox.setChecked(True)
                self.continueButton.setEnabled(True)
                self.hasItensInsideToContinueList.append("data")
                self.hasItensInsideToContinueList.append("flatpak")
            else:
                config.set('RESTORE', 'applications_data', 'false')
                self.restoreFlatpaksPrograms = False
                self.restoreFlatpaksData = False

                self.flatpakDataCheckBox.setChecked(False)
                self.hasItensInsideToContinueList.remove("data")
            
            config.write(configfile)

        self.allow_to_continue()

    def on_files_and_folders_clicked(self):
        # # Open files and folder checkboxes
        # if not self.alreadyShowingFilesAndSoldersInformation:
        #     self.showMoreFileAndFoldersInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingFilesAndSoldersInformation = True
        # else:
        #     self.showMoreFileAndFoldersInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingFilesAndSoldersInformation = False
        
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w', encoding='utf8') as configfile:  
            if self.fileAndFoldersCheckBox.isChecked():
                config.set('RESTORE', 'files_and_folders', 'true')

                self.continueButton.setEnabled(True)
                self.hasItensInsideToContinueList.append("files")
            else:
                config.set('RESTORE', 'files_and_folders', 'false')
                self.continueButton.setEnabled(False)
                self.hasItensInsideToContinueList.remove("files")

            config.write(configfile)
            
        self.allow_to_continue()
  
    def on_system_settings_clicked(self):
        # # Open system settings checkboxe
        # if not self.alreadyShowingSystemSettingsInformation:
        #     self.showMoreSystemSettingsInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingSystemSettingsInformation = True
        # else:
        #     self.showMoreSystemSettingsInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingSystemSettingsInformation = False
        
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w', encoding='utf8') as configfile:  
            if self.systemSettingsCheckBox.isChecked():
                config.set('RESTORE', 'system_settings', 'true')

                self.continueButton.setEnabled(True)
                self.hasItensInsideToContinueList.append("system_settings")
            else:
                config.set('RESTORE', 'system_settings', 'false')
                self.continueButton.setEnabled(False)
                if "system_settings" in self.hasItensInsideToContinueList:
                    self.hasItensInsideToContinueList.remove("system_settings")
            
            config.write(configfile)

        self.allow_to_continue()

    def allow_to_continue(self):
        # If self.hasItensInsideToContinueList is not empty, allow it
        if len(self.hasItensInsideToContinueList) > 0:
            self.continueButton.setEnabled(True)
        else:
            self.continueButton.setEnabled(False)

    def on_back_button_clicked(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

        self.alreadyShowingApplicationInformation = False
        self.alreadyShowingFlatpakInformation = False
        self.alreadyShowingFlatpakDataInformation = False
        self.alreadyShowingFilesAndSoldersInformation = False
        self.alreadyShowingSystemSettingsInformation = False
        
    def on_continue_button_clicked(self):
        if self.applicationPackagesCheckBox.isChecked() == True:
            # Write applications exclude list .exclude-application.txt
            # Create a .exclude-applications
            if not os.path.exists(mainIniFile.exclude_appsications_location()):
                    sub.run(f"{createCMDFile} {mainIniFile.exclude_appsications_location()}", shell=True)

            else:
                # Delete before continue
                sub.run(f"rm -rf {mainIniFile.exclude_appsications_location()}", shell=True)
                # Create again
                sub.run(f"{createCMDFile} {mainIniFile.exclude_appsications_location()}", shell=True)

            if self.excludeAppList:
                # Get user installed flatpaks
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(mainIniFile.exclude_appsications_location(), 'w') as configfile:
                    for apps in self.excludeAppList:  
                        configfile.write(f"{apps}\n")
            
        main4 = BACKUPSCREEN()
        widget.addWidget(main4)
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
            # Clean hasItensInsideToContinueList
            self.hasItensInsideToContinueList.clear()
            # Disable continue button
            self.continueButton.setEnabled(False)
        else:
            self.applicationPackagesCheckBox.setChecked(True)
            # Enable continue button
            self.continueButton.setEnabled(True)

class BACKUPSCREEN(QWidget):
    def __init__(self):
        super().__init__()
        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if app.palette().window().color().getRgb()[0] < 55:
            self.buttonStylesheetDetector = buttonStylesheetDark
            self.separatorstylesheetDetector = separetorLineDark
        else:
            self.buttonStylesheetDetector = buttonStylesheet
            self.separatorstylesheetDetector = separetorLine

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
        self.title.setFont(QFont(mainFont,migrationAssistantTitle))
        self.title.setText("Begin Restoring")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        # Description
        self.description = QLabel()
        self.description.setFont(QFont(mainFont,fontSize11px))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Backup from {appName} " 
            "will been transferred to this PC.")

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont(mainFont,6))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText('<h1>Click on "Restore" to begin.</h1>') 
        
        # Automatically reboot
        self.autoReboot = QCheckBox()
        self.autoReboot.setFont(QFont(mainFont,buttonFontSize))
        self.autoReboot.setText('Automatically reboot after restoring is done. (Recommended)') 
        self.autoReboot.clicked.connect(self.auto_reboot_clicked)

        # Restoring description
        self.whileRestoringDescription = QLabel()
        self.whileRestoringDescription.setFont(QFont(mainFont,fontSize11px))
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
        self.externalDeviceName.setFont(QFont(mainFont,14))
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
        self.thisPCName.setFont(QFont(mainFont,14))
        self.thisPCName.setText(f"{(userName).capitalize()}")
        self.thisPCName.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.thisPCName.adjustSize()

        ################################################################################
        # Buttons
        ################################################################################
        widgetButton = QWidget(self)
        widgetButton.setFixedSize(900,60)
        widgetButton.move(0,600-widgetButton.height())
        widgetButton.setStyleSheet(self.separatorstylesheetDetector)

        widgetButtonLayout = QHBoxLayout(widgetButton)
        widgetButtonLayout.setSpacing(10)
        
        # Back button
        self.backButton = QPushButton()
        self.backButton.setText("   Back   ")
        self.backButton.setFont(QFont(mainFont,buttonFontSize))
        self.backButton.adjustSize()
        self.backButton.setFixedHeight(buttonHeightSize)
        self.backButton.setStyleSheet(self.buttonStylesheetDetector)
        self.backButton.clicked.connect(lambda *args: widget.setCurrentIndex(widget.currentIndex()-1))

        # Continue button
        self.startRestoreButton = QPushButton()
        self.startRestoreButton.setText("   Restore   ")
        self.startRestoreButton.setFont(QFont(mainFont,buttonFontSize))
        self.startRestoreButton.adjustSize()
        self.startRestoreButton.setFixedHeight(buttonHeightSize)
        self.startRestoreButton.setEnabled(True)
        self.startRestoreButton.setStyleSheet(useDiskButtonStylesheet)
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
        widgetButtonLayout.addWidget(self.backButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        widgetButtonLayout.addStretch()
        widgetButtonLayout.addWidget(self.backButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        widgetButtonLayout.addWidget(self.startRestoreButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

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
        
        sub.Popen(f"python3 {src_restore_cmd_py}",shell=True)
        main5 = START_RESTORING()
        widget.addWidget(main5)
        
        widget.showFullScreen()
        widget.setCurrentIndex(widget.currentIndex()+1)

    def auto_reboot_clicked(self):
        if self.autoReboot.isChecked():
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:  
                config.set('INFO', 'auto_reboot', 'true')
                config.write(configfile)
        else:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w', encoding='utf8') as configfile:  
                config.set('INFO', 'auto_reboot', 'false')
                config.write(configfile)

class START_RESTORING(QWidget):
    def __init__(self):
        super().__init__()
        self.widgets()
            
    def widgets(self):
        # Title layout
        self.titlelLayout = QVBoxLayout()
        self.titlelLayout.setSpacing(20)
        self.titlelLayout.setContentsMargins(20, 20, 20, 20)
        
        self.settingsUP = QLabel()
        self.settingsUP.setFont(QFont(mainFont,migrationAssistantTitle))
        self.settingsUP.setText("Setting Up Your PC...")
        self.settingsUP.setAlignment(QtCore.Qt.AlignHCenter)
        self.settingsUP.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        self.title = QLabel()
        self.title.setFont(QFont(mainFont,16))
        self.title.setText("This may take a few minutes...")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        # More description
        self.moreDescription = QLabel()
        self.moreDescription.setFont(QFont(mainFont,fontSize11px))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText(
            "Don't turn off your PC.\n"
            "This window will automatically close after restoring is done.") 
        
        # Image       
        image = QLabel()
        image.setFixedSize(320,320)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_settings_up_icon});"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")
        
        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        self.titlelLayout.addStretch()
        self.titlelLayout.addWidget(self.settingsUP, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titlelLayout.addWidget(image, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
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
    # main3 = PREBACKUP()
    # main4 = BACKUPSCREEN()
    # main5 = START_RESTORING()

    widget.addWidget(main)   
    widget.setCurrentWidget(main)   
    widget.setWindowTitle("Migration Assistant")
    widget.setWindowIcon(QIcon(src_migration_assistant_icon_212px)) 
    widget.setFixedSize(900,600)
    widget.show()

    app.exit(app.exec())