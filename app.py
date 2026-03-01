"""
Timemachine Web Application
A Flask-based web interface for managing backup operations.
"""

import os
import json
import time
import uuid
import hashlib
import mimetypes
import urllib.parse
import difflib
import re
import shutil
import threading
import tempfile
from pathlib import Path
from datetime import datetime
from functools import wraps

import psutil
import configparser
import platform
import subprocess as sub

from flask import Flask, render_template, jsonify, request, send_from_directory, send_file

from py.server import SERVER
from py.search_handler import SearchHandler
from py.daemon_control import send_control_command


# =============================================================================
# APPLICATION SETUP
# =============================================================================

app = Flask(__name__, template_folder='templates')
server = SERVER()
search_handler = SearchHandler()

# Global state
JOBS = {}  # Active background jobs
USERS_HOME = os.path.expanduser("~")


# =============================================================================
# DECORATORS
# =============================================================================

def json_api(f):
    """Decorator to automatically convert return values to JSON responses."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return jsonify(f(*args, **kwargs))
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    return decorated_function


# =============================================================================
# UTILITY FUNCTIONS - File Operations
# =============================================================================

def read_file_content(path, as_lines=False):
    """Read file content with multiple encoding attempts."""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.readlines() if as_lines else f.read()
        except (UnicodeDecodeError, Exception):
            continue
    
    # Binary read as last resort
    try:
        with open(path, 'rb') as f:
            binary_content = f.read()
        content_str = binary_content.decode('utf-8', errors='ignore')
        return content_str.splitlines(True) if as_lines else content_str
    except Exception as e:
        app.logger.error(f"Could not read file {path}: {e}")
        return [] if as_lines else ""


def calculate_checksum(path):
    """Calculate SHA256 checksum for a file or directory."""
    if not os.path.exists(path):
        return None

    sha256 = hashlib.sha256()

    if os.path.isdir(path):
        hashes = []
        for root, dirs, files in os.walk(path):
            dirs.sort()
            files.sort()
            for name in files:
                file_path = os.path.join(root, name)
                relative_path = os.path.relpath(file_path, path)
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.sha256()
                        while chunk := f.read(8192):
                            file_hash.update(chunk)
                    hashes.append(f"{relative_path}:{file_hash.hexdigest()}")
                except (OSError, IOError):
                    continue
        
        hashes.sort()
        for h in hashes:
            sha256.update(h.encode('utf-8'))
            
    elif os.path.isfile(path):
        try:
            with open(path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
        except (OSError, IOError):
            return None
    else:
        return None

    return sha256.hexdigest()


def open_path(path):
    """Open a file or directory in the default application."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            sub.Popen(["open", path], 
                     start_new_session=True,
                     stdout=sub.DEVNULL,
                     stderr=sub.DEVNULL,
                     stdin=sub.DEVNULL)
        else:  # Linux and other Unix-like
            sub.Popen(["xdg-open", path],
                     start_new_session=True,
                     stdout=sub.DEVNULL,
                     stderr=sub.DEVNULL,
                     stdin=sub.DEVNULL)
    except Exception as e:
        app.logger.error(f"Error opening path {path}: {e}")
        raise


# =============================================================================
# UTILITY FUNCTIONS - Formatting
# =============================================================================

def bytes_to_human(bytes_size):
    """Convert bytes to human readable format."""
    if bytes_size == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"


def get_snapshot_timestamp(date_str, time_str):
    """Helper to convert folder date/time strings to timestamp."""
    try:
        if date_str == 'Initial Backup':
            return 0
        
        # Parse date (DD-MM-YYYY) and time (HH-MM)
        dt = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H-%M")
        return dt.timestamp()
    except ValueError:
        return 0

def count_files_in_folder(folder_path):
    """Fast file count."""
    count = 0
    for _, _, files in os.walk(folder_path):
        count += len(files)
    return count

# =============================================================================
# UTILITY FUNCTIONS - Configuration
# =============================================================================

def load_config():
    """Load or create configuration."""
    config = configparser.ConfigParser()
    
    # Default configuration
    config['DEVICE_INFO'] = {
        'name': 'Not Configured',
        'path': '',
        'filesystem': 'N/A',
        'model': 'N/A',
        'total_size_bytes': '0'
    }
    
    if os.path.exists(server.CONF_PATH):
        config.read(server.CONF_PATH)
    
    return config


def save_config(config):
    """Save configuration to file."""
    with open(server.CONF_PATH, 'w') as f:
        config.write(f)


# =============================================================================
# UTILITY FUNCTIONS - Backup Information
# =============================================================================

def get_backup_info():
    """Get backup information without endpoint decorator."""
    backup_path = server.app_main_backup_dir()
    device_path = server.get_database_value('DEVICE_INFO', 'path')
    device_configured = bool(device_path and device_path not in ('None', ''))
    exists = os.path.exists(backup_path) if backup_path and device_configured else False

    return {
        'backup_path': backup_path,
        'exists': exists,
        'device_configured': device_configured,
        'device_name': server.devices_name(),
        'device_path': device_path
    }


def get_backups_root():
    """Get the backups root directory from config."""
    try:
        config = load_config()
        device_path = config.get('DEVICE_INFO', 'path', fallback='')
        if not device_path:
            return None
        
        backups_root = os.path.join(device_path, 'timemachine', 'backups')
        return backups_root if os.path.exists(backups_root) else None
    except Exception as e:
        app.logger.error(f"Error getting backups root: {e}")
        return None

def background_restore_folder_task(job_id, folder_path, target_date, target_time):
    """
    Full reconstruction of a folder using layering + manifest cleanup.
    Handles both main backup and incremental snapshots.
    """
    try:
        JOBS[job_id]['status'] = 'preparing'
        JOBS[job_id]['percentage'] = 0
        
        # Initialize your server config to get the right paths
        backups_root: str = get_backups_root() # This is 'timemachine/backups'
        
        # Clean the folder path (e.g., "Documents/Work")
        clean_folder_path: str = str(folder_path).lstrip('/')
        
        # 1. Setup the target timestamp for comparison (if not restoring from main backup)
        target_ts = None
        if target_date and target_time:
            target_dt = datetime.strptime(f"{target_date} {target_time}", "%d-%m-%Y %H-%M")
            target_ts = target_dt.timestamp()

        # 2. Prepare Destination (Restored folder on Home)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = os.path.basename(folder_path)
        dest_path = os.path.join(os.path.expanduser('~'), f"restored_{folder_name}_{timestamp}")
        os.makedirs(dest_path, exist_ok=True)
        
        JOBS[job_id]['restored_to'] = dest_path

        # --- STEP 1: RESTORE BASE (Main Backup) ---
        JOBS[job_id]['status'] = 'restoring_base'
        # server.py defines MAIN_BACKUP_LOCATION as ".main_backup"
        main_source = os.path.join(backups_root, server.MAIN_BACKUP_LOCATION, clean_folder_path)
        
        if os.path.isdir(main_source):
            shutil.copytree(main_source, dest_path, dirs_exist_ok=True)
        JOBS[job_id]['percentage'] = 20

        # If restoring from main backup only, skip incremental steps
        if target_date is None or target_time is None:
            JOBS[job_id]['status'] = 'completed'
            JOBS[job_id]['percentage'] = 100
            open_path(dest_path)
            return

        # --- STEP 2: APPLY INCREMENTALS ---
        JOBS[job_id]['status'] = 'applying_increments'
        
        # Get folders that match DD-MM-YYYY format
        date_folders = sorted([
            d for d in os.listdir(backups_root) 
            if re.match(r'\d{2}-\d{2}-\d{4}', d)
        ], key=lambda x: datetime.strptime(x, "%d-%m-%Y"))

        for date_folder in date_folders:
            dt_current = datetime.strptime(date_folder, "%d-%m-%Y")
            dt_target = datetime.strptime(target_date, "%d-%m-%Y")

            if dt_current > dt_target:
                break

            date_path = os.path.join(backups_root, date_folder)
            # Time folders are inside date folders (e.g., 14-30)
            time_folders = sorted([t for t in os.listdir(date_path) if os.path.isdir(os.path.join(date_path, t))])

            for time_folder in time_folders:
                if dt_current == dt_target and time_folder > target_time:
                    break

                inc_source = os.path.join(date_path, time_folder, clean_folder_path)
                if os.path.isdir(inc_source):
                    shutil.copytree(inc_source, dest_path, dirs_exist_ok=True)
        
        JOBS[job_id]['percentage'] = 70

        # --- STEP 3: MANIFEST CLEANUP (THE ANTI-GHOST STEP) ---
        JOBS[job_id]['status'] = 'cleaning_deleted_files'
        
        # In server.py, the manifest is inside the backups folder
        manifest_path = os.path.join(backups_root, '.backup_manifest.json')
        
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            # Walk through the files we just restored to find what shouldn't be there
            for root, dirs, files in os.walk(dest_path, topdown=False):
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    
                    # Create the manifest key (original relative path)
                    rel_path = os.path.relpath(full_path, dest_path)
                    manifest_key = os.path.join(clean_folder_path, rel_path)

                    if manifest_key in manifest:
                        data = manifest[manifest_key]
                        
                        # If deleted time is before or equal to our target, kill the ghost
                        if data.get('deleted'):
                            del_time = data.get('deleted_time', 0)
                            if target_ts is not None and del_time <= target_ts:
                                try:
                                    os.remove(full_path)
                                except OSError:
                                    pass  # File may have already been deleted
                
                # Remove folders if they became empty after cleaning
                for d in dirs:
                    dir_full = os.path.join(root, d)
                    if os.path.exists(dir_full) and not os.listdir(dir_full):
                        try:
                            os.rmdir(dir_full)
                        except OSError:
                            pass  # Folder may have other hidden files

        # --- STEP 4: FINISH ---
        JOBS[job_id]['status'] = 'completed'
        JOBS[job_id]['percentage'] = 100
        
        # Open the final folder so the user can see their restored files
        open_path(dest_path)

    except Exception as e:
        JOBS[job_id]['status'] = 'error'
        JOBS[job_id]['error'] = str(e)
        app.logger.error(f"Error in background_restore_folder_task: {e}", exc_info=True)

def convert_backup_to_home_path(backup_path):
    """Convert backup path to expected home path."""
    backups_dir = getattr(server, 'BACKUPS_LOCATION_DIR_NAME', 'timemachine/backups')
    main_backup = getattr(server, 'MAIN_BACKUP_LOCATION', server.MAIN_BACKUP_LOCATION)
    
    home_path = backup_path
    
    # Handle snapshot path
    if backups_dir in backup_path and main_backup not in backup_path:
        pattern = r'.*backups/\d{2}-\d{2}-\d{4}/\d{2}-\d{2}/(.*)'
        match = re.match(pattern, backup_path)
        if match:
            home_path = os.path.join(USERS_HOME, match.group(1))
    # Handle main backup path
    elif main_backup in backup_path:
        pattern = r'.*\.main_backup/(.*)'
        match = re.match(pattern, backup_path)
        if match:
            home_path = os.path.join(USERS_HOME, match.group(1))
    
    return home_path if home_path != backup_path else None


