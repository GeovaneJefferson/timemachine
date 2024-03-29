from ui.ui_migration import Ui_WelcomeScreen
from setup import *
from device_location import device_location
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE
from save_info import save_info
from create_directory import create_directory, create_file

from get_users_de import get_user_de
from restore_backup_flatpaks_data import restore_backup_flatpaks_data
# from restart_kde_session import restart_kde_session
from restore_kde_share_config import restore_kde_share_config
from restore_kde_config import restore_kde_config
from restore_kde_local_share import restore_kde_local_share
from handle_spaces import handle_spaces
from create_backup_checker_desktop import create_directory
from analyse import ANALYSES


# Define a function to convert the date string to a datetime object
def convert_to_datetime(date_str):
	return datetime.strptime(date_str, '%y-%m-%d')


class WelcomeScreen(QWidget):
	def __init__(self):
		super(WelcomeScreen, self).__init__()
		self.ui = Ui_WelcomeScreen()
		self.ui.setupUi(self)

		# Countdown
		# self.countdown = 10

		self.is_restore_done = False

		# Page 1
		self.ui.button_continue.clicked.connect(self.on_continue_button_clicked_page1)

		# Connections
		self.ui.button_continue.clicked.connect(self.on_continue_button_clicked_page1)
		self.ui.button_back_page3.clicked.connect(self.on_continue_button_clicked_page1)

		#######################################################################
		# Page 2
		#######################################################################
		# self.selected_item_texts = []

		# Connections
		self.ui.button_back_page2.clicked.connect(self.on_back_button_page2_clicked)
		self.ui.button_continue_page2.clicked.connect(self.on_continue_button_clicked_page2)

		#######################################################################
		# Page 3
		#######################################################################
		# All items
		self.item_to_restore = []
		
		# Item
		self.applications_to_be_restore = []
		self.flatpaks_to_restore = []
		self.pip_to_restore = []

		# Disable applications sub checkboxes
		self.ui.applications_sub_widget_page3.hide()
		# Disable applications sub checkboxes
		self.ui.flatpaks_sub_widget_page3.hide()
		# Disable pip sub checkboxes
		self.ui.pip_sub_widget_page3.hide()

		# Disable continue button
		self.ui.button_continue_page3.setEnabled(False)

		# Number of sub checkboxes
		self.number_of_item_applications = 0
		self.number_of_item_flatpaks = 0
		self.number_of_item_pip = 0

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
		# Pip
		self.ui.checkbox_pip_page3.clicked.connect(
			self.on_pip_checkbox_clicked_page3)
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

		#######################################################################
		# Page 5
		#######################################################################
		self.ui.button_back_page4.clicked.connect(self.on_back_button_clicked_page4)
		# Connections
		self.ui.button_close_page5.clicked.connect(lambda: sys.exit())

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
		# Animation
		self.stacked_widget_transition(self.ui.page_2, 'right')

	########################################################
	# PAGE 2
	########################################################
	def devices_from(self):
		# Search external inside media
		if device_location():
			return MEDIA
		elif not device_location():
			return RUN
		else:
			return None

	def show_availables_devices_page2(self):
		self.model = QFileSystemModel()
		self.ui.devices_area_page2.setModel(self.model)

		try:
			self.ui.devices_area_page2.setWordWrap(True)
			self.ui.devices_area_page2.setIconSize(QSize(64, 64))
			self.ui.devices_area_page2.setViewMode(QListView.IconMode)
			self.ui.devices_area_page2.setResizeMode(QListView.Adjust)
			self.ui.devices_area_page2.setSelectionMode(QListView.SingleSelection)
			self.ui.devices_area_page2.setSpacing(10)
			self.ui.devices_area_page2.setDragEnabled(False)
			self.ui.devices_area_page2.selectionModel().selectionChanged.connect(
				self.on_device_selected_page2)
			self.ui.devices_area_page2.viewport().installEventFilter(self)

			# Search inside MEDIA or RUN
			self.model.setRootPath(f'{self.devices_from()}/{USERNAME}/')
			self.ui.devices_area_page2.setModel(self.model)
			self.ui.devices_area_page2.setRootIndex(self.model.index(f'{self.devices_from()}/{USERNAME}/'))
		except FileNotFoundError:
			pass

	def on_device_selected_page2(self, selected, deselected):
		# This slot will be called when the selection changes
		selected_indexes = selected.indexes()

		for index in selected_indexes:
			self.selected_device = self.model.data(index)
			print(self.selected_device)

			folder_check = os.path.join(self.devices_from(), USERNAME)
			folder_check = os.path.join(folder_check, self.selected_device)
			folder_check = os.path.join(folder_check, BASE_FOLDER_NAME)

			# Allow only if the selected folder has TMB inside
			# Enable continue button
			if selected.indexes():
				# Check if is 'TMB' inside selected drive
				if os.path.exists(folder_check):
					print(f'{BASE_FOLDER_NAME} found in:', folder_check)
					self.ui.button_continue_page2.setEnabled(True)
				else:
					# Disable continue button
					self.ui.button_continue_page2.setEnabled(False)

			# Disable continue button
			elif deselected.indexes():
				self.ui.button_continue_page2.setEnabled(False)

	def on_back_button_page2_clicked(self):
		# Animation
		self.stacked_widget_transition(self.ui.page_1, 'left')

	def on_continue_button_clicked_page2(self):
		# Register backup device to DB
		save_info(self.selected_device)

		# Load application and sub checkboxes
		self.load_applications_sub_checkbox_page3()
		# Load flatpaks and sub checkboxes
		self.load_flatpaks_sub_checkbox_page3()
		# Load home
		self.load_files_and_folders_page3()
		# Load pip packages and sub checkboxes
		self.load_pip_packages_page3()
		# Load system settings
		self.load_system_settings_page3()

		# Animation
		self.stacked_widget_transition(self.ui.page_3, 'right')

	########################################################
	# PAGE 3
	########################################################
	def load_applications_sub_checkbox_page3(self):
		# Check packager manager compatibility
		if package_manager() == DEB_FOLDER_NAME:
			package_location = f"{MAIN_INI_FILE.deb_main_folder()}"
		elif package_manager() == RPM_FOLDER_NAME:
			package_location = f"{MAIN_INI_FILE.rpm_main_folder()}"
		else:
			package_location = None

		# Disable Application checkbox
		self.ui.checkbox_applications_page3.setEnabled(False)

		# Add all applications sub checkboxes
		if package_location is not None:
			# Has packages inside
			if any(os.scandir(package_location)):
				# Enable Application checkbox
				self.ui.checkbox_applications_page3.setEnabled(True)

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
			for flatpak in flatpaks.read().split():
				if flatpak not in self.flatpaks_to_restore:
					self.flatpaks_to_restore.append(flatpak)

		# Has flatpaks to restore
		if self.flatpaks_to_restore:
			for flatpak in self.flatpaks_to_restore:
				sub_flatpaks_checkboxes = QCheckBox()
				sub_flatpaks_checkboxes.setText(flatpak)
				sub_flatpaks_checkboxes.setChecked(True)
				sub_flatpaks_checkboxes.clicked.connect(
					lambda *args, flatpak=flatpak: self.exclude_flatpaks(flatpak))
				self.ui.flatpaks_sub_checkbox_layout_page3.addWidget(sub_flatpaks_checkboxes)

				# Add 1
				self.number_of_item_flatpaks += 1
		else:
			# Disable Application checkbox
			self.ui.checkbox_flatpaks_page3.setEnabled(False)

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

	def load_pip_packages_page3(self):
		# Read pip txt file
		with open(f'{MAIN_INI_FILE.pip_packages_txt_location()}', 'r') as flatpaks:
			for pip in flatpaks.read().split():
				if pip not in self.pip_to_restore:
					self.pip_to_restore.append(pip)

		# Has pip packages to restore
		if self.pip_to_restore:
			for pip in self.pip_to_restore:
				sub_pip_checkboxes = QCheckBox()
				sub_pip_checkboxes.setText(pip)
				sub_pip_checkboxes.setChecked(True)
				sub_pip_checkboxes.clicked.connect(
					lambda *args, pip=pip: self.exclude_pip(pip))
				self.ui.pip_sub_checkbox_layout_page3.addWidget(sub_pip_checkboxes)

				# Add 1
				self.number_of_item_pip += 1
		else:
			# Disable Application checkbox
			self.ui.checkbox_pip_page3.setEnabled(False)

		# Expand it, 1 item = 20 height
		self.ui.pip_sub_widget_page3.setMinimumHeight(self.number_of_item_pip*20)

	def load_system_settings_page3(self):
		wallpaper_folder = MAIN_INI_FILE.wallpaper_main_folder()

		# Get a list of files in the specified folder
		system_settings_list = os.listdir(wallpaper_folder)

		# Enable/disable the checkbox based on the presence of files
		self.ui.checkbox_system_settings_page3.setEnabled(bool(system_settings_list))

	def on_applications_checkbox_clicked_page3(self):
		# Expand it if selected
		if self.ui.checkbox_applications_page3.isChecked():
			reply = QMessageBox.question(
				self,
				'Root Privileges Required',
				'To install packages, your root password will be required. Continue?',
				QMessageBox.Yes | QMessageBox.No,
    			QMessageBox.No)
			
			if reply == QMessageBox.Yes:
				# Use pkexec for installing packages
				process = sub.run(
					['pkexec', 'true'],
					stdout=sub.PIPE,
					stderr=sub.PIPE,
					text=True)
						
				# User entered password
				if process.returncode == 0:
					print("Authentication successful.")
					
					# Add to list to restore
					self.item_to_restore.append('Applications')
				
					self.ui.checkbox_applications_page3.setChecked(True)

					# Show applications sub checkboxes
					self.ui.applications_sub_widget_page3.show()
				else:
					print("Authentication failed.")
					self.ui.checkbox_applications_page3.setChecked(False)
			else:
				self.ui.checkbox_applications_page3.setChecked(False)
		else:
			# Remove to list to restore
			self.item_to_restore.remove('Applications')
			# Hide applications sub checkboxes
			self.ui.applications_sub_widget_page3.hide()
			# Clear applications exclude list
			self.applications_to_be_restore.clear()

		self.check_checkboxes()

	def on_flatpaks_checkbox_clicked_page3(self):
		# Expand it if selected
		if self.ui.checkbox_flatpaks_page3.isChecked():
			# Add to list to restore
			self.item_to_restore.append('Flatpaks')
			# Show applications sub checkboxes
			self.ui.flatpaks_sub_widget_page3.show()
		else:
			# Remove to list to restore
			self.item_to_restore.remove('Flatpaks')
			# Hide applications sub checkboxes
			self.ui.flatpaks_sub_widget_page3.hide()

		self.check_checkboxes()

	def on_files_and_folders_checkbox_clicked_page3(self):
		# Expand it if selected
		if self.ui.checkbox_files_folders_page3.isChecked():
			# Add to list to restore
			self.item_to_restore.append('Files/Folders')
		else:
			# Remove to list to restore
			self.item_to_restore.remove('Files/Folders')

		self.check_checkboxes()

	def on_pip_checkbox_clicked_page3(self):
		if self.ui.checkbox_pip_page3.isChecked():
			# Add "system_settings" to list
			self.item_to_restore.append("Pip_Packages")
			# Show pip sub checkboxes
			self.ui.pip_sub_widget_page3.show()
		else:
			self.item_to_restore.remove("Pip_Packages")
			
			# Hide pip sub checkboxes
			# if "Pip_Packages" in self.item_to_restore:
			self.ui.pip_sub_widget_page3.hide()
			
		self.check_checkboxes()

	def on_system_settings_checkbox_clicked_page3(self):
		if self.ui.checkbox_system_settings_page3.isChecked():
			# Add "system_settings" to list
			self.item_to_restore.append("System_Settings")
		else:
			if "System_Settings" in self.item_to_restore:
				self.item_to_restore.remove("System_Settings")

		self.check_checkboxes()

	# EXCLUDE
	def exclude_applications(self, exclude):
		print("Exclude application:", exclude)

		# Add to the exclude list
		if exclude not in self.applications_to_be_restore:
			self.applications_to_be_restore.append(exclude)
		else:
			self.applications_to_be_restore.remove(exclude)

		# If all sub checboxes was deselected
		if len(self.applications_to_be_restore) == self.number_of_item_applications:
			# Uncheck applications checkbox
			self.ui.checkbox_applications_page3.setChecked(False)
		else:
			# Check applications checkbox
			self.ui.checkbox_applications_page3.setChecked(True)
	
	def exclude_pip(self, exclude):
		# Add to the exclude list
		if exclude not in self.pip_to_restore:
			print("Adding pip:", exclude)
			self.pip_to_restore.append(exclude)
		else:
			print("Removing pip:", exclude)
			self.pip_to_restore.remove(exclude)
			self.number_of_item_pip -= 1

		# If all sub checboxes was deselected
		if not self.pip_to_restore:
			# Uncheck pip checkbox
			self.ui.checkbox_pip_page3.setChecked(False)
		else:
			# Check pip checkbox
			self.ui.checkbox_pip_page3.setChecked(True)

	def exclude_flatpaks(self, exclude):
		# Add to the exclude list
		if exclude not in self.flatpaks_to_restore:
			print("Adding flatpak:", exclude)
			self.flatpaks_to_restore.append(exclude)
		else:
			print("Removing flatpak:", exclude)
			self.flatpaks_to_restore.remove(exclude)

		# If all sub checboxes was deselected
		if not self.flatpaks_to_restore:
			# Uncheck applications checkbox
			self.ui.checkbox_flatpaks_page3.setChecked(False)
		else:
			# Check applications checkbox
			self.ui.checkbox_flatpaks_page3.setChecked(True)

	def on_back_button_page3_clicked(self):
		#################################
		# APPLICATIONS
		#################################
		# Reset count of applications item
		self.number_of_item_applications = 0

		# Delete all added applications checkboxes
		for i in range(self.ui.applications_sub_checkbox_layout_page3.count()):
			item = self.ui.applications_sub_checkbox_layout_page3.itemAt(i)
			widget=item.widget()
			widget.deleteLater()
			i -= 1

		#################################
		# FLATPAK
		#################################
		# Reset count of flatpaks
		self.number_of_item_flatpaks = 0

		# Delete all added flatpaks checkboxes
		for i in range(self.ui.flatpaks_sub_checkbox_layout_page3.count()):
			item=self.ui.flatpaks_sub_checkbox_layout_page3.itemAt(i)
			widget=item.widget()
			widget.deleteLater()
			i -= 1

		# Animation
		self.stacked_widget_transition(self.ui.page_2, 'left')

	def on_continue_button_clicked_page3(self):	
		# Load page4
		self.load_restore_page4()

		# Animation
		self.stacked_widget_transition(self.ui.page_4, 'right')

	def check_checkboxes(self):
		# If restore list is empty
		if not self.item_to_restore:
			# Disable
			self.ui.button_continue_page3.setEnabled(False)
		else:
			# Enable
			self.ui.button_continue_page3.setEnabled(True)

	########################################################
	# PAGE 4
	########################################################
	def load_restore_page4(self):
		print(self.item_to_restore)

		# Hide progressbar
		self.ui.progress_bar_restoring.hide()

		# Get users backup wallpaper
		# for wallpaper in os.listdir(f'{MAIN_INI_FILE.wallpaper_main_folder()}'):
		# 	set_wallpaper = f'{MAIN_INI_FILE.wallpaper_main_folder()}/{wallpaper}'

		# # Load the system icon 'drive-removable-media'
		# audio_headset_icon = QIcon.fromTheme('drive-removable-media')

		# # Convert the QIcon to a QPixmap
		# audio_headset_pixmap = audio_headset_icon.pixmap(64, 64)  # Adjust the size as needed

		# from_image = QLabel(self.ui.from_image_widget)
		# from_image.setPixmap(audio_headset_pixmap)
		# from_image.setScaledContents(True)
		# from_image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		# from_image.move(10, 10)

		# # To image
		# # Wallpaper
		# # svg_widget = QSvgWidget()
		# # if set_wallpaper.split('.')[-1].endswith('svg'):
		# #     svg_widget.load(set_wallpaper)
		# #     svg_widget.setFixedSize(80, 80)
		# #     svg_widget.setContentsMargins(0, 0, 0, 0)
		# #     svg_widget.setAspectRatioMode(Qt.IgnoreAspectRatio)

		# #     # svg_widget.move(5, 5)
		# # else:
		# #     to_image = QLabel(self.ui.to_image_widget)
		# #     to_image.setPixmap(QPixmap(set_wallpaper))
		# #     to_image.setScaledContents(True)
		# #     to_image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

		# # Load the system icon 'drive-removable-media'
		# audio_headset_icon = QIcon.fromTheme('computer')

		# # Convert the QIcon to a QPixmap
		# audio_headset_pixmap = audio_headset_icon.pixmap(64, 64)  # Adjust the size as needed

		# from_image = QLabel(self.ui.to_image_widget)
		# from_image.setPixmap(audio_headset_pixmap)
		# from_image.setScaledContents(True)
		# from_image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		# from_image.move(10, 10)

		# Current pcs name
		self.ui.from_image_label.setText(MAIN_INI_FILE.hd_name())
		self.ui.from_image_label.adjustSize()

		# Backup devices name
		self.ui.to_image_label.setText(USERNAME.capitalize())
		self.ui.to_image_label.adjustSize()

	def stacked_widget_transition(self, page, direction):
		width = self.ui.stackedWidget.width()

		if direction == 'right':
			page.setGeometry(
				QRect(width, 0, width, self.ui.stackedWidget.height()))
		else:
			page.setGeometry(
				QRect(-width, 0, -width, self.ui.stackedWidget.height()))

		animation = QPropertyAnimation(page, b'geometry', page)
		animation.setDuration(500)
		animation.setEasingCurve(QEasingCurve.OutCubic)
		animation.setStartValue(page.geometry())
		animation.setEndValue(QRect(0, 0, width, self.ui.stackedWidget.height()))
		animation.start()

		self.ui.stackedWidget.setCurrentWidget(page)

	def on_back_button_clicked_page4(self):
		# Animation
		self.stacked_widget_transition(self.ui.page_3, 'left')

	def on_restore_button_clicked_page4(self):
		# Disable restore, back button and automatically checkbox
		self.ui.button_restore_page4.setVisible(False)
		self.ui.button_back_page4.setVisible(False)
		self.ui.checkbox_automatically_reboot_page4.setEnabled(False)

		# Add done image
		done_image = QLabel(self.ui.image_page5)
		done_image.setFixedSize(64, 64)
		done_image.setStyleSheet(
			"QLabel"
			"{"
				f"background-image: url({SRC_DONE_ICON});"
				"background-repeat: no-repeat;"
				"background-color: transparent;"
			"}")

		# Update DB
		# MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'True')

		#self.update_pb()
		# Show progressbar
		self.ui.progress_bar_restoring.show()

		# Call restore class asynchronously
		RESTORE_PROCESS = RESTORE()
		# RESTORE_PROCESS.start_restoring()

		try:
			thread2 = threading.Thread(target=RESTORE_PROCESS.start_restoring)
			thread2.start()
		except Exception as e:
			print(e)
			exit()
		#asyncio.run(RESTORE_PROCESS.start_restoring())

	def update_status_feedback(self):
		if self.is_restore_done:
			try:
				timer.stop()
			except:
				pass
		self.ui.label_restoring_status.adjustSize()
		self.ui.label_restoring_status.setAlignment(
			Qt.AlignHCenter | Qt.AlignVCenter)

	########################################################
	# PAGE 5
	########################################################
	def update_pb(self):
		# Start QTimer to read notification
		timer.timeout.connect(self.update_status_feedback)
		timer.start(1000)


