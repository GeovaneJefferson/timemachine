import os
import time
import logging
import threading
from filesystem import should_process, normalize_rel_path
from config import POLLING_INTERVAL


class FullScanner:
    def __init__(self, daemon):
        self.daemon = daemon
        self._scan_thread = None

    def start_full_scan(self, initial=False):
        """Start full scan in background thread."""
        if self._scan_thread and self._scan_thread.is_alive():
            if not initial:
                logging.warning("Full scan already in progress")
            return

        scan_type = "INITIAL" if initial else "PERIODIC"
        logging.info(f"Starting {scan_type} full scan...")

        self._scan_thread = threading.Thread(
            target=self._full_scan_impl,
            daemon=True,
            name=f"FullScan-{scan_type}"
        )
        self._scan_thread.start()

    def _full_scan_impl(self):
        """Complete full scan implementation."""
        logging.info("=" * 60)
        logging.info("FULL SCAN STARTED")
        logging.info("=" * 60)

        scan_start = time.time()

        try:
            # Scan for new/modified/deleted files
            self._scan_for_file_changes()

            # Save metadata after scan
            try:
                logging.info(f"Saving metadata with {len(self.daemon.metadata.metadata)} entries...")
                self.daemon.metadata.save()
                logging.info("✓ Metadata saved successfully")
            except Exception as e:
                logging.error(f"Failed to save metadata after scan: {e}")

        except Exception as e:
            logging.error(f"Full scan error: {e}")
        finally:
            duration = time.time() - scan_start
            logging.info("=" * 60)
            logging.info(f"FULL SCAN COMPLETED in {duration:.1f}s")
            logging.info("=" * 60)

    def _scan_for_file_changes(self):
        """Scan filesystem and compare with metadata."""
        logging.info("Scanning for file changes...")

        if self.daemon.shutdown_event.is_set():
            return

        # Set backup tracking
        self.daemon.backup_start_time = time.time()
        self.daemon.total_files_to_scan = 0
        self.daemon.total_transfer_size = 0

        # Get folders to scan
        folders = self._get_target_folders()
        if not folders:
            logging.warning("No folders to scan")
            return

        logging.info(f"Scanning {len(folders)} folders")

        current_files = {}

        # Scan all watched folders
        for folder_idx, folder in enumerate(folders):
            if self.daemon.shutdown_event.is_set():
                return

            logging.info(f"Scanning folder {folder_idx + 1}/{len(folders)}: {folder}")

            files_in_folder = 0
            for root, dirs, files in os.walk(folder):
                if self.daemon.shutdown_event.is_set():
                    return

                # Skip excluded directories
                dirs[:] = [d for d in dirs if should_process(os.path.join(root, d))]

                for filename in files:
                    if self.daemon.shutdown_event.is_set():
                        return

                    filepath = os.path.join(root, filename)

                    # Skip excluded files
                    if not should_process(filepath):
                        continue

                    try:
                        stat_result = os.stat(filepath)
                        rel_path = normalize_rel_path(filepath)

                        current_files[rel_path] = {
                            'mtime': stat_result.st_mtime,
                            'size': stat_result.st_size,
                            'path': filepath
                        }

                        files_in_folder += 1

                    except (OSError, PermissionError) as e:
                        logging.debug(f"Cannot access {filepath}: {e}")
                        continue

            logging.info(f"  Found {files_in_folder} files in {os.path.basename(folder)}")

        # Reset counters for actual backup
        with self.daemon.state_lock:
            self.daemon.files_backed_up_count = 0
            self.daemon.total_size_transferred = 0
            
        # Compare with metadata - FIXED: Use dictionary access
        new_files = []
        modified_files = []

        # Check for new and modified files
        for rel_path, file_info in current_files.items():
            if self.daemon.shutdown_event.is_set():
                return

            # FIXED: Use get() method or dictionary access
            metadata_entry = self.daemon.metadata.get(rel_path)

            if not metadata_entry:
                # New file
                new_files.append((rel_path, file_info))
            elif not metadata_entry.get('deleted'):
                # Check if modified
                meta_mtime = metadata_entry.get('mtime', 0)
                meta_size = metadata_entry.get('size', 0)

                if (abs(file_info['mtime'] - meta_mtime) > 1 or
                    file_info['size'] != meta_size):
                    modified_files.append((rel_path, file_info))

        # Check for deleted files - FIXED: Access metadata directly
        with self.daemon.state_lock:
            metadata_paths = set(self.daemon.metadata.metadata.keys())

        current_paths = set(current_files.keys())

        deleted_files = []
        for rel_path in metadata_paths:
            if self.daemon.shutdown_event.is_set():
                return

            # FIXED: Access metadata correctly
            if self.daemon.metadata.metadata.get(rel_path, {}).get('deleted'):
                continue

            if rel_path not in current_paths:
                deleted_files.append(rel_path)

        # Log findings
        logging.info(f"Scan results:")
        logging.info(f"  New files:      {len(new_files)}")
        logging.info(f"  Modified files: {len(modified_files)}")
        logging.info(f"  Deleted files:  {len(deleted_files)}")

        # Process findings
        if new_files or modified_files or deleted_files:
            logging.info("Processing changes found during scan...")

            # Process new files
            for rel_path, file_info in new_files:
                if self.daemon.shutdown_event.is_set():
                    return
                try:
                    logging.info(f"New: {rel_path}")
                    self.daemon.engine._process_file_change(file_info['path'], 'created')
                except Exception as e:
                    logging.error(f"Error processing new file {rel_path}: {e}")

            # Process modified files
            for rel_path, file_info in modified_files:
                if self.daemon.shutdown_event.is_set():
                    return
                try:
                    logging.info(f"Modified: {rel_path}")
                    self.daemon.engine._process_file_change(file_info['path'], 'modified')
                except Exception as e:
                    logging.error(f"Error processing modified file {rel_path}: {e}")

            # Process deleted files
            for rel_path in deleted_files:
                if self.daemon.shutdown_event.is_set():
                    return
                try:
                    logging.info(f"Deleted: {rel_path}")
                    full_path = os.path.join(os.path.expanduser("~"), rel_path.replace('/', os.sep))
                    self.daemon.engine._handle_file_deletion(full_path)
                except Exception as e:
                    logging.error(f"Error processing deleted file {rel_path}: {e}")

            logging.info("Change processing complete")
        else:
            logging.info("No changes detected")

        # After scanning, reset tracking variables
        if self.daemon.shutdown_event.is_set():
            self.daemon.backup_start_time = None
            self.daemon.total_files_to_scan = 0
            self.daemon.total_transfer_size = 0

    def _get_target_folders(self):
        """Get list of folders to watch."""
        folders_str = self.daemon.server.get_database_value('BACKUP_FOLDERS', 'folders')
        if not folders_str:
            return []

        target_folders = [f.strip() for f in folders_str.split(',') if f.strip()]
        valid_folders = []
        for folder in target_folders:
            folder = os.path.abspath(os.path.expanduser(folder))
            if os.path.exists(folder):
                valid_folders.append(folder)

        return valid_folders