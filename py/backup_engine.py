import os
import time
import logging
import threading
import shutil
import uuid
import hashlib
import stat
import errno
from filesystem import calculate_sha256, atomic_copy, handle_special_file, normalize_rel_path, should_process
from config import MIN_REPROCESS_INTERVAL, LARGE_FILE_THRESHOLD
from message_sender import MessageSender


class BackupEngine:
    def __init__(self, daemon):
        self.daemon = daemon
        self.last_processed_time = {}
        self.file_locks = {}
        self.file_locks_lock = threading.Lock()
        self.message_sender = MessageSender()
        self.message_sender_started = False
        self.backup_drive_available = False
        self.last_drive_check = 0
        self.drive_check_interval = 30  # Check every 30 seconds
        self.drive_warning_shown = False

    def start_message_sender(self):
        """Start the message sender thread."""
        if not self.message_sender_started:
            self.message_sender.start()
            self.message_sender_started = True

    def _check_backup_drive_available(self) -> bool:
        """Check if backup drive is accessible."""
        current_time = time.time()

        # Cache the check for drive_check_interval seconds
        if current_time - self.last_drive_check < self.drive_check_interval:
            return self.backup_drive_available

        self.last_drive_check = current_time

        # Check if backup directories are accessible
        try:
            # Check if we can access and write to the backup directories
            for backup_dir in [self.daemon.app_main_backup_dir, self.daemon.app_incremental_backup_dir]:
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir, exist_ok=True)

                # Try to write a test file
                test_file = os.path.join(backup_dir, '.backup_test')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)

            if not self.backup_drive_available:
                logging.info("✓ Backup drive is now available")
                self.message_sender.send_message_sync({"message": "Backup drive connected - resuming backups", "level": "info"})

            self.backup_drive_available = True
            self.drive_warning_shown = False
            return True

        except (PermissionError, OSError) as e:
            if self.backup_drive_available or not self.drive_warning_shown:
                logging.warning(f"⚠ Backup drive not accessible: {e}")
                self.message_sender.send_message_sync({"message": "Backup drive not connected - backups paused until drive is available", "level": "warning"})
                self.drive_warning_shown = True

            self.backup_drive_available = False
            return False

    def process_change(self, path: str, event_type: str, dest_path: str = None):
        """Process file change event.

        Args:
            path: Source path for the event
            event_type: Type of event (created, modified, deleted, moved)
            dest_path: Destination path (only for moved events)
        """
        # Start message sender if not already started
        self.start_message_sender()

        # Check if backup drive is available (except for deletions which only update metadata)
        if event_type != 'deleted':
            if not self._check_backup_drive_available():
                logging.debug(f"Skipping {event_type} for {path} - backup drive not available")
                return

        if event_type == 'deleted':
            self._handle_file_deletion(path)
        elif event_type == 'moved':
            # FIX: Handle moved events properly
            if dest_path:
                logging.info(f"File moved: {path} -> {dest_path}")
                # Treat as delete of old path and create of new path
                self._handle_file_deletion(path)
                if os.path.exists(dest_path):
                    self._process_file_change(dest_path, 'created')
            else:
                logging.warning(f"Moved event without destination path for {path}")
        else:
            self._process_file_change(path, event_type)

    def _process_file_change(self, path: str, event_type: str):
        """Process file creation or modification."""
        if not os.path.exists(path):
            logging.debug(f"File no longer exists: {path}")
            return

        # Check if it's a directory
        if os.path.isdir(path):
            logging.debug(f"Skipping directory: {path}")
            return

        # Double-check drive availability before processing
        if not self.backup_drive_available:
            logging.debug(f"Skipping {path} - backup drive not available")
            return

        rel_path = normalize_rel_path(path)

        try:
            stat_result = os.stat(path)
            file_size = stat_result.st_size
            current_mtime = stat_result.st_mtime

            # Cooldown check to prevent processing the same file too frequently
            current_time = time.time()
            last_time = self.last_processed_time.get(rel_path, 0)
            if current_time - last_time < MIN_REPROCESS_INTERVAL:
                logging.debug(f"Cooldown active for {rel_path}. Ignoring event.")
                return

            # Send processing status
            self.message_sender.send_file_status(rel_path, 'Processing', file_size, 'processing')

            # Calculate hash
            try:
                file_hash = calculate_sha256(path, file_size=file_size)
                if not file_hash:
                    logging.warning(f"Could not calculate hash for {rel_path}")
                    return
            except Exception as e:
                logging.error(f"Error calculating hash for {rel_path}: {e}")
                return

            # Check if content changed - FIXED: use proper dictionary access
            with self.daemon.state_lock:
                metadata = self.daemon.metadata.metadata.get(rel_path, {})

            if metadata.get('hash') == file_hash:
                # Same content, just update timestamp
                with self.daemon.state_lock:
                    if rel_path in self.daemon.metadata.metadata:
                        self.daemon.metadata.metadata[rel_path]['mtime'] = current_mtime
                logging.debug(f"File unchanged (same hash): {rel_path}")
                return

            # Determine if new file - FIXED: check metadata.metadata
            with self.daemon.state_lock:
                is_new = rel_path not in self.daemon.metadata.metadata

            # Build file info
            file_info = {
                'source_path': path,
                'rel_path': rel_path,
                'file_hash': file_hash,
                'size': file_size,
                'mtime': current_mtime,
                'event_type': event_type,
                'new_file': is_new
            }

            # Process the file
            success = self._process_single_file(file_info)
            if success:
                self.message_sender.send_file_status(rel_path, 'Backed Up', file_size, 'success')
                self.last_processed_time[rel_path] = time.time()

                # Update counters
                with self.daemon.state_lock:
                    self.daemon.files_backed_up_count += 1
                    self.daemon.total_size_transferred += file_size
            else:
                self.message_sender.send_file_status(rel_path, 'Failed', file_size, 'error')

        except FileNotFoundError:
            logging.debug(f"File disappeared during processing: {path}")
        except PermissionError:
            logging.warning(f"Permission denied: {path}")
        except Exception as e:
            logging.error(f"Error processing file change for {path}: {e}", exc_info=True)

    def _process_single_file(self, file_info: dict) -> bool:
        """Core file processing logic."""
        source = file_info['source_path']
        rel_path = file_info['rel_path']
        file_hash = file_info['file_hash']
        file_size = file_info['size']
        is_new_file = file_info['new_file']

        # Determine destination
        if is_new_file:
            dest = os.path.join(self.daemon.app_main_backup_dir, rel_path)
            backup_type = "MAIN"
        else:
            dest = os.path.join(self.daemon.app_incremental_backup_dir, rel_path)
            backup_type = "INCREMENTAL"

        # Ensure destination directory exists
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
        except PermissionError as e:
            logging.error(f"⚠ Cannot create backup directory (drive not mounted?): {e}")
            self.backup_drive_available = False  # Mark drive as unavailable
            self.last_drive_check = 0  # Force recheck on next attempt
            return False
        except OSError as e:
            logging.error(f"⚠ Cannot create backup directory: {e}")
            return False

        success = False

        try:
            # Handle special files (symlinks, pipes, etc.)
            if handle_special_file(source, dest):
                success = True
                logging.debug(f"Handled special file: {rel_path}")
            else:
                # Regular file - perform atomic copy
                success = self._perform_atomic_copy(source, dest)

            if success:
                self._update_metadata(rel_path, dest, file_info)
                logging.info(f"✓ [{backup_type}] Backed up: {rel_path} ({file_size} bytes)")
            else:
                logging.error(f"✗ [{backup_type}] Failed to back up: {rel_path}")

        except PermissionError as e:
            logging.error(f"⚠ Permission denied backing up {rel_path} (drive issue?): {e}")
            self.backup_drive_available = False  # Mark drive as unavailable
            self.last_drive_check = 0  # Force recheck
            return False
        except Exception as e:
            logging.error(f"Failed to process {rel_path}: {e}", exc_info=True)

        return success

    def _perform_atomic_copy(self, src_path: str, final_dst_path: str) -> bool:
        """Atomic file copy with temp file."""
        if not os.path.exists(src_path):
            logging.error(f"Source file does not exist: {src_path}")
            return False

        temp_dst_path = f"{final_dst_path}.tmp_{os.getpid()}_{uuid.uuid4().hex[:8]}"

        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(final_dst_path), exist_ok=True)

            # Copy file with buffering for large files
            with open(src_path, 'rb') as fr:
                with open(temp_dst_path, 'wb') as fw:
                    # Use larger buffer for better performance
                    shutil.copyfileobj(fr, fw, length=1024*1024)  # 1MB buffer

            # Preserve metadata (permissions, timestamps)
            try:
                shutil.copystat(src_path, temp_dst_path)
            except Exception as e:
                logging.debug(f"Could not preserve metadata for {src_path}: {e}")

            # Atomic rename
            os.replace(temp_dst_path, final_dst_path)
            return True

        except FileNotFoundError:
            logging.error(f"Source file disappeared during copy: {src_path}")
            return False
        except PermissionError as e:
            logging.error(f"Permission error copying {src_path}: {e}")
            return False
        except OSError as e:
            logging.error(f"OS error copying {src_path}: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error copying {src_path}: {e}", exc_info=True)
            return False
        finally:
            # Clean up temp file if it exists
            if os.path.exists(temp_dst_path):
                try:
                    os.remove(temp_dst_path)
                except:
                    pass

    def _update_metadata(self, rel_path: str, dst_path: str, file_info: dict):
        """Update metadata after successful backup."""
        with self.daemon.state_lock:
            self.daemon.metadata.metadata[rel_path] = {
                'path': dst_path,
                'mtime': file_info.get('mtime', time.time()),
                'size': file_info.get('size', 0),
                'hash': file_info.get('file_hash', ''),
                'deleted': False  # Mark as not deleted
            }


    def _handle_file_deletion(self, path: str):
        """Mark file as deleted in metadata."""
        rel_path = normalize_rel_path(path)

        with self.daemon.state_lock:
            if rel_path in self.daemon.metadata.metadata:
                self.daemon.metadata.metadata[rel_path]['deleted'] = True
                self.daemon.metadata.metadata[rel_path]['deleted_time'] = time.time()

                logging.info(f"Marked as deleted: {rel_path}")

                # Optionally log if this hash is no longer referenced
                file_hash = self.daemon.metadata.metadata[rel_path].get('hash')
                if file_hash:
                    remaining = self.daemon.metadata.count_hash_references(file_hash, include_deleted=False)
                    if remaining == 0:
                        logging.debug(f"No remaining references for hash: {file_hash}")
            else:
                logging.debug(f"File not in metadata, cannot mark as deleted: {rel_path}")

    def _acquire_file_lock(self, path: str, timeout: int = 5) -> bool:
        """Acquire file lock with timeout."""
        key = os.path.normpath(path)

        with self.file_locks_lock:
            if key not in self.file_locks:
                self.file_locks[key] = threading.Lock()
            lock = self.file_locks[key]

        acquired = lock.acquire(timeout=timeout)
        if not acquired:
            logging.warning(f"Could not acquire lock for {path}")
        return acquired

    def _release_file_lock(self, path: str):
        """Release file lock."""
        key = os.path.normpath(path)
        with self.file_locks_lock:
            if key in self.file_locks:
                try:
                    self.file_locks[key].release()
                except RuntimeError:
                    # Lock wasn't held
                    pass
                except Exception as e:
                    logging.error(f"Error releasing lock for {path}: {e}")

    def shutdown(self):
        """Shutdown the message sender."""
        logging.info("Shutting down backup engine...")
        if hasattr(self, 'message_sender') and self.message_sender_started:
            self.message_sender.shutdown()
        logging.info("Backup engine shutdown complete")
