import queue
import threading
import time
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer

from config import server
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

        # Event queue for watchdog events
        self.event_queue = queue.Queue(maxsize=5000)
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
        self.last_full_scan = 0
        self.files_backed_up_count = 0
        self.total_size_transferred = 0

    def watch_worker(self):
        """Main worker thread that processes events."""
        while not self.shutdown_event.is_set():
            try:
                event_type, src, dst = self.event_queue.get(timeout=0.5)
                self.engine.process_change(src, event_type)
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Worker loop error: {e}")
                time.sleep(0.1)

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

        # Start watchdog observer
        event_handler = BackupChangeHandler(self.event_queue)
        observer = Observer()

        folders = self._get_target_folders()
        for path in folders:
            if os.path.isdir(path):
                observer.schedule(event_handler, path, recursive=True)
                logging.info(f"Watching: {path}")

        observer.start()

        # Start worker thread
        watcher_thread = threading.Thread(
            target=self.watch_worker,
            daemon=True,
            name="WatchWorker"
        )
        watcher_thread.start()

        logging.info("Daemon started successfully")

        # Run initial full scan
        logging.info("Running initial full scan to catch offline changes...")
        self.full_scanner.start_full_scan(initial=True)

        # Main loop
        while not self.shutdown_event.is_set():
            current_time = time.time()

            # Periodic full scan (every 30 minutes)
            if current_time - self.last_full_scan >= 1800:  # 30 minutes
                self.full_scanner.start_full_scan(initial=False)
                self.last_full_scan = current_time

            # Check flatpak backup
            if current_time - self.flatpak_backup.last_backup_time >= 1800:
                self.flatpak_backup.backup_flatpaks()

            # Sleep with shutdown checks
            for _ in range(100):
                if self.shutdown_event.is_set():
                    break
                time.sleep(0.1)

        return True

    def shutdown(self):
        """Shutdown the daemon."""
        logging.info("Shutting down...")

        # Signal shutdown
        self.shutdown_event.set()

        # Shutdown engine (which will shutdown message sender)
        self.engine.shutdown()
        
        # Shutdown executor
        self.executor.shutdown(wait=True)

        # Save metadata
        self.metadata.save()

        # Cleanup
        self.lock_manager.remove_lock_file()
        self.lock_manager.remove_ready_state()
        self.lock_manager.remove_socket_file()

        logging.info("Shutdown complete")

    def _get_target_folders(self):
        """Get list of folders to watch."""
        folders_str = self.server.get_database_value('BACKUP_FOLDERS', 'folders')
        if not folders_str:
            return []

        target_folders = [f.strip() for f in folders_str.split(',') if f.strip()]
        valid_folders = []
        for folder in target_folders:
            folder = os.path.abspath(os.path.expanduser(folder))
            if os.path.exists(folder):
                valid_folders.append(folder)

        return valid_folders