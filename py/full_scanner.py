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
        self._is_scanning = False  # FIX: Track scanning state

    def is_scanning(self):
        """Check if a scan is currently in progress."""
        return self._is_scanning

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
        self._is_scanning = True  # FIX: Set scanning flag

        logging.info("=" * 60)
        logging.info("FULL SCAN STARTED")
        logging.info("=" * 60)

        scan_start = time.time()

        try:
            # Check if backup drive is available before scanning
            if not self.daemon.engine._check_backup_drive_available():
                logging.warning("⚠ Backup drive not available - scan will continue but backups will be queued")

            # Scan for new/modified/deleted files
            self._scan_for_file_changes()

            # Save metadata after scan (only if drive is available)
            if self.daemon.engine.backup_drive_available:
                try:
                    with self.daemon.state_lock:
                        metadata_count = len(self.daemon.metadata.metadata)
                    logging.info(f"Saving metadata with {metadata_count} entries...")
                    self.daemon.metadata.save()
                    logging.info("✓ Metadata saved successfully")
                except Exception as e:
                    logging.error(f"Failed to save metadata after scan: {e}")
            else:
                logging.info("⚠ Skipping metadata save - backup drive not available")

        except Exception as e:
            logging.error(f"Full scan error: {e}", exc_info=True)
        finally:
            duration = time.time() - scan_start
            logging.info("=" * 60)
            logging.info(f"FULL SCAN COMPLETED in {duration:.1f}s")
            logging.info("=" * 60)
            self._is_scanning = False  # FIX: Clear scanning flag

    def _scan_for_file_changes(self):
        """Scan filesystem and compare with metadata."""
        logging.info("Scanning for file changes...")

        if self.daemon.shutdown_event.is_set():
            return

        # Get folders to scan
        folders = self._get_target_folders()
        if not folders:
            logging.warning("No folders to scan")
            return

        logging.info(f"Scanning {len(folders)} folders: {folders}")

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

        logging.info(f"Total files found: {len(current_files)}")

        # Reset counters for actual backup
        with self.daemon.state_lock:
            self.daemon.files_backed_up_count = 0
            self.daemon.total_size_transferred = 0

        # Compare with metadata - FIXED: Consistent access pattern
        new_files = []
        modified_files = []

        # Check for new and modified files
        for rel_path, file_info in current_files.items():
            if self.daemon.shutdown_event.is_set():
                return

            # FIXED: Use consistent metadata access
            with self.daemon.state_lock:
                metadata_entry = self.daemon.metadata.metadata.get(rel_path)

            if not metadata_entry:
                # New file
                new_files.append((rel_path, file_info))
            elif not metadata_entry.get('deleted', False):
                # Check if modified
                meta_mtime = metadata_entry.get('mtime', 0)
                meta_size = metadata_entry.get('size', 0)

                # Compare with tolerance for filesystem timestamp precision
                if (abs(file_info['mtime'] - meta_mtime) > 1 or
                    file_info['size'] != meta_size):
                    modified_files.append((rel_path, file_info))
                    logging.info(f"Modified: {rel_path} - mtime {file_info['mtime']:.1f} vs {meta_mtime:.1f}, size {file_info['size']} vs {meta_size}")

        # Check for deleted files - FIXED: Proper metadata access
        with self.daemon.state_lock:
            metadata_paths = set(self.daemon.metadata.metadata.keys())

        current_paths = set(current_files.keys())

        deleted_files = []
        for rel_path in metadata_paths:
            if self.daemon.shutdown_event.is_set():
                return

            # FIXED: Consistent metadata access
            with self.daemon.state_lock:
                meta_entry = self.daemon.metadata.metadata.get(rel_path, {})

            # Skip already deleted files
            if meta_entry.get('deleted', False):
                continue

            # File exists in metadata but not on disk
            if rel_path not in current_paths:
                deleted_files.append(rel_path)

        # Log findings
        logging.info("=" * 60)
        logging.info("SCAN RESULTS:")
        logging.info(f"  New files:      {len(new_files)}")
        logging.info(f"  Modified files: {len(modified_files)}")
        logging.info(f"  Deleted files:  {len(deleted_files)}")
        logging.info("=" * 60)

        # Process findings
        if new_files or modified_files or deleted_files:
            # Check drive availability before processing
            drive_available = self.daemon.engine._check_backup_drive_available()

            if not drive_available:
                logging.warning("⚠ Backup drive not available - changes detected but backups postponed")
                logging.info(f"  {len(new_files)} new, {len(modified_files)} modified, {len(deleted_files)} deleted files waiting")
                return

            logging.info("Processing changes found during scan...")

            # Process new files
            for idx, (rel_path, file_info) in enumerate(new_files):
                if self.daemon.shutdown_event.is_set():
                    return
                try:
                    logging.info(f"[{idx+1}/{len(new_files)}] New: {rel_path}")
                    self.daemon.engine._process_file_change(file_info['path'], 'created')
                except Exception as e:
                    logging.error(f"Error processing new file {rel_path}: {e}", exc_info=True)

            # Process modified files
            for idx, (rel_path, file_info) in enumerate(modified_files):
                if self.daemon.shutdown_event.is_set():
                    return
                try:
                    logging.info(f"[{idx+1}/{len(modified_files)}] Modified: {rel_path}")
                    self.daemon.engine._process_file_change(file_info['path'], 'modified')
                except Exception as e:
                    logging.error(f"Error processing modified file {rel_path}: {e}", exc_info=True)

            # Process deleted files
            for idx, rel_path in enumerate(deleted_files):
                if self.daemon.shutdown_event.is_set():
                    return
                try:
                    logging.info(f"[{idx+1}/{len(deleted_files)}] Deleted: {rel_path}")
                    # Reconstruct full path from rel_path
                    # FIX: Better path reconstruction
                    full_path = self._reconstruct_full_path(rel_path)
                    self.daemon.engine._handle_file_deletion(full_path)
                except Exception as e:
                    logging.error(f"Error processing deleted file {rel_path}: {e}", exc_info=True)

            logging.info("✓ Change processing complete")
        else:
            logging.info("✓ No changes detected")

    def _reconstruct_full_path(self, rel_path):
        """Reconstruct full path from relative path."""
        # The rel_path is typically relative to home or a watched folder
        # Try to find which watched folder it belongs to
        folders = self._get_target_folders()

        for folder in folders:
            # Try constructing the path under this folder
            potential_path = os.path.join(folder, rel_path)
            if os.path.exists(potential_path):
                return potential_path

        # Fallback: assume it's relative to home
        return os.path.join(os.path.expanduser("~"), rel_path.replace('/', os.sep))

    def _get_target_folders(self):
        """Get list of folders to watch."""
        folders_str = self.daemon.server.get_database_value('BACKUP_FOLDERS', 'folders')
        if not folders_str:
            return []

        target_folders = [f.strip() for f in folders_str.split(',') if f.strip()]
        valid_folders = []
        for folder in target_folders:
            folder = os.path.abspath(os.path.expanduser(folder))
            if os.path.exists(folder) and os.path.isdir(folder):
                valid_folders.append(folder)

        return valid_folders
