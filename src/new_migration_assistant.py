from ui.ui_form import Ui_WelcomeScreen
from setup import *
from device_location import device_location
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE
from PySide6.QtSvgWidgets import QSvgWidget
from restore_backup_wallpaper import restore_backup_wallpaper
from restore_backup_home import restore_backup_home
from restore_backup_flatpaks_applications import restore_backup_flatpaks_applications
from restore_backup_package_applications import restore_backup_package_applications
from restore_backup_flatpaks_data import restore_backup_flatpaks_data
# from restart_kde_session import restart_kde_session
from restore_kde_share_config import restore_kde_share_config
from restore_kde_config import restore_kde_config
from restore_kde_local_share import restore_kde_local_share
from get_users_de import get_user_de


class WelcomeScreen(QWidget):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        self.ui = Ui_WelcomeScreen()
        self.ui.setupUi(self)
        
        # Page 1
        self.ui.button_continue.clicked.connect(self.on_continue_button_clicked_page1)

        # Connections
        self.ui.button_continue.clicked.connect(self.on_continue_button_clicked_page1)
        self.ui.button_back_page3.clicked.connect(self.on_continue_button_clicked_page1)
        
        #######################################################################
        # Page 2
        #######################################################################
        self.selected_item_texts = []

        # Connections
        self.ui.button_back_page2.clicked.connect(self.on_back_button_page2_clicked)
        self.ui.button_continue_page2.clicked.connect(self.on_continue_button_clicked_page2)
        
        #######################################################################
        # Page 3
        #######################################################################
        self.item_to_restore = []
        self.applications_to_be_exclude = []
        self.flatpaks_to_be_exclude = []

        # Disable applications sub checkboxes
        self.ui.applications_sub_widget_page3.hide()
        # Disable applications sub checkboxes
        self.ui.flatpaks_sub_widget_page3.hide()
        # Disable continue button
        self.ui.button_continue_page3.setEnabled(False)

        # Number of sub checkboxes
        self.number_of_item_applications = 0
        self.number_of_item_flatpaks = 0

        # Connections
        self.ui.button_back_page3.clicked.connect(self.on_back_button_page3_clicked)
        self.ui.button_continue_page3.clicked.connect(self.on_continue_button_clicked_page3)
        
        # Application
        self.ui.checkbox_applications_page3.clicked.connect(
            self.on_applications_checkbox_clicked_page3)
        # Flapak
        self.ui.checkbox_flatpaks_page3.clicked.connect(
            self.on_flatpaks_checkbox_clicked_page3)
        # Files and Folders
        self.ui.checkbox_files_folders_page3.clicked.connect(
            self.on_files_and_folders_checkbox_clicked_page3)
        # System settings
        self.ui.checkbox_system_settings_page3.clicked.connect(
            self.on_system_settings_checkbox_clicked_page3)
        
        #######################################################################
        # Page 4
        #######################################################################
        # Disable applications sub checkboxes
        # self.ui.progress_bar_restoring.hide()
        # Disable restoring label
        # self.ui.label_restoring_status.hide()

        # Connection
        self.ui.button_restore_page4.clicked.connect(self.on_restore_button_clicked_page4)

        self.ui.checkbox_automatically_reboot_page4.clicked.connect(self.on_automatically_reboot_clicked)
       
        #######################################################################
        # Page 5
        #######################################################################
        self.ui.button_back_page4.clicked.connect(self.on_back_button_clicked_page4)

        self.widgets()

    def widgets(self):
        # Logo image       
        image = QLabel(self.ui.image)
        image.setFixedSize(212, 212)
        image.setStyleSheet(
            "QLabel"
            "{"
                f"background-image: url({SRC_MIGRATION_ASSISTANT_ICON_212PX});"
                "background-repeat: no-repeat;"
                "background-color: transparent;"
                "background-position: center;"
            "}")
        
        # Page 2
        # Disable continue button
        self.ui.button_continue_page2.setEnabled(False)

        self.show_availables_devices_page2()

    def on_continue_button_clicked_page1(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
    
    ########################################################
    # PAGE 2
    ########################################################
    def get_devices_location_page2(self):
        # Search external inside media
        if device_location():
            return MEDIA
        elif not device_location():
            return RUN
        else:
            return None

    def show_availables_devices_page2(self):
        added_devices = []
        
        self.model = QFileSystemModel()
        self.ui.devices_area_page2.setModel(self.model)

        # Show availables devices
        for device in os.listdir(f"{self.get_devices_location_page2()}/{USERNAME}/"):
            # Only show disk the have TMB inside
            if BASE_FOLDER_NAME in os.listdir(f"{self.get_devices_location_page2()}/{USERNAME}/{device}/"):
                # If not already added
                if device not in added_devices:   
                    added_devices.append(device)
                    
                    self.ui.devices_area_page2.setWordWrap(True)
                    self.ui.devices_area_page2.setIconSize(QSize(64, 64))
                    self.ui.devices_area_page2.setViewMode(QListView.IconMode)
                    self.ui.devices_area_page2.setResizeMode(QListView.Adjust)
                    self.ui.devices_area_page2.setSelectionMode(QListView.SingleSelection)
                    self.ui.devices_area_page2.setSpacing(10)
                    self.ui.devices_area_page2.setDragEnabled(False)
                    self.ui.devices_area_page2.selectionModel().selectionChanged.connect(self.on_device_selected_page2)
                    self.ui.devices_area_page2.viewport().installEventFilter(self)

        # Search inside MEDIA or RUN
        self.model.setRootPath(f"{self.get_devices_location_page2()}/{USERNAME}/")
        self.ui.devices_area_page2.setModel(self.model)
        self.ui.devices_area_page2.setRootIndex(self.model.index(f"{self.get_devices_location_page2()}/{USERNAME}/"))

    def on_device_selected_page2(self, selected, deselected):
        # This slot will be called when the selection changes
        selected_indexes = selected.indexes()

        for index in selected_indexes:
            item_text = self.model.data(index)
            self.selected_item_texts.append(str(f"{self.get_devices_location_page2()}/{USERNAME}/{item_text}"))

        # Enable continue button
        if selected.indexes():
            self.ui.button_continue_page2.setEnabled(True)

        elif deselected.indexes():
            self.ui.button_continue_page2.setEnabled(False)

    def on_back_button_page2_clicked(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)

    def on_continue_button_clicked_page2(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
        # Load application and sub checkboxes
        self.load_applications_sub_checkbox_page3()
        # Load flatpaks and sub checkboxes
        self.load_flatpaks_sub_checkbox_page3()
        # Load home
        self.load_files_and_folders_page3()
        # Load system settings
        self.load_system_settings_page3()

    ########################################################
    # PAGE 3
    ########################################################
    def load_applications_sub_checkbox_page3(self):
        # Get user package manager
        if package_manager() == DEB_FOLDER_NAME:  # .deb
            package_location = f"{MAIN_INI_FILE.deb_main_folder()}"
        elif package_manager() == RPM_FOLDER_NAME:  # .rpm
            package_location = f"{MAIN_INI_FILE.rpm_main_folder()}"

        for package in os.listdir(package_location):
            sub_applications_checkboxes = QCheckBox()
            sub_applications_checkboxes.setText(package.capitalize().split('_')[0])
            sub_applications_checkboxes.setChecked(True)
            sub_applications_checkboxes.clicked.connect(
                lambda *args, package=package: self.exclude_applications(package))
            self.ui.applications_sub_checkbox_layout_page3.addWidget(sub_applications_checkboxes)
            
            self.number_of_item_applications += 1

        # Expand it, 1 item = 20 height
        self.ui.applications_sub_widget_page3.setMinimumHeight(self.number_of_item_applications*20)

    def load_flatpaks_sub_checkbox_page3(self):
        # Read installed flatpaks names
        with open(f'{MAIN_INI_FILE.flatpak_txt_location()}', 'r') as flatpaks:
            flatpaks = flatpaks.read().split()

            for flatpak in flatpaks:
                sub_flatpaks_checkboxes = QCheckBox()
                sub_flatpaks_checkboxes.setText(flatpaks[self.number_of_item_flatpaks])
                sub_flatpaks_checkboxes.setChecked(True)
                sub_flatpaks_checkboxes.clicked.connect(
                    lambda *args, flatpak=flatpak: self.exclude_flatpaks(flatpak))
                self.ui.flatpaks_sub_checkbox_layout_page3.addWidget(sub_flatpaks_checkboxes)
                
                self.number_of_item_flatpaks += 1

        # Expand it, 1 item = 20 height
        self.ui.flatpaks_sub_widget_page3.setMinimumHeight(self.number_of_item_flatpaks*20)

    def load_files_and_folders_page3(self):
        home_to_restore = []
        # Check inside backup folder 
        for home in os.listdir(f"{MAIN_INI_FILE.backup_folder_name()}/"):
            home_to_restore.append(home)

        if home_to_restore:
            self.ui.checkbox_files_folders_page3.setEnabled(True)
        else:
            self.ui.checkbox_files_folders_page3.setEnabled(False)  

        # Clean list
        home_to_restore.clear()

    def load_system_settings_page3(self):
        system_settings_list = []

        for output in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
            system_settings_list.append(output)

        if system_settings_list:
            self.ui.checkbox_system_settings_page3.setEnabled(True)
        else:
            self.ui.checkbox_system_settings_page3.setEnabled(False)  

    def on_back_button_page3_clicked(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
    
    def on_continue_button_clicked_page3(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_4)

    def on_applications_checkbox_clicked_page3(self):
        # Expand it if selected
        if self.ui.checkbox_applications_page3.isChecked():
            # Add to list to restore
            self.item_to_restore.append('Applications')
            # Enable continue button
            self.ui.button_continue_page3.setEnabled(True)
            # Show applications sub checkboxes
            self.ui.applications_sub_widget_page3.show()
            # Update DB
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'True')
        else:
            # Remove to list to restore
            self.item_to_restore.remove('Applications')
            # Hide applications sub checkboxes
            self.ui.applications_sub_widget_page3.hide()
            # Clear applications exclude list
            self.applications_to_be_exclude.clear() 
            # Update DB
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'False')
            
    def on_flatpaks_checkbox_clicked_page3(self):
        # Expand it if selected
        if self.ui.checkbox_flatpaks_page3.isChecked():
            # Add to list to restore
            self.item_to_restore.append('Flatpaks')
            # Enable continue button
            self.ui.button_continue_page3.setEnabled(True)
            # Show applications sub checkboxes
            self.ui.flatpaks_sub_widget_page3.show()
            # Update DB
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'True')
        else:
            # Remove to list to restore
            self.item_to_restore.remove('Flatpaks')
            # Hide applications sub checkboxes
            self.ui.flatpaks_sub_widget_page3.hide()
            # Clear applications exclude list
            # self.applications_to_be_exclude.clear() 
            # Update DB
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')

    def on_files_and_folders_checkbox_clicked_page3(self):
        # Expand it if selected
        if self.ui.checkbox_files_folders_page3.isChecked():
            # Add to list to restore
            self.item_to_restore.append('Files/Folders')
            # Enable continue button
            self.ui.button_continue_page3.setEnabled(True)
            # Update DB
            MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'True')
        else:
            # Remove to list to restore
            self.item_to_restore.remove('Files/Folders')
            # Clear applications exclude list
            # self.applications_to_be_exclude.clear() 
            # Update DB
            MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')

    def on_system_settings_checkbox_clicked_page3(self):
        if self.ui.checkbox_system_settings_page3.isChecked():
            MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'True')

            # Enable continue button
            self.ui.button_continue_page3.setEnabled(True)
            # Add "system_settings" to list
            self.item_to_restore.append("System_Settings")
        else:
            MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')
            # Disable continue button
            self.ui.button_continue_page3.setEnabled(False)

            if "System_Settings" in self.item_to_restore:
                self.item_to_restore.remove("System_Settings")
            
    def exclude_applications(self, exclude):
        # Add to the exclude list
        if exclude not in self.applications_to_be_exclude:
            self.applications_to_be_exclude.append(exclude)
        else:
            self.applications_to_be_exclude.remove(exclude)
        
        # # if user deselect all app, application check to False
        # if len(self.applications_to_be_exclude) == len(self.count_of_deb_list) or len(self.applications_to_be_exclude) == len(self.count_of_rpm_list):
        #     self.ui.checkbox_applications_page3.setChecked(False)
        #     # Clean hasItensInsideToContinueList
        #     self.has_itens_inside_to_continue_list.clear()
        #     # Disable continue button
        #     self.continue_button.setEnabled(False)
        # else:
        #     self.ui.checkbox_applications_page3.setChecked(True)
        #     # Enable continue button
        #     self.continue_button.setEnabled(True)

        # If all sub checboxes was deselected
        if len(self.applications_to_be_exclude) == self.number_of_item_applications:
            # Uncheck applications checkbox
            self.ui.checkbox_applications_page3.setChecked(False)
        else:
            # Check applications checkbox
            self.ui.checkbox_applications_page3.setChecked(True)
    
    def exclude_flatpaks(self, exclude):
        # Add to the exclude list
        if exclude not in self.flatpaks_to_be_exclude:
            self.flatpaks_to_be_exclude.append(exclude)
        else:
            self.flatpaks_to_be_exclude.remove(exclude)
        
        # # if user deselect all app, application check to False
        # if len(self.flatpaks_to_be_exclude) == len(self.count_of_deb_list) or len(self.flatpaks_to_be_exclude) == len(self.count_of_rpm_list):
        #     self.ui.checkbox_flatpaks_page3.setChecked(False)
        #     self.has_itens_inside_to_continue_list.clear()
        #     self.ui.button_continue_page3.setEnabled(False)
        # else:
        #     self.ui.checkbox_flatpaks_page3.setChecked(True)
        #     # Enable continue button
        #     self.ui.button_continue_page3.setEnabled(True)

        # If all sub checboxes was deselected
        if len(self.flatpaks_to_be_exclude) == self.number_of_item_flatpaks:
            # Uncheck applications checkbox
            self.ui.checkbox_flatpaks_page3.setChecked(False)
        else:
            # Check applications checkbox
            self.ui.checkbox_flatpaks_page3.setChecked(True)

    ########################################################
    # PAGE 4
    ########################################################
    def load_restore_page4(self):
        # Get users backup wallpaper
        for wallpaper in os.listdir(f'{MAIN_INI_FILE.wallpaper_main_folder()}'):
            set_wallpaper = f'{MAIN_INI_FILE.wallpaper_main_folder()}/{wallpaper}' 
            
        # From image
        original_pixmap = QPixmap(SRC_RESTORE_ICON)  # Load the original image
        resized_pixmap = original_pixmap.scaledToWidth(52)
        from_svg = QLabel()
        from_svg.setPixmap(resized_pixmap) 


        original_pixmap = QPixmap(SRC_MONITOR_ICON)  # Load the original image
        resized_pixmap = original_pixmap.scaledToWidth(96)
        to_pc = QLabel()
        to_pc.setPixmap(resized_pixmap) 

        # To image
        # Wallpaper
        svg_widget = QSvgWidget()
        if set_wallpaper.split('.')[-1].endswith('svg'):
            svg_widget.load(set_wallpaper)
            svg_widget.setFixedSize(96, 96)
            svg_widget.move(5, 5)
        else:
            original_pixmap = QPixmap(set_wallpaper)  # Load the original image
            resized_pixmap = original_pixmap.scaled(96, 96)
            label1 = QLabel()
            label1.setPixmap(resized_pixmap) 
            label1.move(5, 5)

        # Arror image
        arrow_image = QLabel()
        arrow_image.setStyleSheet(
            "QLabel"
            "{"
                f"background-image: url({SRC_ARROW_ICON});"
                "background-repeat: no-repeat;"
                "background-color: transparent;"
                "background-position: center;"
            "}")
        
        # Current pcs name        
        self.ui.from_image_label.setText(f"{USERNAME.capitalize()}")
        self.ui.from_image_label.adjustSize()
        
        # Backup devices name
        self.ui.to_image_label.setText(MAIN_INI_FILE.get_database_value('EXTERNAL', 'name'))
        self.ui.to_image_label.adjustSize()

    def on_restore_button_clicked_page4(self):
        # Call restore class
        MAIN_RESTORE = RESTORE()
        asyncio.run(MAIN_RESTORE.start_restoring())

    def on_back_button_clicked_page4(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)

    def on_automatically_reboot_clicked(self):
        if self.ui.checkbox_automatically_reboot_page4.isChecked():
            print("Reboot True")
            return True
        else:
            print("Reboot False")
            return False

