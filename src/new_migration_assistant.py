from ui.ui_migration import Ui_WelcomeScreen
from setup import *
from device_location import device_location
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE
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
from notification_massage import notification_message_current_backing_up
from save_info import save_info


class WelcomeScreen(QWidget):
	def __init__(self):
		super(WelcomeScreen, self).__init__()
		self.ui = Ui_WelcomeScreen()
		self.ui.setupUi(self)

		# Countdown
		self.countdown = 10

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

		self.get_devices_location_page2()

	def on_continue_button_clicked_page1(self):
		# Animation
		self.stacked_widget_transition(self.ui.page_2, 'right')

	########################################################
	# PAGE 2
	########################################################
	def get_devices_location_page2(self):
		# Search external inside media
		if device_location():
			self.show_availables_devices_page2(MEDIA)
			# return MEDIA
		elif not device_location():
			self.show_availables_devices_page2(RUN)
			# return RUN
		else:
			self.show_availables_devices_page2(None)
			# return None

	def show_availables_devices_page2(self, location):
		added_devices = []

		self.model = QFileSystemModel()
		self.ui.devices_area_page2.setModel(self.model)

		try:
			# Show availables devices
			for device in os.listdir(f"{location}/{USERNAME}/"):
				# Only show disk the have TMB inside
				if BASE_FOLDER_NAME in os.listdir(f"{location}/{USERNAME}/{device}/"):
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
			self.model.setRootPath(f"{location}/{USERNAME}/")
			self.ui.devices_area_page2.setModel(self.model)
			self.ui.devices_area_page2.setRootIndex(self.model.index(f"{location}/{USERNAME}/"))

		except FileNotFoundError:
			pass

	def on_device_selected_page2(self, selected, deselected):
		# This slot will be called when the selection changes
		selected_indexes = selected.indexes()

		for index in selected_indexes:
			self.selected_device = self.model.data(index)
			# self.selected_item_texts.append(f"{self.get_devices_location_page2()}/{USERNAME}/{self.selected_device}")

		# Enable continue button
		if selected.indexes():
			self.ui.button_continue_page2.setEnabled(True)

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

		if package_location is not None:
			for package in os.listdir(package_location):
				sub_applications_checkboxes = QCheckBox()
				sub_applications_checkboxes.setText(package.capitalize().split('_')[0])
				sub_applications_checkboxes.setChecked(True)
				sub_applications_checkboxes.clicked.connect(
					lambda *args, package=package: self.exclude_applications(package))
				self.ui.applications_sub_checkbox_layout_page3.addWidget(sub_applications_checkboxes)

				self.number_of_item_applications += 1

		else:
			# Disable Application checkbox
			self.ui.checkbox_applications_page3.setEnabled(False)

		# Expand it, 1 item = 20 height
		self.ui.applications_sub_widget_page3.setMinimumHeight(self.number_of_item_applications*30)

	def load_flatpaks_sub_checkbox_page3(self):
		self.has_flatpak_to_restore = []

		# Read installed flatpaks names
		with open(f'{MAIN_INI_FILE.flatpak_txt_location()}', 'r') as flatpaks:
			for flatpak in flatpaks.read().split():
				self.has_flatpak_to_restore.append(flatpak)

		# Has flatpaks to restore
		if self.has_flatpak_to_restore:
			for flatpak in self.has_flatpak_to_restore:
				sub_flatpaks_checkboxes = QCheckBox()
				sub_flatpaks_checkboxes.setText(self.has_flatpak_to_restore[self.number_of_item_flatpaks])
				sub_flatpaks_checkboxes.setChecked(True)
				sub_flatpaks_checkboxes.clicked.connect(
					lambda *args, flatpak=flatpak: self.exclude_flatpaks(flatpak))
				self.ui.flatpaks_sub_checkbox_layout_page3.addWidget(sub_flatpaks_checkboxes)

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
		system_settings_list = []

		for output in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
			system_settings_list.append(output)

		if system_settings_list:
			self.ui.checkbox_system_settings_page3.setEnabled(True)
		else:
			self.ui.checkbox_system_settings_page3.setEnabled(False)

	def on_applications_checkbox_clicked_page3(self):
		# Expand it if selected
		if self.ui.checkbox_applications_page3.isChecked():
			# Add to list to restore
			self.item_to_restore.append('Applications')
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

		self.check_checkboxes()

	def on_flatpaks_checkbox_clicked_page3(self):
		# Expand it if selected
		if self.ui.checkbox_flatpaks_page3.isChecked():
			# Add to list to restore
			self.item_to_restore.append('Flatpaks')
			# Show applications sub checkboxes
			self.ui.flatpaks_sub_widget_page3.show()
			# Update DB
			MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'True')
		else:
			# Remove to list to restore
			self.item_to_restore.remove('Flatpaks')
			# Hide applications sub checkboxes
			self.ui.flatpaks_sub_widget_page3.hide()
			# Update DB
			MAIN_INI_FILE.set_database_value('RESTORE', 'applications_flatpak_names', 'False')
		
		self.check_checkboxes()

	def on_files_and_folders_checkbox_clicked_page3(self):
		# Expand it if selected
		if self.ui.checkbox_files_folders_page3.isChecked():
			# Add to list to restore
			self.item_to_restore.append('Files/Folders')
			# Update DB
			MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'True')
		else:
			# Remove to list to restore
			self.item_to_restore.remove('Files/Folders')
			# Update DB
			MAIN_INI_FILE.set_database_value('RESTORE', 'files_and_folders', 'False')

		self.check_checkboxes()

	def on_system_settings_checkbox_clicked_page3(self):
		if self.ui.checkbox_system_settings_page3.isChecked():
			MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'True')
			# Add "system_settings" to list
			self.item_to_restore.append("System_Settings")
		else:
			MAIN_INI_FILE.set_database_value('RESTORE', 'system_settings', 'False')

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
		print("Exclude flatpak:", exclude)

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
		# Clean flaptak list
		self.has_flatpak_to_restore.clear()

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
			sub.run(["touch", dst])
            
		# Write exclude flatpaks to file
		with open(f"{MAIN_INI_FILE.exclude_applications_location()}", 'w') as exclude:
			for exclude_applications in self.applications_to_be_exclude:
				exclude.write(exclude_applications + "\n")

		#################################
		# FLATPAK
		#################################
		# Create a flatpak exlude file
		if os.path.exists(MAIN_INI_FILE.exclude_flatpaks_location()):
			os.remove(MAIN_INI_FILE.exclude_flatpaks_location())
		else:
			dst = MAIN_INI_FILE.exclude_flatpaks_location()
			sub.run(["touch", dst])
            
		# Write exclude flatpaks to file
		with open(f"{MAIN_INI_FILE.exclude_flatpaks_location()}", 'w') as exclude:
			for exclude_flatpak in self.flatpaks_to_be_exclude:
				exclude.write(exclude_flatpak + "\n")

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
		for wallpaper in os.listdir(f'{MAIN_INI_FILE.wallpaper_main_folder()}'):
			set_wallpaper = f'{MAIN_INI_FILE.wallpaper_main_folder()}/{wallpaper}'

		# From image
		pixmap = QPixmap(SRC_RESTORE_ICON)
		pixmap = pixmap.scaledToWidth(60, Qt.SmoothTransformation)  # Adjust width and transformation mode as needed

		from_image = QLabel(self.ui.from_image_widget)
		from_image.setPixmap(pixmap)
		from_image.setScaledContents(True)
		from_image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		from_image.move(10, 10)

		# To image
		# Wallpaper
		# svg_widget = QSvgWidget()
		# if set_wallpaper.split('.')[-1].endswith('svg'):
		#     svg_widget.load(set_wallpaper)
		#     svg_widget.setFixedSize(80, 80)
		#     svg_widget.setContentsMargins(0, 0, 0, 0)
		#     svg_widget.setAspectRatioMode(Qt.IgnoreAspectRatio)

		#     # svg_widget.move(5, 5)
		# else:
		#     to_image = QLabel(self.ui.to_image_widget)
		#     to_image.setPixmap(QPixmap(set_wallpaper))
		#     to_image.setScaledContents(True)
		#     to_image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

		pixmap = QPixmap(SRC_MONITOR_ICON)
		pixmap = pixmap.scaledToWidth(100, Qt.SmoothTransformation)  # Adjust width and transformation mode as needed

		to_image = QLabel(self.ui.to_image_widget)
		to_image.setPixmap(pixmap)
		to_image.setScaledContents(True)
		to_image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

		# Current pcs name
		self.ui.from_image_label.setText(f"{USERNAME.capitalize()}")
		self.ui.from_image_label.adjustSize()

		# Backup devices name
		self.ui.to_image_label.setText(MAIN_INI_FILE.get_database_value('EXTERNAL', 'name'))
		self.ui.to_image_label.adjustSize()

	def on_restore_button_clicked_page4(self):
		# Disable restore, back button and automatically checkbox
		self.ui.button_restore_page4.setEnabled(False)
		self.ui.button_back_page4.setEnabled(False)
		self.ui.checkbox_automatically_reboot_page4.setEnabled(False)

		# Load page5
		self.load_restore_page5()

		# Show progressbar
		self.ui.progress_bar_restoring.show()

		# Call restore class
		command = SRC_RESTORE_CMD_PY
		sub.Popen(["python3", command])

		# Update DB
		MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'True')

		# Start QTimer to read notification
		timer.timeout.connect(self.update_status_feedback)
		timer.start(1000)

	def on_back_button_clicked_page4(self):
		# Animation
		self.stacked_widget_transition(self.ui.page_3, 'left')

	def on_automatically_reboot_clicked(self):
		if self.ui.checkbox_automatically_reboot_page4.isChecked():
			print("Reboot True")
			return True
		else:
			print("Reboot False")
			return False

	def stacked_widget_transition(self, page, direction):
		width = self.ui.stackedWidget.width()

		if direction == 'right':
			page.setGeometry(QRect(width, 0, width, self.ui.stackedWidget.height()))
		else:
			page.setGeometry(QRect(-width, 0, -width, self.ui.stackedWidget.height()))

		animation = QPropertyAnimation(page, b'geometry', page)
		animation.setDuration(1000)
		animation.setEasingCurve(QEasingCurve.OutCubic)
		animation.setStartValue(page.geometry())
		animation.setEndValue(QRect(0, 0, width, self.ui.stackedWidget.height()))
		animation.start()

		self.ui.stackedWidget.setCurrentWidget(page)

	def update_status_feedback(self):
		self.ui.label_restoring_status.setText(MAIN_INI_FILE.get_database_value('INFO', 'saved_notification'))
		self.ui.label_restoring_status.adjustSize()
		self.ui.label_restoring_status.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

		pb_value = MAIN_INI_FILE.get_database_value('RESTORE', 'restore_progress_bar').split('.')[0]
		MAIN.ui.progress_bar_restoring.setValue(int(pb_value))

		if not MAIN_INI_FILE.get_database_value('STATUS', 'is_restoring') :
			# Stop previous timer
			timer.stop()
			# Change to page5
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)

			# Automatically reboot
			if MAIN.on_automatically_reboot_clicked():
				# Reboot system
				print("Rebooting now...")
				sub.run(["sudo", "reboot"])
			else:
				print("All done.")

	def update_progressbar(self):
		pb_value = int(MAIN_INI_FILE.get_database_value('RESTORE', 'restore_progress_bar'))
		MAIN.ui.progress_bar_restoring.setValue(pb_value)

	########################################################
	# PAGE 5
	########################################################
	def load_restore_page5(self):
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