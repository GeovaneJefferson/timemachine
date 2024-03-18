from ui.ui_migration import Ui_WelcomeScreen
from setup import *
from device_location import device_location
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE
from save_info import save_info
from create_directory import create_directory, create_file

from get_users_de import get_user_de
from restore_backup_wallpaper import restore_backup_wallpaper
from restore_backup_flatpaks_data import restore_backup_flatpaks_data
# from restart_kde_session import restart_kde_session
from restore_kde_share_config import restore_kde_share_config
from restore_kde_config import restore_kde_config
from restore_kde_local_share import restore_kde_local_share
from handle_spaces import handle_spaces
from create_backup_checker_desktop import create_directory



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
		self.item_to_restore = []
		self.applications_to_be_exclude = []

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

		#######################################################################
		# Page 5
		#######################################################################
		self.ui.button_back_page4.clicked.connect(self.on_back_button_clicked_page4)
		# Connections
		self.ui.button_close_page5.clicked.connect(lambda: exit())

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
			print(MAIN_INI_FILE.backup_folder_name())

			folder_check = os.path.join(self.devices_from(), USERNAME)
			folder_check = os.path.join(folder_check, self.selected_device)
			folder_check = os.path.join(folder_check, BASE_FOLDER_NAME)
			print(folder_check)

			# Allow only if the selected folder has TMB inside
			# Enable continue button
			if selected.indexes():
				# Check if is 'TMB' inside selected drive
				if os.path.exists(folder_check):
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
		self.list_of_flatpaks_to_restore = []

		# Read installed flatpaks names
		with open(f'{MAIN_INI_FILE.flatpak_txt_location()}', 'r') as flatpaks:
			for flatpak in flatpaks.read().split():
				if flatpak not in self.list_of_flatpaks_to_restore:
					self.list_of_flatpaks_to_restore.append(flatpak)

		# Has flatpaks to restore
		if self.list_of_flatpaks_to_restore:
			for flatpak in self.list_of_flatpaks_to_restore:
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

	def load_system_settings_page3(self):
		wallpaper_folder = MAIN_INI_FILE.wallpaper_main_folder()  

		# Get a list of files in the specified folder
		system_settings_list = os.listdir(wallpaper_folder)

		# Enable/disable the checkbox based on the presence of files
		self.ui.checkbox_system_settings_page3.setEnabled(bool(system_settings_list))

	def on_applications_checkbox_clicked_page3(self):
		# Expand it if selected
		if self.ui.checkbox_applications_page3.isChecked():
			# Add to list to restore
			self.item_to_restore.append('Applications')
			# Show applications sub checkboxes
			self.ui.applications_sub_widget_page3.show()
		else:
			# Remove to list to restore
			self.item_to_restore.remove('Applications')
			# Hide applications sub checkboxes
			self.ui.applications_sub_widget_page3.hide()
			# Clear applications exclude list
			self.applications_to_be_exclude.clear()

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

	def on_system_settings_checkbox_clicked_page3(self):
		if self.ui.checkbox_system_settings_page3.isChecked():
			# Add "system_settings" to list
			self.item_to_restore.append("System_Settings")
		else:
			if "System_Settings" in self.item_to_restore:
				self.item_to_restore.remove("System_Settings")

		self.check_checkboxes()

	def exclude_applications(self, exclude):
		print("Exclude application:", exclude)

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
		if exclude not in self.list_of_flatpaks_to_restore:
			print("Adding flatpak:", exclude)
			self.list_of_flatpaks_to_restore.append(exclude)
		else:
			print("Removing flatpak:", exclude)
			self.list_of_flatpaks_to_restore.remove(exclude)

		# If all sub checboxes was deselected
		if not self.list_of_flatpaks_to_restore:
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
		print(self.item_to_restore)

		#################################
		# APPLICATIONS
		#################################
		# Create a application exlude file
		if os.path.exists(MAIN_INI_FILE.exclude_applications_location()):
			os.remove(MAIN_INI_FILE.exclude_applications_location())
		else:
			dst = MAIN_INI_FILE.exclude_applications_location()
			# Check if the directory exists, and create it if necessary
			create_directory(dst)
			# Check if the file exists, and create it if necessary
			create_file(dst)
			
		# Write exclude flatpaks to file
		with open(f"{MAIN_INI_FILE.exclude_applications_location()}", 'w') as exclude:
			for exclude_applications in self.applications_to_be_exclude:
				exclude.write(exclude_applications + "\n")

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
		self.ui.checkbox_automatically_reboot_page4.setVisible(False)
		
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

		# self.update_pb()
		# Show progressbar
		self.ui.progress_bar_restoring.show()

		# Update DB
		MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'True')

		# Call restore class asynchronously
		RESTORE_PROCESS = RESTORE()
		# asyncio.run(self.start_restoring_and_update_db())
		# asyncio.run(RESTORE_PROCESS.start())
		RESTORE_PROCESS.start_restoring()
	
	def update_status_feedback(self):
		self.ui.label_restoring_status.setText(
			MAIN_INI_FILE.get_database_value('INFO', 'saved_notification'))
		
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
		
		#  Get length of the restore list
		if MAIN.ui.checkbox_applications_page3.isChecked():
			# Number of flatpaks items
			applicationsCount = int(MAIN.number_of_item_applications - len(MAIN.applications_to_be_exclude))
			self.item_to_restore += applicationsCount
		
		if MAIN.ui.checkbox_flatpaks_page3.isChecked():
			# Number of flatpaks items
			flatpaksCount = int(len(MAIN.list_of_flatpaks_to_restore))
			self.item_to_restore += flatpaksCount
		
		# if MAIN.ui.checkbox_flatpaks_page3.isChecked():
		# 	self.item_to_restore += 1
		
		if MAIN.ui.checkbox_files_folders_page3.isChecked():
			self.item_to_restore += 1
		
		if MAIN.ui.checkbox_system_settings_page3.isChecked():
			self.item_to_restore += 1

		# Only one item inside restore list
		if self.item_to_restore == 1:
			# Show 99%
			self.progress_increment = round(99 / self.item_to_restore)
		else:
			self.progress_increment = round(100 / self.item_to_restore)

	def update_progressbar_db(self):
		try:
			pb_value = round(self.progress_increment / (self.item_to_restore) * 100)
			# Fix at 100%
			if pb_value == 100:
				pb_value = 99
			MAIN.ui.progress_bar_restoring.setValue(pb_value)
		except ZeroDivisionError:
			pass

	def start_restoring(self):
		# First change the wallpaper
		if MAIN.ui.checkbox_system_settings_page3.isChecked():
			# self.update_progressbar_db()
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
			# self.update_progressbar_db()
			print('Restoring Applications Packages...')
			self.restore_backup_package_applications()
	   
		# Restore flatpaks
		if MAIN.ui.checkbox_flatpaks_page3.isChecked():
			# self.update_progressbar_db()
			print('Restoring Flatpak Applications...')
			self.restore_backup_flatpaks_applications()
		
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

				# Copy everything from src to dst folder
				for i in os.listdir(src):
					x = src + i
					
					print('Restoring Home Folder:', x)

					# Show current installing flatpak to the user
					MAIN.ui.label_restoring_status.setText(f'Copying: {x}...')
					MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)
					
					# Copy files
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
			# Eclude hidden files/folders
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
							print(f'Restoring {source} to: {destination_location}')
							
							# Show current installing to the user
							MAIN.ui.label_restoring_status.setText(
								f'Copying to: {destination_location}...')
							MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)
						
							# shutil.copy(
							#     source,
							#     destination_location)
							shutil.copy2(source, destination_location)

							# Add to 'Added list'
							added_list.append(files[i])

	## Application packages
	def restore_backup_package_applications(self):
		print("Installing applications packages...")
		
		try:             
			with open(MAIN_INI_FILE.exclude_applications_location(), 'r') as read_exclude:
				read_exclude = read_exclude.read().split("\n")
		except:
			pass

		try:    
			package_manager = MAIN_INI_FILE.get_database_value('INFO', 'packagermanager') 

			if package_manager == DEB_FOLDER_NAME:
				################################################################################
				# Restore DEBS
				################################################################################
				for package in os.listdir(MAIN_INI_FILE.deb_main_folder()):
					# Install only if package if not in the exclude app list
					if package not in read_exclude:
						# Install it
						command = os.path.join(MAIN_INI_FILE.deb_main_folder(), package)
					
						print(f"Installing {command}")
						
						# Show current installing to the user
						MAIN.ui.label_restoring_status.setText(f'Installing: {command}...')
						MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)
						
						sub.run(
							["sudo", "dpkg", "-i", command],
							stdout=sub.PIPE,
							stderr=sub.PIPE)

				# Fix packages installation
				sub.run(
					["sudo", "apt", "install", "-f"],
					stdout=sub.PIPE,
					stderr=sub.PIPE)
				
				# Substract 1
				self.item_to_restore -= 1
				self.update_progressbar_db()

			elif package_manager == RPM_FOLDER_NAME:
				################################################################################
				# Restore RPMS
				################################################################################
				for package in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
					print(f"Installing {MAIN_INI_FILE.rpm_main_folder()}/{package}")

					# Install only if package if not in the exclude app list
					if package not in read_exclude:
						# Install it
						command = os.path.join(MAIN_INI_FILE.rpm_main_folder(), package)
					
						print(f"Installing {command}")
						
						# Show current installing to the user
						MAIN.ui.label_restoring_status.setText(f'Installing: {command}...')
						MAIN.ui.label_restoring_status.setAlignment(Qt.AlignCenter)
						
						sub.run(
							["sudo", "rpm", "-ivh", "--replacepkgs", command],
							stdout=sub.PIPE,
							stderr=sub.PIPE)
						
						# Substract 1
						self.item_to_restore -= 1
						self.update_progressbar_db()
		except Exception as e:
			print(e)
			pass

	## Flatpaks
	def restore_backup_flatpaks_applications(self):
		for cnt in range(len(MAIN.list_of_flatpaks_to_restore)):
			flatpak = str(MAIN.list_of_flatpaks_to_restore[cnt]).strip()

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
		if  get_user_de() == "gnome":
			# Detect color scheme
			get_color_scheme = os.popen(DETECT_THEME_MODE)
			get_color_scheme = get_color_scheme.read().strip().replace("'", "")

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
			
			# TODO
			# Testing
			try:
				# Apply KDE screenlock wallpaper, will be the same as desktop wallpaper
				wallpaper_full_location = 'file://' + HOME_USER + '/.local/share/wallpapers/' + '"' + wallpaper + '"'
				sub.run([
					'kwriteconfig5',
					'--file', 'kscreenlockerrc',
					'--group', 'Greeter',
					'--group', 'Wallpaper',
					'--group', 'org.kde.image',
					'--group', 'General',
					'--key', 'Image',
					wallpaper_full_location
				], check=True)
			except Exception as error:
				print(error)
				pass
		
		else:
			return None
	#----------RESTORE TOPICS----------#

	# End
	def end_restoring(self):
		print("Restoring is done!")
		# Stop the QTimer after the asynchronous operation is complete
		timer.stop()

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