# =============================================================================
# UTILITY FUNCTIONS - Device Management
# =============================================================================

def get_available_devices():
    """Get all storage devices on the system with focus on Linux media."""
    devices = []
    
    try:
        partitions = psutil.disk_partitions(all=False)
        
        for i, partition in enumerate(partitions):
            try:
                mountpoint = partition.mountpoint
                
                # Skip system mounts
                skip_paths = ['/proc', '/sys', '/dev', '/run/user']
                if any(mountpoint.startswith(p) for p in skip_paths):
                    continue
                
                # On Linux, prioritize media devices
                system = platform.system().lower()
                if system == 'linux':
                    if not (mountpoint.startswith('/media/') or 
                            mountpoint.startswith('/run/media/') or
                            mountpoint.startswith('/mnt/')):
                        continue
                
                usage = psutil.disk_usage(mountpoint)
                percent_used = usage.percent
                
                # Determine status
                if percent_used > 90:
                    status, color, dot = 'Critical', 'text-red-500', 'bg-red-500'
                elif percent_used > 75:
                    status, color, dot = 'Warning', 'text-yellow-500', 'bg-yellow-500'
                else:
                    status, color, dot = 'Healthy', 'text-green-500', 'bg-green-500'
                
                # Determine device name and icon
                device_name = os.path.basename(mountpoint) or 'Root'
                icon = 'storage'
                
                if mountpoint == '/':
                    device_name = 'Root Filesystem'
                    icon = 'computer'
                elif mountpoint.startswith('/home/'):
                    username = mountpoint.split('/')[-1] if len(mountpoint.split('/')) > 2 else 'User'
                    device_name = f"{username}'s Home"
                    icon = 'person'
                elif mountpoint.startswith('/media/') or mountpoint.startswith('/run/media/'):
                    icon = 'sd_storage'
                
                # Check if removable
                is_removable = False
                if system == 'linux':
                    if (mountpoint.startswith('/media/') or 
                        mountpoint.startswith('/run/media/') or
                        mountpoint.startswith('/mnt/')):
                        is_removable = True
                    elif any(pattern in partition.device.lower() 
                            for pattern in ['sd', 'mmc', 'usb']):
                        is_removable = True
                elif partition.opts:
                    is_removable = 'removable' in partition.opts.lower()
                
                devices.append({
                    'id': i,
                    'name': device_name,
                    'mountpoint': mountpoint,
                    'device': partition.device,
                    'filesystem': partition.fstype or 'unknown',
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'total_human': bytes_to_human(usage.total),
                    'used_human': bytes_to_human(usage.used),
                    'free_human': bytes_to_human(usage.free),
                    'percent_used': round(percent_used, 1),
                    'status': status,
                    'status_color': color,
                    'status_dot': dot,
                    'icon': icon,
                    'is_removable': is_removable,
                    'is_system': mountpoint == '/',
                    'is_home': mountpoint.startswith('/home/'),
                    'is_media': mountpoint.startswith('/media/') or mountpoint.startswith('/run/media/')
                })
                
            except (PermissionError, OSError) as e:
                app.logger.warning(f"Could not inspect device {partition.mountpoint}: {e}")
                
    except Exception as e:
        app.logger.error(f"Error getting devices: {e}")
    
    # Sort devices: media first, then home, then root, alphabetically
    def sort_key(device):
        if device['is_media']:
            return (0, device['name'].lower())
        elif device['is_home']:
            return (1, device['name'].lower())
        elif device['is_system']:
            return (2, device['name'].lower())
        else:
            return (3, device['name'].lower())
    
    devices.sort(key=sort_key)
    return devices


# =============================================================================
# BACKGROUND TASKS
# =============================================================================

def background_copy_task(job_id, source_path, dest_path, open_when_done=False):
    """Background worker to copy files with progress tracking."""
    try:
        JOBS[job_id]['status'] = 'preparing'
        JOBS[job_id]['speed'] = 0
        
        # Calculate total size
        total_size = 0
        if os.path.isfile(source_path):
            total_size = os.path.getsize(source_path)
        else:
            for root, dirs, files in os.walk(source_path):
                for f in files:
                    fp = os.path.join(root, f)
                    total_size += os.path.getsize(fp)
        
        JOBS[job_id]['total_bytes'] = total_size
        JOBS[job_id]['status'] = 'copying'
        
        # Prepare temp destination
        dest_dir = os.path.dirname(dest_path)
        dest_filename = os.path.basename(dest_path)
        os.makedirs(dest_dir, exist_ok=True)
        
        temp_dest_path = os.path.join(dest_dir, f".{dest_filename}.tmp")
        
        # Cleanup temp if exists
        if os.path.exists(temp_dest_path):
            if os.path.isdir(temp_dest_path):
                shutil.rmtree(temp_dest_path)
            else:
                os.remove(temp_dest_path)

        copied_bytes = [0]
        last_update_time = [time.time()]
        last_bytes = [0]

        def copy_progress_callback(src, dst):
            if JOBS[job_id].get('abort'):
                raise Exception("Operation aborted")
            
            with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                while True:
                    if JOBS[job_id].get('abort'):
                        raise Exception("Operation aborted")
                    buf = fsrc.read(1024 * 1024)  # 1MB chunks
                    if not buf:
                        break
                    fdst.write(buf)
                    copied_bytes[0] += len(buf)
                    
                    # Calculate speed
                    current_time = time.time()
                    if current_time - last_update_time[0] >= 0.5:
                        duration = current_time - last_update_time[0]
                        bytes_diff = copied_bytes[0] - last_bytes[0]
                        speed = bytes_diff / duration
                        JOBS[job_id]['speed'] = speed
                        
                        if speed > 0 and total_size > 0:
                            remaining = total_size - copied_bytes[0]
                            JOBS[job_id]['eta'] = remaining / speed
                            
                        last_update_time[0] = current_time
                        last_bytes[0] = copied_bytes[0]
                    
                    if total_size > 0:
                        pct = (copied_bytes[0] / total_size) * 100
                        JOBS[job_id]['percentage'] = min(90, pct * 0.9)
            
            shutil.copystat(src, dst)

        if os.path.isfile(source_path):
            copy_progress_callback(source_path, temp_dest_path)
        else:
            shutil.copytree(source_path, temp_dest_path, copy_function=copy_progress_callback)

        # Rename to final
        if os.path.exists(dest_path):
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            else:
                os.remove(dest_path)
        
        os.rename(temp_dest_path, dest_path)

        # Verification
        JOBS[job_id]['status'] = 'verifying'
        JOBS[job_id]['percentage'] = 95
        
        source_checksum = calculate_checksum(source_path)
        dest_checksum = calculate_checksum(dest_path)

        if source_checksum is None or dest_checksum is None or source_checksum != dest_checksum:
            if os.path.exists(dest_path):
                if os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
                else:
                    os.remove(dest_path)
            raise Exception("Checksum verification failed")

        JOBS[job_id]['status'] = 'completed'
        JOBS[job_id]['percentage'] = 100
        JOBS[job_id]['result'] = {
            'success': True,
            'checksum_verified': True,
            'path': dest_path,
            'restored_to': dest_path
        }
        
        # In the background_copy_task function, when calling open_path:
        if open_when_done:
            try:
                sub.Popen(["xdg-open", dest_dir] if platform.system() != "Darwin" else ["open", dest_dir],
                        start_new_session=True,
                        stdout=sub.DEVNULL,
                        stderr=sub.DEVNULL,
                        stdin=sub.DEVNULL)
            except Exception as e:
                app.logger.error(f"Could not open destination: {e}")
                
    except Exception as e:
        if 'temp_dest_path' in locals() and os.path.exists(temp_dest_path):
            if os.path.isdir(temp_dest_path):
                shutil.rmtree(temp_dest_path)
            else:
                os.remove(temp_dest_path)
        
        status = 'aborted' if str(e) == "Operation aborted" else 'error'
        JOBS[job_id]['status'] = status
        JOBS[job_id]['error'] = str(e)


def background_install_flatpaks(job_id, apps):
    """Install a list of flatpak applications sequentially."""
    try:
        JOBS[job_id]['status'] = 'preparing'
        total = len(apps)
        JOBS[job_id]['total'] = total
        JOBS[job_id]['percentage'] = 0

        for idx, app_id in enumerate(apps, start=1):
            if JOBS[job_id].get('abort'):
                raise Exception("Operation aborted")
            JOBS[job_id]['status'] = f'installing {app_id}'
            # run flatpak install -y
            try:
                sub.run(['flatpak', 'install', '-y', app_id], check=True)
            except Exception as e:
                app.logger.error(f"Flatpak install failed for {app_id}: {e}")
            JOBS[job_id]['percentage'] = int((idx/total)*100)
        JOBS[job_id]['status'] = 'completed'
        JOBS[job_id]['percentage'] = 100
    except Exception as e:
        status = 'aborted' if str(e) == "Operation aborted" else 'error'
        JOBS[job_id]['status'] = status
        JOBS[job_id]['error'] = str(e)


def background_install_dev_packages(job_id, packages):
    """Install a list of development packages (pip/npm etc) sequentially."""
    try:
        JOBS[job_id]['status'] = 'preparing'
        total = len(packages)
        JOBS[job_id]['total'] = total
        JOBS[job_id]['percentage'] = 0

        for idx, pkg in enumerate(packages, start=1):
            if JOBS[job_id].get('abort'):
                raise Exception("Operation aborted")
            JOBS[job_id]['status'] = f'installing {pkg}'
            try:
                # simply run shell command; user is responsible for correct syntax
                sub.run(pkg, shell=True, check=True)
            except Exception as e:
                app.logger.error(f"Dev package install failed for {pkg}: {e}")
            JOBS[job_id]['percentage'] = int((idx/total)*100)
        JOBS[job_id]['status'] = 'completed'
        JOBS[job_id]['percentage'] = 100
    except Exception as e:
        status = 'aborted' if str(e) == "Operation aborted" else 'error'
        JOBS[job_id]['status'] = status
        JOBS[job_id]['error'] = str(e)


# =============================================================================
# STATIC FILE ROUTES
# =============================================================================

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)


# =============================================================================
# MAIN PAGE ROUTES (SPA fallback)
# =============================================================================

