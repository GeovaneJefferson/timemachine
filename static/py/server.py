import os
import json
import tempfile
import shutil
import time
import logging
import configparser
import subprocess as sub
import math
import datetime
import getpass
import pathlib
import itertools
import sys
import signal
import asyncio
import threading
import multiprocessing
import locale
import traceback
import socket
import errno
import setproctitle
import csv
import random
import platform
import inspect
import gi
import fnmatch
import hashlib
import stat
import psutil
import fcntl
import mimetypes
import cairo
import difflib 
import os
import shutil
import subprocess
import re

from concurrent.futures import ProcessPoolExecutor
from threading import Timer
from queue import Queue, Empty
from typing import Optional, List, Dict, Union
from datetime import datetime, timedelta
from pathlib import Path


class SERVER:
    def __init__(self):
        """Docstring for __init__ :param self: Description"""
        self.DEV_NAME: str = "Geovane J."
        self.GITHUB_PAGE: str = "https://github.com/GeovaneJefferson/timemachine"
        self.GITHUB__ISSUES: str = "https://github.com/GeovaneJefferson/timemachine/issues"
        self.COPYRIGHT: str = "Copyright © 2025 Geovane J.\n\n This application comes with absolutely no warranty. See the GNU General Public License, version 3 or later for details."
        self.ID: str = "io.github.geovanejefferson.timemachine"
        self.APP_NAME: str = "Timemachine"
        self.APP_NAME_CLOSE_LOWER: str = self.APP_NAME.lower().replace(" ", "")
        self.APP_VERSION: str = "v0.1 dev"
        self.SUMMARY_FILENAME: str = ".backup_summary.json"  # 
        self.BACKUPS_LOCATION_DIR_NAME: str = "backups"  # Where backups will be saved
        self.APPLICATIONS_LOCATION_DIR_NAME: str = "applications"
        self.APP_RELEASE_NOTES: str = ""

        # User's home
        self.USERS_HOME = os.path.expanduser('~')
        
        # Paths
        self.LOG_FILE_PATH = os.path.expanduser(f"~/.{self.APP_NAME_CLOSE_LOWER}.log")
        self.SOCKET_PATH = f"/tmp/{self.APP_NAME_CLOSE_LOWER}_socket.sock"
        
        self.DAEMON_PID_LOCATION: str = os.path.expanduser(f"~/.{self.APP_NAME_CLOSE_LOWER}.pid")
        
        # Frontend
        self.timeout = 2.0  # Set a sensible timeout for socket operations

        xdg_config_base = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.config'))
        self.APP_CONFIG_DIR = xdg_config_base / self.APP_NAME_CLOSE_LOWER
        self.CONF_PATH: str = os.path.join(self.APP_CONFIG_DIR, 'config', '.config')
        
        # Backup structure
        self.BACKUPS_LOCATION_DIR_NAME = "backups"
        self.MAIN_BACKUP_LOCATION = '.main_backup'
		
        ################################################################################
		# FLATPAK
		################################################################################
        self.GET_FLATPAKS_APPLICATIONS_NAME_NON_CONTAINER: str = 'flatpak list --app --columns=application'
        self.GET_FLATPAKS_APPLICATIONS_NAME_CONTAINER = 'flatpak-spawn --host flatpak list --app --columns=application'
        # self.FLATPAK_SH_DST: str = f'~/.var/app/{self.ID}/config/list_flatpaks.sh'

        # Initialize config
        self.CONF = configparser.ConfigParser()
        self.CONF.read(self.CONF_PATH)
        
        # Read configuration files
        self.DRIVER_NAME = self.get_database_value('DEVICE_INFO', 'name')
        self.DRIVER_FILESYTEM = self.get_database_value('DEVICE_INFO', 'filesystem')
        self.DRIVER_MODEL = self.get_database_value('DEVICE_INFO', 'model')
        self.EXCLUDE_FOLDER = self.get_database_value('EXCLUDE_FOLDER', 'folders')
        # self.DRIVER_DISK_TYPE = self.get_database_value('DEVICE_INFO', 'disk_type')
        
        self.WATCHED_FOLDERS = self.get_database_value('WATCHED', 'folders')
        self.EXCLUDED_FOLDERS = self.get_database_value('EXCLUDE_FOLDER', 'folders')

        # Journal and metadata paths
        journal_log = ".backup_journal.log"
        metadata = ".backup_manifest.json"
        self.JOURNAL_LOG_FILE: str = os.path.join(self.devices_path(), journal_log)
        self.METADATA_FILE: str = os.path.join(self.devices_path(), metadata)
        
        # Summary file paths
        self.SUMMARY_SCRIPT_FILE: str = "generate_backup_summary.py"
        self.SUMMARY_FILENAME: str = ".backup_summary.json"
        
        # In-memory state
        self.backup_status = "Idle"

        # Platform-Agnostic Persistent Path Setup ---
        # self.APP_CONFIG_DIR = self._get_app_config_dir()
        # self.DAEMON_PID_LOCATION = self.APP_CONFIG_DIR / "daemon.pid"
        self.APP_EXECUTABLE_PATH = Path(os.path.abspath(sys.argv[0])) # Path to the running AppImage/executable

    def _create_default_config(self):
        """Create default configuration file."""
        # This logic ensures the directory for the config file exists
        config_dir = os.path.dirname(self.CONF_PATH)
        os.makedirs(config_dir, exist_ok=True)

        # Returns is already exists
        if os.path.exists(self.CONF_PATH):
           return

        # --- [BACKUP] ---
        self.CONF['BACKUP'] = {
            'automatically_backup': 'false',
            'backing_up': 'false',
            'status': ''  # Added 'status' field with an empty placeholder
        }

        # --- [DEVICE_INFO] ---
        # Replaces all hardcoded values with generic placeholders.
        self.CONF['DEVICE_INFO'] = {
            'path': 'None',
            'name': 'None',
            'filesystem': 'None',
            'device': 'None',
            'serial_number': 'None',
            'model': 'None',
            'total': '0',
            'used': '0',
            'free': '0',
            'human_total': '0 B',
            'human_used': '0 B',
            'human_free': '0 B',
            'disk_type': 'None',
            'total_size_bytes': '0'
        }

        # --- [EXCLUDE] ---
        self.CONF['EXCLUDE'] = {
            'exclude_hidden_itens': 'true'
        }

        # --- [BACKUP_FOLDERS] ---
        # Added this required section with an empty folder list as the generic default
        self.CONF['BACKUP_FOLDERS'] = {
            'folders': ''
        }

        # --- [SEARCH] ---
        # Added this required section with a default value
        self.CONF['SEARCH'] = {
            'need_refresh_database': 'false'
        }

        # --- [EXCLUDE_FOLDER] ---
        self.CONF['EXCLUDE_FOLDER'] = {
            'folders': ''
        }

        with open(self.CONF_PATH, 'w') as config_file:
            self.CONF.write(config_file)

    def _get_app_config_dir(self) -> Path:
        """Returns the persistent, user-specific config directory (~/.config/TimeMachine on Linux)."""
        # Follows XDG Base Directory Specification for Linux
        base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
        
        config_dir = base / self.APP_NAME
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
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

    def start_daemon_double_fork(self):
        """
        Start daemon using double-fork technique (Unix daemon best practice)
        This completely detaches the daemon from the parent process
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            daemon_path = os.path.join(script_dir, "daemon.py")
            
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
                # First child exits immediately
                sys.exit(0)
            
            # Second child - the actual daemon
            # Change directory
            os.chdir(os.path.dirname(daemon_path))
            
            # Close all file descriptors
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


    # =============================================================================
    # BACKUP FOLDERS PATHS
    # =============================================================================
    def app_backup_dir(self):
        """Get main backup folder path."""
        return f"{self.devices_path()}/{self.BACKUPS_LOCATION_DIR_NAME}"

    def app_applications_dir(self):
        """Get main backup folder path."""
        return f"{self.devices_path()}/{self.APP_NAME_CLOSE_LOWER}"

    def app_main_backup_dir(self):
        """Get main backup path."""
        # return f"{self.app_backup_dir()}/{self.MAIN_BACKUP_LOCATION}"
        self.CONF.read(self.CONF_PATH)
        return os.path.join(self.CONF.get('DEVICE_INFO', 'path'), f'{self.APP_NAME_CLOSE_LOWER}', f'{self.BACKUPS_LOCATION_DIR_NAME}', f'{self.MAIN_BACKUP_LOCATION}')

    def app_incremental_backup_dir(self) -> str:
        """Get current incremental backup path."""
        return os.path.join(self.app_backup_dir(), time.strftime("%d-%m-%Y"), time.strftime("%H-%M"))

    def devices_name(self) -> str:
        """Get devices name."""
        return self.get_database_value('DEVICE_INFO', 'name')

    def devices_path(self) -> str:
        f"""Get devices path. e.g.: /media/usb/{self.APP_NAME_CLOSE_LOWER}"""
        device_info_path = self.get_database_value('DEVICE_INFO', 'path')
        if device_info_path:
            return os.path.join(device_info_path, self.APP_NAME_CLOSE_LOWER)
        else:
            return ""

    def devices_filesystem(self) -> str:
        """Get devices filesystem type."""
        return self.get_database_value('DEVICE_INFO', 'filesystem')

    def devices_model(self) -> str:
        """Get devices model type."""
        return self.get_database_value('DEVICE_INFO', 'model')

    def devices_excluded_folders(self):
        """Get devices model type."""
        return self.get_database_value('EXCLUDE_FOLDER', 'folders')


    # =============================================================================
    # DATABASE HANDLER
    # =============================================================================
    def get_database_value(self, section, option):
        """Get value from configuration file."""
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
        """Save metadata to JSON file with atomic write."""
        if not metadata and os.path.exists(self.METADATA_FILE):
            logging.warning("Refusing to overwrite metadata with empty data")
            return False
        
        # Create backup of existing metadata
        if os.path.exists(self.METADATA_FILE):
            try:
                backup_path = f"{self.METADATA_FILE}.bak.{time.strftime('%Y%m%d-%H%M%S')}"
                shutil.copy2(self.METADATA_FILE, backup_path)
            except Exception as e:
                logging.warning(f"Could not create metadata backup: {e}")

        # Clean up old metadata backups
        try:
            # This value should ideally be configurable.
            # We'll use a hardcoded value that matches the daemon's setting.
            meta_backup_keep = 3  # Number of metadata backups to keep 
            backup_dir = os.path.dirname(self.METADATA_FILE)
            meta_name = os.path.basename(self.METADATA_FILE)
            
            # Find all backup files, sort them from newest to oldest
            all_backups = sorted(
                [f for f in os.listdir(backup_dir) if f.startswith(f"{meta_name}.bak.")],
                reverse=True
            )
            
            # Remove backups that exceed the keep limit
            for old_backup in all_backups[meta_backup_keep:]:
                os.remove(os.path.join(backup_dir, old_backup))
                logging.info(f"Deleted old metadata backup: {old_backup}")
        except Exception as e:
            logging.warning(f"Could not clean up old metadata backups: {e}")
        
        # Atomic write
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
        
    def get_summary_file_path(self):
        """Get the current summary file path based on current device"""
        return os.path.join(self.devices_path(), self.SUMMARY_FILENAME)

    # =============================================================================
    # CALCULATIONS
    # =============================================================================        
    def bytes_to_human(size) -> str:
        """Convert bytes to human-readable format"""
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
        
    # =============================================================================
    # RESTORATION
    # ============================================================================= 
    def _get_timestamp(self) -> str:
        """Get formatted minutes like '19 minutes ago'."""
        current_minutes = int(time.time() / 60)
        return f"{current_minutes} minutes ago"
    
    async def send_message(self, message_data: dict) -> bool:
        """  
        Asynchronously send a JSON message to the UI via UNIX socket.
        """
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect(self.socket_path)
                sock.sendall((json.dumps(message_data) + "\n").encode("utf-8"))
            return True
        except Exception as e:
            logging.debug(f"[MessageSender] Failed to send message: {e}")
            return False
        
    async def send_restoring_file(self, description: str, processed: int = 0, progress: int = 0) -> bool:
        """Send sleeping files activity."""
        message = {
            "type": "restoring",
            "title": "Restoring file...",
            "description": description,
            "progress": "progress",
            "processed": "processed",
            "timestamp": self._get_timestamp()
        }
        return await self.send_message(message)
    
    def send_restore_notification(self, description: str, destination_path: str) -> bool:
        """Send file restore completed activity."""
        message = {
            "type": "restore",
            "title": "File Restored", 
            "description": description,
            "destination": destination_path,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(message)


    # =============================================================================
    # DAEMON
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
            # self.DAEMON_PID_LOCATION.unlink(missing_ok=True) # Clean up stale PID
            return False

    def start_daemon(self):
        """Start daemon with best method for platform"""
        return self.start_daemon_simple()
        
        # On Unix-like systems, use double-fork
        if platform.system() in ['Linux', 'Darwin']:
            try:
                return self.start_daemon_double_fork()
            except Exception as e:
                print(f"Double-fork failed, trying simple method: {e}")
                return self.start_daemon_simple()
        else:
            # On other platforms, use simple method
            return self.start_daemon_simple()
    
    def start_daemon_simple(self):
        """Simple daemon start (original fixed version)"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            daemon_path = os.path.join(script_dir, "daemon.py")
            
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
                "message": "Daemon started",
                "pid": pid
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed: {str(e)}"
            }
        
    # APPIMAGE
    # def start_daemon(self):
    #     """[RUN DAEMON] Starts the daemon in a detached process."""
    #     # if self.is_daemon_running():
    #     #     return {"success": False, "message": "Daemon is already running."}
    #     try:
    #         command = [str(self.APP_EXECUTABLE_PATH), "--daemon-only"]
    #         # Use start_new_session=True for clean detachment (important for AppImage)
    #         sub.Popen(command, start_new_session=True, stdout=sub.DEVNULL, stderr=sub.DEVNULL)
            
    #         # Wait for the new daemon process to start and write its PID file
    #         time.sleep(1) 
            
    #         if self.is_daemon_running():
    #             return {"success": True, "message": "Daemon started."}
    #         else:
    #             return {"success": False, "message": "Daemon started but failed to write PID."}
    #     except Exception as e:
    #         return {"success": False, "message": f"Failed to start daemon: {e}"}

    def set_autostart(self, enable: bool):
        """[AUTO STARTUP] Toggles the Linux autostart .desktop file."""
        autostart_dir = Path.home() / '.config' / 'autostart'
        desktop_file = autostart_dir / f"{self.ID}.desktop"

        if enable:
            autostart_dir.mkdir(exist_ok=True)
            exec_command = f"{self.APP_EXECUTABLE_PATH}"
            content = f"""[Desktop Entry]\nType=Application\nName={self.APP_NAME} Daemon\nExec={exec_command}\nNoDisplay=true\nX-GNOME-Autostart-enabled=true\n"""
            try:
                with open(desktop_file, 'w') as f:
                    f.write(content)
                # Update config file to reflect user choice (optional, but good practice)
                # self._update_config('AUTOSTART', 'autostart_daemon', True) 
                return {"success": True, "enabled": True, "message": "Autostart enabled."}
            except Exception as e:
                return {"success": False, "message": f"Failed to enable autostart: {e}"}
        else:
            desktop_file.unlink(missing_ok=True)
            # self._update_config('AUTOSTART', 'autostart_daemon', False)
            return {"success": True, "enabled": False, "message": "Autostart disabled."}

    def get_daemon_status(self):
        """Combines running status and autostart setting for the UI."""
        return {
            'running': self.is_daemon_running(),
            'autostart_enabled': self.config.getboolean('AUTOSTART', 'autostart_daemon', fallback=False)
        }


if __name__ == "__main__":
    server = SERVER()

    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s' 
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_LEVEL = logging.INFO 

    # --- A. Setup Root Logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    # Clear existing handlers to prevent duplicates if main() is called multiple times
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)


    # --- B. Console Handler (Keeps logs printing to terminal) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    root_logger.addHandler(console_handler)


    # --- C. File Handler (Saves logs to disk) ---
    # Use RotatingFileHandler to prevent the log file from getting too large
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            server.LOG_FILE_PATH,
            maxBytes=5 * 1024 * 1024, # 5 MB per file
            backupCount=2, # Keep 2 old log files
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        root_logger.addHandler(file_handler)
        
    except Exception as e:
        # Print error to console if file logging fails (e.g., bad permissions)
        print(f"CRITICAL: Failed to set up file logging to {server.LOG_FILE_PATH}: {e}", file=sys.stderr)

    logging.info(f"Logging initialized. File log path: {server.LOG_FILE_PATH}")

    server.start_daemon()
    pass
