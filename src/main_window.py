from setup import *
from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_dialog import Ui_Dialog
from ui.ui_options import Ui_Options

from stylesheet import *
from check_connection import is_connected
from device_location import device_location
from get_home_folders import get_home_folders
from handle_spaces import handle_spaces

from get_sizes import (
    get_external_device_max_size,
    get_all_max_backup_device_space,
    get_external_device_used_size,
    get_all_used_backup_device_space)

# from read_ini_file import UPDATEINIFILE
from get_oldest_backup_date import oldest_backup_date
from get_latest_backup_date import latest_backup_date_label
from calculate_time_left_to_backup import calculate_time_left_to_backup
from update import backup_db_file
from save_info import save_info
from next_backup_label import next_backup_label
from create_backup_checker_desktop import create_backup_checker_desktop
from notification_massage import notification_message


choose_device = []
capture_devices  = []


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        # Hide update button
        self.ui.update_available_button.hide()

        ######################################################################
        # Connection
        ######################################################################
        # Automatically backup checkbox
        self.ui.automatically_backup_checkbox.clicked.connect(
            self.on_automatically_checkbox_clicked)
        
        # Use select disk button
        self.ui.select_disk_button.clicked.connect(
            self.on_selected_disk_button_clicked)
        
        # System tray button
        self.ui.show_in_system_tray_checkbox.clicked.connect(
            self.on_system_tray_checkbox_clicked)
        
        # Options button
        self.ui.options_button.clicked.connect(self.on_options_button_clicked)

        # Help button
        self.ui.help_button.clicked.connect(
            lambda: sub.Popen(["xdg-open", GITHUB_HOME]))

        # Update button
        self.ui.update_available_button.clicked.connect(self.on_update_button_clicked)

        ######################################################################
        # Add images 
        ######################################################################
        # Logo image
        logo_image = QPixmap(SRC_BACKUP_ICON)
        self.ui.app_logo_image.setPixmap(logo_image)

        # Disk image
        disk_image = QPixmap(SRC_RESTORE_ICON)
        self.ui.app_disk_image.setPixmap(disk_image)
        
        ######################################################################
        # Hide or disable 
        ######################################################################
        # Hide process bar
        self.ui.backing_up_label.hide()

        self.center_main_window()

    def center_main_window(self):
        centerPoint = QtGui.QScreen.availableGeometry(
            QtWidgets.QApplication.primaryScreen()).center()
        
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        # Startup checking
        self.startup_read_db()

        # Check for update
        self.check_for_updates()

        timer.timeout.connect(self.running)
        timer.start(2000)
        self.running()

    def running(self):
        # Check if a backup device was registered
        if self.is_device_registered():
            # Device was registered
            self.registered_action_to_take()
            
            # Check connection to it
            if is_connected(MAIN_INI_FILE.hd_hd()):
                ################################################
                # Connection
                ################################################
                # Set external status label to Connected
                # self.external_status_label.setText("Status: Connected")
                # Set external status label to color Green
                # self.external_status_label.setStyleSheet('color: green')

                ################################################
                # Clean notification massage
                ################################################
                notification_message("")

                ################################################
                # Get backup devices size informations
                ################################################
                try:
                    self.ui.external_size_label.setText(
                        f"{get_external_device_used_size()} of "
                        f"{get_external_device_max_size()} available")

                except:
                    self.ui.external_size_label.setText("No information available")

                ################################################
                # Check if is current busy doing something
                ################################################
                # If is backing up right now
                if MAIN_INI_FILE.get_database_value('STATUS', 'backing_up_now'):
                    # Show backing up labe
                    self.ui.backing_up_label.show()
                    # Show current backing up
                    self.ui.backing_up_label.setText(
                        f"{MAIN_INI_FILE.get_database_value('INFO', 'current_backing_up')}")
                    
                    # Disable select disk
                    self.ui.select_disk_button.setEnabled(False)

                    # Disable automatically backup
                    self.ui.automatically_backup_checkbox.setEnabled(False)

                else:
                    # Hide backing up label
                    self.ui.backing_up_label.hide()

                    # Enable select disk
                    self.ui.select_disk_button.setEnabled(True)

                    # Enable automatically backup
                    self.ui.automatically_backup_checkbox.setEnabled(True)

                # Automatically backup
                if MAIN_INI_FILE.automatically_backup():
                    if (59 - MAIN_INI_FILE.current_minute()) <= TIME_LEFT_WINDOW:
                        self.ui.next_backup_label.setText(
                            f'Next Backup: {calculate_time_left_to_backup()}')
                    
                    else:
                        # Next backup label
                        self.ui.next_backup_label.setText('Next Backup: ' + next_backup_label())
                
                else:
                    self.ui.next_backup_label.setText(
                        'Next Backup: Automatic backups off')

            ################################################
            # Has no connection to it
            ################################################
            else:
                self.ui.external_size_label.setText("No information available")

        else:
            # No device was registered yet
            self.not_registered_action_to_take()
            
    def is_device_registered(self):
        # Check if a backup device was registered
        if MAIN_INI_FILE.hd_name() != "None":
            return True
    
    ################################################################################
    # STATIC
    ################################################################################
    def startup_read_db(self):
        if MAIN_INI_FILE.automatically_backup():
            self.ui.automatically_backup_checkbox.setChecked(True)
        
        else:
            self.ui.automatically_backup_checkbox.setChecked(False)

        if MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
            self.ui.show_in_system_tray_checkbox.setChecked(True)
        
        else:
            self.ui.show_in_system_tray_checkbox.setChecked(False)
    
    def check_for_updates(self):
        # Check for git updates
        git_update_command = os.popen(
            'git remote update && git status -uno').read()

        # Updates found
        if "Your branch is behind" in git_update_command:
            # Show update button
            self.ui.update_available_button.show()
        
        else:
            print("No new updates available...")
    
    def on_update_button_clicked(self):
        # Set system tray to False
        MAIN_INI_FILE.set_database_value(
            'SYSTEMTRAY', 'system_tray', 'False')

        # Set automatically backupt to False
        MAIN_INI_FILE.set_database_value(
            'STATUS', 'automatically_backup', 'False')

        # Uncheck system tray
        self.ui.show_in_system_tray_checkbox.setChecked(False)
        
        # Uncheck automatically backup
        self.ui.automatically_backup_checkbox.setChecked(False)

        # Update and make save the DB
        backup_db_file(True)

    def on_automatically_checkbox_clicked(self):
        if self.ui.automatically_backup_checkbox.isChecked():
            # Create backup checker .desktop and move it to the destination
            create_backup_checker_desktop()

            # Copy backup_check.desktop
            shutil.copy(DST_BACKUP_CHECK_DESKTOP, DST_AUTOSTART_LOCATION)

            MAIN_INI_FILE.set_database_value(
                'STATUS', 'automatically_backup', 'True')

            # call backup check
            sub.Popen(["python3", SRC_BACKUP_CHECKER_PY],
             stdout=sub.PIPE, 
             stderr=sub.PIPE)

            print("Auto backup was successfully activated!")

        else:
            # Remove autostart.desktop
            sub.run(f"rm -f {DST_AUTOSTART_LOCATION}",shell=True)

            MAIN_INI_FILE.set_database_value(
                'STATUS', 'automatically_backup', 'False')

            print("Auto backup was successfully deactivated!")
   
    def on_system_tray_checkbox_clicked(self):
        if self.ui.show_in_system_tray_checkbox.isChecked():
            MAIN_INI_FILE.set_database_value(
                'SYSTEMTRAY', 'system_tray', 'True')

            # Call system tray
            sub.Popen(["python3", SRC_SYSTEM_TRAY_PY])

            print("System tray was successfully enabled!")

        else:
            MAIN_INI_FILE.set_database_value(
                'SYSTEMTRAY', 'system_tray', 'False')

            print("System tray was successfully disabled!")
    
    def connected_action_to_take(self):
        self.ui.select_disk_button.setEnabled(True)
        # self.backup_now_button.setEnabled(True)
        self.ui.automatically_backup_checkbox.setEnabled(True)
        self.ui.show_in_system_tray_checkbox.setEnabled(True)

    # def not_connected_action_to_take(self):
    #     self.ui.select_disk_button.setEnabled(False)
    #     # self.backup_now_button.setEnabled(False)
    #     self.ui.automatically_backup_checkbox.setEnabled(False)
    #     self.ui.show_in_system_tray_checkbox.setEnabled(False)
    
    def registered_action_to_take(self):
        # Show devices name
        self.ui.external_name_label.setText(f"{MAIN_INI_FILE.hd_name()}")
        # Show oldest backup label
        self.ui.oldest_backup_label.setText(f"Oldest Backup: {oldest_backup_date()}")
        # Show latest backup label
        self.ui.latest_backup_label.setText(f"Latest Backup: {latest_backup_date_label()}")

    def not_registered_action_to_take(self):
            # Set external size label to No information
            self.ui.external_size_label.setText("No information available")

            # Set external name label to None
            self.ui.external_name_label.setText("None")

            # Disable automatically backup checkbox
            self.ui.automatically_backup_checkbox.setEnabled(False)

    def backup_now_clicked(self):
        sub.Popen(["python3", SRC_PREPARE_BACKUP_PY])

    def on_options_button_clicked(self):
        # options_window_class = OptionsWindow()

        # Show options window
        options_window_class.get_folders()

    def on_selected_disk_button_clicked(self):
        select_disk_class = SelectDisk()

        # Show dialog window
        select_disk_class.show_disk_dialog()
    

