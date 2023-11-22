from setup import *
from read_ini_file import UPDATEINIFILE
from get_folders_to_be_backup import get_folders
from notification_massage import notification_message
from handle_spaces import handle_spaces

# Handle signal
import error_catcher
signal.signal(signal.SIGINT, error_catcher.signal_exit)
signal.signal(signal.SIGTERM, error_catcher.signal_exit)


list_gnome_include = [
	'gnome-shell',
	'dconf'
	]

# Backup .local/share/ selected folder for KDE
list_include_kde = [
	'kwin',
	'plasma_notes',
	'plasma',
	'aurorae',
	'color-schemes',
	'fonts',
	'kate',
	'kxmlgui5',
	'icons',
	'themes',

	'gtk-3.0',
	'gtk-4.0',
	'kdedefaults',
	'dconf',
	'fontconfig',
	'xsettingsd',
	'dolphinrc',
	'gtkrc',
	'gtkrc-2.0',
	'kdeglobals',
	'kwinrc',
	'plasmarc',
	'plasmarshellrc',
	'kglobalshortcutsrc',
	'khotkeysrc',
	'kwinrulesrc'
	'dolphinrc',
	'ksmserverrc',
	'konsolerc',
	'kscreenlockerrc',
	'plasmashellr',
	'plasma-org.kde.plasma.desktop-appletsrc',
	'plasmarc',
	'kdeglobals',
	
	'gtk-3.0',
	'gtk-4.0',
	'kdedefaults',
	'dconf',
	'fontconfig',
	'xsettingsd',
	'dolphinrc',
	'gtkrc',
	'gtkrc-2.0',
	'kdeglobals',
	'kwinrc',
	'plasmarc',
	'plasmarshellrc',
	'kglobalshortcutsrc',
	'khotkeysrc'
	]

# HOME
def count_files():
	file_count = 0
	subdirectories = get_folders()

	print('Counting total files...')
	for i in subdirectories:
		source_folder = os.path.join(HOME_USER, i)

		# Sum all files from selected HOME folders
		for root, dirs, files in os.walk(source_folder):
			# Add to count
			file_count += len(files)

	return file_count

def make_first_backup():
	# Get a list of subdirectories to back up
	subdirectories = get_folders()
	
	# Target location
	target_folder = MAIN_INI_FILE.main_backup_folder() + '/'
	# target_folder = '/media/macbook/Backup_Drive/TMB/test'

	# Number of total files to back up
	total_files = count_files()
	
	# Copied file value
	copied_files = 0

	# Loop through selected HOME folders to back up
	for i in subdirectories:
		source_folder = os.path.join(HOME_USER, i)

		# Loop through current HOME folder location
		for root, dirs, files in os.walk(source_folder):
			for file in files:
				source_path = os.path.join(root, file)
				relative_path = os.path.relpath(source_path, source_folder)
				target_path = os.path.join(target_folder, i, relative_path)
				
				# Create dst folder with relative name is necessary
				os.makedirs(os.path.dirname(target_path), exist_ok=True)

				try:
					# Back up 
					shutil.copy(source_path, target_path)
					print(f"Backed up: {source_path}")

				except Exception as e:
					print(f"Error while backing up {source_path}: {e}")
				
				# Add 1 to copied file value
				copied_files += 1

				# Caculate the progress bar
				progress = int(copied_files / total_files * 100)
				print(progress)
				print('Copied file:', copied_files, '/', total_files)
				
				# Save current progress value to DB
				MAIN_INI_FILE.set_database_value(
					'STATUS', 'progress_bar', str(progress))

				# Save current backing up
				MAIN_INI_FILE.set_database_value(
	            	'INFO', 'current_backing_up', source_path)


	# Set progress bar value to None
	MAIN_INI_FILE.set_database_value(
			'STATUS', 'progress_bar', 'None')