class RESTORE:
	def __init__(self):
		# Length of item to restore
		self.item_to_restore = 0
		analyses = ANALYSES()
		
		# Create QProcess instance
		self.process = QProcess()
		self.process.readyReadStandardOutput.connect(self.write_output)
		self.process.readyReadStandardError.connect(self.write_output)
		self.process.finished.connect(self.write_finished)

		# Hide
		MAIN.ui.qprocess_text_edit.hide()

		#  Get length of the restore list
		if MAIN.ui.checkbox_applications_page3.isChecked():
			# Number of flatpaks items
			applicationsCount = int(MAIN.number_of_item_applications - len(MAIN.applications_to_be_restore))
			self.item_to_restore += applicationsCount

		if MAIN.ui.checkbox_flatpaks_page3.isChecked():
			# Number of flatpaks items
			flatpaksCount = int(len(MAIN.flatpaks_to_restore))
			self.item_to_restore += flatpaksCount

		# if MAIN.ui.checkbox_flatpaks_page3.isChecked():
		# 	self.item_to_restore += 1

		# Files and Folders
		if MAIN.ui.checkbox_files_folders_page3.isChecked():
			homeCount = int(len(analyses.get_source_dir()))
			self.item_to_restore += homeCount

		# Pip
		if MAIN.ui.checkbox_pip_page3.isChecked():
			pip_count = int(MAIN.number_of_item_pip - len(MAIN.pip_to_restore))
			if pip_count == 0:
				pip_count = len(MAIN.pip_to_restore)		
			self.item_to_restore += pip_count

		# System Settings
		if MAIN.ui.checkbox_system_settings_page3.isChecked():
			self.item_to_restore += 1

		# Only one item inside restore list
		if self.item_to_restore == 1:
			# Show 99%
			self.progress_increment = round(99 / self.item_to_restore)
		else:
			self.progress_increment = round(100 / self.item_to_restore)
    
	def write_output(self):
		# Read and display standard output and error
		output = self.process.readAllStandardOutput().data().decode()
		MAIN.ui.qprocess_text_edit.append(output)

		error = self.process.readAllStandardError().data().decode()
		if error:
			MAIN.ui.qprocess_text_edit.append("Error: " + error)

	def write_finished(self):
		# Display a message when the process finishes
		MAIN.ui.qprocess_text_edit.append("Process finished.")

	def update_progressbar_db(self):
		try:
			pb_value = round(self.progress_increment / (self.item_to_restore) * 100)
			# Fix at 100%
			if pb_value == 100:
				pb_value = 99
			MAIN.ui.progress_bar_restoring.setValue(pb_value)
		except ZeroDivisionError:
			pass

	#async def start_restoring(self):
	def start_restoring(self):
		# Restore user's wallpaper
		if MAIN.ui.checkbox_system_settings_page3.isChecked():
			print('Restoring wallpaper...')
			self.restore_backup_wallpaper()

		# Restore home folder
		if MAIN.ui.checkbox_files_folders_page3.isChecked():
			# self.update_progressbar_db()
			print('Restoring HOME...')
			self.restore_backup_home()
			# Restore updates file to HOME
			self.restore_backup_home_updates()

		# Restore applications packages
		if MAIN.ui.checkbox_applications_page3.isChecked():
			print('Restoring Applications Packages...')
			self.restore_backup_package_applications()

		# Restore flatpaks
		if MAIN.ui.checkbox_flatpaks_page3.isChecked():
			print('Restoring Flatpak Applications...')
			self.restore_backup_flatpaks_applications()
		
		# Restore pip
		if MAIN.ui.checkbox_pip_page3.isChecked():
			print('Restoring Pip Packages...')
			self.restore_backup_pip_packages()

		# # Restore flatpaks data
		# if MAIN_INI_FILE.get_database_value('RESTORE', 'applications_flatpak_data'):
		# 	# self.update_progressbar_db()
		# 	print('Restoring Flatpak Data...')
		# 	restore_backup_flatpaks_data()

		# # Restore system settings
		if MAIN.ui.checkbox_system_settings_page3.isChecked():
			# Only for kde
			if get_user_de() == 'kde':
				# self.update_progressbar_db()
				print('Restoring KDE .local/share...')
				restore_kde_local_share()

				# self.update_progressbar_db()
				print('Restoring KDE .config...')
				restore_kde_config()

				# self.update_progressbar_db()
				print('Restoring KDE .share/config...')
				restore_kde_share_config()

				# # Restart KDE session
				# sub.run(
				#     ['kquitapp5', 'plasmashell'],
				#     stdout=sub.PIPE,
				#     stderr=sub.PIPE)

				# sub.run(
				#     ['kstart5', 'plasmashell'],
				#     stdout=sub.PIPE,
				#     stderr=sub.PIPE)

		self.end_restoring()


	#----------RESTORE TOPICS----------#
	## Home
	def restore_backup_home(self):
		location = MAIN_INI_FILE.main_backup_folder()

		for folder in os.listdir(location):
			# EXclude hidden files/folder
			if not folder.startswith('.'):
				folder = handle_spaces(folder)

				# If folder folder do not exist, create it
				if not os.path.exists(f"{HOME_USER}/{folder}"):
					dst = os.path.join(HOME_USER, folder)
					# Create directory if necessary
					create_directory(dst)

				# Source from main backup folder
				src = os.path.join(location, folder) + '/'
				dst = os.path.join(HOME_USER, folder) + '/'

				# Show current installing flatpak to the user
				MAIN.ui.label_restoring_status.setText(f'Copying: {dst}...')
				MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)

				# Copy everything from src to dst folder
				for i in os.listdir(src):
					x = src + i

					print('Restoring Home Folder:', x)

					# Create if necessary
					if not os.path.exists(dst):
						os.makedirs(dst)

					# Copy files
					if os.path.isdir(x):
						try:
							shutil.copytree(x, dst)
						except FileExistsError:
							pass
					else:
						shutil.copy2(x, dst)

					# Substract 1
					self.item_to_restore -= 1
					self.update_progressbar_db()

	## Home Updates
	def restore_backup_home_updates(self):
		date_list = []
		added_list = []
		dst_loc = MAIN_INI_FILE.backup_dates_location()

		# Add all dates to the list
		for date in os.listdir(dst_loc):
			# Exclude hidden files/folders
			if not date.startswith('.'):
				date_list.append(date)

		# Sort the dates in descending order using the converted datetime objects
		sorted_date = sorted(date_list,
					key=convert_to_datetime,
					reverse=True)

		# Loop through each date folder
		for i in range(len(sorted_date)):
			# Get date path
			date_path = f'{dst_loc}/{sorted_date[i]}'

			# Get latest file update and add to the 'Added list'
			for root, _, files in os.walk(date_path):
				if files:
					for i in range(len(files)):
						if files[i] not in added_list:
							destination_location = root.replace(date_path, '')
							destination_location =  os.path.join(
									HOME_USER, '/'.join(
									destination_location.split(
									'/')[2:]))

							source = os.path.join(root, files[i])
							# print('Restoring:', files[i])
							# print('Source:', source)
							# print('Destination:', os.path.join(destination_location, files[i]))

							# Restore lastest file update
							#print(f'Restoring {source} to: {destination_location}')

							# Create if necessary
							if not os.path.exists(destination_location):
								os.makedirs(destination_location)

							# Copy files
							if os.path.isdir(source):
								try:
									shutil.copytree(source, destination_location)
								except FileExistsError:
									pass
							else:
								shutil.copy2(source, destination_location)

							# Add to 'Added list'
							added_list.append(files[i])

	## Application packages
	def restore_backup_package_applications(self):
		print("Installing applications packages...")

		try:
			if package_manager() == DEB_FOLDER_NAME:
				# Restore DEBS
				################################################################################
				for package in os.listdir(MAIN_INI_FILE.deb_main_folder()):
					# Install only if package if not in the exclude app list
					if package not in MAIN.applications_to_be_restore:
						# Install it
						command = os.path.join(MAIN_INI_FILE.deb_main_folder(), package)

						print(f"Installing package: {command}")

						# Show current installing to the user
						MAIN.ui.label_restoring_status.setText(f'Installing package: {command}...')
						MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)
						
						# Run the installation command with yes to automatically press Enter
						process = sub.run(
							['dpkg', '-i', command],
								stdout=sub.PIPE,
								stderr=sub.PIPE,
								text=True)
						
						# Clear output text
						# MAIN.ui.qprocess_text_edit.clear()

						# # Define the command to fix broken packages using apt
						# dpkg_command = ['dpkg', '-i']

						# # Set program and arguments for QProcess to execute dpkg
						# self.process.setProgram("dpkg")
						# self.process.setArguments(dpkg_command)

						# # Start the dpkg process
						# self.process.start()
						# self.process.waitForFinished()

						# Check the output and error if needed
						if process.returncode == 0:
							print(f"Package {package} installed successfully.")
							# Handle success
						else:
							print(f"Error installing package {package}: {process.stderr}")
							# Handle error

				# Fix packages installation using pkexec
				sub.run(
					['apt', '--fix-broken', 'install'],
					stdout=sub.PIPE,
					stderr=sub.PIPE,
					text=True)
				
				# Substract 1
				self.item_to_restore -= 1
				self.update_progressbar_db()

			elif package_manager() == RPM_FOLDER_NAME:
				################################################################################
				# Restore RPMS
				################################################################################
				for package in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
					print(f"Installing {MAIN_INI_FILE.rpm_main_folder()}/{package}")

					# Install only if package if not in the exclude app list
					if package not in MAIN.applications_to_be_restore:
						# Install it
						command = os.path.join(MAIN_INI_FILE.rpm_main_folder(), package)

						print(f"Installing package: {command}")

						# Show current installing to the user
						MAIN.ui.label_restoring_status.setText(f'Installing package: {command}...')
						MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)

						# Run the installation command with yes to automatically press Enter
						process = sub.run(
							['yes', '|', 'rpm', '-ivh', '--replacepkgs', command],
								stdout=sub.PIPE,
								stderr=sub.PIPE,
								text=True)

						# Check the output and error if needed
						if process.returncode == 0:
							print(f"Package {package} installed successfully.")
							# Handle success
						else:
							print(f"Error installing package {package}: {process.stderr}")
							# Handle error
						
						# Substract 1
						self.item_to_restore -= 1
						self.update_progressbar_db()
		except Exception as e:
			print(e)
			pass
	
	## Flatpaks
	def restore_backup_flatpaks_applications(self):
		for cnt in range(len(MAIN.flatpaks_to_restore)):
			flatpak = str(MAIN.flatpaks_to_restore[cnt]).strip()

			# Install only if flatpak if not in the exclude app list
			try:
				print(f'Installing flatpak: {flatpak}...')

				# Show current installing flatpak to the user
				MAIN.ui.label_restoring_status.setText(f'Installing flatpak: {flatpak}...')
				MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)

				# Install them
				sub.run(
					["flatpak", "install", "--system",
					"--noninteractive", "--assumeyes", "--or-update",
					flatpak],
					stdout=sub.PIPE,
					stderr=sub.PIPE)

				# Substract 1
				self.item_to_restore -= 1
				self.update_progressbar_db()
			except Exception as e:
				print(e)
				pass

	## Pip
	def restore_backup_pip_packages(self):
		# Iterate over the list and install each package
		for cnt in range(len(MAIN.pip_to_restore)):
			pip = str(MAIN.pip_to_restore[cnt]).strip()

			# Install only if pip if not in the exclude app list
			try:
				print(f'Installing pip: {pip}...')

				# Show current installing pip to the user
				MAIN.ui.label_restoring_status.setText(f'Installing pip: {pip}...')
				MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)

				# Install the pip package
				sub.run(
					["pip", "install", "-y", pip],
					stdout=sub.PIPE,
					stderr=sub.PIPE)

				# Substract 1
				self.item_to_restore -= 1
				self.update_progressbar_db()
			except Exception as e:
				print(e)
				pass
	## Wallpaper
	def restore_backup_wallpaper(self):
		# Check for at least a wallpaper
		wallpaper_folder = MAIN_INI_FILE.wallpaper_main_folder()  # Assuming this is a valid path

		# Get a list of wallpapers in the specified folder
		wallpapers_to_restore = os.listdir(wallpaper_folder)

		if wallpapers_to_restore:
			# Copy backed up wallpaper to .local/share/wallpapers/
			for wallpaper in os.listdir(wallpaper_folder):

				# Restore
				src = os.path.join(MAIN_INI_FILE.wallpaper_main_folder(), wallpaper)
				dst = os.path.join(HOME_USER, "Pictures")

				print('Copying this wallpaper:', wallpaper)

				# Show it to the UI
				MAIN.ui.label_restoring_status.setText(f'Applying: {wallpaper}...')
				MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)

				# Copy files
				shutil.copy2(src, dst)

			# Handle spaces
			# wallpaper = handle_spaces(wallpaper)

			# Apply wallpaper
			self.apply_wallpaper(wallpaper)

	## Apply Wallpaper
	def apply_wallpaper(self, wallpaper):
		print("Applying", wallpaper)

		# Activate wallpaper option
		if get_user_de() == "gnome" or get_user_de() == 'unity':
			# Detect color scheme
			get_color_scheme = os.popen(DETECT_THEME_MODE)
			get_color_scheme = get_color_scheme.read().strip().replace("'", "")

			# print(get_color_scheme)
			# print(wallpaper)
			# print(f'{HOME_USER}/Pictures/{wallpaper}')

			# Light or Dark wallpaper
			if get_color_scheme == "prefer-light" or get_color_scheme == "default":
				sub.run(
					['gsettings',
					'set',
					'org.gnome.desktop.background',
					'picture-uri',
					f'{HOME_USER}/Pictures/{wallpaper}'],
					stdout=sub.PIPE,
					stderr=sub.PIPE)
			else:
				sub.run(
					['gsettings',
					'set',
					'org.gnome.desktop.background',
					'picture-uri-dark',
					f'{HOME_USER}/Pictures/{wallpaper}'],
					stdout=sub.PIPE,
					stderr=sub.PIPE)

			# Set wallpaper to Zoom
			sub.run(
				["gsettings",
				"set",
				"org.gnome.desktop.background",
				"picture-options",
				"zoom"],
				stdout=sub.PIPE,
				stderr=sub.PIPE)

			################################################################
		elif get_user_de() == "kde":
			# Apply KDE wallpaper
			os.system("""
				dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
				var Desktops=desktops();
				for (i=0;i<Desktops.length;i++)
				{
					d=Desktops[i];
					d.wallpaperPlugin="org.kde.image";
					d.currentConfigGroup=Array("Wallpaper",
												"org.kde.image",
												"General");
					d.writeConfig("Image", "file://%s/.local/share/wallpapers/%s");
				}'""" % (HOME_USER, wallpaper))

			# # TODO
			# # Testing
			# try:
			# 	print("Applying", wallpaper, 'to login screen.')

			# 	# Apply KDE screenlock wallpaper, will be the same as desktop wallpaper
			# 	# wallpaper_full_location = 'file://' + HOME_USER + '/.local/share/wallpapers/' + '"' + wallpaper + '"'
			# 	wallpaper_full_location = 'file://' + HOME_USER + '/.local/share/wallpapers/' + wallpaper

			# 	sub.run([
			# 		'kwriteconfig5',
			# 		'--file', 'kscreenlockerrc',
			# 		'--group', 'Greeter',
			# 		'--group', 'Wallpaper',
			# 		'--group', 'org.kde.image',
			# 		'--group', 'General',
			# 		'--key', 'Image',
			# 		wallpaper_full_location
			# 	], check=True)
			# except Exception as error:
			# 	print(error)
			# 	pass
		else:
			return None
		
	#----------RESTORE TOPICS----------#
	# End
	def end_restoring(self):
		print("Restoring is done!")

		MAIN.is_restore_done = True

		# Update DB
		MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')
		MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')
		MAIN_INI_FILE.set_database_value('RESTORE', 'applications_packages', 'False')
		MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')
		MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_data', 'False')
		MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')
		MAIN_INI_FILE.set_database_value('RESTORE', 'restore_progress_bar', '0')

		# Change to page5
		MAIN.ui.stackedWidget.setCurrentWidget(MAIN.ui.page_5)

		# Automatically reboot
		if MAIN.ui.checkbox_automatically_reboot_page4.isChecked():
			# Reboot system
			print("Rebooting now...")

			# Wait few seconds
			time.sleep(10)

			# Reboot
			sub.run(
				["sudo", "reboot"],
					stdout=sub.PIPE,
					stderr=sub.PIPE)



if __name__ == '__main__':
	APP = QApplication(sys.argv)
	WIDGET = QStackedWidget()

	MAIN_INI_FILE = UPDATEINIFILE()
	MAIN = WelcomeScreen()

	WIDGET.setWindowTitle("Migration Assistant")
	WIDGET.setWindowIcon(QPixmap(SRC_MIGRATION_ASSISTANT_ICON_212PX))
	WIDGET.setFixedSize(900, 600)
	WIDGET.addWidget(MAIN)
	WIDGET.setCurrentWidget(MAIN)
	WIDGET.show()

	APP.exit(APP.exec())
