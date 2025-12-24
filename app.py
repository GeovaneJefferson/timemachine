# # app.py - Time Machine Backup Application
# import getpass
# import os
# import pathlib
# import itertools
# import subprocess as sub
# import configparser
# import shutil
# import time
# import sys
# import signal
# import asyncio
# import threading
# import multiprocessing
# import locale
# import logging
# import traceback
# import socket
# import errno
# import setproctitle
# import csv
# import random
# import platform
# import json
# import fnmatch
# import hashlib
# import stat
# import psutil
# import fcntl
# import mimetypes
# import tempfile
# import math
# import difflib
# import sqlite3
# from datetime import datetime, timedelta
# from pathlib import Path
# from threading import Thread, Timer
# from queue import Queue, Empty
#
# # Application modules
# from static.py.server import *
# from static.py.search_handler import SearchHandler
# from static.py.storage_util import get_all_storage_devices
# from static.py.daemon_control import send_control_command
# from static.py.necessaries_actions import base_folders_creation
#
# # Flask libraries
# from flask import Flask, render_template, jsonify, request
# from flask_sock import Sock
#
# # =============================================================================
# # APP INITIALIZATION
# # =============================================================================
# app = Flask(__name__)
# sock = Sock(app)
# server = SERVER()
# search_handler = SearchHandler()
#
# # =============================================================================
# # APP SETTINGS
# # =============================================================================
# app_dir = os.path.dirname(os.path.abspath(__file__))
# CONFIG_PATH = os.path.join(app_dir, 'config', 'config.conf')
# LOCATION_DB_PATH = os.path.join(app_dir, 'config', 'file_locations.db')
#
# # Calculations
# bytes_to_human = SERVER.bytes_to_human
#
# USERS_HOME: str = os.path.expanduser("~")
# USERNAME: str = getpass.getuser()
#
# # Socket
# SOCKET_PATH = server.SOCKET_PATH
# ws_clients = []  # Track WebSocket clients
#
# # --- Icon Mapping ---
# FOLDER_ICONS = {
#     'documents': {'icon': 'bi-file-earmark-text-fill', 'color': 'text-blue-500'},
#     'downloads': {'icon': 'bi-arrow-down-circle-fill', 'color': 'text-teal-500'},
#     'pictures': {'icon': 'bi-image-fill', 'color': 'text-pink-500'},
#     'photos': {'icon': 'bi-image-fill', 'color': 'text-pink-500'},
#     'videos': {'icon': 'bi-camera-video-fill', 'color': 'text-red-500'},
#     'video': {'icon': 'bi-camera-video-fill', 'color': 'text-red-500'},
#     'music': {'icon': 'bi-music-note-beamed', 'color': 'text-purple-500'},
#     'desktop': {'icon': 'bi-display-fill', 'color': 'text-emerald-500'},
#     'public': {'icon': 'bi-share-fill', 'color': 'text-yellow-500'},
#     'templates': {'icon': 'bi-code-square', 'color': 'text-orange-500'},
#     'code': {'icon': 'bi-code-slash', 'color': 'text-cyan-500'},
#     'games': {'icon': 'bi bi-joystick', 'color': 'text-cyan-500'},
#     'mega': {'icon': 'bi bi-cloudy-fill', 'color': 'text-cyan-500'},
#     'dropbox': {'icon': 'bi bi-cloudy-fill', 'color': 'text-cyan-500'},
# }
#
# # =============================================================================
# # DATABASE FOR FILE LOCATION TRACKING
# # =============================================================================
# def init_location_database():
#     """Initialize SQLite database for tracking file locations"""
#     try:
#         os.makedirs(os.path.dirname(LOCATION_DB_PATH), exist_ok=True)
#
#         conn = sqlite3.connect(LOCATION_DB_PATH)
#         cursor = conn.cursor()
#
#         # Create table for file locations
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS file_locations (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 backup_path TEXT NOT NULL,
#                 original_home_path TEXT NOT NULL,
#                 current_home_path TEXT NOT NULL,
#                 file_hash TEXT NOT NULL,
#                 found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 UNIQUE(backup_path, file_hash)
#             )
#         ''')
#
#         # Create table for file metadata
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS file_metadata (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 file_path TEXT NOT NULL UNIQUE,
#                 file_size INTEGER,
#                 file_hash TEXT,
#                 last_modified TIMESTAMP,
#                 indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#
#         # Create index for faster lookups
#         cursor.execute('CREATE INDEX IF NOT EXISTS idx_backup_path ON file_locations(backup_path)')
#         cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_hash ON file_locations(file_hash)')
#         cursor.execute('CREATE INDEX IF NOT EXISTS idx_current_path ON file_locations(current_home_path)')
#
#         conn.commit()
#         conn.close()
#         print(f"[Database] Initialized location database at {LOCATION_DB_PATH}")
#         return True
#     except Exception as e:
#         print(f"[Database] Error initializing database: {e}")
#         return False
#
# def get_file_location(backup_path, file_hash=None):
#     """Get the current home location for a backup file"""
#     try:
#         conn = sqlite3.connect(LOCATION_DB_PATH)
#         cursor = conn.cursor()
#
#         if file_hash:
#             cursor.execute('''
#                 SELECT current_home_path FROM file_locations
#                 WHERE (backup_path = ? OR file_hash = ?)
#                 ORDER BY last_checked DESC LIMIT 1
#             ''', (backup_path, file_hash))
#         else:
#             cursor.execute('''
#                 SELECT current_home_path FROM file_locations
#                 WHERE backup_path = ?
#                 ORDER BY last_checked DESC LIMIT 1
#             ''', (backup_path,))
#
#         result = cursor.fetchone()
#         conn.close()
#
#         if result:
#             current_path = result[0]
#             # Verify the file still exists at this location
#             if os.path.exists(current_path):
#                 return current_path
#             else:
#                 # File moved again, remove stale entry
#                 remove_file_location(backup_path)
#                 return None
#         return None
#     except Exception as e:
#         print(f"[Database] Error getting file location: {e}")
#         return None
#
# def save_file_location(backup_path, original_home_path, current_home_path, file_hash):
#     """Save or update the location of a file"""
#     try:
#         conn = sqlite3.connect(LOCATION_DB_PATH)
#         cursor = conn.cursor()
#
#         # Check if entry exists
#         cursor.execute('SELECT id FROM file_locations WHERE backup_path = ?', (backup_path,))
#         existing = cursor.fetchone()
#
#         if existing:
#             # Update existing entry
#             cursor.execute('''
#                 UPDATE file_locations
#                 SET current_home_path = ?, file_hash = ?, last_checked = CURRENT_TIMESTAMP
#                 WHERE backup_path = ?
#             ''', (current_home_path, file_hash, backup_path))
#         else:
#             # Insert new entry
#             cursor.execute('''
#                 INSERT INTO file_locations
#                 (backup_path, original_home_path, current_home_path, file_hash)
#                 VALUES (?, ?, ?, ?)
#             ''', (backup_path, original_home_path, current_home_path, file_hash))
#
#         conn.commit()
#         conn.close()
#         print(f"[Database] Saved location for {os.path.basename(backup_path)}: {current_home_path}")
#         return True
#     except Exception as e:
#         print(f"[Database] Error saving file location: {e}")
#         return False
#
# def remove_file_location(backup_path):
#     """Remove a file location entry"""
#     try:
#         conn = sqlite3.connect(LOCATION_DB_PATH)
#         cursor = conn.cursor()
#         cursor.execute('DELETE FROM file_locations WHERE backup_path = ?', (backup_path,))
#         conn.commit()
#         conn.close()
#         return True
#     except Exception as e:
#         print(f"[Database] Error removing file location: {e}")
#         return False
#
# def cache_file_metadata(file_path, file_size, file_hash):
#     """Cache file metadata for faster lookups"""
#     try:
#         conn = sqlite3.connect(LOCATION_DB_PATH)
#         cursor = conn.cursor()
#
#         cursor.execute('''
#             INSERT OR REPLACE INTO file_metadata
#             (file_path, file_size, file_hash, last_modified, indexed_at)
#             VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
#         ''', (file_path, file_size, file_hash, int(time.time())))
#
#         conn.commit()
#         conn.close()
#         return True
#     except Exception as e:
#         print(f"[Database] Error caching metadata: {e}")
#         return False
#
# def get_cached_hash(file_path):
#     """Get cached hash for a file"""
#     try:
#         if not os.path.exists(file_path):
#             return None
#
#         file_stat = os.stat(file_path)
#         file_size = file_stat.st_size
#         last_modified = int(file_stat.st_mtime)
#
#         conn = sqlite3.connect(LOCATION_DB_PATH)
#         cursor = conn.cursor()
#
#         cursor.execute('''
#             SELECT file_hash FROM file_metadata
#             WHERE file_path = ? AND file_size = ? AND last_modified = ?
#         ''', (file_path, file_size, last_modified))
#
#         result = cursor.fetchone()
#         conn.close()
#
#         return result[0] if result else None
#     except Exception as e:
#         print(f"[Database] Error getting cached hash: {e}")
#         return None
#
# # =============================================================================
# # FILE HASHING FUNCTIONS
# # =============================================================================
# def calculate_file_hash(file_path, use_cache=True, fast_mode=False):
#     """Calculate SHA256 hash with caching"""
#     if fast_mode:
#         return calculate_fast_hash(file_path)
#
#     # Try to get cached hash first
#     if use_cache:
#         cached_hash = get_cached_hash(file_path)
#         if cached_hash:
#             return cached_hash
#
#     # Calculate fresh hash
#     sha256_hash = hashlib.sha256()
#     try:
#         with open(file_path, "rb") as f:
#             for chunk in iter(lambda: f.read(65536), b""):
#                 sha256_hash.update(chunk)
#
#         hash_value = sha256_hash.hexdigest()
#
#         # Cache the result
#         if use_cache and os.path.exists(file_path):
#             file_stat = os.stat(file_path)
#             cache_file_metadata(file_path, file_stat.st_size, hash_value)
#
#         return hash_value
#
#     except Exception as e:
#         print(f"Error calculating hash for {file_path}: {e}")
#         return None
#
# def calculate_fast_hash(file_path, bytes_to_read=1024*1024):
#     """Fast hash calculation for searching"""
#     if not os.path.exists(file_path):
#         return None
#
#     try:
#         file_size = os.path.getsize(file_path)
#         hasher = hashlib.sha256()
#
#         # Include file size in hash
#         hasher.update(str(file_size).encode())
#
#         with open(file_path, "rb") as f:
#             # Read first chunk
#             first_chunk_size = min(bytes_to_read, file_size)
#             first_chunk = f.read(first_chunk_size)
#             hasher.update(first_chunk)
#
#             # Read last 64KB if file is large enough
#             if file_size > bytes_to_read * 2:
#                 last_chunk_size = min(65536, file_size - first_chunk_size)
#                 if last_chunk_size > 0:
#                     f.seek(-last_chunk_size, 2)
#                     last_chunk = f.read()
#                     hasher.update(last_chunk)
#
#         return hasher.hexdigest()
#
#     except Exception as e:
#         print(f"Fast hash error: {e}")
#         return None
#
# # =============================================================================
# # SEARCH FUNCTIONS
# # =============================================================================
# def search_directory_by_hash(directory, target_hash, max_depth=3, current_depth=0):
#     """Search directory for file matching target hash"""
#     if current_depth > max_depth:
#         return None
#
#     try:
#         for item in os.listdir(directory):
#             if item.startswith('.'):
#                 continue
#
#             item_path = os.path.join(directory, item)
#
#             if os.path.isfile(item_path):
#                 try:
#                     # Skip very large files
#                     if os.path.getsize(item_path) > 500 * 1024 * 1024:
#                         continue
#
#                     # Get hash (cached or calculated)
#                     current_hash = get_cached_hash(item_path)
#                     if not current_hash:
#                         current_hash = calculate_fast_hash(item_path)
#
#                     if current_hash and current_hash == target_hash:
#                         return {
#                             'path': item_path,
#                             'hash': current_hash,
#                             'depth': current_depth
#                         }
#
#                 except (PermissionError, OSError):
#                     continue
#
#             elif os.path.isdir(item_path) and current_depth < max_depth:
#                 result = search_directory_by_hash(
#                     item_path, target_hash, max_depth, current_depth + 1
#                 )
#                 if result:
#                     return result
#
#     except PermissionError:
#         pass
#
#     return None
#
# def find_file_by_hash(target_hash, backup_path):
#     """Find file by hash in common locations"""
#     if not target_hash:
#         return None
#
#     home_dir = os.path.expanduser("~")
#     expected_home_path = convert_backup_to_home_path(backup_path)
#     expected_dir = os.path.dirname(expected_home_path)
#
#     # Search locations in priority order
#     search_locations = []
#
#     # 1. Check database first
#     current_location = get_file_location(backup_path, target_hash)
#     if current_location and os.path.exists(current_location):
#         # Verify hash matches
#         current_hash = calculate_fast_hash(current_location)
#         if current_hash == target_hash:
#             return {
#                 'path': current_location,
#                 'hash': target_hash,
#                 'found_in': 'database',
#                 'source': 'cached_location'
#             }
#
#     # 2. Expected directory
#     if os.path.exists(expected_dir):
#         search_locations.append({
#             'path': expected_dir,
#             'depth': 3,
#             'priority': 1
#         })
#
#     # 3. Common directories
#     common_dirs = ['Desktop', 'Downloads', 'Documents', 'Pictures', 'Music', 'Videos']
#     for dir_name in common_dirs:
#         dir_path = os.path.join(home_dir, dir_name)
#         if os.path.exists(dir_path):
#             search_locations.append({
#                 'path': dir_path,
#                 'depth': 2,
#                 'priority': 2
#             })
#
#     # 4. Home directory
#     search_locations.append({
#         'path': home_dir,
#         'depth': 1,
#         'priority': 3
#     })
#
#     # Sort by priority
#     search_locations.sort(key=lambda x: x['priority'])
#
#     # Search each location
#     for location in search_locations:
#         result = search_directory_by_hash(
#             location['path'],
#             target_hash,
#             max_depth=location['depth']
#         )
#
#         if result:
#             return {
#                 'path': result['path'],
#                 'hash': result['hash'],
#                 'found_in': os.path.basename(location['path']),
#                 'source': 'hash_search',
#                 'depth': result['depth']
#             }
#
#     return None
#
#
# # =============================================================================
# # BACKUP SERVICE CLASS
# # =============================================================================
# class BackupService:
#     """Placeholder class for the application's core backup/daemon service."""
#     def __init__(self):
#         logging.info("BackupService initialized.")
#
#     def start_server(self):
#         """UNIX Socket listener to receive messages and broadcast to WebSockets."""
#         if os.path.exists(SOCKET_PATH):
#             os.remove(SOCKET_PATH)
#
#         try:
#             with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
#                 listener.bind(SOCKET_PATH)
#                 listener.listen(1)
#                 print(f"[IPC] Listening for daemon on UNIX socket: {SOCKET_PATH}")
#
#                 while True:
#                     conn, _ = listener.accept()
#                     with conn:
#                         data = b''
#                         while True:
#                             chunk = conn.recv(4096)
#                             if not chunk:
#                                 break
#                             data += chunk
#
#                         if data:
#                             decoded_data = data.decode('utf-8')
#
#                             # Split the stream by '\n' to handle multiple JSON messages
#                             for line in decoded_data.strip().split('\n'):
#                                 if not line:
#                                     continue
#                                 try:
#                                     msg = json.loads(line)
#                                     # Broadcast to WebSocket clients
#                                     message_json = json.dumps(msg)
#                                     for client_ws in list(ws_clients):
#                                         try:
#                                             client_ws.send(message_json)
#                                         except Exception:
#                                             try:
#                                                 ws_clients.remove(client_ws)
#                                             except ValueError:
#                                                 pass
#                                 except json.JSONDecodeError as e:
#                                     print(f"[IPC] Invalid JSON line: {e}. Data: {line[:50]}...")
#
#         except Exception as e:
#             print(f"[IPC] Fatal UNIX Socket listener error: {e}")
#
#     def clear_cache(self):
#         """Clear the file cache (useful when backup files change)"""
#         self._files_cache = None
#         self._cache_time = 0
#         self.files_loaded = False
#
#     def update_backup_location(self):
#         """Clear cache to force rescan of new location"""
#         self.clear_cache()
#
# # =============================================================================
# # HELPER FUNCTIONS
# # =============================================================================
# def convert_backup_to_home_path(backup_path):
#     """Convert backup path to home directory path"""
#     if not backup_path:
#         return ''
#
#     home_dir = os.path.expanduser("~")
#
#     # Check for different backup path patterns
#     patterns = [server.MAIN_BACKUP_LOCATION, 'timemachine/backups', 'backups']
#
#     for pattern in patterns:
#         if pattern in backup_path:
#             parts = backup_path.split(pattern)
#             if len(parts) > 1:
#                 relative_path = parts[1].lstrip('/').lstrip('\\')
#                 return os.path.join(home_dir, relative_path)
#
#     # If no pattern found, extract filename
#     filename = os.path.basename(backup_path)
#     return os.path.join(home_dir, filename)
#
# def get_system_devices():
#     """Gathers local storage device information for the Devices tab."""
#     devices = []
#     partitions = psutil.disk_partitions(all=False)
#
#     for i, partition in enumerate(partitions):
#         try:
#             usage = psutil.disk_usage(partition.mountpoint)
#             used_gb = usage.used / (1024 ** 3)
#             total_gb = usage.total / (1024 ** 3)
#             percent_used = usage.percent
#
#             status = 'Healthy'
#             color = 'text-green-500'
#             if percent_used > 90:
#                 status = 'Critical'
#                 color = 'text-red-500'
#             elif percent_used > 75:
#                 status = 'Warning'
#                 color = 'text-yellow-500'
#
#             devices.append({
#                 'id': i + 1,
#                 'name': f"{os.path.basename(partition.mountpoint) or 'Root'}",
#                 'mountpoint': partition.mountpoint,
#                 'status': status,
#                 'color': color,
#                 'progress': percent_used,
#                 'used_space': f"{used_gb:.2f} GB",
#                 'total_space': f"{total_gb:.2f} GB",
#                 'last_backup': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 'backup_count': random.randint(10, 50),
#                 'icon': 'bi-hdd-fill' if partition.mountpoint == '/' else ('bi-usb-drive-fill' if partition.opts.startswith('rw') else 'bi-disc-fill')
#             })
#         except Exception as e:
#             print(f"Error reading partition {partition.mountpoint}: {e}")
#             continue
#
#     return devices
#
# # =============================================================================
# # ROUTES
# # =============================================================================
#
# # =============================================================================
# # USER ROUTES
# # =============================================================================
# @app.route('/api/username')
# def get_username():
#     username = os.path.basename(os.path.expanduser("~"))
#     return jsonify({'username': username})
#
# # =============================================================================
# # FIRST ACTIONS
# # =============================================================================
# @app.route('/api/base-folders-creation')
# def create_necessaries_folders():
#     try:
#         if base_folders_creation():
#             return jsonify({'success': True, 'message': 'Created necessaries folders!'})
#         return jsonify({'success': False, 'message': 'Folder creation failed due to internal check.'})
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': 'Error creating necessary folders: Operation failed.',
#             'error': str(e)
#         })
#
# # =============================================================================
# # CONFIG FILE ROUTES
# # =============================================================================
# @app.route('/api/config')
# def get_config_data():
#     """Reads the entire config.conf file"""
#     config = configparser.ConfigParser()
#     try:
#         config.read(CONFIG_PATH)
#         config_dict = {}
#         for section in config.sections():
#             config_dict[section] = dict(config.items(section))
#
#         if config.defaults():
#             config_dict['DEFAULT'] = config.defaults()
#
#         return jsonify(config_dict)
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': f'Failed to read configuration file: {str(e)}'
#         }), 500
#
# @app.route('/api/backup-folders', methods=['GET'])
# def get_backup_folders():
#     """List ALL home folders and check if they are in config."""
#     try:
#         home_path = os.path.expanduser('~')
#
#         # Get saved folders from config
#         config = configparser.ConfigParser()
#         config.read(CONFIG_PATH)
#         saved_folders = []
#         if config.has_section('BACKUP_FOLDERS') and config.has_option('BACKUP_FOLDERS', 'folders'):
#             raw = config.get('BACKUP_FOLDERS', 'folders')
#             saved_folders = [os.path.normpath(f.strip()) for f in raw.split(',') if f.strip()]
#
#         folders_data = []
#
#         def get_icon_for_folder(name: str):
#             return FOLDER_ICONS.get(
#                 name.lower(),
#                 {'icon': 'bi-folder-fill', 'color': 'text-brand-500'}
#             )
#
#         # List all folders in Home Directory
#         if os.path.exists(home_path):
#             for item in os.listdir(home_path):
#                 full_path = os.path.join(home_path, item)
#                 if os.path.isdir(full_path) and not item.startswith('.'):
#                     is_selected = os.path.normpath(full_path) in saved_folders
#                     icon_data = get_icon_for_folder(item)
#
#                     folders_data.append({
#                         'name': item,
#                         'path': full_path,
#                         'selected': is_selected,
#                         'icon': icon_data['icon'],
#                         'color': icon_data['color']
#                     })
#
#         folders_data.sort(key=lambda x: x['name'].lower())
#         return jsonify({'success': True, 'folders': folders_data})
#
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# @app.route('/api/backup-folders', methods=['POST'])
# def save_backup_folders():
#     """Save the user's selection to the config file."""
#     try:
#         data = request.get_json()
#         selected_folders = data.get('folders', [])
#
#         config = configparser.ConfigParser()
#         config.read(CONFIG_PATH)
#
#         config.set('BACKUP_FOLDERS', 'folders', ','.join(selected_folders))
#
#         with open(CONFIG_PATH, 'w') as f:
#             config.write(f)
#
#         return jsonify({'success': True})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# # =============================================================================
# # USAGE AND CONNECTION ROUTES
# # =============================================================================
# @app.route('/api/backup/connection')
# def backup_connection():
#     DRIVER_PATH = server.get_database_value('DEVICE_INFO', 'path')
#
#     if DRIVER_PATH:
#         if os.path.exists(DRIVER_PATH):
#             return jsonify({
#                 'success': True,
#                 'connected': True,
#                 'location': DRIVER_PATH
#             })
#         else:
#             return jsonify({
#                 'success': True,
#                 'connected': False,
#                 'location': DRIVER_PATH
#             })
#     else:
#         return jsonify({
#             'success': False,
#             'connected': False,
#             'location': 'Not configured'
#         })
#
# @app.route('/api/backup/usage')
# def backup_usage():
#     try:
#         config = configparser.ConfigParser()
#         config.read(CONFIG_PATH)
#
#         necessary_config_sections = config.has_section('DEVICE_INFO')
#         necessary_config_options = config.has_option('DEVICE_INFO', 'path')
#         DRIVER_PATH = server.get_database_value('DEVICE_INFO', 'path')
#
#         if not necessary_config_sections or not necessary_config_options:
#             return jsonify({
#                 'success': False,
#                 'error': 'Please select a backup device first! Go to Devices → Select your storage → Confirm Selection',
#                 'user_action_required': True,
#                 'location': 'Not configured'
#             })
#
#         if not DRIVER_PATH or not os.path.exists(DRIVER_PATH):
#             return jsonify({
#                 'success': False,
#                 'error': 'Connection to backup device is not available. Please ensure the backup device is connected and mounted.',
#                 'user_action_required': True,
#                 'location': DRIVER_PATH or 'Not configured'
#             })
#
#         # Get disk usage
#         total, used, free = shutil.disk_usage(DRIVER_PATH)
#         percent_used = (used / total) * 100 if total > 0 else 0
#
#         # Get home disk usage
#         home_total, home_used, home_free = shutil.disk_usage(os.path.expanduser('~'))
#         home_percent_used = (home_used / home_total) * 100 if home_total > 0 else 0
#
#         def get_backup_summary() -> dict:
#             try:
#                 summary_file = server.get_summary_file_path()
#                 if not os.path.exists(summary_file):
#                     return {}
#
#                 with open(summary_file, 'r') as f:
#                     return json.load(f)
#             except json.JSONDecodeError as e:
#                 logging.error(f"Error decoding JSON from backup summary: {e}")
#                 return {}
#
#         return jsonify({
#             'success': True,
#             'location': DRIVER_PATH,
#             'percent_used': round(percent_used, 1),
#             'human_used': bytes_to_human(used),
#             'human_total': bytes_to_human(total),
#             'human_free': bytes_to_human(free),
#             'home_human_used': bytes_to_human(home_used),
#             'home_human_total': bytes_to_human(home_total),
#             'home_human_free': bytes_to_human(home_free),
#             'home_percent_used': round(home_percent_used, 1),
#             'users_home_path': os.path.expanduser('~'),
#             'summary': get_backup_summary() if get_backup_summary() else "No backup summary available",
#             'device_name': server.DRIVER_NAME,
#             'filesystem': server.DRIVER_FILESYTEM,
#             'model': server.DRIVER_MODEL,
#             'serial_number': "DRIVER_SERIAL"
#         })
#     except Exception as e:
#         app.logger.error(f"Error in backup_usage: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e),
#             'location': 'Error'
#         }), 500
#
# # =============================================================================
# # DEVICES ROUTES
# # =============================================================================
# @app.route('/api/storage/devices', methods=['GET'])
# def scan_devices():
#     """Scan and return all available storage devices"""
#     try:
#         devices = get_all_storage_devices()
#         app.logger.info(f"Found {len(devices)} storage devices")
#         return jsonify({
#             'success': True,
#             'devices': devices,
#             'count': len(devices)
#         })
#     except Exception as e:
#         app.logger.error(f"Error scanning devices: {str(e)}", exc_info=True)
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#
# @app.route('/api/backup/select-device', methods=['POST'])
# def select_device():
#     data = request.get_json()
#     device_info = data.get('device_info', {})
#     device_path = device_info.get('mount_point')
#
#     if not device_path:
#         return jsonify({'success': False, 'error': 'No device path provided'}), 400
#
#     try:
#         if not os.path.exists(device_path):
#             return jsonify({
#                 'success': False,
#                 'error': f'Path does not exist: {device_path}'
#             }), 400
#
#         config = configparser.ConfigParser()
#         config.read(CONFIG_PATH)
#
#         if not config.has_section('DEVICE_INFO'):
#             config.add_section('DEVICE_INFO')
#
#         config.set('DEVICE_INFO', 'path', str(device_path))
#         config.set('DEVICE_INFO', 'name', str(device_info.get('name', 'N/A')))
#         config.set('DEVICE_INFO', 'device', str(device_info.get('device', 'N/A')))
#         config.set('DEVICE_INFO', 'serial_number', str(device_info.get('serial_number', 'N/A')))
#         config.set('DEVICE_INFO', 'model', str(device_info.get('model', 'N/A')))
#
#         is_ssd = device_info.get('is_ssd', False)
#         is_ssd_value = 'ssd' if is_ssd else 'hdd'
#         config.set('DEVICE_INFO', 'disk_type', is_ssd_value)
#         config.set('DEVICE_INFO', 'filesystem', str(device_info.get('filesystem', 'N/A')))
#
#         total_size = device_info.get('total', 0)
#         config.set('DEVICE_INFO', 'total_size_bytes', str(int(total_size)))
#
#         with open(CONFIG_PATH, 'w') as configfile:
#             config.write(configfile)
#
#         # Update global variables
#         global DRIVER_NAME, DRIVER_PATH, DRIVER_FILESYTEM, DRIVER_MODEL
#         global APP_MAIN_BACKUP_DIR, APP_BACKUP_DIR
#
#         DRIVER_NAME = device_info.get('name', 'N/A')
#         DRIVER_PATH = device_path
#         DRIVER_FILESYTEM = device_info.get('filesystem', 'N/A')
#         DRIVER_MODEL = device_info.get('model', 'N/A')
#
#         APP_MAIN_BACKUP_DIR = os.path.join(DRIVER_PATH, 'timemachine', 'backups', server.MAIN_BACKUP_LOCATION)
#         APP_BACKUP_DIR = os.path.join(DRIVER_PATH, 'timemachine', 'backups')
#
#         search_handler.update_backup_location()
#
#         import gc
#         gc.collect()
#
#         return jsonify({
#             'success': True,
#             'message': f'Backup device {device_path} configured successfully.',
#             'path': device_path
#         })
#
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': f'Failed to save configuration: {str(e)}'
#         }), 500
#
# # =============================================================================
# # WEBSOCKET FOR LIVE TRANSFERS FEED
# # =============================================================================
# @sock.route('/ws/transfers-feed')
# def transfers_feed_websocket(ws):
#     """WebSocket endpoint for live transfers feed updates from the daemon."""
#     ws_clients.append(ws)
#
#     try:
#         while True:
#             try:
#                 data = ws.receive(timeout=None)
#                 if data is None:
#                     break
#             except Exception as e:
#                 if "timeout" not in str(e).lower():
#                     print(f"[WebSocket] Receive error: {e}")
#                 break
#     except Exception as e:
#         print(f"[WebSocket] Connection error: {e}")
#     finally:
#         try:
#             ws_clients.remove(ws)
#         except ValueError:
#             pass
#
# # =============================================================================
# # SEARCH ROUTES
# # =============================================================================
# @app.route('/api/search/status', methods=['GET'])
# def search_status():
#     """Check the status of file caching and scanning."""
#     try:
#         return jsonify({
#             'success': True,
#             'files_loaded': search_handler.files_loaded,
#             'file_count': len(search_handler.files),
#             'cache_valid': search_handler._files_cache is not None
#         })
#     except Exception as e:
#         app.logger.error(f"Error getting search status: {e}", exc_info=True)
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#
# @app.route('/api/search/init', methods=['POST'])
# def init_search():
#     """Trigger initial file scanning in background if not already done."""
#     try:
#         if not search_handler.files_loaded:
#             search_handler.scan_files_folder_threaded()
#             return jsonify({
#                 'success': True,
#                 'message': 'File scanning started in background',
#                 'scanning': True
#             })
#         else:
#             return jsonify({
#                 'success': True,
#                 'message': 'Files already loaded',
#                 'scanning': False,
#                 'file_count': len(search_handler.files)
#             })
#     except Exception as e:
#         app.logger.error(f"Error initializing search: {e}", exc_info=True)
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#
# @app.route('/api/search', methods=['GET'])
# def search_files():
#     """Search endpoint with robust error handling and caching support."""
#     query = request.args.get('query', '').strip().lower()
#     print(f"Search query received: '{query}'")
#
#     if not query:
#         return jsonify({'files': [], 'total': 0})
#
#     try:
#         search_results = search_handler.perform_search(query)
#
#         return jsonify({
#             'files': search_results,
#             'total': len(search_handler.files)
#         })
#     except AttributeError as e:
#         app.logger.error(f"Search handler attribute error: {e}", exc_info=True)
#         return jsonify({
#             'success': False,
#             'error': 'Search handler not properly initialized. Please refresh the page.',
#             'files': []
#         }), 500
#     except Exception as e:
#         app.logger.error(f"Error during file search: {e}", exc_info=True)
#         return jsonify({
#             'success': False,
#             'error': 'An error occurred during search.',
#             'files': []
#         }), 500
#
# @app.route('/api/search/folder', methods=['GET'])
# def get_folder_contents():
#     """Get folder contents (files and directories) from the backup directory."""
#     path = request.args.get('path', '').strip()
#     main_backup_dirname = server.MAIN_BACKUP_LOCATION_LOCATION
#
#     try:
#         backup_dir = server.app_main_backup_dir()
#
#         if not os.path.isdir(backup_dir):
#             return jsonify({
#                 'success': False,
#                 'error': f'Backup directory not found: {backup_dir}',
#                 'items': []
#             }), 404
#
#         if path and path != '' and path != main_backup_dirname:
#             full_path = os.path.join(backup_dir, path.lstrip('/'))
#         else:
#             full_path = backup_dir
#
#         real_path = os.path.realpath(full_path)
#         real_backup = os.path.realpath(backup_dir)
#         if not real_path.startswith(real_backup):
#             return jsonify({
#                 'success': False,
#                 'error': 'Invalid path',
#                 'items': []
#             }), 403
#
#         if not os.path.isdir(real_path):
#             return jsonify({
#                 'success': False,
#                 'error': f'Directory not found: {path}',
#                 'items': []
#             }), 404
#
#         items = []
#         try:
#             for entry in os.scandir(real_path):
#                 item = {
#                     'name': entry.name,
#                     'type': 'folder' if entry.is_dir(follow_symlinks=False) else 'file',
#                     'path': entry.path
#                 }
#
#                 if item['type'] == 'file':
#                     item['icon'] = 'bi-file-earmark-fill'
#                     item['color'] = 'text-gray-500'
#
#                 items.append(item)
#         except PermissionError:
#             return jsonify({
#                 'success': False,
#                 'error': 'Permission denied accessing directory',
#                 'items': []
#             }), 403
#
#         return jsonify({
#             'success': True,
#             'items': items,
#             'path': path or '/'
#         })
#
#     except Exception as e:
#         app.logger.error(f"Error getting folder contents: {e}", exc_info=True)
#         return jsonify({
#             'success': False,
#             'error': str(e),
#             'items': []
#         }), 500
#
# # =============================================================================
# # FILE OPERATIONS ROUTES
# # =============================================================================
# @app.route('/api/open-file', methods=['POST'])
# def open_file():
#     try:
#         data = request.get_json()
#         file_path = data.get('file_path')
#
#         if not file_path:
#             return jsonify({'success': False, 'error': 'No file_path provided'}), 400
#
#         if os.name == 'nt':
#             os.startfile(file_path)
#         elif os.uname().sysname == 'Darwin':
#             sub.run(['open', file_path])
#         else:
#             sub.run(['xdg-open', file_path])
#
#         return jsonify({'success': True, 'message': f'Attempted to open file: {file_path}'}), 200
#
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# @app.route('/api/open-location', methods=['POST'])
# def open_location():
#     try:
#         data = request.get_json()
#         file_path = data.get('file_path')
#         file_path = os.path.dirname(file_path)
#
#         if not file_path:
#             return jsonify({'success': False, 'error': 'No file_path provided'}), 400
#
#         if os.name == 'nt':
#             os.startfile(file_path)
#         elif os.uname().sysname == 'Darwin':
#             sub.run(['open', file_path])
#         else:
#             sub.run(['xdg-open', file_path])
#
#         return jsonify({'success': True, 'message': f'Attempted to open folder: {file_path}'}), 200
#
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# @app.route('/api/restore-file', methods=['POST'])
# def restore_file():
#     """Restore file to its original or current location"""
#     try:
#         data = request.get_json()
#         file_path = data.get('file_path')
#         restore_to = data.get('restore_to')  # 'original' or 'current' or specific path
#
#         if not file_path:
#             return jsonify({'success': False, 'error': 'No file_path provided'}), 400
#
#         # Determine destination path
#         if restore_to == 'original':
#             destination_path = convert_backup_to_home_path(file_path)
#         elif restore_to == 'current':
#             # Get current location from database
#             file_hash = calculate_fast_hash(file_path)
#             current_location = get_file_location(file_path, file_hash)
#             if not current_location:
#                 destination_path = convert_backup_to_home_path(file_path)
#             else:
#                 destination_path = current_location
#         elif restore_to and os.path.isdir(restore_to):
#             # Custom location
#             filename = os.path.basename(file_path)
#             destination_path = os.path.join(restore_to, filename)
#         else:
#             destination_path = convert_backup_to_home_path(file_path)
#
#         def preserve_file_timestamp(src_path: str, dst_path: str) -> bool:
#             """Copy file while preserving original timestamps."""
#             try:
#                 # Get original metadata
#                 src_stat = os.stat(src_path)
#                 original_atime = src_stat.st_atime
#                 original_mtime = src_stat.st_mtime
#
#                 # Copy file with metadata
#                 shutil.copy2(src_path, dst_path)
#
#                 # Ensure timestamps are preserved (copy2 should do this, but let's be sure)
#                 os.utime(dst_path, (original_atime, original_mtime))
#
#                 # Verify
#                 dst_stat = os.stat(dst_path)
#                 if abs(dst_stat.st_mtime - original_mtime) > 1:
#                     print(f"Warning: Timestamp mismatch for {dst_path}")
#                     return False
#
#                 return True
#
#             except Exception as e:
#                 print(f"Error preserving timestamp: {e}")
#                 return False
#
#         def do_restore_async(src, dst):
#             try:
#                 print(f"🚀 Starting restore from: {src}")
#                 print(f"🎯 Restoring to: {dst}")
#
#                 os.makedirs(os.path.dirname(dst), exist_ok=True)
#
#                 if not os.path.exists(src):
#                     print(f"❌ Error: Source file does not exist: {src}")
#                     return
#
#                 # 1. Get original metadata
#                 src_stat = os.stat(src)
#                 original_mtime = src_stat.st_mtime
#                 original_atime = src_stat.st_atime
#
#                 print(f"⏰ Original timestamp: {datetime.fromtimestamp(original_mtime)}")
#
#                 # 2. Copy the file
#                 shutil.copy2(src, dst)
#
#                 # 3. WAIT for file write to complete
#                 print("⏳ Waiting for file write to complete...")
#                 time.sleep(1)  # Wait 1 second
#
#                 # 4. Preserve ORIGINAL timestamp
#                 os.utime(dst, (original_atime, original_mtime))
#
#                 # 5. Verify
#                 dst_stat = os.stat(dst)
#                 print(f"✅ Restored with timestamp: {datetime.fromtimestamp(dst_stat.st_mtime)}")
#
#                 if abs(dst_stat.st_mtime - original_mtime) > 1:  # Allow 1 second tolerance
#                     print(f"⚠️  Warning: Timestamp may not have been preserved")
#                     print(f"   Expected: {original_mtime}, Got: {dst_stat.st_mtime}")
#
#                 print(f"✅ Successfully restored {src} to {dst}")
#                 print(f"⏰ Preserved original timestamp: {datetime.fromtimestamp(dst_stat.st_mtime)}")
#
#                 # Update location in database
#                 file_hash = calculate_fast_hash(src)
#                 original_home_path = convert_backup_to_home_path(src)
#                 save_file_location(src, original_home_path, dst, file_hash)
#
#                 print(f"🎉 Restore completed successfully!")
#
#                 # ========== NOTIFY DAEMON TO PREVENT RE-BACKUP ==========
#                 try:
#                     daemon_socket_path = server.SOCKET_PATH + ".ctrl"
#                     if os.path.exists(daemon_socket_path):
#                         restore_notification = {
#                             "command": "file_restored",
#                             "path": dst,
#                             "original_mtime": original_mtime,
#                             "hash": file_hash,
#                             "timestamp": time.time()
#                         }
#
#                         with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
#                             sock.settimeout(2)
#                             sock.connect(daemon_socket_path)
#                             sock.sendall(json.dumps(restore_notification).encode('utf-8'))
#
#                         print(f"📢 Notified daemon about restore: {dst}")
#                     else:
#                         print(f"⚠️  Daemon control socket not found at {daemon_socket_path}")
#                 except Exception as e:
#                     print(f"⚠️  Could not notify daemon: {e}")
#
#             except Exception as e:
#                 print(f"❌ Error restoring file (async thread): {e}")
#                 import traceback
#                 traceback.print_exc()
#
#         # Start the restoration in a background thread
#         threading.Thread(target=do_restore_async, args=(file_path, destination_path), daemon=True).start()
#
#         return jsonify({
#             'success': True,
#             'message': 'File restoration process started in background.',
#             'restored_to': destination_path
#         }), 202
#
#     except Exception as e:
#         print(f"Error in restore_file endpoint: {e}")
#         traceback.print_exc()
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# @app.route('/api/file-versions', methods=['GET'])
# def get_file_versions():
#     file_path_requested = request.args.get('file_path')
#     if not file_path_requested:
#         return jsonify({'success': False, 'error': 'Missing file_path'}), 400
#
#     versions: list = []
#     try:
#         app.logger.debug(f"File versions lookup requested for: {file_path_requested}")
#
#         home_abs_path = os.path.abspath(USERS_HOME)
#         main_backup_abs_path = os.path.abspath(server.app_main_backup_dir())
#         incremental_base_path = os.path.abspath(server.app_backup_dir())
#
#         rel_path = None
#         file_abs_path = os.path.abspath(file_path_requested)
#
#         if file_abs_path.startswith(main_backup_abs_path):
#             rel_path = os.path.relpath(file_abs_path, main_backup_abs_path)
#         elif file_abs_path.startswith(incremental_base_path):
#             temp_rel = os.path.relpath(file_abs_path, incremental_base_path)
#             parts = temp_rel.split(os.sep)
#             if len(parts) >= 3:
#                 rel_path = os.path.join(*parts[2:])
#             else:
#                 rel_path = parts[-1] if parts else ""
#         elif file_abs_path.startswith(home_abs_path):
#             rel_path = os.path.relpath(file_abs_path, home_abs_path)
#         else:
#             rel_path = file_path_requested
#
#         if not rel_path:
#             return jsonify({'success': False, 'error': 'Could not determine file path'}), 400
#
#         # 1) Main backup version
#         main_backup_file = os.path.join(main_backup_abs_path, rel_path)
#         if os.path.exists(main_backup_file):
#             stat = os.stat(main_backup_file)
#             versions.append({
#                 'key': 'main',
#                 'time': 'Main Backup',
#                 'path': main_backup_file,
#                 'size': stat.st_size,
#                 'mtime': stat.st_mtime
#             })
#
#         # 2) Incremental backups
#         if os.path.exists(incremental_base_path):
#             for date_folder in sorted(os.listdir(incremental_base_path), reverse=True):
#                 date_path = os.path.join(incremental_base_path, date_folder)
#                 if not os.path.isdir(date_path):
#                     continue
#                 for time_folder in sorted(os.listdir(date_path), reverse=True):
#                     time_path = os.path.join(date_path, time_folder)
#                     if not os.path.isdir(time_path):
#                         continue
#                     backup_file = os.path.join(time_path, rel_path)
#                     if os.path.exists(backup_file):
#                         stat = os.stat(backup_file)
#                         versions.append({
#                             'key': f"{date_folder}_{time_folder}",
#                             'time': f"{date_folder} {time_folder.replace('_', ':')}",
#                             'path': backup_file,
#                             'size': stat.st_size,
#                             'mtime': stat.st_mtime
#                         })
#
#         versions.sort(key=lambda x: x.get('mtime', 0), reverse=True)
#         for v in versions:
#             v.pop('mtime', None)
#
#         return jsonify({'success': True, 'versions': versions}), 200
#
#     except Exception as e:
#         app.logger.error(f"Error in get_file_versions: {e}", exc_info=True)
#         traceback.print_exc()
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# @app.route('/api/file-info', methods=['POST'])
# def file_info():
#     """Get information about a file, including its current location"""
#     data = request.json
#     backup_path = data.get('file_path', '')
#
#     # --- 1. Get essential path configurations ---
#     # These names must match what your server/daemon uses
#     main_backups_dirname: str = server.BACKUPS_LOCATION_DIR_NAME  # e.g., 'timemachine/backups'
#     original_backups_dirname: str = server.MAIN_BACKUP_LOCATION_LOCATION  # e.g., server.MAIN_BACKUP_LOCATION
#
#     # --- 2. Determine if viewing a historical snapshot ---
#     # is_snapshot_view is True if it contains the backups folder structure but is NOT the main_backup
#     is_snapshot_view: bool = bool((main_backups_dirname in backup_path) and not (original_backups_dirname in backup_path))
#
#     # --- 3. Initial Path Derivation ---
#     # Get expected home path (this is required for restore and display, even for snapshots)
#     home_path = convert_backup_to_home_path(backup_path)
#
#     # --- 4. Database and Live System Checks ---
#     # File hash is only needed if the file physically exists for comparison
#     file_hash = calculate_fast_hash(backup_path) if os.path.exists(backup_path) else None
#     current_location = get_file_location(backup_path, file_hash) if file_hash else None
#
#     exists_at_home = os.path.exists(home_path) if home_path else False
#     exists_at_current = os.path.exists(current_location) if current_location else False
#
#     # Determine the actual path where the file is currently found
#     actual_path = None
#     location_source = 'unknown'
#
#     if exists_at_current:
#         actual_path = current_location
#         location_source = 'database'
#     elif exists_at_home:
#         actual_path = home_path
#         location_source = 'expected'
#
#     # --- 5. File Size Calculation ---
#     size = 0
#     if actual_path and os.path.exists(actual_path):
#         size = os.path.getsize(actual_path)
#     elif os.path.exists(backup_path): # Check backup path size if live file isn't found
#         size = os.path.getsize(backup_path)
#
#     # --- 6. CRITICAL SNAPSHOT OVERRIDE ---
#     if is_snapshot_view:
#         # For a snapshot, the only relevant 'actual_path' is the backup_path itself.
#         actual_path = backup_path
#         location_source = 'snapshot'
#
#         # Override status flags to reflect existence in the backup
#         exists_at_home = True
#         exists_at_current = True
#
#     # --- 7. Final Status Calculation ---
#     is_moved: bool = bool(actual_path and actual_path != home_path and actual_path != backup_path)
#
#     # --- 8. Debugging (keep for development) ---
#     print(f"Size: {size}")
#     print(f"Home Path: {home_path}")
#     print(f"Current Location (DB): {current_location}")
#     print(f"Actual Path: {actual_path}")
#     print(f"Exists: {exists_at_home or exists_at_current}")
#     print(f"Backup Path: {backup_path}")
#     print(f"Is Moved: {is_moved}")
#     print(f"Location Source: {location_source}")
#
#     return jsonify({
#         'success': True,
#         'size': size,
#         'home_path': home_path,        # Expected original path (used for restore destination)
#         'current_location': current_location, # Last known location from database
#         'actual_path': actual_path,      # Where it is physically found (or backup_path if snapshot)
#         'exists': exists_at_home or exists_at_current, # True if found live or in backup
#         'backup_path': backup_path,    # The path that was requested
#         'is_moved': is_moved,          # Status flag for moved files
#         'needs_search': not (exists_at_home or exists_at_current),
#         'location_source': location_source,
#         'display_path': actual_path or home_path # Path to show the user
#     })
#
#
# @app.route('/api/search-moved-file', methods=['POST'])
# def search_moved_file():
#     """ON-DEMAND hash-based search for moved files"""
#     try:
#         data = request.get_json()
#         backup_path = data.get('file_path')
#         fast_search = data.get('fast_search', True)
#
#         if not backup_path or not os.path.exists(backup_path):
#             app.logger.error(f"❌ Backup file not found: {backup_path}")
#             return jsonify({'success': False, 'error': 'Backup file not found'}), 404
#
#         print(f"\n🔍 ON-DEMAND SEARCH STARTED")
#         print(f"   Backup file: {backup_path}")
#         print(f"   File exists: {os.path.exists(backup_path)}")
#
#         # 1. Calculate hash of backup file
#         start_time = time.time()
#
#         if fast_search:
#             backup_hash = calculate_fast_hash(backup_path)
#         else:
#             backup_hash = calculate_file_hash(backup_path, use_cache=True)
#
#         hash_time = time.time() - start_time
#
#         if not backup_hash:
#             print(f"❌ Could not calculate file hash")
#             return jsonify({
#                 'success': True,
#                 'found': False,
#                 'message': 'Could not calculate file hash'
#             })
#
#         print(f"✓ Hash calculated in {hash_time:.2f}s")
#         print(f"   Hash (first 12 chars): {backup_hash[:12]}...")
#
#         # 2. Get expected home location
#         expected_home_path = convert_backup_to_home_path(backup_path)
#         print(f"   Expected home path: {expected_home_path}")
#
#         # 3. Check database first
#         current_location = get_file_location(backup_path, backup_hash)
#         if current_location and os.path.exists(current_location):
#             # Verify hash matches
#             current_hash = calculate_fast_hash(current_location)
#             if current_hash == backup_hash:
#                 print(f"✓ File found in database cache!")
#                 return jsonify({
#                     'success': True,
#                     'found': True,
#                     'current_location': current_location,
#                     'original_location': expected_home_path,
#                     'search_method': 'database_cache',
#                     'search_time': 0.0,
#                     'hash_time': hash_time
#                 })
#
#         # 4. Check if file exists at expected location
#         if os.path.exists(expected_home_path):
#             # Verify hash matches
#             existing_hash = calculate_fast_hash(expected_home_path)
#             if existing_hash == backup_hash:
#                 print(f"✓ File exists at expected location!")
#                 # Save to database
#                 save_file_location(backup_path, expected_home_path, expected_home_path, backup_hash)
#                 return jsonify({
#                     'success': True,
#                     'found': True,
#                     'current_location': expected_home_path,
#                     'original_location': expected_home_path,
#                     'search_method': 'path',
#                     'search_time': 0.0,
#                     'hash_time': hash_time
#                 })
#
#         # 5. Hash-based search
#         print(f"📂 Starting hash-based search...")
#         search_start = time.time()
#
#         result = find_file_by_hash(backup_hash, backup_path)
#         search_time = time.time() - search_start
#
#         if result:
#             print(f"\n✅ SEARCH SUCCESSFUL!")
#             print(f"   Found file at: {result['path']}")
#             print(f"   Found in: {result.get('found_in', 'unknown')}")
#
#             # Save to database
#             save_file_location(backup_path, expected_home_path, result['path'], backup_hash)
#
#             return jsonify({
#                 'success': True,
#                 'found': True,
#                 'current_location': result['path'],
#                 'original_location': expected_home_path,
#                 'search_method': 'hash',
#                 'search_time': search_time,
#                 'hash_time': hash_time,
#                 'found_in': result.get('found_in', 'unknown'),
#                 'source': result.get('source', 'hash_search')
#             })
#
#         print(f"\n❌ SEARCH FAILED - File not found")
#
#         return jsonify({
#             'success': True,
#             'found': False,
#             'message': 'File not found in home directory',
#             'search_time': search_time,
#             'hash_time': hash_time
#         })
#
#     except Exception as e:
#         app.logger.error(f"❌ Search error: {e}", exc_info=True)
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# @app.route('/api/save-file-location', methods=['POST'])
# def save_file_location_endpoint():
#     """Save or update a file's location in the database"""
#     try:
#         data = request.get_json()
#         backup_path = data.get('backup_path')
#         current_home_path = data.get('current_home_path')
#
#         if not backup_path or not current_home_path:
#             return jsonify({'success': False, 'error': 'Missing required fields'}), 400
#
#         # Calculate hash
#         file_hash = None
#         if os.path.exists(backup_path):
#             file_hash = calculate_fast_hash(backup_path)
#
#         original_home_path = convert_backup_to_home_path(backup_path)
#
#         if save_file_location(backup_path, original_home_path, current_home_path, file_hash):
#             return jsonify({'success': True, 'message': 'File location saved'})
#         else:
#             return jsonify({'success': False, 'error': 'Failed to save location'}), 500
#
#     except Exception as e:
#         app.logger.error(f"Error saving file location: {e}", exc_info=True)
#         return jsonify({'success': False, 'error': str(e)}), 500
#
# def cleanup_zombie_daemons():
#     """Clean up any zombie/defunct daemon processes."""
#     app_name = server.APP_NAME.lower()
#     zombies_cleaned = 0
#
#     for proc in psutil.process_iter(['pid', 'name', 'status', 'cmdline']):
#         try:
#             # Check if it's our daemon
#             cmdline = ' '.join(proc.info['cmdline'] or []).lower()
#             if app_name in cmdline and 'daemon' in cmdline:
#
#                 # Check if it's zombie/defunct
#                 if proc.info['status'] == psutil.STATUS_ZOMBIE:
#                     print(f"Found zombie daemon process: PID {proc.info['pid']}")
#
#                     # Try to reap it
#                     try:
#                         os.waitpid(proc.info['pid'], os.WNOHANG)
#                         zombies_cleaned += 1
#                     except (ChildProcessError, ProcessLookupError):
#                         pass
#
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue
#
#     if zombies_cleaned > 0:
#         print(f"Cleaned up {zombies_cleaned} zombie daemon processes")
#
#     return zombies_cleaned
#
# def cleanup_zombie_daemons():
#     """Clean up any zombie/defunct daemon processes."""
#     app_name = server.APP_NAME.lower()
#     zombies_cleaned = 0
#
#     for proc in psutil.process_iter(['pid', 'name', 'status', 'cmdline']):
#         try:
#             # Check if it's our daemon
#             cmdline = ' '.join(proc.info['cmdline'] or []).lower()
#             if app_name in cmdline and 'daemon' in cmdline:
#
#                 # Check if it's zombie/defunct
#                 if proc.info['status'] == psutil.STATUS_ZOMBIE:
#                     print(f"Found zombie daemon process: PID {proc.info['pid']}")
#
#                     # Try to reap it
#                     try:
#                         os.waitpid(proc.info['pid'], os.WNOHANG)
#                         zombies_cleaned += 1
#                     except (ChildProcessError, ProcessLookupError):
#                         pass
#
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue
#
#     if zombies_cleaned > 0:
#         print(f"Cleaned up {zombies_cleaned} zombie daemon processes")
#
#     return zombies_cleaned
#
#
# # =============================================================================
# # MIGRATION SOURCES
# # =============================================================================
# @app.route('/api/migration/sources', methods=['GET'])
# def get_migration_sources():
#     """Scans all storage devices and returns only those that contain a valid Time Machine backup directory."""
#     try:
#         all_devices = get_all_storage_devices()
#         valid_sources = []
#
#         for device in all_devices:
#             mount_point = device.get('mount_point')
#             if not mount_point:
#                 continue
#
#             main_backup_path = os.path.join(mount_point, 'timemachine', 'backups', server.MAIN_BACKUP_LOCATION)
#
#             if os.path.isdir(main_backup_path) and os.listdir(main_backup_path):
#                 device['has_backup'] = True
#                 device['last_backup_date'] = "Recent"
#                 valid_sources.append(device)
#
#         return jsonify({
#             'success': True,
#             'sources': valid_sources
#         })
#
#     except Exception as e:
#         app.logger.error(f"Error scanning for migration sources: {e}", exc_info=True)
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#
# # =============================================================================
# # DAEMON CONTROL ROUTES
# # =============================================================================
# @app.route('/api/daemon/ready-status', methods=['GET'])
# def daemon_ready_status():
#     """Check if daemon is ready for auto-start configuration."""
#     try:
#         def check_daemon_ready():
#             """Check if daemon is ready by looking for the hidden file."""
#             try:
#                 app_name = server.APP_NAME
#                 ready_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon_ready')
#                 lock_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon.lock')
#
#                 status = {
#                     "is_ready": False,
#                     "daemon_running": False,
#                     "pid": None,
#                     "startup_time": None,
#                     "metadata_loaded": False,
#                     "has_lock_file": False,
#                     "error": None
#                 }
#
#                 # Check lock file first (indicates daemon is running)
#                 if os.path.exists(lock_file):
#                     status["has_lock_file"] = True
#                     try:
#                         with open(lock_file, 'r') as f:
#                             pid_str = f.read().strip()
#                             if pid_str.isdigit():
#                                 pid = int(pid_str)
#                                 status["pid"] = pid
#
#                                 # Check if process is actually running
#                                 try:
#                                     process = psutil.Process(pid)
#                                     if process.is_running():
#                                         status["daemon_running"] = True
#                                 except (psutil.NoSuchProcess, psutil.AccessDenied):
#                                     # Stale lock file
#                                     status["daemon_running"] = False
#                                     status["error"] = "Stale lock file detected"
#                     except Exception as e:
#                         status["error"] = f"Lock file error: {e}"
#
#                 # Check ready file (indicates daemon is fully initialized)
#                 if os.path.exists(ready_file):
#                     try:
#                         with open(ready_file, 'r') as f:
#                             data = json.load(f)
#
#                         status["pid"] = data.get('pid')
#                         status["startup_time"] = data.get('ready_time')
#                         status["metadata_count"] = data.get('metadata_count', 0)
#                         status["metadata_loaded"] = status["metadata_count"] > 0
#
#                         # Verify PID is still running
#                         if status["pid"]:
#                             try:
#                                 process = psutil.Process(status["pid"])
#                                 if process.is_running():
#                                     status["daemon_running"] = True
#                                     status["is_ready"] = True
#                                 else:
#                                     status["error"] = "Ready file exists but process not running"
#                             except (psutil.NoSuchProcess, psutil.AccessDenied):
#                                 status["error"] = "Ready file exists but process not running"
#                         else:
#                             status["error"] = "No PID in ready file"
#
#                     except json.JSONDecodeError:
#                         status["error"] = "Corrupted ready file"
#                     except Exception as e:
#                         status["error"] = f"Error reading ready file: {e}"
#                 elif status["daemon_running"]:
#                     # Daemon is running but not ready yet
#                     status["is_ready"] = False
#                     status["error"] = "Daemon is starting up..."
#
#                 return status
#
#             except Exception as e:
#                 return {
#                     "is_ready": False,
#                     "daemon_running": False,
#                     "error": f"Check error: {e}"
#                 }
#
#         status = check_daemon_ready()
#
#         # Calculate startup progress if daemon is running but not ready
#         startup_progress = None
#         if status["daemon_running"] and not status["is_ready"]:
#             # Check if we have a lock file with timestamp
#             lock_file = os.path.join(os.path.expanduser("~"), f'.{server.APP_NAME.lower()}_daemon.lock')
#             if os.path.exists(lock_file):
#                 file_age = time.time() - os.path.getmtime(lock_file)
#                 # Assuming max startup time is 90 seconds
#                 startup_progress = min(90, int(file_age))
#
#         return jsonify({
#             "success": True,
#             "ready": status["is_ready"],
#             "running": status["daemon_running"],
#             "status": status,
#             "startup_progress": startup_progress,
#             "message": (
#                 "Daemon is ready" if status["is_ready"] else
#                 "Daemon is starting up..." if status["daemon_running"] else
#                 "Daemon is not running"
#             )
#         })
#
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "ready": False,
#             "running": False
#         }), 500
#
# def check_daemon_ready():
#     """Check if daemon is ready by looking for the hidden file."""
#     try:
#         app_name = server.APP_NAME
#         ready_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon_ready')
#         lock_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon.lock')
#
#         status = {
#             "is_ready": False,
#             "daemon_running": False,
#             "pid": None,
#             "startup_time": None,
#             "metadata_loaded": False,
#             "has_lock_file": False,
#             "error": None
#         }
#
#         # Check lock file first (indicates daemon is running)
#         if os.path.exists(lock_file):
#             status["has_lock_file"] = True
#             try:
#                 with open(lock_file, 'r') as f:
#                     pid_str = f.read().strip()
#                     if pid_str.isdigit():
#                         pid = int(pid_str)
#                         status["pid"] = pid
#
#                         # Check if process is actually running
#                         try:
#                             process = psutil.Process(pid)
#                             if process.is_running():
#                                 status["daemon_running"] = True
#                         except (psutil.NoSuchProcess, psutil.AccessDenied):
#                             # Stale lock file
#                             status["daemon_running"] = False
#                             status["error"] = "Stale lock file detected"
#             except Exception as e:
#                 status["error"] = f"Lock file error: {e}"
#
#         # Check ready file (indicates daemon is fully initialized)
#         if os.path.exists(ready_file):
#             try:
#                 with open(ready_file, 'r') as f:
#                     data = json.load(f)
#
#                 status["pid"] = data.get('pid')
#                 status["startup_time"] = data.get('ready_time')
#                 status["metadata_count"] = data.get('metadata_count', 0)
#                 status["metadata_loaded"] = status["metadata_count"] > 0
#
#                 # Verify PID is still running
#                 if status["pid"]:
#                     try:
#                         process = psutil.Process(status["pid"])
#                         if process.is_running():
#                             status["daemon_running"] = True
#                             status["is_ready"] = True
#                         else:
#                             status["error"] = "Ready file exists but process not running"
#                     except (psutil.NoSuchProcess, psutil.AccessDenied):
#                         status["error"] = "Ready file exists but process not running"
#                 else:
#                     status["error"] = "No PID in ready file"
#
#             except json.JSONDecodeError:
#                 status["error"] = "Corrupted ready file"
#             except Exception as e:
#                 status["error"] = f"Error reading ready file: {e}"
#         elif status["daemon_running"]:
#             # Daemon is running but not ready yet
#             status["is_ready"] = False
#             status["error"] = "Daemon is starting up..."
#
#         return status
#
#     except Exception as e:
#         return {
#             "is_ready": False,
#             "daemon_running": False,
#             "error": f"Check error: {e}"
#         }
#
# @app.route('/api/daemon/status', methods=['GET'])
# def get_daemon_status():
#     return jsonify(server.get_daemon_status())
#
# @app.route('/api/daemon/start', methods=['POST'])
# def start_daemon_process():
#     result = server.start_daemon() or {'success': False, 'error': 'No response from daemon'}
#     return jsonify(result), 200 if result.get('success') else 500
#
# @app.post('/api/backup/cancel')
# def cancel_backup_task():
#     data = request.get_json(silent=True) or {}
#     mode = data.get('mode', 'graceful')
#     ok = send_control_command('cancel', mode)
#     return jsonify({'result': 'ok' if ok else 'error', 'mode': mode}), (200 if ok else 500)
#
# # =============================================================================
# # CORE APPLICATION ROUTES
# # =============================================================================
# @app.route('/')
# def main_index():
#     """The main route rendering the base index.html template."""
#     return render_template('index.html')
#
# # =============================================================================
# # APPLICATION ENTRY POINT
# # =============================================================================
# if __name__ == '__main__':
#     # Initialize the database
#     init_location_database()
#
#     # Create backup service
#     backup_service = BackupService()
#
#     # Start WebSocket server in background thread
#     threading.Thread(target=backup_service.start_server, daemon=True).start()
#
#     # Start Flask application
#     from werkzeug.serving import run_simple
#     run_simple('127.0.0.1', 5000, app, use_reloader=False, use_debugger=False, threaded=True)

# app.py - Time Machine Backup Application
import os
import json
import time
import signal
import sqlite3
import threading
import configparser
import subprocess as sub
from datetime import datetime
import pathlib
from pathlib import Path
import socket
import hashlib
import psutil
import shutil
import re
import platform

from flask import Flask, render_template, jsonify, request
from flask_sock import Sock

# Application modules
from static.py.server import SERVER
from static.py.search_handler import SearchHandler
from static.py.storage_util import get_all_storage_devices
from static.py.daemon_control import send_control_command
from static.py.necessaries_actions import base_folders_creation

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
USERS_HOME: str = os.path.expanduser("~")
# app_dir = os.path.dirname(os.path.abspath(__file__))
# CONFIG_PATH = os.path.join(app_dir, 'config', 'config.conf')
# LOCATION_DB_PATH = os.path.join(app_dir, 'config', 'file_locations.db')

# Icon mappings for folder types
FOLDER_ICONS = {
    'documents': {'icon': 'bi-file-earmark-text-fill', 'color': 'text-blue-500'},
    'downloads': {'icon': 'bi-arrow-down-circle-fill', 'color': 'text-teal-500'},
    'pictures': {'icon': 'bi-image-fill', 'color': 'text-pink-500'},
    'photos': {'icon': 'bi-image-fill', 'color': 'text-pink-500'},
    'videos': {'icon': 'bi-camera-video-fill', 'color': 'text-red-500'},
    'video': {'icon': 'bi-camera-video-fill', 'color': 'text-red-500'},
    'music': {'icon': 'bi-music-note-beamed', 'color': 'text-purple-500'},
    'desktop': {'icon': 'bi-display-fill', 'color': 'text-emerald-500'},
    'public': {'icon': 'bi-share-fill', 'color': 'text-yellow-500'},
    'templates': {'icon': 'bi-code-square', 'color': 'text-orange-500'},
    'code': {'icon': 'bi-code-slash', 'color': 'text-cyan-500'},
    'games': {'icon': 'bi-joystick', 'color': 'text-cyan-500'},
    'mega': {'icon': 'bi-cloudy-fill', 'color': 'text-cyan-500'},
    'dropbox': {'icon': 'bi-cloudy-fill', 'color': 'text-cyan-500'},
}

# =============================================================================
# APP INITIALIZATION
# =============================================================================
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
sock = Sock(app)

server = SERVER()
search_handler = SearchHandler()
ws_clients = []  # Track WebSocket clients

CONFIG_PATH = server.CONF_PATH
LOCATION_DB_PATH = os.path.join(os.path.dirname(server.CONF_PATH), 'file_locations.db')


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def calculate_fast_hash(file_path: str, bytes_to_read: int = 1024 * 1024) -> str | None:
    """Fast hash calculation for searching."""
    if not os.path.exists(file_path):
        return None

    try:
        file_size = os.path.getsize(file_path)
        hasher = hashlib.sha256()

        # Include file size in hash
        hasher.update(str(file_size).encode())

        with open(file_path, "rb") as f:
            # Read first chunk
            first_chunk_size = min(bytes_to_read, file_size)
            first_chunk = f.read(first_chunk_size)
            hasher.update(first_chunk)

            # Read last 64KB if file is large enough
            if file_size > bytes_to_read * 2:
                last_chunk_size = min(65536, file_size - first_chunk_size)
                if last_chunk_size > 0:
                    f.seek(-last_chunk_size, 2)
                    last_chunk = f.read()
                    hasher.update(last_chunk)

        return hasher.hexdigest()
    except Exception as e:
        app.logger.error(f"Fast hash error for {file_path}: {e}")
        return None

def get_cached_hash(file_path: str) -> str | None:
    """Get cached hash for a file from database."""
    try:
        if not os.path.exists(file_path):
            return None

        conn = sqlite3.connect(LOCATION_DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT file_hash FROM file_metadata
            WHERE file_path = ?
        ''', (file_path,))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None
    except Exception as e:
        app.logger.error(f"Error getting cached hash: {e}")
        return None

def cache_file_metadata(file_path: str, file_size: int, file_hash: str) -> bool:
    """Cache file metadata in database."""
    try:
        conn = sqlite3.connect(LOCATION_DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO file_metadata
            (file_path, file_size, file_hash, last_modified, indexed_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (file_path, file_size, file_hash, int(time.time())))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        app.logger.error(f"Error caching metadata: {e}")
        return False

def calculate_file_hash(file_path: str, use_cache: bool = True, fast_mode: bool = False) -> str | None:
    """Calculate SHA256 hash with caching."""
    if fast_mode:
        return calculate_fast_hash(file_path)

    # Try to get cached hash first
    if use_cache:
        cached_hash = get_cached_hash(file_path)
        if cached_hash:
            return cached_hash

    # Calculate fresh hash
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256_hash.update(chunk)

        hash_value = sha256_hash.hexdigest()

        # Cache the result
        if use_cache and os.path.exists(file_path):
            file_stat = os.stat(file_path)
            cache_file_metadata(file_path, file_stat.st_size, hash_value)

        return hash_value
    except Exception as e:
        app.logger.error(f"Error calculating hash for {file_path}: {e}")
        return None

# =============================================================================
# DATABASE MANAGEMENT
# =============================================================================
def init_location_database() -> bool:
    """Initialize SQLite database for tracking file locations."""
    try:
        os.makedirs(os.path.dirname(LOCATION_DB_PATH), exist_ok=True)

        conn = sqlite3.connect(LOCATION_DB_PATH)
        cursor = conn.cursor()

        # File locations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_path TEXT NOT NULL,
                original_home_path TEXT NOT NULL,
                current_home_path TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(backup_path, file_hash)
            )
        ''')

        # File metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                file_size INTEGER,
                file_hash TEXT,
                last_modified TIMESTAMP,
                indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_backup_path ON file_locations(backup_path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_hash ON file_locations(file_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_current_path ON file_locations(current_home_path)')

        conn.commit()
        conn.close()
        app.logger.info(f"Initialized location database at {LOCATION_DB_PATH}")
        return True
    except Exception as e:
        app.logger.error(f"Error initializing database: {e}")
        return False

class DatabaseManager:
    """Manages database operations for file tracking."""

    @staticmethod
    def get_file_location(backup_path: str, file_hash: str = None) -> str | None:
        """Get current home location for a backup file."""
        try:
            conn = sqlite3.connect(LOCATION_DB_PATH)
            cursor = conn.cursor()

            if file_hash:
                cursor.execute('''
                    SELECT current_home_path FROM file_locations
                    WHERE (backup_path = ? OR file_hash = ?)
                    ORDER BY last_checked DESC LIMIT 1
                ''', (backup_path, file_hash))
            else:
                cursor.execute('''
                    SELECT current_home_path FROM file_locations
                    WHERE backup_path = ?
                    ORDER BY last_checked DESC LIMIT 1
                ''', (backup_path,))

            result = cursor.fetchone()
            conn.close()

            if result and os.path.exists(result[0]):
                return result[0]
            elif result:
                DatabaseManager.remove_file_location(backup_path)
            return None
        except Exception as e:
            app.logger.error(f"Error getting file location: {e}")
            return None

    @staticmethod
    def save_file_location(backup_path: str, original_home_path: str,
                          current_home_path: str, file_hash: str) -> bool:
        """Save or update file location."""
        try:
            conn = sqlite3.connect(LOCATION_DB_PATH)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO file_locations
                (backup_path, original_home_path, current_home_path, file_hash, last_checked)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (backup_path, original_home_path, current_home_path, file_hash))

            conn.commit()
            conn.close()
            app.logger.info(f"Saved location for {os.path.basename(backup_path)}")
            return True
        except Exception as e:
            app.logger.error(f"Error saving file location: {e}")
            return False

    @staticmethod
    def remove_file_location(backup_path: str) -> bool:
        """Remove file location entry."""
        try:
            conn = sqlite3.connect(LOCATION_DB_PATH)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM file_locations WHERE backup_path = ?', (backup_path,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            app.logger.error(f"Error removing file location: {e}")
            return False

# =============================================================================
# BACKUP SERVICE
# =============================================================================
class BackupService:
    """Core backup service managing daemon communication."""

    def __init__(self):
        app.logger.info("BackupService initialized")
        server._create_default_config()

    def start_ipc_server(self):
        """UNIX Socket listener for daemon communication."""
        socket_path = server.SOCKET_PATH

        if os.path.exists(socket_path):
            os.remove(socket_path)

        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
                listener.bind(socket_path)
                listener.listen(1)
                app.logger.info(f"Listening for daemon on UNIX socket: {socket_path}")

                while True:
                    conn, _ = listener.accept()
                    with conn:
                        data = b''
                        while True:
                            chunk = conn.recv(4096)
                            if not chunk:
                                break
                            data += chunk

                        if data:
                            self._process_ipc_data(data.decode('utf-8'))

        except Exception as e:
            app.logger.error(f"Fatal UNIX Socket error: {e}")

    def _process_ipc_data(self, data: str):
        """Process IPC messages and broadcast to WebSocket clients."""
        for line in data.strip().split('\n'):
            if not line:
                continue
            try:
                msg = json.loads(line)
                self._broadcast_to_websockets(msg)
            except json.JSONDecodeError as e:
                app.logger.error(f"Invalid JSON line: {e}. Data: {line[:50]}...")

    def _broadcast_to_websockets(self, message: dict):
        """Broadcast message to all WebSocket clients."""
        message_json = json.dumps(message)
        disconnected_clients = []

        for client_ws in ws_clients:
            try:
                client_ws.send(message_json)
            except Exception:
                disconnected_clients.append(client_ws)

        # Clean up disconnected clients
        for client in disconnected_clients:
            try:
                ws_clients.remove(client)
            except ValueError:
                pass

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def convert_backup_to_home_path(backup_path: str) -> str:
    """Convert backup path to home directory path."""
    if not backup_path:
        return ''

    home_dir = os.path.expanduser("~")
    patterns = [server.MAIN_BACKUP_LOCATION, 'timemachine/backups', 'backups']

    for pattern in patterns:
        if pattern in backup_path:
            parts = backup_path.split(pattern)
            if len(parts) > 1:
                relative_path = parts[1].lstrip('/').lstrip('\\')
                return os.path.join(home_dir, relative_path)

    # Fallback: just return filename in home directory
    filename = os.path.basename(backup_path)
    return os.path.join(home_dir, filename)

def get_system_devices() -> list:
    """Gather local storage device information."""
    devices = []

    try:
        partitions = psutil.disk_partitions(all=False)

        for i, partition in enumerate(partitions):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                used_gb = usage.used / (1024 ** 3)
                total_gb = usage.total / (1024 ** 3)
                percent_used = usage.percent

                # Determine status
                if percent_used > 90:
                    status, color = 'Critical', 'text-red-500'
                elif percent_used > 75:
                    status, color = 'Warning', 'text-yellow-500'
                else:
                    status, color = 'Healthy', 'text-green-500'

                # Determine icon
                if partition.mountpoint == '/':
                    icon = 'bi-hdd-fill'
                elif 'usb' in partition.device.lower():
                    icon = 'bi-usb-drive-fill'
                else:
                    icon = 'bi-disc-fill'

                devices.append({
                    'id': i + 1,
                    'name': os.path.basename(partition.mountpoint) or 'Root',
                    'mountpoint': partition.mountpoint,
                    'status': status,
                    'color': color,
                    'progress': percent_used,
                    'used_space': f"{used_gb:.2f} GB",
                    'total_space': f"{total_gb:.2f} GB",
                    'last_backup': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'backup_count': 0,
                    'icon': icon
                })
            except Exception as e:
                app.logger.warning(f"Error reading partition {partition.mountpoint}: {e}")
                continue

    except Exception as e:
        app.logger.error(f"Error getting system devices: {e}")

    return devices

def check_daemon_ready():
    """Check if daemon is ready by looking for the hidden file."""
    try:
        app_name = server.APP_NAME
        ready_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon_ready')
        lock_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon.lock')

        status = {
            "is_ready": False,
            "daemon_running": False,
            "pid": None,
            "startup_time": None,
            "metadata_loaded": False,
            "has_lock_file": False,
            "error": None
        }

        # Check lock file first (indicates daemon is running)
        if os.path.exists(lock_file):
            status["has_lock_file"] = True
            try:
                with open(lock_file, 'r') as f:
                    pid_str = f.read().strip()
                    if pid_str.isdigit():
                        pid = int(pid_str)
                        status["pid"] = pid

                        # Check if process is actually running
                        try:
                            process = psutil.Process(pid)
                            if process.is_running():
                                status["daemon_running"] = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            # Stale lock file
                            status["daemon_running"] = False
                            status["error"] = "Stale lock file detected"
            except Exception as e:
                status["error"] = f"Lock file error: {e}"

        # Check ready file (indicates daemon is fully initialized)
        if os.path.exists(ready_file):
            try:
                with open(ready_file, 'r') as f:
                    data = json.load(f)

                status["pid"] = data.get('pid')
                status["startup_time"] = data.get('ready_time')
                status["metadata_count"] = data.get('metadata_count', 0)
                status["metadata_loaded"] = status["metadata_count"] > 0

                # Verify PID is still running
                if status["pid"]:
                    try:
                        process = psutil.Process(status["pid"])
                        if process.is_running():
                            status["daemon_running"] = True
                            status["is_ready"] = True
                        else:
                            status["error"] = "Ready file exists but process not running"
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        status["error"] = "Ready file exists but process not running"
                else:
                    status["error"] = "No PID in ready file"

            except json.JSONDecodeError:
                status["error"] = "Corrupted ready file"
            except Exception as e:
                status["error"] = f"Error reading ready file: {e}"
        elif status["daemon_running"]:
            # Daemon is running but not ready yet
            status["is_ready"] = False
            status["error"] = "Daemon is starting up..."

        return status

    except Exception as e:
        return {
            "is_ready": False,
            "daemon_running": False,
            "error": f"Check error: {e}"
        }

# =============================================================================
# ROUTES - CONFIGURATION
# =============================================================================
@app.route('/api/config')
def get_config_data():
    """Read the entire config.conf file."""
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_PATH)
        config_dict = {}

        for section in config.sections():
            config_dict[section] = dict(config.items(section))

        if config.defaults():
            config_dict['DEFAULT'] = config.defaults()

        return jsonify(config_dict)
    except Exception as e:
        app.logger.error(f"Error reading config: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to read configuration file: {str(e)}'
        }), 500

@app.route('/api/backup-folders', methods=['GET'])
def get_backup_folders():
    """List all home folders and check if they are in config."""
    try:
        home_path = os.path.expanduser('~')
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        # Get saved folders from config
        saved_folders = []
        if config.has_section('BACKUP_FOLDERS') and config.has_option('BACKUP_FOLDERS', 'folders'):
            raw = config.get('BACKUP_FOLDERS', 'folders')
            saved_folders = [os.path.normpath(f.strip()) for f in raw.split(',') if f.strip()]

        folders_data = []

        for item in os.listdir(home_path):
            full_path = os.path.join(home_path, item)
            if os.path.isdir(full_path) and not item.startswith('.'):
                is_selected = os.path.normpath(full_path) in saved_folders
                icon_data = FOLDER_ICONS.get(
                    item.lower(),
                    {'icon': 'bi-folder-fill', 'color': 'text-brand-500'}
                )

                folders_data.append({
                    'name': item,
                    'path': full_path,
                    'selected': is_selected,
                    'icon': icon_data['icon'],
                    'color': icon_data['color']
                })

        folders_data.sort(key=lambda x: x['name'].lower())
        return jsonify({'success': True, 'folders': folders_data})

    except Exception as e:
        app.logger.error(f"Error getting backup folders: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save-backup-folders', methods=['POST'])
def save_backup_folders():
    """Save selected folders to config file."""
    try:
        data = request.get_json()
        selected_folders = data.get('folders', [])

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        if not config.has_section('BACKUP_FOLDERS'):
            config.add_section('BACKUP_FOLDERS')

        config.set('BACKUP_FOLDERS', 'folders', ','.join(selected_folders))

        with open(CONFIG_PATH, 'w') as f:
            config.write(f)

        return jsonify({'success': True})
    except Exception as e:
        app.logger.error(f"Error saving backup folders: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# =============================================================================
# ROUTES - DEVICES & STORAGE
# =============================================================================
@app.route('/api/storage/devices', methods=['GET'])
def scan_devices():
    """Scan and return all available storage devices."""
    try:
        devices = get_all_storage_devices()
        return jsonify({
            'success': True,
            'devices': devices,
            'count': len(devices)
        })
    except Exception as e:
        app.logger.error(f"Error scanning devices: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/backup/select-device', methods=['POST'])
def select_device():
    """Select and configure backup device."""
    try:
        data = request.get_json()
        device_info = data.get('device_info', {})
        device_path = device_info.get('mount_point')

        if not device_path:
            return jsonify({'success': False, 'error': 'No device path provided'}), 400

        if not os.path.exists(device_path):
            return jsonify({
                'success': False,
                'error': f'Path does not exist: {device_path}'
            }), 400

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        if not config.has_section('DEVICE_INFO'):
            config.add_section('DEVICE_INFO')


        def update_backup_folders_path(config):
            # 2. Get the current folders string from the config
            current_folders_string = config.get('BACKUP_FOLDERS', 'folders', fallback='')

            # 3. Dynamically determine the NEW user's home path (e.g., /home/macbook)
            NEW_HOME_PATH_PREFIX = str(pathlib.Path.home())

            # 4. Extract the OLD home path prefix (e.g., /home/mark) using regex
            # This looks for '/home/username' at the start of any folder path
            old_user_match = re.search(r'(/home/[^/]+)', current_folders_string)

            if old_user_match:
                OLD_HOME_PATH_PREFIX = old_user_match.group(1)

                # 5. Only perform the replacement if the paths are different
                if OLD_HOME_PATH_PREFIX != NEW_HOME_PATH_PREFIX:

                    # Perform the replacement on the entire folders string
                    updated_folders_string = current_folders_string.replace(
                        OLD_HOME_PATH_PREFIX,
                        NEW_HOME_PATH_PREFIX
                    )

                    # 6. Save the updated string back to the config object
                    if not config.has_section('BACKUP_FOLDERS'):
                        config.add_section('BACKUP_FOLDERS')

                    config.set('BACKUP_FOLDERS', 'folders', updated_folders_string)
                # If OLD_HOME_PATH_PREFIX == NEW_HOME_PATH_PREFIX, no change is needed.

            # --- DYNAMIC PATH UPDATE LOGIC END ---

        # --- DYNAMIC PATH UPDATE LOGIC START ---
        update_backup_folders_path(config)

        # Save device info to config
        config.set('DEVICE_INFO', 'path', str(device_path))
        config.set('DEVICE_INFO', 'name', str(device_info.get('name', 'N/A')))
        config.set('DEVICE_INFO', 'device', str(device_info.get('device', 'N/A')))
        config.set('DEVICE_INFO', 'serial_number', str(device_info.get('serial_number', 'N/A')))
        config.set('DEVICE_INFO', 'model', str(device_info.get('model', 'N/A')))
        config.set('DEVICE_INFO', 'filesystem', str(device_info.get('filesystem', 'N/A')))
        config.set('DEVICE_INFO', 'total_size_bytes', str(device_info.get('total', 0)))

        # Set disk type
        is_ssd = device_info.get('is_ssd', False)
        config.set('DEVICE_INFO', 'disk_type', 'ssd' if is_ssd else 'hdd')

        # Update configs [BACKUP_FOLDERS], to also match selected device:

        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

        # Update search handler with new location
        if hasattr(search_handler, 'update_backup_location'):
            search_handler.update_backup_location()

        return jsonify({
            'success': True,
            'message': f'Backup device {device_path} configured successfully.',
            'path': device_path
        })

    except Exception as e:
        app.logger.error(f"Failed to save configuration: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to save configuration: {str(e)}'
        }), 500

# =============================================================================
# ROUTES - BACKUP STATUS
# =============================================================================
@app.route('/api/backup/connection')
def backup_connection():
    """Check backup device connection status."""
    try:
        if hasattr(server, 'get_database_value'):
            driver_path = server.get_database_value('DEVICE_INFO', 'path')
        else:
            # Fallback to reading config directly
            config = configparser.ConfigParser()
            config.read(CONFIG_PATH)
            driver_path = config.get('DEVICE_INFO', 'path', fallback=None)

        if driver_path:
            return jsonify({
                'success': True,
                'connected': os.path.exists(driver_path),
                'location': driver_path
            })
        else:
            return jsonify({
                'success': False,
                'connected': False,
                'location': 'Not configured'
            })
    except Exception as e:
        app.logger.error(f"Error checking backup connection: {e}")
        return jsonify({
            'success': False,
            'connected': False,
            'error': str(e)
        }), 500

@app.route('/api/backup/usage')
def backup_usage():
    """Get backup device usage statistics."""
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        # Check if device is configured
        if not config.has_section('DEVICE_INFO') or not config.has_option('DEVICE_INFO', 'path'):
            return jsonify({
                'success': False,
                'error': 'Please select a backup device first!',
                'user_action_required': True
            })

        driver_path = config.get('DEVICE_INFO', 'path')

        if not driver_path or not os.path.exists(driver_path):
            return jsonify({
                'success': False,
                'error': 'Backup device is not connected.',
                'user_action_required': True,
                'location': driver_path or 'Not configured'
            })

        # Get backup device usage
        total, used, free = shutil.disk_usage(driver_path)
        percent_used = (used / total) * 100 if total > 0 else 0

        # Get home directory usage
        home_total, home_used, home_free = shutil.disk_usage(os.path.expanduser('~'))
        home_percent_used = (home_used / home_total) * 100 if home_total > 0 else 0

        bytes_to_human = SERVER.bytes_to_human
        
        def get_backup_summary() -> dict:
            """Retrieve backup summary from JSON file."""
            try:
                summary_file = server.get_summary_file_path()
                if not os.path.exists(summary_file):
                    return {}
                
                with open(summary_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                app.logger.error(f"Error decoding backup summary JSON: {e}")
                return {}
            
        return jsonify({
            'success': True,
            'location': driver_path,
            'percent_used': round(percent_used, 1),
            'human_used': bytes_to_human(used),
            'human_total': bytes_to_human(total),
            'human_free': bytes_to_human(free),
            'home_human_used': bytes_to_human(home_used),
            'home_human_total': bytes_to_human(home_total),
            'home_human_free': bytes_to_human(home_free),
            'home_percent_used': round(home_percent_used, 1),
            'users_home_path': os.path.expanduser('~'),
            'summary': get_backup_summary() or "No backup summary available",

        })

    except Exception as e:
        app.logger.error(f"Error in backup_usage: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'location': 'Error'
        }), 500

# =============================================================================
# ROUTES - SEARCH
# =============================================================================
@app.route('/api/search/status', methods=['GET'])
def search_status():
    """Check search cache status."""
    try:
        return jsonify({
            'success': True,
            'files_loaded': search_handler.files_loaded,
            'file_count': len(search_handler.files),
            'cache_valid': search_handler._files_cache is not None
        })
    except Exception as e:
        app.logger.error(f"Error getting search status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search/init', methods=['POST'])
def init_search():
    """Initialize file search indexing."""
    try:
        if not search_handler.files_loaded:
            search_handler.scan_files_folder_threaded()
            return jsonify({
                'success': True,
                'message': 'File scanning started in background',
                'scanning': True
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Files already loaded',
                'scanning': False,
                'file_count': len(search_handler.files)
            })
    except Exception as e:
        app.logger.error(f"Error initializing search: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search', methods=['GET'])
def search_files():
    """Search for files in backup."""
    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify({'files': [], 'total': 0})

    try:
        search_results = search_handler.perform_search(query)
        return jsonify({
            'files': search_results,
            'total': len(search_handler.files)
        })
    except Exception as e:
        app.logger.error(f"Error during file search: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred during search.',
            'files': []
        }), 500

# =============================================================================
# ROUTES - FILE OPERATIONS
# =============================================================================
@app.route('/api/file-info', methods=['POST'])
def file_info():
    """Get information about a file including current location."""
    try:
        data = request.json
        backup_path = data.get('file_path', '')

        if not backup_path:
            return jsonify({'success': False, 'error': 'No file path provided'}), 400

        # Get server attributes safely
        backups_dir = getattr(server, 'BACKUPS_LOCATION_DIR_NAME', 'timemachine/backups')
        main_backup = getattr(server, 'MAIN_BACKUP_LOCATION', server.MAIN_BACKUP_LOCATION)

        # Determine if viewing a snapshot
        is_snapshot = (backups_dir in backup_path and main_backup not in backup_path)

        # Get expected home path
        home_path = convert_backup_to_home_path(backup_path)

        # Check current location from database
        current_location = DatabaseManager.get_file_location(backup_path)

        # Determine actual path
        actual_path = None
        location_source = 'unknown'

        if current_location and os.path.exists(current_location):
            actual_path = current_location
            location_source = 'database'
        elif home_path and os.path.exists(home_path):
            actual_path = home_path
            location_source = 'expected'
        elif is_snapshot:
            actual_path = backup_path
            location_source = 'snapshot'

        # Get file size
        size = 0
        if actual_path and os.path.exists(actual_path):
            size = os.path.getsize(actual_path)
        elif os.path.exists(backup_path):
            size = os.path.getsize(backup_path)

        # Determine if file was moved
        is_moved = (actual_path and
                   actual_path != home_path and
                   actual_path != backup_path)

        return jsonify({
            'success': True,
            'size': size,
            'home_path': home_path,
            'current_location': current_location,
            'actual_path': actual_path,
            'exists': bool(actual_path),
            'backup_path': backup_path,
            'is_moved': is_moved,
            'needs_search': not bool(actual_path),
            'location_source': location_source,
            'display_path': actual_path or home_path
        })

    except Exception as e:
        app.logger.error(f"Error in file_info: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/restore-file', methods=['POST'])
def restore_file():
    """Restore file from backup to original or custom location."""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        restore_to = data.get('restore_to', 'original')  # 'original', 'current', or custom path

        if not file_path or not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404

        # Determine destination path
        if restore_to == 'original':
            destination_path = convert_backup_to_home_path(file_path)
        elif restore_to == 'current':
            current_location = DatabaseManager.get_file_location(file_path)
            destination_path = current_location or convert_backup_to_home_path(file_path)
        elif restore_to and os.path.isdir(restore_to):
            filename = os.path.basename(file_path)
            destination_path = os.path.join(restore_to, filename)
        else:
            destination_path = convert_backup_to_home_path(file_path)

        # Create destination directory if needed
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Copy file preserving metadata
        shutil.copy2(file_path, destination_path)

        # Update database with new location
        file_hash = calculate_fast_hash(file_path)
        original_home_path = convert_backup_to_home_path(file_path)
        DatabaseManager.save_file_location(file_path, original_home_path, destination_path, file_hash)

        # Open location dir
        if os.name == 'nt':
            os.startfile(os.path.dirname(destination_path))
        elif os.uname().sysname == 'Darwin':
            sub.run(['open', os.path.dirname(destination_path)])
        else:
            sub.run(['xdg-open', os.path.dirname(destination_path)])

        return jsonify({
            'success': True,
            'message': 'File restored successfully',
            'restored_to': destination_path
        })

    except Exception as e:
        app.logger.error(f"Error restoring file: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search-moved-file', methods=['POST'])
def search_moved_file():
    """ON-DEMAND hash-based search for moved files"""
    try:
        data = request.get_json()
        backup_path = data.get('file_path')
        fast_search = data.get('fast_search', True)

        if not backup_path or not os.path.exists(backup_path):
            app.logger.error(f"❌ Backup file not found: {backup_path}")
            return jsonify({'success': False, 'error': 'Backup file not found'}), 404

        print(f"\n🔍 ON-DEMAND SEARCH STARTED")
        print(f"   Backup file: {backup_path}")
        print(f"   File exists: {os.path.exists(backup_path)}")

        # 1. Calculate hash of backup file
        start_time = time.time()

        if fast_search:
            backup_hash = calculate_fast_hash(backup_path)
        else:
            backup_hash = calculate_file_hash(backup_path, use_cache=True)

        hash_time = time.time() - start_time

        if not backup_hash:
            print(f"❌ Could not calculate file hash")
            return jsonify({
                'success': True,
                'found': False,
                'message': 'Could not calculate file hash'
            })

        print(f"✓ Hash calculated in {hash_time:.2f}s")
        print(f"   Hash (first 12 chars): {backup_hash[:12]}...")

        # 2. Get expected home location
        expected_home_path = convert_backup_to_home_path(backup_path)
        print(f"   Expected home path: {expected_home_path}")

        # 3. Check database first
        def get_file_location(backup_path, file_hash=None):
            """Get the current home location for a backup file"""
            try:
                conn = sqlite3.connect(LOCATION_DB_PATH)
                cursor = conn.cursor()
        
                if file_hash:
                    cursor.execute('''
                        SELECT current_home_path FROM file_locations
                        WHERE (backup_path = ? OR file_hash = ?)
                        ORDER BY last_checked DESC LIMIT 1
                    ''', (backup_path, file_hash))
                else:
                    cursor.execute('''
                        SELECT current_home_path FROM file_locations
                        WHERE backup_path = ?
                        ORDER BY last_checked DESC LIMIT 1
                    ''', (backup_path,))
        
                result = cursor.fetchone()
                conn.close()
        
                if result: 
                    current_path = result[0]
                    # Verify the file still exists at this location
                    if os.path.exists(current_path):
                        return current_path
                    else:
                        # File moved again, remove stale entry
                        DatabaseManager.remove_file_location(backup_path)
                        return None
                return None
            except Exception as e:
                print(f"[Database] Error getting file location: {e}")
                return None
        current_location = get_file_location(backup_path, backup_hash)
        if current_location and os.path.exists(current_location):
            # Verify hash matches
            current_hash = calculate_fast_hash(current_location)
            if current_hash == backup_hash:
                print(f"✓ File found in database cache!")
                return jsonify({
                    'success': True,
                    'found': True,
                    'current_location': current_location,
                    'original_location': expected_home_path,
                    'search_method': 'database_cache',
                    'search_time': 0.0,
                    'hash_time': hash_time
                })

        def search_directory_by_hash(directory, target_hash, max_depth=3, current_depth=0):
            """Search directory for file matching target hash"""
            if current_depth > max_depth:
                return None
        
            try:
                for item in os.listdir(directory):
                    if item.startswith('.'):
                        continue
        
                    item_path = os.path.join(directory, item)
        
                    if os.path.isfile(item_path):
                        try:
                            # Skip very large files
                            if os.path.getsize(item_path) > 500 * 1024 * 1024:
                                continue
        
                            # Get hash (cached or calculated)
                            current_hash = get_cached_hash(item_path)
                            if not current_hash:
                                current_hash = calculate_fast_hash(item_path)
        
                            if current_hash and current_hash == target_hash:
                                return {
                                    'path': item_path,
                                    'hash': current_hash,
                                    'depth': current_depth
                                }
        
                        except (PermissionError, OSError):
                            continue
        
                    elif os.path.isdir(item_path) and current_depth < max_depth:
                        result = search_directory_by_hash(
                            item_path, target_hash, max_depth, current_depth + 1
                        )
                        if result:
                            return result
        
            except PermissionError:
                pass
        
            return None
        def find_file_by_hash(target_hash, backup_path):
            """Find file by hash in common locations"""
            if not target_hash:
                return None
        
            home_dir = os.path.expanduser("~")
            expected_home_path = convert_backup_to_home_path(backup_path)
            expected_dir = os.path.dirname(expected_home_path)
        
            # Search locations in priority order
            search_locations = []
        
            # 1. Check database first
            current_location = get_file_location(backup_path, target_hash)
            if current_location and os.path.exists(current_location):
                # Verify hash matches
                current_hash = calculate_fast_hash(current_location)
                if current_hash == target_hash:
                    return {
                        'path': current_location,
                        'hash': target_hash,
                        'found_in': 'database',
                        'source': 'cached_location'
                    }
        
            # 2. Expected directory
            if os.path.exists(expected_dir):
                search_locations.append({
                    'path': expected_dir,
                    'depth': 3,
                    'priority': 1
                })
        
            # 3. Common directories
            common_dirs = ['Desktop', 'Downloads', 'Documents', 'Pictures', 'Music', 'Videos']
            for dir_name in common_dirs:
                dir_path = os.path.join(home_dir, dir_name)
                if os.path.exists(dir_path):
                    search_locations.append({
                        'path': dir_path,
                        'depth': 2,
                        'priority': 2
                    })
        
            # 4. Home directory
            search_locations.append({
                'path': home_dir,
                'depth': 1,
                'priority': 3
            })
        
            # Sort by priority
            search_locations.sort(key=lambda x: x['priority'])
        
            # Search each location
            for location in search_locations:
                result = search_directory_by_hash(
                    location['path'],
                    target_hash,
                    max_depth=location['depth']
                )
        
                if result:
                    return {
                        'path': result['path'],
                        'hash': result['hash'],
                        'found_in': os.path.basename(location['path']),
                        'source': 'hash_search',
                        'depth': result['depth']
                    }
        
            return None
        def save_file_location(backup_path, original_home_path, current_home_path, file_hash):
            """Save or update the location of a file"""
            try:
                conn = sqlite3.connect(LOCATION_DB_PATH)
                cursor = conn.cursor()

                # Check if entry exists
                cursor.execute('SELECT id FROM file_locations WHERE backup_path = ?', (backup_path,))
                existing = cursor.fetchone()

                if existing:
                    # Update existing entry
                    cursor.execute('''
                        UPDATE file_locations
                        SET current_home_path = ?, file_hash = ?, last_checked = CURRENT_TIMESTAMP
                        WHERE backup_path = ?
                    ''', (current_home_path, file_hash, backup_path))
                else:
                    # Insert new entry
                    cursor.execute('''
                        INSERT INTO file_locations
                        (backup_path, original_home_path, current_home_path, file_hash)
                        VALUES (?, ?, ?, ?)
                    ''', (backup_path, original_home_path, current_home_path, file_hash))

                conn.commit()
                conn.close()
                print(f"[Database] Saved location for {os.path.basename(backup_path)}: {current_home_path}")
                return True
            except Exception as e:
                print(f"[Database] Error saving file location: {e}")
                return False

        # 4. Check if file exists at expected location
        if os.path.exists(expected_home_path):
            # Verify hash matches
            existing_hash = calculate_fast_hash(expected_home_path)
            if existing_hash == backup_hash:
                print(f"✓ File exists at expected location!")
                # Save to database
                save_file_location(backup_path, expected_home_path, expected_home_path, backup_hash)
                return jsonify({
                    'success': True,
                    'found': True,
                    'current_location': expected_home_path,
                    'original_location': expected_home_path,
                    'search_method': 'path',
                    'search_time': 0.0,
                    'hash_time': hash_time
                })

        # 5. Hash-based search
        print(f"📂 Starting hash-based search...")
        search_start = time.time()

        result = find_file_by_hash(backup_hash, backup_path)
        search_time = time.time() - search_start

        if result:
            print(f"\n✅ SEARCH SUCCESSFUL!")
            print(f"   Found file at: {result['path']}")
            print(f"   Found in: {result.get('found_in', 'unknown')}")

            # Save to database
            save_file_location(backup_path, expected_home_path, result['path'], backup_hash)

            return jsonify({
                'success': True,
                'found': True,
                'current_location': result['path'],
                'original_location': expected_home_path,
                'search_method': 'hash',
                'search_time': search_time,
                'hash_time': hash_time,
                'found_in': result.get('found_in', 'unknown'),
                'source': result.get('source', 'hash_search')
            })

        print(f"\n❌ SEARCH FAILED - File not found")

        return jsonify({
            'success': True,
            'found': False,
            'message': 'File not found in home directory',
            'search_time': search_time,
            'hash_time': hash_time
        })

    except Exception as e:
        app.logger.error(f"❌ Search error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


# =============================================================================
# ROUTES - DAEMON CONTROL
# =============================================================================
@app.route('/api/daemon/status', methods=['GET'])
def get_daemon_status():
    """Get daemon status."""
    try:
        # Try to get status from server object
        if hasattr(server, 'get_daemon_status'):
            status = server.get_daemon_status()
        else:
            # Fallback status
            status = check_daemon_ready()

        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        app.logger.error(f"Error getting daemon status: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'status': {'running': False, 'ready': False, 'error': str(e)}
        }), 500

@app.route('/api/daemon/start', methods=['POST'])
def start_daemon_process():
    """Start the backup daemon."""
    try:
        if hasattr(server, 'start_daemon'):
            result = server.start_daemon()
        else:
            result = {'success': False, 'error': 'Daemon start not implemented'}

        return jsonify(result), 200 if result.get('success') else 500
    except Exception as e:
        app.logger.error(f"Error starting daemon: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/daemon/ready-status', methods=['GET'])
def daemon_ready_status():
    """Check if daemon is ready."""
    try:
        status = check_daemon_ready()

        # Calculate startup progress if daemon is running but not ready
        startup_progress = None
        if status["daemon_running"] and not status["is_ready"]:
            app_name = getattr(server, 'APP_NAME', 'timemachine').lower()
            lock_file = os.path.join(os.path.expanduser("~"), f'.{app_name}_daemon.lock')
            if os.path.exists(lock_file):
                file_age = time.time() - os.path.getmtime(lock_file)
                startup_progress = min(90, int(file_age))

        return jsonify({
            "success": True,
            "ready": status["is_ready"],
            "running": status["daemon_running"],
            "status": status,
            "startup_progress": startup_progress,
            "message": (
                "Daemon is ready" if status["is_ready"] else
                "Daemon is starting up..." if status["daemon_running"] else
                "Daemon is not running"
            )
        })
    except Exception as e:
        app.logger.error(f"Error checking daemon ready status: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "ready": False,
            "running": False
        }), 500

@app.route('/api/backup/cancel', methods=['POST'])
def cancel_backup_task():
    """Cancel backup task."""
    try:
        data = request.get_json(silent=True) or {}
        mode = data.get('mode', 'graceful')

        if hasattr(send_control_command, '__call__'):
            ok = send_control_command('cancel', mode)
        else:
            ok = False

        return jsonify({'result': 'ok' if ok else 'error', 'mode': mode}), (200 if ok else 500)
    except Exception as e:
        app.logger.error(f"Error canceling backup: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# =============================================================================
# WEB SOCKET ENDPOINTS
# =============================================================================
@sock.route('/ws/transfers-feed')
def transfers_feed_websocket(ws):
    """WebSocket endpoint for live transfer updates."""
    ws_clients.append(ws)

    try:
        while True:
            try:
                data = ws.receive(timeout=None)
                if data is None:
                    break
            except Exception:
                break
    except Exception as e:
        app.logger.error(f"WebSocket error: {e}")
    finally:
        try:
            ws_clients.remove(ws)
        except ValueError:
            pass

# =============================================================================
# UTILITY ROUTES
# =============================================================================
@app.route('/api/base-folders-creation')
def create_necessaries_folders():
    """Create necessary application folders."""
    try:
        if base_folders_creation():
            return jsonify({'success': True, 'message': 'Created necessary folders!'})
        return jsonify({'success': False, 'message': 'Folder creation failed.'})
    except Exception as e:
        app.logger.error(f"Error creating folders: {e}")
        return jsonify({
            'success': False,
            'message': 'Error creating folders',
            'error': str(e)
        })

@app.route('/api/username')
def get_username():
    """Get current username."""
    try:
        username = os.path.basename(os.path.expanduser("~"))
        return jsonify({'username': username})
    except Exception as e:
        app.logger.error(f"Error getting username: {e}")
        return jsonify({'username': 'user'})

# Get backup folders and display in User Data (System Restore)
@app.route('/api/search/folder', methods=['GET'])
def get_folder_contents():
    """Get folder contents (files and directories) from the backup directory."""
    path = request.args.get('path', '').strip()

    try:
        backup_dir = server.app_main_backup_dir()
        
        # Get the name of the backup directory for comparison (e.g., '.main_backup' or 'Backups')
        backup_dir_name = os.path.basename(os.path.realpath(backup_dir))

        # If the path is empty, a single slash, or the name of the backup directory,
        # treat it as the root directory request.
        if not path or path == '/' or path == backup_dir_name:
            full_path = backup_dir
        elif path == backup_dir:
            full_path = backup_dir
        else:
            # Otherwise, assume it's a subdirectory relative to the backup root
            full_path = os.path.join(backup_dir, path.lstrip('/'))
        
        if not os.path.isdir(backup_dir):
            return jsonify({
                'success': False,
                'error': f'Backup directory not found: {backup_dir}',
                'items': []
            }), 404

        real_path = os.path.realpath(full_path)
        real_backup = os.path.realpath(backup_dir)
        
        if not real_path.startswith(real_backup):
            return jsonify({
                'success': False,
                'error': 'Invalid path',
                'items': []
            }), 403

        if not os.path.isdir(real_path):
            return jsonify({
                'success': False,
                'error': f'Directory not found: {path}',
                'items': []
            }), 404

        items = []
        try:
            for entry in os.scandir(real_path):
                item = {
                    'name': entry.name,
                    'type': 'folder' if entry.is_dir(follow_symlinks=False) else 'file',
                    'path': entry.path
                }

                if item['type'] == 'file':
                    item['icon'] = 'bi-file-earmark-fill'
                    item['color'] = 'text-gray-500'

                items.append(item)
        except PermissionError:
            return jsonify({
                'success': False,
                'error': 'Permission denied accessing directory',
                'items': []
            }), 403

        return jsonify({
            'success': True,
            'items': items,
            'path': path or '/'
        })

    except Exception as e:
        app.logger.error(f"Error getting folder contents: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e),
            'items': []
        }), 500

@app.route('/api/file-versions', methods=['GET'])
def get_file_versions():
    file_path_requested = request.args.get('file_path')
    if not file_path_requested:
        return jsonify({'success': False, 'error': 'Missing file_path'}), 400

    versions: list = []
    try:
        app.logger.debug(f"File versions lookup requested for: {file_path_requested}")

        home_abs_path = os.path.abspath(USERS_HOME)
        main_backup_abs_path = os.path.abspath(server.app_main_backup_dir())
        incremental_base_path = os.path.abspath(server.app_backup_dir())

        rel_path = None
        file_abs_path = os.path.abspath(file_path_requested)

        if file_abs_path.startswith(main_backup_abs_path):
            rel_path = os.path.relpath(file_abs_path, main_backup_abs_path)
        elif file_abs_path.startswith(incremental_base_path):
            temp_rel = os.path.relpath(file_abs_path, incremental_base_path)
            parts = temp_rel.split(os.sep)
            if len(parts) >= 3:
                rel_path = os.path.join(*parts[2:])
            else:
                rel_path = parts[-1] if parts else ""
        elif file_abs_path.startswith(home_abs_path):
            rel_path = os.path.relpath(file_abs_path, home_abs_path)
        else:
            rel_path = file_path_requested

        if not rel_path:
            return jsonify({'success': False, 'error': 'Could not determine file path'}), 400

        # 1) Main backup version
        main_backup_file = os.path.join(main_backup_abs_path, rel_path)
        if os.path.exists(main_backup_file):
            stat = os.stat(main_backup_file)
            versions.append({
                'key': 'main',
                'time': 'Main Backup',
                'path': main_backup_file,
                'size': stat.st_size,
                'mtime': stat.st_mtime
            })

        # 2) Incremental backups
        if os.path.exists(incremental_base_path):
            for date_folder in sorted(os.listdir(incremental_base_path), reverse=True):
                date_path = os.path.join(incremental_base_path, date_folder)
                if not os.path.isdir(date_path):
                    continue
                for time_folder in sorted(os.listdir(date_path), reverse=True):
                    time_path = os.path.join(date_path, time_folder)
                    if not os.path.isdir(time_path):
                        continue
                    backup_file = os.path.join(time_path, rel_path)
                    if os.path.exists(backup_file):
                        stat = os.stat(backup_file)
                        versions.append({
                            'key': f"{date_folder}_{time_folder}",
                            'time': f"{date_folder} {time_folder.replace('_', ':')}",
                            'path': backup_file,
                            'size': stat.st_size,
                            'mtime': stat.st_mtime
                        })

        versions.sort(key=lambda x: x.get('mtime', 0), reverse=True)
        app.logger.debug(f"Restults: {versions}")
        
        for v in versions:
            v.pop('mtime', None)

        return jsonify({'success': True, 'versions': versions}), 200

    except Exception as e:
        app.logger.error(f"Error in get_file_versions: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/open-location', methods=['POST'])
def open_location():
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        file_path = os.path.dirname(file_path)

        if not file_path:
            return jsonify({'success': False, 'error': 'No file_path provided'}), 400

        if os.name == 'nt':
            os.startfile(file_path)
        elif os.uname().sysname == 'Darwin':
            sub.run(['open', file_path])
        else:
            sub.run(['xdg-open', file_path])

        return jsonify({'success': True, 'message': f'Attempted to open folder: {file_path}'}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/open-file', methods=['POST'])
def open_file():
    try:
        data = request.get_json()
        file_path = data.get('file_path')

        if not file_path:
            return jsonify({'success': False, 'error': 'No file_path provided'}), 400

        if os.name == 'nt':
            os.startfile(file_path)
        elif os.uname().sysname == 'Darwin':
            sub.run(['open', file_path])
        else:
            sub.run(['xdg-open', file_path])

        return jsonify({'success': True, 'message': f'Attempted to open file: {file_path}'}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# =============================================================================
# ERROR HANDLING
# =============================================================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {error}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500



# =============================================================================
# DEVICES LOGICS
# =============================================================================
def get_available_devices():
    """
    Get available storage devices across Linux, Windows, and macOS.
    Returns a list of dictionaries with device information.
    """
    system = platform.system().lower()
    
    if system == 'linux':
        return _get_linux_devices()
    elif system == 'windows':
        return _get_windows_devices()
    elif system == 'darwin':  # macOS
        return _get_mac_devices()
    else:
        return []

def _get_linux_devices():
    """Get storage devices on Linux using /proc/mounts and df command"""
    devices = []
    
    try:
        import psutil
        
        # Get all mounted partitions
        partitions = psutil.disk_partitions(all=False)
        
        for partition in partitions:
            try:
                # Skip system mounts and virtual filesystems
                skip_mounts = [
                    '/proc', '/sys', '/dev', '/run', '/snap',
                    '/sys/kernel', '/dev/shm', '/proc/sys',
                    '/sys/fs', '/sys/firmware'
                ]
                
                if any(partition.mountpoint.startswith(m) for m in skip_mounts):
                    continue
                    
                # Get usage statistics
                usage = psutil.disk_usage(partition.mountpoint)
                
                # Get device details
                device_name = partition.device
                if device_name.startswith('/dev/'):
                    device_name = device_name[5:]
                
                # Try to get label
                label = _get_linux_label(partition.mountpoint)
                
                # Determine if SSD (check via /sys/block)
                is_ssd = _is_ssd_linux(partition.device)
                
                # Get filesystem
                filesystem = partition.fstype if partition.fstype else 'unknown'
                
                # Calculate used space (total - free)
                used = usage.total - usage.free
                
                devices.append({
                    'id': partition.device.replace('/', '_'),
                    'name': label if label else device_name,
                    'label': label if label else f"Drive {device_name}",
                    'device': partition.device,
                    'mount_point': partition.mountpoint,
                    'filesystem': filesystem,
                    'total': usage.total,
                    'used': used,
                    'free': usage.free,
                    'total_GB': round(usage.total / (1024**3), 1),
                    'used_GB': round(used / (1024**3), 1),
                    'free_GB': round(usage.free / (1024**3), 1),
                    'is_ssd': is_ssd,
                    'is_removable': _is_removable_linux(partition.device),
                    'is_system': partition.mountpoint == '/',
                    'percent_used': round((used / usage.total) * 100, 1) if usage.total > 0 else 0
                })
                
            except (PermissionError, OSError, psutil.AccessDenied):
                continue  # Skip devices we can't access
                
    except ImportError:
        # Fallback without psutil using df command
        try:
            import subprocess
            result = subprocess.run(['df', '-hT'], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 7:
                    device = parts[0]
                    filesystem = parts[1]
                    total_str = parts[2]
                    used_str = parts[3]
                    available_str = parts[4]
                    percent_used = parts[5]
                    mount_point = parts[6]
                    
                    # Skip system mounts
                    if mount_point in ['/dev', '/proc', '/sys', '/run', '/snap']:
                        continue
                    
                    # Parse sizes (convert from human-readable)
                    total = _parse_size_linux(total_str)
                    free = _parse_size_linux(available_str)
                    used = _parse_size_linux(used_str)
                    
                    devices.append({
                        'id': device.replace('/', '_'),
                        'name': f"Drive on {mount_point}",
                        'label': f"Drive on {mount_point}",
                        'device': device,
                        'mount_point': mount_point,
                        'filesystem': filesystem,
                        'total': total,
                        'used': used,
                        'free': free,
                        'total_GB': round(total / (1024**3), 1),
                        'used_GB': round(used / (1024**3), 1),
                        'free_GB': round(free / (1024**3), 1),
                        'is_ssd': False,  # Can't determine without psutil
                        'is_removable': _is_removable_linux(device),
                        'is_system': mount_point == '/',
                        'percent_used': int(percent_used.replace('%', ''))
                    })
                    
        except Exception as e:
            print(f"Error getting Linux devices: {e}")
    
    return devices

def _get_windows_devices():
    """Get storage devices on Windows using wmi or psutil"""
    devices = []
    
    try:
        import psutil
        
        partitions = psutil.disk_partitions(all=False)
        
        for partition in partitions:
            try:
                # Skip CD-ROM drives and network drives for backup purposes
                if partition.opts == 'cdrom' or 'removable' in partition.opts:
                    continue
                    
                # Get usage
                usage = psutil.disk_usage(partition.mountpoint)
                
                # Calculate used space
                used = usage.total - usage.free
                
                # Get drive letter and label
                drive_letter = partition.device.replace(':', '')
                label = _get_windows_label(drive_letter)
                
                # Determine if SSD (requires wmi)
                is_ssd = _is_ssd_windows(drive_letter)
                
                devices.append({
                    'id': f"drive_{drive_letter}",
                    'name': label if label else f"Local Disk ({drive_letter}:)",
                    'label': label if label else f"Drive {drive_letter}:",
                    'device': partition.device,
                    'mount_point': partition.mountpoint,
                    'filesystem': partition.fstype if partition.fstype else 'NTFS',
                    'total': usage.total,
                    'used': used,
                    'free': usage.free,
                    'total_GB': round(usage.total / (1024**3), 1),
                    'used_GB': round(used / (1024**3), 1),
                    'free_GB': round(usage.free / (1024**3), 1),
                    'is_ssd': is_ssd,
                    'is_removable': 'removable' in partition.opts,
                    'is_system': partition.mountpoint == 'C:\\',
                    'percent_used': round((used / usage.total) * 100, 1) if usage.total > 0 else 0
                })
                
            except (PermissionError, OSError, psutil.AccessDenied):
                continue
                
    except ImportError:
        # Fallback using wmic command
        try:
            import subprocess
            result = subprocess.run(
                ['wmic', 'logicaldisk', 'get', 'size,freespace,caption,volumename,drivetype,filesystem'],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 6:
                    drive = parts[0]
                    drive_type = int(parts[1])
                    filesystem = parts[2]
                    free_space = int(parts[3]) if parts[3].isdigit() else 0
                    size = int(parts[4]) if parts[4].isdigit() else 0
                    volume_name = ' '.join(parts[5:]) if len(parts) > 5 else ''
                    
                    # Skip network drives (type=4) and CD-ROM (type=5)
                    if drive_type in [4, 5]:
                        continue
                    
                    used = size - free_space if size > 0 else 0
                    
                    devices.append({
                        'id': f"drive_{drive.replace(':', '')}",
                        'name': volume_name if volume_name else f"Local Disk ({drive})",
                        'label': volume_name if volume_name else f"Drive {drive}",
                        'device': drive,
                        'mount_point': f"{drive}\\",
                        'filesystem': filesystem,
                        'total': size,
                        'used': used,
                        'free': free_space,
                        'total_GB': round(size / (1024**3), 1),
                        'used_GB': round(used / (1024**3), 1),
                        'free_GB': round(free_space / (1024**3), 1),
                        'is_ssd': False,  # Can't determine without WMI
                        'is_removable': drive_type == 2,  # Removable disk
                        'is_system': drive == 'C:',
                        'percent_used': round((used / size) * 100, 1) if size > 0 else 0
                    })
                    
        except Exception as e:
            print(f"Error getting Windows devices: {e}")
    
    return devices

def _get_mac_devices():
    """Get storage devices on macOS using diskutil and psutil"""
    devices = []
    
    try:
        import psutil
        
        partitions = psutil.disk_partitions(all=False)
        
        for partition in partition:
            try:
                # Skip system mounts
                skip_mounts = [
                    '/dev', '/proc', '/sys', '/Volumes/Recovery',
                    '/private/var/vm', '/Network'
                ]
                
                if any(partition.mountpoint.startswith(m) for m in skip_mounts):
                    continue
                    
                # Get usage
                usage = psutil.disk_usage(partition.mountpoint)
                used = usage.total - usage.free
                
                # Get device name from mount point
                device_name = os.path.basename(partition.mountpoint)
                
                # Get label (volume name)
                label = _get_mac_label(partition.mountpoint)
                
                # Determine if SSD
                is_ssd = _is_ssd_mac(partition.device)
                
                devices.append({
                    'id': partition.device.replace('/', '_'),
                    'name': label if label else device_name,
                    'label': label if label else f"Disk {device_name}",
                    'device': partition.device,
                    'mount_point': partition.mountpoint,
                    'filesystem': partition.fstype if partition.fstype else 'apfs',
                    'total': usage.total,
                    'used': used,
                    'free': usage.free,
                    'total_GB': round(usage.total / (1024**3), 1),
                    'used_GB': round(used / (1024**3), 1),
                    'free_GB': round(usage.free / (1024**3), 1),
                    'is_ssd': is_ssd,
                    'is_removable': _is_removable_mac(partition.mountpoint),
                    'is_system': partition.mountpoint == '/',
                    'percent_used': round((used / usage.total) * 100, 1) if usage.total > 0 else 0
                })
                
            except (PermissionError, OSError, psutil.AccessDenied):
                continue
                
    except ImportError:
        # Fallback using diskutil command
        try:
            import subprocess
            import plistlib
            
            # Get disk info in plist format
            result = subprocess.run(
                ['diskutil', 'list', '-plist'],
                capture_output=True, text=False, check=True
            )
            
            # Parse plist
            disk_info = plistlib.loads(result.stdout)
            
            for disk in disk_info.get('AllDisksAndPartitions', []):
                # Skip disk images and recovery partitions
                if disk.get('Content', '') == 'Apple_APFS_Recovery':
                    continue
                    
                for partition in disk.get('Partitions', []):
                    mount_point = partition.get('MountPoint', '')
                    if not mount_point:
                        continue
                        
                    # Get volume name
                    volume_name = partition.get('VolumeName', 'Untitled')
                    
                    # Get size
                    size = partition.get('Size', 0)
                    
                    # Get free space using df
                    try:
                        df_result = subprocess.run(
                            ['df', mount_point],
                            capture_output=True, text=True, check=True
                        )
                        df_lines = df_result.stdout.strip().split('\n')
                        if len(df_lines) > 1:
                            parts = df_lines[1].split()
                            if len(parts) >= 4:
                                total_blocks = int(parts[1]) * 512  # Convert 512-byte blocks
                                free_blocks = int(parts[3]) * 512
                                used = total_blocks - free_blocks
                            else:
                                used = size * 0.5  # Estimate
                                free_blocks = size * 0.5
                        else:
                            used = size * 0.5
                            free_blocks = size * 0.5
                    except:
                        used = size * 0.5
                        free_blocks = size * 0.5
                    
                    devices.append({
                        'id': partition.get('DeviceIdentifier', 'unknown'),
                        'name': volume_name,
                        'label': volume_name,
                        'device': f"/dev/{partition.get('DeviceIdentifier', '')}",
                        'mount_point': mount_point,
                        'filesystem': partition.get('FilesystemType', 'apfs'),
                        'total': size,
                        'used': used,
                        'free': free_blocks,
                        'total_GB': round(size / (1024**3), 1),
                        'used_GB': round(used / (1024**3), 1),
                        'free_GB': round(free_blocks / (1024**3), 1),
                        'is_ssd': 'Solid State' in str(disk.get('MediaType', '')),
                        'is_removable': disk.get('RemovableMedia', False),
                        'is_system': mount_point == '/',
                        'percent_used': round((used / size) * 100, 1) if size > 0 else 0
                    })
                    
        except Exception as e:
            print(f"Error getting macOS devices: {e}")

    return devices

# Helper functions for Linux
def _get_linux_label(mount_point):
    """Get volume label on Linux"""
    try:
        import subprocess
        # Try to get label from blkid
        result = subprocess.run(
            ['blkid', '-o', 'value', '-s', 'LABEL', mount_point],
            capture_output=True, text=True
        )
        label = result.stdout.strip()
        if label:
            return label
            
        # Try to get from /etc/mtab or mount
        result = subprocess.run(
            ['mount'],
            capture_output=True, text=True
        )
        lines = result.stdout.split('\n')
        for line in lines:
            if mount_point in line and ' on ' in line:
                parts = line.split(' on ')
                if len(parts) > 1:
                    device_part = parts[0]
                    # Extract label if present in brackets
                    if '[' in device_part and ']' in device_part:
                        start = device_part.find('[') + 1
                        end = device_part.find(']')
                        return device_part[start:end]
    except:
        pass
    return None

def _is_ssd_linux(device_path):
    """Check if device is SSD on Linux"""
    try:
        import subprocess
        
        # Extract device name (e.g., /dev/sda -> sda)
        device_name = os.path.basename(device_path)
        # Remove partition numbers
        if device_name[-1].isdigit():
            base_device = ''.join([c for c in device_name if not c.isdigit()])
        else:
            base_device = device_name
            
        # Check /sys/block/DEVICE/queue/rotational
        rotational_path = f"/sys/block/{base_device}/queue/rotational"
        if os.path.exists(rotational_path):
            with open(rotational_path, 'r') as f:
                rotational = f.read().strip()
                return rotational == '0'  # 0 = SSD, 1 = HDD
                
        # Alternative: use lsblk
        result = subprocess.run(
            ['lsblk', '-d', '-o', 'name,rota'],
            capture_output=True, text=True
        )
        lines = result.stdout.split('\n')
        for line in lines:
            if base_device in line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1] == '0'
                    
    except:
        pass
    return False

def _is_removable_linux(device_path):
    """Check if device is removable on Linux"""
    try:
        import subprocess
        
        device_name = os.path.basename(device_path)
        base_device = ''.join([c for c in device_name if not c.isdigit()])
        
        # Check /sys/block/DEVICE/removable
        removable_path = f"/sys/block/{base_device}/removable"
        if os.path.exists(removable_path):
            with open(removable_path, 'r') as f:
                removable = f.read().strip()
                return removable == '1'
    except:
        pass
    return False

def _parse_size_linux(size_str: str):
    """Parse human-readable size string to bytes"""
    size_str = size_str.upper()
    if 'G' in size_str:
        return int(float(size_str.replace('G', '')) * (1024**3))
    elif 'M' in size_str:
        return int(float(size_str.replace('M', '')) * (1024**2))
    elif 'K' in size_str:
        return int(float(size_str.replace('K', '')) * 1024)
    elif 'T' in size_str:
        return int(float(size_str.replace('T', '')) * (1024**4))
    else:
        try:
            return int(size_str)
        except:
            return 0

# Helper functions for Windows
def _get_windows_label(drive_letter):
    """Get volume label on Windows"""
    try:
        import ctypes
        import string
        
        # Get volume information
        volume_name_buffer = ctypes.create_unicode_buffer(1024)
        file_system_name_buffer = ctypes.create_unicode_buffer(1024)
        
        success = ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(f"{drive_letter}:\\"),
            volume_name_buffer,
            ctypes.sizeof(volume_name_buffer),
            None,
            None,
            None,
            file_system_name_buffer,
            ctypes.sizeof(file_system_name_buffer)
        )
        
        if success:
            return volume_name_buffer.value
    except:
        pass
    return None

def _is_ssd_windows(drive_letter):
    """Check if drive is SSD on Windows using WMI"""
    try:
        import wmi
        c = wmi.WMI()
        
        # Get drive by letter
        for disk in c.Win32_LogicalDisk(DeviceID=f"{drive_letter}:"):
            # Get physical disk
            for partition in c.Win32_DiskPartition(DeviceID=disk.DeviceID):
                for physical_disk in c.Win32_DiskDrive(Index=partition.DiskIndex):
                    # Check MediaType for SSD
                    media_type = getattr(physical_disk, 'MediaType', '')
                    if 'SSD' in media_type.upper() or 'Solid State' in media_type:
                        return True
                    
                    # Alternative: check rotational speed
                    if hasattr(physical_disk, 'BytesPerSector'):
                        # SSDs often report 0 or very high RPM
                        if hasattr(physical_disk, 'SCSIBus'):
                            return False  # This is heuristic
    except:
        # Fallback: check if it's likely SSD based on size and name
        try:
            import psutil
            usage = psutil.disk_usage(f"{drive_letter}:\\")
            # Very large drives are more likely HDDs
            return usage.total < 2 * (1024**4)  # Less than 2TB
        except:
            pass
    return False

# Helper functions for macOS
def _get_mac_label(mount_point):
    """Get volume label on macOS"""
    try:
        import subprocess
        result = subprocess.run(
            ['diskutil', 'info', mount_point],
            capture_output=True, text=True
        )
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Volume Name:' in line:
                return line.split(':')[1].strip()
    except:
        pass
    return os.path.basename(mount_point)

def _is_ssd_mac(device_path):
    """Check if device is SSD on macOS"""
    try:
        import subprocess
        # Use diskutil to check media type
        result = subprocess.run(
            ['diskutil', 'info', device_path],
            capture_output=True, text=True
        )
        output = result.stdout
        return 'Solid State' in output or 'SSD' in output
    except:
        return False

def _is_removable_mac(mount_point):
    """Check if device is removable on macOS"""
    try:
        import subprocess
        result = subprocess.run(
            ['diskutil', 'info', mount_point],
            capture_output=True, text=True
        )
        output = result.stdout
        return 'Removable Media' in output or 'External' in output
    except:
        return False

# Flask API endpoint example
@app.route('/api/storage/devices')
def get_storage_devices():
    """API endpoint to get available storage devices"""
    try:
        devices = get_available_devices()
        return jsonify({
            'success': True,
            'devices': devices,
            'count': len(devices),
            'platform': platform.system(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'devices': [],
            'count': 0
        })

# For migration sources specifically (checking for Time Machine backup)
@app.route('/api/migration/sources')
def get_migration_sources():
    """Get devices that have Time Machine backup structure (server.MAIN_BACKUP_LOCATION folder)"""
    try:
        sources = []
        devices = get_available_devices()
        
        for device in devices:
            mount_point = device['mount_point']

            # Check for server.MAIN_BACKUP_LOCATION folder
            backup_path: str = server.app_main_backup_dir()
            backup_path = os.path.join(
                mount_point, 
                server.APP_NAME_CLOSE_LOWER, 
                server.BACKUPS_LOCATION_DIR_NAME, 
                server.MAIN_BACKUP_LOCATION)
            
            if os.path.exists(backup_path):
                # Check if it has actual backup data
                has_backup = _check_backup_data(backup_path)
                if has_backup:
                    device['has_backup'] = True
                    device['backup_path'] = backup_path
                    device['backup_type'] = 'time_machine'
                    sources.append(device)
        
        return jsonify({
            'success': True,
            'sources': sources,
            'count': len(sources)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def _check_backup_data(backup_path):
    """Check if backup folder has actual data"""
    try:
        # Check if there's at least some backup data
        if os.path.exists(backup_path):
            # Check if there are files in main backup
            try:
                items = os.listdir(backup_path)
                return len(items) > 0
            except:
                return False
        
        return False
    except:
        return False

# =============================================================================
# SIZES LOGICS
# =============================================================================
@app.route('/api/backup/total-size')
def get_backup_total_size():
    """
    Calculate total size of user data in .main_backup folder
    Returns size in bytes and human-readable format
    """
    try:
        # Ensure .main_backup folder exists
        backup_root: str = server.app_main_backup_dir()
        if not os.path.exists(backup_root):
            return {'success': False, 'error': 'No .main_backup folder found'}
        
        # Calculate total size
        total_bytes = _calculate_backup_size(backup_root)
        
        return {
            'success': True,
            'total_bytes': total_bytes,
            'human_readable': _format_bytes(total_bytes),
            'backup_path': backup_root,
            'calculated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def _calculate_backup_size(path):
    """Calculate total size of backup data"""
    total = 0
    try:
        # Walk through all files in backup
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Get file size
                    total += os.path.getsize(file_path)
                except (OSError, PermissionError):
                    continue
        
        return total
        
    except Exception as e:
        raise e

def _format_bytes(bytes_size):
    """Format bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} EB"

# Alternative: Faster method using du command (Linux/Mac)
def _calculate_backup_size_fast(path):
    """Faster backup size calculation using system commands"""
    system = platform.system().lower()
    
    try:
        if system in ['linux', 'darwin']:  # Linux or macOS
            import subprocess
            # Use du command for faster calculation
            result = subprocess.run(
                ['du', '-sb', path],
                capture_output=True,
                text=True,
                check=True
            )
            # du output: "size_in_bytes\tpath"
            size_str = result.stdout.strip().split('\t')[0]
            return int(size_str)
            
        elif system == 'windows':
            import subprocess
            # PowerShell command for Windows
            ps_command = f"""
            $total = 0
            Get-ChildItem -Path "{path}" -Recurse -File | 
            ForEach-Object {{ $total += $_.Length }}
            $total
            """
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                shell=True
            )
            return int(result.stdout.strip())
            
        else:
            # Fallback to Python walk
            return _calculate_backup_size(path)
            
    except Exception:
        # Fallback to Python method
        return _calculate_backup_size(path)


# =============================================================================
# FOLDER RESTORATION LOGIC
# =============================================================================
# NEW
def reconstruct_folder_from_backups(folder_path, target_date=None, target_time=None, destination=None):
    """
    Reconstruct folder state from backups up to target datetime.
    """
    try:
        app.logger.info(f"Reconstructing folder: {folder_path}, date: {target_date}, time: {target_time}")

        # 1. Get backup directories
        main_backup_dir = server.app_main_backup_dir()
        incremental_base = server.app_backup_dir()

        # 2. Determine destination
        if not destination:
            home_dir = os.path.expanduser("~")
            folder_name = os.path.basename(folder_path.rstrip('/'))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            destination = os.path.join(home_dir, f"restored_{folder_name}_{timestamp}")

        os.makedirs(destination, exist_ok=True)

        # 3. Get all file versions up to target time
        folder_files = find_all_files_in_folder(folder_path, main_backup_dir, incremental_base)

        if not folder_files:
            app.logger.warning(f"No files found for folder: {folder_path}")
            return False

        # 4. For each file, find appropriate version
        restored_count = 0
        total_files = len(folder_files)

        app.logger.info(f"Found {total_files} files to restore")

        for idx, rel_file_path in enumerate(folder_files):
            if idx % 10 == 0:
                app.logger.info(f"Restoring files: {idx}/{total_files}")

            # Find the right version of this file
            file_version = find_file_version_for_datetime(
                rel_file_path,
                main_backup_dir,
                incremental_base,
                target_date,
                target_time
            )

            if file_version and os.path.exists(file_version):
                # Restore this file
                if restore_file_version(file_version, destination, main_backup_dir):
                    restored_count += 1
                else:
                    app.logger.warning(f"Failed to restore: {rel_file_path}")
            else:
                app.logger.warning(f"Version not found for: {rel_file_path}")

        app.logger.info(f"Restored {restored_count}/{total_files} files to {destination}")

        # 5. Open restored location
        open_restored_location(destination)

        return True

    except Exception as e:
        app.logger.error(f"Error reconstructing folder: {e}", exc_info=True)
        return False


def find_all_files_in_folder(folder_path, main_backup_dir, incremental_base):
    """
    Find all files that ever existed in this folder across all backups.
    Returns list of relative paths.
    """
    all_files = set()

    # 1. Check main backup
    main_folder_path = os.path.join(main_backup_dir, folder_path)
    if os.path.exists(main_folder_path):
        for root, dirs, files in os.walk(main_folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, main_backup_dir)
                all_files.add(rel_path)

    # 2. Check all incremental backups
    if os.path.exists(incremental_base):
        # Walk through all date/time folders
        for date_folder in os.listdir(incremental_base):
            date_path = os.path.join(incremental_base, date_folder)
            if not os.path.isdir(date_path):
                continue

            for time_folder in os.listdir(date_path):
                time_path = os.path.join(date_path, time_folder)
                if not os.path.isdir(time_path):
                    continue

                # Check if this incremental has our folder
                inc_folder_path = os.path.join(time_path, folder_path)
                if os.path.exists(inc_folder_path):
                    for root, dirs, files in os.walk(inc_folder_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            # Get path relative to this incremental backup
                            rel_to_inc = os.path.relpath(full_path, time_path)
                            all_files.add(rel_to_inc)

    return list(all_files)

# NEW
def find_file_version_for_datetime(rel_file_path, main_backup_dir, incremental_base, target_date=None, target_time=None):
    """
    Find file version for specific datetime.
    Uses folder timestamps (not file mtimes).
    """
    app.logger.info(f"Looking for {rel_file_path} at {target_date} {target_time}")

    # If no target, use latest
    if not target_date:
        # Find latest incremental
        if os.path.exists(incremental_base):
            all_backups = []
            for date_folder in os.listdir(incremental_base):
                if date_folder.startswith('.'):
                    continue

                date_path = os.path.join(incremental_base, date_folder)
                if not os.path.isdir(date_path):
                    continue

                for time_folder in os.listdir(date_path):
                    time_path = os.path.join(date_path, time_folder)
                    inc_file = os.path.join(time_path, rel_file_path)

                    if os.path.exists(inc_file):
                        try:
                            # Parse folder timestamp
                            day, month, year = map(int, date_folder.split('-'))
                            hour, minute = map(int, time_folder.split('-'))
                            dt = datetime(year, month, day, hour, minute)
                            all_backups.append((dt.timestamp(), inc_file))
                        except:
                            continue

            if all_backups:
                # Return newest
                all_backups.sort(reverse=True)
                return all_backups[0][1]

        # Fallback to main backup
        main_file = os.path.join(main_backup_dir, rel_file_path)
        if os.path.exists(main_file):
            return main_file
        return None

    # We have target date/time - parse it
    try:
        target_day, target_month, target_year = map(int, target_date.split('-'))
        target_hour, target_minute = map(int, target_time.split('-'))
        target_dt = datetime(target_year, target_month, target_day, target_hour, target_minute)
        target_timestamp = target_dt.timestamp()
    except:
        app.logger.error(f"Invalid target date/time: {target_date} {target_time}")
        return None

    # Start with main backup
    main_file = os.path.join(main_backup_dir, rel_file_path)
    best_version = main_file if os.path.exists(main_file) else None
    best_timestamp = 0

    # Check all incrementals
    if os.path.exists(incremental_base):
        for date_folder in os.listdir(incremental_base):
            if date_folder.startswith('.'):
                continue

            try:
                day, month, year = map(int, date_folder.split('-'))
            except:
                continue

            date_path = os.path.join(incremental_base, date_folder)

            for time_folder in os.listdir(date_path):
                try:
                    hour, minute = map(int, time_folder.split('-'))
                except:
                    continue

                time_path = os.path.join(date_path, time_folder)
                inc_file = os.path.join(time_path, rel_file_path)

                if os.path.exists(inc_file):
                    # Calculate backup timestamp from folder names
                    backup_dt = datetime(year, month, day, hour, minute)
                    backup_timestamp = backup_dt.timestamp()

                    app.logger.debug(f"Found backup at {backup_dt}, timestamp: {backup_timestamp}, target: {target_timestamp}")

                    # Check if this backup is at or before target AND newer than current best
                    if backup_timestamp <= target_timestamp and backup_timestamp > best_timestamp:
                        best_version = inc_file
                        best_timestamp = backup_timestamp
                        app.logger.debug(f"New best: {best_version}")

    app.logger.info(f"Selected version: {best_version}")
    return best_version


# NEW
def get_all_incremental_versions_fixed(rel_file_path, incremental_base):
    """Use FOLDER timestamps, not file mtime."""
    versions = []

    if not os.path.exists(incremental_base):
        return versions

    for date_folder in os.listdir(incremental_base):
        date_path = os.path.join(incremental_base, date_folder)
        if not os.path.isdir(date_path):
            continue

        # Parse date from folder name
        try:
            day, month, year = map(int, date_folder.split('-'))
        except:
            continue

        for time_folder in os.listdir(date_path):
            time_path = os.path.join(date_path, time_folder)
            if not os.path.isdir(time_path):
                continue

            # Check if file exists
            inc_file_path = os.path.join(time_path, rel_file_path)
            if os.path.exists(inc_file_path):
                # Parse time from FOLDER NAME (not file mtime)
                try:
                    hour, minute = map(int, time_folder.split('-'))
                    # Create datetime from folder name
                    folder_dt = datetime(year, month, day, hour, minute)
                    folder_timestamp = folder_dt.timestamp()

                    versions.append((inc_file_path, folder_timestamp))
                except:
                    continue

    # Sort by folder timestamp
    versions.sort(key=lambda x: x[1])
    return versions

def restore_file_version(source_path, destination_root, main_backup_dir):
    """
    Copy a single file version to destination.
    """
    try:
        # Determine relative path
        if '.main_backup' in source_path or source_path.startswith(main_backup_dir):
            # From main backup
            rel_path = os.path.relpath(source_path, main_backup_dir)
        else:
            # From incremental backup
            # Extract path after the time folder
            parts = source_path.split(os.sep)
            # Find the time folder (pattern: HH-MM)
            for i, part in enumerate(parts):
                if '-' in part and len(part) == 5 and part[2] == '-':
                    # Found time folder, everything after is the relative path
                    rel_path = os.sep.join(parts[i+1:])
                    break
            else:
                # Fallback: use the last part
                rel_path = os.path.basename(source_path)

        dest_path = os.path.join(destination_root, rel_path)

        # Create destination directory
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Copy file with metadata
        shutil.copy2(source_path, dest_path)

        app.logger.debug(f"Restored: {rel_path}")
        return True

    except Exception as e:
        app.logger.error(f"Error restoring {source_path}: {e}")
        return False

def open_restored_location(destination):
    """Open restored folder in file manager."""
    try:
        if os.name == 'nt':
            os.startfile(destination)
        elif os.uname().sysname == 'Darwin':
            sub.run(['open', destination])
        else:
            sub.run(['xdg-open', destination])
    except Exception as e:
        app.logger.warning(f"Could not open restored location: {e}")

@app.route('/api/restore-folder', methods=['POST'])
def restore_folder():
    try:
        data = request.get_json()
        folder_path = data.get('folder_path')
        target_date = data.get('target_date')
        target_time = data.get('target_time')

        if not folder_path:
            return jsonify({'success': False, 'error': 'Missing folder_path'}), 400

        main_backup = server.app_main_backup_dir()
        incremental_base = server.app_backup_dir()

        # Destination
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dest = os.path.join(
            os.path.expanduser('~'),
            f"restored_{os.path.basename(folder_path)}_{timestamp}"
        )

        os.makedirs(dest, exist_ok=True)

        # 1️⃣ RESTORE MAIN BACKUP FIRST (BASE)
        main_source = os.path.join(main_backup, folder_path)
        if not os.path.isdir(main_source):
            return jsonify({
                'success': False,
                'error': 'Main backup not found for folder'
            }), 404

        shutil.copytree(
            main_source,
            dest,
            symlinks=True,
            copy_function=shutil.copy2,
            dirs_exist_ok=True
        )

        # 2️⃣ APPLY INCREMENTALS UP TO TARGET DATETIME
        if target_date and target_time:
            for date in sorted(os.listdir(incremental_base)):
                date_path = os.path.join(incremental_base, date)
                if date > target_date:
                    break

                for time in sorted(os.listdir(date_path)):
                    if date == target_date and time > target_time:
                        break

                    inc_source = os.path.join(
                        date_path,
                        time,
                        folder_path
                    )

                    if os.path.isdir(inc_source):
                        shutil.copytree(
                            inc_source,
                            dest,
                            symlinks=True,
                            copy_function=shutil.copy2,
                            dirs_exist_ok=True
                        )

        try:
            if os.name == 'nt':
                os.startfile(dest)
            elif os.uname().sysname == 'Darwin':
                sub.run(['open', dest])
            else:
                sub.run(['xdg-open', dest])
        except Exception as e:
            print(f"Error while trying to open {dest}directory")

        return jsonify({
            'success': True,
            'restored_to': dest
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/folder-snapshots', methods=['GET'])
def get_folder_snapshots_api():
    """
    Get available snapshot dates for a folder.
    Useful for UI dropdown.
    """
    folder_path = request.args.get('folder_path')

    if not folder_path:
        return jsonify({'success': False, 'error': 'No folder path provided'}), 400

    try:
        snapshots = []
        main_backup_dir = server.app_main_backup_dir()
        incremental_base = server.app_backup_dir()

        # Check main backup
        main_folder = os.path.join(main_backup_dir, folder_path)
        if os.path.exists(main_folder):
            try:
                main_mtime = os.path.getmtime(main_backup_dir)
                file_count = count_files_in_folder(main_folder)

                snapshots.append({
                    'date': 'Initial Backup',
                    'time': datetime.fromtimestamp(main_mtime).strftime('%H:%M'),
                    'timestamp': main_mtime,
                    'type': 'main',
                    'file_count': file_count,
                    'display': 'Initial Backup'
                })
            except:
                pass

        # Check incremental backups
        if os.path.exists(incremental_base):
            for date_folder in sorted(os.listdir(incremental_base), reverse=True):
                date_path = os.path.join(incremental_base, date_folder)
                if not os.path.isdir(date_path):
                    continue

                for time_folder in sorted(os.listdir(date_path), reverse=True):
                    time_path = os.path.join(date_path, time_folder)
                    snapshot_folder = os.path.join(time_path, folder_path)

                    if os.path.exists(snapshot_folder):
                        # Count files in this snapshot
                        file_count = count_files_in_folder(snapshot_folder)

                        # Format for display
                        display_time = time_folder.replace('-', ':')

                        snapshots.append({
                            'date': date_folder,
                            'time': display_time,
                            'timestamp': get_snapshot_timestamp(date_folder, time_folder),
                            'type': 'incremental',
                            'file_count': file_count,
                            'path': time_path,
                            'display': f"{date_folder} {display_time}"
                        })

        return jsonify({
            'success': True,
            'folder_path': folder_path,
            'snapshots': snapshots,
            'count': len(snapshots)
        })

    except Exception as e:
        app.logger.error(f"Error getting folder snapshots: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

def count_files_in_folder(folder_path):
    """Count files in a folder."""
    if not os.path.exists(folder_path):
        return 0

    count = 0
    try:
        for root, dirs, files in os.walk(folder_path):
            count += len(files)
    except:
        pass
    return count

def get_snapshot_timestamp(date_str, time_str):
    """Convert snapshot date/time to timestamp."""
    try:
        # Your format: "08-12-2025 21-41"
        time_formatted = time_str.replace('-', ':')
        dt = datetime.strptime(f"{date_str} {time_formatted}", "%d-%m-%Y %H:%M")
        return dt.timestamp()
    except:
        # Fallback to current time
        return time.time()


# =============================================================================
# MAIN ROUTE
# =============================================================================
@app.route('/')
def main_index():
    """Main application route."""
    return render_template('index.html')

# ... import statements (make sure you have 'import os' and 'import sys')

# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================
if __name__ == '__main__':
    # --- Port Argument Logic ---
    flask_port = 5000  # Default fallback port
    import sys
    
    if '--port' in sys.argv:
        try:
            port_index = sys.argv.index('--port') + 1
            if port_index < len(sys.argv):
                arg_port = int(sys.argv[port_index]) 
                if arg_port == 0:
                    flask_port = 0 # Dynamic port selection
                else:
                    flask_port = arg_port 
        except (ValueError, IndexError):
            pass 
    
    # --- Standard Initialization ---
    import setproctitle
    if setproctitle:
        setproctitle.setproctitle(f'{server.APP_NAME} - UI')

    import logging
    logging.basicConfig(level=logging.INFO)

    init_location_database()
    backup_service = BackupService()

    ipc_thread = threading.Thread(target=backup_service.start_ipc_server, daemon=True)
    ipc_thread.start()

    if flask_port == 0:
        # If dynamic port is requested, use socket to find an available port
        # We must select the port BEFORE calling app.run(threaded=True)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        flask_port = s.getsockname()[1]
        s.close()
        
        # Write the selected port to the file for Electron to read immediately
        try:
            port_file = os.path.join(os.path.expanduser('~'), '.timemachine.flask_port')
            with open(port_file, 'w') as f:
                f.write(str(flask_port))
            app.logger.info(f"Wrote dynamic port {flask_port} to {port_file}")
        except Exception as e:
            app.logger.error(f"Failed to write port file: {e}")

    # Start Flask application using the determined port
    app.logger.info(f"Starting Time Machine Backup Application on http://127.0.0.1:{flask_port}")
    
    # We use app.run with the selected port (dynamic or fixed)
    # The port is written to the file BEFORE this call, guaranteeing Electron can read it immediately.
    app.run(host='127.0.0.1', port=flask_port, debug=False, use_reloader=False)