class BACKUP:
	# Backup USER HOME 
	def backup_home(self, first_backup):
		# Target location is empty
		if not any(os.scandir(MAIN_INI_FILE.main_backup_folder())):
			# Save time informations
			MAIN_INI_FILE.set_database_value(
				'INFO',
				'oldest_backup_date',
				MAIN_INI_FILE.current_full_date_plus_time_str())

			# Make first backup 
			make_first_backup()

		else:
			# Static time value, fx. 10-00
			STATIC_TIME_FOLDER = MAIN_INI_FILE.time_folder_format().split('/')[-1] 

			# Read the include file and process each item's information
			with open(MAIN_INI_FILE.include_to_backup(), 'r') as f:
				lines = f.readlines()
				
				for i in range(0, len(lines), 6):
					try:
						filename = lines[i + 0].split(':')[-1].strip()
						size_string = lines[i + 1].split(':')[-1].strip()
						size = int(size_string.split()[0])
						location = lines[i + 2].split(':')[-1].strip()
						destination = lines[i + 3].split(':')[-1].strip()
						status = lines[i + 4].split(':')[-1].strip()
						
						##########################################################
						# .MAIN BACKUP
						##########################################################
						if status == 'NEW':  # Is a new file/folder
							# Copy to .main backup
							destination_location = (
								f'{MAIN_INI_FILE.main_backup_folder()}{destination}')

							# Remove invalid keys
							destination_location = destination_location.replace('../','')
						
						##########################################################
						# LATEST DATE/TIME
						##########################################################
						elif status == 'UPDATED':
							# Sent to a new date/time backup folder
							destination_location = (
								f'{MAIN_INI_FILE.time_folder_format()}{destination}')
							
							# Static time folder 
							# So it won't update if backup passes more than one minute
							destination_location = MAIN_INI_FILE.time_folder_format().split('/')[:-1]
							destination_location = '/'.join(destination_location)

							# Add static time to it
							destination_location = (destination_location + 
								'/' + STATIC_TIME_FOLDER + destination)
						
						try:
							# Back up 
							# is a dir
							if os.path.isdir(location):
								# Dir has files inside
								if any(os.scandir(location)):
									# Create proper for it
									os.makedirs(
									os.path.dirname(
									os.path.join(destination_location, filename)), exist_ok=True)
								
									shutil.copy(os.path.join(location, filename), destination_location)
							else:
								shutil.copy(location, destination_location)
							
							print(f"Backed up: {os.path.join(location, filename)}")

						except Exception as e:
							print(f"Error while backing up {os.path.join(location, filename)}: {e}")
					
					except Exception as e:
						print(e)
						exit()

	# HIDDEN FILES/FOLDERS
	def backup_hidden_home(self, user_de):
		# Gnome and KDE
		if user_de == 'gnome' or user_de == 'kde': 
			self.backup_hidden_local_share(user_de)
			self.backup_hidden_config(user_de)

			# Extra step for kde
			if user_de == 'kde':
				self.backup_hidden_kde_share() 

	def backup_hidden_local_share(self, user_de):
		# Local share
		for folder in os.listdir(LOCAL_SHARE_LOCATION):
			# Handle spaces
			folder = handle_spaces(folder)
			
			# Gnome or KDE
			if user_de == 'gnome':
				compare_list = list_gnome_include
				
				# Destination
				dst = MAIN_INI_FILE.gnome_local_share_main_folder() + '/' + folder

			elif user_de == 'kde':
				compare_list = list_include_kde

				# Destination
				dst = MAIN_INI_FILE.kde_local_share_main_folder() + '/' + folder

			# Find match in list
			if folder in compare_list:
				src = LOCAL_SHARE_LOCATION + folder
				# dst = MAIN_INI_FILE.main_backup_folder() + '/.local/share/' + folder
				
				# Create current directory in backup device
				dst_moded = dst.split('/')[:-1]  # Remove the last component (file name)
				dst_moded = '/'.join(dst_moded)    # Join components with forward slashes

				if not os.path.exists(dst_moded):
					os.makedirs(dst_moded, exist_ok=True)

				print(f'Backing up: {LOCAL_SHARE_LOCATION}{folder}')

				notification_message(f'Backing up: .local/share/{folder}')
				
				sub.run(
					['cp', '-rvf', src, dst],
					stdout=sub.PIPE,
					stderr=sub.PIPE)

	def backup_hidden_config(self, user_de):
		# Config
		for folder in os.listdir(CONFIG_LOCATION):
			# Handle spaces
			folder = handle_spaces(folder)

			# Adapt for users DE
			if user_de == 'gnome':
				compare_list = list_gnome_include
		   
				# Destination
				dst = MAIN_INI_FILE.gnome_config_main_folder() + '/' + folder

			elif user_de == 'kde':
				compare_list = list_include_kde

				# Destination
				dst = MAIN_INI_FILE.kde_config_main_folder() + '/' + folder

			if folder in compare_list:
				src = CONFIG_LOCATION + folder
				# dst = MAIN_INI_FILE.main_backup_folder() + '/.config/' + folder
				
				# Create current directory in backup device
				dst_moded = dst.split('/')[:-1]  # Remove the last component (file name)
				dst_moded = '/'.join(dst_moded)    # Join components with forward slashes

				if not os.path.exists(dst_moded):
					os.makedirs(dst_moded, exist_ok=True)

				print(f'Backing up: {CONFIG_LOCATION}{folder}')
				
				notification_message(f'Backing up: .config/{folder}')
				
				sub.run(
					['cp', '-rvf', src, dst],
					stdout=sub.PIPE,
					stderr=sub.PIPE)
				
	def backup_hidden_kde_share(self):
		try:
			# .kde/share/
			for folder in os.listdir(KDE_SHARE_LOCATION):
				# Handle spaces
				folder = handle_spaces(folder)
			
				src = KDE_SHARE_LOCATION + folder
				# dst = MAIN_INI_FILE.main_backup_folder() + '/.kde/share/' + folder
				
				# Destination
				dst = MAIN_INI_FILE.kde_share_config_main_folder() + '/' + folder

				# Create current directory in backup device
				dst_moded = dst.split('/')[:-1]  # Remove the last component (file name)
				dst_moded = '/'.join(dst_moded)    # Join components with forward slashes
				
				if not os.path.exists(dst_moded):
					os.makedirs(dst_moded, exist_ok=True)

				print(f'Backing up: {KDE_SHARE_LOCATION}{folder}')
				
				notification_message(f'Backing up: .kde/share/{folder}')
				
				sub.run(
					['cp', '-rvf', src, dst],
					stdout=sub.PIPE,
					stderr=sub.PIPE)
					
		except FileNotFoundError as e:
			print(e)
			pass

	def end_backup(self):
		print("Backup is done!")
		print("Sleeping for 60 seconds")
		
		# Finnish notification
		notification_message('Finalizing backup...')

		# Wait x, so if it finish fast, won't repeat the backup
		time.sleep(60)

		# Update DB
		MAIN_INI_FILE.set_database_value(
			'STATUS', 'backing_up_now', 'False')
		MAIN_INI_FILE.set_database_value(
			'STATUS', 'unfinished_backup', 'No')

		