class SelectDisk(QDialog):
    def __init__(self, parent=True):
        super().__init__()
        self.dialog_ui = Ui_Dialog()
        self.dialog_ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

    def show_disk_dialog(self):
        ######################################################################
        # Connection
        ######################################################################
        # Cancel button dialog
        self.dialog_ui.cancel_button_dialog.clicked.connect(self.on_cancel_dialog_button_clicked)
        
        # Use disk button dialog
        self.dialog_ui.use_disk_button_dialog.clicked.connect(self.on_use_disk_dialog_button_clicked)
        
        ######################################################################
        # Hide or disable
        ######################################################################
        # Use disk button
        self.dialog_ui.use_disk_button_dialog.setEnabled(False)
        
        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside /Media
        ################################################################################
        if device_location():
            try:
                # Add buttons and images for each external
                for backup_device in os.listdir(f'{MEDIA}/{USERNAME}'):
                    # No spaces and special characters allowed
                    if backup_device not in capture_devices  and "'" not in backup_device and " " not in backup_device:
                        print("     Device:", backup_device)

                        # Add to capture list
                        capture_devices .append(backup_device)

                        # Avaliables external  devices
                        self.available_devices = QPushButton()
                        self.available_devices.setFont(
                            QFont(MAIN_FONT, FONT_SIZE_11PX))
                        self.available_devices.setText(backup_device)
                        self.available_devices.setFixedHeight(52)
                        self.available_devices.setCheckable(True)
                        self.available_devices.setAutoExclusive(True)

                        # if MAIN_INI_FILE.hd_name() != "None":
                        #     self.available_devices.setAutoExclusive(True)
       
                        # Image
                        icon = QLabel(self.available_devices)
                        image = QPixmap(f"{SRC_RESTORE_ICON}")
                        image = image.scaled(
                            36, 36, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation)
                        icon.move(7,7)
                        icon.setStyleSheet(transparentBackground)
                        icon.setPixmap(image)

                        # Free Space Label
                        free_space_label = QLabel(self.available_devices)
                        free_space_label.setText(
                            f'{get_all_used_backup_device_space(backup_device)} / {get_all_max_backup_device_space(backup_device)}')
                        free_space_label.setFont(QFont(MAIN_FONT, 8))
                        free_space_label.move(
                            (self.available_devices.width() - 354), 32)
                        
                        text = self.available_devices.text()
                        self.available_devices.toggled.connect(
                            lambda *args, text=text: self.on_device_clicked(text))

                        ################################################################################
                        # Add widgets and Layouts
                        ################################################################################
                        # Auto checked the choosed backup device
                        if text == MAIN_INI_FILE.hd_name():
                            self.available_devices.setChecked(True)

                            # Add the saved device to to this layput
                            self.dialog_ui.backup_disk_dialog_layout.addWidget(self.available_devices, Qt.AlignLeft | Qt.AlignTop)

                        else:
                            # Vertical layout
                            self.dialog_ui.available_disk_dialog_layout.addWidget(self.available_devices, Qt.AlignLeft | Qt.AlignTop)

            except FileNotFoundError:
                pass

        # If backup devices found inside /Run
        else:
            try:
                # If x device is removed or unmounted, remove from screen
                for backup_device in os.listdir(f'{RUN}/{USERNAME}'):
                    # No spaces and special characters allowed
                    if backup_device not in capture_devices  and "'" not in backup_device and " " not in backup_device:
                        print("     Devices:", backup_device)

                        capture_devices .append(backup_device)

                        # Avaliables external  devices
                        self.available_devices=QPushButton()
                        self.available_devices.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
                        self.available_devices.setText(backup_device)
                        self.available_devices.setCheckable(True)
                        self.available_devices.setAutoExclusive(True)
                        self.available_devices.setFixedHeight(52)
                        # self.available_devices.setStyleSheet(availableDeviceButtonStylesheet)
                        device = self.available_devices.text()

                        # Connect the device
                        self.available_devices.toggled.connect(lambda *args, device=device: self.on_device_clicked(device))

                        # Image
                        icon = QLabel(self.available_devices)
                        image = QPixmap(f"{SRC_RESTORE_ICON}")
                        image = image.scaled(46, 46, Qt.KeepAspectRatio)
                        icon.move(7, 7)
                        icon.setPixmap(image)

                        # Free Space Label
                        free_space_label = QLabel(self.available_devices)
                        free_space_label.setText(
                            f'{get_all_used_backup_device_space(backup_device)} / {get_all_max_backup_device_space(backup_device)}')
                        free_space_label.setFont(QFont(MAIN_FONT, 8))
                        free_space_label.setAlignment(Qt.AlignRight)
                        free_space_label.move((self.available_devices.width() - 354), 32)
                        
                        text = self.available_devices.text()
                        self.available_devices.toggled.connect(lambda *args, text=text: self.on_device_clicked(text))

                        ################################################################################
                        # Add widgets and Layouts
                        ################################################################################
                        # Auto checked the choosed backup device
                        if text == MAIN_INI_FILE.hd_name():
                            self.available_devices.setChecked(True)

                            # Add the saved device to to this layput
                            self.dialog_ui.backup_disk_dialog_layout.addWidget(self.available_devices, Qt.AlignLeft | Qt.AlignTop)

                        else:
                            # Vertical layout
                            self.dialog_ui.available_disk_dialog_layout.addWidget(self.available_devices, Qt.AlignLeft | Qt.AlignTop)

            except FileNotFoundError:
                pass

        
        # Add strech to layout
        self.dialog_ui.available_disk_dialog_layout.addStretch()

        # Show the dialog
        self.exec()

    def on_use_disk_dialog_button_clicked(self):
        # Update INI file
        save_info(choose_device[-1])

        # Close dialog window
        self.on_cancel_dialog_button_clicked()
    
    def on_device_clicked(self, device):
        # Enable use disk button
        self.dialog_ui.use_disk_button_dialog.setEnabled(True)
        self.dialog_ui.use_disk_button_dialog.setStyleSheet(
            """
                background-color: blue;
                color: white;
            """)
        
        # Add to the list
        if device not in choose_device:
            # Add to choosed device list
            choose_device.insert(0, device)

        # else:
        #     # Remove from the list
        #     choose_device.remove(device)

    def on_cancel_dialog_button_clicked(self):
        # Clean lists
        capture_devices.clear()
        
        # Close dialog window 
        self.close()


