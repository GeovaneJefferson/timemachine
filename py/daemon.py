#!/usr/bin/env python3

import queue
import threading
import time
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer

from config import server
from filesystem import should_process
from metadata import MetadataStore
from backup_engine import BackupEngine
from watchdog_handler import BackupChangeHandler
from full_scanner import FullScanner
from flatpak_backup import FlatpakBackup
from lock_manager import LockManager
from socket_listener import SocketListener

class Daemon:
    def __init__(self):
        self.server = server
        self.app_main_backup_dir = server.app_main_backup_dir()
        self.app_incremental_backup_dir = server.app_incremental_backup_dir()
        self.app_backup_dir = server.devices_path()

        # Threading setup
        cpu_count = os.cpu_count() or 4
        self.max_threads = min(32, cpu_count * 4)
        self.executor = ThreadPoolExecutor(max_workers=self.max_threads, thread_name_prefix="FileWorker")

        # Event queue for watchdog events - INCREASED SIZE to prevent drops
        self.event_queue = queue.Queue(maxsize=10000)  # Increased from 5000
        self.shutdown_event = threading.Event()
        self.state_lock = threading.Lock()

        # Initialize components
        self.metadata = MetadataStore()
        self.engine = BackupEngine(self)
        self.full_scanner = FullScanner(self)
        self.flatpak_backup = FlatpakBackup(self)
        self.lock_manager = LockManager(self)
        self.socket_listener = SocketListener(self)

        # State tracking
        self.last_full_scan = 0  # Now initialized properly
        self.files_backed_up_count = 0
        self.total_size_transferred = 0

        # FIX #1: Keep reference to observer for proper shutdown
        self.observer = None
        self.watcher_thread = None

    def is_dir_excluded(self, dir_path):
        """Check if a directory should be excluded from watching."""
        # Use should_process logic - if it returns False, exclude
        return not should_process(dir_path)

    def schedule_selective_watching(self, observer, event_handler, root_path):
        """Schedule watchers only on non-excluded directories to reduce inotify load."""
        scheduled_count = 0
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Filter out excluded subdirectories from dirnames to prevent walking into them
            dirnames[:] = [d for d in dirnames if not self.is_dir_excluded(os.path.join(dirpath, d))]
            
            # Schedule watcher on this directory if it's not excluded
            if not self.is_dir_excluded(dirpath):
                try:
                    observer.schedule(event_handler, dirpath, recursive=False)
                    scheduled_count += 1
                except Exception as e:
                    logging.error(f"Failed to schedule watcher on {dirpath}: {e}")
            else:
                # If excluded, don't walk into subdirs
                dirnames[:] = []
        
        logging.info(f"Scheduled {scheduled_count} watchers for {root_path}")
        return scheduled_count

    def watch_worker(self):
        """Main worker thread that processes events."""
        logging.info("Watch worker thread started")

        while not self.shutdown_event.is_set():
            try:
                # FIX #2: Unpack all three values
                event_type, src, dst = self.event_queue.get(timeout=0.5)

                # Process the event with proper parameters
                try:
                    if event_type == 'moved' and dst:
                        # Pass destination for moved events
                        self.engine.process_change(src, event_type, dest_path=dst)
                    else:
                        # No destination needed for other events
                        self.engine.process_change(src, event_type)
                except Exception as e:
                    logging.error(f"Error processing change for {src}: {e}", exc_info=True)

                # Mark task as done
                self.event_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Worker loop error: {e}", exc_info=True)
                time.sleep(0.1)

        logging.info("Watch worker thread stopped")

    def start(self):
        """Start the daemon."""
        # Create lock file
        if os.path.exists(self.lock_manager.lock_file_path):
            os.remove(self.lock_manager.lock_file_path)

        if not self.lock_manager.create_lock_file():
            logging.error("Could not create lock file")
            return False

        # Load metadata
        logging.info("Loading metadata...")
        self.metadata.load()

        # Create ready state
        self.lock_manager.create_ready_state()

        # Start control socket listener
        self.socket_listener.start_listener()

        # Start message sender in engine
        self.engine.start_message_sender()

        # FIX #3: Run initial full scan BEFORE starting watchdog
        # This ensures we catch any changes that happened while daemon was offline
        logging.info("Running initial full scan to catch offline changes...")
        self.last_full_scan = time.time()  # Set before scan
        self.full_scanner.start_full_scan(initial=True)

        # Wait for initial scan to complete before starting watchdog
        # This prevents duplicate processing
        while self.full_scanner.is_scanning():
            time.sleep(0.5)

        logging.info("Initial scan complete, starting watchdog observer...")

        # FIX #4: Start watchdog observer AFTER initial scan
        event_handler = BackupChangeHandler(self.event_queue, self)
        self.observer = Observer()  # Keep reference!

        folders = self._get_target_folders()
        if not folders:
            logging.warning("No folders configured for watching")

        for path in folders:
            if os.path.isdir(path):
                try:
                    # Use selective scheduling to avoid watching excluded directories
                    scheduled = self.schedule_selective_watching(self.observer, event_handler, path)
                    logging.info(f"Watching: {path} ({scheduled} directories scheduled)")
                except Exception as e:
                    logging.error(f"Failed to watch {path}: {e}")

        # Start the observer
        try:
            self.observer.start()
            logging.info("Watchdog observer started successfully")
        except Exception as e:
            logging.error(f"Failed to start observer: {e}")
            return False

        # FIX #5: Start worker thread AFTER observer
        self.watcher_thread = threading.Thread(
            target=self.watch_worker,
            daemon=True,
            name="WatchWorker"
        )
        self.watcher_thread.start()

        logging.info("Daemon started successfully")

        # Main loop
        try:
            while not self.shutdown_event.is_set():
                current_time = time.time()

                # Periodic full scan (every 30 minutes)
                if current_time - self.last_full_scan >= 1800:  # 30 minutes
                    logging.info("Starting periodic full scan...")
                    self.full_scanner.start_full_scan(initial=False)
                    self.last_full_scan = current_time

                # Check flatpak backup
                if current_time - self.flatpak_backup.last_backup_time >= 1800:
                    logging.info("Starting flatpak backup...")
                    self.flatpak_backup.backup_flatpaks()

                # Periodic drive check (every 5 minutes when not available)
                if not self.engine.backup_drive_available:
                    if current_time - self.engine.last_drive_check >= 300:  # 5 minutes
                        logging.info("Checking if backup drive has become available...")
                        self.engine._check_backup_drive_available()

                # FIX #6: Check queue size and warn if getting full
                queue_size = self.event_queue.qsize()
                if queue_size > 8000:  # 80% full
                    logging.warning(f"Event queue is getting full: {queue_size}/10000")

                # Sleep with shutdown checks
                for _ in range(100):
                    if self.shutdown_event.is_set():
                        break
                    time.sleep(0.1)

        except KeyboardInterrupt:
            logging.info("Received keyboard interrupt")
        except Exception as e:
            logging.error(f"Main loop error: {e}", exc_info=True)
        finally:
            self.shutdown()

        return True

    def shutdown(self):
        """Shutdown the daemon."""
        logging.info("Shutting down...")

        # Signal shutdown
        self.shutdown_event.set()

        # FIX #7: Stop watchdog observer first
        if self.observer is not None:
            try:
                logging.info("Stopping watchdog observer...")
                self.observer.stop()
                self.observer.join(timeout=5.0)  # Wait up to 5 seconds
                if self.observer.is_alive():
                    logging.warning("Observer did not stop cleanly")
                else:
                    logging.info("Observer stopped successfully")
            except Exception as e:
                logging.error(f"Error stopping observer: {e}")

        # Wait for watcher thread
        if self.watcher_thread is not None and self.watcher_thread.is_alive():
            logging.info("Waiting for watcher thread to finish...")
            self.watcher_thread.join(timeout=3.0)

        # Shutdown engine (which will shutdown message sender)
        self.engine.shutdown()

        # Wait for any remaining queue items to be processed
        try:
            logging.info("Waiting for event queue to empty...")
            self.event_queue.join()  # Wait for all items to be processed
        except Exception as e:
            logging.error(f"Error waiting for queue: {e}")

        # Shutdown executor
        logging.info("Shutting down thread pool...")
        self.executor.shutdown(wait=True, cancel_futures=False)

        # Save metadata
        logging.info("Saving metadata...")
        self.metadata.save()
        # Close SQLite connection (if used)
        try:
            self.metadata.close()
        except Exception:
            pass

        # Cleanup
        self.lock_manager.remove_lock_file()
        self.lock_manager.remove_ready_state()
        self.lock_manager.remove_socket_file()

        logging.info("Shutdown complete")

    def _get_target_folders(self):
        """Get list of folders to watch."""
        folders_str = self.server.get_database_value('BACKUP_FOLDERS', 'folders')
        if not folders_str:
            logging.warning("No BACKUP_FOLDERS configured in database")
            return []

        target_folders = [f.strip() for f in folders_str.split(',') if f.strip()]
        valid_folders = []

        for folder in target_folders:
            # Expand user home directory and make absolute
            folder = os.path.abspath(os.path.expanduser(folder))

            if os.path.exists(folder):
                if os.path.isdir(folder):
                    valid_folders.append(folder)
                    logging.info(f"Found valid folder: {folder}")
                else:
                    logging.warning(f"Path exists but is not a directory: {folder}")
            else:
                logging.warning(f"Folder does not exist: {folder}")

        if not valid_folders:
            logging.error("No valid folders found to watch!")

        return valid_folders
