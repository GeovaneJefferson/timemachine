from setup import *
from prepare_backup import PREPAREBACKUP
from read_ini_file import UPDATEINIFILE
from get_folders_to_be_backup import get_folders
from handle_spaces import handle_spaces
from get_sizes import number_of_item_to_backup, get_item_size
from get_users_de import get_user_de
from notification_massage import notification_message
from backup_flatpak import backup_flatpak
from backup_pip_packages import backup_pip_packages
from backup_wallpaper import backup_wallpaper
from backup_now import LIST_KDE_INCLUDE, LIST_GNOME_INCLUDE
import json

MAIN_INI_FILE = UPDATEINIFILE()
MAIN_PREPARE = PREPAREBACKUP()

backup_home_dict = {}
items_to_backup_dict = {}

# Color
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Supported
SUPPORTED_DE = ['gnome', 'kde', 'unity']

# List of all dates
has_date_time_to_compare = []
date_time_folders_to_check = []


# Define a function to convert the date string to a datetime object
def convert_to_datetime(date_str):
	return datetime.strptime(date_str, '%y-%m-%d')

def get_all_backups_date_time():
	for date in os.listdir(MAIN_INI_FILE.backup_dates_location()):
		# Eclude hidden files/folders
		if not date.startswith('.'):
			# Add all dates to the list
			has_date_time_to_compare.append(date)
	return has_date_time_to_compare


