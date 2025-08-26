from concurrent.futures import ThreadPoolExecutor
from has_driver_connection import has_driver_connection
import re # Added for package name parsing
from server import *

WAIT_TIME = 5  # Minutes between backup checks


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

            HIGH_CPU_THRESHOLD = 75.0
            LOW_CONCURRENCY_ON_HIGH_LOAD = max(1, (cpu_cores // 4) if cpu_cores else 1)

            if cpu_load > HIGH_CPU_THRESHOLD:
                new_concurrency = LOW_CONCURRENCY_ON_HIGH_LOAD
                # logging.info(
                #     f"High CPU load ({cpu_load}%) detected. "
                #     f"Setting COPY_CONCURRENCY to a conservative {new_concurrency}."
                # )
            else:
                new_concurrency = max(1, min(cpu_cores if cpu_cores else server.DEFAULT_COPY_CONCURRENCY, 8))
                # logging.info(
                #     f"CPU load ({cpu_load}%) is moderate. "
                #     f"Setting COPY_CONCURRENCY to {new_concurrency} based on {cpu_cores or 'default'} CPU cores."
                # )
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
    
    def _get_package_info(self, filename: str) -> tuple[str | None, str | None, str | None]:
        """
        Extracts the base name, version/architecture string, and extension from a package filename.
        Returns (base_name, version_arch_part, extension) or (None, None, None) if not a package.
        - base_name: The name of the package without version/arch info.
        - version_arch_part: The part of the filename typically containing version and architecture.
                             Includes the leading separator (_ or -). Is empty if no version detected.
        - extension: .deb or .rpm
        """
        name_root, ext = os.path.splitext(filename)
        if ext not in [".deb", ".rpm"]:
            return None, None, None

        # Heuristic: find the first hyphen or underscore followed by a digit.
        # Example: 'code_1.2.3-amd64' -> base='code', version_arch='_1.2.3-amd64'
        # Example: 'mypkg-1.0' -> base='mypkg', version_arch='-1.0'
        match = re.search(r"(_|-)(?=\d)", name_root)
        if match:
            split_index = match.start()
            base_name = name_root[:split_index]
            version_arch_part = name_root[split_index:] 
            return base_name, version_arch_part, ext
        else:
            # If no version-like pattern is found, consider the whole name (without ext) as base_name.
            return name_root, "", ext
        
    ############################################################################
    # DOWNLOADED PACKAGES BACKUP
    ############################################################################
    async def _backup_downloaded_packages(self):
        """Scans ~/Downloads for .deb/.rpm packages and backs them up if new."""
        logging.info("Starting scan of Downloads for new packages...")
        downloads_path = os.path.join(self.user_home, "Downloads")
        if not os.path.isdir(downloads_path):
            logging.warning(f"Downloads folder not found at {downloads_path}. Skipping package backup.")
            return

        if not server.DRIVER_LOCATION:
            logging.warning("Backup device not connected. Skipping package backup.")
            return
        
        if not self.is_backup_location_writable():
            logging.warning("[CRITICAL]: Backup device is not writable. Skipping package backup.")
            return 

        package_backup_tasks = []
        for item_name in os.listdir(downloads_path):
            item_path = os.path.join(downloads_path, item_name)
            if os.path.isfile(item_path):
                dest_folder = None
                if item_name.endswith(".deb"):
                    dest_folder = server.deb_main_folder()
                elif item_name.endswith(".rpm"):
                    dest_folder = server.rpm_main_folder()

                if dest_folder:
                    # Check if package with the same name already exists in backup
                    backed_up_package_path = os.path.join(dest_folder, item_name)
                    if not os.path.exists(backed_up_package_path):
                        logging.info(f"New package found in Downloads: {item_name}. Queuing for backup.")
                        package_backup_tasks.append(self._backup_package_file(item_path, dest_folder))
        
        if package_backup_tasks:
            await asyncio.gather(*package_backup_tasks)
            logging.info(f"Finished backing up {len(package_backup_tasks)} new package(s) from Downloads.")
        else:
            logging.info("No new packages found in Downloads to backup.")
            
    ############################################################################
    # MAIN BACKUP PROCESS
    ############################################################################
    async def scan_and_backup(self):
        if self.should_exit or self.suspend_flag:
            logging.info("scan_and_backup: Exiting or suspending at method start.")
            return

        # Update concurrency settings at the beginning of each scan
        self._update_copy_concurrency()

        tasks = []
        now = datetime.now()
        date_str = now.strftime('%d-%m-%Y')
        time_str = now.strftime('%H-%M')
        session_backup_dir = os.path.join(self.update_backup_dir, date_str, time_str)

        # Reload ignored folders and hidden items preference at the start of each scan
        self.ignored_folders = set(os.path.abspath(p) for p in server.load_ignored_folders_from_config())
        exclude_hidden_master_switch = server.get_database_value(section='EXCLUDE', option='exclude_hidden_itens')
        if exclude_hidden_master_switch is None: # Default to True if not set
            exclude_hidden_master_switch = True

        try:
            with open(self.interruped_main_file, 'w') as f:
                f.write("interrupted")
        except OSError as e:
            logging.critical(f"Could not write to interrupted_main_file {self.interruped_main_file}: {e}. "
                          "Backup may not resume correctly if interrupted again. "
                          "This may indicate a read-only filesystem.")
            # Depending on severity, might return or raise to stop the backup cycle

        if self.should_exit or self.suspend_flag: # Check after writing interrupted file
            logging.info("scan_and_backup: Exiting or suspending after writing interrupted_main_file.")
            return
        for entry in os.scandir(self.user_home):
            if (exclude_hidden_master_switch and entry.name.startswith('.')) or \
               entry.name in self.excluded_dirs:
                continue

            src_path = entry.path
            top_level_rel_path = os.path.relpath(src_path, self.user_home)

            # Skip ignored folders
            if any(os.path.commonpath([src_path, ign]) == ign for ign in self.ignored_folders):
                continue
            
            if self.should_exit or self.suspend_flag:
                logging.info(f"scan_and_backup: Exiting or suspending before processing entry: {entry.name}")
                return

            if entry.is_dir():
                cached_meta = self.load_folder_metadata(top_level_rel_path)
                new_meta = {}

                for root, dirs, files_in_dir in os.walk(src_path): # Renamed 'files' to 'files_in_dir'
                    if self.should_exit or self.suspend_flag:
                        logging.info(f"scan_and_backup: Exiting or suspending during os.walk of {src_path}.")
                        return

                    # Filter directories based on hidden status and excluded_dirs
                    dirs[:] = [d for d in dirs if not ((exclude_hidden_master_switch and d.startswith('.')) or \
                                                       d in self.excluded_dirs)]
                    send_to_ui(json.dumps({
                        "type": "scanning",
                        "folder": os.path.relpath(root, self.user_home).replace("\\", "/")
                    }))
                    subfolder_key = os.path.relpath(root, src_path).replace("\\", "/")
        
                    current_meta = self._compute_folder_metadata(
                        root,
                        excluded_dirs=self.excluded_dirs,
                        excluded_exts=self.excluded_exts
                    )
                    new_meta[subfolder_key] = current_meta

                    if self.should_exit or self.suspend_flag: # Check after computing metadata
                        logging.info(f"scan_and_backup: Exiting or suspending after metadata computation for {root}.")
                        return

                    if not self.folder_needs_check(subfolder_key, current_meta, cached_meta):
                        continue

                    for f_in_dir_loop in files_in_dir: # Renamed 'f' to avoid conflict
                        if (exclude_hidden_master_switch and f_in_dir_loop.startswith('.')) or \
                           any(f_in_dir_loop.endswith(ext) for ext in self.excluded_exts):
                            continue
                        
                        if self.should_exit or self.suspend_flag: # Check inside file loop
                            logging.info(f"scan_and_backup: Exiting or suspending during file processing in {root}.")
                            return

                        fsrc_loop = os.path.join(root, f_in_dir_loop)
                        frel_loop = os.path.relpath(fsrc_loop, self.user_home)
                        main_path_loop = os.path.join(self.main_backup_dir, frel_loop)

                        if not os.path.exists(main_path_loop):
                            tasks.append(self.copy_file(fsrc_loop, main_path_loop, frel_loop))
                        elif self.file_was_updated(fsrc_loop, frel_loop):
                            session_backup_path_loop = os.path.join(session_backup_dir, frel_loop)
                            tasks.append(self.copy_file(fsrc_loop, session_backup_path_loop, frel_loop))

                self.save_folder_metadata(top_level_rel_path, new_meta)
            
            elif entry.is_file():
                if self.should_exit or self.suspend_flag: # Check before processing top-level file
                    logging.info(f"scan_and_backup: Exiting or suspending before processing top-level file {entry.name}.")
                    return

                # This is a top-level file in user_home
                fsrc = src_path 
                frel = top_level_rel_path # Relative path of the top-level file

                # Apply hidden/excluded extension checks for top-level files
                if (exclude_hidden_master_switch and entry.name.startswith('.')) or \
                   any(entry.name.endswith(ext) for ext in self.excluded_exts):
                    continue
                
                main_path = os.path.join(self.main_backup_dir, frel)

                if not os.path.exists(main_path):
                    tasks.append(self.copy_file(fsrc, main_path, frel))
                elif self.file_was_updated(fsrc, frel):
                    session_backup_path = os.path.join(session_backup_dir, frel)
                    tasks.append(self.copy_file(fsrc, session_backup_path, frel))

        if self.should_exit or self.suspend_flag: # Check before gathering tasks
            logging.info("scan_and_backup: Exiting or suspending before awaiting tasks.")
            return

        if tasks:
            await asyncio.gather(*tasks)
            # After tasks are gathered, check flags again before proceeding
            if self.should_exit or self.suspend_flag:
                logging.info("scan_and_backup: Exiting or suspending after awaiting tasks, before summary.")
                return
            
            server.update_recent_backup_information()
            
            # After backup tasks are complete, generate the summary
            try:
                summary_script_path = os.path.join(os.path.dirname(__file__), 'generate_backup_summary.py')
                process = sub.run(
                    ['python3', summary_script_path],
                    check=True,
                    capture_output=True, # Capture stdout and stderr
                    text=True # Decode stdout/stderr as text
                )
                # If successful, process.stdout will have the script's print statements/logs
                logging.info(f"generate_backup_summary.py stdout:\n{process.stdout}")
                send_to_ui(json.dumps({"type": "summary_updated"}))

            except sub.CalledProcessError as e: # This will be raised if check=True and script returns non-zero
                logging.warning(f"Failed to generate backup summary. Script: {summary_script_path}, Return code: {e.returncode}")
            except Exception as e: # Catch other potential errors like FileNotFoundError for the script itself
                logging.critical(f"Failed to generate backup summary (unexpected error): {e}", exc_info=True)
            logging.info("Backup session complete.")

            # After main backup and summary, backup downloaded packages
            if not (self.should_exit or self.suspend_flag):
                if server.DRIVER_LOCATION and self.is_backup_location_writable():
                    await self._backup_downloaded_packages()
        
        try:
            if os.path.exists(self.interruped_main_file):
                os.remove(self.interruped_main_file)
        except OSError as e:
            logging.critical(f"Could not remove interrupted_main_file {self.interruped_main_file}: {e}. "
                          "This may indicate a read-only filesystem.")
        
        # Cleanup empty incremental folders
        if os.path.exists(session_backup_dir): # Check if session_backup_dir was even created
            self._cleanup_empty_incremental_folders(session_backup_dir)

    ############################################################################
    # CLEANUP OF EMPTY INCREMENTAL FOLDERS
    ############################################################################
    def _cleanup_empty_incremental_folders(self, session_backup_dir: str):
        """
        Removes the session backup directory if it's empty.
        Also removes the parent date directory if it becomes empty as a result.
        """
        try:
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

    ############################################################################
    # DAEMON MAIN RUN LOOP
    ############################################################################
    async def run(self):
        self.loop = asyncio.get_running_loop() # Store the loop for threadsafe calls
        self.pid = str(os.getpid())
        pid_file_path = server.DAEMON_PID_LOCATION

        # Check for existing daemon and manage PID file
        if os.path.exists(pid_file_path):
            try:
                with open(pid_file_path, 'r') as pf:
                    existing_pid = int(pf.read().strip())
                if existing_pid != int(self.pid): # Check if it's not self (e.g. from a previous crash)
                    try:
                        os.kill(existing_pid, 0) # Check if process exists
                        logging.critical(f"Another daemon instance (PID {existing_pid}) appears to be running. Exiting.")
                        return # Exit the run method, daemon will stop
                    except OSError: # Process with existing_pid not running (stale PID file)
                        logging.warning(f"Stale PID file found for PID {existing_pid}. Removing it.")
                        os.remove(pid_file_path)
            except (ValueError, FileNotFoundError, OSError) as e: # Added OSError for os.remove
                logging.warning(f"Error processing existing PID file {pid_file_path}: {e}. Attempting to remove and continue.")
                try:
                    if os.path.exists(pid_file_path): os.remove(pid_file_path)
                except OSError:
                    pass # Ignore if removal fails, will try to write next

        # Create new PID file
        try:
            os.makedirs(os.path.dirname(pid_file_path), exist_ok=True)
            with open(pid_file_path, 'w') as pf:
                pf.write(self.pid)
            logging.info(f"Daemon (PID: {self.pid}) started. PID file: {pid_file_path}")
        except Exception as e:
            logging.critical(f"Failed to create PID file {pid_file_path}: {e}. Daemon cannot start.")
            return # Exit the run method, daemon will stop
        # await self.resume_from_interruption()
        shutdown_event = asyncio.Event()

        # Define signal handlers for use with signal.signal
        def stop_loop_for_termination(signum, frame): # For SIGTERM, SIGINT
            logging.debug(f"stop_loop_for_termination called for signal {signum}")
            self.signal_handler(signum, frame)
            shutdown_event.set()

        # Setup signal handlers
        signal.signal(signal.SIGTERM, stop_loop_for_termination)
        signal.signal(signal.SIGINT, stop_loop_for_termination)
        signal.signal(signal.SIGTSTP, self.signal_handler)  # Suspend (Ctrl+Z)
        signal.signal(signal.SIGCONT, self.resume_handler)  # Resume

        logging.info("Starting scan and backup...")

        while not self.should_exit:
            if self.suspend_flag:
                logging.info("Daemon suspended... sleeping.")
                await asyncio.sleep(5)
                continue

            # Check if the PID file created by this daemon instance was removed externally
            if not os.path.exists(pid_file_path):
                logging.warning(f"Daemon PID file {pid_file_path} was removed externally. Shutting down.")
                self.signal_handler(signal.SIGTERM, None) # This sets self.should_exit = True
                break

            if has_driver_connection():
                if self.is_backup_location_writable():
                    # Reset a flag indicating writability issue if it was set
                    self.had_writability_issue = False
                    await self.scan_and_backup()
                else:
                    # Log critical only if this is a new or persistent issue
                    logging.critical(f"[CRITICAL]: Backup location {server.create_base_folder()} is not writable. Automatic backups will be disabled by the UI if running.")
                    self.had_writability_issue = True # Set flag to avoid repeated critical logs for the same issue in one session
            else:
                logging.info("[CRITICAL]: Backup device is not connected. Skipping backup cycle.")
                self.had_writability_issue = False

            logging.debug(f"Waiting for {WAIT_TIME} minutes before next cycle.")
            total_wait = WAIT_TIME * 60
            interval = 1
            elapsed = 0
            
            while elapsed < total_wait and not self.should_exit:
                try:
                    await asyncio.wait_for(shutdown_event.wait(), timeout=interval)
                    break
                except asyncio.TimeoutError:
                    elapsed += interval
            
            if self.should_exit: # If already exiting due to a signal, break before config check
                logging.debug("Main loop: should_exit is true, breaking before auto_backup_enabled check.")
                break

            # Check if auto backup is still enabled
            auto_backup_enabled = server.get_database_value('BACKUP', 'automatically_backup')
            if str(auto_backup_enabled).lower() != 'true':
                logging.info("Automatic backup is disabled in configuration. Daemon will shut down.")
                self.signal_handler(signal.SIGTERM, None) # Trigger shutdown
                # self.should_exit will be true now, loop will terminate

        # Executor shutdown is handled in the main script's finally block
        # if self.executor:
        #    self.executor.shutdown(wait=True) 

################################################################################
# MAIN EXECUTION BLOCK
################################################################################
if __name__ == "__main__":
    # Print a message immediately upon starting, before any complex initialization.
    server = SERVER()

    # Ensure the directory for the log file exists, attempt to create if not.
    # This is important if DRIVER_LOCATION is initially unavailable.
    log_file_path = server.get_log_file_path()
    # This path should be determined before the daemon object 'daemon' is created or fails
    pid_file_path_for_cleanup = server.DAEMON_PID_LOCATION
    daemon_obj = None # Initialize to None
    current_process_pid = str(os.getpid()) # Get PID early
    # if os.path.exists(log_file_path): # Optional: remove old log on start
    #     os.remove(log_file_path)
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

        # Daemon removes its own PID file
        if os.path.exists(pid_file_path_for_cleanup):
            try:
                pid_in_file = ""
                with open(pid_file_path_for_cleanup, 'r') as f:
                    pid_in_file = f.read().strip()

                expected_pid = daemon_obj.pid if daemon_obj and hasattr(daemon_obj, 'pid') and daemon_obj.pid else current_process_pid

                if pid_in_file == expected_pid:
                    os.remove(pid_file_path_for_cleanup)
                    logging.info(f"Daemon (PID {expected_pid}) removed its PID file: {pid_file_path_for_cleanup}")
                else:
                    logging.warning(
                        f"PID file {pid_file_path_for_cleanup} contains PID {pid_in_file}, "
                        f"but expected PID {expected_pid}. Not removing file."
                    )
            except Exception as e_remove:
                logging.error(f"Error removing PID file {pid_file_path_for_cleanup} on daemon exit: {e_remove}")
        else:
            logging.info(f"PID file {pid_file_path_for_cleanup} not found during daemon shutdown.")

        # Executor shutdown
        if daemon_obj and hasattr(daemon_obj, 'executor') and daemon_obj.executor:
            logging.info("Shutting down executor pool...")
            daemon_obj.executor.shutdown(wait=True)
            logging.info("Executor pool shut down.")
