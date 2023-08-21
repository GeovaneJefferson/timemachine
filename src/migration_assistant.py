#! /usr/bin/python3
from setup import *
from device_location import device_location
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE
from stylesheet import *
from get_packages_size import get_packages_size
from get_system_settings_size import get_system_settings_size
from package_manager import package_manager
from get_backup_home_name_and_size import get_backup_folders_size_pretty
from save_info import save_info
from detect_theme_color import detect_theme_color
# from restore_cmd import RESTORE


class WelcomeScreen(QWidget):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if detect_theme_color(APP):
            self.left_background_color_detector=leftBackgroundColorStylesheetDark
            self.button_stylesheet_detector=buttonStylesheetDark
            self.external_window_background_detector=externalWindowbackgroundStylesheetDark
            self.separator_stylesheet_detector=separetorLineDark
        else:
            self.left_background_color_detector=leftBackgroundColorStylesheet
            self.button_stylesheet_detector=buttonStylesheet
            self.external_window_background_detector=externalWindowbackgroundStylesheet
            self.separator_stylesheet_detector=separetorLine

        self.widgets()

    def widgets(self):
        # Title layout
        self.titlel_layout=QVBoxLayout()
        self.titlel_layout.setSpacing(20)
        self.titlel_layout.setContentsMargins(20, 20, 20, 20)
        
        # Image       
        image=QLabel()
        image.setFixedSize(212,212)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({SRC_MIGRATION_ASSISTANT_ICON_212PX});"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")
        
        # Welcome
        self.title=QLabel()
        self.title.setFont(QFont(MAIN_FONT,MIGRATION_ASSISTANT_TITLE))
        self.title.setText("Migration Assistant")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet(
        """
            font-weight: Bold;
            color:gray;
        """)

       # More description
        self.more_description=QLabel()
        self.more_description.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.more_description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.more_description.setText("Use Migration Assistant to restore information such as "
            "Applications, Files, Folders and more to this PC.") 

        ################################################################################
        # Buttons
        ################################################################################
        widget_button=QWidget(self)
        widget_button.setFixedSize(900,60)
        widget_button.move(0,600-widget_button.height())
        widget_button.setStyleSheet(self.separator_stylesheet_detector)

        widget_button_layout=QHBoxLayout(widget_button)
        widget_button_layout.setSpacing(10)
        
        # Continue button
        self.continue_button=QPushButton()
        self.continue_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.continue_button.setText("   Continue   ")
        self.continue_button.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.continue_button.adjustSize()
        self.continue_button.setStyleSheet(self.button_stylesheet_detector)
        self.continue_button.clicked.connect(self.on_continueButton_clicked)

        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        self.titlel_layout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.titlel_layout.addWidget(image, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titlel_layout.addWidget(self.more_description, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        widget_button_layout.addWidget(self.continue_button,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.setLayout(self.titlel_layout)

    def on_continueButton_clicked(self):
        main2=ChooseDevice()
        WIDGET.addWidget(main2) 
        WIDGET.setCurrentIndex(WIDGET.currentIndex()+1)

class ChooseDevice(QWidget):
    def __init__(self):
        super().__init__()
        self.foundInMedia=None
        self.outputBox=()
        self.captureDevices=[]

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if detect_theme_color(APP):
            self.button_stylesheet_detector=buttonStylesheetDark
            self.separator_stylesheet_detector=separetorLineDark
            self.availableDeviceButtonDetector=availableDeviceButtonStylesheetDark
        else:
            self.button_stylesheet_detector=buttonStylesheet
            self.separator_stylesheet_detector=separetorLine
            self.availableDeviceButtonDetector=availableDeviceButtonStylesheet

        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        self.vertical_layout=QVBoxLayout()
        self.vertical_layout.setSpacing(20)
        self.vertical_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        self.title=QLabel()
        self.title.setFont(QFont(MAIN_FONT,MIGRATION_ASSISTANT_TITLE))
        self.title.setText("Restore Information To This PC")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        # Description
        self.description=QLabel()
        self.description.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Select a {APP_NAME} " 
            "backup disk to retore it's information to this PC.")

        # More description
        self.more_description=QLabel()
        self.more_description.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.more_description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.more_description.setText(f"Make sure that your Backup external device " 
            f"with a {APP_NAME}'s backup is already connected to this PC.")

        ################################################################################
        # Devices Area
        ################################################################################
        self.devices_aread_widget=QWidget()
        self.devices_aread_widget.setFixedSize(700, 200)

        # Device layout
        self.devicesAreaLayout=QHBoxLayout(self.devices_aread_widget)
        
        ################################################################################
        # Buttons
        ################################################################################
        widget_button=QWidget(self)
        widget_button.setFixedSize(900,60)
        widget_button.move(0,600-widget_button.height())
        widget_button.setStyleSheet(self.separator_stylesheet_detector)

        widget_button_layout=QHBoxLayout(widget_button)
        widget_button_layout.setSpacing(10)
        
        # Back button
        self.back_button=QPushButton()
        self.back_button.setText("   Back   ")
        self.back_button.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.back_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.back_button.adjustSize()
        self.back_button.setStyleSheet(self.button_stylesheet_detector)
        self.back_button.clicked.connect(lambda *args: WIDGET.setCurrentIndex(WIDGET.currentIndex()-1))

        # Continue button
        self.continue_button=QPushButton()
        self.continue_button.setText("   Continue  ")
        self.continue_button.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.continue_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.continue_button.adjustSize()
        self.continue_button.setEnabled(False)
        self.continue_button.setStyleSheet(self.button_stylesheet_detector)
        self.continue_button.clicked.connect(self.on_continue_clicked)
        
        widget_button_layout.addStretch()
        widget_button_layout.addWidget(self.back_button,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        widget_button_layout.addWidget(self.continue_button,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.show_on_screen()

    def show_on_screen(self):
        print("Searching devices...")
  
        # Search external inside media
        if device_location():
            location=f"{MEDIA}"

        elif not device_location():
            location=f"{RUN}"
            
        else:
            location=None
        
        # Show available files
        try:
            for output in os.listdir(f"{location}/{USERNAME}/"):
                # Only show disk the have baseFolderName inside
                if BASE_FOLDER_NAME in os.listdir(f"{location}/{USERNAME}/{output}/"):
                    if output not in self.captureDevices:   
                        self.captureDevices.append(output)

                        self.available_devices=QPushButton(self.devices_aread_widget)
                        self.available_devices.setCheckable(True)
                        self.available_devices.setAutoExclusive(True)
                        self.available_devices.setFixedSize(140,140)
                        self.available_devices.setText(f"\n\n\n\n\n{output}")
                        self.available_devices.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
                        self.available_devices.adjustSize()
                        self.available_devices.clicked.connect(
                            lambda *args, output=output: self.on_device_clicked(output))
                        self.available_devices.setStyleSheet(self.availableDeviceButtonDetector)
           
                        # Image
                        image=QLabel(self.available_devices)
                        image.setFixedSize(96, 96)
                        image.move(42,30)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                                f"background-image: url({SRC_RESTORE_ICON});"
                                "background-repeat: no-repeat;"
                                "background-color: transparent;"
                                "border-radius:0px solid transparent;"
                            "}")

                        self.devicesAreaLayout.addWidget(self.available_devices)

        except Exception:
            pass

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.vertical_layout.addWidget(self.title)
        self.vertical_layout.addWidget(self.description)
        self.vertical_layout.addWidget(self.devices_aread_widget,0,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.vertical_layout.addWidget(self.refreshButton, 0,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.vertical_layout.addWidget(self.more_description,1,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.setLayout(self.vertical_layout)

    def on_device_clicked(self, output):
        if self.available_devices.isChecked():
            self.choose_device=output
            self.continue_button.setEnabled(True)

        else:
            self.continue_button.setEnabled(False)
            
    def on_continue_clicked(self):
        # Update INI file
        save_info(self.choose_device)

        main3=PreBackup()
        WIDGET.addWidget(main3) 
        WIDGET.setCurrentIndex(WIDGET.currentIndex()+1)

class PreBackup(QWidget):
    def __init__(self):
        super().__init__()
        self.has_itens_inside_to_continue_list=[]
        self.exclude_app_list=[]
        self.count_of_deb_list=[]
        self.count_of_rpm_list=[]

        self.already_showing_application_information=False
        self.already_showing_flatpak_information=False
        self.already_showing_flatpak_data_information=False
        self.already_showing_files_and_folders_information=False
        self.already_showing_system_settings_information=False
        
        # Delete .exclude-applications.txt first
        if os.path.exists(MAIN_INI_FILE.exclude_applications_location()):
            sub.run(f"rm -rf {MAIN_INI_FILE.exclude_applications_location()}",shell=True)

        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if detect_theme_color(APP):
            self.button_stylesheet_detector=buttonStylesheetDark
            self.separator_stylesheet_detector=separetorLineDark
            self.application_Background_Box_detector=leftBackgroundColorStylesheetDark
        else:
            self.button_stylesheet_detector=buttonStylesheet
            self.separator_stylesheet_detector=separetorLine
            self.application_Background_Box_detector=leftBackgroundColorStylesheet

        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        # Restore WIDGET
        self.options_widget=QWidget()

        self.scroll_options=QScrollArea(self)
        self.scroll_options.setFixedSize(420,260)
        self.scroll_options.setWidgetResizable(True)
        self.scroll_options.setWidget(self.options_widget)
        self.scroll_options.setStyleSheet(self.application_Background_Box_detector)

        # Vertical base layout
        self.vertical_layout=QVBoxLayout()
        self.vertical_layout.setSpacing(20)
        self.vertical_layout.setContentsMargins(20, 20, 20, 20)

        # Vertical options layout
        self.vertical_layout_for_options=QVBoxLayout(self.options_widget)
        self.vertical_layout_for_options.setSpacing(5)
        self.vertical_layout_for_options.setAlignment(QtCore.Qt.AlignTop)
        self.vertical_layout_for_options.setContentsMargins(10, 10, 10, 10)

        # Title
        self.title=QLabel()
        self.title.setFont(QFont(MAIN_FONT,MIGRATION_ASSISTANT_TITLE))
        self.title.setText("Select The Information To Restore")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
            font-weight: Bold;
            color:gray;
        """)

        # Description
        self.description=QLabel()
        self.description.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText("Choose which information you'd like to restore to this PC.")
        
        ################################################################################
        # Application checkbox (DATA)
        ################################################################################
        self.flatpak_data_Checkbox=QCheckBox()
        self.flatpak_data_Checkbox.setText(" Flatpak Data")
        self.flatpak_data_Checkbox.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.flatpak_data_Checkbox.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/application-vnd.flatpak.ref.svg"))
        self.flatpak_data_Checkbox.setIconSize(QtCore.QSize(32,32))
        self.flatpak_data_Checkbox.setEnabled(False)
        self.flatpak_data_Checkbox.clicked.connect(self.on_applications_data_clicked)
        
        ################################################################################
        # Buttons
        ################################################################################
        widget_button=QWidget(self)
        widget_button.setFixedSize(900,60)
        widget_button.move(0,self.height()+60)
        widget_button.setStyleSheet(self.separator_stylesheet_detector)

        self.widgetButtonLayout=QHBoxLayout(widget_button)
        self.widgetButtonLayout.setSpacing(10)
        
        # Back button
        self.back_button=QPushButton()
        self.back_button.setText("   Back   ")
        self.back_button.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.back_button.adjustSize()
        self.back_button.setStyleSheet(self.button_stylesheet_detector)
        self.back_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.back_button.clicked.connect(self.on_back_button_clicked)

        # Continue button
        self.continue_button=QPushButton()
        self.continue_button.setText("   Continue   ")
        self.continue_button.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.continue_button.adjustSize()
        self.continue_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.continue_button.setStyleSheet(self.button_stylesheet_detector)
        self.continue_button.clicked.connect(self.on_continue_button_clicked)
        
        # No item in the list
        if not self.has_itens_inside_to_continue_list:
            self.continue_button.setEnabled(False)
        
        self.applications_option()

    def applications_option(self):
        ################################################################################
        # Application checkbox
        ################################################################################
        self.application_packages_Checkbox=QCheckBox()
        self.application_packages_Checkbox.setText(f" Applications "
            "                              "
            f"                           {get_packages_size()}")
        self.application_packages_Checkbox.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.application_packages_Checkbox.adjustSize()
        self.application_packages_Checkbox.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/folder-templates.svg"))
        self.application_packages_Checkbox.setIconSize(QtCore.QSize(32,32))
        self.application_packages_Checkbox.setToolTip(
            "This will reinstall: \n"
            "* All backup's deb packages.")
        self.application_packages_Checkbox.clicked.connect(self.on_application_clicked)
        
        ################################################################################
        # More informations about
        ################################################################################
        base_widget_For_more_information=QWidget()

        self.show_more_application_information_widget=QScrollArea()
        self.show_more_application_information_widget.setFixedHeight(0)
        self.show_more_application_information_widget.setWidgetResizable(True)
        self.show_more_application_information_widget.setWidget(base_widget_For_more_information)

        self.show_more_application_information_layout=QVBoxLayout(base_widget_For_more_information)
        self.show_more_application_information_layout.setSpacing(5)

        ################################################################################
        if get_packages_size() != "None":
            # Application size information
            self.applicationSizeInformation=QLabel()
            self.applicationSizeInformation.setText(f"{get_packages_size()}")
            self.applicationSizeInformation.adjustSize()
            self.applicationSizeInformation.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
            self.applicationSizeInformation.setAlignment(QtCore.Qt.AlignRight)
    
        self.flatpak_names_option()

    def flatpak_names_option(self):
        try:
            ################################################################################
            # Flatpak checkbox (names)
            ################################################################################
            with open(MAIN_INI_FILE.flatpak_txt_location(), "r") as read_file:
                flatpaksToBeInstalled = len(read_file.readlines())

                self.flatpakCheckBox = QCheckBox()
                self.flatpakCheckBox.setText(f" Flatpak "
                    "                                  "
                    f"                               {flatpaksToBeInstalled} Apps")
                self.flatpakCheckBox.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
                self.flatpakCheckBox.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/application-vnd.flatpak.ref.svg"))
                self.flatpakCheckBox.setIconSize(QtCore.QSize(32,32))
                self.flatpakCheckBox.setToolTip("This will reinstall: \n"
                    "* All flatpak applications")
                self.flatpakCheckBox.clicked.connect(self.on_flatpak_clicked)

            ################################################################################
            # More informations about
            ################################################################################
            base_widget_For_more_information=QWidget()

            self.showMoreFlatpakInformationWidget=QScrollArea()
            self.showMoreFlatpakInformationWidget.setFixedHeight(0)
            self.showMoreFlatpakInformationWidget.setWidgetResizable(True)
            self.showMoreFlatpakInformationWidget.setWidget(base_widget_For_more_information)

            self.showMoreFlatpakInformationLayout=QVBoxLayout(base_widget_For_more_information)
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
            self.flatpakDataSize=os.popen(f"du -hs {MAIN_INI_FILE.ini_external_location()}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}")
            self.flatpakDataSize=self.flatpakDataSize.read().strip("\t").strip("\n").replace(f"{MAIN_INI_FILE.ini_external_location()}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}", "").replace("\t", "")
        
            # Application size information
            self.applicationSizeInformation=QLabel()
            self.applicationSizeInformation.setText(f"{self.flatpakDataSize}")
            self.applicationSizeInformation.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
            self.applicationSizeInformation.adjustSize()
            
            ################################################################################
            # More informations about
            ################################################################################
            base_widget_For_more_information=QWidget()

            self.showMoreFlatpakDataInformationWidget=QScrollArea()
            self.showMoreFlatpakDataInformationWidget.setFixedHeight(0)
            self.showMoreFlatpakDataInformationWidget.setWidgetResizable(True)
            self.showMoreFlatpakDataInformationWidget.setWidget(base_widget_For_more_information)

            self.showMoreFlatpakDataInformationLayout=QVBoxLayout(base_widget_For_more_information)
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
            self.SystemSettingsSizeInformation=QLabel()
            self.SystemSettingsSizeInformation.setText(f"{str(get_system_settings_size())}")
            self.SystemSettingsSizeInformation.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
            self.SystemSettingsSizeInformation.adjustSize()
        
            self.systemSettingsCheckBox=QCheckBox()
            self.systemSettingsCheckBox.setText(" System Settings"
                "                               "
                f"                       {self.SystemSettingsSizeInformation.text()}")
            self.systemSettingsCheckBox.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
            self.systemSettingsCheckBox.adjustSize()
            self.systemSettingsCheckBox.setToolTip("This will restore: \n"
                "* Wallpaper\n"
                "* Theme\n"
                "   -- Icon\n"
                "   -- Cursor")
            self.systemSettingsCheckBox.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/preferences-system.svg"))
            self.systemSettingsCheckBox.setIconSize(QtCore.QSize(34,34))
            self.systemSettingsCheckBox.clicked.connect(self.on_system_settings_clicked)
            
            ################################################################################
            # More informations about
            ################################################################################
            base_widget_For_more_information=QWidget()

            self.showMoreSystemSettingsInformationWidget=QScrollArea()
            self.showMoreSystemSettingsInformationWidget.setFixedHeight(0)
            self.showMoreSystemSettingsInformationWidget.setWidgetResizable(True)
            self.showMoreSystemSettingsInformationWidget.setWidget(base_widget_For_more_information)

            self.showMoreSystemSettingsInformationLayout=QVBoxLayout(base_widget_For_more_information)
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
            self.fileAndFoldersCheckBox=QCheckBox()
            if get_backup_folders_size_pretty() != None:
                self.fileAndFoldersCheckBox.setText(" Files and Folders"
                    "                               "
                    f"                      {get_backup_folders_size_pretty()}")
            else:
                self.fileAndFoldersCheckBox.setText(" Files and Folders ")
                
            self.fileAndFoldersCheckBox.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
            self.fileAndFoldersCheckBox.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/text-x-generic.svg"))
            self.fileAndFoldersCheckBox.setIconSize(QtCore.QSize(32,32))
            self.fileAndFoldersCheckBox.setToolTip("This will restore: \n"
                "* All recents back up files and folders")
            self.fileAndFoldersCheckBox.clicked.connect(self.on_files_and_folders_clicked)

            ################################################################################
            # More informations about
            ################################################################################
            base_widget_For_more_information=QWidget()

            self.showMoreFileAndFoldersInformationWidget=QScrollArea()
            self.showMoreFileAndFoldersInformationWidget.setFixedHeight(0)
            self.showMoreFileAndFoldersInformationWidget.setWidgetResizable(True)
            self.showMoreFileAndFoldersInformationWidget.setWidget(base_widget_For_more_information)

            self.showMoreFileAndFoldersInformationLayout=QVBoxLayout(base_widget_For_more_information)
            self.showMoreFileAndFoldersInformationLayout.setSpacing(5)

        except Exception as error:
            print("Files and Folders",error)
            pass
        
        ################################################################################
        self.vertical_layout.addWidget(self.title)
        self.vertical_layout.addWidget(self.description)
        self.vertical_layout.addStretch()
        self.vertical_layout.addWidget(self.scroll_options, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.vertical_layout_for_options.addWidget(self.application_packages_Checkbox)
        self.vertical_layout_for_options.addWidget(self.show_more_application_information_widget)

        self.vertical_layout_for_options.addWidget(self.flatpakCheckBox)
        self.vertical_layout_for_options.addWidget(self.show_more_application_information_widget)
        
        self.vertical_layout_for_options.addWidget(self.flatpak_data_Checkbox)
        # self.vertical_layout_for_options.addWidget(self.showMoreFlatpakDataInformationWidget)
        
        self.vertical_layout_for_options.addWidget(self.fileAndFoldersCheckBox)
        self.vertical_layout_for_options.addWidget(self.showMoreFileAndFoldersInformationWidget)
        
        self.vertical_layout_for_options.addWidget(self.systemSettingsCheckBox)
        self.vertical_layout_for_options.addWidget(self.showMoreSystemSettingsInformationWidget)
        self.vertical_layout.addStretch(5)
        
        self.widgetButtonLayout.addStretch()
        self.widgetButtonLayout.addWidget(self.back_button,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.widgetButtonLayout.addWidget(self.continue_button,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.setLayout(self.vertical_layout)

        self.has_flatpak_names_to_install()

    def has_flatpak_names_to_install(self):
        dummy=[]
        try:
            # Look for flatpakTxt inside external device
            with open(f"{MAIN_INI_FILE.flatpak_txt_location()}", 'r') as output:
                dummy.append(output.read().strip())

            if dummy:
                self.flatpakCheckBox.setEnabled(True)
            else:
                self.flatpakCheckBox.setEnabled(False)  

        except FileNotFoundError:
            pass

        self.has_applications_packages_to_install()

    def has_applications_packages_to_install(self):
        dummyList=[]

        try:
            if package_manager() == RPM_FOLDER_NAME:
                for outputRPM in os.listdir(f"{MAIN_INI_FILE.rpm_main_folder()}/"):
                    dummyList.append(outputRPM)

            elif package_manager() == DEB_FOLDER_NAME:
                for outputDeb in os.listdir(f"{MAIN_INI_FILE.deb_main_folder()}/"):
                    dummyList.append(outputDeb)
            
            if dummyList:
                self.application_packages_Checkbox.setEnabled(True)
            else:
                self.application_packages_Checkbox.setEnabled(False)  

            dummyList.clear()
            
        except:
            pass

        self.find_applications_data()

    def find_applications_data(self):
        dummy=[]

        try:
            for output in os.listdir(f"{MAIN_INI_FILE.flatpak_var_folder()}/"):
                dummy.append(output)

            if dummy:
                self.flatpak_data_Checkbox.setEnabled(True)
            else:
                self.flatpak_data_Checkbox.setEnabled(False)  
            
            dummy.clear()

        except:
            pass

        self.find_files_and_folders()

    def find_files_and_folders(self):
        ################################################################################
        try:
            dummyList=[]
            # Check inside backup folder 
            for output in os.listdir(f"{MAIN_INI_FILE.backup_folder_name()}/"):
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
        self.system_settings_list=[]

        try:
            for output in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
                self.system_settings_list.append(output)

            # If has something inside
            if self.system_settings_list:
                self.systemSettingsCheckBox.setEnabled(True)
            else:
                self.systemSettingsCheckBox.setEnabled(False)  

        except:
            pass
                
    def on_application_clicked(self):
        # Expand if clicked on it
        if not self.already_showing_application_information:
            self.show_more_application_information_widget.setFixedHeight(240)
            self.already_showing_application_information=True
        else:
            self.show_more_application_information_widget.setFixedHeight(0)
            self.already_showing_application_information=False
        
        if self.application_packages_Checkbox.isChecked():
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'True')

            self.application_packages_Checkbox.setChecked(True)
            self.continue_button.setEnabled(True)
            self.has_itens_inside_to_continue_list.append("packages")

            # DEP
            if package_manager() == DEB_FOLDER_NAME:
                for exclude in os.listdir(f"{MAIN_INI_FILE.deb_main_folder()}"):
                    # Exclude
                    # exclude=exclude.split("_")[0].split("-")[0]
                    # Checkbox
                    dummyCheckBox=QCheckBox()
                    dummyCheckBox.setText(exclude.capitalize())
                    dummyCheckBox.setChecked(True)
                    self.count_of_deb_list.append(exclude)
                    dummyCheckBox.clicked.connect(lambda *args, exclude=exclude: self.exclude_apps(exclude))

                    self.show_more_application_information_layout.addWidget(dummyCheckBox)
            
            # RPM
            elif package_manager() == RPM_FOLDER_NAME:
                for exclude in os.listdir(f"{MAIN_INI_FILE.rpm_main_folder()}"):
                    # Exclude
                    # exclude=exclude.split("_")[0].split("-")[0]
                    # Checkbox
                    dummyCheckBox=QCheckBox()
                    dummyCheckBox.setText(exclude.capitalize())
                    dummyCheckBox.setChecked(True)
                    self.count_of_deb_list.append(exclude)
                    dummyCheckBox.clicked.connect(lambda *args, exclude=exclude: self.exclude_apps(exclude))

                    self.show_more_application_information_layout.addWidget(dummyCheckBox)
        else:
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'False')

            self.has_itens_inside_to_continue_list.remove("packages")
            self.exclude_app_list.clear()

            # Remove applications checkboxes
            for i in range(self.show_more_application_information_layout.count()):
                item=self.show_more_application_information_layout.itemAt(i)
                WIDGET=item.widget()
                WIDGET.deleteLater()
                i -= 1

        self.allow_to_continue()

    # TODO
    def on_flatpak_clicked(self):
        # # Open flatpak checkboxes
        # if not self.alreadyShowingFlatpakInformation:
        #     self.showMoreFlatpakInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingFlatpakInformation=True
        # else:
        #     self.showMoreFlatpakInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingFlatpakInformation=False
                       

        if self.flatpakCheckBox.isChecked():
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'True')

            # Set flatpak checkbox to True
            self.flatpakCheckBox.setChecked(True)
            # Enable continue button
            self.continue_button.setEnabled(True)
            # Add "flatpak" from list
            self.has_itens_inside_to_continue_list.append("flatpak")
        else:
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')

            # Uncheck flatpak checkbox
            self.flatpakCheckBox.setChecked(False)
            # Remove "flatpak" from list
            self.has_itens_inside_to_continue_list.remove("flatpak")

        self.allow_to_continue()

    def on_applications_data_clicked(self):
        # # Open flatpak data checkboxes
        # if not self.alreadyShowingFlatpakDataInformation:
        #     self.showMoreFlatpakDataInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingFlatpakDataInformation=True
        # else:
        #     self.showMoreFlatpakDataInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingFlatpakDataInformation=False
                
        if self.flatpak_data_Checkbox.isChecked():
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_data', 'True')

            # Check flatpak data checkbox
            self.flatpak_data_Checkbox.setChecked(True)
            # Enable continue button
            self.continue_button.setEnabled(True)
            # Add "data" from list
            self.has_itens_inside_to_continue_list.append("data")
            # Add "flatpak" from list
            self.has_itens_inside_to_continue_list.append("flatpak")
        else:
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_data', 'False')

            # Uncheck flatpak data checkbox
            self.flatpak_data_Checkbox.setChecked(False)
            # Remove "data" from list
            self.has_itens_inside_to_continue_list.remove("data")
            
        self.allow_to_continue()

    def on_files_and_folders_clicked(self):
        # # Open files and folder checkboxes
        # if not self.alreadyShowingFilesAndSoldersInformation:
        #     self.showMoreFileAndFoldersInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingFilesAndSoldersInformation=True
        # else:
        #     self.showMoreFileAndFoldersInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingFilesAndSoldersInformation=False
        
        if self.fileAndFoldersCheckBox.isChecked():
            MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'True')

            # Enable continue button
            self.continue_button.setEnabled(True)
            # Add "files" to list
            self.has_itens_inside_to_continue_list.append("files")
        else:
            MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')

            # Disable continue button
            self.continue_button.setEnabled(False)
            # Remove "files" to list
            self.has_itens_inside_to_continue_list.remove("files")
        
        self.allow_to_continue()
  
    def on_system_settings_clicked(self):
        # # Open system settings checkboxe
        # if not self.alreadyShowingSystemSettingsInformation:
        #     self.showMoreSystemSettingsInformationWidget.setFixedHeight(240)
        #     self.alreadyShowingSystemSettingsInformation=True
        # else:
        #     self.showMoreSystemSettingsInformationWidget.setFixedHeight(0)
        #     self.alreadyShowingSystemSettingsInformation=False

        if self.systemSettingsCheckBox.isChecked():
            MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'True')

            # Enable continue button
            self.continue_button.setEnabled(True)
            # Add "system_settings" to list
            self.has_itens_inside_to_continue_list.append("system_settings")
        else:
            MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')

            # Disable continue button
            self.continue_button.setEnabled(False)
            
            if "system_settings" in self.has_itens_inside_to_continue_list:
                self.has_itens_inside_to_continue_list.remove("system_settings")
            
        self.allow_to_continue()

    def allow_to_continue(self):
        # If self.hasItensInsideToContinueList is not empty, allow it
        if len(self.has_itens_inside_to_continue_list) > 0:
            self.continue_button.setEnabled(True)
        else:
            self.continue_button.setEnabled(False)

    def on_back_button_clicked(self):
        WIDGET.setCurrentIndex(WIDGET.currentIndex()-1)

        self.already_showing_application_information=False
        self.already_showing_flatpak_information=False
        self.already_showing_flatpak_data_information=False
        self.already_showing_files_and_folders_information=False
        self.already_showing_system_settings_information=False
        
    def on_continue_button_clicked(self):
        if self.application_packages_Checkbox.isChecked() == True:
            # Write applications exclude list .exclude-application.txt
            # Create a .exclude-applications
            if not os.path.exists(MAIN_INI_FILE.exclude_applications_location()):
                sub.run(f"{CREATE_CMD_FILE} {MAIN_INI_FILE.exclude_applications_location()}", shell=True)

            else:
                # Delete before continue
                sub.run(f"rm -rf {MAIN_INI_FILE.exclude_applications_location()}", shell=True)
                # Create again
                sub.run(f"{CREATE_CMD_FILE} {MAIN_INI_FILE.exclude_applications_location()}", shell=True)

            if self.exclude_app_list:
                # Get user installed flatpaks
                with open(MAIN_INI_FILE.exclude_applications_location(), 'w') as configfile:
                    for apps in self.exclude_app_list:  
                        configfile.write(f"{apps}\n")
            
        main4 = BackupScreen()
        WIDGET.addWidget(main4)
        WIDGET.setCurrentIndex(WIDGET.currentIndex()+1)

    def exclude_apps(self, exclude):
        # Only add to exclude, if it not already there
        if exclude not in self.exclude_app_list:
            self.exclude_app_list.append(exclude)
        else:
            self.exclude_app_list.remove(exclude)
        
        # if user deselect all app, application check to False
        if len(self.exclude_app_list) == len(self.count_of_deb_list) or len(self.exclude_app_list) == len(self.count_of_rpm_list):
            self.application_packages_Checkbox.setChecked(False)
            # Clean hasItensInsideToContinueList
            self.has_itens_inside_to_continue_list.clear()
            # Disable continue button
            self.continue_button.setEnabled(False)
        else:
            self.application_packages_Checkbox.setChecked(True)
            # Enable continue button
            self.continue_button.setEnabled(True)

class BackupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if detect_theme_color(APP):
            self.button_stylesheet_detector=buttonStylesheetDark
            self.separator_stylesheet_detector=separetorLineDark
        else:
            self.button_stylesheet_detector=buttonStylesheet
            self.separator_stylesheet_detector=separetorLine

        self.widgets()

    def widgets(self):
        ################################################################################
        # Layouts
        ################################################################################
        self.vertical_layout=QVBoxLayout()
        self.vertical_layout.setSpacing(20)
        self.vertical_layout.setContentsMargins(20, 20, 20, 20)

        # Restore area WIDGET
        self.devicesAreadWidget=QWidget()
        self.devicesAreadWidget.setFixedSize(400, 200)

        # Horizontal layout
        self.imagesLayout=QHBoxLayout(self.devicesAreadWidget)
        self.imagesLayout.setSpacing(10)

        ################################################################################
        # Texts
        ################################################################################
        # Title
        self.title=QLabel()
        self.title.setFont(QFont(MAIN_FONT,MIGRATION_ASSISTANT_TITLE))
        self.title.setText("Begin Restoring")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        # Description
        self.description=QLabel()
        self.description.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description.setText(f"Backup from {APP_NAME} " 
            "will been transferred to this PC.")

        # More description
        self.moreDescription=QLabel()
        self.moreDescription.setFont(QFont(MAIN_FONT,6))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText('<h1>Click on "Restore" to begin.</h1>') 
        
        # Automatically reboot
        self.autoReboot=QCheckBox()
        self.autoReboot.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.autoReboot.setText('Automatically reboot after restoring is done. (Recommended)') 
        self.autoReboot.clicked.connect(self.auto_reboot_clicked)

        # Restoring description
        self.whileRestoringDescription=QLabel()
        self.whileRestoringDescription.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.whileRestoringDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        ################################################################################
        # Images
        ################################################################################
        # Image 1       
        image=QLabel()
        image.setFixedSize(68, 68)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/restore_64px.svg);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        # Image 2       
        image2=QLabel()
        image2.setFixedSize(96, 96)
        image2.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/arrow.png);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        # Image 3       
        image3=QLabel()
        image3.setFixedSize(96, 96)
        image3.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/applications-system.svg);"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")

        ################################################################################
        # External device name
        ################################################################################
        widgetDeviceName=QWidget(self)
        widgetDeviceName.setFixedSize(185, 40)
        widgetDeviceName.move(232, 265)

        # Widget device layout
        widgetDeviceLayout=QHBoxLayout(widgetDeviceName)

        # External device name
        self.externalDeviceName=QLabel()
        self.externalDeviceName.setFont(QFont(MAIN_FONT,14))
        try:
            # Add userName 
            self.externalDeviceName.setText(MAIN_INI_FILE.get_database_value('EXTERNAL', 'name'))
            self.externalDeviceName.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.externalDeviceName.adjustSize()
        
        except:
            pass

        ################################################################################
        # This pc label
        ################################################################################
        widgetThisPCName=QWidget(self)
        widgetThisPCName.setFixedSize(170, 40)
        widgetThisPCName.move(488, 265)

        # This pc name layout
        widgetLayout=QHBoxLayout(widgetThisPCName)
        self.thisPCName=QLabel()
        self.thisPCName.setFont(QFont(MAIN_FONT,14))
        self.thisPCName.setText(f"{USERNAME.capitalize()}")
        self.thisPCName.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.thisPCName.adjustSize()

        ################################################################################
        # Buttons
        ################################################################################
        widget_button=QWidget(self)
        widget_button.setFixedSize(900,60)
        widget_button.move(0,600-widget_button.height())
        widget_button.setStyleSheet(self.separator_stylesheet_detector)

        widgetButtonLayout=QHBoxLayout(widget_button)
        widgetButtonLayout.setSpacing(10)
        
        # Back button
        self.back_button=QPushButton()
        self.back_button.setText("   Back   ")
        self.back_button.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.back_button.adjustSize()
        self.back_button.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.back_button.setStyleSheet(self.button_stylesheet_detector)
        self.back_button.clicked.connect(lambda *args: WIDGET.setCurrentIndex(WIDGET.currentIndex()-1))

        # Continue button
        self.startRestoreButton=QPushButton()
        self.startRestoreButton.setText("   Restore   ")
        self.startRestoreButton.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.startRestoreButton.adjustSize()
        self.startRestoreButton.setFixedHeight(BUTTONHEIGHT_SIZE)
        self.startRestoreButton.setEnabled(True)
        self.startRestoreButton.setStyleSheet(useDiskButtonStylesheet)
        self.startRestoreButton.clicked.connect(self.change_screen)

        ################################################################################
        # Add layouts and widgets
        ################################################################################
        self.vertical_layout.addWidget(self.title)
        self.vertical_layout.addWidget(self.description)
        self.vertical_layout.addWidget(self.devicesAreadWidget, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.vertical_layout.addWidget(self.moreDescription, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.vertical_layout.addWidget(self.whileRestoringDescription, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.vertical_layout.addWidget(self.autoReboot, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        widgetButtonLayout.addWidget(self.back_button,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        widgetButtonLayout.addStretch()
        widgetButtonLayout.addWidget(self.back_button,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        widgetButtonLayout.addWidget(self.startRestoreButton,0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        # Widget device layouts
        self.imagesLayout.addWidget(image, 1, QtCore.Qt.AlignHCenter)
        self.imagesLayout.addWidget(image2, 0, QtCore.Qt.AlignHCenter)
        self.imagesLayout.addWidget(image3, 1, QtCore.Qt.AlignHCenter)

        widgetDeviceLayout.addWidget(self.externalDeviceName)
        widgetLayout.addWidget(self.thisPCName)

        # Add userName self.set
        self.setLayout(self.vertical_layout)

        self.read_ini_file()

    def read_ini_file(self):
        try:
            self.externalDeviceName.setText(MAIN_INI_FILE.get_database_value('EXTERNAL', 'name'))

            ################################################################################
            # Update widgets
            ################################################################################
            # if restoring is running
            if MAIN_INI_FILE.get_database_value('RESTORE', 'is_restoring_running'):
                # Show restoring description
                # TODO
                self.whileRestoringDescription.setText(f'Transferring '
                    f"{MAIN_INI_FILE.get_database_value('INFO', 'current_backing_up')} to the user {USERNAME}...") 
                # Hide more description
                self.moreDescription.hide()
                # Show restoring description
                self.whileRestoringDescription.show()

        except:
            pass

    def change_screen(self):
        MAIN_INI_FILE.set_database_value('RESTORE', 'is_restore_running', 'True')

        sub.Popen(f"python3 {src_restore_cmd_py}",shell=True)

        MAIN5 = StartRestoring()
        WIDGET.addWidget(MAIN5)
        WIDGET.showFullScreen()
        WIDGET.setCurrentIndex(WIDGET.currentIndex()+1)

    def auto_reboot_clicked(self):
        MAIN_INI_FILE.set_database_value('INFO', 'auto_reboot', 'True')

class StartRestoring(QWidget):
    def __init__(self):
        super().__init__()
        self.widgets()
            
    def widgets(self):
        # Title layout
        titlel_layout=QVBoxLayout()
        titlel_layout.setSpacing(20)
        titlel_layout.setContentsMargins(20, 20, 20, 20)
        
        setting_up = QLabel()
        setting_up.setFont(QFont(MAIN_FONT,MIGRATION_ASSISTANT_TITLE))
        setting_up.setText("Setting Up Your PC...")
        setting_up.setAlignment(QtCore.Qt.AlignHCenter)
        setting_up.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        self.current_status = QLabel()
        self.current_status.setFont(QFont(MAIN_FONT, 12))
        self.current_status.setAlignment(QtCore.Qt.AlignHCenter)
        self.current_status.setStyleSheet("""
        color:white;
        """)

        title=QLabel()
        title.setFont(QFont(MAIN_FONT,16))
        title.setText("This may take a few minutes...")
        title.setAlignment(QtCore.Qt.AlignHCenter)
        title.setStyleSheet("""
        font-weight: Bold;
        color:gray;
        """)

        # More description
        self.moreDescription=QLabel()
        self.moreDescription.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
        self.moreDescription.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.moreDescription.setText(
            "Don't turn off your PC.\n"
            "This window will automatically close after restoring is done.") 
        
        # Image       
        image=QLabel()
        image.setFixedSize(320,320)
        image.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({SRC_LAPTOP_ICON});"
            "background-repeat: no-repeat;"
            "background-color: transparent;"
            "background-position: center;"
            "}")
        
        ###########################################################################
        # Add layouts and widgets
        ################################################################################
        titlel_layout.addStretch()
        titlel_layout.addWidget(setting_up, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        titlel_layout.addWidget(image, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        titlel_layout.addWidget(self.current_status, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        titlel_layout.addWidget(title, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        titlel_layout.addWidget(self.moreDescription, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        titlel_layout.addStretch()
        self.setLayout(titlel_layout)

        # Update
        timer.timeout.connect(self.read_ini_file)
        timer.start(1000) # Update every x seconds
        self.read_ini_file()

    def read_ini_file(self):
        self.current_status.setText(MAIN_INI_FILE.get_database_value('INFO', 'current_backing_up'))

        if not MAIN_INI_FILE.get_database_value('RESTORE', 'is_restoring_running'):
            MAIN_INI_FILE.set_database_value('RESTORE', 'is_restoring_running', 'None')
            exit()


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WIDGET = QStackedWidget()

    MAIN_INI_FILE = UPDATEINIFILE()
    MAIN = BackupScreen()

    WIDGET.addWidget(MAIN)   
    WIDGET.setCurrentWidget(MAIN)   
    WIDGET.setWindowTitle("Migration Assistant")
    WIDGET.setWindowIcon(QIcon(SRC_MIGRATION_ASSISTANT_ICON_212PX)) 
    WIDGET.setFixedSize(900,600)
    WIDGET.show()

    APP.exit(APP.exec())