class OptionsWindow(QDialog):
    def __init__(self, parent=True):
        super().__init__()
        self.options_ui = Ui_Options()
        self.options_ui.setupUi(self)
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool)
                
        # Already added
        self.home_folder_added = False
        
        # Flatpak data
        if MAIN_INI_FILE.get_database_value('STATUS', 'allow_flatpak_data'):
            self.options_ui.allow_flatpak_data_checkBox.setChecked(True)

        # Version
        self.options_ui.version_label.setText(APP_VERSION)
        ######################################################################
        # Connection
        ######################################################################
        # Cancel options button dialog
        self.options_ui.cancel_button_options.clicked.connect(
            self.on_cancel_options_button_clicked)
        
        # Flatpaks
        self.options_ui.allow_flatpak_data_checkBox.clicked.connect(
            self.on_allow__flatpak_data_clicked)

        # Reset
        self.options_ui.reset_button.clicked.connect(
            self.on_button_fix_clicked)

    def get_folders(self):
        # start tab index from 0
        self.options_ui.tabWidget.setCurrentIndex(0)

        if not self.home_folder_added:
            home_folers_list = []

            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Query all keys from the specified table
            cursor.execute(f"SELECT key FROM FOLDER")
            keys = [row[0] for row in cursor.fetchall()]

            # Close the connection
            conn.close()

            for key in keys:
                home_folers_list.append(key)

            ################################################################################
            # Get Home Folders and Sort them alphabetically
            # Add On Screen
            ################################################################################
            horizontal = 0
            vertical = 0

            for folder in get_home_folders():
                # Hide hidden folder
                if not "." in folder:
                    # Checkboxes
                    self.home_folders_checkbox = QCheckBox()
                    self.home_folders_checkbox.setText(folder)
                    self.home_folders_checkbox.adjustSize()
                    # self.home_folders_checkbox.setIcon(
                    # QIcon(f"{homeUser}/.local/share/{APPNAMEClose}/src/icons/folder.png"))
                    self.home_folders_checkbox.setStyleSheet(
                        "QCheckBox"
                        "{"
                        "border-color: transparent;"
                        "}")
                    self.home_folders_checkbox.clicked.connect(
                        lambda *args, folder = folder: self.on_folder_clicked(
                            folder))

                    # Activate checkboxes in user.ini
                    if folder.lower() in home_folers_list:
                        self.home_folders_checkbox.setChecked(True)

                    # Add to layout self.leftLayout
                    self.options_ui.grid_folders_layout.addWidget(
                        self.home_folders_checkbox, horizontal, vertical)

                    horizontal += 1

                    # Number of checkbox per column
                    if horizontal == 14:
                        vertical = 1
                        horizontal = 0
            
            self.home_folder_added = True
        
        # App loop
        self.exec()

    def on_folder_clicked(self, folder):
        # Handle spaces 
        folder = handle_spaces(folder)
        
        if MAIN_INI_FILE.get_database_value('FOLDER', f'{folder.lower()}'):
            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Delete the key-value pair from the 'STATUS' table
            cursor.execute(f'DELETE FROM FOLDER WHERE key = ?', (f'{folder.lower()}',))
            conn.commit()
        else:
            MAIN_INI_FILE.set_database_value('FOLDER', f'{folder.lower()}', 'True')

    def on_allow__flatpak_data_clicked(self):
        if self.options_ui.allow_flatpak_data_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'True')
        else:
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'False')

    def on_button_fix_clicked(self):
        reset_confirmation = QMessageBox.question(
            self,
            'Reset',
            'Are you sure you want to reset settings?', QMessageBox.Yes | QMessageBox.No)

        if reset_confirmation == QMessageBox.Yes:
            # MAIN.latest_backup_label.setText("Latest Backup: None")
            # MAIN.oldest_backup_label.setText("Oldest Backup: None")
            
            # Reset settings
            # Backup section
            MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'No')
            MAIN_INI_FILE.set_database_value('STATUS', 'automatically_backup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'first_startup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_names', 'True')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')

            # INFO
            MAIN_INI_FILE.set_database_value('INFO', 'checked_backup_date', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'oldest_backup_to_main', 'None')

            # EXTERNAL  
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'hd', 'None')
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'name', 'None')
            
            # SYSTEMTRAY 
            MAIN_INI_FILE.set_database_value('SYSTEMTRAY', 'system_tray', 'False')
            
            MAIN_INI_FILE.set_database_value('INFO', 'language', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'os', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'packageManager', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'theme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'icon', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'cursor', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'colortheme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', 'None')
            
            # Remove all keys first
            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Execute the DELETE statement to remove all rows from a table
            table_name = 'FOLDER'
            cursor.execute(f"DELETE FROM {table_name}")

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            MAIN_INI_FILE.set_database_value('FOLDER', 'pictures', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'documents', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'music', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'videos', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'desktop', 'True')

            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_data', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')
            MAIN_INI_FILE.set_database_value('RESTORE', 'is_restore_running', 'False')

            print("All settings was reset!")

            # Re-open Main Windows
            sub.Popen(["python3", SRC_MAIN_WINDOW_PY])

            # Quit
            exit()

        else:
            QMessageBox.Close

    def on_cancel_options_button_clicked(self):
        # Close dialog window 
        self.close()

    # def on_save_options_button_clicked(self):
    #     # Close dialog window 
    #     self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Main window
    MAIN = MainWindow()

    # Window icon
    MAIN.setWindowIcon(QIcon(SRC_BACKUP_ICON))

    # Options window
    options_window_class = OptionsWindow()

    # Window size
    MAIN.setFixedSize(700, 450)
    
    MAIN.show()

    sys.exit(app.exec())
