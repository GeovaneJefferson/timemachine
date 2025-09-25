from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from has_driver_connection import has_driver_connection
import re # Added for package name parsing
from server import *

WAIT_TIME = 5  # Minutes between backup checks
HIGH_CPU_THRESHOLD = 75.0  # Max CPU

def send_to_ui(message: str):
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(server.SOCKET_PATH)
        sock.sendall(message.encode("utf-8"))
        sock.close()
    except socket.timeout:
        logging.warning(f"send_to_ui: Socket operation timed out for {server.SOCKET_PATH}.")
    except FileNotFoundError:
        logging.debug(f"send_to_ui: Socket file not found at {server.SOCKET_PATH}. UI likely not running or socket not created yet.")
    except ConnectionRefusedError:
        # This is common if UI is not running, can be debug level if too noisy
        logging.debug(f"send_to_ui: Connection refused at {server.SOCKET_PATH}. UI likely not running or not listening.")
    except Exception as e:
        # Log other unexpected errors during UI communication
        logging.warning(f"send_to_ui: Error communicating with UI via {server.SOCKET_PATH}: {e}")


class Daemon:
    ############################################################################
    # INITIALIZATION AND CONFIGURATION
    ############################################################################
    def __init__(self):
        """Initialize the daemon with necessary configurations and signal handlers."""
        self.copy_concurrency = server.DEFAULT_COPY_CONCURRENCY # Initialize with default
        self.executor = None # Initialize before first use in _update_copy_concurrency
        self.copy_semaphore = None # Initialize before first use in _update_copy_concurrency
        self.loop = None # To store the event loop for threadsafe calls

        self.user_home = server.USER_HOME
        self.excluded_dirs = {'__pycache__', 'snap'}
        self.excluded_exts = {'.crdownload', '.part', '.tmp'}
        self.ignored_folders = set(os.path.abspath(p) for p in server.load_ignored_folders_from_config())
        self.main_backup_dir = server.main_backup_folder()
        self.update_backup_dir = server.backup_folder_name()
        self.interruped_main_file = server.get_interrupted_main_file()

        # Initialize/Update executor and semaphore based on current conditions
        self._update_copy_concurrency()

        self.backup_in_progress = False
        self.suspend_flag = False
        self.should_exit = False
        self.had_writability_issue = False # Tracks if a writability issue was logged

    def _update_copy_concurrency(self):  # NONSONAR
        """Determine and update copy concurrency based on CPU cores and current load."""
        try:
            cpu_cores = os.cpu_count()
            cpu_load = psutil.cpu_percent(interval=0.1)

            LOW_CONCURRENCY_ON_HIGH_LOAD = max(1, (cpu_cores // 4) if cpu_cores else 1)

            if cpu_load > HIGH_CPU_THRESHOLD:
                new_concurrency = LOW_CONCURRENCY_ON_HIGH_LOAD
                logging.info(
                    f"High CPU load ({cpu_load}%) detected. "
                    f"Setting COPY_CONCURRENCY to a conservative {new_concurrency}."
                )
            else:
                new_concurrency = max(1, min(cpu_cores if cpu_cores else server.DEFAULT_COPY_CONCURRENCY, 8))
                logging.info(
                    f"CPU load ({cpu_load}%) is moderate. "
                    f"Setting COPY_CONCURRENCY to {new_concurrency} based on {cpu_cores or 'default'} CPU cores."
                )
        except Exception as e:
            logging.warning(
                f"Could not determine CPU cores/load, defaulting COPY_CONCURRENCY to {server.DEFAULT_COPY_CONCURRENCY}. Error: {e}"
            )
            new_concurrency = server.DEFAULT_COPY_CONCURRENCY

        if self.copy_concurrency != new_concurrency or self.executor is None:
            self.copy_concurrency = new_concurrency
            if self.executor:
                # Shutdown existing executor if it exists and concurrency changed
                self.executor.shutdown(wait=False) # Consider if wait=True is needed
            self.executor = ThreadPoolExecutor(max_workers=self.copy_concurrency)
            self.copy_semaphore = asyncio.Semaphore(self.copy_concurrency)
            logging.info(f"Copy concurrency updated to {self.copy_concurrency}. Executor and Semaphore re-initialized.")

    ############################################################################
    # SIGNAL HANDLING
    ############################################################################
    async def _send_ui_message_threadsafe(self, message_type: str):
        """Helper to send a status message to UI from a potentially different thread."""
        # This method is called via run_coroutine_threadsafe, so it runs in the event loop.
        try:
            message = {"type": message_type}
            send_to_ui(json.dumps(message)) # send_to_ui is synchronous
            logging.info(f"Sent '{message_type}' message to UI.")
        except Exception as e:
            logging.error(f"Error sending '{message_type}' to UI via _send_ui_message_threadsafe: {e}")

    def signal_handler(self, signum, frame):
        logging.info("")

        if signum == signal.SIGTSTP:
            logging.info(f"Received SIGTSTP (suspend), pausing daemon...")
            self.suspend_flag = True
            if self.loop and self.loop.is_running():
                asyncio.run_coroutine_threadsafe(self._send_ui_message_threadsafe("daemon_suspended"), self.loop)
        elif signum in (signal.SIGTERM, signal.SIGINT):
            logging.info(f"Received termination signal {signum}, stopping daemon...")
            self.should_exit = True
            if self.loop and self.loop.is_running():
                asyncio.run_coroutine_threadsafe(self._send_ui_message_threadsafe("daemon_stopping"), self.loop)

    def _compute_folder_metadata(self, folder_path, excluded_dirs=None, excluded_exts=None):
        """Compute total size, file count, and latest modification time for a folder."""
        total_size = 0
        latest_mtime = 0
        total_files = 0
    
        excluded_dirs = excluded_dirs or set()
        excluded_exts = excluded_exts or set()
    
        for root, dirs, files in os.walk(folder_path):
            if self.should_exit or self.suspend_flag:
                logging.debug(f"_compute_folder_metadata: Exiting or suspending during walk of {folder_path}.")
                break 
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in excluded_dirs]
            for f_loop in files: # Renamed f to f_loop
                if f_loop.startswith('.') or any(f_loop.endswith(ext) for ext in excluded_exts):
                    continue
                try:
                    full_path = os.path.join(root, f_loop)
                    stat_info = os.stat(full_path) # Renamed stat to stat_info
                    total_size += stat_info.st_size
                    if stat_info.st_mtime > latest_mtime:
                        latest_mtime = stat_info.st_mtime
                    total_files += 1
                except Exception:
                    pass  # Skip unreadable files
        return {
            "path": folder_path,
            "computed_at": time.time(),
            "total_files": total_files,
            "total_size": total_size,
            "latest_mtime": latest_mtime
        }
    
    def resume_handler(self, signum, frame):
        logging.info(f"Received resume signal {signum}, resuming operations.")
        self.suspend_flag = False
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self._send_ui_message_threadsafe("daemon_resumed"), self.loop)

    ############################################################################
    # BACKUP LOCATION AND PERMISSIONS
    ############################################################################
    def is_backup_location_writable(self) -> bool:
        """Checks if the base backup folder is writable."""
        base_path = server.create_base_folder()
        # Check if the path itself can be formed (e.g. DRIVER_LOCATION is set)
        try:
            os.makedirs(base_path, exist_ok=True)
        except OSError as e:
            logging.critical(f"Backup base path {base_path} does not exist and cannot be created: {e}")
            return False
        
        test_file_path = os.path.join(base_path, ".writetest.tmp")
        try:
            with open(test_file_path, "w") as f:
                f.write("test")
            os.remove(test_file_path)
            return True
        except OSError as e:
            logging.critical(f"Backup location {base_path} is not writable: {e}")
            return False

    ############################################################################
    # FILE HASHING AND COMPARISON
    ############################################################################
    def file_hash(self, path: str) -> str:
        """Compute SHA-256 hash of a file."""
        try:
            h = hashlib.sha256()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            logging.critical(f"Hash error: {path}: {e}")
            return ""

    def file_was_updated(self, src: str, rel_path: str) -> bool:
        """Check if a file differs from its backup versions."""
        try:
            current_stat = os.stat(src)
        except FileNotFoundError: #NOSONAR
            logging.warning(f"File '{rel_path}' not found at source '{src}'. Cannot compare.")
            return False
        # Add a src_hash_cache to avoid re-calculating hash for the same source file

        backup_dates = server.has_backup_dates_to_compare()
        for date_folder in backup_dates:
            try:
                datetime.strptime(date_folder, "%d-%m-%Y")
            except ValueError:
                continue

            date_path = os.path.join(self.update_backup_dir, date_folder)
            if not os.path.isdir(date_path):
                continue

            time_folders = []
            for t in os.listdir(date_path):
                try:
                    datetime.strptime(t, '%H-%M')
                    full_time_path = os.path.join(date_path, t)
                    if os.path.isdir(full_time_path):
                        time_folders.append(t)
                except ValueError:
                    continue

            time_folders.sort(reverse=True)

            for time_folder in time_folders:
                backup_file_path = os.path.join(date_path, time_folder, rel_path)
                if os.path.exists(backup_file_path):
                    try:
                        b_stat = os.stat(backup_file_path)
                        if b_stat.st_size != current_stat.st_size or abs(b_stat.st_mtime - current_stat.st_mtime) > 1:
                            # logging.info(f"File '{rel_path}' updated (size/mtime mismatch with incremental backup {backup_file_path}). Src size: {current_stat.st_size}, Dst size: {b_stat.st_size}. Src mtime: {current_stat.st_mtime}, Dst mtime: {b_stat.st_mtime}")
                            return True
                        if self.file_hash(src) != self.file_hash(backup_file_path):
                            # logging.info(f"File '{rel_path}' updated (hash mismatch with incremental backup {backup_file_path}).")
                            return True
                        return False
                    except Exception as e:
                        # logging.warning(f"Error comparing '{src}' with incremental backup '{backup_file_path}': {e}. Trying older versions or main.")
                        continue

        # Compare with the "main" backup (if no incremental version was found to match)
        main_path = os.path.join(self.main_backup_dir, rel_path)
        if os.path.exists(main_path):
            try:
                b_stat = os.stat(main_path)
                if b_stat.st_size != current_stat.st_size or abs(b_stat.st_mtime - current_stat.st_mtime) > 1:
                    # logging.info(f"File '{rel_path}' updated (size/mtime mismatch with main backup {main_path}). Src size: {current_stat.st_size}, Dst size: {b_stat.st_size}. Src mtime: {current_stat.st_mtime}, Dst mtime: {b_stat.st_mtime}")
                    return True
                if self.file_hash(src) != self.file_hash(main_path):
                    # logging.info(f"File '{rel_path}' updated (hash mismatch with main backup {main_path}).")
                    return True
                return False # Explicitly return False if it matches the main backup
            except Exception as e:
                # logging.warning(f"Error comparing '{src}' with main backup '{main_path}': {e}. Assuming update needed.")
                return True
            
        # If no backup (main or incremental) exists, or if main backup comparison failed, it's considered new/updated.
        logging.info(f"File '{rel_path}' is new or no existing valid backup was definitively matched. Marking for backup.")
        return True # Default to True if no existing backup is found or if errors occurred in main comparison

    ############################################################################
    # FILE COPYING (CORE BACKUP LOGIC)
    ############################################################################
    async def copy_file(self, src: str, dst: str, rel_path: str):
        async with self.copy_semaphore:
            file_id = rel_path  # Use rel_path as a unique ID for the UI
            filename = os.path.basename(src)
            total_size_bytes = 0
            human_readable_size = "N/A"

            try:
                total_size_bytes = os.path.getsize(src)
                human_readable_size = server.get_item_size(src, True)
            except OSError as e:
                logging.critical(f"Cannot get size of {src}: {e}")
                error_msg = {"id": file_id, "filename": filename, "size": human_readable_size, "eta": "error", "progress": 0.0, "error": f"Cannot access file: {e}"}
                send_to_ui(json.dumps(error_msg))
                return

            # Check for sufficient disk space
            threshold_bytes = 2 * 1024 * 1024 * 1024  # 2 GB
            try:
                _, _, device_free_size = shutil.disk_usage(server.DRIVER_LOCATION)
                if device_free_size <= (total_size_bytes + threshold_bytes):
                    logging.warning(f"Not enough space to backup: {src}. Required: {total_size_bytes}, Free: {device_free_size}")
                    error_msg = {"id": file_id, "filename": filename, "size": human_readable_size, "eta": "no space", "progress": 0.0, "error": "Not enough disk space"}
                    send_to_ui(json.dumps(error_msg))
                    return
            except Exception as e:
                logging.critical(f"Error checking disk space: {e}")
                error_msg = {"id": file_id, "filename": filename, "size": human_readable_size, "eta": "error", "progress": 0.0, "error": f"Disk check failed: {e}"}
                send_to_ui(json.dumps(error_msg))
                return

            os.makedirs(os.path.dirname(dst), exist_ok=True)
            loop = asyncio.get_event_loop()
            tmp_dst = dst + ".tmp"

            copied_bytes = 0
            start_time = time.time()
            last_update_time = start_time
            prev_progress = -0.01 # Ensure first update is sent

            # Send initial progress
            initial_msg = {
                "type": "transfer_progress",
                "id": file_id,
                "filename": filename,
                "size": human_readable_size,
                "eta": "calculating...",
                "progress": 0.0
            }
            send_to_ui(json.dumps(initial_msg))

            try:
                with open(src, 'rb') as fsrc, open(tmp_dst, 'wb') as fdst:
                    while True:
                        if self.should_exit or self.suspend_flag:
                            logging.info(f"Copy of {src} interrupted or suspended.")
                            if os.path.exists(tmp_dst): os.remove(tmp_dst)
                            # Optionally send a "cancelled" or "paused" status to UI
                            return

                        chunk = await loop.run_in_executor(self.executor, fsrc.read, 8192 * 16) # 128KB chunk
                        if not chunk:
                            break
                        await loop.run_in_executor(self.executor, fdst.write, chunk)
                        copied_bytes += len(chunk)
                        
                        progress = copied_bytes / total_size_bytes if total_size_bytes > 0 else 1.0
                        
                        current_time = time.time()
                        if progress > prev_progress + 0.01 or current_time - last_update_time > 0.5: # Update every 1% or 0.5s
                            elapsed_time = current_time - start_time
                            eta_str = "calculating..."
                            if progress > 0.001 and elapsed_time > 0.1:
                                bytes_per_second = copied_bytes / elapsed_time
                                if bytes_per_second > 0:
                                    remaining_bytes = total_size_bytes - copied_bytes
                                    remaining_seconds = remaining_bytes / bytes_per_second if remaining_bytes > 0 else 0
                                    eta_str = f"{int(remaining_seconds // 60)}m {int(remaining_seconds % 60)}s"
                                else:
                                    eta_str = "stalled"
                            
                            progress_msg = {
                                "type": "transfer_progress",
                                "id": file_id, 
                                "filename": filename, 
                                "size": human_readable_size, 
                                "eta": eta_str, "progress": progress}
                            send_to_ui(json.dumps(progress_msg))
                            prev_progress = progress
                            last_update_time = current_time

                with open(tmp_dst, 'rb') as f_tmp_for_fsync:
                    await loop.run_in_executor(self.executor, os.fsync, f_tmp_for_fsync.fileno())

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                os.replace(tmp_dst, dst)
                # Preserve metadata (including mtime) from src to dst
                await loop.run_in_executor(self.executor, shutil.copystat, src, dst)

                logging.info(f"Backed up: {src} -> {dst}")

                final_msg = {
                    "type": "transfer_progress",
                    "id": file_id, 
                    "filename": filename, 
                    "size": human_readable_size, 
                    "eta": "done", "progress": 1.0}
                send_to_ui(json.dumps(final_msg))
            except Exception as e:
                logging.critical(f"Error copying {src} -> {dst}: {e}")
                try:
                    if os.path.exists(tmp_dst):
                        os.remove(tmp_dst)
                except Exception:
                    pass
                error_msg = {
                    "type": "transfer_progress", # Or a dedicated "transfer_error" type
                    "id": file_id,
                    "filename": filename,
                    "size": human_readable_size,
                    "eta": "error",
                    "progress": prev_progress if prev_progress > 0 else 0.0,
                    "error": str(e)}
                send_to_ui(json.dumps(error_msg))

    async def _backup_package_file(self, src_path: str, dest_folder: str):
        """Backs up a package file from Downloads to the specified destination folder."""
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_folder, filename)
        try:
            # Ensure the destination directory exists
            await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: os.makedirs(dest_folder, exist_ok=True)
            )
            # Copy the file
            await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: shutil.copy2(src_path, dest_path)  # copy2 preserves metadata
            )
            logging.info(f"Backed up downloaded package: {src_path} -> {dest_path}")
        except Exception as e:
            logging.critical(f"Error backing up downloaded package {src_path} to {dest_path}: {e}")

    ############################################################################
    # FOLDER METADATA HANDLING
    ############################################################################
    def load_folder_metadata(self, top_rel_path):
        meta_path = os.path.join(self.main_backup_dir, top_rel_path, '.backup_meta.json')
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r') as f:
                    data = json.load(f)
                return data
            except Exception:
                pass
        return {}
    
    def save_folder_metadata(self, top_rel_path, metadata):
        meta_path = os.path.join(self.main_backup_dir, top_rel_path, '.backup_meta.json')
        try:
            os.makedirs(os.path.dirname(meta_path), exist_ok=True)

            with tempfile.NamedTemporaryFile('w', delete=False, dir=os.path.dirname(meta_path)) as tmpf:
                json.dump(metadata, tmpf, indent=4) # Added indent for readability
                temp_path = tmpf.name
            # Ensure data is written to disk before replacing
            # For NamedTemporaryFile, flush and fsync can be explicit if needed,
            # but os.replace is atomic on POSIX if src and dst are on the same filesystem.
            os.replace(temp_path, meta_path)
        except OSError as e:
            logging.critical(f"OSError while saving folder metadata for {top_rel_path} at {meta_path}: {e}")
        except Exception as e:
            logging.critical(f"Unexpected error while saving folder metadata for {top_rel_path} at {meta_path}: {e}")
        
    def folder_needs_check(self, rel_folder, current_meta, cached_meta):
        cached = cached_meta.get(rel_folder)
        if cached is None:
            return True
        for key in ('total_files', 'total_size', 'latest_mtime'):
            cached_val = cached.get(key)
            current_val = current_meta.get(key)
            if cached_val != current_val:
                return True
        return False

    ############################################################################
    # DOWNLOADED PACKAGES BACKUP
    ############################################################################
    # async def _backup_downloaded_packages(self):
    #     """Scans ~/Downloads for .deb/.rpm packages and backs them up if new."""
    #     logging.info("")
    #     logging.info("Starting scan of Downloads for new packages...")
    #     downloads_path = os.path.join(self.user_home, "Downloads")
        
    #     if not os.path.isdir(downloads_path):
    #         logging.warning(f"Downloads folder not found at {downloads_path}. Skipping package backup.")
    #         return

    #     if not server.DRIVER_LOCATION:
    #         logging.warning("Backup device not connected. Skipping package backup.")
    #         return
        
    #     if not self.is_backup_location_writable():
    #         logging.warning("[CRITICAL]: Backup device is not writable. Skipping package backup.")
    #         return 

    #     package_backup_tasks = []
    #     for item_name in os.listdir(downloads_path):
    #         item_path = os.path.join(downloads_path, item_name)
    #         if os.path.isfile(item_path):
    #             dest_folder = None
    #             if item_name.endswith(".deb"):
    #                 dest_folder = server.deb_main_folder()
    #             elif item_name.endswith(".rpm"):
    #                 dest_folder = server.rpm_main_folder()

    #             if dest_folder:
    #                 # Check if package with the same name already exists in backup
    #                 backed_up_package_path = os.path.join(dest_folder, item_name)
    #                 if not os.path.exists(backed_up_package_path):
    #                     logging.info(f"New package found in Downloads: {item_name}. Queuing for backup.")
    #                     package_backup_tasks.append(self._backup_package_file(item_path, dest_folder))
        
    #     if package_backup_tasks:
    #         await asyncio.gather(*package_backup_tasks)
    #         logging.info(f"Finished backing up {len(package_backup_tasks)} new package(s) from Downloads.")
    #     else:
    #         logging.info("No new packages found in Downloads to backup.")
        
    #     logging.info("")
    
    # def _get_package_info(self, filename: str) -> tuple[str | None, str | None, str | None]:
    #     """
    #     Extracts package information (name, version, extension) from a filename.
    #     Returns a tuple of (base_name, version, extension).
    #     """
    #     name_root, ext = os.path.splitext(filename)
    #     if ext not in [".deb", ".rpm"]:
    #         return None, None, None

    #     # This regex is more robust. It looks for a sequence of digits and dots,
    #     # optionally followed by a hyphen and a mix of letters and numbers.
    #     # It finds the last such sequence in the name before the extension.
    #     match = re.search(r'([\d.]+)(?:[_-][a-zA-Z\d-]+)*$', name_root)
        
    #     if match:
    #         version = match.group(1)
    #         base_name = name_root[:match.start()]
    #         # Clean up any trailing hyphens or underscores from the base name
    #         base_name = base_name.rstrip('_-')
    #         return base_name, version, ext
    #     else:
    #         return name_root, "0", ext # Return a default version for comparison
   
    # def find_latest_package(self, filenames: list[str]) -> str | None:
    #     """
    #     Given a list of filenames, returns the name of the latest package.
    #     """
    #     latest_package = None
    #     latest_version = Version("0") # Initialize with a very low version

    #     for filename in filenames:
    #         base_name, version_str, ext = self._get_package_info(filename)
            
    #         if not all([base_name, version_str, ext]):
    #             continue
            
    #         try:
    #             current_version = Version(version_str)
    #             if current_version > latest_version:
    #                 latest_version = current_version
    #                 latest_package = filename
    #         except InvalidVersion:
    #             # If the version string is invalid, just skip it.
    #             # You could add logging here to track malformed filenames.
    #             continue
        
    #     return latest_package

    async def _backup_downloaded_packages(self):
        """Scans ~/Downloads for .deb/.rpm packages and backs them up if new."""
        logging.info("Starting scan of Downloads for new packages...")

        downloads_path = os.path.join(self.user_home, "Downloads")
        
        if not os.path.isdir(downloads_path):
            logging.warning(f"Downloads folder not found at {downloads_path}. Skipping package backup.")
            return
        
        if not self._can_write_to_backup_location():
            return

        package_backup_tasks = []
        for item_name in os.listdir(downloads_path):
            item_path = os.path.join(downloads_path, item_name)
            if os.path.isfile(item_path):
                dest_folder = self._get_package_destination(item_path)
                if dest_folder:
                    # Check if package with the same name already exists in backup
                    backed_up_package_path = Path(dest_folder) / item_path
                    if not backed_up_package_path.exists():
                        logging.info(f"New package found in Downloads: {item_path}. Queuing for backup.")
                        package_backup_tasks.append(self._backup_package_file(item_path, dest_folder))
        
        if package_backup_tasks:
            await asyncio.gather(*package_backup_tasks)
            logging.info(f"Finished backing up {len(package_backup_tasks)} new package(s) from Downloads.")
        else:
            logging.info("No new packages found in Downloads to backup.")
        
        logging.info("")

    def _get_package_destination(self, filename: str) -> str | None:
        """Returns the destination folder for a package file based on its extension."""
        if filename.endswith(".deb"):
            return server.deb_main_folder()
        if filename.endswith(".rpm"):
            return server.rpm_main_folder()
        return None
    
    def _can_write_to_backup_location(self) -> bool:
        """Checks for both device connection and writability, logs messages."""
        if not has_driver_connection():
            logging.info("Backup device not connected. Skipping package backup.")
            return False
        
        if not self.is_backup_location_writable():
            self.had_writability_issue = True
            logging.warning("[CRITICAL]: Backup device is not writable. Skipping package backup.")
            return False
        
        self.had_writability_issue = False
        return True

    ############################################################################
    # MAIN BACKUP PROCESS
    ############################################################################
    async def scan_and_backup(self):
        """
        Main backup loop. Scans the user's home directory for new/updated files and backs them up.
        """
        if self.should_exit or self.suspend_flag:
            logging.info("scan_and_backup: Exiting or suspending at method start.")
            return

        session_backup_dir = self._prepare_backup_session()
        if not session_backup_dir:
            return

        tasks = []
        try:
            for entry in os.scandir(self.user_home):
                if self.should_exit or self.suspend_flag:
                    logging.info("scan_and_backup: Exiting or suspending during user home scan.")
                    break
                
                await self._scan_and_process_entry(entry, session_backup_dir, tasks)

            if tasks:
                await asyncio.gather(*tasks)
                logging.info("All backup tasks completed.")
        except Exception as e:
            logging.critical(f"An unexpected error occurred during the backup process: {e}", exc_info=True)
        finally:
            if not self.should_exit and not self.suspend_flag:
                await self._finalize_backup_session(session_backup_dir)
            else:
                logging.info("Backup session interrupted. Skipping finalization.")

    def _prepare_backup_session(self) -> str | None:
        """Handles pre-backup setup tasks."""
        self._update_copy_concurrency()
        
        now = datetime.now()
        date_str = now.strftime('%d-%m-%Y')
        time_str = now.strftime('%H-%M')
        session_backup_dir = os.path.join(self.update_backup_dir, date_str, time_str)
        
        # Reload configuration settings
        self.ignored_folders = set(os.path.abspath(p) for p in server.load_ignored_folders_from_config())

        # Write the interrupted file to indicate a backup is in progress
        try:
            with open(self.interruped_main_file, 'w') as f:
                f.write("interrupted")
        except OSError as e:
            logging.critical(
                f"Could not write to interrupted_main_file {self.interruped_main_file}: {e}. "
                "This may indicate a read-only filesystem or permissions issue."
            )
            return None
        
        return session_backup_dir

    async def _scan_and_process_entry(self, entry: os.DirEntry, session_backup_dir: str, tasks: list):
        """Processes a single file or directory entry from the user's home."""
        exclude_hidden = server.get_database_value(
            section='EXCLUDE', 
            option='exclude_hidden_itens')
            
        if (exclude_hidden and entry.name.startswith('.')) or \
           entry.name in self.excluded_dirs:
            return

        src_path = entry.path
        if any(os.path.commonpath([src_path, ign]) == ign for ign in self.ignored_folders):
            return

        try:
            if entry.is_dir():
                await self._process_folder_entry(src_path, session_backup_dir, tasks)
            elif entry.is_file():
                await self._process_file_entry(src_path, session_backup_dir, tasks)
        except Exception as e:
            logging.warning(f"Error processing entry {src_path}: {e}")

    async def _process_folder_entry(self, folder_path: str, session_backup_dir: str, tasks: list):
        """Scans a directory recursively and queues files for backup."""
        top_level_rel_path = os.path.relpath(folder_path, self.user_home)
        cached_meta = self.load_folder_metadata(top_level_rel_path)
        new_meta = {}

        exclude_hidden = server.get_database_value(
            section='EXCLUDE', 
            option='exclude_hidden_itens')

        for root, dirs, files_in_dir in os.walk(folder_path):
            if self.should_exit or self.suspend_flag:
                logging.info(f"Exiting or suspending during os.walk of {folder_path}.")
                break
            
            # Filter directories in-place
            dirs[:] = [d for d in dirs if not ((exclude_hidden and d.startswith('.')) or d in self.excluded_dirs)]
            send_to_ui(json.dumps({
                "type": "scanning",
                "folder": os.path.relpath(root, self.user_home).replace("\\", "/")
            }))
            
            subfolder_key = os.path.relpath(root, folder_path).replace("\\", "/")
            current_meta = self._compute_folder_metadata(
                root, excluded_dirs=self.excluded_dirs, excluded_exts=self.excluded_exts
            )
            new_meta[subfolder_key] = current_meta

            if not self.folder_needs_check(subfolder_key, current_meta, cached_meta):
                continue

            for f_name in files_in_dir:
                fsrc = os.path.join(root, f_name)
                frel = os.path.relpath(fsrc, self.user_home)

                if (exclude_hidden and f_name.startswith('.')) or \
                   any(f_name.endswith(ext) for ext in self.excluded_exts):
                    continue

                if self.should_exit or self.suspend_flag:
                    break

                if not os.path.exists(os.path.join(self.main_backup_dir, frel)):
                    tasks.append(self.copy_file(fsrc, os.path.join(self.main_backup_dir, frel), frel))
                elif self.file_was_updated(fsrc, frel):
                    tasks.append(self.copy_file(fsrc, os.path.join(session_backup_dir, frel), frel))

        self.save_folder_metadata(top_level_rel_path, new_meta)

    async def _process_file_entry(self, file_path: str, session_backup_dir: str, tasks: list):
        """Queues a single file for backup."""
        frel = os.path.relpath(file_path, self.user_home)
        main_path = os.path.join(self.main_backup_dir, frel)

        exclude_hidden = server.get_database_value(
            section='EXCLUDE', 
            option='exclude_hidden_itens')

        if (exclude_hidden and os.path.basename(file_path).startswith('.')) or \
           any(os.path.basename(file_path).endswith(ext) for ext in self.excluded_exts):
            return

        if not os.path.exists(main_path):
            tasks.append(self.copy_file(file_path, main_path, frel))
        elif self.file_was_updated(file_path, frel):
            tasks.append(self.copy_file(file_path, os.path.join(session_backup_dir, frel), frel))

    async def _finalize_backup_session(self, session_backup_dir: str):
        """Performs post-backup tasks and cleanup."""
        server.update_recent_backup_information()
        
        # Run the backup summary script
        try:
            summary_script_path = os.path.join(os.path.dirname(__file__), 'generate_backup_summary.py')
            sub.run(['python3', summary_script_path], check=True, capture_output=True, text=True)
            send_to_ui(json.dumps({"type": "summary_updated"}))
            logging.info("Backup summary generated successfully.")
        except sub.CalledProcessError as e:
            logging.warning(f"Failed to generate backup summary. Return code: {e.returncode}")
        except Exception as e:
            logging.critical(f"Unexpected error while generating backup summary: {e}")

        # Check for new packages and Flatpaks if the device is writable
        if server.DRIVER_LOCATION and self.is_backup_location_writable():
            await self._backup_downloaded_packages()
            await self.backup_flatpaks()

        # Remove the interrupted file and clean up empty folders
        try:
            if os.path.exists(self.interruped_main_file):
                os.remove(self.interruped_main_file)
        except OSError as e:
            logging.critical(f"Could not remove interrupted_main_file: {e}. Check filesystem permissions.")
        
        self._cleanup_empty_incremental_folders(session_backup_dir)
        logging.info("Backup session complete.")

    ############################################################################
    # CLEANUP OF EMPTY INCREMENTAL FOLDERS
    ############################################################################
    def _cleanup_empty_incremental_folders(self, session_backup_dir: str):
        """
        Removes the session backup directory if it's empty.
        Also removes the parent date directory if it becomes empty as a result.
        """
        try:
            if not os.path.exists(session_backup_dir):
                logging.info(f"Session backup folder does not exist: {session_backup_dir}. Skipping cleanup.")
                return

            if not os.listdir(session_backup_dir): # Check if HH-MM folder is empty
                logging.info(f"Removing empty incremental session folder: {session_backup_dir}")
                os.rmdir(session_backup_dir)

                # Check and remove parent date folder if it's now empty
                date_dir = os.path.dirname(session_backup_dir)
                if os.path.exists(date_dir) and not os.listdir(date_dir):
                    logging.info(f"Removing empty incremental date folder: {date_dir}")
                    os.rmdir(date_dir)
            # else:
                # logging.info(f"Incremental session folder {session_backup_dir} is not empty.")
        except OSError as e:
            logging.critical(f"Error during cleanup of empty incremental folders for {session_backup_dir}: {e}")
            
    ############################################################################
    # INTERRUPTION HANDLING
    ############################################################################
    async def resume_from_interruption(self):
        if os.path.exists(self.interruped_main_file):
            logging.info("Interrupted backup session file found.")
            if self.is_backup_location_writable():
                logging.info("Backup location is writable. Attempting to resume interrupted backup...")
                await self.scan_and_backup() 
            else:
                if not self.had_writability_issue:
                    logging.critical(f"[CRITICAL]: Backup location {server.create_base_folder()} is not writable. Automatic backups will be disabled by the UI if running.")
                    self.had_writability_issue = True
    
    ####################################################################
    # Flatpak
    ####################################################################
    async def _execute_flatpak_command(self, command: list) -> str | None:
        """
        Executes a given command asynchronously and returns its stdout on success.
        Returns None on failure.
        """
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                # logging.info(f"Successfully executed: {' '.join(command)}")
                return stdout.decode('utf-8').strip()
            else:
                error_msg = stderr.decode('utf-8').strip()
                logging.warning(f"Command failed: {' '.join(command)}\nError: {error_msg}")
                return None

        except FileNotFoundError:
            # logging.warning(f"Command not found: '{command[0]}'.")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred with command {' '.join(command)}: {e}")
            return None

    async def _save_flatpak_list(self, content: str):
        """Saves the flatpak list content to the backup file asynchronously."""
        backup_path = server.flatpak_txt_location()
        loop = asyncio.get_event_loop()
        
        try:
            # Run blocking I/O in the executor to avoid stalling the event loop
            await loop.run_in_executor(
                self.executor,
                lambda: (
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True),
                    (lambda f: f.write(content + "\n"))(open(backup_path, "w", encoding="utf-8"))
                )
            )
            logging.info(f"Successfully backed up Flatpak application list to {backup_path}")
        except Exception as e:
            logging.critical(f"Failed to write Flatpak backup file to {backup_path}: {e}")

    async def backup_flatpaks(self):
        """
        Backs up the list of installed Flatpak applications.
        """
        logging.info("Starting Flatpak application backup...")

        # 1. Pre-checks: Ensure the backup location is ready
        if not has_driver_connection() or not self.is_backup_location_writable():
            logging.warning("Backup device not available or not writable. Skipping Flatpak backup.")
            return

        # 2. Define commands to try
        commands_to_try = [
            server.GET_FLATPAKS_APPLICATIONS_NAME_CONTAINER.split(),
            server.GET_FLATPAKS_APPLICATIONS_NAME_NON_CONTAINER.split()
        ]
        
        # 3. Execute commands until one succeeds
        output = None
        for command in commands_to_try:
            output = await self._execute_flatpak_command(command)
            if output is not None:
                break  # Stop on the first successful command

        # 4. Save the output if successful
        if output is not None:
            await self._save_flatpak_list(output)
        else:
            logging.error("All attempts to list Flatpak applications failed.")

    ############################################################################
    # DAEMON MAIN RUN LOOP
    ############################################################################,
    def _setup_signal_handlers(self, shutdown_event: asyncio.Event):
        """Configures the signal handlers for the daemon."""
        
        def stop_loop_for_termination(signum, frame):
            """Handler for SIGTERM and SIGINT."""
            logging.debug(f"stop_loop_for_termination called for signal {signum}")
            self.signal_handler(signum, frame)
            shutdown_event.set()

        signal.signal(signal.SIGTERM, stop_loop_for_termination)
        signal.signal(signal.SIGINT, stop_loop_for_termination)
        signal.signal(signal.SIGTSTP, self.signal_handler)  # Suspend (Ctrl+Z)
        signal.signal(signal.SIGCONT, self.resume_handler)  # Resume

    async def _wait_for_next_cycle(self, shutdown_event: asyncio.Event):
        """Waits for the configured time in an interruptible manner."""
        logging.info(f"Waiting for {WAIT_TIME} minutes before next cycle.")
        total_wait_seconds = WAIT_TIME * 60
        check_interval = 1.0  # seconds

        try:
            # This waits for the total duration, but checks the event every second.
            # If the shutdown_event is set, it will wake up immediately.
            await asyncio.wait_for(shutdown_event.wait(), timeout=total_wait_seconds)
        except asyncio.TimeoutError:
            # This is the expected outcome after waiting the full duration.
            pass 

    async def _perform_backup_cycle(self):
        """Checks for the backup device and runs the backup if available."""
        # BUG:
        """
        Device is not connected but looks like has_driver_connection() is returning True
        because, if self.is_backup_location_writable() is being called, even disconnected.
        """
        if not self._can_write_to_backup_location():
            return

        await self.scan_and_backup()

    async def _run_health_checks(self) -> bool:
            """
            Performs periodic checks to ensure the daemon should continue running.
            Returns False if the daemon should shut down.
            """
            # 1. Check for suspension
            if self.suspend_flag:
                logging.info("Daemon suspended... sleeping.")
                await asyncio.sleep(5)
                return True # Continue running, but skip this cycle's work

            # 2. Check if the UI socket file was removed
            if not os.path.exists(server.SOCKET_PATH):
                logging.info(f"Socket file {server.SOCKET_PATH} was removed externally. Shutting down.")
                self.signal_handler(signal.SIGTERM, None)
                return False # Stop running

            # 3. Check if auto-backup is still enabled in the config
            auto_backup_enabled = server.get_database_value('BACKUP', 'automatically_backup')
            if str(auto_backup_enabled).lower() != 'true':
                logging.info("Automatic backup is disabled in configuration. Shutting down.")
                self.signal_handler(signal.SIGTERM, None)
                return False # Stop running
            
            return True
    
    async def run(self):
        self.loop = asyncio.get_running_loop() # Store the loop for threadsafe calls
        self.pid = str(os.getpid())

        # await self.resume_from_interruption()
        shutdown_event = asyncio.Event()
        self._setup_signal_handlers(shutdown_event)

        logging.info("Daemon started. Performing initial checks...")
        
        while not self.should_exit:
            # should_continue = await self._run_health_checks()
            # if not should_continue:
            #     break

            # If suspended, the health check will sleep and we can skip the backup cycle
            if self.suspend_flag:
                continue

            await self._perform_backup_cycle()

            await self._wait_for_next_cycle(shutdown_event)
            
            logging.info("Daemon main loop finished.")


################################################################################
# MAIN EXECUTION BLOCK
################################################################################
if __name__ == "__main__":
    # Print a message immediately upon starting, before any complex initialization.
    server = SERVER()

    # Ensure the directory for the log file exists, attempt to create if not.
    # This is important if DRIVER_LOCATION is initially unavailable.
    log_file_path = server.get_log_file_path()
    daemon_obj = None # Initialize to None

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True) 
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    setproctitle.setproctitle(f'{server.APP_NAME} - daemon')

    try:
        daemon_obj = Daemon() # daemon_obj.pid will be set inside daemon_obj.run()
        asyncio.run(daemon_obj.run())
    except SystemExit: # Handle cases where daemon exits cleanly via sys.exit()
        logging.info("Daemon received SystemExit.")
    except KeyboardInterrupt: # Handle Ctrl+C
        logging.info("Daemon interrupted by user (KeyboardInterrupt).")
    except Exception as e:
        logging.critical(f"Unhandled exception in daemon's main execution block: {e}", exc_info=True)
    finally:
        logging.info("Daemon shutting down (finally block reached).")

        # Executor shutdown
        if daemon_obj and hasattr(daemon_obj, 'executor') and daemon_obj.executor:
            daemon_obj.executor.shutdown(wait=True)