class ANALYSES:
	def __init__(self):
		self.new_files = int()
		self.updates_files = int()
		self.found_items = []

		pass
	def add_to_home_dict(self, item_name, item_path_location):
		# Store item information in the dictionary, to check they size
		backup_home_dict[item_name] = {
			"size": get_item_size(item_path_location),
			"location": item_path_location
			}

	def add_to_backup_dict(self, location, destination, status):
		item_name = str(location).split('/')[-1]

		if os.path.isdir(destination):
			# If directory is empty, return
			if not any(os.scandir(destination)):
				return

		# Add item to dict
		items_to_backup_dict[item_name] = {
			"size": get_item_size(location),
			"location": location,
			"destination": destination,
			"status": status
		}

		# print(json.dumps(items_to_backup_dict, indent=4))

	def is_new_item(self, location):
		# Check if item location in backup exist
		if not os.path.exists(location):
			return True
		else:
			return False

	def compare_sizes(self, location, destination):
		# Compare item from Home <-> from backup
		if get_item_size(location) != get_item_size(destination):
			# Exclude item with 0 bytes size
			if get_item_size(location) != 0:
				return True
		else:
			return False

	def write_to_file(self):
		# Write file and folder information to the output file
		with open(MAIN_INI_FILE.include_to_backup(), "w") as f:
			for item_name, info in items_to_backup_dict.items():
				item_path = info['location']
				destination = info['destination']
				status = info['status']

				if not os.path.isdir(item_path):
					f.write(f"Filename: {item_name}\n")
					f.write(f"Size: {info['size']} bytes\n")
					f.write(f"Location: {item_path}\n")
					f.write(f"Destination: {destination}\n")
					f.write(f"Status: {status}\n")
					f.write("\n")
				else:
					f.write(f"Filename: {str(item_name).split('/')[-1]}\n")
					f.write(f"Size: {info['size']} bytes\n")
					f.write(f"Location: {item_path}\n")
					f.write(f"Destination: {destination}\n")
					f.write(f"Status: {status}\n")
					f.write("\n")

	def get_select_backup_home(self):
		counter = 0
		counter_limit = 0

		try:
			# Loop through items in the source directory
			for counter_limit in range(len(self.get_source_dir())):
				counter_limit = counter_limit

			# Run loop through list
			for _ in range(counter_limit):
				for item_name in os.listdir(self.get_source_dir()[counter]):

					item_path_location = os.path.join(
                        self.get_source_dir()[counter], item_name)

					self.add_to_home_dict(item_name, item_path_location)

				counter += 1
		except FileNotFoundError as e:
			print(e, 140)
			pass

	def get_source_dir(self):
		source_folders = []

		# HOME folders selected by user
		for item in get_folders():
			# Handle spaces
			item = handle_spaces(item)
			source_folders.append(f'{HOME_USER}/{item}')

		# For GNOME or KDE
		user_de = get_user_de()
		if user_de in SUPPORTED_DE:
			for base_dir in [f"{HOME_USER}/.local/share/", f"{HOME_USER}/.config/"]:
				for item in os.listdir(base_dir):
					# Handle spaces
					item = handle_spaces(item)
					if (user_de == 'gnome' and item in list_gnome_include) or \
					   (user_de == 'unity' and item in list_gnome_include) or \
					   (user_de == 'kde' and item in list_include_kde):
						source_folders.append(os.path.join(base_dir, item))

		return source_folders

	def analyse_home(self):
		self.to_check_list = []
		try:
			folders_to_check = get_folders()

			# Loop thourgh folder
			# Search inside current dir
			for i in range(len(folders_to_check)):
				# /home/user/Pictures
				home_folder = os.path.join(HOME_USER, folders_to_check[i])
				for root, _, files in os.walk(home_folder):
					if files:
						for file in files:
							# /home/user/Pictures/image.jpg
							file_location = os.path.join(root, file)
							
							# /media/user/BACKUP/TMB/backups/.main_backup/Pictures
							combine_home_with_backup_dirname = (
								MAIN_INI_FILE.main_backup_folder() + str(file_location).replace(HOME_USER, ''))
							
							#print('File Location:',file_location)
							#print('HOME + BACKUP:', combine_home_with_backup_dirname)
							#print()
							#exit()
							# New file
							if not os.path.exists(combine_home_with_backup_dirname):
								self.add_to_backup_dict(
									location=file_location ,
									destination=combine_home_with_backup_dirname,
									status='NEW')
								
								#print('[NEW]:', combine_home_with_backup_dirname)
							else:
								# Compare file size difference
								if self.compare_sizes(
									location=file_location,
									destination=combine_home_with_backup_dirname):

									# Has no other date to compare to
									if not has_date_time_to_compare: 
										self.add_to_backup_dict(
											location=file_location,
											destination=combine_home_with_backup_dirname,
											status='UPDATED')
										
										print('[UPDATED]:', file_location)
									else:
										# Searching in Date/Time
										# self.to_check_list.append(file_location)
										self.check_with_dates(
											location=file_location, 
											destination=combine_home_with_backup_dirname)

			# Main Backup Folder
			# self.search_in_main_dir()

		except FileNotFoundError as e:
			print(e)
			pass
		
	def check_with_dates(self, location, destination):
		print('------[DATE/TIME]------')
		already_backup_list = []

		# /Documents/Godot_Demos/Street/props/trash/trash.blend
		only_dirname = str(destination).replace(MAIN_INI_FILE.main_backup_folder(), '')
		home_file_name= str(location).split('/')[-1]

		#print(location)
		#print(destination)
		#print(only_dirname)
		#exit()
		
		# Sort the dates in descending order using the converted datetime objects
		sorted_date = sorted(has_date_time_to_compare,
					key=convert_to_datetime,
					reverse=True)

		# DATE
		# Loop through each date folder
		for i in range(len(sorted_date)):
			# Get date path
			update_folder_location = os.path.join(
				MAIN_INI_FILE.backup_dates_location(), sorted_date[i])
				
			# Append 
			date_time_folders_to_check.append(update_folder_location)

		# Len of dates
		for i in range(len(date_time_folders_to_check)):
			# Available times
			for time_folder in os.listdir(date_time_folders_to_check[i]):
				folder_path = os.path.join(date_time_folders_to_check[i], time_folder)

				#print(time_folder)
				#print(folder_path)
				#exit()

				# Search inside time folder
				for root, _, files in os.walk(folder_path):
					if files:
						for file in files:
							file_location = os.path.join(root, file)
							test = str(file_location).replace(folder_path, '')

							print()
							print('------[HOME]------')
							print(home_file_name)
							#print(folder_path)
							print('Only Dirname:', only_dirname)
							# print('DATE/TIME:', test)
							print('Search updates for this file:', location)

							# Find source dirname match
							#HOME: /Documents/Godot_Demos/Street/props/trash/trash.blend
							#DATE/TIME: /Documents/Godot_Demos/Street/props/trash/trash.blend
							if only_dirname not in already_backup_list:
								y = os.path.join(folder_path + only_dirname)

								splitt = folder_path.split('/')[-2:]
								splitt = '/'.join(splitt)

								print()
								print(f'[{splitt}]')
								print('Name:', file)
								print('Where:', file_location)

								## Check if combine location exists
								if home_file_name == file:
								#if os.path.exists(y):
									print()
									print('[MATCH]')
									print('Home Name:', home_file_name)
									print('Backup Name:', file)
									print('[MATCH]')
									print()
									#exit()

									# Compare sizes with Home
									if self.compare_sizes(
										location=location,
										destination=file_location):
										print()
										print('[UPDATED]')
										print('Home Location:', location)
										print('Backup Location:', file_location)
										print('[UPDATED]')
										print()

										self.add_to_backup_dict(
											location=location,
											destination=only_dirname,
											status='UPDATED')

										#exit()
									else:
										print()
										print('[NOT UPDATED]')
										print('Home Location:', location)
										print('Backup Location:', file_location)
										print('[NOT UPDATED]')
										print()
										#exit()

									# Sizes did not changed
									already_backup_list.append(only_dirname)

		#if only_dirname not in already_backup_list:
			#self.add_to_backup_dict(
				#location=location,
				#destination=only_dirname,
				#status='UPDATED')


	def need_to_backup_analyse(self):
		# Check if it's not the first backup with Time Machine
		if os.path.exists(MAIN_INI_FILE.main_backup_folder()):
			# Part of the analyses
			get_all_backups_date_time()
			# self.get_select_backup_home()

			# Loop thourgh Home
			self.analyse_home()

			# Write dict to file .txt
			self.write_to_file()

			# If the number of items to backup is 0
			if number_of_item_to_backup() == 0:
				# Indicate that no backup is needed
				print(YELLOW + 'ANALYSE: No need to backup.' + RESET)
				return False
			else:
				# Write backup information to file
				self.write_to_file()

				# Indicate that backup is needed
				print(GREEN + 'ANALYSE: Need to backup.' + RESET)
				return True
		else:
			# Make the first backup
			print(GREEN + 'ANALYSE: Making first backup.' + RESET)
			return True

	def is_process_running(self, process_title):
		try:
			result = sub.run(
				['pgrep', '-f', process_title],
				check=True,
				stdout=sub.PIPE)
			return bool(result.stdout.strip())
		except sub.CalledProcessError:
			return False


