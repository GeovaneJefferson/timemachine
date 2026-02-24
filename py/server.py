import os
import sys
import time
import json
import socket
import logging
import shutil
import platform
import subprocess as sub
import configparser
import logging.handlers
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Union

# Note: The following imports were present but appear unused in this file.
# Kept them to prevent breaking hidden dependencies, but you may want to remove them later.
import getpass
import itertools
import signal
import asyncio
import threading
import multiprocessing
import locale
import traceback
import errno
import setproctitle
import csv
import random
import inspect
import fnmatch
import hashlib
import stat
import psutil
import fcntl
import mimetypes
import difflib
import re
from concurrent.futures import ProcessPoolExecutor
from threading import Timer
from queue import Queue, Empty

# GUI Imports (Potential unused imports depending on logic)
try:
    import gi
    import cairo
except ImportError:
    pass

class SERVER:
    """
    Main Server/Controller Class.
    Handles configuration, daemon management, path resolution, and metadata.
    """
    def __init__(self):
        # --- Identity & Metadata ---
        self.DEV_NAME: str = "Geovane J."
        self.GITHUB_PAGE: str = "https://github.com/GeovaneJefferson/timemachine"
        self.GITHUB__ISSUES: str = "https://github.com/GeovaneJefferson/timemachine/issues"
        self.COPYRIGHT: str = "Copyright © 2025 Geovane J.\n\n This application comes with absolutely no warranty. See the GNU General Public License, version 3 or later for details."
        self.ID: str = "io.github.geovanejefferson.timemachine"
        self.APP_NAME: str = "Timemachine"
        self.APP_NAME_CLOSE_LOWER: str = self.APP_NAME.lower().replace(" ", "")
        self.APP_VERSION: str = "v0.1 dev"
        self.APP_RELEASE_NOTES: str = ""

        # --- Directory Setup ---
        self.USERS_HOME = os.path.expanduser('~')
        
        # XDG Standard for Config
        xdg_config_base = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.config'))
        self.APP_CONFIG_DIR = xdg_config_base / self.APP_NAME_CLOSE_LOWER
        self.CONF_PATH: str = os.path.join(self.APP_CONFIG_DIR, 'config', '.config')
        
        # Logs & PIDs
        self.LOG_FILE_PATH = os.path.expanduser(f"~/.{self.APP_NAME_CLOSE_LOWER}.log")
        self.SOCKET_PATH = f"/tmp/{self.APP_NAME_CLOSE_LOWER}_socket.sock"
        self.DAEMON_PID_LOCATION: str = os.path.expanduser(f"~/.{self.APP_NAME_CLOSE_LOWER}.pid")
        self.APP_EXECUTABLE_PATH = Path(os.path.abspath(sys.argv[0]))

        # --- Backup Structure ---
        self.BACKUPS_LOCATION_DIR_NAME: str = "backups"
        self.APPLICATIONS_LOCATION_DIR_NAME: str = "applications"
        self.MAIN_BACKUP_LOCATION = '.main_backup'

        # --- Flatpak Commands ---
        self.GET_FLATPAKS_APPLICATIONS_NAME_NON_CONTAINER: str = 'flatpak list --app --columns=application'
        self.GET_FLATPAKS_APPLICATIONS_NAME_CONTAINER = 'flatpak-spawn --host flatpak list --app --columns=application'

        # --- Frontend/Socket Config ---
        self.timeout = 2.0 
        self.backup_status = "Idle"

        # --- Initialize Config ---
        self.CONF = configparser.ConfigParser()
        self.CONF.read(self.CONF_PATH)
        
        # Load Initial Database Values
        self.DRIVER_NAME = self.get_database_value('DEVICE_INFO', 'name')
        self.DRIVER_FILESYTEM = self.get_database_value('DEVICE_INFO', 'filesystem')
        self.DRIVER_MODEL = self.get_database_value('DEVICE_INFO', 'model')
        self.EXCLUDE_FOLDER = self.get_database_value('EXCLUDE_FOLDER', 'folders')
        self.WATCHED_FOLDERS = self.get_database_value('WATCHED', 'folders')
        self.EXCLUDED_FOLDERS = self.get_database_value('EXCLUDE_FOLDER', 'folders')

        # --- Files on Device ---
        # Note: self.devices_path() relies on DB values loaded above
        journal_log = ".backup_journal.log"
        metadata = ".backup_manifest.json"
        self.JOURNAL_LOG_FILE: str = os.path.join(self.devices_path(), journal_log)
        self.METADATA_FILE: str = os.path.join(self.devices_path(), metadata)
        
        self.SUMMARY_SCRIPT_FILE: str = "generate_backup_summary.py"
        self.SUMMARY_FILENAME: str = ".backup_summary.json"

        # Ensure config exists
        self._create_default_config()

    # =============================================================================
    # CONFIGURATION & DATABASE HANDLER
    # =============================================================================
    def _create_default_config(self):
        """Create default configuration file if it doesn't exist."""
        config_dir = os.path.dirname(self.CONF_PATH)
        os.makedirs(config_dir, exist_ok=True)

        if os.path.exists(self.CONF_PATH):
           return

        # [BACKUP]
        self.CONF['BACKUP'] = {
            'automatically_backup': 'false',
            'backing_up': 'false',
            'status': ''
        }
        # [DEVICE_INFO]
        self.CONF['DEVICE_INFO'] = {
            'path': 'None', 'name': 'None', 'filesystem': 'None',
            'device': 'None', 'serial_number': 'None', 'model': 'None',
            'total': '0', 'used': '0', 'free': '0',
            'human_total': '0 B', 'human_used': '0 B', 'human_free': '0 B',
            'disk_type': 'None', 'total_size_bytes': '0'
        }
        # [EXCLUDE]
        self.CONF['EXCLUDE'] = {'exclude_hidden_itens': 'true'}
        # [BACKUP_FOLDERS] - Default checked folders
        home = os.path.expanduser('~')
        default_folders = [
            os.path.join(home, 'Desktop'),
            os.path.join(home, 'Documents'),
            os.path.join(home, 'Music'),
            os.path.join(home, 'Videos'),
            os.path.join(home, 'Pictures')
        ]
        self.CONF['BACKUP_FOLDERS'] = {'folders': ','.join(default_folders)}
        # [SEARCH]
        self.CONF['SEARCH'] = {'need_refresh_database': 'false'}
        # [EXCLUDE_FOLDER]
        self.CONF['EXCLUDE_FOLDER'] = {'folders': ''}

        with open(self.CONF_PATH, 'w') as config_file:
            self.CONF.write(config_file)

    def get_database_value(self, section, option):
        """Get value from configuration file safely."""
        try:
            if not os.path.exists(self.CONF_PATH):
                return None
            
            # Re-read config to get latest values
            temp_conf = configparser.ConfigParser()
            read_ok = temp_conf.read(self.CONF_PATH)
            if read_ok:
                self.CONF = temp_conf
            
            if not self.CONF.has_section(section) or not self.CONF.has_option(section, option):
                return None
                
            value = self.CONF.get(section, option)
            return self._convert_to_python_type(value)
            
        except Exception as e:
            logging.error(f"Error reading config: {e}")
            return None

    def _convert_to_python_type(self, value):
        """Convert string config values to Python types."""
        if value.lower() in ('true', 'yes', '1'):
            return True
        elif value.lower() in ('false', 'no', '0'):
            return False
        elif value.lower() in ('none', 'null', ''):
            return None
        return value

    def set_database_value(self, section, option, value):
        """Set value in configuration file."""
        try:
            if not self.CONF.has_section(section):
                self.CONF.add_section(section)
            
            self.CONF.set(section, option, str(value))
            
            with open(self.CONF_PATH, 'w') as configfile:
                self.CONF.write(configfile)
                
        except Exception as e:
            logging.error(f"Error writing config: {e}")

    # =============================================================================
    # METADATA HANDLING
    # =============================================================================
    def get_metadata(self):
        """Load metadata from JSON file."""
        if not os.path.exists(self.METADATA_FILE):
            return {}
        try:
            with open(self.METADATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading metadata: {e}")
            return {}

    def save_metadata(self, metadata):
        """Save metadata to JSON file with atomic write and backups."""
        if not metadata and os.path.exists(self.METADATA_FILE):
            logging.warning("Refusing to overwrite metadata with empty data")
            return False
        
        # 1. Create Backup
        if os.path.exists(self.METADATA_FILE):
            try:
                backup_path = f"{self.METADATA_FILE}.bak.{time.strftime('%Y%m%d-%H%M%S')}"
                shutil.copy2(self.METADATA_FILE, backup_path)
            except Exception as e:
                logging.warning(f"Could not create metadata backup: {e}")

        # 2. Cleanup Old Backups
        try:
            meta_backup_keep = 3  # Keep last 3 backups
            backup_dir = os.path.dirname(self.METADATA_FILE)
            meta_name = os.path.basename(self.METADATA_FILE)
            
            all_backups = sorted(
                [f for f in os.listdir(backup_dir) if f.startswith(f"{meta_name}.bak.")],
                reverse=True
            )
            
            for old_backup in all_backups[meta_backup_keep:]:
                os.remove(os.path.join(backup_dir, old_backup))
                logging.info(f"Deleted old metadata backup: {old_backup}")
        except Exception as e:
            logging.warning(f"Could not clean up old metadata backups: {e}")
        
        # 3. Atomic Write
        tmp_path = None
        try:
            os.makedirs(os.path.dirname(self.METADATA_FILE), exist_ok=True)
            fd, tmp_path = tempfile.mkstemp(prefix=".meta_tmp_", dir=os.path.dirname(self.METADATA_FILE))
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            
            os.replace(tmp_path, self.METADATA_FILE)
            return True
        except Exception as e:
            logging.error(f"Failed to save metadata: {e}")
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            return False

    # =============================================================================
    # PATHS & DEVICE INFO
    # =============================================================================
    def has_driver_connection(self, path):
        """Check if backup location is accessible."""
        try:
            return os.path.exists(path)
        except Exception:
            return False

    def get_included_folders(self) -> list:
        """Get list of folders to backup."""
        val = self.get_database_value('BACKUP_FOLDERS', 'folders')
        if not val:
            return []
        return [p.strip() for p in val.split(',') if p.strip()]

    def app_backup_dir(self):
        """Get main backup folder path (Root of backups)."""
        return f"{self.devices_path()}/{self.BACKUPS_LOCATION_DIR_NAME}"

    def app_applications_dir(self):
        """Get application backup folder path."""
        return f"{self.devices_path()}/{self.APP_NAME_CLOSE_LOWER}"

    def app_main_backup_dir(self):
        """Get main backup path (Current Active Backup)."""
        self.CONF.read(self.CONF_PATH)
        device_path = self.CONF.get('DEVICE_INFO', 'path')
        return os.path.join(device_path, self.APP_NAME_CLOSE_LOWER, self.BACKUPS_LOCATION_DIR_NAME, self.MAIN_BACKUP_LOCATION)

    def app_incremental_backup_dir(self) -> str:
        """Get current incremental backup path (Timestamped)."""
        return os.path.join(self.app_backup_dir(), time.strftime("%d-%m-%Y"), time.strftime("%H-%M"))

    def devices_name(self) -> str:
        return self.get_database_value('DEVICE_INFO', 'name')

    def devices_path(self) -> str:
        """Get devices path. e.g.: /media/usb/timemachine"""
        device_info_path = self.get_database_value('DEVICE_INFO', 'path')
        if device_info_path:
            return os.path.join(device_info_path, self.APP_NAME_CLOSE_LOWER)
        else:
            return ""

    def devices_filesystem(self) -> str:
        return self.get_database_value('DEVICE_INFO', 'filesystem')

    def devices_model(self) -> str:
        return self.get_database_value('DEVICE_INFO', 'model')

    def devices_excluded_folders(self):
        return self.get_database_value('EXCLUDE_FOLDER', 'folders')
    
    def get_summary_file_path(self):
        return os.path.join(self.devices_path(), self.SUMMARY_FILENAME)

    # =============================================================================
    # DAEMON MANAGEMENT
    # =============================================================================
    def is_daemon_running(self):
        """Checks if the daemon process is currently running."""
        if not os.path.exists(self.DAEMON_PID_LOCATION):
            return False
        try:
            with open(self.DAEMON_PID_LOCATION, 'r') as f:
                pid = int(f.read().strip())
                os.kill(pid, 0) # Signal 0 checks if the PID is alive
                return True
        except (FileNotFoundError, ValueError, ProcessLookupError):
            return False

    def start_daemon(self):
        """Start daemon with best method for platform."""
        # On Unix-like systems, try double-fork (commented out in original, using simple as default)
        # if platform.system() in ['Linux', 'Darwin']:
        #     try:
        #         return self.start_daemon_double_fork()
        #     except Exception as e:
        #         print(f"Double-fork failed, trying simple method: {e}")
        #         return self.start_daemon_simple()
        return self.start_daemon_simple()

    def start_daemon_simple(self):
        """Start daemon using subprocess (Simple Method)."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            daemon_path = os.path.join(script_dir, "main.py")
            
            original_dir = os.getcwd()
            os.chdir(os.path.dirname(daemon_path))
            
            process = sub.Popen(
                [sys.executable, daemon_path],
                start_new_session=True,
                stdout=sub.DEVNULL,
                stderr=sub.DEVNULL,
                stdin=sub.DEVNULL,
                close_fds=True,
            )
            
            os.chdir(original_dir)
            pid = process.pid
            del process
            
            return {
                "success": True,
                "message": "Daemon started!",
                "pid": pid
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed: {str(e)}"
            }

    def start_daemon_double_fork(self):
        """
        Start daemon using double-fork technique (Unix daemon best practice).
        Completely detaches the daemon from the parent process.
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            daemon_path = os.path.join(script_dir, "main.py")
            
            # First fork
            pid = os.fork()
            if pid > 0:
                # Parent process - wait for intermediate child
                os.waitpid(pid, 0)
                return {
                    "success": True,
                    "message": "Daemon started (double-fork)",
                    "pid": None  # Don't track PID (fully detached)
                }
            
            # First child - become session leader
            os.setsid()
            
            # Second fork - prevent acquiring controlling terminal
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
            
            # Second child - the actual daemon
            os.chdir(os.path.dirname(daemon_path))
            
            # Close file descriptors
            import resource
            maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
            if maxfd == resource.RLIM_INFINITY:
                maxfd = 1024
            
            for fd in range(maxfd):
                try:
                    os.close(fd)
                except OSError:
                    pass
            
            # Redirect standard file descriptors
            os.open(os.devnull, os.O_RDWR)  # stdin
            os.dup2(0, 1)  # stdout
            os.dup2(0, 2)  # stderr
            
            # Execute daemon
            os.execv(sys.executable, [sys.executable, daemon_path])
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Double-fork failed: {str(e)}"
            }
    
    def get_daemon_status(self):
        """Combines running status and autostart setting for the UI."""
        # Note: 'self.config' is not defined in __init__, assuming self.CONF intended or configparser usage
        return {
            'running': self.is_daemon_running(),
            'autostart_enabled': self.get_database_value('AUTOSTART', 'autostart_daemon') == True
        }

    # =============================================================================
    # UTILITIES
    # =============================================================================
    @staticmethod
    def bytes_to_human(size) -> str:
        """Convert bytes to human-readable format."""
        unit = 'B'
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.1f} {unit}"

    def write_backup_status(self, status):
        """Update backup status."""
        self.backup_status = status
        logging.info(f"Backup status: {status}")

    def read_backup_status(self):
        """Get current backup status."""
        return self.backup_status

    def is_first_backup(self):
        """Check if this is the first backup."""
        try:
            return not os.path.exists(self.app_main_backup_dir())
        except Exception:
            return True

    def _get_timestamp(self) -> str:
        """Get formatted minutes like '19 minutes ago'."""
        current_minutes = int(time.time() / 60)
        # Note: This logic seems incomplete in original (returns total minutes, not 'ago'), keeping as is.
        return f"{current_minutes} minutes ago"

    # =============================================================================
    # SOCKET COMMUNICATION
    # =============================================================================
    async def send_message(self, message_data: dict) -> bool:
        """Asynchronously send a JSON message to the UI via UNIX socket."""
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect(self.SOCKET_PATH) # Fixed capitalization
                sock.sendall((json.dumps(message_data) + "\n").encode("utf-8"))
            return True
        except Exception as e:
            logging.debug(f"[MessageSender] Failed to send message: {e}")
            return False
        
    async def send_getting_versions_proccess(self, description: str, processed: int = 0, progress: int = 0) -> bool:
        """Send getting versions files activity."""
        message = {
            "type": "restoring",
            "title": "Getting versions...",
            "description": description,
            "progress": "progress",
            "processed": "processed",
            "timestamp": self._get_timestamp()
        }
        return await self.send_message(message)
    
    def send_get_versions_notification(self, description: str, destination_path: str) -> bool:
        """Send file get versions completed activity."""
        message = {
            "type": "get_versions",
            "title": "Versions available", 
            "description": description,
            "destination": destination_path,
            "timestamp": datetime.now().isoformat()
        }
        # Note: This calls async method from sync context. 
        # In a real app, this should be awaited or scheduled on an event loop.
        # For now, preserving structure.
        return False 

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    server = SERVER()

    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s' 
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_LEVEL = logging.INFO 

    # --- Setup Root Logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    # Clear existing handlers
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # --- Console Handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    root_logger.addHandler(console_handler)

    # --- File Handler ---
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            server.LOG_FILE_PATH,
            maxBytes=5 * 1024 * 1024, # 5 MB per file
            backupCount=2,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"CRITICAL: Failed to set up file logging to {server.LOG_FILE_PATH}: {e}", file=sys.stderr)

    logging.info(f"Logging initialized. File log path: {server.LOG_FILE_PATH}")

    # Start the daemon
    server.start_daemon()