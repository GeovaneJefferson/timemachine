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
    
    def start_message_sender(self):
        """Start the message sender thread."""
        if not self.message_sender_started:
            self.message_sender.start()
            self.message_sender_started = True

    def process_change(self, path: str, event_type: str):
        """Process file change event."""
        # Start message sender if not already started
        self.start_message_sender()

        if event_type == 'deleted':
            self._handle_file_deletion(path)
        elif event_type == 'moved':
            # For moved events, we need both src and dest
            # This will be handled differently
            pass
        else:
            self._process_file_change(path, event_type)

    def _process_file_change(self, path: str, event_type: str):
        """Process file creation or modification."""
        if not os.path.exists(path):
            return
        
        rel_path = normalize_rel_path(path)
        
        try:
            stat_result = os.stat(path)
            file_size = stat_result.st_size
            current_mtime = stat_result.st_mtime

            # Cooldown check
            current_time = time.time()
            last_time = self.last_processed_time.get(rel_path, 0)
            if current_time - last_time < MIN_REPROCESS_INTERVAL:
                logging.debug(f"Cooldown active for {rel_path}. Ignoring event.")
                return

            self.message_sender.send_file_status(rel_path, 'Processing', file_size, 'processing')
            
            # Calculate hash
            file_hash = calculate_sha256(path, file_size=file_size)
            if not file_hash:
                return

            # Check if content changed - FIXED: use dictionary access
            metadata = self.daemon.metadata.get(rel_path, {})
            if metadata.get('hash') == file_hash:
                # Same content, update timestamp
                with self.daemon.state_lock:
                    if rel_path in self.daemon.metadata:
                        self.daemon.metadata[rel_path]['mtime'] = current_mtime
                logging.debug(f"File unchanged: {rel_path}")
                return

            # Determine if new file - FIXED: use 'in' operator
            is_new = rel_path not in self.daemon.metadata

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
                
        except Exception as e:
            logging.error(f"Error processing file change for {path}: {e}")

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
        else:
            dest = os.path.join(self.daemon.app_incremental_backup_dir, rel_path)

        os.makedirs(os.path.dirname(dest), exist_ok=True)

        success = False

        try:
            # Handle special files
            if handle_special_file(source, dest):
                success = True
            else:
                # Try atomic copy
                success = self._perform_atomic_copy(source, dest)

            if success:
                self._update_metadata(rel_path, dest, file_info)
                logging.info(f"Backed up: {rel_path} -> {dest}")
                
        except Exception as e:
            logging.error(f"Failed to process {rel_path}: {e}")

        return success

    def _perform_atomic_copy(self, src_path: str, final_dst_path: str) -> bool:
        """Atomic file copy with temp file."""
        if not os.path.exists(src_path):
            return False

        temp_dst_path = f"{final_dst_path}.tmp_{os.getpid()}_{uuid.uuid4().hex}"

        try:
            os.makedirs(os.path.dirname(final_dst_path), exist_ok=True)

            # Copy file
            with open(src_path, 'rb') as fr, open(temp_dst_path, 'wb') as fw:
                shutil.copyfileobj(fr, fw)

            # Preserve metadata
            try:
                shutil.copystat(src_path, temp_dst_path)
            except:
                pass

            # Atomic rename
            os.rename(temp_dst_path, final_dst_path)
            return True
            
        except Exception as e:
            logging.error(f"Atomic copy failed for {src_path}: {e}")
            if os.path.exists(temp_dst_path):
                os.remove(temp_dst_path)
            return False

    def _update_metadata(self, rel_path: str, dst_path: str, file_info: dict):
        """Update metadata after successful backup."""
        with self.daemon.state_lock:
            self.daemon.metadata[rel_path] = {
                'path': dst_path,
                'mtime': file_info.get('mtime', time.time()),
                'size': file_info.get('size'),
                'hash': file_info.get('file_hash'),
            }

            file_hash = file_info.get('file_hash')
            if file_hash:
                self.daemon.metadata.hash_to_path_map[file_hash] = dst_path

    def _handle_file_deletion(self, path: str):
        """Mark file as deleted in metadata."""
        with self.daemon.state_lock:
            rel_path = normalize_rel_path(path)
            if rel_path in self.daemon.metadata:
                self.daemon.metadata[rel_path]['deleted'] = True
                self.daemon.metadata[rel_path]['deleted_time'] = time.time()

                # Cleanup hash map if needed
                file_hash = self.daemon.metadata[rel_path].get('hash')
                if file_hash:
                    all_refs = [k for k, v in self.daemon.metadata.items()
                               if v.get('hash') == file_hash and not v.get('deleted', False)]
                    
                    if not all_refs and file_hash in self.daemon.metadata.hash_to_path_map:
                        del self.daemon.metadata.hash_to_path_map[file_hash]

        # logging.info(f"Marked as deleted: {rel_path}")

    def _acquire_file_lock(self, path: str, timeout: int = 5) -> bool:
        """Acquire file lock with timeout."""
        key = os.path.normpath(path)

        with self.file_locks_lock:
            if key not in self.file_locks:
                self.file_locks[key] = threading.Lock()
            lock = self.file_locks[key]

        return lock.acquire(timeout=timeout)

    def _release_file_lock(self, path: str):
        """Release file lock."""
        key = os.path.normpath(path)
        with self.file_locks_lock:
            if key in self.file_locks:
                try:
                    self.file_locks[key].release()
                except:
                    pass

    def shutdown(self):
        """Shutdown the message sender."""
        if hasattr(self, 'message_sender'):
            self.message_sender.shutdown()