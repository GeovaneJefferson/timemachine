"""
Hybrid Daemon: Incremental, Atomic, and Concurrent File Backup Service
PURE THREADING MODEL with FIXED LOCKING

[ARCHITECTURE]
1. Fast Path (Watchdog): Real-time events detected and queued
2. Worker Thread: Processes events in batches using ThreadPoolExecutor
3. Safety Net (Polling): Infrequent full scans catch missed events
4. Flatpak Backup: Periodic backup of installed Flatpak applications

[LOCKING IMPROVEMENTS]
1. Minimal lock scope - only during atomic rename
2. Longer timeouts (30s instead of 5s)
3. Stale lock detection and cleanup
4. Better error handling with exponential backoff
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Dict, Tuple, Any, Set
from server import *
import os
import time
import logging
import json
import shutil
import hashlib
import socket
import errno
import sys
import psutil
import uuid
import threading
import fnmatch
import stat
import atexit
import queue
import signal
import subprocess as sub
from datetime import datetime
from generate_backup_summary import generate_summary
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import setproctitle
except ImportError:
    setproctitle = None

# --- GLOBAL SHARED STATE ---
server = SERVER()

# --- CONFIGURATION ---
POLLING_INTERVAL = 1800  # 30 minutes
HIGH_CPU_THRESHOLD = 75.0
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50 MB
MIN_BATCH_SIZE = 10
BASE_BATCH_SIZE = 50
MAX_BATCH_SIZE = 200
MIN_REPROCESS_INTERVAL = 60  # 1 minute
FLATPAK_BACKUP_INTERVAL = POLLING_INTERVAL


# =============================================================================
# WATCHDOG EVENT HANDLER
# =============================================================================
class BackupChangeHandler(FileSystemEventHandler):
    """Simplified event handler with basic debouncing."""
    def __init__(self, daemon: 'Daemon'):
        self.daemon = daemon
        self.queue = daemon.event_queue
        self._last_event_time: Dict[str, float] = {}
        self.DEBOUNCE_COOLDOWN = 1.0  # 1s

    def _should_process(self, path: str) -> bool:
        """Check if file should be processed."""
        if not os.path.exists(path):
            return False
        if self.daemon._should_exclude(path):
            return False

        norm_path = os.path.normpath(path)
        current_time = time.time()

        if current_time - self._last_event_time.get(norm_path, 0) < self.DEBOUNCE_COOLDOWN:
            return False

        self._last_event_time[norm_path] = current_time
        return True

    def on_any_event(self, event):
        """Universal event handler."""
        if event.is_directory:
            return

        if not self._should_process(event.src_path):
            return

        src_path = os.path.normpath(event.src_path)
        dest_path = os.path.normpath(event.dest_path) if hasattr(event, 'dest_path') else None

        try:
            self.queue.put((event.event_type, src_path, dest_path), timeout=1)
            logging.debug(f"Queued: {event.event_type} - {src_path}")
        except queue.Full:
            logging.warning(f"Event queue full, dropping event for {src_path}")

    def on_created(self, event):
        self.on_any_event(event)

    def on_modified(self, event):
        self.on_any_event(event)

    def on_deleted(self, event):
        self.on_any_event(event)

    def on_moved(self, event):
        self.on_any_event(event)


# =============================================================================
# DAEMON CLASS
# =============================================================================
class Daemon:
    def __init__(self):
        self.users_home_dir = os.path.expanduser("~")
        self.app_main_backup_dir = server.app_main_backup_dir()
        self.app_incremental_backup_dir = server.app_incremental_backup_dir()
        self.app_backup_dir = server.devices_path()

        # Threading setup
        cpu_count = os.cpu_count() or 4
        self.max_threads = min(32, cpu_count * 4)
        self.scan_threads = min(8, cpu_count * 2)
        self.executor = ThreadPoolExecutor(max_workers=self.max_threads, thread_name_prefix="FileWorker")

        # Event queue for watchdog events
        self.event_queue = queue.Queue(maxsize=5000)  
        self.message_queue = queue.Queue(maxsize=500)
        self.shutdown_event = threading.Event()

        # State
        self.metadata = {}
        self.hash_to_path_map = {}
        self.excludes_extras = [".git", "node_modules", ".temp", "*.tmp", "__pycache__"]
        self.journal = Journal()

        self.last_processed_time: Dict[str, float] = {}
        self.last_flatpak_backup_time = 0

        # NEW: Track files currently being processed to prevent duplicates
        self.processing_files: Set[str] = set()
        self.processing_lock = threading.Lock()

        # Daemon lock
        self.ready_file_path = os.path.join(self.users_home_dir, f'.{server.APP_NAME.lower()}_daemon_ready')
        self.lock_file_path = os.path.join(self.users_home_dir, f'.{server.APP_NAME.lower()}_daemon.lock')

        # Progress tracking
        self.files_backed_up_count = 0
        self.total_size_transferred = 0
        self.backup_start_time = None
        self.total_files_to_scan = 0
        self.total_transfer_size = 0

        # IMPROVED LOCKING SYSTEM
        self.state_lock = threading.Lock()  # Main state lock for metadata
        self.file_locks = {}
        self.file_locks_access_lock = threading.Lock()
        self.lock_timeouts = {}  # Track when locks were acquired
        self.MAX_LOCK_AGE = 300  # 5 minutes - auto-release stale locks

        # Batching
        self.current_batch_size = BASE_BATCH_SIZE

        # Settings
        exclude_hidden_val = server.get_database_value('EXCLUDE', 'exclude_hidden_itens')
        self._exclude_hidden = str(exclude_hidden_val).lower() == 'true' if exclude_hidden_val else False
        self._watch_paths = self._get_target_folders()

        # Message sender
        self.message_sender = MessageSender()

    # =========================================================================
    # IMPROVED FILE LOCKING
    # =========================================================================

    def _acquire_file_lock(self, path: str, timeout: int = 30) -> bool:
        """
        Acquire file lock with longer timeout and stale lock detection.

        Key improvements:
        1. Longer default timeout (30s instead of 5s)
        2. Automatic stale lock detection and cleanup
        3. Better error handling
        """
        key = os.path.normpath(path)

        # Clean up stale locks first
        self._cleanup_stale_locks()

        with self.file_locks_access_lock:
            if key not in self.file_locks:
                self.file_locks[key] = threading.Lock()
            lock = self.file_locks[key]

        # Try to acquire with timeout
        acquired = lock.acquire(timeout=timeout)

        if acquired:
            # Record when we acquired this lock
            with self.file_locks_access_lock:
                self.lock_timeouts[key] = time.time()
        else:
            logging.warning(f"Failed to acquire lock for {path} after {timeout}s")

        return acquired

    def _release_file_lock(self, path: str):
        """Release file lock safely."""
        key = os.path.normpath(path)

        with self.file_locks_access_lock:
            if key in self.file_locks:
                try:
                    self.file_locks[key].release()
                    # Remove timeout tracking
                    if key in self.lock_timeouts:
                        del self.lock_timeouts[key]
                except RuntimeError:
                    # Lock wasn't held by this thread - this is OK
                    pass
                except Exception as e:
                    logging.error(f"Error releasing lock for {key}: {e}")

    def _cleanup_stale_locks(self):
        """Remove locks that have been held too long."""
        current_time = time.time()
        stale_keys = []

        with self.file_locks_access_lock:
            for key, acquired_time in list(self.lock_timeouts.items()):
                if current_time - acquired_time > self.MAX_LOCK_AGE:
                    stale_keys.append(key)

            # Clean up stale locks
            for key in stale_keys:
                logging.warning(f"Cleaning up stale lock: {key}")
                try:
                    if key in self.file_locks:
                        del self.file_locks[key]
                    if key in self.lock_timeouts:
                        del self.lock_timeouts[key]
                except Exception as e:
                    logging.error(f"Error cleaning stale lock {key}: {e}")

    # =========================================================================
    # FLATPAK BACKUP METHODS
    # =========================================================================

    def _has_driver_connection(self) -> bool:
        """Check if backup location is available."""
        return os.path.exists(self.app_backup_dir)

    def _is_backup_location_writable(self) -> bool:
        """Check if backup location is writable."""
        try:
            test_file = os.path.join(self.app_backup_dir, f".test_{uuid.uuid4().hex}")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return True
        except:
            return False

    def _execute_flatpak_command(self, command: List[str]) -> Optional[str]:
        """Execute flatpak command and return output."""
        try:
            result = sub.run(
                command,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )
            return result.stdout.strip()
        except sub.TimeoutExpired:
            logging.error(f"Flatpak command timed out: {command}")
            return None
        except sub.CalledProcessError as e:
            logging.error(f"Flatpak command failed (exit {e.returncode}): {e.stderr}")
            return None
        except Exception:
            return None

    def _save_flatpak_list(self, flatpak_list: str) -> bool:
        """Save flatpak list to backup location."""
        try:
            flatpak_backup_dir = os.path.join(self.app_backup_dir, "flatpaks")
            os.makedirs(flatpak_backup_dir, exist_ok=True)

            flatpak_file = os.path.join(flatpak_backup_dir, "flatpak_applications.txt")

            with open(flatpak_file, 'w') as f:
                f.write(flatpak_list)

            # Also save as JSON
            json_file = os.path.join(flatpak_backup_dir, "flatpak_applications.json")
            applications = []
            for line in flatpak_list.splitlines():
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        applications.append({
                            "name": parts[0].strip(),
                            "version": parts[1].strip(),
                            "arch": parts[2].strip(),
                            "branch": parts[3].strip() if len(parts) > 3 else "",
                            "origin": parts[4].strip() if len(parts) > 4 else ""
                        })

            with open(json_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "total_applications": len(applications),
                    "applications": applications
                }, f, indent=2)

            logging.info(f"Flatpak application list saved to {flatpak_file}")
            return True
        except Exception as e:
            logging.error(f"Failed to save Flatpak list: {e}")
            return False

    def backup_flatpaks(self):
        """Backs up the list of installed Flatpak applications."""
        logging.info("Starting Flatpak application backup...")

        if not self._has_driver_connection() or not self._is_backup_location_writable():
            logging.warning("Backup device not available or not writable. Skipping Flatpak backup.")
            return

        commands_to_try = [
            server.GET_FLATPAKS_APPLICATIONS_NAME_CONTAINER.split(),
            server.GET_FLATPAKS_APPLICATIONS_NAME_NON_CONTAINER.split()
        ]

        output = None
        for command in commands_to_try:
            output = self._execute_flatpak_command(command)
            if output is not None:
                break

        if output is not None and output.strip():
            success = self._save_flatpak_list(output)
            if success:
                self.last_flatpak_backup_time = time.time()
                logging.info("Flatpak backup completed successfully")
        else:
            logging.error("All attempts to list Flatpak applications failed.")

    def check_and_backup_flatpaks(self):
        """Check if it's time to backup flatpaks and do it if needed."""
        current_time = time.time()

        if current_time - self.last_flatpak_backup_time >= FLATPAK_BACKUP_INTERVAL:
            logging.info(f"Scheduled Flatpak backup")
            self.backup_flatpaks()

    # =========================================================================
    # DAEMON LOCK
    # =========================================================================
    def _create_ready_state(self):
        """Create ready state file."""
        try:
            with open(self.ready_file_path, 'w') as f:
                json.dump({
                    'pid': os.getpid(),
                    'ready_time': time.time(),
                    'metadata_count': len(self.metadata),
                    'flatpak_last_backup': self.last_flatpak_backup_time,
                    'version': '2.1'
                }, f, indent=2)
            logging.info(f"Created ready state file")
            return True
        except Exception as e:
            logging.error(f"Failed to create ready state: {e}")
            return False

    def _socket_listener_thread(self):
        """UNIX Socket listener for daemon communication."""
        control_socket_path = server.SOCKET_PATH + '.ctrl'
        self._remove_socket_file()

        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
                listener.bind(control_socket_path)
                listener.listen(1)
                logging.info(f"Listening for control commands on: {control_socket_path}")

                while not self.shutdown_event.is_set():
                    listener.settimeout(0.5)
                    try:
                        conn, _ = listener.accept()
                    except socket.timeout:
                        continue

                    with conn:
                        data = b''
                        while True:
                            chunk = conn.recv(4096)
                            if not chunk:
                                break
                            data += chunk

                        if data:
                            try:
                                command_obj = json.loads(data.decode('utf-8'))
                                command = command_obj.get('command')

                                if command == 'cancel':
                                    logging.warning("Received 'cancel' command. Initiating shutdown.")
                                    self.shutdown_event.set()
                            except Exception as e:
                                logging.error(f"Error processing control command: {e}")

        except Exception as e:
            logging.error(f"Control socket listener failed: {e}")
            self.shutdown_event.set()
        finally:
            self._remove_socket_file()

    def _remove_ready_state(self):
        """Remove ready state file."""
        try:
            if os.path.exists(self.ready_file_path):
                os.remove(self.ready_file_path)
        except:
            pass

    def _remove_socket_file(self):
        """Remove socket file."""
        try:
            control_socket_path = server.SOCKET_PATH + '.ctrl'
            if os.path.exists(control_socket_path):
                try:
                    os.remove(control_socket_path)
                    logging.info(f"Removed control socket: {control_socket_path}")
                except Exception as e:
                    logging.error(f"Error removing control socket: {e}")
        except:
            pass

    def _create_lock_file(self):
        """Create lock file."""
        try:
            with open(self.lock_file_path, 'w') as f:
                f.write(str(os.getpid()))
            return True
        except Exception as e:
            logging.error(f"Failed to create lock file: {e}")
            return False

    def _remove_lock_file(self):
        """Remove lock file."""
        try:
            if os.path.exists(self.lock_file_path):
                os.remove(self.lock_file_path)
        except:
            pass

    # =========================================================================
    # PATH MANAGEMENT
    # =========================================================================
    def _get_target_folders(self) -> List[str]:
        """Get list of folders to watch."""
        folders_str = server.get_database_value('BACKUP_FOLDERS', 'folders')
        if not folders_str:
            return []

        target_folders = [f.strip() for f in folders_str.split(',') if f.strip()]
        valid_folders = []

        for folder in target_folders:
            folder = os.path.abspath(os.path.expanduser(folder))
            if os.path.exists(folder):
                valid_folders.append(folder)

        return valid_folders

    def _should_exclude(self, path: str) -> bool:
        """Check if path should be excluded."""
        if self._exclude_hidden:
            relative = os.path.relpath(path, self.users_home_dir)
            if any(part.startswith('.') for part in relative.split(os.sep)):
                return True

        filename = os.path.basename(path)
        if any(fnmatch.fnmatch(filename, p) for p in self.excludes_extras):
            return True

        return False

    # =========================================================================
    # WORKER THREAD
    # =========================================================================
    def watch_worker(self):
        """Main worker thread that processes events in batches."""
        logging.info("Worker thread started")

        while not self.shutdown_event.is_set():
            try:
                try:
                    first_event = self.event_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                batch = [first_event]
                batch_size = self._calculate_optimal_batch_size(self.event_queue.qsize())

                try:
                    while len(batch) < batch_size:
                        batch.append(self.event_queue.get_nowait())
                except queue.Empty:
                    pass

                unique_events = self._deduplicate_batch(batch)

                futures = []
                for event_data in unique_events.values():
                    if self.shutdown_event.is_set():
                        break

                    future = self.executor.submit(
                        self._process_event_wrapper,
                        event_data
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"Worker error: {e}")

            except Exception as e:
                logging.error(f"Worker loop error: {e}")
                time.sleep(0.1)

        logging.info("Worker thread stopped")

    def _calculate_optimal_batch_size(self, queue_size: int) -> int:
        """Calculate optimal batch size based on system load."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0)
        except:
            cpu_percent = 50

        batch_size = BASE_BATCH_SIZE

        if cpu_percent > HIGH_CPU_THRESHOLD:
            batch_size = max(MIN_BATCH_SIZE, BASE_BATCH_SIZE // 2)
        elif cpu_percent < 30:
            batch_size = int(BASE_BATCH_SIZE * 1.5)

        if queue_size > batch_size * 2:
            batch_size = min(MAX_BATCH_SIZE, batch_size * 2)

        return max(MIN_BATCH_SIZE, min(MAX_BATCH_SIZE, batch_size))

    def _deduplicate_batch(self, batch: List[Tuple]) -> Dict[str, Tuple]:
        """De-duplicate events in batch, keeping last event per path."""
        unique = {}

        for event in batch:
            event_type, src_path, dest_path = event

            if event_type == 'moved' and dest_path:
                unique[f"move_{dest_path}"] = event
            else:
                unique[src_path] = event

        return unique

    def _process_event_wrapper(self, event_data: Tuple):
        """Wrapper to process different event types."""
        event_type, src_path, dest_path = event_data

        try:
            if event_type == 'deleted':
                self._handle_file_deletion(src_path)
            elif event_type == 'moved' and dest_path:
                self._handle_file_move(src_path, dest_path)
            else:
                self._process_file_change(src_path, event_type)
        except Exception as e:
            logging.error(f"Error processing {event_type} for {src_path}: {e}")

    # =========================================================================
    # FILE PROCESSING
    # =========================================================================
    def _process_file_change(self, path: str, event_type: str):
        """Process file creation or modification."""
        rel_path = os.path.relpath(path, self.users_home_dir)

        # Check if file is already being processed
        with self.processing_lock:
            if rel_path in self.processing_files:
                logging.debug(f"Skipping {rel_path}: Already being processed by another thread")
                return
            # Mark as being processed
            self.processing_files.add(rel_path)

        try:
            self._process_file_change_internal(path, event_type, rel_path)
        finally:
            # Always remove from processing set when done
            with self.processing_lock:
                self.processing_files.discard(rel_path)

    def _process_file_change_internal(self, path: str, event_type: str, rel_path: str):
        """Internal file processing logic."""
        if not os.path.exists(path):
            logging.debug(f"Skipping {rel_path}: File does not exist")
            return

        file_size = 0

        # Robust stat check with retry
        stat_result = None
        for attempt in range(3):
            try:
                stat_result = os.stat(path)
                file_size = stat_result.st_size
                break
            except (OSError, PermissionError) as e:
                if attempt < 2:
                    logging.debug(f"Stat attempt {attempt + 1} failed for {rel_path}. Retrying...")
                    time.sleep(0.1)
                else:
                    logging.error(f"Stat failed for {rel_path} after 3 attempts: {e}")
                    self._send_file_status(rel_path, 'Failed (Stat Error)', 0, 'error')
                    return
            except FileNotFoundError:
                logging.debug(f"Skipping {rel_path}: File disappeared")
                return

        if not stat_result:
            logging.debug(f"Skipping {rel_path}: Could not stat file")
            return

        current_mtime = stat_result.st_mtime

        try:
            # Check cooldown
            current_time = time.time()
            last_time = self.last_processed_time.get(rel_path, 0)
            if current_time - last_time < MIN_REPROCESS_INTERVAL:
                logging.debug(f"Cooldown active for {rel_path} (last processed {int(current_time - last_time)}s ago)")
                return

            # Calculate hash
            logging.debug(f"Calculating hash for {rel_path} ({file_size} bytes)")
            file_hash = calculate_sha256(path, file_size=file_size)

            if not file_hash:
                logging.warning(f"File {rel_path} persistently locked or unreadable. Deferring.")
                return

            logging.debug(f"Hash calculated for {rel_path}: {file_hash[:16]}...")

            # Check if content changed
            metadata = self.metadata.get(rel_path, {})
            if metadata.get('hash') == file_hash:
                with self.state_lock:
                    self.metadata.setdefault(rel_path, {})['mtime'] = current_mtime
                    self.last_processed_time[rel_path] = current_time
                logging.debug(f"File unchanged: {rel_path} (hash match)")
                return


            # RESTORE DETECTOR
            # =========================================================================
            # # Check for restore
            # backup_locations = self._find_backup_locations_by_hash(file_hash)

            # if backup_locations:
            #     try:
            #         backup_stat = os.stat(backup_locations[0])
            #         if current_mtime > backup_stat.st_mtime:
            #             logging.info(f"RESTORE detected: {rel_path}")
            #             self._update_metadata_restore(rel_path, current_mtime, file_size, file_hash)
            #             return
            #     except FileNotFoundError:
            #         pass

            is_new = rel_path not in self.metadata
            existing_backup = self.hash_to_path_map.get(file_hash)

            file_info = {
                'source_path': path,
                'rel_path': rel_path,
                'file_hash': file_hash,
                'size': file_size,
                'mtime': current_mtime,
                'is_hardlink_candidate': existing_backup is not None,
                'existing_path': existing_backup,
                'new_file': is_new,
                'event_type': event_type
            }

            logging.info(f"Processing {rel_path} ({file_size} bytes, {'new' if is_new else 'modified'})")
            self._send_file_status(rel_path, 'Processing', file_size, 'processing')

            success = self._process_single_file_sync(file_info)

            if success:
                logging.info(f"Successfully backed up {rel_path}")
                self._send_file_status(rel_path, 'Backed Up', file_size, 'success')
                with self.state_lock:
                    self.last_processed_time[rel_path] = current_time
            else:
                logging.error(f"Failed to back up {rel_path}")
                self._send_file_status(rel_path, 'Failed (Copy Error)', file_size, 'error')

        except FileNotFoundError:
            logging.debug(f"File {path} disappeared during processing")
            return
        except PermissionError:
            logging.error(f"Permission denied: {path}")
            self._send_file_status(rel_path, 'Failed (Permission Denied)', file_size, 'error')
        except Exception as e:
            logging.error(f"Error processing {path}: {e}", exc_info=True)
            self._send_file_status(rel_path, 'Failed (Unknown Error)', file_size, 'error')

    def _check_if_restore(self, rel_path: str, current_hash: str, current_mtime: float) -> bool:
        """Check if file was restored from backup."""
        # Method 1: Check if file recently appeared with OLD content
        if rel_path not in self.metadata:
            return False  # New file, not restore
            
        old_meta = self.metadata.get(rel_path)
        if not old_meta:
            return False
            
        old_hash = old_meta.get('hash')
        
        # If hash matches backup but file is NEWER, might be restore
        if old_hash == current_hash:
            # Check if backup file exists and is OLDER
            backup_path = old_meta.get('path')
            if backup_path and os.path.exists(backup_path):
                backup_mtime = os.stat(backup_path).st_mtime
                
                # RESTORE = current file is IDENTICAL to backup but TIMESTAMP is newer
                # This could indicate a restore operation
                if abs(current_mtime - backup_mtime) < 5:  # Within 5 seconds
                    logging.info(f"Possible restore: {rel_path}")
                    return True
                    
        return False

    def _process_single_file_sync(self, file_info: Dict[str, Any], retries: int = 3) -> bool:
        """
        Atomically processes a single file with MINIMAL locking.
        Only locks during the atomic rename, not the entire copy.
        """
        source_path = file_info['source_path']
        rel_path = file_info['rel_path']
        file_hash = file_info['file_hash']
        is_hardlink_candidate = file_info['is_hardlink_candidate']

        backup_dir = server.app_main_backup_dir()

        # Define target path first
        target_path = os.path.join(backup_dir, rel_path)
        target_dir = os.path.dirname(target_path)

        # CRITICAL FIX: Use temp file in the SAME directory as target
        # This ensures os.rename() works (same filesystem) and has enough space
        temp_filename = f".tmp_{uuid.uuid4().hex}_{os.path.basename(target_path)}"
        temp_path = os.path.join(target_dir, temp_filename)

        # Create target directory
        try:
            os.makedirs(target_dir, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create directory {target_dir}: {e}")
            return False

        # Copy/hardlink to temp location (NO LOCKING)
        success = False
        for attempt in range(retries):
            try:
                if is_hardlink_candidate:
                    existing_path = self.hash_to_path_map.get(file_hash)
                    if existing_path and os.path.exists(existing_path):
                        os.link(existing_path, temp_path)
                        logging.debug(f"Hardlinked {rel_path}")
                    else:
                        shutil.copy2(source_path, temp_path)
                        logging.debug(f"Copied {rel_path} (hardlink failed)")
                else:
                    shutil.copy2(source_path, temp_path)
                    logging.debug(f"Copied {rel_path}")

                success = True
                break

            except (OSError, PermissionError) as e:
                if attempt < retries - 1:
                    wait_time = 0.5 * (attempt + 1)
                    logging.warning(f"Copy attempt {attempt + 1} failed for {rel_path}: {e}. Retry in {wait_time}s")
                    time.sleep(wait_time)
                else:
                    logging.error(f"Failed to copy {rel_path} after {retries} attempts: {e}")
                    if os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except:
                            pass
                    return False

        if not success:
            return False

        # Atomic rename with SHORT lock
        lock_acquired = False
        try:
            lock_acquired = self._acquire_file_lock(target_path, timeout=10)

            if not lock_acquired:
                logging.error(f"Could not acquire lock for {target_path}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return False

            # Check if target exists and is identical
            if os.path.exists(target_path):
                existing_hash = calculate_sha256(target_path)
                if existing_hash == file_hash:
                    logging.debug(f"Target {target_path} already correct")
                    os.remove(temp_path)
                    self._update_metadata_backup(rel_path, file_info['mtime'], file_info['size'],
                                                 file_hash, target_path)
                    return True

            # Atomic rename
            os.rename(temp_path, target_path)

            # Update metadata
            self._update_metadata_backup(rel_path, file_info['mtime'], file_info['size'],
                                         file_hash, target_path)

            return True

        except Exception as e:
            logging.error(f"Failed atomic rename for {rel_path}: {e}", exc_info=True)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            return False
        finally:
            if lock_acquired:
                self._release_file_lock(target_path)

    def _update_metadata_backup(self, rel_path: str, mtime: float, size: int,
                                file_hash: str, backup_path: str):
        """Update metadata after successful backup."""
        with self.state_lock:
            self.metadata[rel_path] = {
                'path': backup_path,
                'mtime': mtime,
                'size': size,
                'hash': file_hash,
            }
            self.hash_to_path_map[file_hash] = backup_path

        """
        Enhanced File Move Detection and Backup Synchronization
        Detects when files are moved/renamed in the user's home directory
        and updates their locations in both main and incremental backups.
        """

    def _handle_file_move(self, src_path: str, dest_path: str):
        """
        Enhanced file move handler that updates backup locations.
        
        Handles three scenarios:
        1. File moved to a different directory
        2. File renamed in same directory
        3. File moved AND renamed
        """
        if not os.path.exists(dest_path):
            logging.info(f"Destination no longer exists, treating as deletion: {dest_path}")
            self._handle_file_deletion(src_path)
            return

        src_rel = os.path.relpath(src_path, self.users_home_dir)
        dest_rel = os.path.relpath(dest_path, self.users_home_dir)

        logging.info(f"File moved: {src_rel} -> {dest_rel}")

        # Calculate hash of the moved file
        file_hash = calculate_sha256(dest_path)
        if not file_hash:
            logging.warning(f"Cannot calculate hash for moved file: {dest_path}")
            # Fall back to treating as new file
            self._process_file_change(dest_path, 'created')
            return

        # Find ALL backup locations for this file (main + incrementals)
        backup_locations = self._find_all_backup_locations(src_rel, file_hash)

        if not backup_locations:
            logging.info(f"No backup found for {src_rel}, treating as new file")
            self._process_file_change(dest_path, 'created')
            return

        # Verify hash matches
        primary_backup = backup_locations[0]
        backup_hash = calculate_sha256(primary_backup)
        
        if backup_hash != file_hash:
            logging.warning(f"File content changed during move: {src_rel}")
            # Content changed - backup as modified file
            self._process_file_change(dest_path, 'modified')
            return

        # Content is identical - just update locations
        stat_result = os.stat(dest_path)
        
        # Update ALL backup locations (main + incrementals)
        success_count = 0
        for backup_path in backup_locations:
            if self._rename_in_backup_location(backup_path, dest_rel, file_hash, stat_result):
                success_count += 1
                logging.info(f"Updated backup location: {backup_path}")
            else:
                logging.warning(f"Failed to update backup location: {backup_path}")

        # Update metadata
        with self.state_lock:
            if src_rel in self.metadata:
                old_meta = self.metadata[src_rel].copy()
                del self.metadata[src_rel]
                
                # Update metadata with new location
                self.metadata[dest_rel] = old_meta
                self.metadata[dest_rel]['mtime'] = stat_result.st_mtime
                self.metadata[dest_rel]['renamed_from'] = src_rel
                self.metadata[dest_rel]['renamed_at'] = time.time()
                
                # Update hash map
                if file_hash in self.hash_to_path_map:
                    old_backup_path = self.hash_to_path_map[file_hash]
                    new_backup_path = old_backup_path.replace(src_rel, dest_rel)
                    self.hash_to_path_map[file_hash] = new_backup_path

        # Send status update
        self._send_file_status(dest_rel, 'Moved', stat_result.st_size, 'success')
        
        logging.info(f"Successfully processed move: {success_count}/{len(backup_locations)} backups updated")

    def _find_all_backup_locations(self, rel_path: str, file_hash: str) -> List[str]:
        """
        Find ALL backup locations for a file (main backup + all incrementals).
        
        Returns list of absolute paths to backup files, ordered by priority:
        1. Main backup location
        2. Most recent incremental
        3. Older incrementals
        """
        locations = []
        
        # 1. Check main backup
        main_backup_path = os.path.join(self.app_main_backup_dir, rel_path)
        if os.path.exists(main_backup_path):
            locations.append(main_backup_path)
        
        # 2. Check metadata for hash-based locations
        with self.state_lock:
            for path_key, meta in self.metadata.items():
                if meta.get('hash') == file_hash:
                    backup_path = meta.get('path')
                    if backup_path and os.path.exists(backup_path) and backup_path not in locations:
                        locations.append(backup_path)
        
        # 3. Check all incremental backup directories
        if os.path.exists(self.app_incremental_backup_dir):
            incremental_locations = []
            
            # Walk through date folders (YYYY-MM-DD)
            for date_folder in os.listdir(self.app_incremental_backup_dir):
                date_path = os.path.join(self.app_incremental_backup_dir, date_folder)
                if not os.path.isdir(date_path):
                    continue
                
                # Walk through time folders (HH_MM_SS)
                for time_folder in os.listdir(date_path):
                    time_path = os.path.join(date_path, time_folder)
                    if not os.path.isdir(time_path):
                        continue
                    
                    # Check for the file in this incremental backup
                    incremental_file = os.path.join(time_path, rel_path)
                    if os.path.exists(incremental_file):
                        # Verify hash matches
                        inc_hash = calculate_sha256(incremental_file)
                        if inc_hash == file_hash:
                            # Store with timestamp for sorting
                            timestamp = f"{date_folder}_{time_folder}"
                            incremental_locations.append((timestamp, incremental_file))
            
            # Sort incrementals by timestamp (newest first) and add to locations
            incremental_locations.sort(reverse=True)
            locations.extend([path for _, path in incremental_locations])
        
        return locations


    def _handle_file_deletion(self, path: str):
        """Mark file as deleted in metadata."""
        rel_path = os.path.relpath(path, self.users_home_dir)

        with self.state_lock:
            if rel_path in self.metadata:
                self.metadata[rel_path]['deleted'] = True
                self.metadata[rel_path]['deleted_time'] = time.time()

                file_hash = self.metadata[rel_path].get('hash')
                if file_hash:
                    all_refs = [k for k, v in self.metadata.items()
                               if v.get('hash') == file_hash and not v.get('deleted', False)]
                    if not all_refs and file_hash in self.hash_to_path_map:
                        del self.hash_to_path_map[file_hash]

        self._send_file_status(rel_path, 'Deleted', 0, 'error')
        logging.info(f"Marked as deleted: {rel_path}")

    def _rename_in_backup_location(self, old_backup_path: str, dest_rel_path: str,
                                file_hash: str, stat_result: os.stat_result) -> bool:
        """
        Rename/move file in a specific backup location (main or incremental).
        
        Uses atomic operations with proper locking.
        """
        try:
            # Determine the backup root (main or incremental)
            if old_backup_path.startswith(self.app_main_backup_dir):
                backup_root = self.app_main_backup_dir
            else:
                # For incrementals, find the root (date/time folder)
                # Structure: .../incremental/YYYY-MM-DD/HH_MM_SS/rel_path
                parts = old_backup_path.split(os.sep)
                try:
                    # Find the incremental root
                    inc_index = parts.index(os.path.basename(self.app_incremental_backup_dir))
                    # Root is: incremental/date/time
                    backup_root = os.sep.join(parts[:inc_index + 3])
                except (ValueError, IndexError):
                    logging.error(f"Cannot determine backup root for: {old_backup_path}")
                    return False
            
            # Construct new backup path
            new_backup_path = os.path.join(backup_root, dest_rel_path)
            
            # Nothing to do if paths are identical
            if old_backup_path == new_backup_path:
                logging.debug(f"Backup path unchanged: {old_backup_path}")
                return True
            
            # Ensure destination directory exists
            new_backup_dir = os.path.dirname(new_backup_path)
            os.makedirs(new_backup_dir, exist_ok=True)
            
            # Acquire locks for both old and new paths
            old_lock_acquired = self._acquire_file_lock(old_backup_path, timeout=10)
            if not old_lock_acquired:
                logging.error(f"Cannot acquire lock for source: {old_backup_path}")
                return False
            
            try:
                new_lock_acquired = self._acquire_file_lock(new_backup_path, timeout=10)
                if not new_lock_acquired:
                    logging.error(f"Cannot acquire lock for destination: {new_backup_path}")
                    return False
                
                try:
                    # Check if destination already exists
                    if os.path.exists(new_backup_path):
                        # Verify it's the same file
                        existing_hash = calculate_sha256(new_backup_path)
                        if existing_hash == file_hash:
                            # Destination is already correct, just remove old
                            os.remove(old_backup_path)
                            logging.info(f"Removed old backup (destination exists): {old_backup_path}")
                            return True
                        else:
                            # Conflict - don't overwrite different file
                            logging.warning(f"Conflict: destination exists with different content: {new_backup_path}")
                            return False
                    
                    # Perform the rename
                    try:
                        # Try atomic rename first (same filesystem)
                        os.rename(old_backup_path, new_backup_path)
                        logging.debug(f"Renamed via os.rename: {old_backup_path} -> {new_backup_path}")
                        return True
                        
                    except OSError as e:
                        if e.errno == errno.EXDEV:
                            # Cross-filesystem - use copy + delete
                            logging.debug(f"Cross-filesystem move detected, using copy")
                            shutil.copy2(old_backup_path, new_backup_path)
                            os.remove(old_backup_path)
                            logging.debug(f"Moved via copy: {old_backup_path} -> {new_backup_path}")
                            return True
                        else:
                            raise
                
                finally:
                    self._release_file_lock(new_backup_path)
            
            finally:
                self._release_file_lock(old_backup_path)
        
        except Exception as e:
            logging.error(f"Failed to rename backup {old_backup_path} -> {new_backup_path}: {e}", exc_info=True)
            return False
        
    def _cleanup_empty_backup_dirs(self, backup_path: str):
        """
        Clean up empty directories left after file moves.
        Walks up the directory tree removing empty dirs.
        """
        try:
            current_dir = os.path.dirname(backup_path)
            
            # Don't remove backup root directories
            protected_roots = [
                self.app_main_backup_dir,
                self.app_incremental_backup_dir,
                self.app_backup_dir
            ]
            
            while current_dir and current_dir not in protected_roots:
                try:
                    # Check if directory is empty
                    if not os.listdir(current_dir):
                        logging.debug(f"Removing empty directory: {current_dir}")
                        os.rmdir(current_dir)
                        current_dir = os.path.dirname(current_dir)
                    else:
                        # Directory not empty, stop
                        break
                except (OSError, PermissionError):
                    break
        
        except Exception as e:
            logging.debug(f"Error cleaning up empty dirs: {e}")

    def _detect_and_sync_moved_files(self):
        """
        Periodic scan to detect files that were moved while daemon was offline.
        Compares current file locations with metadata to find moves.
        """
        logging.info("Starting moved file detection scan...")
        
        moved_files_found = 0
        synced_successfully = 0
        
        try:
            # Build hash -> current location map
            current_hash_locations = {}
            
            for folder in self._get_target_folders():
                if self.shutdown_event.is_set():
                    break
                
                for root, dirs, files in os.walk(folder):
                    if self.shutdown_event.is_set():
                        break
                    
                    # Skip excluded directories
                    dirs[:] = [d for d in dirs if not self._should_exclude(os.path.join(root, d))]
                    
                    for filename in files:
                        if self.shutdown_event.is_set():
                            break
                        
                        filepath = os.path.join(root, filename)
                        
                        if self._should_exclude(filepath):
                            continue
                        
                        try:
                            # Calculate hash
                            file_hash = calculate_sha256(filepath)
                            if not file_hash:
                                continue
                            
                            rel_path = os.path.relpath(filepath, self.users_home_dir)
                            
                            # Store current location for this hash
                            if file_hash not in current_hash_locations:
                                current_hash_locations[file_hash] = []
                            current_hash_locations[file_hash].append(rel_path)
                        
                        except Exception as e:
                            logging.debug(f"Error processing {filepath}: {e}")
                            continue
            
            # Compare with metadata to detect moves
            with self.state_lock:
                for old_rel_path, meta in list(self.metadata.items()):
                    if self.shutdown_event.is_set():
                        break
                    
                    file_hash = meta.get('hash')
                    if not file_hash:
                        continue
                    
                    # Skip deleted files
                    if meta.get('deleted'):
                        continue
                    
                    # Check if file exists at old location
                    old_full_path = os.path.join(self.users_home_dir, old_rel_path)
                    if os.path.exists(old_full_path):
                        # File still at original location
                        continue
                    
                    # File not at old location - check if it moved
                    current_locations = current_hash_locations.get(file_hash, [])
                    
                    if not current_locations:
                        # File deleted
                        logging.debug(f"File deleted: {old_rel_path}")
                        self._handle_file_deletion(old_full_path)
                        continue
                    
                    # File moved to new location(s)
                    for new_rel_path in current_locations:
                        if new_rel_path == old_rel_path:
                            continue
                        
                        moved_files_found += 1
                        logging.info(f"Detected moved file: {old_rel_path} -> {new_rel_path}")
                        
                        # Sync backup locations
                        new_full_path = os.path.join(self.users_home_dir, new_rel_path)
                        
                        # Simulate move event
                        try:
                            self._handle_file_move(old_full_path, new_full_path)
                            synced_successfully += 1
                        except Exception as e:
                            logging.error(f"Error syncing moved file {old_rel_path}: {e}")
            
            if moved_files_found > 0:
                logging.info(f"Moved file detection complete: {synced_successfully}/{moved_files_found} synced successfully")
                # Save updated metadata
                server.save_metadata(self.metadata)
            else:
                logging.info("No moved files detected")
        
        except Exception as e:
            logging.error(f"Error in moved file detection: {e}", exc_info=True)

    # =========================================================================
    # METADATA MANAGEMENT
    # =========================================================================
    def _load_metadata(self):
        """Load metadata from disk."""
        if not os.path.exists(server.METADATA_FILE):
            logging.info("No metadata file found, starting fresh")
            self.metadata = {}
            self.hash_to_path_map = {}
            return

        try:
            with open(server.METADATA_FILE, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)

            self.hash_to_path_map = {}
            for key, val in self.metadata.items():
                file_hash = val.get('hash')
                backup_path = val.get('path')

                if file_hash and backup_path:
                    if backup_path.startswith(self.app_main_backup_dir):
                        self.hash_to_path_map[file_hash] = backup_path
                    elif file_hash not in self.hash_to_path_map:
                        self.hash_to_path_map[file_hash] = backup_path

            logging.info(f"Loaded {len(self.metadata)} metadata entries")
        except Exception as e:
            logging.error(f"Failed to load metadata: {e}")
            self.metadata = {}
            self.hash_to_path_map = {}

    def _update_metadata_restore(self, rel_path, mtime, size, file_hash):
        """Update metadata for restored file."""
        with self.state_lock:
            if rel_path in self.metadata:
                self.metadata[rel_path].update({
                    'mtime': mtime,
                    'restored': True,
                    'restore_time': time.time()
                })
            else:
                dest = os.path.join(self.app_main_backup_dir, rel_path)
                self.metadata[rel_path] = {
                    'path': dest,
                    'mtime': mtime,
                    'size': size,
                    'hash': file_hash,
                    'restored': True,
                    'restore_time': time.time()
                }
                self.hash_to_path_map[file_hash] = dest

    def _find_backup_locations_by_hash(self, file_hash: str) -> List[str]:
        """Find backup locations by hash."""
        locations = []

        with self.state_lock:
            for rel_path, meta in self.metadata.items():
                if meta.get('hash') == file_hash:
                    backup_path = meta.get('path')
                    if backup_path and os.path.exists(backup_path):
                        locations.append(backup_path)

        return list(set(locations))

    # =========================================================================
    # MESSAGING
    # =========================================================================
    def _send_file_status(self, rel_path: str, title: str, size: int, status: str):
        """Send file status message."""
        try:
            display_path = _truncate_path(rel_path)
            self.message_queue.put({
                'type': 'file_activity',
                'title': title,
                'description': display_path,
                'size': size,
                'status': status,
                'timestamp': int(time.time())
            }, timeout=0.5)
        except Exception as e:
            logging.error(f"Send file status error: {e}")

    def message_sender_thread(self):
        """Thread to send queued messages."""
        logging.info("Message sender thread started")

        while not self.shutdown_event.is_set():
            try:
                msg = self.message_queue.get(timeout=0.5)
                self.message_sender.send_message_sync(msg)
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Message sender error: {e}")

        while not self.message_queue.empty():
            try:
                msg = self.message_queue.get_nowait()
                self.message_sender.send_message_sync(msg)
            except:
                break

        logging.info("Message sender thread stopped")

    # =========================================================================
    # SAFETY NET
    # =========================================================================
    def full_scan(self):
        """
        Enhanced full scan that includes moved file detection.
        Replaces the existing full_scan method.
        """
        logging.info("Starting enhanced full scan with move detection...")
        
        # Run moved file detection first
        self._detect_and_sync_moved_files()
        
        # Then run normal full scan for new/modified files
        self._scan_for_new_and_modified_files()
        
        logging.info("Enhanced full scan complete")

    def _scan_for_new_and_modified_files(self):
        """Scan for new and modified files (original full scan logic)."""
        logging.info("Scanning for new and modified files...")
        
        processed_count = 0
        skipped_count = 0
        
        for folder in self._get_target_folders():
            if self.shutdown_event.is_set():
                break
            
            if not os.path.isdir(folder):
                continue
            
            for root, dirs, files in os.walk(folder):
                if self.shutdown_event.is_set():
                    break
                
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not self._should_exclude(os.path.join(root, d))]
                
                for filename in files:
                    if self.shutdown_event.is_set():
                        break
                    
                    filepath = os.path.join(root, filename)
                    
                    if self._should_exclude(filepath):
                        continue
                    
                    try:
                        rel_path = os.path.relpath(filepath, self.users_home_dir)
                        stat_result = os.stat(filepath)
                        
                        # Check if file needs processing
                        current_time = time.time()
                        metadata = self.metadata.get(rel_path, {})
                        
                        # Skip if recently processed
                        if current_time - self.last_processed_time.get(rel_path, 0) < MIN_REPROCESS_INTERVAL:
                            skipped_count += 1
                            continue
                        
                        # Check if file changed
                        if metadata.get('mtime', 0) < stat_result.st_mtime - 1:  # 1 second tolerance
                            # Process file change
                            self._process_file_change(filepath, 'modified')
                            processed_count += 1
                        else:
                            skipped_count += 1
                            
                    except Exception as e:
                        logging.debug(f"Error scanning {filepath}: {e}")
                        continue
        
        logging.info(f"Scan complete: {processed_count} processed, {skipped_count} skipped")


# =============================================================================
# INTEGRATION INSTRUCTIONS
# =============================================================================
"""
To integrate this into your daemon.py:

1. Replace the existing _handle_file_move method with the enhanced version above

2. Add these new methods to the Daemon class:
   - _find_all_backup_locations
   - _cleanup_empty_backup_dirs
   - _detect_and_sync_moved_files
   - _enhanced_full_scan

3. Update the _rename_in_backup_location method with the improved version

4. In the main() function, replace the full_scan call with:
   
   if current_time - last_full_scan >= POLLING_INTERVAL:
       daemon._enhanced_full_scan()  # Use enhanced version
       generate_summary()
       last_full_scan = current_time

5. The enhanced system will now:
   - Detect when files are moved/renamed
   - Update ALL backup locations (main + incrementals)
   - Clean up empty directories after moves
   - Periodically scan for moves that happened while daemon was offline
   - Maintain consistent file paths across all backups
"""

# =============================================================================
# UTILITIES
# =============================================================================
def _truncate_path(path: str, max_len: int = 35) -> str:
    """Truncate long paths for display."""
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


def calculate_sha256(file_path: str, chunk_size: int = 65536, file_size: int = None, retries: int = 5) -> Optional[str]:
    """Calculate SHA256 hash with robust retry mechanism."""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    if file_size is None:
        try:
            file_size = os.stat(file_path).st_size
        except Exception:
            return None

    if file_size is not None and file_size == 0:
        return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    if file_size is not None and file_size > LARGE_FILE_THRESHOLD:
        return _calculate_large_file_signature(file_path, file_size, chunk_size)

    for attempt in range(retries):
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    sha256_hash.update(chunk)

            return sha256_hash.hexdigest()

        except (IOError, OSError) as e:
            if attempt < retries - 1:
                logging.debug(f"Hash attempt {attempt + 1} failed for {file_path}. Retrying in 0.5s")
                time.sleep(0.5)
            else:
                logging.warning(f"Failed to hash {file_path} after {retries} attempts: {e}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error hashing {file_path}: {e}")
            return None

    return None


def _calculate_large_file_signature(file_path: str, file_size: int, chunk_size: int) -> str:
    """Create signature for large files using sampling."""
    try:
        hasher = hashlib.sha256()
        st = os.stat(file_path)
        hasher.update(f"{file_size}-{st.st_mtime}".encode('utf-8'))

        with open(file_path, 'rb') as f:
            hasher.update(f.read(chunk_size))

            if file_size > chunk_size * 2:
                f.seek(file_size // 2)
                hasher.update(f.read(chunk_size))

            if file_size > chunk_size:
                f.seek(-chunk_size, 2)
                hasher.update(f.read(chunk_size))

        return "quick_" + hasher.hexdigest()
    except:
        return None


class Journal:
    """Simple append-only journal for recovery."""
    def __init__(self):
        self.path = server.JOURNAL_LOG_FILE
        self.lock = threading.Lock()

    def append_entry(self, op_type: str, payload: dict) -> str:
        """Append journal entry."""
        entry_id = uuid.uuid4().hex
        entry = {
            "id": entry_id,
            "time": time.time(),
            "type": op_type,
            "payload": payload,
            "status": "started"
        }

        with self.lock:
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + "\n")
                f.flush()

        return entry_id

    def mark_completed(self, entry_id: str):
        """Mark entry as completed."""
        entry = {"id": entry_id, "time": time.time(), "status": "completed"}

        with self.lock:
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + "\n")
                f.flush()

    def replay(self, daemon: 'Daemon'):
        """Replay incomplete operations."""
        if not os.path.exists(self.path):
            return

        logging.info("Replaying journal...")

        try:
            completed = set()
            incomplete = []

            with open(self.path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        e = json.loads(line)
                        if e.get('status') == 'completed':
                            completed.add(e.get('id'))
                        elif e.get('status') == 'started':
                            incomplete.append(e)
                    except:
                        continue

            for entry in incomplete:
                if entry.get('id') not in completed:
                    self._replay_entry(entry, daemon)
        except Exception as e:
            logging.error(f"Journal replay error: {e}")

    def _replay_entry(self, entry, daemon):
        """Replay single entry."""
        try:
            etype = entry.get('type')
            payload = entry.get('payload', {})

            if etype == 'copy':
                tmp = payload.get('tmp')
                if tmp and os.path.exists(tmp):
                    os.remove(tmp)
            elif etype == 'rename':
                old = payload.get('old_path')
                new = payload.get('new_path')
                if old and new and os.path.exists(old) and not os.path.exists(new):
                    os.rename(old, new)
        except:
            pass


class MessageSender:
    """Simplified message sender."""
    def __init__(self):
        self.socket_path = server.SOCKET_PATH
        self.timeout = 2

    def send_message_sync(self, message_data: dict) -> bool:
        """Send message via UNIX socket."""
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect(self.socket_path)
                sock.sendall((json.dumps(message_data) + "\n").encode("utf-8"))
            return True
        except Exception as e:
            logging.debug(f"Failed to send message: {e}")
            return False


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """Main entry point."""
    daemon = None
    watcher_thread = None
    observer = None
    message_thread = None
    control_thread = None

    def signal_handler(signum, frame):
        logging.info(f"Received signal {signum}")
        if daemon:
            daemon.shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        daemon = Daemon()

        if os.path.exists(daemon.lock_file_path):
            os.remove(daemon.lock_file_path)

        if not daemon._create_lock_file():
            logging.error("Could not create lock file")
            return

        atexit.register(daemon._remove_lock_file)

        daemon._load_metadata()
        daemon._create_ready_state()
        daemon.journal.replay(daemon)

        control_thread = threading.Thread(
            target=daemon._socket_listener_thread,
            daemon=True
        )
        control_thread.start()

        message_thread = threading.Thread(
            target=daemon.message_sender_thread,
            daemon=True
        )
        message_thread.start()

        event_handler = BackupChangeHandler(daemon)
        observer = Observer()

        for path in daemon._get_target_folders():
            if os.path.isdir(path):
                observer.schedule(event_handler, path, recursive=True)
                logging.info(f"Watching: {path}")

        observer.start()

        watcher_thread = threading.Thread(
            target=daemon.watch_worker,
            daemon=True
        )
        watcher_thread.start()

        logging.info("Daemon started successfully")

        last_full_scan = 0
        while not daemon.shutdown_event.is_set():
            current_time = time.time()

            if current_time - last_full_scan >= POLLING_INTERVAL:
                daemon.full_scan()
                generate_summary()
                last_full_scan = current_time

            daemon.check_and_backup_flatpaks()

            for _ in range(100):
                if daemon.shutdown_event.is_set():
                    break
                time.sleep(0.1)

    except Exception as e:
        logging.error(f"Main error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        logging.info("Shutting down...")

        if daemon:
            daemon.shutdown_event.set()

        if observer:
            observer.stop()

        if watcher_thread and watcher_thread.is_alive():
            watcher_thread.join(timeout=5)

        if message_thread and message_thread.is_alive():
            message_thread.join(timeout=2)

        if observer:
            observer.join(timeout=5)

        if daemon and hasattr(daemon, 'executor'):
            daemon.executor.shutdown(wait=True)

        if daemon:
            server.save_metadata(daemon.metadata)
            daemon._remove_lock_file()
            daemon._remove_ready_state()
            daemon._remove_socket_file()

        logging.info("Shutdown complete")


if __name__ == "__main__":
    if setproctitle:
        setproctitle.setproctitle(f'{server.APP_NAME} - daemon')

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)