# The frontend is a single-page app that uses HTML5 history; when the user
# navigates to a deep link (/settings, /update, etc) the browser will request
# that path from the server.  To keep things simple we render the same
# `index.html` for any non-API route and let the client-side router take over.
#
# We still expose explicit static routes (/css/, /js/, /assets/) earlier so
# those assets will be served normally.

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """Render the SPA shell, ignoring the requested path."""
    devices = get_available_devices()
    username = os.path.basename(os.path.expanduser("~"))
    return render_template(
        'index.html',
        devices=devices,
        username=username,
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )


# =============================================================================
# SYSTEM INFO ROUTES
# =============================================================================

@app.route('/api/username')
@json_api
def get_username_api():
    """Get current username."""
    return {'username': os.path.basename(os.path.expanduser("~"))}


@app.route('/api/system-info')
@json_api
def system_info():
    """Get system information."""
    uname = os.uname() if hasattr(os, 'uname') else None
    
    return {
        'success': True,
        'platform': uname.sysname if uname else 'Unknown',
        'platform_version': uname.release if uname else 'Unknown',
        'machine': uname.machine if uname else 'Unknown',
        'username': os.path.basename(os.path.expanduser("~")),
        'home_directory': os.path.expanduser("~"),
        'device_count': len(get_available_devices())
    }


@app.route('/api/system-memory')
@json_api
def get_system_memory():
    """Get system memory info."""
    memory = psutil.virtual_memory()
    return {
        'success': True,
        'memory_total': bytes_to_human(memory.total),
        'memory_used': bytes_to_human(memory.used),
        'memory_percent': round(memory.percent, 1)
    }



@app.route('/api/check-for-updates')
def check_for_updates_route():
    from py.update_checker import get_update_info
    # This runs your git-based update script
    result = get_update_info()
    return jsonify(result)


@app.route('/api/update/perform', methods=['POST'])
@json_api
def perform_update_route():
    """Trigger the backend to fetch and apply the latest code.
    The frontend should only call this when we already know an update is
    available; the routine will do a git pull and return the output.
    """
    try:
        from py.update_checker import perform_update
        update_result = perform_update()
        # the helper already returns a dict with success/key
        return update_result
    except Exception as e:
        app.logger.error(f"Error performing update: {e}")
        return {'success': False, 'error': str(e)}


# =============================================================================
# HOME FOLDER ROUTES
# =============================================================================

