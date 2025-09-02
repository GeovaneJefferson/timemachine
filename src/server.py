import getpass
import os
import pathlib
import itertools
import subprocess as sub
import configparser
import shutil
import time
import sys
import signal
import asyncio
import threading
from threading import Timer
import multiprocessing
import locale
import sqlite3
import logging
import traceback
import socket
import errno
import setproctitle
import csv
import random
import platform
import inspect
import gi
import json
import fnmatch
import hashlib
import stat
import psutil
import fcntl
import mimetypes
import cairo
import tempfile
import math
import difflib 

from datetime import datetime, timedelta

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk, GdkPixbuf, Pango, GObject

# Ignore SIGPIPE signal, so that the app doesn't crash
signal.signal(signal.SIGPIPE, signal.SIG_IGN)


class SERVER:
	def __init__(self):
		self.backup_status = "Idle"  # In-memory shared state for backup status
		self.backup_in_progress = False
		self.suspend_flag = False

		self.failed_backup: list = []
		# Format the current date and time to get the day name
		self.DAY_NAME: str = datetime.now().strftime("%A").upper().strip()  # SUNDAY, MONDAY...

		# List of file extensions that can be used for generating thumbnails or previews
		self.thumbnails_extensions_list = [
			".png",  # PNG image files
			".jpg",  # JPEG image files
			".jpeg", # JPEG image files
			".gif",  # GIF image files
			".bmp",  # Bitmap image files
			".webp", # WebP image files
			".tiff", # TIFF image files
			".svg",  # SVG image files (note: may require additional handling)
			".ico",  # Icon files
			".mp4",  # Video files (previews)
			".avi",  # AVI video files
			".mov",  # MOV video files
			".pdf",  # PDF documents (may require special handling like Poppler to render)
			".docx", # Word documents (requires a library to render previews)
			".txt",  # Text files
			".xlsx", # Excel files (requires libraries like OpenPyXL to render)
			".pptx", # PowerPoint files (requires libraries like python-pptx to render)
		]
		self.IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"}
		self.TEXT_EXTENSIONS = {
			".txt", ".py", ".md", ".csv", ".json", ".xml", ".ini", ".log",
			  ".gd", ".js", ".html", ".css", ".sh", ".c", ".cpp", ".h", ".hpp",
			    ".java", ".rs", ".go", ".toml", ".yml", ".yaml"}
		################################################################################
		# APP SETTINGS
		################################################################################
		self.DEV_NAME: str = "Geovane J."
		self.GITHUB_PAGE: str = "https://github.com/GeovaneJefferson/timemachine"
		self.GITHUB__ISSUES: str = "https://github.com/GeovaneJefferson/timemachine/issues"
		self.COPYRIGHT: str = "Copyright © 2025 Geovane J.\n\n This application comes with absolutely no warranty. See the GNU General Public License, version 3 or later for details."
		self.ID: str = "io.github.geovanejefferson.timemachine"
		self.APP_NAME: str = "Time Machine"
		# self.APP_NAME_CLOSE_LOWER: str = "timemachine"
		self.APP_NAME_CLOSE_LOWER: str = self.APP_NAME.lower().replace(" ", "")
		self.APP_VERSION: str = "v0.1 dev"
		self.SUMMARY_FILENAME: str = ".backup_summary.json"
		self.BACKUPS_LOCATION_DIR_NAME: str = "backups"  # Where backups will be saved
		self.APPLICATIONS_LOCATION_DIR_NAME: str = "applications"
		self.APP_RELEASE_NOTES: str = ""
		
		################################################################################
		# DRIVER LOCATION
		################################################################################
		self.MEDIA: str = "/media"
		self.RUN: str = "/run/media"	
		self.MAIN_BACKUP_LOCATION: str = '.main_backup'

		################################################################################
		# SYSTEM
		################################################################################
		self.GET_USERS_DE: str = "XDG_CURRENT_DESKTOP"
		self.GET_USERS_PACKAGE_MANAGER: str = "cat /etc/os-release"
		self.USER_HOME: str = os.path.expanduser("~")  # Get user's home directory
		self.LOG_FILE_PATH = os.path.expanduser(f"~/.{self.APP_NAME_CLOSE_LOWER}.log")
		
		# self.SOCKET_PATH = "/tmp/timemachine-ui.sock"
		# self.SOCKET_PATH: str = f"~/.var/app/{self.ID}/cache/tmp/timemachine-ui.sock"
		self.SOCKET_PATH = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "timemachine-ui.sock")
		# Concurrency settings for copying files
		# Default, can be adjusted based on system resources and current load
		self.DEFAULT_COPY_CONCURRENCY = 2

		################################################################################
		# HOME SYSTEM LOCATIONS
		################################################################################
		self.HOME_USER: str = os.path.expanduser("~") # Path.home() is equivalent to os.path.expanduser("~")
		self.USERNAME = getpass.getuser()
		self.GET_HOME_FOLDERS: str = os.listdir(self.HOME_USER)
		self.GET_CURRENT_LOCATION = pathlib.Path().resolve()

		################################################################################
		# FLATPAK
		################################################################################
		self.GET_FLATPAKS_APPLICATIONS_NAME_NON_CONTAINER: str = 'flatpak list --app --columns=application'
		self.GET_FLATPAKS_APPLICATIONS_NAME_CONTAINER = 'flatpak-spawn --host flatpak list --app --columns=application'
		# self.FLATPAK_SH_DST: str = f'~/.var/app/{self.ID}/config/list_flatpaks.sh'

		################################################################################
		# LOCATIONS
		################################################################################
		self.CONF = configparser.ConfigParser()
		self.CONF_LOCATION: str = os.path.join(os.path.expanduser("~"), '.var', 'app', self.ID, 'config', 'config.conf')
		self.autostart_file: str = os.path.expanduser(f"~/.config/autostart/{self.APP_NAME.lower()}_autostart.desktop")

		if not os.path.exists(self.CONF_LOCATION):
			self.create_and_move_files_to_users_home()

		if os.path.exists(self.CONF_LOCATION):
			self.CONF.read(self.CONF_LOCATION)
		else:
			print(f"Config file {self.CONF_LOCATION} not found!")

		# DRIVER Section
		self.DRIVER_NAME = self.get_database_value(
			section='DRIVER',
			option='driver_name')

		self.DRIVER_LOCATION = self.get_database_value(
			section='DRIVER',
			option='driver_location')

		self.AUTOMATICALLY_BACKUP = self.get_database_value(
			section='BACKUP',
			option='automatically_backup')

		self.BACKING_UP = self.get_database_value(
			section='BACKUP',
			option='backing_up')

		# DAEMON PID
		# self.DAEMON_PY_LOCATION: str = 'src/daemon.py'
		# self.DAEMON_PID_LOCATION: str = os.path.join(self.create_base_folder(), 'daemon.pid')
		
		# Flatpak
		self.DAEMON_PY_LOCATION: str = os.path.join('/app/share/timemachine/src', 'daemon.py')
		self.DAEMON_PID_LOCATION: str = os.path.join(os.path.expanduser("~"), '.var', 'app', self.ID, 'config', 'daemon.pid')
        
		self.CACHE = {}
		self.cache_file = os.path.join(self.backup_folder_name(), ".cache.json")
	
	##############################################################################
	# Signal, Loading and Saving Handling
	##############################################################################
	def create_and_move_files_to_users_home(self):
		# Create the directory if it doesn't exist
		config_dir = os.path.dirname(self.CONF_LOCATION)
		os.makedirs(config_dir, exist_ok=True)

		# Write default config values
		self.CONF['BACKUP'] = {
			'automatically_backup': 'false',
			'backing_up': 'false',
			'status': ''
		}

		self.CONF['DRIVER'] = {
			'driver_location': '',
			'driver_name': ''
		}

		self.CONF['EXCLUDE'] = {
			'exclude_hidden_itens': 'true',
		}

		self.CONF['EXCLUDE_FOLDER'] = {
			'folders': '',
		}

		self.CONF['RECENT'] = {
			'recent_backup_file_path': '',
			'recent_backup_timeframe': '',
		}

		# Save the config to the file
		with open(self.CONF_LOCATION, 'w') as config_file:
			self.CONF.write(config_file)

	def is_daemon_running(self):
		"""Check if the daemon is already running by checking the PID in the Flatpak sandbox."""
		if not os.path.exists(self.DAEMON_PID_LOCATION):
			logging.info(f"PID file {self.DAEMON_PID_LOCATION} does not exist. Daemon not running or PID file cleaned up.")
			return False

		try:
			with open(self.DAEMON_PID_LOCATION, 'r') as f:
				pid_str = f.read().strip()
				if not pid_str:
					logging.warning(f"PID file {self.DAEMON_PID_LOCATION} is empty. Assuming daemon not running.")
					return False
				pid = int(pid_str)
		except (ValueError, FileNotFoundError) as e:
			logging.error(f"Error reading PID from {self.DAEMON_PID_LOCATION}: {e}. Assuming daemon not running.")
			return False
		except Exception as e: # Catch any other unexpected error during file read
			logging.error(f"Unexpected error reading PID file {self.DAEMON_PID_LOCATION}: {e}. Assuming daemon not running.")
			return False

		try:
			# Attempt to create a Process object. This will raise NoSuchProcess if the PID is invalid.
			p = psutil.Process(pid) # Raises NoSuchProcess, ZombieProcess, AccessDenied

			# If we reach here, the process exists. Now verify it's our daemon.
			cmdline = p.cmdline()
			if not cmdline:
				# This case is unlikely if psutil.Process(pid) succeeded without ZombieProcess
				logging.info(f"Could not retrieve command line for PID {pid}. Cannot definitively verify daemon identity. Assuming running based on PID existence and Process() success.")
				return True

			daemon_script_name = os.path.basename(self.DAEMON_PY_LOCATION)
			is_our_daemon = False
			for arg in cmdline:
				# # Check if the daemon script path or just the script name is in the command line arguments
				# if self.DAEMON_PY_LOCATION in arg or daemon_script_name in arg:
				# 	is_our_daemon = True
				# 	break

				# Allow proctitle-based renaming like 'Time Machine - daemon'
				if any("guardian" in arg.lower() or "daemon" in arg.lower() for arg in cmdline):
					is_our_daemon = True
					break

			
			if is_our_daemon:
				logging.info(f"Daemon is running with PID: {pid} and verified command line.")
				return True
			else:
				logging.warning(f"Process with PID {pid} exists, but its command line {cmdline} does not match expected daemon script '{daemon_script_name}'. PID file may be stale or belong to another process.")
				# Consider if the PID file should be cleaned up by the daemon's startup logic if this state persists.
				return False

		except psutil.NoSuchProcess:
			logging.warning(f"Process with PID {pid} from {self.DAEMON_PID_LOCATION} does not exist (psutil.NoSuchProcess). PID file may be stale.")
			return False
		except psutil.ZombieProcess:
			logging.warning(f"Process with PID {pid} from {self.DAEMON_PID_LOCATION} is a zombie process. PID file is stale.")
			# The daemon's startup logic should ideally clean up stale PID files.
			return False
		except psutil.AccessDenied:
			logging.error(f"Access denied when trying to inspect process with PID {pid}. Cannot verify daemon identity. Assuming not running for safety.")
			# Returning False is safer as it might allow a new daemon to start and correct the PID file.
			return False
		except Exception as e:
			logging.error(f"Unexpected error checking process PID {pid} with psutil: {e}. Assuming not running.")
			return False
	
	def is_first_backup(self) -> bool:
		try:
			if not os.path.exists(self.main_backup_folder()):
				return True
			return False
			# else:
			# 	# Make sure that backup to main was not interrupted
			# 	if os.path.exists(self.INTERRUPTED_MAIN):
			# 		return True
			# 	return False
		except FileNotFoundError:
			return True
		except Exception as e:
			logging.error('Error while trying to find if is the first backup.')


	# Get users device mount point
	def get_device_for_mountpoint(self, mount_point):
		try:
			output = sub.check_output(["findmnt", "-n", "-o", "SOURCE", mount_point])
			return output.decode("utf-8").strip()  # e.g., "/dev/sdb1"
		except Exception as e:
			#print("Failed to find device for mount point:", e)
			return None
		
	# Get the filesystem type of a given path
	def get_filesystem_type(self, path):
		try:
			output = sub.check_output(['lsblk', '-no', 'FSTYPE', path])
			fs_type = output.decode('utf-8').strip()
			return fs_type or "Unknown"
		except Exception as e:
			#print("Failed to detect filesystem type:", e)
			return "Unknown"
	
	# Starred files location
	def get_starred_files_location(self) -> str: 
		return f"{self.create_base_folder()}/.starred_files.json"

	# Hidden files location
	def get_summary_filename(self) -> str: 
		return f"{self.create_base_folder()}/{self.SUMMARY_FILENAME}"

	def get_log_file_path(self) -> str:
		"""Get the path to the log file."""
		return self.LOG_FILE_PATH
	
	def get_interrupted_main_file(self) -> str:
		"""Get the path to the interrupted main file."""
		return f"{self.create_base_folder()}/.interrupted_main"

	# EXCLUDE FOLDERS
	def load_ignored_folders_from_config(self):
		"""
		Load ignored folders from the configuration file.
		"""
		try:
			# Get the folder string from the config
			folder_string = self.get_database_value(
				section='EXCLUDE_FOLDER', 
				option='folders')
			
			# Split the folder string into a list
			return [folder.strip() for folder in folder_string.split(',')] if folder_string else []
		except ValueError as e:
			#print(f"Configuration error: {e}")
			return []
		except Exception as e:
			#print(f"Error while loading ignored folders: {e}")
			return []
		
	# async def get_filtered_home_files(self) -> tuple:
	# 	"""
	# 	Asynchronously retrieves all files from the user's home directory while excluding:
	# 	- Hidden files (if enabled via configuration)
	# 	- Unfinished downloads (e.g., files ending with .crdownload, .part, or .tmp)
	# 	- Directories specified in the EXCLUDE_FOLDER config

	# 	Returns:
	# 		A tuple (files, total_count) where:
	# 		- files: List of tuples (src_path, rel_path, size)
	# 		- total_count: Total number of files found
	# 	"""
	# 	home_files = []
	# 	excluded_dirs = {'__pycache__'}
	# 	excluded_extensions = {'.crdownload', '.part', '.tmp'}

	# 	ignored_folders = self.load_ignored_folders_from_config() or []
		
	# 	try:
	# 		exclude_hidden_items = bool(self.get_database_value(
	# 			section='EXCLUDE', 
	# 			option='exclude_hidden_itens'
	# 		))
	# 	except Exception as e:
	# 		logging.error(f"Error retrieving 'exclude_hidden_itens' config: {e}")
	# 		exclude_hidden_items = False

	# 	def scan_files():
	# 		"""Perform file scanning in a separate thread (non-blocking for async)."""
	# 		for root, _, files in os.walk(self.USER_HOME):
	# 			if getattr(self, 'suspend_flag', False):
	# 				self.signal_handler(signal.SIGTERM, None)
	# 				break

	# 			if any(os.path.commonpath([root, ignored]) == ignored for ignored in ignored_folders):
	# 				continue

	# 			for file in files:
	# 				try:
	# 					src_path = os.path.join(root, file)
	# 					rel_path = os.path.relpath(src_path, self.USER_HOME)

	# 					# Check if file still exists before getting its size
	# 					if not os.path.exists(src_path):
	# 						continue

	# 					size = os.path.getsize(src_path)

	# 					is_hidden_file = (
	# 						exclude_hidden_items and (
	# 							file.startswith('.') or 
	# 							any(part.startswith('.') for part in rel_path.split(os.sep))
	# 						)
	# 					)
	# 					is_unfinished_file = any(file.endswith(ext) for ext in excluded_extensions)

	# 					if not (is_hidden_file or is_unfinished_file):
	# 						home_files.append((src_path, rel_path, size))

	# 				except FileNotFoundError:
	# 					logging.warning(f"File not found (skipped): {src_path}")
	# 					continue
	# 				except Exception as e:
	# 					logging.exception(f"Error processing file '{file}' in '{root}': {e}")
	# 					continue

	# 	# Offload the scanning to a separate thread to keep async performance
	# 	await asyncio.to_thread(scan_files)

	# 	return home_files, len(home_files)
	
	def free_space_by_deleting_oldest_backups(self, required_space):
		"""
		Delete oldest backup folders until required_space is available.
		Returns True if enough space is freed, False otherwise.
		"""
		backup_root = self.backup_folder_name()
		while True:
			statvfs = os.statvfs(backup_root)
			available_space = statvfs.f_frsize * statvfs.f_bavail
			if available_space >= required_space:
				return True  # Enough space now

			# Find all date folders
			date_folders = [
				os.path.join(backup_root, d)
				for d in os.listdir(backup_root)
				if os.path.isdir(os.path.join(backup_root, d))
			]
			if not date_folders:
				#print("No backup folders found to delete.")
				logging.error("No more backup folders to delete, but still not enough space.")
				return False

			# Sort by creation time (oldest first)
			date_folders.sort(key=lambda x: os.path.getctime(x))
			oldest = date_folders[0]
			try:
				shutil.rmtree(oldest)
				#print(f"Deleting old backup folder: {oldest}")
				logging.warning(f"Deleted old backup folder to free space: {oldest}")
			except Exception as e:
				logging.error(f"Failed to delete {oldest}: {e}")
				return False
        
	# BACKUP DESTINATION
	def backup_to_dst(self, src_path: str, dst_path: str) -> None:
		try:
			dst_path_dir: str = os.path.dirname(dst_path)
			os.makedirs(dst_path_dir, exist_ok=True)

			# Copies files
			shutil.copy2(src_path, dst_path)
		except Exception as e:
			logging.error(f"Backing up from {src_path} to {dst_path}.")

	def convert_result_to_python_type(self, value):
		try:
			if value == 'True' or value == 'true' or value == 'Yes':
				return True
			elif value == 'False' or value == 'false' or value == 'No':
				return False
			elif value == 'None' or value == ' ' or value is None:
				return None
			else:
				return value
		except TypeError:
			return None

	# def save_timeframe_to_db(self, timeframe: list, where: str, current_day:bool):
	# 	if current_day:
	# 		day = self.DAY_NAME
	# 	else:
	# 		day = self.get_next_day_name()

	# 	print(f'Generating {day} timeframe...')

	# 	# Convert list to string
	# 	timeframe_str = ','.join(map(str, timeframe))

	# 	# Assuming day_name is defined somewhere
	# 	self.set_database_value(
	# 		section=day,  # Current day name in upper case
	# 		option=where,
	# 		value=timeframe_str,
	# 		func=self.save_timeframe_to_db)

	def get_user_device_size(self, path: str, get_total: bool) -> str:
		total, used, device_free_size = shutil.disk_usage(path)

		# Convert to human-readable format (KB, MB, GB, TB)
		suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
		index = 0
		size = total if get_total else used
		while size >= 1024 and index < len(suffixes) - 1:
			size /= 1024.0
			index += 1
		return f"{size:.2f} {suffixes[index]}"

	def get_item_size(self, item_path: str, human_readable: bool = False) -> str:
		if not os.path.exists(item_path):
			return "None"
		
		try:
			size_bytes = os.path.getsize(item_path)
		except Exception as e:
			return str(e)

		if human_readable:
			# Convert to human-readable format (KB, MB, GB, TB)
			suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
			index = 0
			size = size_bytes
			while size >= 1024 and index < len(suffixes) - 1:
				size /= 1024.0
				index += 1
			return f"{size:.2f} {suffixes[index]}"
		else:
			return size_bytes

	def count_total_files(self, path: str) -> int:
		total_files: int = 0
		# Load ignored folders from config
		ignored_folders = self.load_ignored_folders_from_config()

		for root, dirs, files in os.walk(path):
			for file in files:
				src_path: str = os.path.join(root, file)
				only_dirname: str =  src_path.split('/')[3]

				# Exclude directories that match the ignored folders
				if any(os.path.commonpath([root, ignored_folder]) == ignored_folder for ignored_folder in ignored_folders):
					continue

				total_files += 1
		return total_files
	
	def has_backup_device_enough_space(
			self, 
			file_path: str=None, 
			backup_list: list=None) -> bool:
		threshold_bytes = 2 * 1024 * 1024 * 1024  # 2 GB
		total, used, device_free_size = shutil.disk_usage(self.DRIVER_LOCATION)

		if backup_list:
			try:
				# Cast sizes to int just in case
				file_size = sum(int(size) for _, _, size in backup_list)
			except Exception as e:
				return False
		else:
			file_size = self.get_item_size(file_path)
			if not isinstance(file_size, int):
				try:
					file_size = int(file_size)
				except Exception as e:
					return False
		# logging.debug(f"Checking space: device_free_size={device_free_size}, file_size={file_size}, threshold_bytes={threshold_bytes}")
		return device_free_size > (file_size + threshold_bytes)

	####################################################################
	# Packages managers
	####################################################################
	def rpm_main_folder(self):
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}/packages/rpm"

	def deb_main_folder(self):
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}/packages/deb"

	################################################################################
	# LOCATION
	# Base backup folder location
	def main_backup_folder(self) -> str:
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}/{self.BACKUPS_LOCATION_DIR_NAME}/{self.MAIN_BACKUP_LOCATION}"

	def backup_folder_name(self) -> str:
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}/{self.BACKUPS_LOCATION_DIR_NAME}"

	def create_base_folder(self) -> str:
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}"

	def has_backup_dates_to_compare(self) -> list:
		# Get all date folder names, parse them as dates, then sort from newest to oldest
		valid_dates = []
		for date in os.listdir(self.backup_folder_name()):
			if '-' in date:
				try:
					# Attempt to parse the date
					datetime.strptime(date, '%d-%m-%Y')
					valid_dates.append(date)
				except ValueError:
					# Skip invalid folder names
					continue
		return sorted(
			valid_dates,
			key=lambda d: datetime.strptime(d, '%d-%m-%Y'),
        	reverse=True  # Sort dates from newest to oldest
		)
	
	################################################################################
	# FLATPAK
	def flatpak_txt_location(self) -> str:
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}/flatpak/flatpak.txt"

	def flatpak_var_folder(self) -> str:
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}/flatpak/var"

	def flatpak_local_folder(self) -> str:
		return f"{self.DRIVER_LOCATION}/{self.APP_NAME_CLOSE_LOWER}/flatpak/share"

	def get_next_day_name(self) -> str:
		today = datetime.now()
		next_day = today + timedelta(days=1)
		next_day_name = next_day.strftime("%A").upper()
		return next_day_name

	def get_database_value(self, section: str, option: str):
		try:
			if not os.path.exists(self.CONF_LOCATION):
				return None

			with open(self.CONF_LOCATION, 'r') as f:
				fcntl.flock(f, fcntl.LOCK_SH) # Shared lock for reading
				
				config = configparser.ConfigParser()
				config.read_file(f)
				
				# Lock is released when 'with' block exits

			if not config.has_section(section) or not config.has_option(section, option):
				return None
			
			value = config.get(section, option)
			return self.convert_result_to_python_type(value)

		except configparser.Error as e:
			logging.warning(f"[CRITICAL]: Could not parse config file '{self.CONF_LOCATION}': {e}. It may be corrupt.")
			return None
		except Exception as e:
			logging.warning(f"[CRITICAL]: Error reading database value for {section}/{option}: {e}", exc_info=True)
			return None
		
	# def get_database_value(self, section: str, option: str) -> str:
	# 	try:
	# 		# Check if config file exists and is loaded
	# 		if not os.path.exists(self.CONF_LOCATION):
	# 			logging.warning(f"Config file '{self.CONF_LOCATION}' does not exist. Cannot get value for {section}/{option}.")
	# 			# Reset self.CONF to an empty state if the file is gone,
	# 			# so subsequent checks for sections/options don't use stale data.
	# 			self.CONF = configparser.ConfigParser()
	# 			return None

	# 		# Re-read the configuration file to get the latest values
	# 		# This ensures that changes made by other processes (like the UI) are picked up.
	# 		# Use a temporary parser to avoid issues if the file is malformed during read.
	# 		temp_conf = configparser.ConfigParser()
	# 		read_ok = temp_conf.read(self.CONF_LOCATION)

	# 		if read_ok:
	# 			self.CONF = temp_conf # Update the instance's config object if read was successful
	# 		else:
	# 			# Log a warning but continue with the potentially stale self.CONF
	# 			# This might be preferable to returning None if the file is temporarily unreadable
	# 			# but was previously read successfully.
	# 			logging.warning(f"[CRITICAL]: Failed to re-read config file '{self.CONF_LOCATION}' in get_database_value. Using potentially stale data.")

	# 		if not self.CONF.has_section(section):
	# 			logging.debug(f"Section '{section}' not found in configuration.")
	# 			return None  # Or return a default value if needed

	# 		if not self.CONF.has_option(section, option):
	# 			logging.debug(f"Option '{option}' not found in section '{section}'.")
	# 			return None  # Or return a default value if needed

	# 		# Retrieve and convert the value
	# 		value = self.CONF.get(section, option)
	# 		return self.convert_result_to_python_type(value=value)

	# 	except BrokenPipeError:  
	# 		# Handle broken pipe without crashing
	# 		logging.warning(f"Broken Pipe Error in {self.APP_NAME}'s database: {e}")
	# 		return None
	# 	except FileNotFoundError as e:
	# 		logging.warning(f"[CRITICAL]: {self.APP_NAME}'s database not found: {e}")
	# 		return None
	# 	except Exception as e:
	# 		logging.warning(f"[CRITICAL]: {self.APP_NAME}'s database Exception: {e}")
	# 		return None
		
	def safe_write_config(config, file_path):
		with open(file_path, 'w') as config_file:
			# Lock the file for writing
			fcntl.flock(config_file, fcntl.LOCK_EX)
			config.write(config_file)
			# Unlock the file
			fcntl.flock(config_file, fcntl.LOCK_UN)
	
	def set_database_value(self, section: str, option: str, value: str):
		try:
			os.makedirs(os.path.dirname(self.CONF_LOCATION), exist_ok=True)
			# Open with 'a+' creates the file if it doesn't exist and allows reading/writing
			with open(self.CONF_LOCATION, 'a+') as f:
				fcntl.flock(f, fcntl.LOCK_EX) # Exclusive lock

				# Read the current content of the file
				f.seek(0)
				self.CONF.read_file(f)

				if not self.CONF.has_section(section):
					self.CONF.add_section(section)
				
				self.CONF.set(section, option, str(value))
				
				# Overwrite the file with the updated config
				f.seek(0)
				f.truncate()
				self.CONF.write(f)

				# The lock is automatically released when the 'with' block exits
		except Exception as e:
			logging.error(f"Failed to set database value for {section}/{option}: {e}", exc_info=True)
			
	# def set_database_value(self, section: str, option: str, value: str):
	# 	try:
	# 		if os.path.exists(self.CONF_LOCATION):
	# 			if not self.CONF.has_section(section):
	# 				self.CONF.add_section(section)

	# 			# Only update if the value has changed
	# 			if self.CONF.get(section, option, fallback=None) != value:
	# 				self.CONF.set(section, option, value)
	# 				with open(self.CONF_LOCATION, 'w') as configfile:
	# 					self.CONF.write(configfile)
	# 		else:
	# 			raise FileNotFoundError(f"Config file '{self.CONF_LOCATION}' not found")
	# 	except Exception as e:
	# 		logging.error(f"Error in set_database_value: {e}")

	def write_backup_status(self, status: str):
		"""
		Update the in-memory backup status and persist it to disk if necessary.
		"""
		self.backup_status = status  # Update the in-memory state
		logging.info(f"Backup status updated: {status}")

		# Optionally persist to disk (e.g., every 10 seconds or on shutdown)
		# Uncomment the following line if persistence is required:
		# self.set_database_value(section='BACKUP', option='status', value=status)

	def read_backup_status(self) -> str:
		"""
		Retrieve the current backup status from memory.
		"""
		return self.backup_status

	def print_progress_bar(self, progress: int, total: int, start_time: float) -> str:
		bar_length: int = 50
		percent: float = float(progress / total)
		filled_length: int = int(round(bar_length * percent))
		bar = f'|' + '#' * filled_length + '-' * (bar_length - filled_length) + '|'

		# Calculate elapsed time
		elapsed_time = time.time() - start_time
		velocity = progress / elapsed_time if elapsed_time > 0 else 0

		if velocity > 0:
			estimated_time_left = (total - progress) / velocity
			hours, remainder = divmod(estimated_time_left, 3600)
			minutes, seconds = divmod(remainder, 60)
		# 	estimated_time_str = f'Estimated Time Left: {int(hours)}h {int(minutes)}m {int(seconds)}s'
		# else:
		# 	estimated_time_str = 'Estimated Time Left: N/A'  # If velocity is 0, show N/A

		# Show progress and estimated time
		if progress >= (total / 2):  # Only show estimated time at min. 50%
			estimated_time_str = f'Estimated Time Left: {int(hours)}h {int(minutes)}m {int(seconds)}s'
		else:
			estimated_time_str = 'Estimated Time Left: Calculating...'

		# print(f'Progress: {progress}/{total} ({percent:.0%}) - {bar} | '
		# 	f'Time Elapsed: {int(elapsed_time)}s | '
		# 	f'Velocity: {velocity:.2f} files/s | '
		# 	f'{estimated_time_str}', end='\r')
		# print()

	def copytree_with_progress(self, src: str, dst: str) -> None:
		num_files = sum([len(files) for r, d, files in os.walk(src)])
		progress: int = 0

		try:
			# Handle source as a file or directory
			if os.path.isfile(src):
				dst_without_filename = '/'.join(dst.split('/')[:-1])

				os.makedirs(dst_without_filename, exist_ok=True)
				shutil.copy2(src, dst)

				#print(f"\033[92m[✓]\033[0m {src} -> {dst}")
			elif os.path.isdir(src):
				for root, dirs, files in os.walk(src):
					for dir in dirs:
						source_folder: str = os.path.join(root, dir)
						destination_dir: str = source_folder.replace(src, dst, 1)

						os.makedirs(destination_dir, exist_ok=True)

					for file in files:
						src_file: str = os.path.join(root, file)
						dst_file: str = src_file.replace(src, dst, 1)

						os.makedirs(dst_file, exist_ok=True)
						shutil.copy2(src_file, dst_file)

						progress += 1

						#print(f"\033[92m[✓]\033[0m {src_file} -> {dst_file}")
						self.print_progress_bar(progress, num_files)
		except Exception as e:
			logging.error(f"copytree_with_progress: {e}")

	def update_recent_backup_information(self):
		current_datetime: datetime = datetime.now()  # Get the current date and time
		# Format the datetime as a string
		formatted_datetime: str = str(
			current_datetime.strftime("%d-%m-%Y %H:%M:%S"))
		
		# Update the conf file
		self.set_database_value(
			section='RECENT',
			option='recent_backup_timeframe',
			value=formatted_datetime)
		
	def setup_logging(self):
		"""Sets up logging for file changes."""
		log_file_path = self.get_log_file_path()

		MAX_LOG_SIZE: int = 20 * 1024 * 1024  # Example: 20 MB

		# Check if the directory for the log file exists; if not, create it
		log_dir = os.path.dirname(log_file_path)

		os.makedirs(log_dir, exist_ok=True)  # Create the directory for the log file
		# Ensure directory and file have correct permissions (user read/write/execute)
		os.chmod(log_dir, 0o700)  # Only owner can read/write/execute

		"""Check log file size and delete if it exceeds the limit."""
		if os.path.exists(log_file_path):
			log_size = os.path.getsize(log_file_path)
			if log_size > MAX_LOG_SIZE:
				# Delete the log file if it exceeds the max size
				os.remove(log_file_path)
		else:
			# Create a new empty log file
			with open(log_file_path, 'w'):
				pass

		# # Convert the timestamp to a human-readable format
		# timestamp = source["date"]
		# human_readable_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

		logging.basicConfig(
							filename=log_file_path,
							level=logging.INFO,
							format='%(asctime)s - %(message)s')
		console_handler = logging.StreamHandler()
		console_handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(message)s')
		console_handler.setFormatter(formatter)
		logging.getLogger().addHandler(console_handler)


if __name__ == "__main__":
	pass