class RESTORE:
    def __init__(self):
        # Progressbar
        self.current_item_index = 0
        self.progress_increment = 100 / len(MAIN.item_to_restore)
        MAIN.ui.progress_bar_restoring.setValue(0)
        
        # Countdowm
        self.countdown = 10

        # Connections
        MAIN.ui.button_close_page5.clicked.connect(lambda: exit())
    
    async def start_restoring(self):
        # First change the wallpaper
        if MAIN_INI_FILE.get_database_value('RESTORE', 'system_settings'):
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring wallpaper...')

            self.update_progressbar()

            await restore_backup_wallpaper()
        
        # Restore home folder
        if MAIN_INI_FILE.get_database_value('RESTORE', 'files_and_folders'):
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring Home...')

            self.update_progressbar()

            await restore_backup_home()

        # Restore applications packages (.deb, .rpm etc.)
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_packages'):
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring Applications...')

            self.update_progressbar()

            await restore_backup_package_applications()
       
        # Restore flatpaks
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_names'):
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring Flatpaks Applications...')
            
            MAIN.ui.label_restoring_status.setText(MAIN_INI_FILE.get_database_value('INFO', 'saved_notification '))
            MAIN.ui.label_restoring_status.adjustSize()

            self.update_progressbar()

            await restore_backup_flatpaks_applications()
        
        # Restore flatpaks data
        if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_data'):
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring Flatpak Data...')
            
            MAIN.ui.label_restoring_status.setText(MAIN_INI_FILE.get_database_value('INFO', 'saved_notification '))
            MAIN.ui.label_restoring_status.adjustSize()

            self.update_progressbar()

            await restore_backup_flatpaks_data()
        
        # # Restore system settings
        if MAIN_INI_FILE.get_database_value('RESTORE', 'system_settings'):
            # Only for kde
            if get_user_de() == 'kde':
                MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring KDE local/share...')

                self.update_progressbar()

                # Restore kde local share
                await restore_kde_local_share()
                
                MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring KDE config...')

                self.update_progressbar()

                # Restore kde CONFIG
                await restore_kde_config()

                MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'Restoring KDE share/CONFIG....')

                
                self.update_progressbar()
                
                # Restore kde share CONFIG
                await restore_kde_share_config()
                
        # Restart KDE session
        # sub.Popen("kquitapp5 plasmashell; kstart5 plasmashell",shell=True)

        self.end_restoring()

    def end_restoring(self):
        # Set all to False
        MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')
        MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_data', 'False')
        MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', '')

        # After backup is done
        print("Restoring is done!")

        ########################################################
        # PAGE 5
        ########################################################
        # Add done image
        done_image = QLabel(MAIN.ui.image_page5)
        done_image.setFixedSize(64, 64)
        done_image.setStyleSheet(
            "QLabel"
            "{"
                f"background-image: url({SRC_DONE_ICON});"
                "background-repeat: no-repeat;"
                "background-color: transparent;"
            "}")
        
        # Change stackwidget
        MAIN.ui.stackedWidget.setCurrentWidget(MAIN.ui.page_5)
        
    #     # Automatically reboot
    #     if MAIN.on_automatically_reboot_clicked():
    #         print("REbooting now...")
    #         self.start_countdown()

    # def start_countdown(self):
    #     timer.timeout.connect(self.count_down_reboot)
    #     timer.start(2000)
    #     self.count_down_reboot()

    # def count_down_reboot(self):
    #     print(f"Rebooting in {self.countdown} seconds...")
    #     MAIN.ui.reboot_label.setText(f"Rebooting in {self.countdown} seconds...")
    #     MAIN.ui.reboot_label.adjustSize()

    #     self.countdown -= 1

    #     if self.countdown == 0:
    #         timer.stop()

    #         # Reboot system
    #         print("Rebooting...")
    #         MAIN.ui.reboot_label.setText(f"Rebooting...")
    #         MAIN.ui.reboot_label.adjustSize()
    #         sub.run("sudo reboot", shell=True)

    def update_progressbar(self):
        MAIN.ui.label_restoring_status.setText(MAIN_INI_FILE.get_database_value('INFO', 'saved_notification'))
        MAIN.ui.label_restoring_status.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        MAIN.ui.label_restoring_status.adjustSize()
        
        new_value = MAIN.ui.progress_bar_restoring.value() + self.progress_increment
        MAIN.ui.progress_bar_restoring.setValue(new_value)
        self.current_item_index += 1


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WIDGET = QStackedWidget()

    MAIN_INI_FILE = UPDATEINIFILE()
    MAIN = WelcomeScreen()

    WIDGET.setWindowTitle("Migration Assistant")   
    WIDGET.addWidget(MAIN)   
    WIDGET.setCurrentWidget(MAIN)   
    WIDGET.show()

    APP.exit(APP.exec())