if __name__ == "__main__":
	MAIN = ANALYSES()

	print('Analysing backup...')
	notification_message('Analysing backup...')

	# MAIN.need_to_backup_analyse()

	try:
		# Backup flatpak
		print("Backing up: flatpak applications")
		backup_flatpak()

		# Backup pip packages
		print("Backing up: pip packages")
		backup_pip_packages()

		# TODO
		try:
			# Backup wallpaper
			print("Backing up: Wallpaper")
			backup_wallpaper()
		except:
			pass

		# Need to backup
		if MAIN.need_to_backup_analyse():
			# Prepare backup
			if MAIN_PREPARE.prepare_the_backup():
				print('Calling backup now...')

				# Backup now
				sub.Popen(
					['python3', SRC_BACKUP_NOW_PY],
						stdout=sub.PIPE,
						stderr=sub.PIPE)
		else:
			print('No need to back up.')

			# Backing up to False
			MAIN_INI_FILE.set_database_value(
				'STATUS', 'backing_up_now', 'False')

			# Check if backup checker is not already running
			process_title = "Time Machine - Backup Checker"
			if not MAIN.is_process_running(process_title):
				print(f"No process with the title '{process_title}' is currently running.")
				# Re.open backup checker
				sub.Popen(
					['python3', SRC_BACKUP_CHECKER_PY],
					stdout=sub.PIPE,
					stderr=sub.PIPE)
	except BrokenPipeError:
		# Ignore Broken pipe error
		pass
	except Exception as error:
		print(error)
		# Save error log
		MAIN_INI_FILE.report_error(error)
