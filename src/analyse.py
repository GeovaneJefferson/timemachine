from setup import *
from get_folders_to_be_backup import get_folders
from handle_spaces import handle_spaces
from get_sizes import number_of_item_to_backup, get_item_size
from get_users_de import get_user_de
from prepare_backup import PREPAREBACKUP
from prepare_backup import create_base_folders
from notification_massage import notification_message
from read_ini_file import UPDATEINIFILE
from backup_flatpak import backup_flatpak
from backup_pip_packages import backup_pip_packages
from backup_wallpaper import backup_wallpaper
from backup_now import list_include_kde, list_gnome_include
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
rest_list = []
no_need_to_update_list = []
already_checked = []
files_to_datetime_check = []

# Define a function to convert the date string to a datetime object
def convert_to_datetime(date_str):
	return datetime.strptime(date_str, '%y-%m-%d')

def get_all_backups_date_time():
	for date in os.listdir(MAIN_INI_FILE.backup_dates_location()):
		# Eclude hidden files/folders
		if not date.startswith('.'):
			# Add all dates to the list
			has_date_time_to_compare.append(date)

class ANALYSES:
	def add_to_home_dict(self, item_name, item_path_location):
		# Store item information in the dictionary, to check they size
		backup_home_dict[item_name] = {
			"size": get_item_size(item_path_location),
			"location": item_path_location
			}
		
	def add_to_backup_dict(self, location, destination, status):
		item_name = str(location).split('/')[-1] 

		# Analysing right now
		notification_message(
			f'Analysing: {self.item_name}' )

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
			print(e)
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
					   (user_de == 'kde' and item in list_include_kde):
						source_folders.append(os.path.join(base_dir, item))
		
		return source_folders
	
	def analyse_home(self):
		try:                  
			# Source from .main backup folder
			for item_name, info in backup_home_dict.items():
				self.item_name = item_name

				# Handle spaces
				self.item_name = handle_spaces(item_name)

				# Home item path
				self.item_path_location_top_level = info['location']
			
				# if os.path.isdir(self.item_path_location_top_level):
				# 	self.item_path_location_top_level = os.path.join(self.item_path_location_top_level, self.item_name)

				# Remove home username
				self.item_without_username_location = (
					str(self.item_path_location_top_level).replace(f'{HOME_USER}/', ' ').strip())
				# self.item_without_username_location = os.path.dirname(self.item_path_location_top_level).replace(f'{HOME_USER}/', ' ').strip()

				# Only item dirname. Fx. Desktop
				self.item_dirname = os.path.dirname(self.item_path_location_top_level)

				# Destination/Source full location
				self.combined_home_with_backup_location = (
					os.path.join(MAIN_INI_FILE.main_backup_folder(), self.item_without_username_location)
					)

				# Item main dir
				self.item_home_dirname = os.path.join(HOME_USER, self.item_dirname)

				# Extracted item dirname
				self.extracted_item_dirname = os.path.dirname(self.item_path_location_top_level)
				self.extracted_item_dirname = str(self.extracted_item_dirname).replace(HOME_USER, '')
				self.extracted_item_dirname = self.extracted_item_dirname.split('/')[3:]
				self.extracted_item_dirname = ('/').join(self.extracted_item_dirname) + '/'

				# Main Backup Folder
				self.search_in_main_dir()

		except FileNotFoundError as e:
			print(e)
			pass
		
		print('LIST OF UPDATED FILES.')
		print('\n'.join(files_to_datetime_check))
		print()
		self.search_in_all_date_time_file()


	def check_this_item(self):  
		# Process
		'''
		1 - Check the item
			- Is a new file/folder?
				True:
					- Send to Main backup folder
				False:
					- Has at least a backup date/time to compare to?
						True:
							- Compare file/folder sizes (Home <-> Latest backup folder (date/time))
							- Has changed?
								True:
									- Search inside for the updates
										Compare with Main Backup Folder
										- Is a new file/folder?
											True:
												- Send to Main backup folder
											False:
												- Compare file/folder sizes (Home <-> Latest backup folder (date/time))
										
										Compare with Latest Backup date/time
										- Has changed?
											- True: Send to a new date/time backup folder
		'''


		# # MAIN 
		# # No Date/Time folder to compare
		# if not has_date_time_to_compare:
		# 	# This item was already backup, check for updates
		# 	if os.path.exists(self.combined_home_with_backup_location):
		# 		# Compera item with the backup one
		# 		if self.compare_sizes(
		# 			self.item_path_location_top_level, 
		# 			self.combined_home_with_backup_location):
					
		# 			# Item has been updated
		# 			if not os.path.isdir(self.item_path_location_top_level):
		# 				# Is a file
		# 				self.add_to_backup_dict(
		# 					self.item_path_location_top_level, 
		# 					self.item_without_username_location, 
		# 					'UPDATED')
		# 			else:
		# 				# Search inside this folder
		# 				self.search_in_main_dir()
		# 	else:
		# 		# Backtup this NEW item
		# 		self.add_to_backup_dict(
		# 			self.item_path_location_top_level, 
		# 			self.combined_home_with_backup_location, 
		# 			'NEW')
		# else:
		# 	# DATE/TIME
		# 	if not os.path.exists(self.combined_home_with_backup_location):
		# 		if not os.path.isdir(self.item_path_location_top_level):
		# 			# Has itens inside
		# 			# if any(os.scandir(self.item_path_location_top_level)):
		# 			# Backtup this NEW item
		# 			self.add_to_backup_dict(
		# 				self.item_path_location_top_level, 
		# 				self.combined_home_with_backup_location, 
		# 				'NEW')
		# 		else:
		# 			# UPDATED 
		# 			self.search_in_all_date_time_file()

	def search_in_main_dir(self):
		# Loop through the files to find updates
		for root, _, files in os.walk(self.item_path_location_top_level):
			if files:
				for file in files:
					# Is a match
					local_item_path_location = os.path.join(root, file)
					# local_file_only_name = str(local_item_path_location).split('/')[-1:][0]

					i = str(local_item_path_location).replace(MAIN_INI_FILE.main_backup_folder(), '')
					i = i.replace(HOME_USER, '')
					local_combined_home_with_backup_location = MAIN_INI_FILE.main_backup_folder() + i

					# print(local_item_path_location)
					# print(i)
					# print(local_combined_home_with_backup_location)
					
					check_home_folder_size = '/'.join(str(local_item_path_location).split('/')[:-1]) 
					check_backup_folder_size = '/'.join(str(local_combined_home_with_backup_location).split('/')[:-1]) 
					
					# print(check_home_folder_size)
					# print(check_backup_folder_size)
					# exit()

					'''
					Loop through user's home, if item do not exist in .main backup
					folder, is a new item. 
					'''
					# New Item
					if not os.path.exists(local_combined_home_with_backup_location):
						self.add_to_backup_dict(
							local_item_path_location , 
							local_combined_home_with_backup_location, 
							'NEW')
					else:
						# Check folder for size diff
						if self.compare_sizes(
							check_home_folder_size, 
							check_backup_folder_size):

							# Check files for size diff (.main backup)
							if self.compare_sizes(
								local_item_path_location,
								local_combined_home_with_backup_location):
								# if not os.path.isdir(local_combined_home_with_backup_location):
								# Destination will be only the dirname, without the Home username.
								# Final destination will be set in backup_now script
								destinarion = (
									str(os.path.dirname(
										local_item_path_location)).replace(
											f'{HOME_USER}/', ' ').strip())
								
								# Has not date/time to compare to
								if not has_date_time_to_compare:
									# Date/Time Folder
									self.add_to_backup_dict(
										local_item_path_location, 
										os.path.join(destinarion, file), 
										'UPDATED')
								else:
									# Check files for size diff (date/time)
									files_to_datetime_check.append(local_item_path_location)

	def search_in_all_date_time_file(self):
		# Sort the dates in descending order using the converted datetime objects
		sorted_date = sorted(has_date_time_to_compare,
					key=convert_to_datetime,
					reverse=True)

		# Loop through each date folder
		for i in range(len(sorted_date)):
			# Get date path
			date_path_location = os.path.join(
				MAIN_INI_FILE.backup_dates_location(), sorted_date[i])

			# Loop through each time folder in the current date folder
			# Start from the latest time_path folder
			for time_path_location in reversed(os.listdir(date_path_location)):
				# Get data path + time path, join it
				date_time_path_location = os.path.join(date_path_location, time_path_location)

				# Loop through the files in the current time folder
				for root, _, files in os.walk(date_time_path_location):
					# Has files inside
					if files:
						for file in files:
							# Is a match
							datetime_location = os.path.join(root, file)
							
							# /Documents/Godot_Demos/Street/props/cinder_blocks/cinder_blocks.blend
							datetime_removed = str(datetime_location).replace(date_time_path_location, '')
							# Add to HOME user
							modeed_home_item = HOME_USER + datetime_removed
							
							# print(datetime_location)
							# print(datetime_removed)
							# print(modeed_home_item)
							print(file)
							# exit()

							if file not in already_checked:
								if self.compare_sizes(
									modeed_home_item, 
									datetime_location):		

									destinarion = (
										str(os.path.dirname(
											modeed_home_item)).replace(
												f'{HOME_USER}/', ' ').strip())
									
									already_checked.append(file)
									
									# Date/Time Folder
									if not os.path.isdir(modeed_home_item):
										self.add_to_backup_dict(
											modeed_home_item, 
											os.path.join(destinarion, file), 
											'UPDATED')
									else:
										self.add_to_backup_dict(
											modeed_home_item, 
											destinarion, 
											'UPDATED')

	def search_in_dir(self, location, compare_to):
		# search in dir
		for root, _, files in os.walk(location):
			# Has files inside
			if files:   
				for file in files:
					# Is a match
					full_local_location = os.path.join(root, file)
					
					# if not os.path.isdir(full_local_location):
					# 	local_item_path_location = '/'.join(str(full_local_location).split('/')[:-1])
					# else:
					# 	local_item_path_location = os.path.join(root, file)
					
					# local_file_only_name = str(local_item_path_location).split('/')[-1:][0]
					# home_item_path_location = os.path.join(location, local_file_only_name)

					# x = home_item_path_location.split('/')[-1]
					# y = os.path.join(location, str(compare_to).split('/')[-1])
					
					# destination = str(local_item_path_location).replace(HOME_USER, '') 
					
					# if os.path.isdir(home_item_path_location):
					# 	local_combine_home_with_backup_location = os.path.join(
					# 		MAIN_INI_FILE.main_backup_folder(), file)
					# else:
					# 	local_combine_home_with_backup_location = os.path.join(
					# 		MAIN_INI_FILE.main_backup_folder(), str(home_item_path_location).replace(HOME_USER, ''))

					# # Main Backup Folder
					# main_backup_folder_location = (
					# 	MAIN_INI_FILE.main_backup_folder() 
					# 	+ 
					# 	local_item_path_location)
					# main_backup_folder_location = main_backup_folder_location.replace(HOME_USER, '')

					# print(home_item_path_location)
					# print(main_backup_folder_location)
					# print(local_item_path_location)
					# exit()

					# # NEW
					# if not os.path.exists(main_backup_folder_location):
					# 	# Backtup this NEW item
					# 		self.add_to_backup_dict(
					# 			local_item_path_location, 
					# 			main_backup_folder_location, 
					# 				'NEW')
					# else:
					# 	if main_backup_folder_location not in already_checked:
					# 		already_checked.append(main_backup_folder_location)
							
					# 		# Check diff sizes
					# 		if self.compare_sizes(
					# 			local_item_path_location,
					# 			main_backup_folder_location):

					# 			# Search inside this dir
					# 			print('Need to search inside this dir:', main_backup_folder_location)

						# if not os.path.isdir(main_backup_folder_location):
						# 		# if os.path.isdir(main_backup_folder_location):
						# 		# if any(os.scandir(home_item_path_location)):
						# 		# Backtup this NEW item
						# 		self.add_to_backup_dict(
						# 			local_item_path_location, 
						# 			main_backup_folder_location, 
						# 				'NEW')
						# else:
						# 	print('Need to search insid ethis dir:', main_backup_folder_location)


					# # UPDATED
					# if file not in no_need_to_update_list:
					# 	if file == x:
					# 		if self.compare_sizes(
					# 			y, 
					# 			compare_to):
					# 			# Add to list, so it won't check this item again,
					# 			# in other date/time folder
					# 			no_need_to_update_list.append(file)
					# 			# print('Adding', file, 'to list')

					# 			# Backtup this UPDATED item
					# 			self.add_to_backup_dict(
					# 				home_item_path_location, 
					# 				destination, 
					# 				'UPDATED')

	# def search_in_dir(self, location, compare_to):
	# 	z = str(compare_to).split('/')[-1]
	# 	z = os.path.join(location, z)
	# 	destination = str(z).replace(HOME_USER, '') 

	# 	# UPDATED
	# 	if self.compare_sizes(
	# 		z, 
	# 		compare_to):
	# 		# Backtup this UPDATED item
	# 		self.add_to_backup_dict(
	# 			z, 
	# 			destination, 
	# 			'UPDATED')

	def need_to_backup_analyse(self):
		# Check if it's not the first backup with Time Machine
		if os.path.exists(MAIN_INI_FILE.main_backup_folder()):     
			# Part of the analyses
			get_all_backups_date_time()
			self.get_select_backup_home() 
			
			# Loop thourgh Home
			self.analyse_home()
			
			# Write dict to file .txt
			self.write_to_file()
			
			# If the number of items to backup is 0
			if number_of_item_to_backup() == 0:
				# Display a notification
				# notification_message(' ')
				
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


# if __name__ == "__main__":
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
	
    # Backup wallpaper
    print("Backing up: Wallpaper")
    backup_wallpaper()
	
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
except Exception as e:
    # Save error log
    MAIN_INI_FILE.report_error(e)