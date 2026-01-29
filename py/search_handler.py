from py.server import *
import re
import configparser

server = SERVER()
config = configparser.ConfigParser()


class SearchHandler:
    def __init__(self):
        server._create_default_config()

        ##########################################################################
        # VARIABLES
        ##########################################################################
        self.selected_file_path: bool = None
        # Don't set main_files_dir here - make it dynamic
        self.location_buttons: list = []
        
        # For search
        self.files: list = [] # Holds dicts of scanned files from .main_backup
        self.file_names_lower: list = [] # Lowercase basenames for searching
        self.file_search_display_paths_lower: list = [] # Lowercase relative paths for searching
        self.last_query: str = ""
        self.files_loaded: bool = False # Flag indicating if initial scan is complete
        self.pending_search_query: str = None # Stores search query if files aren't loaded yet
        
        # Cache system
        self._files_cache = None
        self._cache_time = 0
        self.CACHE_DURATION = 300  # 5 minutes
        
        self.thumbnail_cache = {} # For in-memory thumbnail caching
        self.ignored_folders = []
        self.page_size = 17  # Number of results per page
        self.current_page = 0  # Start from the first page
        self.search_results = []  # Store results based on filtering/searching
        self.date_combo = None  # To reference date combo in filtering
        self.search_timer = None  # Initialize in the class constructor
        self.folder_status_widgets = {} # To store icon widgets for top-level folders
        self.currently_scanning_top_level_folder_name = None # Track which top-level folder is scanning
        self.transfer_rows = {} # To track active transfers and their Gtk.ListBoxRow widgets
        self.search_spinner = None # Initialize search spinner
        self.starred_files_flowbox = None # For the "Starred Items" section
        self.starred_files = [] # Use a list to maintain order for starred files
        
        # Initialize with cached files if available
        self.scan_files_folder_threaded()

    @property
    def main_files_dir(self):
        """Dynamic property that always gets the current backup location"""
        app_main_backup_dir = server.app_main_backup_dir()
        return os.path.expanduser(app_main_backup_dir)

    def get_files(self):
        """Get cached files or scan if cache is expired"""
        current_time = time.time()
        if (self._files_cache is None or 
            current_time - self._cache_time > self.CACHE_DURATION):
            self._files_cache = self._scan_files()
            self._cache_time = current_time
            self.files_loaded = True
        return self._files_cache

    def _scan_files(self):
        """Scan files and return a list of file dictionaries."""
        current_main_files_dir = self.main_files_dir  # Use the dynamic property

        if not os.path.exists(current_main_files_dir):
            print(f"Documents path for scanning does not exist: {current_main_files_dir}")
            return []
        
        print("Caching files, Please Wait...")

        file_list = []
        # base_for_rel_path is the folder *containing* .main_backup, i.e., server.backup_folder_name()
        base_for_search_display_path = os.path.dirname(current_main_files_dir) 

        for root, dirs, files in os.walk(current_main_files_dir):
            # Optionally, add logic here to exclude hidden directories or specific directories
            # dirs[:] = [d for d in dirs if not d.startswith('.')] # Example: exclude hidden dirs
            for file_name in files:
                # Optionally, add logic here to exclude hidden files
                # if file_name.startswith('.'): continue # Example: exclude hidden files
                file_path = os.path.join(root, file_name)
                file_date = os.path.getmtime(file_path)
                search_display_path = os.path.relpath(file_path, base_for_search_display_path)
                file_list.append({
                    "name": file_name, 
                    "path": file_path, 
                    "date": file_date, 
                    "search_display_path": search_display_path
                })
        return file_list
    
    def browse_backup_folder(self, path):
        """Get files from the backup directory with version counts"""
        backup_base_path = self.main_files_dir
        
        # Build full path
        if path:
            full_path = os.path.join(backup_base_path, path.lstrip('/'))
        else:
            full_path = backup_base_path
        
        # Security check
        if not os.path.commonpath([full_path, backup_base_path]) == backup_base_path:
            raise Exception("Invalid path")
        
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            return {'items': [], 'message': 'Directory not found'}
        
        # List contents
        items = []
        try:
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                
                try:
                    is_dir = os.path.isdir(item_path)
                    size = 0
                    
                    if not is_dir:
                        size = os.path.getsize(item_path)
                    
                    # Get relative path for version counting
                    if path:
                        relative_path = os.path.join(path, item)
                    else:
                        relative_path = item
                    
                    # Get version count for files (not folders)
                    version_count = 0
                    if not is_dir:
                        version_count = self.get_file_version_count(relative_path)
                    
                    items.append({
                        'name': item,
                        'path': relative_path,
                        'type': 'folder' if is_dir else 'file',
                        'size': size,
                        'lastModified': os.path.getmtime(item_path) if os.path.exists(item_path) else 0,
                        'versionCount': version_count  # Add version count
                    })
                except (PermissionError, OSError):
                    continue
        except PermissionError:
            return {'items': [], 'message': 'Permission denied'}
        
        return {
            'items': items,
            'path': path or '/',
            'total': len(items),
            'backup_base': backup_base_path
        }

    def get_file_version_count(self, file_path):
        """Get the number of backup versions for a file"""
        try:
            # Get backups root
            config.read('config/config.conf')
            device_path = config.get('DEVICE_INFO', 'path', fallback='')
            if not device_path:
                return 0
            
            backups_root = os.path.join(device_path, 'timemachine', 'backups')
            if not os.path.exists(backups_root):
                return 0
            
            version_count = 0
            
            # Count versions in date/time folders
            try:
                date_pattern = re.compile(r'\d{2}-\d{2}-\d{4}')
                time_pattern = re.compile(r'\d{2}-\d{2}')
                
                for date_folder in os.listdir(backups_root):
                    date_path = os.path.join(backups_root, date_folder)
                    if not os.path.isdir(date_path) or not date_pattern.match(date_folder):
                        continue
                    
                    for time_folder in os.listdir(date_path):
                        time_path = os.path.join(date_path, time_folder)
                        if not os.path.isdir(time_path) or not time_pattern.match(time_folder):
                            continue
                        
                        target_path = os.path.join(time_path, file_path.lstrip('/'))
                        if os.path.exists(target_path):
                            version_count += 1
            
            except Exception as e:
                print(f"Error counting versions: {e}")
            
            return version_count
            
        except Exception as e:
            print(f"Error in get_file_version_count: {e}")
            return 0

    def update_backup_location(self):
        """Clear cache to force rescan of new location"""
        self.clear_cache()

    def perform_search(self, query: str):
        """Perform the search using cached files"""
        try:
            # Use cached files instead of scanning every time
            files_data = self.get_files()
            
            # Update the instance variables for backward compatibility
            self.files = files_data
            self.file_names_lower = [f["name"].lower() for f in files_data]
            self.file_search_display_paths_lower = [f["search_display_path"].lower().replace(os.sep, "/") for f in files_data]
            
            query = str(query).strip().lower()
            if not query:
                return []

            def search_backup_sources(query):
                matches = []
                for idx, name in enumerate(self.file_names_lower):
                    # Check against basename or the searchable display path
                    if query in name or query in self.file_search_display_paths_lower[idx]:
                        matches.append(self.files[idx])
                return matches[:self.page_size]

            results = search_backup_sources(query)
            
        except AttributeError as e:
            print(f"Critical Search Error (AttributeError): {e}. File attributes might be missing.")
            print("Attempting to re-initialize file scan and deferring search.")
            self.files_loaded = False
            self.pending_search_query = query
            self.scan_files_folder_threaded()
            results = []
        except Exception as e:
            print(f"Error during search: {e}")
            results = []

        print(f"Search completed. Found {len(results)} results for query: '{query}'")
        return results

    def scan_files_folder_threaded(self):
        """Scan files in background thread and update cache"""
        def scan():
            try:
                # Send proper JSON message
                # self._send_message_to_frontend("scanning", {"status": "started", "message": "Starting file scan..."})

                # Use the caching method
                files_data = self.get_files()
                
                # Update instance variables
                self.files = files_data
                self.file_names_lower = [f["name"].lower() for f in files_data]
                self.file_search_display_paths_lower = [f["search_display_path"].lower().replace(os.sep, "/") for f in files_data]
                self.files_loaded = True

                # Send proper JSON completion message
                print("Caching completed!")
                # self._send_message_to_frontend("scan_complete", {"status": "success", "message": "File caching completed", "file_count": len(files_data)})

            except Exception as e:
                print(f"Error during background file scanning: {e}")
                # Ensure a clean state on error
                self.files = []
                self.file_names_lower = []
                self.file_search_display_paths_lower = []
                self.files_loaded = False
                self._files_cache = None  # Clear cache on error
                
                # Send error message
                # self._send_message_to_frontend("scan_error", {"status": "error", "message": str(e)})

        threading.Thread(target=scan, daemon=True).start()

    def clear_cache(self):
        """Clear the file cache (useful when backup files change)"""
        self._files_cache = None
        self._cache_time = 0
        self.files_loaded = False

    ##########################################################################
    # SOCKET
    ##########################################################################
    def _send_message_to_frontend(self, message_type, data=None):
        """Send proper JSON messages to the frontend via UNIX socket"""
        try:
            # Create proper JSON message
            message_data = {
                "type": message_type,
                "data": data or {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Convert to JSON string
            json_message = json.dumps(message_data) + "\n"
            
            # Send via socket
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(2)  # Add timeout
            sock.connect(server.SOCKET_PATH)
            sock.sendall(json_message.encode("utf-8"))
            sock.close()
            
        except socket.timeout:
            logging.warning(f"Socket operation timed out for {server.SOCKET_PATH}.")
        except FileNotFoundError:
            logging.debug(f"Socket file not found at {server.SOCKET_PATH}. UI likely not running.")
        except ConnectionRefusedError:
            logging.debug(f"Connection refused at {server.SOCKET_PATH}. UI likely not running.")
        except Exception as e:
            logging.warning(f"Error communicating with UI via {server.SOCKET_PATH}: {e}")
    

if __name__ == "__main__":    
    pass
