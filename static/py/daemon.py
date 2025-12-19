"""
Hybrid Daemon: Incremental, Atomic, and Concurrent File Backup Service
PURE THREADING MODEL: Eliminates async/threading complexity

[ARCHITECTURE]
1. Fast Path (Watchdog): Real-time events detected and queued
2. Worker Thread: Processes events in batches using ThreadPoolExecutor
3. Safety Net (Polling): Infrequent full scans catch missed events
4. Flatpak Backup: Periodic backup of installed Flatpak applications
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

# Watchdog imports
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import setproctitle
except ImportError:
    setproctitle = None

# --- GLOBAL SHARED STATE ---
server = SERVER()
EXPANDUSER = os.path.expanduser("~")
DEBOUNCE_COOLDOWN = 1.0  # 1s
_LAST_EVENT_TIME: Dict[str, float] = {}
DIR_PATTERNS = [".git", "node_modules", ".temp", "*.tmp", "__pycache__"]
FILE_PATTERNS = ["*.tmp"]


# --- CONFIGURATION ---
POLLING_INTERVAL = 1800  # 30 minutes
HIGH_CPU_THRESHOLD = 75.0
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50 MB
MIN_BATCH_SIZE = 10
BASE_BATCH_SIZE = 50
MAX_BATCH_SIZE = 200
# Minimum time to wait before processing the same file path again
MIN_REPROCESS_INTERVAL = 60  # 1 minute
# Flatpak backup interval (same as polling interval)
FLATPAK_BACKUP_INTERVAL = POLLING_INTERVAL


# ------------------------------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------------------------------
def _truncate_path(path: str, max_len: int = 35) -> str:
    """Truncate long paths for display."""
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


def calculate_sha256(file_path: str, chunk_size: int = 65536, file_size: int = None, retries: int = 3) -> Optional[str]:
    """
    Calculates the SHA256 hash of a file with a retry mechanism for I/O errors.
    This handles transient file locks (common with active image files).
    """
    
    # ------------------------------------------------------------------
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    # ------------------------------------------------------------------
    # Use the file's stat size if not provided
    if file_size is None:
        try:
            file_size = os.stat(file_path).st_size
        except OSError:
            pass # Continue, let the retry loop handle potential locks
            
    # ------------------------------------------------------------------
    if file_size is not None and file_size == 0: 
        return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

        # ------------------------------------------------------------------
    # Only sample large files if the file_size is known and exceeds threshold
    if file_size is not None and file_size > LARGE_FILE_THRESHOLD:
        # Assuming _calculate_large_file_signature handles its own I/O errors
        def _calculate_large_file_signature(file_path: str, file_size: int, chunk_size: int) -> str:
            """Create signature for large files using sampling."""
            try:
                hasher = hashlib.sha256()
                st = os.stat(file_path)
                hasher.update(f"{file_size}-{st.st_mtime}".encode('utf-8'))

                with open(file_path, 'rb') as f:
                    # Head
                    hasher.update(f.read(chunk_size))

                    # Middle
                    if file_size > chunk_size * 2:
                        f.seek(file_size // 2)
                        hasher.update(f.read(chunk_size))

                    # Tail
                    if file_size > chunk_size:
                        f.seek(-chunk_size, 2)
                        hasher.update(f.read(chunk_size))

                return "quick_" + hasher.hexdigest()
            except:
                return None
        return _calculate_large_file_signature(file_path, file_size, chunk_size)

    # Full hash with retry loop for smaller files (most images/documents)
    for attempt in range(retries):
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    sha256_hash.update(chunk)
            
            # Success
            return sha256_hash.hexdigest()

        except (OSError, PermissionError) as e:
            # Catch I/O errors like file in use (lock), permission denied
            if attempt < retries - 1:
                logging.debug(
                    f"Attempt {attempt + 1} of {retries} failed for {file_path}. Retrying in 0.5s.")
                time.sleep(0.5)
            else:
                logging.warning(
                    f"Failed to calculate hash for {file_path} after {retries} attempts: {e}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error while hashing {file_path}: {e}")
            return None

    return None

def _should_process(path: str) -> bool:
    """Check if file should be processed."""
    # ------------------------------------------------------------------
    if not os.path.exists(path):
        return False

    # ------------------------------------------------------------------
    def _should_exclude(path: str) -> bool:
        """Check if path should be excluded."""
        # Separate directory and file patterns
        all_patterns = DIR_PATTERNS + FILE_PATTERNS  # For backward compatibility
        
        _exclude_hidden_val = server.get_database_value('EXCLUDE', 'exclude_hidden_itens')
        _exclude_hidden = str(_exclude_hidden_val).lower() == 'true' if _exclude_hidden_val else False
        
        basename = os.path.basename(path)
        is_directory = os.path.isdir(path) if os.path.exists(path) else False
        
        # Check patterns
        for pattern in all_patterns:
            if fnmatch.fnmatch(basename, pattern):
                # If it's a directory pattern and we're checking a file inside it
                if pattern in DIR_PATTERNS and not is_directory:
                    # Check if parent directory matches the pattern
                    parent = os.path.dirname(path)
                    parent_name = os.path.basename(parent)
                    if fnmatch.fnmatch(parent_name, pattern):
                        return True
                return True
        
        # Hidden files/folders exclusion
        if _exclude_hidden:
            try:
                relative = os.path.relpath(path, EXPANDUSER)
                
                # Check if the file/directory itself is hidden
                if basename.startswith('.'):
                    return True
                
                # Check if any parent directory is hidden (except home directory)
                parts = relative.split(os.sep)
                for part in parts[:-1]:  # Exclude the last part (already checked)
                    if part.startswith('.'):
                        return True
                        
            except ValueError:
                pass
        
        return False
    if _should_exclude(path):
        return False
    
    # ------------------------------------------------------------------
    # Simple time-based debounce
    norm_path = os.path.normpath(path)
    current_time = time.time()

    if current_time - _LAST_EVENT_TIME.get(norm_path, 0) < DEBOUNCE_COOLDOWN:
        return False

    _LAST_EVENT_TIME[norm_path] = current_time
    return True


# ------------------------------------------------------------------
# WATCHDOG EVENT HANDLER
# ------------------------------------------------------------------
class BackupChangeHandler(FileSystemEventHandler):
    """Simplified event handler with basic debouncing."""
    def __init__(self, daemon: 'Daemon'):
        self.daemon = daemon
        self.queue = daemon.event_queue

    def on_any_event(self, event):
        """Universal event handler."""
        # ------------------------------------------------------------------
        # TO REMOVE
        # if event.is_directory:
        #     return
        
        # ------------------------------------------------------------------
        if not _should_process(event.src_path):
            return

        # ------------------------------------------------------------------
        try:
            src_path = os.path.normpath(event.src_path)
            dest_path = os.path.normpath(event.dest_path)
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
        self.app_main_backup_dir = server.app_main_backup_dir()
        self.app_incremental_backup_dir = server.app_incremental_backup_dir()
        self.app_backup_dir = server.devices_path()

        # ------------------------------------------------------------------
        # Threading setup
        cpu_count = os.cpu_count() or 4
        self.max_threads = min(32, cpu_count * 4)
        self.scan_threads = min(8, cpu_count * 2)
        self.executor = ThreadPoolExecutor(max_workers=self.max_threads, thread_name_prefix="FileWorker")

        # ------------------------------------------------------------------
        # Event queue for watchdog events
        self.event_queue = queue.Queue(maxsize=5000)
        self.message_queue = queue.Queue(maxsize=500)
        self.shutdown_event = threading.Event()

        # ------------------------------------------------------------------
        # State
        self.metadata = {}
        self.hash_to_path_map = {}
        self.journal = Journal()

        self.last_processed_time: Dict[str, float] = {}
        self.last_flatpak_backup_time = 0

        # ------------------------------------------------------------------
        # Daemon lock
        self.ready_file_path = os.path.join(EXPANDUSER, f'.{server.APP_NAME.lower()}_daemon_ready')
        self.lock_file_path = os.path.join(EXPANDUSER, f'.{server.APP_NAME.lower()}_daemon.lock')

        # ------------------------------------------------------------------
        # Progress tracking
        self.files_backed_up_count = 0
        self.total_size_transferred = 0
        self.backup_start_time = None
        self.total_files_to_scan = 0
        self.total_transfer_size = 0

        # ------------------------------------------------------------------
        # Locks
        self.state_lock = threading.Lock()
        self.file_locks = {}
        self.file_locks_access_lock = threading.Lock()

        # ------------------------------------------------------------------
        # Batching
        self.current_batch_size = BASE_BATCH_SIZE

        # ------------------------------------------------------------------
        # Settings
        self._watch_paths = self._get_target_folders()

        # ------------------------------------------------------------------
        # Message sender
        self.message_sender = MessageSender()


    # ---------------------------------------------------------------------------
    # SOCKET
    # ---------------------------------------------------------------------------
    def _socket_listener_thread(self): # Use this name for consistency with our threading plan
        """UNIX Socket listener for daemon communication."""

        # ---------------------------------------------------------------------------
        # Use the control path for commands from the web UI
        control_socket_path = server.SOCKET_PATH + '.ctrl' 

        # ---------------------------------------------------------------------------
        # Clean up the file path before binding
        self._remove_socket_file() # Requires your cleanup method (Step 1)

        # ---------------------------------------------------------------------------
        try:
            # Use your existing logic, but with the correct path and thread checks
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
                listener.bind(control_socket_path) 
                listener.listen(1)
                print("#" * 40)
                logging.info(f"Listening for control commands on UNIX socket: {control_socket_path}")

                while not self.shutdown_event.is_set():
                    listener.settimeout(0.5) # Allow thread to check shutdown_event
                    try:
                        conn, _ = listener.accept()
                    except socket.timeout:
                        continue # Check shutdown flag

                    with conn:
                        data = b''
                        while True:
                            chunk = conn.recv(4096)
                            if not chunk:
                                break
                            data += chunk

                        if data:
                            def _process_control_command(data: str):
                                """Processes commands received over the control socket."""
                                try:
                                    command_obj = json.loads(data)
                                    command = command_obj.get('command')
                                    
                                    if command == 'cancel':
                                        # This is the line that actually stops the daemon
                                        logging.warning("Received 'cancel' command. Initiating shutdown.")
                                        self.shutdown_event.set()
                                        # Note: You still need to implement sending 'ok' back to the client here
                                        
                                    # Add logic for other commands (e.g., 'status', 'start') here
                                except Exception as e:
                                    logging.error(f"Error processing control command data: {e}")
                            # Process the control data (e.g., '{"command": "cancel"}')
                            _process_control_command(data.decode('utf-8')) # New helper method
        except Exception as e:
            logging.error(f"CRITICAL: Control socket listener failed: {e}")
            self.shutdown_event.set()
        finally:
            self._remove_socket_file()


    # ---------------------------------------------------------------------------
    # BACKUP DEVICE
    # ---------------------------------------------------------------------------
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


    # ---------------------------------------------------------------------------
    # FLATPAK
    # ---------------------------------------------------------------------------
    def backup_flatpaks(self):
        """Backs up the list of installed Flatpak applications."""
        logging.info("Starting Flatpak application backup...")

        # ------------------------------------------------------------------
        if not self._has_driver_connection() or not self._is_backup_location_writable():
            logging.warning("Backup device not available or not writable. Skipping Flatpak backup.")
            return

        # ------------------------------------------------------------------
        commands_to_try = [
            server.GET_FLATPAKS_APPLICATIONS_NAME_CONTAINER.split(),
            server.GET_FLATPAKS_APPLICATIONS_NAME_NON_CONTAINER.split()
        ]

        def _execute_flatpak_command(command: List[str]) -> Optional[str]:
            """Execute flatpak command and return output."""
            try:
                result = sub.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=30,  # 30 second timeout
                    check=True
                )
                return result.stdout.strip()
            except sub.TimeoutExpired:
                logging.error(f"Flatpak command timed out: {command}")
                return None
            except sub.CalledProcessError as e:
                logging.error(f"Flatpak command failed (exit {e.returncode}): {e.stderr}")
                return None
            except Exception as e:
                return None
        output = None
        for command in commands_to_try:
            output = _execute_flatpak_command(command)
            if output is not None:
                break

        # ------------------------------------------------------------------
        if output is not None and output.strip():
            success = self._save_flatpak_list(output)
            if success:
                self.last_flatpak_backup_time = time.time()
                logging.info("Flatpak backup completed successfully")
        else:
            logging.error("All attempts to list Flatpak applications failed.")

    def _save_flatpak_list(self, flatpak_list: str) -> bool:
        """Save flatpak list to backup location."""

        # ------------------------------------------------------------------
        try:
            flatpak_backup_dir = os.path.join(self.app_backup_dir, "flatpaks")
            os.makedirs(flatpak_backup_dir, exist_ok=True)
            flatpak_file = os.path.join(flatpak_backup_dir, "flatpak_applications.txt")
            
            with open(flatpak_file, 'w') as f:
                f.write(flatpak_list)
            
            # Also save as JSON for easier parsing
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


    # ---------------------------------------------------------------------------
    # LOCK
    # ---------------------------------------------------------------------------
    def _create_ready_state(self):
        """Create ready state file."""
        
        # ------------------------------------------------------------------
        try:
            with open(self.ready_file_path, 'w') as f:
                json.dump({
                    'pid': os.getpid(),
                    'ready_time': time.time(),
                    'metadata_count': len(self.metadata),
                    'flatpak_last_backup': self.last_flatpak_backup_time,
                    'version': '2.1'
                }, f, indent=2)
            # logging.info(f"Created ready state file")
            return True
        except Exception as e:
            logging.error(f"Failed to create ready state: {e}")
            return False
        
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
            # 1. Define the correct control socket path
            control_socket_path = server.SOCKET_PATH + '.ctrl'
            
            # 2. Check if the file exists before trying to remove it
            if os.path.exists(control_socket_path):
                try:
                    # 3. Use os.remove to delete the stale socket file
                    os.remove(control_socket_path)
                    logging.info(f"Removed control socket: {control_socket_path}")
                except Exception as e:
                    # 4. Log any failure but do not crash the shutdown process
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

    def _acquire_file_lock(self, path: str, timeout: int = 5) -> bool:
        """Acquire file lock with timeout."""
        key = os.path.normpath(path)

        with self.file_locks_access_lock:
            if key not in self.file_locks:
                self.file_locks[key] = threading.Lock()
            lock = self.file_locks[key]

        return lock.acquire(timeout=timeout)

    def _release_file_lock(self, path: str):
        """Release file lock."""
        key = os.path.normpath(path)
        with self.file_locks_access_lock:
            if key in self.file_locks:
                try:
                    self.file_locks[key].release()
                except:
                    pass


    # ---------------------------------------------------------------------------
    # WATCHDOG
    # ---------------------------------------------------------------------------
    def _get_target_folders(self) -> List[str]:
        """Get list of folders to watch."""
        
        # ---------------------------------------------------------------------------
        folders_str = server.get_database_value('BACKUP_FOLDERS', 'folders')
        if not folders_str:
            return []

        # ---------------------------------------------------------------------------
        target_folders = [f.strip() for f in folders_str.split(',') if f.strip()]
        valid_folders = []
        for folder in target_folders:
            folder = os.path.abspath(os.path.expanduser(folder))
            if os.path.exists(folder):
                valid_folders.append(folder)

        return valid_folders


    # ---------------------------------------------------------------------------
    # WORKER THREAD - CORE EVENT PROCESSOR
    # ---------------------------------------------------------------------------
    def watch_worker(self):
        """Main worker thread that processes events in batches."""
        
        # ---------------------------------------------------------------------------
        while not self.shutdown_event.is_set():
            try:
                # Wait for first event with timeout
                try:
                    first_event = self.event_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                # ---------------------------------------------------------------------------
                # Collect batch
                def _calculate_optimal_batch_size(queue_size: int) -> int:
                    """Calculate optimal batch size based on system load."""
                    
                    # ---------------------------------------------------------------------------
                    try:
                        cpu_percent = psutil.cpu_percent(interval=0)
                    except:
                        cpu_percent = 50

                    # ---------------------------------------------------------------------------
                    batch_size = BASE_BATCH_SIZE
                    # High CPU: reduce batch
                    if cpu_percent > HIGH_CPU_THRESHOLD:
                        batch_size = max(MIN_BATCH_SIZE, BASE_BATCH_SIZE // 2)
                    # Low CPU: increase batch
                    elif cpu_percent < 30:
                        batch_size = int(BASE_BATCH_SIZE * 1.5)

                    # ---------------------------------------------------------------------------
                    # Large queue: boost processing
                    if queue_size > batch_size * 2:
                        batch_size = min(MAX_BATCH_SIZE, batch_size * 2)

                    # ---------------------------------------------------------------------------
                    return max(MIN_BATCH_SIZE, min(MAX_BATCH_SIZE, batch_size))
                batch = [first_event]
                batch_size = _calculate_optimal_batch_size(self.event_queue.qsize())
                try:
                    while len(batch) < batch_size:
                        batch.append(self.event_queue.get_nowait())
                except queue.Empty:
                    pass

                # ---------------------------------------------------------------------------
                # De-duplicate batch
                def _deduplicate_batch(batch: List[Tuple]) -> Dict[str, Tuple]:
                    """De-duplicate events in batch, keeping last event per path."""
                    unique = {}

                    for event in batch:
                        event_type, src_path, dest_path = event

                        if event_type == 'moved' and dest_path:
                            # Move events use destination as key
                            unique[f"move_{dest_path}"] = event
                        else:
                            # Other events use source path, last one wins
                            unique[src_path] = event

                    return unique
                unique_events = _deduplicate_batch(batch)
                # Process batch concurrently
                futures = []
                for event_data in unique_events.values():
                    if self.shutdown_event.is_set():
                        break

                    future = self.executor.submit(
                        self._process_event_wrapper,
                        event_data
                    )
                    futures.append(future)

                # ---------------------------------------------------------------------------
                # Wait for batch completion
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"Worker error: {e}")
            except Exception as e:
                logging.error(f"Worker loop error: {e}")
                time.sleep(0.1)

    def _process_event_wrapper(self, event_data: Tuple):
        """Wrapper to process different event types."""

        # ---------------------------------------------------------------------------
        event_type, src_path, dest_path = event_data
        try:
            if event_type == 'deleted':
                self._handle_file_deletion(src_path)
            elif event_type == 'moved' and dest_path:
                self._handle_file_move(src_path, dest_path)
            else:
                # created or modified
                self._process_file_change(src_path, event_type)
        except Exception as e:
            logging.error(f"Error processing {event_type} for {src_path}: {e}")


    # ---------------------------------------------------------------------------
    # MESSAGING - SIMPLIFIED
    # ---------------------------------------------------------------------------
    def _send_file_status(self, rel_path: str, title: str, size: int, status: str):
        """Send file status message."""
        
        # ---------------------------------------------------------------------------
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
            logging.error("Send file status error:", e)


    # ---------------------------------------------------------------------------
    # FILE PROCESSING
    # ---------------------------------------------------------------------------
    def _process_file_change(self, path: str, event_type: str):
        """Process file creation or modification."""

        # ---------------------------------------------------------------------------
        if not os.path.exists(path):
            return
        
        # ---------------------------------------------------------------------------
        rel_path = os.path.relpath(path, EXPANDUSER)
        
        # ---------------------------------------------------------------------------
        try:
            stat_result = os.stat(path)
            file_size = stat_result.st_size
            current_mtime = stat_result.st_mtime

            # ---------------------------------------------------------------------------
            # CHECK 0: Cooldown Period (1 Minute)
            # Skip processing if the file was successfully backed up recently.
            # ---------------------------------------------------------------------------
            current_time = time.time()
            last_time = self.last_processed_time.get(rel_path, 0)
            if current_time - last_time < MIN_REPROCESS_INTERVAL:
                logging.debug(f"Cooldown active for {rel_path}. Ignoring event.")
                return

            # ---------------------------------------------------------------------------
            # Calculate hash
            file_hash = calculate_sha256(path, file_size=file_size)
            if not file_hash:
                # Hash failed after retries (e.g., persistent file lock). Report error.
                self._send_file_status(rel_path, 'Failed (Locked/I/O)', file_size, 'error')
                return

            # ---------------------------------------------------------------------------
            # CHECK 1 (NEW ORDER): Has content changed since *last backup*?
            # If the hash is the same, it's just a time update (autosave/drift).
            # This check must come first to stop the false positive restore log.
            # ---------------------------------------------------------------------------
            metadata = self.metadata.get(rel_path, {})
            if metadata.get('hash') == file_hash:
                # Same content, update timestamp and exit.
                with self.state_lock:
                    self.metadata[rel_path]['mtime'] = current_mtime
                logging.debug(f"File unchanged: {rel_path}")
                return

            # # =========================================================
            # # CHECK 2: RESTORE/HARDLINK Candidate? (New content/new path)
            # # Check if the new hash matches an existing file in the global map.
            # # =========================================================
            # backup_locations = self._find_backup_locations_by_hash(file_hash)

            # if backup_locations:
            #     try:
            #         # RESTORE detected: Content matches an existing backup, and the source file is newer
            #         backup_stat = os.stat(backup_locations[0])
            #         if current_mtime > backup_stat.st_mtime:
            #             logging.info(f"RESTORE detected: {rel_path}")
            #             self._update_metadata_restore(rel_path, current_mtime, file_size, file_hash)
            #             return
            #         # If mtime is older or same, it falls through to be treated as a hardlink candidate
            #         # in the file_info section below.
            #     except FileNotFoundError:
            #         # Ignore if the backup file itself disappeared
            #         pass

            # ---------------------------------------------------------------------------
            # Determine if new file
            is_new = rel_path not in self.metadata
            existing_backup = self.hash_to_path_map.get(file_hash)

            # ---------------------------------------------------------------------------
            # Build file info
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

            # ---------------------------------------------------------------------------
            # Send processing status
            self._send_file_status(rel_path, 'Processing', file_size, 'processing')

            # ---------------------------------------------------------------------------
            # Process the file
            success = self._process_single_file_sync(file_info)
            if success:
                self._send_file_status(rel_path, 'Backed Up', file_size, 'success')
            else:
                self._send_file_status(rel_path, 'Failed (I/O Error)', file_size, 'error')
        except FileNotFoundError:
            # File disappeared during processing (e.g., temporary file). Clean exit.
            logging.warning(f"File {path} disappeared during processing. Treating as clean deletion.")
            return # Do not send 'Failed' status to the UI
        except PermissionError:
            # Likely cause for the SVG errors in icon directories
            # File disappeared during processing (e.g., temporary file). Clean exit.
            logging.error(f"Permission denied accessing file: {path}")
            self._send_file_status(rel_path, 'Failed (Permission Denied)', 0, 'error')
        except Exception as e:
            # Handle all other genuine errors (permissions, corrupted data, etc.)
            logging.error(f"Error processing file change for {path}: {e}")
            # Send failure status for genuine errors
            self._send_file_status(rel_path, 'Failed (System Error)', 0, 'error')
            
    def _process_single_file_sync(self, file_info: Dict[str, Any]) -> bool:
        """Core file processing logic."""

        # ---------------------------------------------------------------------------
        source = file_info['source_path']
        rel_path = file_info['rel_path']
        file_hash = file_info['file_hash']
        file_size = file_info['size']
        event_type = file_info.get('event_type', 'modified')
        is_new_file = file_info['new_file']
        is_hardlink_candidate = file_info['is_hardlink_candidate']

        # ---------------------------------------------------------------------------
        # Determine destination
        if is_new_file or event_type == 'created':
            dest = os.path.join(self.app_main_backup_dir, rel_path)
        else:
            dest = os.path.join(self.app_incremental_backup_dir, rel_path)

        # ---------------------------------------------------------------------------
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        # ---------------------------------------------------------------------------
        success: bool = False

        # ---------------------------------------------------------------------------
        try:
            # Handle special files
            def _handle_special_file(src_path: str, dst_path: str) -> bool:
                """Handle symlinks and special files."""
                try:
                    if not os.path.exists(src_path):
                        return False

                    mode = os.lstat(src_path).st_mode

                    if stat.S_ISLNK(mode):
                        link_target = os.readlink(src_path)
                        os.symlink(link_target, dst_path)
                        return True
                    elif stat.S_ISFIFO(mode):
                        os.mkfifo(dst_path)
                        return True
                    elif stat.S_ISSOCK(mode) or stat.S_ISCHR(mode) or stat.S_ISBLK(mode):
                        return True
                    return False
                except:
                    return False
            if _handle_special_file(source, dest):
                success = True
            # Try hardlink
            elif is_hardlink_candidate:
                existing = self.hash_to_path_map.get(file_hash)

                # ---------------------------------------------------------------------------
                def _try_hardlink(source_path: str, dest_path: str) -> bool:
                    """Attempt hardlink creation."""
                    try:
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        if os.path.exists(dest_path):
                            os.remove(dest_path)
                        os.link(source_path, dest_path)
                        try:
                            shutil.copystat(source_path, dest_path)
                        except:
                            pass
                        return True
                    except Exception:
                        return False
                if existing and _try_hardlink(existing, dest):
                    logging.info(f"Hardlinked: {rel_path}")
                    with self.state_lock:
                        self.files_backed_up_count += 1
                        self.total_size_transferred += file_size

                    # ---------------------------------------------------------------------------
                    success = True
            # ---------------------------------------------------------------------------
            # Atomic copy
            elif self._perform_atomic_copy(source, dest, file_hash, file_size):
                logging.info(f"Backed up: {rel_path} -> {dest}")
                # ---------------------------------------------------------------------------
                self.files_backed_up_count += 1
                # ---------------------------------------------------------------------------
                self.total_size_transferred += file_size
                # ---------------------------------------------------------------------------
                success = True
        except Exception as e:
            logging.error(f"Failed to process {rel_path}: {e}")

        # ---------------------------------------------------------------------------
        if success:
            def _update_metadata(rel_path: str, dst_path: str, file_info: dict):
                """Update metadata after successful backup."""
                with self.state_lock:
                    self.metadata[rel_path] = {
                        'path': dst_path,
                        'mtime': file_info.get('mtime', time.time()),
                        'size': file_info.get('size'),
                        'hash': file_info.get('file_hash'),
                    }

                    file_hash = file_info.get('file_hash')
                    if file_hash:
                        self.hash_to_path_map[file_hash] = dst_path
            _update_metadata(rel_path, dest, file_info)
            
            # ---------------------------------------------------------------------------
            self._send_progress_update(rel_path, file_size)
            
            # ---------------------------------------------------------------------------
            self.last_processed_time[file_info['rel_path']] = time.time()
        
        # ---------------------------------------------------------------------------
        return success

    def _handle_file_move(self, src_path: str, dest_path: str):
        """
        Enhanced file move handler that updates backup locations.
        
        Handles three scenarios:
        1. File moved to a different directory
        2. File renamed in same directory
        3. File moved AND renamed
        """

        # ---------------------------------------------------------------------------
        if not os.path.exists(dest_path):
            self._handle_file_deletion(src_path)
            return

        # ---------------------------------------------------------------------------
        src_rel = os.path.relpath(src_path, EXPANDUSER)
        dest_rel = os.path.relpath(dest_path, EXPANDUSER)
        
        # ---------------------------------------------------------------------------
        logging.info(f"File moved: {src_rel} -> {dest_rel}")

        # ---------------------------------------------------------------------------
        # Check if file content changed
        file_hash = calculate_sha256(dest_path)
        if not file_hash:
            # Fall back to treating as new file
            self._process_file_change(dest_path, 'created')
            return

        # ---------------------------------------------------------------------------
        backup_locations = self._find_all_backup_locations(src_path, file_hash)
        if not backup_locations:
            logging.info(f"No backup found for {src_rel}, treating as new file")
            self._process_file_change(dest_path, 'created')
            return

        # ---------------------------------------------------------------------------
        # Check if content changed
        primary_backup = backup_locations[0]
        backup_hash = calculate_sha256(primary_backup)
        if backup_hash != file_hash:
            # ---------------------------------------------------------------------------
            logging.warning(f"File content changed during move: {src_rel}")
            # ---------------------------------------------------------------------------
            self._process_file_change(dest_path, 'modified')
            # ---------------------------------------------------------------------------
            return

        # ---------------------------------------------------------------------------
        # Content is identical - just update locations
        stat_result = os.stat(dest_path)

        # ---------------------------------------------------------------------------
        # Update ALL backup locations (main + incrementals)
        success_count = 0
        for backup_path in backup_locations:
            def _rename_in_backup_location(old_backup_path: str, dest_rel_path: str,
                                        file_hash: str, stat_result: os.stat_result) -> bool:
                """
                Rename/move file in a specific backup location (main or incremental).
                
                Uses atomic operations with proper locking.
                """
                
                # ---------------------------------------------------------------------------
                try:
                    # Determine the backup root (main or incremental)
                    if old_backup_path.startswith(self.app_main_backup_dir):
                        backup_root = self.app_main_backup_dir
                    else:
                        # For incrementals, find the root (date/time folder)
                        # Structure: .../DD-MM-YYY/HH-MM/rel_path
                        parts = old_backup_path.split(os.sep)
                        
                        # ---------------------------------------------------------------------------
                        try:
                            # Find the incremental root
                            inc_index = parts.index(os.path.basename(self.app_incremental_backup_dir))
                            # Root is: incremental/date/time
                            backup_root = os.sep.join(parts[:inc_index + 3])
                        except (ValueError, IndexError):
                            logging.error(f"Cannot determine backup root for: {old_backup_path}")
                            return False
                    
                    # ---------------------------------------------------------------------------
                    # Construct new backup path
                    new_backup_path = os.path.join(backup_root, dest_rel_path)
                    
                    # ---------------------------------------------------------------------------
                    # Nothing to do if paths are identical
                    if old_backup_path == new_backup_path:
                        logging.debug(f"Backup path unchanged: {old_backup_path}")
                        return True
                    
                    # ---------------------------------------------------------------------------
                    # Ensure destination directory exists
                    new_backup_dir = os.path.dirname(new_backup_path)
                    os.makedirs(new_backup_dir, exist_ok=True)
                    
                    # ---------------------------------------------------------------------------
                    # Acquire locks for both old and new paths
                    old_lock_acquired = self._acquire_file_lock(old_backup_path, timeout=10)
                    if not old_lock_acquired:
                        logging.error(f"Cannot acquire lock for source: {old_backup_path}")
                        return False
                    
                    # ---------------------------------------------------------------------------
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
            # ---------------------------------------------------------------------------
            if _rename_in_backup_location(backup_path, dest_rel, file_hash, stat_result):
                success_count += 1

        # ---------------------------------------------------------------------------
        # Update metadata
        with self.state_lock:
            if src_rel in self.metadata:
                old_meta = self.metadata[src_rel]
                del self.metadata[src_rel]
                self.metadata[dest_rel] = old_meta
                self.metadata[dest_rel]['mtime'] = stat_result.st_mtime
                self.metadata[dest_rel]['renamed_from'] = src_rel
                
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
        
        # ---------------------------------------------------------------------------
        # Send status update
        self._send_file_status(dest_rel, 'Moved', stat_result.st_size, 'success')
        
        # ---------------------------------------------------------------------------
        logging.info(f"Successfully processed move: {success_count}/{len(backup_locations)} backups updated")

    def _handle_file_deletion(self, path: str):
        """Mark file as deleted in metadata."""
       
        # ---------------------------------------------------------------------------
        with self.state_lock:
            rel_path = os.path.relpath(path, EXPANDUSER)
            if rel_path in self.metadata:
                self.metadata[rel_path]['deleted'] = True
                self.metadata[rel_path]['deleted_time'] = time.time()

                # ---------------------------------------------------------------------------
                # Cleanup hash map if needed
                file_hash = self.metadata[rel_path].get('hash')
                if file_hash:
                    all_refs = [k for k, v in self.metadata.items()
                               if v.get('hash') == file_hash and not v.get('deleted', False)]
                    
                    # ---------------------------------------------------------------------------
                    if not all_refs and file_hash in self.hash_to_path_map:
                        del self.hash_to_path_map[file_hash]
        
        # ---------------------------------------------------------------------------
        self._send_file_status(rel_path, 'Deleted', 0, 'error')
        
        # ---------------------------------------------------------------------------
        logging.info(f"Marked as deleted: {rel_path}")

    def _perform_atomic_copy(self, src_path: str, final_dst_path: str,
                            file_hash: str = None, file_size: int = None) -> bool:
        """Atomic file copy with temp file."""
        
        # ---------------------------------------------------------------------------
        if not os.path.exists(src_path):
            return False

        # ---------------------------------------------------------------------------
        temp_dst_path = f"{final_dst_path}.tmp_{os.getpid()}_{uuid.uuid4().hex}"

        # ---------------------------------------------------------------------------
        try:
            os.makedirs(os.path.dirname(final_dst_path), exist_ok=True)

            entry_id = self.journal.append_entry('copy', {
                'src': src_path,
                'dst': final_dst_path,
                'tmp': temp_dst_path
            })

            # ---------------------------------------------------------------------------
            # Copy in chunks
            with open(src_path, 'rb') as fr, open(temp_dst_path, 'wb') as fw:
                while True:
                    if self.shutdown_event.is_set():
                        raise InterruptedError("Shutdown requested")
                    chunk = fr.read(65536)
                    if not chunk:
                        break
                    fw.write(chunk)

            # ---------------------------------------------------------------------------
            # Preserve metadata
            try:
                shutil.copystat(src_path, temp_dst_path)
            except:
                pass

            # ---------------------------------------------------------------------------
            os.rename(temp_dst_path, final_dst_path)  # Atomic rename
            # ---------------------------------------------------------------------------
            self.journal.mark_completed(entry_id)
            # ---------------------------------------------------------------------------
            return True
        except InterruptedError:
            if os.path.exists(temp_dst_path):
                os.remove(temp_dst_path)
            return False
        except Exception as e:
            logging.error(f"Atomic copy failed for {src_path}: {e}")
            if os.path.exists(temp_dst_path):
                os.remove(temp_dst_path)
            return False


    # ---------------------------------------------------------------------------
    # FINDER
    # ---------------------------------------------------------------------------
    def _find_all_backup_locations(self, rel_path: str, file_hash: str) -> List[str]:
        """
        Find ALL backup locations for a file (main backup + all incrementals).
        
        Returns list of absolute paths to backup files, ordered by priority:
        1. Main backup location
        2. Most recent incremental
        3. Older incrementals
        """

        # ---------------------------------------------------------------------------
        locations = []
        
        # ---------------------------------------------------------------------------
        # 1. Check main backup
        main_backup_path = os.path.join(self.app_main_backup_dir, rel_path)
        if os.path.exists(main_backup_path):
            locations.append(main_backup_path)
        
        # ---------------------------------------------------------------------------
        # 2. Check metadata for hash-based locations
        with self.state_lock:
            for path_key, meta in self.metadata.items():
                if meta.get('hash') == file_hash:
                    backup_path = meta.get('path')
                    if backup_path and os.path.exists(backup_path) and backup_path not in locations:
                        locations.append(backup_path)
        
        # ---------------------------------------------------------------------------
        # 3. Check all incremental backup directories
        if os.path.exists(self.app_incremental_backup_dir):
            incremental_locations = []
            
            # ---------------------------------------------------------------------------
            # Walk through date folders (YYYY-MM-DD)
            for date_folder in os.listdir(self.app_incremental_backup_dir):
                date_path = os.path.join(self.app_incremental_backup_dir, date_folder)
                if not os.path.isdir(date_path):
                    continue
                
                # ---------------------------------------------------------------------------
                # Walk through time folders (HH_MM_SS)
                for time_folder in os.listdir(date_path):
                    time_path = os.path.join(date_path, time_folder)
                    if not os.path.isdir(time_path):
                        continue
                    
                    # ---------------------------------------------------------------------------
                    # Check for the file in this incremental backup
                    incremental_file = os.path.join(time_path, rel_path)
                    if os.path.exists(incremental_file):
                        # Verify hash matches
                        inc_hash = calculate_sha256(incremental_file)
                        if inc_hash == file_hash:
                            # Store with timestamp for sorting
                            timestamp = f"{date_folder}_{time_folder}"
                            incremental_locations.append((timestamp, incremental_file))
            
            # ---------------------------------------------------------------------------
            # Sort incrementals by timestamp (newest first) and add to locations
            incremental_locations.sort(reverse=True)
            locations.extend([path for _, path in incremental_locations])
        
        # ---------------------------------------------------------------------------
        return locations

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

    # ---------------------------------------------------------------------------
    # METADATA MANAGEMENT
    # ---------------------------------------------------------------------------
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

            # Rebuild hash map
            self.hash_to_path_map = {}
            for key, val in self.metadata.items():
                file_hash = val.get('hash')
                backup_path = val.get('path')

                if file_hash and backup_path:
                    if backup_path.startswith(self.app_main_backup_dir):
                        self.hash_to_path_map[file_hash] = backup_path
                    elif file_hash not in self.hash_to_path_map:
                        self.hash_to_path_map[file_hash] = backup_path

            # logging.info(f"Loaded {len(self.metadata)} metadata entries")
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

    def _send_progress_update(self, rel_path: str, file_size: int):
        """Send progress update."""
        try:
            total_files = max(1, self.total_files_to_scan)
            total_bytes = max(1, self.total_transfer_size)

            with self.state_lock:
                current_files = self.files_backed_up_count
                current_bytes = self.total_size_transferred

            if total_bytes > 0:
                progress = (current_bytes / total_bytes) * 100
            else:
                progress = (current_files / total_files) * 100

            progress = min(100.0, max(0.0, progress))

            # Calculate ETA
            eta = "Calculating..."
            if self.backup_start_time and progress >= 0.5:
                elapsed = time.time() - self.backup_start_time
                if progress > 0:
                    total_estimate = elapsed / (progress / 100.0)
                    remaining = total_estimate - elapsed

                    if remaining > 1:
                        minutes = int(remaining / 60)
                        seconds = int(remaining % 60)
                        if minutes > 0:
                            eta = f"{minutes} min {seconds} sec"
                        else:
                            eta = f"{seconds} sec"
                    else:
                        eta = "Finishing soon"

            display_path = _truncate_path(rel_path)

            self.message_queue.put({
                'type': 'backup_progress',
                'title': 'Backup Progress',
                'description': display_path,
                'progress': progress / 100.0,
                'status': 'running',
                'current_file': rel_path,
                'files_completed': current_files,
                'total_files': total_files,
                'bytes_processed': current_bytes,
                'total_bytes': total_bytes,
                'eta': eta,
                'timestamp': int(time.time())
            }, timeout=0.5)
        except queue.Full:
            pass

    def message_sender_thread(self):
        """Thread to send queued messages."""
        while not self.shutdown_event.is_set():
            try:
                msg = self.message_queue.get(timeout=0.5)
                self.message_sender.send_message_sync(msg)
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Message sender error: {e}")

        # Drain remaining messages
        while not self.message_queue.empty():
            try:
                msg = self.message_queue.get_nowait()
                self.message_sender.send_message_sync(msg)
            except:
                break

    # =========================================================================
    # SAFETY NET
    # =========================================================================
    def start_full_scan(self):
        """Start full scan in background thread to avoid blocking main loop."""
        
        # ---------------------------------------------------------------------------
        if hasattr(self, '_scan_thread') and self._scan_thread.is_alive():
            logging.warning("Full scan already in progress")
            return
           
        # ---------------------------------------------------------------------------
        self._scan_thread = threading.Thread(
            target=self._full_scan_impl,
            daemon=True
        )
        self._scan_thread.start()


    def _full_scan_impl(self):
        """Background implementation of full scan."""
        logging.info("Full scan started in background...")
        
        # ---------------------------------------------------------------------------
        def _detect_and_sync_moved_files():
            """
            Periodic scan to detect files that were moved while daemon was offline.
            With timeout and shutdown checks to prevent hanging.
            """
            
            logging.info("Starting moved file detection scan...")
            
            # CRITICAL: Check if we should even start
            if self.shutdown_event.is_set():
                logging.info("Shutdown in progress, skipping moved file detection")
                return
            
            # Time tracking for timeout
            scan_start = time.time()
            MAX_SCAN_TIME = 30  # 30 seconds max for moved detection
            files_processed = 0
            
            moved_files_found = 0
            synced_successfully = 0
            
            try:
                current_hash_locations = {}
                
                # Get folders to scan
                folders = self._get_target_folders()
                logging.info(f"Scanning {len(folders)} folders for moved files")
                
                for folder_index, folder in enumerate(folders):
                    # Check shutdown before starting each folder
                    if self.shutdown_event.is_set():
                        logging.info("Shutdown requested, aborting moved file scan")
                        return
                        
                    # Check timeout
                    if time.time() - scan_start > MAX_SCAN_TIME:
                        logging.warning(f"Moved file scan timeout after {MAX_SCAN_TIME}s")
                        return
                    
                    logging.debug(f"Scanning folder {folder_index+1}/{len(folders)}: {folder}")
                    
                    # Walk directory
                    for root, dirs, files in os.walk(folder):
                        # Check shutdown during walk
                        if self.shutdown_event.is_set():
                            logging.info("Shutdown requested, aborting moved file scan")
                            return
                            
                        # Check timeout during walk
                        if time.time() - scan_start > MAX_SCAN_TIME:
                            logging.warning(f"Moved file scan timeout after {MAX_SCAN_TIME}s")
                            return
                        
                        # Skip excluded directories
                        dirs[:] = [d for d in dirs if not _should_process(os.path.join(root, d))]
                        
                        # Process files in this directory
                        for filename in files:
                            # Check shutdown for each file
                            if self.shutdown_event.is_set():
                                logging.info("Shutdown requested, aborting moved file scan")
                                return
                                
                            # Check timeout for each file
                            if time.time() - scan_start > MAX_SCAN_TIME:
                                logging.warning(f"Moved file scan timeout after {MAX_SCAN_TIME}s")
                                return
                            
                            filepath = os.path.join(root, filename)
                            
                            # Skip if file shouldn't be processed
                            if not _should_process(filepath):
                                continue
                            
                            files_processed += 1
                            
                            # Progress logging every 100 files
                            if files_processed % 100 == 0:
                                logging.debug(f"Moved scan progress: {files_processed} files processed")
                            
                            try:
                                # OPTIMIZATION: Skip large files (>50MB) for moved detection
                                # They're unlikely to be moved frequently and hashing is slow
                                try:
                                    file_size = os.path.getsize(filepath)
                                    if file_size > LARGE_FILE_THRESHOLD:  # 50MB
                                        continue
                                except:
                                    continue
                                
                                # Quick check: Only process files modified in last 7 days
                                try:
                                    mtime = os.path.getmtime(filepath)
                                    if time.time() - mtime > 7 * 86400:  # 7 days
                                        continue
                                except:
                                    continue
                                
                                # Calculate hash with potential timeout
                                file_hash = calculate_sha256(filepath)
                                if not file_hash:
                                    continue
                                
                                rel_path = os.path.relpath(filepath, EXPANDUSER)
                                
                                # Store current location for this hash
                                if file_hash not in current_hash_locations:
                                    current_hash_locations[file_hash] = []
                                
                                current_hash_locations[file_hash].append(rel_path)
                                
                            except Exception as e:
                                logging.debug(f"Error processing {filepath} in moved scan: {e}")
                                continue
                
                logging.info(f"Moved file scan: processed {files_processed} files")
                
                # Now compare with metadata to find moved files
                if not current_hash_locations:
                    logging.info("No current files found to compare for moved detection")
                    return
                
                # Compare with metadata
                with self.state_lock:
                    metadata_items = list(self.metadata.items())
                
                logging.info(f"Comparing with {len(metadata_items)} metadata entries")
                
                for old_rel_path, meta in metadata_items:
                    # Check shutdown during comparison
                    if self.shutdown_event.is_set():
                        logging.info("Shutdown requested during moved file comparison")
                        return
                        
                    # Check timeout during comparison
                    if time.time() - scan_start > MAX_SCAN_TIME:
                        logging.warning(f"Moved file scan timeout after {MAX_SCAN_TIME}s")
                        return
                    
                    file_hash = meta.get('hash')
                    if not file_hash:
                        continue
                    
                    # Skip deleted files
                    if meta.get('deleted'):
                        continue
                    
                    # Check if file exists at old location
                    old_full_path = os.path.join(EXPANDUSER, old_rel_path)
                    if os.path.exists(old_full_path):
                        # File still at original location
                        continue
                    
                    # File not at old location - check if it moved
                    current_locations = current_hash_locations.get(file_hash, [])
                    if not current_locations:
                        # File deleted (not found in current scan)
                        logging.debug(f"File deleted (not found in scan): {old_rel_path}")
                        # Don't call _handle_file_deletion here - let real-time events handle it
                        continue
                    
                    # File moved to new location(s)
                    for new_rel_path in current_locations:
                        if new_rel_path == old_rel_path:
                            continue
                        
                        moved_files_found += 1
                        
                        logging.info(f"Detected moved file: {old_rel_path} -> {new_rel_path}")
                        
                        # Sync backup locations
                        try:
                            new_full_path = os.path.join(EXPANDUSER, new_rel_path)
                            self._handle_file_move(old_full_path, new_full_path)
                            synced_successfully += 1
                        except Exception as e:
                            logging.error(f"Error syncing moved file {old_rel_path}: {e}")
                
                # Log results
                if moved_files_found > 0:
                    logging.info(f"Moved file detection complete: {synced_successfully}/{moved_files_found} synced successfully")
                    # Save updated metadata
                    try:
                        server.save_metadata(self.metadata)
                    except Exception as e:
                        logging.error(f"Failed to save metadata after moved detection: {e}")
                else:
                    logging.info("No moved files detected")
                    
            except Exception as e:
                logging.error(f"Error in moved file detection: {e}", exc_info=True)
            finally:
                scan_duration = time.time() - scan_start
                logging.info(f"Moved file scan completed in {scan_duration:.1f}s")
        _detect_and_sync_moved_files()
        
        # ---------------------------------------------------------------------------
        logging.info("Full scan complete")

        
# ---------------------------------------------------------------------------
# JOURNAL
# ---------------------------------------------------------------------------
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

        # logging.info("Replaying journal...")

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
    """Main entry point - pure threading model."""
    daemon = None
    watcher_thread = None
    observer = None
    message_thread = None
    control_thread = None

    # Signal handler
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

        # Initialize daemon
        daemon = Daemon()

        # Create lock file
        if os.path.exists(daemon.lock_file_path):
            os.remove(daemon.lock_file_path)

        if not daemon._create_lock_file():
            logging.error("Could not create lock file")
            return

        atexit.register(daemon._remove_lock_file)

        # Load state
        daemon._load_metadata()
        daemon._create_ready_state()
        daemon.journal.replay(daemon)

        # Start control socket listener thread (NEW)
        # This is where you initialize the thread object
        control_thread = threading.Thread( 
            target=daemon._socket_listener_thread, # The method to run
            daemon=True                          # Ensures it dies if the main process dies
        )
        control_thread.start()
        
        # Start message sender thread
        message_thread = threading.Thread(
            target=daemon.message_sender_thread,
            daemon=True
        )
        message_thread.start()

        # Start watchdog observer
        event_handler = BackupChangeHandler(daemon)
        observer = Observer()

        for path in daemon._get_target_folders():
            if os.path.isdir(path):
                observer.schedule(event_handler, path, recursive=True)
                logging.info(f"Watching: {path}")

        observer.start()

        # Start worker thread
        watcher_thread = threading.Thread(
            target=daemon.watch_worker,
            daemon=True
        )
        watcher_thread.start()

        logging.info("Daemon started successfully")

        # Main loop - periodic full scans and flatpak backups
        last_full_scan = 0
        while not daemon.shutdown_event.is_set():
            current_time = time.time()

            # Periodic full scan
            if current_time - last_full_scan >= POLLING_INTERVAL:
                daemon.start_full_scan()
                generate_summary()  # Generate backup summary
                last_full_scan = current_time

            # Also check flatpak backup separately in case full scan doesn't run
            def check_and_backup_flatpaks():
                """Check if it's time to backup flatpaks and do it if needed."""
                if current_time - daemon.last_flatpak_backup_time >= FLATPAK_BACKUP_INTERVAL:
                    logging.info(f"Scheduled Flatpak backup")
                    daemon.backup_flatpaks()
            check_and_backup_flatpaks()

            # Sleep with frequent checks
            for _ in range(100):  # Check every 100ms
                if daemon.shutdown_event.is_set():
                    break
                time.sleep(0.1)

    except Exception as e:
        logging.error(f"Main error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        logging.info("Shutting down...")

        # Signal shutdown
        if daemon:
            daemon.shutdown_event.set()

        # Stop observer
        if observer:
            observer.stop()

        # Wait for threads
        if watcher_thread and watcher_thread.is_alive():
            watcher_thread.join(timeout=5)

        if message_thread and message_thread.is_alive():
            message_thread.join(timeout=2)

        if observer:
            observer.join(timeout=5)

        # Shutdown executor
        if daemon and hasattr(daemon, 'executor'):
            daemon.executor.shutdown(wait=True)

        # Save metadata
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