@app.route('/api/home/folders')
@json_api
def get_home_folders():
    """Get list of folders in user's home directory."""
    home_path = os.path.expanduser('~')
    folders = []
    
    for item in os.listdir(home_path):
        if item.startswith('.'):
            continue
            
        item_path = os.path.join(home_path, item)
        if os.path.isdir(item_path):
            try:
                stat = os.stat(item_path)
                last_modified = datetime.fromtimestamp(stat.st_mtime)
                
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(item_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        try:
                            total_size += os.path.getsize(fp)
                        except OSError:
                            continue
                
                folders.append({
                    'name': item,
                    'path': item_path,
                    'size': total_size,
                    'lastModified': last_modified.isoformat(),
                    'isDirectory': True
                })
            except (PermissionError, OSError):
                continue
    
    return {
        'success': True,
        'folders': folders,
        'homePath': home_path,
        'count': len(folders)
    }


# =============================================================================
# DEVICE & LOCATION ROUTES
# =============================================================================


@app.route('/api/dev-packages', methods=['GET'])
@json_api
def get_dev_packages():
    """Return saved developer packages from the current backup device.

    The packages are stored as JSON in: <server.devices_path()>/dev/dev_packages.json
    """
    try:
        # ensure a device is configured
        device_root = server.devices_path()
        if not device_root:
            return {'success': False, 'error': 'No backup device configured'}

        dev_dir = os.path.join(device_root, 'dev')
        os.makedirs(dev_dir, exist_ok=True)
        file_path = os.path.join(dev_dir, 'dev_packages.json')

        if not os.path.exists(file_path):
            return {'success': True, 'packages': []}

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {'success': True, 'packages': data}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.route('/api/dev-packages', methods=['POST'])
@json_api
def save_dev_packages():
    """Save developer packages to the backup device as JSON.

    Accepts JSON body: {"packages": [ ... ]}
    """
    try:
        payload = request.get_json(force=True) or {}
        packages = payload.get('packages', [])

        device_root = server.devices_path()
        if not device_root:
            return {'success': False, 'error': 'No backup device configured'}

        dev_dir = os.path.join(device_root, 'dev')
        os.makedirs(dev_dir, exist_ok=True)
        file_path = os.path.join(dev_dir, 'dev_packages.json')

        tmp_path = file_path + '.tmp'
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(packages, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        os.replace(tmp_path, file_path)

        return {'success': True, 'saved': len(packages)}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.route('/api/locations/devices')
@json_api
def get_locations_devices():
    """Get all available devices."""
    devices = get_available_devices()
    config = load_config()
    current_path = config.get('DEVICE_INFO', 'path', fallback='')
    
    for device in devices:
        device['is_current_backup'] = device['mountpoint'] == current_path
    
    return {
        'success': True,
        'devices': devices,
        'count': len(devices),
        'current_backup_path': current_path
    }


@app.route('/api/locations/sidebar-devices')
@json_api
def get_sidebar_devices():
    """Get devices specifically formatted for the sidebar."""
    devices = get_available_devices()
    config = load_config()
    current_backup_path = config.get('DEVICE_INFO', 'path', fallback='')
    
    sidebar_devices = []
    for device in devices:
        if device['total'] < 100 * 1024 * 1024:  # Skip < 100MB
            continue
        
        sidebar_devices.append({
            'id': device['id'],
            'name': device['name'],
            'mountpoint': device['mountpoint'],
            'percent_used': device['percent_used'],
            'status': device['status'],
            'status_color': device['status_color'],
            'status_dot': device['status_dot'],
            'icon': device['icon'],
            'is_removable': device['is_removable'],
            'is_current_backup': bool(current_backup_path) and device['mountpoint'] == current_backup_path,
            'total_human': device['total_human'],
            'used_human': device['used_human'],
            'display_name': device['name']
        })
    
    return {
        'success': True,
        'devices': sidebar_devices,
        'count': len(sidebar_devices),
        'platform': platform.system(),
        'media_paths': {
            'media': '/media/',
            'run_media': '/run/media/',
            'mnt': '/mnt/'
        }
    }


@app.route('/api/locations/current-backup')
@json_api
def get_current_backup():
    """Get current backup device."""
    config = load_config()
    current_path = config.get('DEVICE_INFO', 'path', fallback='')
    
    if not current_path:
        return {
            'success': True,
            'has_backup': False,
            'message': 'No backup device configured'
        }
    
    devices = get_available_devices()
    device = next((d for d in devices if d['mountpoint'] == current_path), None)
    
    if device:
        return {
            'success': True,
            'has_backup': True,
            'device': device,
            'config': dict(config['DEVICE_INFO'])
        }
    else:
        return {
            'success': True,
            'has_backup': False,
            'message': 'Configured device not found'
        }


@app.route('/api/locations/select-device', methods=['POST'])
@json_api
def select_device():
    """Select a backup device."""
    data = request.get_json()
    mountpoint = data.get('mountpoint')
    
    if not mountpoint:
        return {'success': False, 'error': 'No mountpoint provided'}
    
    device_info_payload = data.get('device_info') if isinstance(data, dict) else None
    devices = get_available_devices()
    device = next((d for d in devices if d['mountpoint'] == mountpoint), None)

    # Prepare config values
    name = None
    dev_path = mountpoint
    dev_node = ''
    filesystem = ''
    total = 0

    if device_info_payload and isinstance(device_info_payload, dict):
        name = device_info_payload.get('name') or device_info_payload.get('display_name')
        dev_node = device_info_payload.get('device', '')
        filesystem = device_info_payload.get('filesystem', '')
        total = int(device_info_payload.get('total', 0) or 0)

    if device:
        name = name or device.get('name')
        dev_node = dev_node or device.get('device', '')
        filesystem = filesystem or device.get('filesystem', '')
        total = total or int(device.get('total', 0) or 0)

    if not name:
        return {'success': False, 'error': 'Device not found and no metadata provided'}

    config = load_config()
    if 'DEVICE_INFO' not in config:
        config['DEVICE_INFO'] = {}

    existing = config['DEVICE_INFO']
    existing['name'] = name
    existing['path'] = dev_path
    if dev_node:
        existing['device'] = dev_node
    if filesystem:
        existing['filesystem'] = filesystem
    existing['model'] = (device_info_payload.get('model') if device_info_payload and device_info_payload.get('model') is not None else existing.get('model', 'N/A'))
    existing['total_size_bytes'] = str(total if total else existing.get('total_size_bytes', '0'))

    config['DEVICE_INFO'] = existing
    save_config(config)
    
    return {
        'success': True,
        'message': f'Backup device set to {device["name"]}',
        'device': device
    }


@app.route('/api/locations/save-folders', methods=['POST'])
@json_api
def save_backup_folders():
    """Save selected backup folders into config."""
    data = request.get_json() or {}
    folders = data.get('folders', [])

    if not isinstance(folders, list):
        return {'success': False, 'error': 'folders must be a list'}

    folders_str = ','.join([f for f in folders if isinstance(f, str)])

    config = load_config()
    if 'BACKUP_FOLDERS' not in config:
        config['BACKUP_FOLDERS'] = {}
    config['BACKUP_FOLDERS']['folders'] = folders_str
    save_config(config)

    return {'success': True, 'message': 'Backup folders saved', 'folders': folders}


@app.route('/api/locations/backup-folders')
@json_api
def get_backup_folders():
    """Return saved backup folders from config."""
    config = load_config()
    folders_str = config.get('BACKUP_FOLDERS', 'folders', fallback='')
    if not folders_str:
        return {'success': True, 'folders': [], 'folders_str': ''}

    folders = [f for f in [s.strip() for s in folders_str.split(',')] if f]
    return {'success': True, 'folders': folders, 'folders_str': folders_str}


@app.route('/api/locations/eject-device', methods=['POST'])
@json_api
def eject_device():
    """Eject a device and reset config if it's the backup device."""
    data = request.get_json()
    mountpoint = data.get('mountpoint')
    
    if not mountpoint:
        return {'success': False, 'error': 'No mountpoint provided'}
    
    config = load_config()
    current_path = config.get('DEVICE_INFO', 'path', fallback='')
    
    if current_path == mountpoint:
        # Backup existing config
        try:
            config_path = os.path.join('config', 'config.conf')
            backup_path = os.path.join('config', 'config.conf.bak')
            if os.path.exists(config_path):
                with open(config_path, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
        except Exception as be:
            app.logger.warning(f'Failed to backup config before eject: {be}')
        
        # Reset config
        config = configparser.ConfigParser()
        config['DEVICE_INFO'] = {
            'name': '', 'path': '', 'filesystem': '', 'model': '',
            'total_size_bytes': '0', 'device': '', 'serial_number': 'None',
            'total': '0', 'used': '0', 'free': '0',
            'human_total': '0 B', 'human_used': '0 B', 'human_free': '0 B',
            'disk_type': 'ssd'
        }
        config['BACKUP'] = {
            'automatically_backup': 'false',
            'backing_up': 'false',
            'status': ''
        }
        config['EXCLUDE'] = {'exclude_hidden_itens': 'true'}
        config['BACKUP_FOLDERS'] = {'folders': ''}
        config['SEARCH'] = {'need_refresh_database': 'false'}
        config['EXCLUDE_FOLDER'] = {'folders': ''}
        
        save_config(config)
    
    return {
        'success': True,
        'message': f'Device {mountpoint} ejected',
        'mountpoint': mountpoint,
        'config_reset': current_path == mountpoint
    }


# =============================================================================
# BACKUP ROUTES
# =============================================================================

@app.route('/api/backup/path')
@json_api
def get_backup_path():
    """Get the main backup directory path."""
    info = get_backup_info()
    return {'success': True, **info}


# -----------------------------------------------------------------------------
# SYSTEM RESTORE ROUTES
# -----------------------------------------------------------------------------

@app.route('/api/system-restore/options')
@json_api
def system_restore_options():
    """Return available folders in backup (top-level), plus flatpak list.
    Dev packages are managed on the client side via localStorage.
    """
    try:
        backups_root = get_backups_root()
        if not backups_root:
            return {'success': True, 'folders': [], 'flatpaks': []}

        # reuse existing backup file browsing API to list root items
        folders = []
        try:
            result = search_handler.browse_backup_folder('')
            items = result.get('items', [])
            for it in items:
                if it.get('type') == 'folder':
                    size = it.get('size', 0)
                    size_str = bytes_to_human(size) if isinstance(size, (int, float)) else '--'
                    folders.append({
                        'name': it.get('name'),
                        'path': it.get('path'),
                        'size': size_str
                    })
        except Exception as e:
            app.logger.error(f"Error listing top-level backup folders: {e}")

        # get flatpak list - read directly to debug
        flatpaks = []
        try:
            # Read flatpaks directly
            device_path = server.devices_path()
            flatpak_txt_file = os.path.join(device_path, 'flatpaks', 'flatpak_applications.txt')
            
            if os.path.exists(flatpak_txt_file):
                with open(flatpak_txt_file, 'r') as f:
                    app_identifiers = [line.strip() for line in f if line.strip()]
                
                # Icon and color mappings
                icon_map = {
                    'app.zen_browser.zen': 'web',
                    'com.spotify.Client': 'music_note',
                    'com.visualstudio.code': 'terminal',
                    'us.zoom.Zoom': 'videocam',
                    'org.godotengine.Godot': 'sports_esports',
                    'com.anydesk.Anydesk': 'desktop_mac',
                    'com.valvesoftware.Steam': 'sports_esports',
                    'com.discordapp.Discord': 'chat',
                    'org.blender.Blender': 'palette',
                    'io.dbeaver.DBeaverCommunity': 'database',
                }
                
                color_map = {
                    'app.zen_browser.zen': 'bg-orange-500',
                    'com.spotify.Client': 'bg-green-600',
                    'com.visualstudio.code': 'bg-gray-800',
                    'us.zoom.Zoom': 'bg-blue-500',
                    'org.godotengine.Godot': 'bg-indigo-500',
                    'com.anydesk.Anydesk': 'bg-red-500',
                }
                
                # Build apps list
                for identifier in app_identifiers:
                    flatpaks.append({
                        'name': identifier.split('.')[-1],
                        'identifier': identifier,
                        'icon': icon_map.get(identifier, 'apps'),
                        'color': color_map.get(identifier, 'bg-blue-500')
                    })
                app.logger.info(f"Loaded {len(flatpaks)} flatpak applications")
                
        except Exception as e:
            app.logger.error(f"Error reading flatpaks: {e}", exc_info=True)

        return {
            'success': True, 
            'folders': folders, 
            'flatpaks': flatpaks
        }
    except Exception as e:
        app.logger.error(f"Error in system_restore/options: {e}", exc_info=True)
        return {'success': False, 'error': str(e), 'folders': [], 'flatpaks': []}


@app.route('/api/system-restore/install-flatpaks', methods=['POST'])
@json_api
def install_flatpaks():
    data = request.get_json() or {}
    apps = data.get('apps', [])
    if not isinstance(apps, list):
        return {'success': False, 'error': 'apps must be a list'}
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {'id': job_id, 'type': 'install_flatpaks', 'status': 'pending', 'percentage': 0, 'abort': False}
    thread = threading.Thread(target=background_install_flatpaks, args=(job_id, apps))
    thread.daemon = True
    thread.start()
    return {'success': True, 'job_id': job_id, 'message': 'Flatpak install started'}


@app.route('/api/system-restore/install-dev-packages', methods=['POST'])
@json_api
def install_dev_packages():
    data = request.get_json() or {}
    packages = data.get('packages', [])
    if not isinstance(packages, list):
        return {'success': False, 'error': 'packages must be a list'}
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {'id': job_id, 'type': 'install_dev_packages', 'status': 'pending', 'percentage': 0, 'abort': False}
    thread = threading.Thread(target=background_install_dev_packages, args=(job_id, packages))
    thread.daemon = True
    thread.start()
    return {'success': True, 'job_id': job_id, 'message': 'Dev package installation started'}


@app.route('/api/backup/files')
@json_api
def get_backup_files():
    """Get files from the backup directory with version counts."""
    path = request.args.get('path', '').strip()
    backup_info = get_backup_info()
    
    if not backup_info.get('device_configured', False):
        return {'success': True, 'items': [], 'message': 'No backup device configured'}
    
    if not backup_info.get('exists', False):
        return {'success': True, 'items': [], 'message': 'No backup directory found. Perform your first backup.'}
    
    result = search_handler.browse_backup_folder(path)
    return {'success': True, **result}


@app.route('/api/backup/connection')
@json_api
def backup_connection():
    """Check backup device connection status."""
    config = load_config()
    current_path = config.get('DEVICE_INFO', 'path', fallback='')
    
    if current_path and os.path.exists(current_path):
        return {'success': True, 'connected': True, 'location': current_path}
    else:
        return {'success': True, 'connected': False, 'location': current_path or 'Not configured'}


@app.route('/api/backup/usage')
@json_api
def backup_usage():
    """Get backup device usage statistics."""
    config = load_config()
    current_path = config.get('DEVICE_INFO', 'path', fallback='')
    
    if not current_path or not os.path.exists(current_path):
        return {
            'success': True, 'connected': False, 'has_backup': False,
            'message': 'No backup device configured or connected',
            'location': current_path or 'Not configured'
        }
    
    usage = psutil.disk_usage(current_path)
    devices = get_available_devices()
    device = next((d for d in devices if d['mountpoint'] == current_path), None)
    
    if not device:
        return {'success': True, 'connected': False, 'has_backup': False, 'message': 'Configured device not found'}
    
    home_usage = psutil.disk_usage(os.path.expanduser('~'))
    
    return {
        'success': True,
        'connected': True,
        'has_backup': True,
        'location': current_path,
        'device_name': device['name'],
        'filesystem': device['filesystem'],
        'percent_used': device['percent_used'],
        'human_used': device['used_human'],
        'human_total': device['total_human'],
        'human_free': device['free_human'],
        'home_human_used': bytes_to_human(home_usage.used),
        'home_human_total': bytes_to_human(home_usage.total),
        'home_human_free': bytes_to_human(home_usage.free),
        'home_percent_used': round((home_usage.used / home_usage.total * 100), 1) if home_usage.total > 0 else 0,
        'users_home_path': os.path.expanduser('~'),
        'device': device,
        'summary': {
            'total_files': 0,
            'last_backup': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    }


@app.route('/api/backup-summary')
@json_api
def get_backup_summary():
    """Get backup summary information from the summary file."""
    try:
        config = load_config()
        device_path = config.get('DEVICE_INFO', 'path', fallback='')
        
        if not device_path:
            return {'success': False, 'error': 'No backup device configured'}
        
        summary_path = os.path.join(device_path, 'timemachine', '.backup_summary.json')
        if not os.path.exists(summary_path):
            summary_path = os.path.join(device_path, '.backup_summary.json')
            
        if not os.path.exists(summary_path):
            return {'success': False, 'error': 'Backup summary not found', 'categories': []}
        
        with open(summary_path, 'r') as f:
            summary_data = json.load(f)
        
        total_files = 0
        total_size_bytes = 0
        
        if 'categories' in summary_data:
            for category in summary_data['categories']:
                total_files += category.get('count', 0)
                total_size_bytes += category.get('size_bytes', 0)
        
        return {
            'success': True,
            'categories': summary_data.get('categories', []),
            'most_frequent_backups': summary_data.get('most_frequent_backups', []),
            'most_frequent_recent_backups': summary_data.get('most_frequent_recent_backups', []),
            'total_files': total_files,
            'total_size_bytes': total_size_bytes,
            'total_size_str': bytes_to_human(total_size_bytes),
            'generated_at': summary_data.get('generated_at', ''),
            'summary_version': summary_data.get('summary_version', '1.0')
        }
    except Exception as e:
        app.logger.error(f"Error reading backup summary: {e}")
        return {'success': False, 'error': str(e), 'categories': []}


@app.route('/api/backup/recent-files')
@json_api
def get_recent_backup_files():
    """Get recent backed-up files (not backup folders)."""
    try:
        # Get filter parameter from query
        file_type_filter = request.args.get('type', 'all').lower()  # all, new, modified
        
        config = load_config()
        device_path = config.get('DEVICE_INFO', 'path', fallback='')
        
        if not device_path:
            return {'success': False, 'error': 'No backup device configured', 'files': []}
        
        backups_path = os.path.join(device_path, 'timemachine', 'backups')
        if not os.path.exists(backups_path):
            return {'success': True, 'files': [], 'message': 'No backups found'}
        
        files = []
        file_dict = {}  # Track files by name to get most recent
        files_in_main = set()  # Track which files exist in main backup
        
        def get_file_icon(filename):
            """Get appropriate icon based on file extension."""
            ext = os.path.splitext(filename)[1].lower()
            icons = {
                '.pdf': 'description',
                '.doc': 'description', '.docx': 'description', '.txt': 'description',
                '.xls': 'table_chart', '.xlsx': 'table_chart', '.csv': 'table_chart',
                '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image', '.bmp': 'image',
                '.mp4': 'video_library', '.mkv': 'video_library', '.mov': 'video_library', '.avi': 'video_library',
                '.mp3': 'music_note', '.wav': 'music_note', '.flac': 'music_note', '.m4a': 'music_note',
                '.zip': 'archive', '.rar': 'archive', '.7z': 'archive', '.tar': 'archive',
                '.py': 'code', '.js': 'code', '.cpp': 'code', '.java': 'code', '.go': 'code'
            }
            return icons.get(ext, 'description')
        
        # Scan recent backups for files
        try:
            # Track main backup file metadata (name + size + mtime)
            main_file_metadata = {}  # filename -> (size, mtime) tuple
            
            # STEP 1: Check main backup first
            main_backup_path = os.path.join(backups_path, server.MAIN_BACKUP_LOCATION)
            if os.path.exists(main_backup_path):
                for dirpath, dirnames, filenames in os.walk(main_backup_path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            mtime = os.path.getmtime(filepath)
                            size = os.path.getsize(filepath)
                            
                            # Store metadata for comparison
                            main_file_metadata[filename] = (size, mtime)
                            files_in_main.add(filename)
                            
                            # Add to file_dict
                            if filename not in file_dict or file_dict[filename]['mtime'] < mtime:
                                file_dict[filename] = {
                                    'name': filename,
                                    'path': filepath,
                                    'type': 'file',
                                    'icon': get_file_icon(filename),
                                    'date': datetime.fromtimestamp(mtime).isoformat(),
                                    'size': bytes_to_human(size),
                                    'status': 'completed',
                                    'mtime': mtime,
                                    'change_type': 'new',
                                    'snapshotLink': '#'
                                }
                        except (OSError, PermissionError):
                            continue
            
            # STEP 2: Check incremental backups
            date_folders = [item for item in os.listdir(backups_path) 
                           if os.path.isdir(os.path.join(backups_path, item)) 
                           and re.match(r'\d{2}-\d{2}-\d{4}', item)]
            date_folders.sort(reverse=True)
            
            for date_str in date_folders[:5]:  # Check last 5 days
                date_path = os.path.join(backups_path, date_str)
                try:
                    time_folders = [item for item in os.listdir(date_path)
                                   if os.path.isdir(os.path.join(date_path, item))
                                   and re.match(r'\d{2}-\d{2}', item)]
                    time_folders.sort(reverse=True)
                except (OSError, PermissionError):
                    continue
                
                for time_str in time_folders[:5]:  # Check last 5 backups per day
                    time_path = os.path.join(date_path, time_str)
                    
                    for dirpath, dirnames, filenames in os.walk(time_path):
                        for filename in filenames:
                            filepath = os.path.join(dirpath, filename)
                            try:
                                mtime = os.path.getmtime(filepath)
                                size = os.path.getsize(filepath)
                                
                                # Simple detection: compare with main backup metadata
                                if filename in main_file_metadata:
                                    main_size, main_mtime = main_file_metadata[filename]
                                    # Modified if size or mtime differs significantly
                                    change_type = 'modified' if (size != main_size or abs(mtime - main_mtime) > 1) else 'new'
                                else:
                                    # New file not in main backup
                                    change_type = 'new'
                                
                                # Keep most recent version of each file
                                if filename not in file_dict or file_dict[filename]['mtime'] < mtime:
                                    file_dict[filename] = {
                                        'name': filename,
                                        'path': filepath,
                                        'type': 'file',
                                        'icon': get_file_icon(filename),
                                        'date': datetime.fromtimestamp(mtime).isoformat(),
                                        'size': bytes_to_human(size),
                                        'status': 'completed',
                                        'mtime': mtime,
                                        'change_type': change_type,
                                        'snapshotLink': '#'
                                    }
                            except (OSError, PermissionError):
                                continue
        
        except Exception as e:
            app.logger.error(f"Error scanning backup files: {e}")
        
        # Convert to list and sort by modification time
        files = list(file_dict.values())
        files.sort(key=lambda x: x['mtime'], reverse=True)
        
        # Apply filter
        if file_type_filter == 'new':
            files = [f for f in files if f.get('change_type') == 'new']
        elif file_type_filter == 'modified':
            files = [f for f in files if f.get('change_type') == 'modified']
        # 'all' shows everything
        
        files = files[:20]  # Limit to 20 most recent files
        
        # Remove mtime from response
        for file in files:
            del file['mtime']
        
        return {
            'success': True,
            'files': files,
            'count': len(files),
            'filter': file_type_filter,
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        app.logger.error(f"Error getting recent backup files: {e}")
        return {'success': False, 'error': str(e), 'files': []}


# =============================================================================
# APPLICATIONS ROUTES
# =============================================================================

@app.route('/api/applications/list')
@json_api
def get_installed_applications():
    """Get list of installed Flatpak applications from backup."""
    try:
        # Flatpak file is stored at: <device_path>/timemachine/flatpaks/flatpak_applications.txt
        device_path = server.devices_path()
        flatpak_txt_file = os.path.join(
            device_path,
            'flatpaks',
            'flatpak_applications.txt'
        )
        
        app.logger.info(f"Looking for flatpak file at: {flatpak_txt_file}")
        
        if not os.path.exists(flatpak_txt_file):
            app.logger.warning(f"Flatpak file not found at: {flatpak_txt_file}")
            return {
                'success': True,
                'applications': [],
                'count': 0,
                'message': f'No flatpak backup found',
                'raw': ''
            }
        
        app.logger.info(f"Reading flatpak file from: {flatpak_txt_file}")
        with open(flatpak_txt_file, 'r') as f:
            app_identifiers = [line.strip() for line in f if line.strip()]
        
        app.logger.info(f"Found {len(app_identifiers)} flatpak applications")
        
        # read raw file contents so UI can display debug info
        try:
            with open(flatpak_txt_file, 'r') as rf:
                raw_contents = rf.read()
        except Exception:
            raw_contents = ''
        
        # Map flatpak data to UI format
        ui_apps = []
        icon_map = {
            'app.zen_browser.zen': 'web',
            'com.spotify.Client': 'music_note',
            'com.visualstudio.code': 'terminal',
            'us.zoom.Zoom': 'videocam',
            'org.godotengine.Godot': 'sports_esports',
            'com.anydesk.Anydesk': 'desktop_mac',
        }
        
        color_map = {
            'app.zen_browser.zen': 'bg-orange-500',
            'com.spotify.Client': 'bg-green-600',
            'com.visualstudio.code': 'bg-gray-800',
            'us.zoom.Zoom': 'bg-blue-500',
            'org.godotengine.Godot': 'bg-indigo-500',
            'com.anydesk.Anydesk': 'bg-red-500',
        }
        
        for identifier in app_identifiers:
            ui_apps.append({
                'name': identifier.split('.')[-1],  # Last part of identifier as display name
                'identifier': identifier,
                'icon': icon_map.get(identifier, 'apps'),
                'color': color_map.get(identifier, 'bg-blue-500')
            })
        
        response_data = {
            'success': True,
            'applications': ui_apps,
            'count': len(ui_apps),
            'raw': raw_contents
        }
        app.logger.info(f"Returning {len(ui_apps)} applications in response")
        return response_data
    except Exception as e:
        app.logger.error(f"Error getting installed applications: {e}")
        return {'success': False, 'error': str(e), 'applications': []}


# =============================================================================
# FILE OPERATION ROUTES
# =============================================================================

@app.route('/api/open-file', methods=['POST'])
@json_api
def open_file():
    """Open a file in default application."""
    data = request.get_json()
    file_path = data.get('file_path')

    if not file_path:
        return {'success': False, 'error': 'No file_path provided'}
    
    if not os.path.exists(file_path):
        return {'success': False, 'error': f'File not found: {file_path}'}

    open_path(file_path)
    return {'success': True, 'message': f'Attempted to open file: {file_path}'}


@app.route('/api/open-location', methods=['POST'])
@json_api
def open_location():
    """Open folder containing a file."""
    data = request.get_json()
    file_path = data.get('file_path')
    
    if not file_path:
        return {'success': False, 'error': 'No file_path provided'}
        
    folder_path = os.path.dirname(file_path)
    if not os.path.isdir(folder_path):
        return {'success': False, 'error': f'Directory not found: {folder_path}'}

    open_path(folder_path)
    return {'success': True, 'message': f'Attempted to open folder: {folder_path}'}


@app.route('/api/file-info', methods=['POST'])
@json_api
def file_info():
    """Get information about a file including current location."""
    data = request.json
    backup_path = data.get('file_path', '')

    if not backup_path:
        return {'success': False, 'error': 'No file path provided'}

    backups_dir = getattr(server, 'BACKUPS_LOCATION_DIR_NAME', 'timemachine/backups')
    main_backup = getattr(server, 'MAIN_BACKUP_LOCATION', server.MAIN_BACKUP_LOCATION)

    is_snapshot = (backups_dir in backup_path and main_backup not in backup_path)
    home_path = convert_backup_to_home_path(backup_path)
    current_location = server.get_file_location(backup_path) if hasattr(server, 'get_file_location') else None

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

    size = 0
    if actual_path and os.path.exists(actual_path):
        size = os.path.getsize(actual_path)
    elif os.path.exists(backup_path):
        size = os.path.getsize(backup_path)

    is_moved = (actual_path and actual_path != home_path and actual_path != backup_path)

    return {
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
    }


@app.route('/api/file-checksum', methods=['POST'])
@json_api
def calculate_file_checksum():
    """Calculate SHA256 checksum of a file."""
    data = request.get_json()
    file_path = data.get('file_path', '')
    
    if not file_path or not os.path.exists(file_path):
        return {'success': False, 'error': 'File not found'}
    
    checksum = calculate_checksum(file_path)
    return {'success': True, 'checksum': checksum}


@app.route('/api/file-stats', methods=['POST'])
@json_api
def get_file_stats():
    """Get file statistics."""
    data = request.get_json()
    file_path = data.get('file_path', '')
    
    if not file_path or not os.path.exists(file_path):
        return {'success': False, 'error': 'File not found'}
    
    try:
        stat = os.stat(file_path)
        return {
            'success': True,
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'ctime': stat.st_ctime
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.route('/api/file-exists', methods=['POST'])
@json_api
def check_file_exists():
    """Check if a file exists."""
    data = request.get_json()
    file_path = data.get('file_path', '')
    exists = os.path.exists(file_path) if file_path else False
    return {'success': True, 'exists': exists}


# =============================================================================
# SEARCH ROUTES
# =============================================================================

@app.route('/api/search/files', methods=['GET'])
@json_api
def search_files():
    """Search for files in backup directory."""
    query = request.args.get('query', '').strip()

    if not query:
        return {'success': True, 'results': [], 'message': 'No query', 'query': query}

    config = load_config()
    current_path = config.get('DEVICE_INFO', 'path', fallback='')

    if not current_path or not os.path.exists(current_path):
        return {'success': True, 'results': [], 'message': 'No backup device', 'query': query}

    results = search_handler.perform_search(query)
    formatted_results = []
    
    for result in results:
        try:
            file_path = result['path']
            is_dir = os.path.isdir(file_path)
            size = 0 if is_dir else os.path.getsize(file_path)

            backup_base = search_handler.main_files_dir
            if file_path.startswith(backup_base):
                relative_path = os.path.relpath(file_path, backup_base)
            else:
                relative_path = result.get('search_display_path', result['name'])

            formatted_results.append({
                'name': result['name'],
                'path': relative_path,
                'full_path': file_path,
                'type': 'folder' if is_dir else 'file',
                'size': size,
                'date': result.get('date', os.path.getmtime(file_path))
            })
        except (OSError, PermissionError):
            continue

    return {
        'success': True,
        'results': formatted_results,
        'query': query,
        'total': len(formatted_results),
        'message': f'Found {len(formatted_results)} results'
    }


@app.route('/api/search/status', methods=['GET'])
@json_api
def search_status():
    """Get search handler status."""
    return {
        'success': True,
        'files_loaded': search_handler.files_loaded,
        'total_files': len(search_handler.files),
        'cache_time': search_handler._cache_time,
        'cache_age_seconds': time.time() - search_handler._cache_time if search_handler._cache_time > 0 else 0
    }


@app.route('/api/search/folder')
@json_api
def get_folder_contents():
    """Get folder contents from backup directory."""
    path = request.args.get('path', '').strip()
    config = load_config()
    current_path = config.get('DEVICE_INFO', 'path', fallback='')
    
    if not current_path or not os.path.exists(current_path):
        return {'success': True, 'items': [], 'message': 'No backup device configured'}
    
    full_path = os.path.join(current_path, path.lstrip('/')) if path else current_path
    
    if not os.path.commonpath([full_path, current_path]) == current_path:
        return {'success': False, 'error': 'Invalid path', 'items': []}
    
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        return {'success': True, 'items': [], 'message': 'Directory not found'}
    
    items = []
    try:
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            try:
                is_dir = os.path.isdir(item_path)
                size = 0 if is_dir else os.path.getsize(item_path)
                
                items.append({
                    'name': item,
                    'path': os.path.join(path, item),
                    'type': 'folder' if is_dir else 'file',
                    'size': size,
                    'lastModified': os.path.getmtime(item_path) if os.path.exists(item_path) else 0
                })
            except (PermissionError, OSError):
                continue
    except PermissionError:
        return {'success': True, 'items': [], 'message': 'Permission denied'}
    
    return {'success': True, 'items': items, 'path': path or '/', 'total': len(items)}


# =============================================================================
# DAEMON ROUTES
# =============================================================================

def check_daemon_ready():
    """Check if daemon is ready by looking for the ready file."""
    try:
        app_name = server.APP_NAME
        ready_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon_ready')
        lock_file = os.path.join(os.path.expanduser("~"), f'.{app_name.lower()}_daemon.lock')

        status = {
            "is_ready": False, "daemon_running": False, "pid": None,
            "startup_time": None, "metadata_loaded": False,
            "has_lock_file": False, "error": None
        }

        if os.path.exists(lock_file):
            status["has_lock_file"] = True
            try:
                with open(lock_file, 'r') as f:
                    pid_str = f.read().strip()
                    if pid_str.isdigit():
                        pid = int(pid_str)
                        status["pid"] = pid
                        try:
                            process = psutil.Process(pid)
                            if process.is_running():
                                status["daemon_running"] = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            status["daemon_running"] = False
                            status["error"] = "Stale lock file detected"
            except Exception as e:
                status["error"] = f"Lock file error: {e}"

        if os.path.exists(ready_file):
            try:
                with open(ready_file, 'r') as f:
                    data = json.load(f)
                status["pid"] = data.get('pid')
                status["startup_time"] = data.get('ready_time')
                status["metadata_count"] = data.get('metadata_count', 0)
                status["metadata_loaded"] = status["metadata_count"] > 0

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
            status["is_ready"] = False
            status["error"] = "Daemon is starting up..."

        return status
    except Exception as e:
        return {"is_ready": False, "daemon_running": False, "error": f"Check error: {e}"}


@app.route('/api/daemon/start', methods=['POST'])
@json_api
def start_daemon():
    """Start the backup daemon."""
    # First check if already running
    status = check_daemon_ready()
    
    if status["is_ready"] and status["daemon_running"]:
        return {
            'success': False, 
            'message': 'Daemon is already running and ready',
            'already_running': True
        }
    
    if status["daemon_running"] and not status["is_ready"]:
        return {
            'success': False,
            'message': 'Daemon is starting up. Please wait.',
            'already_starting': True
        }
    
    # Attempt to start daemon
    result = server.start_daemon()
    
    # Return result from start_daemon, but ensure it has success field
    if isinstance(result, dict):
        return result
    else:
        return {
            'success': True,
            'message': 'Daemon start request sent. Please wait for it to become ready.'
        }


@app.route('/api/daemon/stop', methods=['POST'])
@json_api
def stop_daemon():
    """Stop the backup daemon."""
    try:
        data = request.get_json(silent=True) or {}
        mode = data.get('mode', 'graceful')
        
        # Check actual daemon state using the ready-status logic
        status = check_daemon_ready()
        is_running = status.get("daemon_running", False)
        
        if not is_running:
            return {
                'success': True,
                'result': 'already_stopped',
                'message': 'Daemon is already stopped',
                'running': False
            }
        
        # Try to send stop command
        if hasattr(send_control_command, '__call__'):
            ok = send_control_command('cancel', mode)
        else:
            result = server.stop_daemon()
            ok = result.get('success', False) if isinstance(result, dict) else False
        
        if ok:
            return {
                'success': True,
                'result': 'ok',
                'message': f'Daemon stop request sent (graceful shutdown). Waiting for cleanup...',
                'mode': mode,
                'running': True  # Still technically running while cleaning up
            }
        else:
            return {
                'success': False,
                'result': 'error',
                'message': 'Failed to send stop command to daemon',
                'running': True
            }
    except Exception as e:
        app.logger.error(f"Error in stop_daemon endpoint: {e}")
        return {
            'success': False,
            'result': 'error',
            'error': str(e),
            'message': f'Error stopping daemon: {str(e)}',
            'running': True
        }


@app.route('/api/daemon/status', methods=['GET'])
@json_api
def daemon_status():
    """Get the status of the backup daemon."""
    try:
        if hasattr(server, 'get_daemon_status'):
            status = server.get_daemon_status()
        else:
            status = check_daemon_ready()
        return {'success': True, 'status': status}
    except Exception as e:
        app.logger.error(f"Error getting daemon status: {e}")
        return {'success': False, 'error': str(e), 'status': {'running': False, 'ready': False, 'error': str(e)}}


@app.route('/api/daemon/ready-status', methods=['GET'])
def daemon_ready_status():
    """Check if daemon is ready."""
    try:
        status = check_daemon_ready()
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
        return jsonify({"success": False, "error": str(e), "ready": False, "running": False}), 500


# =============================================================================
# RESTORE & SNAPSHOT ROUTES
# =============================================================================

@app.route('/api/task/status/<job_id>')
@json_api
def get_task_status(job_id):
    """Get the status of a background task."""
    job = JOBS.get(job_id)
    if not job:
        return {'success': False, 'error': 'Job not found'}
    return {'success': True, 'job': job}


@app.route('/api/task/abort/<job_id>', methods=['POST'])
@json_api
def abort_task(job_id):
    """Abort a background task."""
    job = JOBS.get(job_id)
    if not job:
        return {'success': False, 'error': 'Job not found'}
    job['abort'] = True
    return {'success': True}


@app.route('/api/backup/snapshots')
@json_api
def get_backup_snapshots():
    """Get all available snapshots/versions for a specific file."""
    file_path = request.args.get('file_path', '').strip()
    
    if not file_path:
        return {'success': False, 'error': 'No file path provided'}
    
    backup_info = get_backup_info()
    if not backup_info.get('device_configured', False):
        return {'success': False, 'error': 'No backup device configured', 'snapshots': []}
    
    config = load_config()
    device_path = config.get('DEVICE_INFO', 'path', fallback='')
    if not device_path:
        return {'success': False, 'error': 'Device path not found', 'snapshots': []}
    
    backups_root = os.path.join(device_path, 'timemachine', 'backups')
    if not os.path.exists(backups_root):
        return {'success': True, 'snapshots': [], 'message': 'No backups found'}
    
    snapshots = []
    
    try:
        date_folders = [item for item in os.listdir(backups_root)
                       if os.path.isdir(os.path.join(backups_root, item))
                       and re.match(r'\d{2}-\d{2}-\d{4}', item)]
        date_folders.sort(reverse=True)
        
        for date_str in date_folders:
            date_path = os.path.join(backups_root, date_str)
            try:
                date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                continue
            
            time_folders = [item for item in os.listdir(date_path)
                           if os.path.isdir(os.path.join(date_path, item))
                           and re.match(r'\d{2}-\d{2}', item)]
            time_folders.sort(reverse=True)
            
            for time_str in time_folders:
                time_path = os.path.join(date_path, time_str)
                target_path = os.path.join(time_path, file_path.lstrip('/'))
                
                if os.path.exists(target_path):
                    try:
                        if os.path.isdir(target_path):
                            size_str = "Folder"
                        else:
                            size = os.path.getsize(target_path)
                            size_str = bytes_to_human(size)
                        
                        time_obj = datetime.strptime(time_str, '%H-%M')
                        timestamp = datetime.combine(date_obj.date(), time_obj.time())
                        
                        snapshots.append({
                            'id': f"{date_str}/{time_str}",
                            'time': time_str.replace('-', ':'),
                            'date': date_obj.strftime('%b %d %Y'),
                            'full_date': date_obj.strftime('%Y-%m-%d'),
                            'size': size_str,
                            'type': 'Snapshot',
                            'timestamp': timestamp.isoformat(),
                            'full_path': target_path,
                            'date_folder': date_str,
                            'time_folder': time_str,
                            'is_main_backup': False
                        })
                    except Exception as e:
                        app.logger.error(f"Error processing snapshot {date_str}/{time_str}: {e}")
                        continue
    except Exception as e:
        app.logger.error(f"Error scanning backups: {e}")
    
    # Check for .main_backup version
    main_backup_path = os.path.join(backups_root, server.MAIN_BACKUP_LOCATION, file_path.lstrip('/'))
    if os.path.exists(main_backup_path):
        try:
            if os.path.isdir(main_backup_path):
                size_str = "Folder"
            else:
                size = os.path.getsize(main_backup_path)
                size_str = bytes_to_human(size)

            mtime = os.path.getmtime(main_backup_path)
            mtime_dt = datetime.fromtimestamp(mtime)
            
            snapshots.append({
                'id': server.MAIN_BACKUP_LOCATION,
                'time': mtime_dt.strftime('%H:%M'),
                'date': mtime_dt.strftime('%b %d %Y'),
                'full_date': mtime_dt.strftime('%Y-%m-%d'),
                'size': size_str,
                'type': 'Primary Backup',
                'timestamp': mtime_dt.isoformat(),
                'full_path': main_backup_path,
                'date_folder': server.MAIN_BACKUP_LOCATION,
                'time_folder': '',
                'is_main_backup': True
            })
        except Exception as e:
            app.logger.error(f"Error processing .main_backup: {e}")
    
    # Sort with .main_backup at end
    def sort_key(snapshot):
        if snapshot.get('is_main_backup', False):
            return (0, '')
        else:
            return (1, snapshot['timestamp'])
    
    snapshots.sort(key=sort_key, reverse=True)
    
    return {
        'success': True,
        'snapshots': snapshots,
        'total': len(snapshots),
        'file_path': file_path
    }


@app.route('/api/backup/file-content')
@json_api
def get_file_content():
    """Get content of a file for preview."""
    file_path = request.args.get('file_path', '').strip()
    snapshot_id = request.args.get('snapshot_id', '').strip()
    
    if not file_path:
        return {'success': False, 'error': 'No file path provided'}
    if not snapshot_id:
        return {'success': False, 'error': 'No snapshot ID provided'}
    
    backups_root = get_backups_root()
    if not backups_root:
        return {'success': False, 'error': 'No backup device configured'}
    
    if snapshot_id == server.MAIN_BACKUP_LOCATION:
        date_str = server.MAIN_BACKUP_LOCATION
        time_str = ''
    else:
        try:
            date_str, time_str = snapshot_id.split('/')
        except ValueError:
            return {'success': False, 'error': f"Invalid snapshot ID format: {snapshot_id}"}
    
    full_path = os.path.join(backups_root, date_str, time_str, file_path.lstrip('/'))
    
    if not os.path.exists(full_path):
        return {'success': False, 'error': 'File not found'}
    
    text_extensions = [
        '.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.csv',
        '.log', '.yml', '.yaml', '.ini', '.cfg', '.java', '.cpp', '.c', '.h',
        '.php', '.rb', '.go', '.rs', '.sh', '.bash', '.zsh', '.conf', '.properties'
    ]
    
    file_ext = os.path.splitext(full_path)[1].lower()
    if file_ext not in text_extensions:
        return {'success': False, 'error': 'File type not supported for preview'}
    
    content = read_file_content(full_path, as_lines=False)
    return {'success': True, 'content': content, 'path': full_path}


@app.route('/api/backup/file-diff')
@json_api
def get_file_diff_api():
    """Get diff between two file versions."""
    file_path = request.args.get('file_path', '').strip()
    snapshot_id = request.args.get('snapshot_id', '').strip()
    
    if not file_path or not snapshot_id:
        return {'success': False, 'error': 'Missing parameters'}
    
    backups_root = get_backups_root()
    if not backups_root:
        return {'success': False, 'error': 'No backup device configured'}
    
    if snapshot_id == server.MAIN_BACKUP_LOCATION:
        date_str = server.MAIN_BACKUP_LOCATION
        time_str = ''
    else:
        try:
            date_str, time_str = snapshot_id.split('/')
        except ValueError:
            return {'success': False, 'error': f"Invalid snapshot ID format: {snapshot_id}"}
    
    full_path = os.path.join(backups_root, date_str, time_str, file_path.lstrip('/'))
    home_path = os.path.expanduser('~')
    current_path = os.path.join(home_path, file_path.lstrip('/'))
    
    if not os.path.exists(full_path):
        return {'success': False, 'error': 'Snapshot file not found'}
    
    snapshot_content = read_file_content(full_path, as_lines=True)
    current_content = []
    if os.path.exists(current_path):
        current_content = read_file_content(current_path, as_lines=True)
    
    diff_lines = []
    for line in difflib.unified_diff(
        snapshot_content, current_content,
        fromfile=f'Snapshot ({date_str} {time_str.replace("-", ":")})',
        tofile='Current Version',
        lineterm=''
    ):
        if line.startswith('+++') or line.startswith('---'):
            continue
        elif line.startswith('+'):
            diff_lines.append({'type': 'added', 'content': line[1:]})
        elif line.startswith('-'):
            diff_lines.append({'type': 'removed', 'content': line[1:]})
        else:
            diff_lines.append({'type': 'normal', 'content': line})
    
    return {
        'success': True,
        'diff': diff_lines,
        'snapshot_id': snapshot_id,
        'snapshot_date': date_str,
        'snapshot_time': time_str.replace('-', ':')
    }


@app.route('/api/backup/download', methods=['POST'])
@json_api
def download_backup_file():
    """Download a file from a snapshot to Downloads folder."""
    data = request.get_json()
    file_path = data.get('file_path', '').strip()
    snapshot_id = data.get('snapshot_id', '').strip()
    
    if not file_path or not snapshot_id:
        return {'success': False, 'error': 'Missing parameters'}
    
    backups_root = get_backups_root()
    if not backups_root:
        return {'success': False, 'error': 'No backup device configured'}
    
    if snapshot_id == server.MAIN_BACKUP_LOCATION:
        date_str = server.MAIN_BACKUP_LOCATION
        time_str = ''
    else:
        try:
            date_str, time_str = snapshot_id.split('/')
        except ValueError:
            return {'success': False, 'error': f"Invalid snapshot ID format: {snapshot_id}"}
    
    source_file = os.path.join(backups_root, date_str, time_str, file_path.lstrip('/'))
    if not os.path.exists(source_file):
        return {'success': False, 'error': f'Snapshot file not found: {source_file}'}
    
    home_dir = os.path.expanduser('~')
    downloads_dir = os.path.join(home_dir, 'Downloads')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    target_dir = os.path.join(downloads_dir, timestamp)
    filename = os.path.basename(file_path)
    target_file = os.path.join(target_dir, filename)
    
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        'id': job_id,
        'type': 'download',
        'status': 'pending',
        'percentage': 0,
        'abort': False
    }
    
    thread = threading.Thread(target=background_copy_task, args=(job_id, source_file, target_file, True))
    thread.daemon = True
    thread.start()
    
    return {'success': True, 'job_id': job_id, 'message': 'Download started'}


@app.route('/api/backup/restore', methods=['POST'])
@json_api
def restore_file():
    """Restore a file from a specific snapshot. If it's a folder, use folder restoration logic."""
    data = request.get_json()
    file_path = data.get('file_path', '').strip()
    snapshot_id = data.get('snapshot_id', '').strip()
    restore_to = data.get('restore_to', 'original')
    
    if not file_path:
        return {'success': False, 'error': 'No file path provided'}
    if not snapshot_id:
        return {'success': False, 'error': 'No snapshot ID provided'}
    
    backups_root = get_backups_root()
    if not backups_root:
        return {'success': False, 'error': 'No backup device configured'}
    
    # Parse snapshot ID
    if snapshot_id == server.MAIN_BACKUP_LOCATION:
        date_str = server.MAIN_BACKUP_LOCATION
        time_str = ''
    else:
        try:
            date_str, time_str = snapshot_id.split('/')
        except ValueError:
            return {'success': False, 'error': f"Invalid snapshot ID format: {snapshot_id}"}
    
    source_file = os.path.join(backups_root, date_str, time_str, file_path.lstrip('/'))
    source_file = os.path.abspath(source_file)
    
    if not source_file.startswith(os.path.abspath(backups_root)):
        return {'success': False, 'error': 'Access denied - invalid source path'}
    
    if not os.path.exists(source_file):
        return {'success': False, 'error': f'Snapshot file not found: {source_file}'}
    
    # Check if the source is a folder - if so, use folder restoration logic
    if os.path.isdir(source_file):
        # Convert snapshot_id format from "DD-MM-YYYY/HH-MM" to "DD-MM-YYYY|HH-MM"
        if snapshot_id == server.MAIN_BACKUP_LOCATION:
            folder_snapshot_id = 'main'
        else:
            folder_snapshot_id = snapshot_id.replace('/', '|')
        
        # Extract date and time from folder_snapshot_id
        if folder_snapshot_id == 'main':
            target_date = None
            target_time = None
        else:
            try:
                target_date, target_time = folder_snapshot_id.split('|')
            except ValueError:
                return {'success': False, 'error': 'Invalid folder restoration parameters'}
        
        # Create Background Job for folder restoration
        job_id = str(uuid.uuid4())
        JOBS[job_id] = {
            'id': job_id,
            'type': 'restore_folder',
            'status': 'pending',
            'percentage': 0,
            'abort': False
        }
        
        # Start folder restoration thread
        thread = threading.Thread(
            target=background_restore_folder_task, 
            args=(job_id, file_path, target_date, target_time)
        )
        thread.daemon = True
        thread.start()
        
        return {'success': True, 'job_id': job_id, 'message': 'Folder restore started'}
    
    # For regular files, proceed with file restoration
    if restore_to == 'original':
        home_path = os.path.expanduser('~')
        dest_file = os.path.join(home_path, file_path.lstrip('/'))
    else:
        dest_file = restore_to
    
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        'id': job_id,
        'type': 'restore',
        'status': 'pending',
        'percentage': 0,
        'abort': False
    }
    
    thread = threading.Thread(target=background_copy_task, args=(job_id, source_file, dest_file, False))
    thread.daemon = True
    thread.start()
    
    return {'success': True, 'job_id': job_id, 'message': 'Restore started'}

@app.route('/api/folder-snapshots', methods=['GET'])
@json_api
def get_folder_snapshots_api():
    """
    Get available snapshot dates for a specific folder.
    Logic: Scans Main Backup + Incrementals and checks if folder exists in them.
    """
    folder_path = request.args.get('folder_path')

    if not folder_path:
        return {'success': False, 'error': 'No folder path provided'}

    try:
        snapshots = []
        backups_root = get_backups_root()
        
        if not backups_root:
            return {'success': False, 'error': 'No backup device configured'}

        clean_folder_path = folder_path.lstrip('/')
        main_backup_dir = os.path.join(backups_root, server.MAIN_BACKUP_LOCATION)

        # 1. Check Main Backup
        main_folder = os.path.join(main_backup_dir, clean_folder_path)
        if os.path.exists(main_folder):
            try:
                main_mtime = os.path.getmtime(main_folder)
                file_count = count_files_in_folder(main_folder)

                snapshots.append({
                    'date': 'Initial Backup',
                    'time': datetime.fromtimestamp(main_mtime).strftime('%H:%M'),
                    'timestamp': main_mtime,
                    'type': 'main',
                    'file_count': file_count,
                    'display': 'Initial Backup',
                    'id': 'main'
                })
            except Exception as e:
                app.logger.error(f"Error checking main backup for folder: {e}")

        # 2. Check Incremental Backups
        # Get all date folders (DD-MM-YYYY)
        date_folders = [d for d in os.listdir(backups_root) 
                       if os.path.isdir(os.path.join(backups_root, d)) 
                       and re.match(r'\d{2}-\d{2}-\d{4}', d)]
        
        # Sort newest first for UI
        date_folders.sort(key=lambda x: datetime.strptime(x, "%d-%m-%Y"), reverse=True)

        for date_folder in date_folders:
            date_path = os.path.join(backups_root, date_folder)
            
            # Get time folders (HH-MM)
            time_folders = sorted(os.listdir(date_path), reverse=True)

            for time_folder in time_folders:
                time_path = os.path.join(date_path, time_folder)
                snapshot_folder = os.path.join(time_path, clean_folder_path)

                if os.path.exists(snapshot_folder):
                    # Count files in this snapshot version
                    file_count = count_files_in_folder(snapshot_folder)

                    # Format for display
                    display_time = time_folder.replace('-', ':')

                    snapshots.append({
                        'date': date_folder,
                        'time': display_time,
                        'timestamp': get_snapshot_timestamp(date_folder, time_folder),
                        'type': 'incremental',
                        'file_count': file_count,
                        'id': f"{date_folder}|{time_folder}", # Unique ID for the restore request
                        'display': f"{date_folder} {display_time}"
                    })

        return {
            'success': True,
            'folder_path': folder_path,
            'snapshots': snapshots,
            'count': len(snapshots)
        }

    except Exception as e:
        app.logger.error(f"Error getting folder snapshots: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}

@app.route('/api/restore-folder', methods=['POST'])
@json_api
def restore_folder():
    """
    Start the background process to restore a folder to a specific date.
    """
    data = request.get_json()
    folder_path = data.get('folder_path')
    snapshot_id = data.get('snapshot_id') # Format: "DD-MM-YYYY|HH-MM" or "main"

    if not folder_path:
        return {'success': False, 'error': 'Missing folder_path'}
    
    if not snapshot_id:
        return {'success': False, 'error': 'Missing snapshot_id'}

    # Parse snapshot ID
    target_date = None
    target_time = None
    
    if snapshot_id != 'main':
        try:
            target_date, target_time = snapshot_id.split('|')
        except ValueError:
            return {'success': False, 'error': 'Invalid snapshot ID format'}

    # Create Background Job
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        'id': job_id,
        'type': 'restore_folder',
        'status': 'pending',
        'percentage': 0,
        'abort': False
    }

    # Start Thread
    thread = threading.Thread(
        target=background_restore_folder_task, 
        args=(job_id, folder_path, target_date, target_time)
    )
    thread.daemon = True
    thread.start()

    return {
        'success': True, 
        'job_id': job_id, 
        'message': 'Folder restore started'
    }

# =============================================================================
# FILE STREAMING ROUTE
# =============================================================================

@app.route('/api/stream/file')
def stream_file():
    """Stream a file from the backup directory for preview."""
    path = request.args.get('path', '').strip()
    
    if not path:
        return jsonify({'error': 'No path provided'}), 400
    
    backup_info = get_backup_info()
    if not backup_info.get('device_configured', False):
        return jsonify({'error': 'No backup device configured'}), 404
    if not backup_info.get('exists', False):
        return jsonify({'error': 'Backup directory not found'}), 404
    
    backup_base_path = backup_info['backup_path']
    decoded_path = urllib.parse.unquote(path)
    full_path = os.path.join(backup_base_path, decoded_path.lstrip('/'))
    
    # Security check
    try:
        common_path = os.path.commonpath([os.path.abspath(full_path), os.path.abspath(backup_base_path)])
        if common_path != os.path.abspath(backup_base_path):
            return jsonify({'error': 'Access denied - path traversal detected'}), 403
    except ValueError:
        return jsonify({'error': 'Access denied - invalid path'}), 403
    
    if not os.path.exists(full_path):
        return jsonify({'error': 'File not found', 'requested_path': path, 'full_path': full_path}), 404
    if not os.path.isfile(full_path):
        return jsonify({'error': 'Not a file'}), 400
    
    # Guess mime type
    mime_type, _ = mimetypes.guess_type(full_path)
    if not mime_type:
        ext = os.path.splitext(full_path)[1].lower()
        mime_types = {
            '.glb': 'model/gltf-binary', '.gltf': 'model/gltf+json',
            '.fbx': 'application/octet-stream', '.obj': 'text/plain',
            '.stl': 'application/sla', '.blend': 'application/x-blender',
            '.3ds': 'application/x-3ds', '.dae': 'model/vnd.collada+xml'
        }
        mime_type = mime_types.get(ext, 'application/octet-stream')
    
    file_size = os.path.getsize(full_path)
    range_header = request.headers.get('Range')
    
    if range_header and mime_type.startswith(('video/', 'audio/', 'model/')):
        byte_range = range_header.replace('bytes=', '').split('-')
        start = int(byte_range[0]) if byte_range[0] else 0
        end = int(byte_range[1]) if len(byte_range) > 1 and byte_range[1] else file_size - 1
        
        if start >= file_size or end >= file_size or start > end:
            return jsonify({'error': 'Invalid range'}), 416
        
        with open(full_path, 'rb') as f:
            f.seek(start)
            chunk = f.read(end - start + 1)
        
        response = app.response_class(chunk, 206, mimetype=mime_type, direct_passthrough=True)
        response.headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Content-Length'] = len(chunk)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
    
    response = send_file(full_path, mimetype=mime_type, as_attachment=False, download_name=os.path.basename(full_path))
    
    if mime_type.startswith('model/'):
        response.headers['Cache-Control'] = 'public, max-age=3600'
        response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response


# =============================================================================
# SETTINGS ROUTES
# =============================================================================

def get_autostart_path():
    """Get the path for autostart .desktop file."""
    autostart_dir = os.path.expanduser('~/.config/autostart')
    return os.path.join(autostart_dir, 'timemachine.desktop')

def create_autostart_desktop():
    """Create autostart .desktop file with hardcoded absolute paths."""
    try:
        home_dir = os.path.expanduser('~')
        autostart_dir = os.path.join(home_dir, '.config', 'autostart')
        os.makedirs(autostart_dir, exist_ok=True)

        python_path = '/usr/bin/python3'
        main_py_path = os.path.join(home_dir, '.local', 'share', 'timemachine', 'py', 'main.py')

        desktop_content = f"""[Desktop Entry]
Type=Application
Name=TimeMachine
Comment=Automatic Backup Application
Exec={python_path} {main_py_path}
Icon=timemachine
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
X-KDE-autostart-after=panel
StartupNotify=false
"""

        autostart_file = os.path.join(autostart_dir, 'timemachine.desktop')

        with open(autostart_file, 'w') as f:
            f.write(desktop_content)

        os.chmod(autostart_file, 0o755)
        app.logger.info(f"Created autostart file: {autostart_file}")
        return True
    except Exception as e:
        app.logger.error(f"Error creating autostart file: {e}")
        return False


def remove_autostart_desktop():
    """Remove autostart .desktop file."""
    try:
        autostart_file = get_autostart_path()
        if os.path.exists(autostart_file):
            os.remove(autostart_file)
        return True
    except Exception as e:
        app.logger.error(f"Error removing autostart file: {e}")
        return False


@app.route('/api/settings/preferences', methods=['GET'])
@json_api
def get_preferences():
    """Get user preferences."""
    try:
        config = load_config()
        
        # Get automatic backup setting
        auto_backup = config.get('BACKUP', 'automatic_backups', fallback='false').lower() == 'true'
        
        # Check if autostart is enabled
        autostart_enabled = os.path.exists(get_autostart_path())
        
        return {
            'success': True,
            'preferences': {
                'automatic_backups': auto_backup,
                'autostart_enabled': autostart_enabled,
                'cloud_sync': config.get('BACKUP', 'cloud_sync', fallback='false').lower() == 'true',
                'encryption': config.get('BACKUP', 'encryption', fallback='false').lower() == 'true'
            }
        }
    except Exception as e:
        app.logger.error(f"Error getting preferences: {e}")
        return {'success': False, 'error': str(e)}


@app.route('/api/settings/preferences', methods=['POST'])
@json_api
def save_preferences():
    """Save user preferences."""
    try:
        data = request.get_json() or {}
        config = load_config()
        
        # Ensure BACKUP section exists
        if 'BACKUP' not in config:
            config['BACKUP'] = {}
        
        # Save automatic backups setting
        if 'automatic_backups' in data:
            is_enabled = data['automatic_backups']
            config['BACKUP']['automatic_backups'] = 'true' if is_enabled else 'false'
            
            # When automatic backups is enabled, automatically enable autostart
            # When automatic backups is disabled, automatically disable autostart
            if is_enabled:
                create_autostart_desktop()
                config['BACKUP']['autostart_enabled'] = 'true'
            else:
                remove_autostart_desktop()
                config['BACKUP']['autostart_enabled'] = 'false'

        # Allow manual control over launch-at-startup separate from automatic backups
        if 'autostart_enabled' in data:
            if data['autostart_enabled']:
                create_autostart_desktop()
                config['BACKUP']['autostart_enabled'] = 'true'
            else:
                remove_autostart_desktop()
                config['BACKUP']['autostart_enabled'] = 'false'
        
        # Save other settings
        if 'cloud_sync' in data:
            config['BACKUP']['cloud_sync'] = 'true' if data['cloud_sync'] else 'false'
        
        if 'encryption' in data:
            config['BACKUP']['encryption'] = 'true' if data['encryption'] else 'false'
        
        save_config(config)
        
        return {
            'success': True,
            'message': 'Preferences saved successfully',
            'preferences': {
                'automatic_backups': config['BACKUP'].get('automatic_backups', 'false').lower() == 'true',
                'autostart_enabled': os.path.exists(get_autostart_path()),
                'cloud_sync': config['BACKUP'].get('cloud_sync', 'false').lower() == 'true',
                'encryption': config['BACKUP'].get('encryption', 'false').lower() == 'true'
            }
        }
    except Exception as e:
        app.logger.error(f"Error saving preferences: {e}")
        return {'success': False, 'error': str(e)}


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Server error'}), 500


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    # Ensure config directory exists
    os.makedirs('config', exist_ok=True)
    
    print(f"Devices detected: {len(get_available_devices())}")
    print("=" * 60)
    print(f"Server running at: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(host='127.0.0.1', port=5000, debug=True)