if __name__ == "__main__":
	MAIN = BACKUP()
	MAIN_INI_FILE = UPDATEINIFILE()
			
	######################################################################
	# Update db
	######################################################################
	MAIN_INI_FILE.set_database_value(
		'STATUS', 'backing_up_now', 'True')

	# Set oldest backup date
	if MAIN_INI_FILE.oldest_backup_date() is None:
		# Oldest backup today
		MAIN_INI_FILE.set_database_value(
			'INFO',
			'oldest_backup_date',
			MAIN_INI_FILE.current_full_date_plus_time_str())

	# Set latest backup date
	MAIN_INI_FILE.set_database_value(
		'INFO',
		'latest_backup_date',
		MAIN_INI_FILE.current_full_date_plus_time_str())

	try:
		# backup hidden home
		# MAIN.backup_hidden_home(get_user_de())

		# First backup
		if not any(os.scandir(MAIN_INI_FILE.main_backup_folder())):  # Target location is empty
			MAIN.backup_home(True)
		else:
			MAIN.backup_home(False)
		
		# End backup process
		MAIN.end_backup()

	except Exception as e:
		print(e)
		# if 'BrokenPipeError: [Errno 32] Broken pipe' not in e:
		MAIN_INI_FILE.report_error(e)

		# Set backup now to False
		MAIN_INI_FILE.set_database_value(
			'STATUS', 'backing_up_now', 'False')
		
		# Unfinished to Yes 
		MAIN_INI_FILE.set_database_value(
			'STATUS', 'unfinished_backup', 'Yes')

	# Wait few seconds
	time.sleep(60)

	# Re-open backup checker
	sub.Popen(
		['python3', SRC_BACKUP_CHECKER_PY], 
		stdout=sub.PIPE, 
		stderr=sub.PIPE)


