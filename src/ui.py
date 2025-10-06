from server import *
from device_location import device_location
from has_driver_connection import has_driver_connection
from check_package_manager import check_package_manager #NOSONAR

server = SERVER()  # <-- Instantiate first!

class DeviceSelectionWindow(Adw.Window):
    __gsignals__ = {
        'device-selection-changed': (GObject.SignalFlags.RUN_FIRST, None, (bool,))
    }

    def __init__(self, transient_for, **kwargs):
        super().__init__(modal=True, transient_for=transient_for, **kwargs)
        self.set_title("Select Backup Device")
        self.set_default_size(400, 300)

        self.parent_backup_window = transient_for
        self.location_buttons = []

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_content(main_vbox)

        header = Adw.HeaderBar()
        main_vbox.append(header)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        main_vbox.append(scrolled_window)

        self.devices_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.devices_list_box.set_margin_top(12)
        self.devices_list_box.set_margin_bottom(12)
        self.devices_list_box.set_margin_start(12)
        self.devices_list_box.set_margin_end(12)
        scrolled_window.set_child(self.devices_list_box)

        self.select_button = Gtk.Button(label="Select")
        self.select_button.add_css_class("suggested-action")
        self.select_button.set_sensitive(False)
        self.select_button.connect("clicked", self.on_select_clicked)
        header.pack_end(self.select_button)

        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", lambda w: self.close())
        header.pack_start(cancel_button)

        self._populate_devices()
        self._auto_select_saved_device()
        
    def _populate_devices(self):
        # Clear old children
        while True:
            child = self.devices_list_box.get_first_child()
            if not child:
                break
            self.devices_list_box.remove(child)
        self.location_buttons.clear()

        dev_loc = device_location()
        if not dev_loc:
            label = Gtk.Label(label="No mountable devices found in /media or /run/media.", xalign=0)
            self.devices_list_box.append(label)
            return
            
        users_devices_location = os.path.join(dev_loc, server.USERNAME)

        if not os.path.exists(users_devices_location) or not os.listdir(users_devices_location):
            label = Gtk.Label(label=f"No devices found in {users_devices_location}.", xalign=0)
            self.devices_list_box.append(label)
            return

        for device_name in os.listdir(users_devices_location):
            device_path = os.path.join(users_devices_location, device_name)
            if os.path.isdir(device_path): # Ensure it's a directory
                check = Gtk.CheckButton(label=device_path)
                self.devices_list_box.append(check)
                self.location_buttons.append(check)
                check.connect("toggled", self._on_device_toggled, device_path)

        if not self.location_buttons:
            label = Gtk.Label(label="No backup devices found.", xalign=0)
            self.devices_list_box.append(label)

    def _on_device_toggled(self, toggled_button, device_path_for_button):
        is_active = toggled_button.get_active()
        if is_active:
            for btn in self.location_buttons:
                if btn != toggled_button:
                    btn.set_active(False)
        self.select_button.set_sensitive(is_active)

    def on_select_clicked(self, button):
        selected_path = None
        selected_device_name = None
        for btn in self.location_buttons:
            if btn.get_active():
                selected_path = btn.get_label()
                selected_device_name = os.path.basename(selected_path)
                break

        server.set_database_value('DRIVER', 'driver_location', selected_path or "")
        server.set_database_value('DRIVER', 'driver_name', selected_device_name or "")
        
        # Emit signal to notify parent window
        self.emit("device-selection-changed", bool(selected_path))
        self.close()

    def _auto_select_saved_device(self):
        saved_driver_location = server.get_database_value('DRIVER', 'driver_location')
        if saved_driver_location:
            for button in self.location_buttons:
                if button.get_label() == saved_driver_location:
                    button.set_active(True) # This will trigger _on_device_toggled
                    self.select_button.set_sensitive(True)
                    break

    def do_close_request(self):
        # Emit signal with False if window is closed without selection (e.g., Esc or Cancel)
        if not any(btn.get_active() for btn in self.location_buttons):
             self.emit("device-selection-changed", False)
        return Adw.Window.do_close_request(self)


class BackupWindow(Adw.ApplicationWindow):
    MAX_STARRED_FILES = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(1300, 800) # Adjusted width for the new panel
        self.set_title(server.APP_NAME)

        ##########################################################################
        # VARIABLES
        ##########################################################################
        self.selected_file_path: bool = None
        self.documents_path = os.path.expanduser(server.main_backup_folder())
        self.location_buttons: list = []
        # For search
        self.files: list = [] # Holds dicts of scanned files from .main_backup
        self.file_names_lower: list = [] # Lowercase basenames for searching
        self.file_search_display_paths_lower: list = [] # Lowercase relative paths for searching
        self.last_query: str = ""
        self.files_loaded: bool = False # Flag indicating if initial scan is complete
        self.pending_search_query: str = None # Stores search query if files aren't loaded yet
        self.scan_files_folder_threaded()
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

        # Spinner for center content loading/searching
        self.center_search_spinner = Gtk.Spinner()
        self.center_search_spinner.set_spinning(False)
        self.center_search_spinner.set_visible(True) # Spinner itself is visible, stack controls page
        self._load_starred_files_from_json() # Load starred files at startup, this method initializes self.starred_files

        # Get exclude hidden items setting from the server 
        self.exclude_hidden_itens: bool = server.get_database_value(
            section='EXCLUDE',
            option='exclude_hidden_itens')
        
        # Get stored driver_location and driver_name
        self.driver_location = server.get_database_value(
            section='DRIVER',
            option='driver_location')

        self.driver_name = server.get_database_value(
            section='DRIVER',
            option='driver_name')
        
        self.main_layout_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(self.main_layout_box)

        self._create_header_bar()
        self._create_left_sidebar()
        self._create_main_content()

        self._populate_suggested_files() # Add this call
        self._populate_starred_files() # Add this call for starred items
        self._set_initial_daemon_state_and_update_icon()
        # self.populate_latest_backups() # This will be handled by scan_files_folder_threaded completion
        # self.update_overview_cards_from_summary() # Load summary data for overview cards

        # Start the summary data loading in a separate thread
        threading.Thread(target=self._populate_summary_data, daemon=True).start()

        # Grab searchbar focus on startup
        self.search_entry.grab_focus()
        self._check_for_critical_log_errors() # Check for critical errors at startup

    def _create_header_bar(self):
        # Header Bar
        header = Adw.HeaderBar()
        self.main_layout_box.append(header)

        # --- HeaderBar Left Content ---
        add_device_button = Gtk.Button(icon_name="list-add-symbolic")
        add_device_button.set_tooltip_text("Manage Backup Devices")
        add_device_button.connect("clicked", self.on_devices_clicked)
        header.pack_start(add_device_button)

        # Settings Action
        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.on_settings_clicked)
        self.add_action(settings_action)

        # Search Entry - Moved to Header Bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search e.g: text.txt or Documents/text.txt")
        self.search_entry.set_hexpand(False) # The Clamp will handle expansion if needed
        self.search_entry.set_sensitive(has_driver_connection())
        self.search_entry.connect("search-changed", self.on_search_changed)

        # Wrap search entry in Adw.Clamp to control its maximum width
        search_clamp = Adw.Clamp()
        search_clamp.set_child(self.search_entry)
        search_clamp.set_size_request(850, 22) # Adjust this value as needed for desired min width
        search_clamp.set_maximum_size(500) # Adjust this value as needed for desired max width
        header.set_title_widget(search_clamp)

        # System Restore Action
        restore_action = Gio.SimpleAction.new("systemrestore", None)
        restore_action.connect("activate", self.on_restore_system_button_clicked)
        self.add_action(restore_action)
        # restore_action.set_enabled(False)
        # restore_action.set_enabled(has_driver_connection())

        # Logs Action
        logs_action = Gio.SimpleAction.new("logs", None)
        logs_action.connect("activate", self.show_backup_logs_dialog)
        self.add_action(logs_action)

        # About Action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_clicked)
        self.add_action(about_action)

        # --- HeaderBar Right Content (Main Menu) ---
        main_menu_button = Gtk.MenuButton(icon_name="open-menu-symbolic")
        main_menu_button.set_tooltip_text("Main Menu")
        header.pack_end(main_menu_button)

        main_popover_menu = Gtk.PopoverMenu()
        main_menu_button.set_popover(main_popover_menu)

        menu_model = Gio.Menu()

        # Logs
        logs_item = Gio.MenuItem.new(label="Logs", detailed_action="win.logs") #NOSONAR
        logs_icon = Gio.ThemedIcon.new("text-x-generic-symbolic") # Or "document-properties-symbolic"
        logs_item.set_icon(logs_icon)
        menu_model.append_item(logs_item)

        # Search Spinner (added before the menu button)
        self.search_spinner = Gtk.Spinner()
        self.search_spinner.set_spinning(False)
        self.search_spinner.set_visible(False)
        header.pack_end(self.search_spinner)

        # System Restore
        restore_item = Gio.MenuItem.new(label="System Restore", detailed_action="win.systemrestore")
        restore_icon = Gio.ThemedIcon.new("document-revert-symbolic") # Or "system-backup-symbolic"
        restore_item.set_icon(restore_icon)
        menu_model.append_item(restore_item)

        # Settings
        settings_item = Gio.MenuItem.new(label="Settings", detailed_action="win.settings")
        settings_icon = Gio.ThemedIcon.new("preferences-system-symbolic") # Or "emblem-system-symbolic"
        settings_item.set_icon(settings_icon)
        menu_model.append_item(settings_item)

        # About
        about_item = Gio.MenuItem.new(label="About", detailed_action="win.about")
        about_icon = Gio.ThemedIcon.new("help-about-symbolic")
        about_item.set_icon(about_icon)
        menu_model.append_item(about_item)

        main_popover_menu.set_menu_model(menu_model)
        main_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.main_content = main_content # Store as instance variable
        self.main_content.set_hexpand(True)
        main_content.set_vexpand(True)
        self.main_layout_box.append(main_content) # Add main_content below the HeaderBar.

    def _create_main_content(self):
        """Creates and populates the center panel."""
        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0) # Changed spacing to 0
        center_box.set_margin_top(0) # No top margin, header bar is separate
        center_box.set_margin_bottom(12)
        center_box.set_margin_start(6) # Margin from the new left sidebar
        center_box.set_margin_end(12)   # Margin from the right window edge
        center_box.set_hexpand(True)
        center_box.set_vexpand(True)
        center_box.set_css_classes(["center-panel"])
        center_box.set_name("center-box")

        # Create a Gtk.Stack for the main content and the spinner
        self.center_content_stack = Gtk.Stack()
        self.center_content_stack.set_transition_type(Gtk.StackTransitionType.NONE) # No animation for spinner
        center_box.append(self.center_content_stack)

        # Page 1: Actual content
        content_page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_page_box.set_vexpand(True)
        self.center_content_stack.add_named(content_page_box, "content_page")

        # Page 2: Spinner
        spinner_page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        spinner_page_box.set_hexpand(True)
        spinner_page_box.set_vexpand(True)
        spinner_page_box.set_halign(Gtk.Align.CENTER)
        spinner_page_box.set_valign(Gtk.Align.CENTER)
        
        # self.center_search_spinner is already initialized in __init__
        self.center_search_spinner.set_size_request(64, 64) # Make it a bit larger
        spinner_page_box.append(self.center_search_spinner)
        self.center_content_stack.add_named(spinner_page_box, "spinner_page")

        # Initially show the content page (or spinner if files are loading)
        # self.center_content_stack.set_visible_child_name("content_page") # scan_files_folder_threaded will manage this
        
        # --- Suggested Files Section ---
        suggested_files_title_label = Gtk.Label(xalign=0)
        suggested_files_title_label.set_text("Suggested Files")
        suggested_files_title_label.add_css_class("title-3")
        suggested_files_title_label.set_margin_top(12)
        suggested_files_title_label.set_margin_bottom(0)
        content_page_box.append(suggested_files_title_label)

        self.suggested_files_flowbox = Gtk.FlowBox()
        self.suggested_files_flowbox.set_valign(Gtk.Align.START)
        self.suggested_files_flowbox.set_max_children_per_line(5) # Adjust as needed
        self.suggested_files_flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.suggested_files_flowbox.set_margin_bottom(12) # Space before next section
        content_page_box.append(self.suggested_files_flowbox)

        # --- Starred Files Section ---
        starred_files_header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        starred_files_header_box.set_margin_top(0) # Margin from suggested files
        starred_files_header_box.set_margin_bottom(0)
        content_page_box.append(starred_files_header_box)

        starred_files_title_label = Gtk.Label(xalign=0)
        starred_files_title_label.set_text("Starred Files")
        starred_files_title_label.add_css_class("title-3")
        starred_files_title_label.set_hexpand(True) # Allow label to take space
        starred_files_header_box.append(starred_files_title_label)

        clear_starred_button = Gtk.Button(icon_name="edit-clear-all-symbolic")
        clear_starred_button.set_tooltip_text("Clear all starred files")
        clear_starred_button.add_css_class("flat")
        clear_starred_button.set_valign(Gtk.Align.CENTER)
        clear_starred_button.connect("clicked", self._on_clear_starred_files_clicked)
        starred_files_header_box.append(clear_starred_button)

        self.starred_files_flowbox = Gtk.FlowBox()
        self.starred_files_flowbox.set_valign(Gtk.Align.START)
        self.starred_files_flowbox.set_max_children_per_line(5) # Consistent with suggested files
        self.starred_files_flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.starred_files_flowbox.set_margin_bottom(12) # Space before latest backups
        content_page_box.append(self.starred_files_flowbox)

        # --- Latest Backups/Search Resulst Section ---
        self.top_center_label = Gtk.Label(xalign=0)
        self.top_center_label.add_css_class("title-3") # Ensure .title-3 is styled in your CSS
        self.top_center_label.set_margin_top(0) # Space will be from previous section's bottom margin
        self.top_center_label.set_margin_bottom(12) # Space between title and listbox
        content_page_box.append(self.top_center_label)

        # Header grid
        left_column_titles = Gtk.Grid()
        left_column_titles.set_margin_top(0)
        left_column_titles.set_column_spacing(42)
        left_column_titles.set_hexpand(True)

        # Icon header (empty)
        icon_header = Gtk.Label()
        icon_header.set_hexpand(False)
        icon_header.set_halign(Gtk.Align.START)
        #left_column_titles.attach(icon_header, 0, 0, 1, 1)

        # Name header
        name_header = Gtk.Label(label="Name")
        name_header.set_hexpand(True)
        name_header.set_halign(Gtk.Align.START)
        #left_column_titles.attach(name_header, 1, 0, 1, 1)

        # Size header
        size_header = Gtk.Label(label="Size" + " " * 4)  # Add padding for alignment
        size_header.set_hexpand(False)
        size_header.set_halign(Gtk.Align.START)
        #left_column_titles.attach(size_header, 2, 0, 1, 1)

        # Date header
        date_header = Gtk.Label(label="Date"  + " " * 18)  # Add padding for alignment
        date_header.set_hexpand(False)
        date_header.set_halign(Gtk.Align.START)
        left_column_titles.attach(date_header, 3, 0, 1, 1)
        #center_box.append(left_column_titles)

        # ScrolledWindow for the ListBox
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC) # Horizontal, Vertical

        # Listbox for search results
        self.listbox = Gtk.ListBox()
        self.listbox.add_css_class("overview-card")
        self.listbox.connect("row-selected", self.on_listbox_selection_changed)

        scrolled_window.set_child(self.listbox) # Add ListBox to ScrolledWindow
        content_page_box.append(scrolled_window) # Add ScrolledWindow to content_page_box
        self.main_content.append(center_box)

    def _show_center_spinner(self):
        if self.center_content_stack.get_visible_child_name() != "spinner_page":
            self.center_content_stack.set_visible_child_name("spinner_page")
        if not self.center_search_spinner.get_spinning():
            self.center_search_spinner.start()

    def _hide_center_spinner(self):
        if self.center_content_stack.get_visible_child_name() != "content_page":
            self.center_content_stack.set_visible_child_name("content_page")
        if self.center_search_spinner.get_spinning():
            self.center_search_spinner.stop()

    def _create_detail_row(self, name, icon_name, color_hex, count_str, size_str):
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, margin_top=8, margin_bottom=8)

        content_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6) # Main horizontal container for the row content
        content_hbox.set_margin_start(6) # Space from the left edge
        content_hbox.set_margin_end(12) # Space from the right edge
        content_hbox.set_hexpand(False) # Allow this to take available space
        content_hbox.set_valign(Gtk.Align.CENTER) # Center align vertically within the row

        # Icon with colored background
        icon_bg = Gtk.Box()
        # icon_bg.add_css_class("icon-bg") # General class for base styling
        # icon_bg.set_size_request(32, 32) # Ensure a consistent size for the bg
        icon_bg.set_valign(Gtk.Align.CENTER)
        
        # Adjust padding for detail row icons specifically if needed, or rely on .icon-bg
        # For example, if .icon-bg padding is too large:
        icon_bg.set_margin_start(6) # Custom padding
        icon_bg.set_margin_end(6) # Space between icon_bg and name_label
        icon_bg.set_margin_top(6)
        icon_bg.set_margin_bottom(6)

        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(16) # Smaller icon for rows
        icon_bg.append(icon)
        content_hbox.append(icon_bg)

        # Dynamic CSS for icon background color
        icon_bg_class_name = f"dyn-icon-bg-{color_hex.replace('#', '')}"
        icon_bg_css_rule = f""".{icon_bg_class_name} {{
            background-color: alpha({color_hex}, 0.15);
            border-radius: 6px; /* Slightly smaller radius for smaller icon */
            padding: 6px; /* Smaller padding for row icons */
        }}"""
        self._add_dynamic_css_rule(icon_bg_css_rule)
        icon_bg.add_css_class(icon_bg_class_name)
        
        # Vertical box for Name and Count
        name_and_count_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0) # No spacing for tight stacking
        name_and_count_vbox.set_valign(Gtk.Align.CENTER) # Align this vbox vertically with the icon
        name_and_count_vbox.set_hexpand(True) # Allow this to take available space

        name_label = Gtk.Label(label=name)
        name_label.set_xalign(0) # Align left
        name_and_count_vbox.append(name_label)

        count_label = Gtk.Label(label=count_str)
        count_label.add_css_class("dim-label")
        count_label.set_xalign(0) # Align left
        name_and_count_vbox.append(count_label)

        content_hbox.append(name_and_count_vbox)
        
        size_label = Gtk.Label(label=size_str)
        size_label.set_halign(Gtk.Align.END)
        # size_label.set_hexpand(True) # No longer needed as name_and_count_vbox expands
        size_label.set_valign(Gtk.Align.CENTER)
        content_hbox.append(size_label)
        box.append(content_hbox)
        row.set_child(box)
        row.set_activatable(False)
        return row

    def _create_left_sidebar(self):
        # Dynamic CSS provider for runtime styles (e.g., card accents, icon backgrounds)
        # This should be in your __init__ if not already present.
        if not hasattr(self, 'dynamic_css_provider'):
            self.dynamic_css_provider = Gtk.CssProvider()
            self._dynamic_rules_set = set() # To keep track of added rules and avoid duplicates
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                self.dynamic_css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        # Ensure the helper method for adding dynamic CSS rules exists
        if not hasattr(self, '_add_dynamic_css_rule'):
            self._add_dynamic_css_rule = self._default_add_dynamic_css_rule_impl
        
        left_sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6
        )
        left_sidebar.set_size_request(240, -1) # Slightly wider for device info
        left_sidebar.add_css_class("left-sidebar")
        left_sidebar.set_margin_top(12)
        left_sidebar.set_margin_bottom(12)
        left_sidebar.set_margin_start(12) # Margin from left window edge
        left_sidebar.set_margin_end(0)   # Small margin from center panel
        left_sidebar.set_vexpand(True) # Allow vertical expansion
        left_sidebar.set_hexpand(False) # Prevent vertical expansion
        left_sidebar.set_valign(Gtk.Align.FILL) # Fill available vertical space

        # Revealer for Scan Status
        self.scan_status_revealer = Gtk.Revealer()
        self.scan_status_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self.scan_status_revealer.set_transition_duration(300)
        # Revealer for Transfer Title
        self.transfer_title_revealer = Gtk.Revealer()
        self.transfer_title_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self.transfer_title_revealer.set_transition_duration(300)

        self.current_scan_status_label = Gtk.Label(label="Scanning...")
        self.current_scan_status_label.set_margin_top(6)
        self.current_scan_status_label.set_margin_bottom(6)
        self.current_scan_status_label.set_margin_start(6)
        self.current_scan_status_label.set_margin_end(6)
        self.current_scan_status_label.add_css_class("caption") # Make text smaller
        self.current_scan_status_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.current_scan_status_card = Adw.Clamp(child=self.current_scan_status_label) # Use Adw.Clamp or Gtk.Frame
        self.current_scan_status_card.set_hexpand(False)
        self.current_scan_status_card.set_maximum_size(200) # Adjust this value as needed
        self.current_scan_status_card.set_visible(True) # Card is always visible, revealer controls it
        self.scan_status_revealer.set_child(self.current_scan_status_card)
        self.current_scan_status_card.set_css_classes(["card"]) # Optional: for styling

        # --- Backup/Restore Queue Section (Card in Right Panel) ---
        self.queue_card_frame = Gtk.Frame()
        self.queue_card_frame.add_css_class("card") # Apply card styling
        self.queue_card_frame.set_margin_top(6) # Internal padding for the card
        self.queue_card_frame.set_margin_bottom(0)
        self.queue_card_frame.set_margin_start(0)
        self.queue_card_frame.set_margin_end(0)

        # Box
        queue_card_inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        queue_card_inner_box.set_margin_top(10) # Internal padding for the card
        queue_card_inner_box.set_margin_bottom(10)
        queue_card_inner_box.set_margin_start(10)
        queue_card_inner_box.set_margin_end(10)
        self.queue_card_frame.set_child(queue_card_inner_box) # Set inner_box as child of the frame

        # Title
        queue_section_title = Gtk.Label(label="Backup/Restore Queue")
        queue_section_title.set_hexpand(False)
        queue_section_title.set_xalign(0)
        queue_section_title.add_css_class("title-3") # Use a smaller title style
        queue_card_inner_box.append(queue_section_title) # Add title to card's inner box

        # Items listbox
        self.queue_listbox = Gtk.ListBox()
        self.queue_listbox.add_css_class("card")
        self.queue_listbox.set_vexpand(True) # Allow it to take available vertical space        
        self.queue_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.queue_listbox.set_margin_top(3) # No top margin, space will be from the header
        self.queue_listbox.set_margin_bottom(3)
        self.queue_listbox.set_margin_start(3)
        self.queue_listbox.set_margin_end(3)
        self.queue_listbox.set_hexpand(False)

        queue_scrolled_window = Gtk.ScrolledWindow()
        queue_scrolled_window.set_child(self.queue_listbox)
        queue_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) # Only vertical scrolling
        queue_scrolled_window.set_hexpand(False) # Prevent it from taking all horizontal space
        queue_scrolled_window.set_vexpand(False) # Child of revealer, so revealer handles expansion
        queue_scrolled_window.set_margin_top(0) # No top margin, space will be from the header
        queue_scrolled_window.set_visible(True) # Scrolled window is always visible, revealer controls it
        queue_scrolled_window.set_margin_bottom(0)
        queue_scrolled_window.set_margin_start(0)
        queue_scrolled_window.set_margin_end(0)
        queue_card_inner_box.append(queue_scrolled_window) # Add scrolled list to card's inner box
        
        self.current_scan_status_card.set_margin_bottom(0)

        # Transfer Section Title (initialized in __init__)
        queue_section_title.add_css_class("title-4")
        queue_section_title.set_xalign(0)
        queue_section_title.set_hexpand(False)
        queue_section_title.set_vexpand(False)
        queue_section_title.set_margin_top(0)
        queue_section_title.set_margin_bottom(0)
        queue_section_title.set_margin_start(0) # Align with the left sidebar
        queue_section_title.set_margin_end(0)
        queue_section_title.set_visible(True) # Label is always visible, revealer controls it

        # Transfer Scrolled Window (initialized in __init__)
        queue_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        queue_scrolled_window.set_min_content_height(200) # Example height
        queue_scrolled_window.set_hexpand(False)

        # Overall Usage
        self.usage_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6) # Main container for this section
        self.usage_box.set_margin_top(0) # No top margin, space will be from the header
        self.usage_box.set_margin_bottom(0)
        self.usage_box.set_margin_start(0) # No left margin, space will be from the left sidebar
        self.usage_box.set_margin_end(0)
        self.usage_box.set_hexpand(True) # Allow it to take available horizontal space
        self.usage_box.set_vexpand(False)
        self.usage_box.add_css_class("card") # Add a card class for styling
        
        # --- Get device usage info ---
        total_size_str = "N/A"
        used_size_str = "N/A"
        total_bytes = 0
        used_bytes = 0
        fraction = 0.0

        # Get the device usage info only if driver_location is set
        # and the path exists to avoid errors.
        if self.driver_location and os.path.exists(self.driver_location):
            try:
                total_bytes_val, used_bytes_val, _ = shutil.disk_usage(self.driver_location)
                total_bytes = total_bytes_val
                used_bytes = used_bytes_val
                if total_bytes > 0:
                    fraction = used_bytes / total_bytes
                
                total_size_str = server.get_user_device_size(self.driver_location, True)
                used_size_str = server.get_user_device_size(self.driver_location, False)
            except Exception as e:
                print(f"Error getting disk usage for right sidebar: {e}")
        # --- End get device usage info ---

        # Detailed breakdown
        self.details_list = Gtk.ListBox()
        self.details_list.set_margin_top(0) # Space above the details list
        self.details_list.set_margin_bottom(0) # Space below the details list
        self.details_list.set_margin_start(0)
        self.details_list.set_margin_end(0)
        self.details_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self.details_list.add_css_class("card")

        # # Define mappings for icons and colors
        # category_icons = {
        #     "Image": "image-x-generic-symbolic",
        #     "Video": "video-x-generic-symbolic",
        #     "Document": "x-office-document-symbolic",
        #     "Others": "application-x-addon-symbolic",
        #     # Add more categories and their icons as needed
        # }
        # default_icon = "dialog-question-symbolic"

        # category_colors = {
        #     "Image": "#EA4335",
        #     "Video": "#4285F4",
        #     "Document": "#34A853",
        #     "Others": "#FBBC04",
        #     # Add more categories and their colors as needed
        # }
        # default_color = "#9E9E9E"

        # items_from_summary = []
        # summary_file_path = server.get_summary_filename()

        # if os.path.exists(summary_file_path):
        #     try:
        #         with open(summary_file_path, 'r') as f:
        #             summary_data = json.load(f)
        #         if "categories" in summary_data:
        #             for category_info in summary_data["categories"]:
        #                 name = category_info.get("name", "Unknown")
        #                 items_from_summary.append({
        #                     "name": name,
        #                     "icon_name": category_icons.get(name, default_icon),
        #                     "color_hex": category_colors.get(name, default_color),
        #                     "count": f"{category_info.get('count', 0)} files",
        #                     "size": category_info.get("size_str", "0 B")
        #                 })
        #     except Exception as e:
        #         print(f"Error loading or parsing summary file {summary_file_path}: {e}")

        # if not items_from_summary: # Fallback or empty state
        #     self.details_list.append(self._create_detail_row("No summary data", default_icon, default_color, "0 files", "0 B"))
        # else:
        #     for item_data in items_from_summary:
        #         self.details_list.append(self._create_detail_row(item_data["name"], item_data["icon_name"], item_data["color_hex"], item_data["count"], item_data["size"]))

        # This widget will take up all the extra space
        spacer = Gtk.Box()
        spacer.set_vexpand(True)

        # Horizontal Box for Device Name and Status Icon
        device_name_and_status_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        # Margins from original device_name_label, applied to the HBox
        device_name_and_status_hbox.set_margin_top(6) # No top margin, space will be from the header
        device_name_and_status_hbox.set_margin_bottom(0) # Space before progress bar
        device_name_and_status_hbox.set_margin_start(12)
        device_name_and_status_hbox.set_margin_end(0) # Space on the right side

        # Status Icon
        self.status_icon = Gtk.Image()
        self.status_icon.set_pixel_size(16) # Consistent icon size
        self.status_icon.set_margin_top(6) # No top margin, space will be from the header
        self.status_icon.set_margin_bottom(6) # Space before progress bar
        self.status_icon.set_margin_start(12)
        self.status_icon.set_margin_end(12) # Space on the right side

        self.current_daemon_state = "idle" # Initial state, will be updated

        # Device Name Label
        self.device_name_label_text = self.driver_name if self.driver_name else "N/A" # Store initial text
        self.device_name_label = Gtk.Label(label=self.device_name_label_text)
        self.device_name_label.add_css_class("title-4") # Or "caption" or other appropriate style
        self.device_name_label.set_xalign(0) # Align text to the left within its allocation
        self.device_name_label.set_ellipsize(Pango.EllipsizeMode.END) # Add this line
        self.device_name_label.set_hexpand(True) # Allow label to take available space
        device_name_and_status_hbox.append(self.device_name_label)

        # Status Icon (already initialized in __init__)
        self.status_icon.set_valign(Gtk.Align.CENTER) # Vertically align with the device name
        device_name_and_status_hbox.append(self.status_icon)
        self.usage_box.append(device_name_and_status_hbox)

        # Progress bar first
        self.usage_progress_bar = Gtk.ProgressBar(fraction=fraction)
        self.usage_progress_bar.set_margin_top(0) # No top margin, space will be from the header
        self.usage_progress_bar.set_margin_bottom(0) # Space before progress bar
        self.usage_progress_bar.set_margin_start(12)
        self.usage_progress_bar.set_margin_end(12) # Space on the right side
        self.usage_box.append(self.usage_progress_bar)
        
        # Combined usage label
        self.combined_usage_label = Gtk.Label(label=f"{used_size_str} of {total_size_str}")
        self.combined_usage_label.add_css_class("caption") # Make text smaller
        self.combined_usage_label.set_xalign(0) # Align left
        self.combined_usage_label.set_margin_top(0) # No top margin, space will be from the header
        self.combined_usage_label.set_margin_bottom(6) # Space before progress bar
        self.combined_usage_label.set_margin_start(12)
        self.combined_usage_label.set_margin_end(12) # Space on the right side
        self.usage_box.append(self.combined_usage_label)
        
        left_sidebar.append(spacer)
        left_sidebar.append(self.details_list)
        left_sidebar.append(self.queue_card_frame)
        left_sidebar.append(self.scan_status_revealer) # Add revealer instead of card directly
        left_sidebar.append(self.usage_box)

        self.folder_scan_status_box = left_sidebar # Keep reference if needed elsewhere
        self.main_content.append(left_sidebar) # Add to the main horizontal box

    def _check_for_critical_log_errors(self):
        log_file_path = server.get_log_file_path()
        last_critical_message = None
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, 'r') as f:
                    for line in f:
                        if "[CRITICAL]" in line:
                            # Extract message part after "[CRITICAL] "
                            parts = line.split("[CRITICAL] ", 1)
                            if len(parts) > 1:
                                last_critical_message = parts[1].strip()
                            else: # Fallback if format is slightly off
                                last_critical_message = line.strip()
        except Exception as e:
            print(f"Error reading log file for critical errors: {e}")
            return

        if last_critical_message:
            print(f"CRITICAL ERROR DETECTED: {last_critical_message}")
            GLib.idle_add(self._show_critical_error_dialog, last_critical_message)
            GLib.idle_add(self._disable_auto_backup_due_to_critical_error)

    def _show_critical_error_dialog(self, critical_message_text):
        dialog = Adw.MessageDialog(
            transient_for=self,
            modal=True,
            title="Critical Error",
            heading="A critical error has occurred:",
            body=critical_message_text + "\n\nAutomatic backup has been disabled. Please resolve the issue and restart the application."
        )
        dialog.add_response("ok", "OK")
        dialog.add_response("problem-fixed", "Problem Fixed")
        dialog.set_response_appearance("problem-fixed", Adw.ResponseAppearance.DESTRUCTIVE) # Or .SUGGESTED
        dialog.set_default_response("ok")  # <-- Add this line
        dialog.set_close_response("ok")    # <-- Add this line

        def on_dialog_response(d, response_id):
            if response_id == "problem-fixed":
                if os.path.exists(server.get_log_file_path()):
                    os.remove(server.get_log_file_path())
            d.close()
        dialog.connect("response", on_dialog_response)
        dialog.present()

    def _disable_auto_backup_due_to_critical_error(self):
        print("Disabling automatic backup due to critical error.")
        server.set_database_value('BACKUP', 'automatically_backup', 'false')
        # The daemon should pick up this change and stop if it was running due to auto-backup.

    # Helper method to add dynamic CSS rules (should be part of BackupWindow class)
    # This is a default implementation if you don't have one.
    def _default_add_dynamic_css_rule_impl(self, rule_string):
        if rule_string not in self._dynamic_rules_set:
            self._dynamic_rules_set.add(rule_string)
            # GTK4 load_from_data expects bytes
            self.dynamic_css_provider.load_from_data("\n".join(self._dynamic_rules_set).encode('utf-8'))

    ##########################################################################
    # UI VISIBILITY
    ##########################################################################
    def _update_left_panel_visibility(self):
        # Check if folder scanning is active or has items
        has_file_transfers = bool(self.queue_listbox.get_first_child())

        self.transfer_title_revealer.set_reveal_child(has_file_transfers)
        # self.transfer_list_revealer.set_reveal_child(has_file_transfers)

    ##########################################################################
    # BACKUP
    ##########################################################################
    def on_devices_clicked(self, button):
        # Create and present the modal device selection window
        device_selection_win = DeviceSelectionWindow(transient_for=self, application=self.get_application())
        device_selection_win.present()

        # Connect to a custom signal to know when a device is selected or window closed
        device_selection_win.connect("device-selection-changed", self._on_device_selection_changed_from_modal)

    def _on_device_selection_changed_from_modal(self, modal_window, device_selected):
        self.driver_location = server.get_database_value(section='DRIVER', option='driver_location')
        self.driver_name = server.get_database_value(section='DRIVER', option='driver_name')

        # Update the server instance's in-memory understanding of the driver location and name
        # This is crucial because server methods like server.main_backup_folder()
        # use server.DRIVER_LOCATION and server.DRIVER_NAME directly.
        server.DRIVER_LOCATION = self.driver_location
        server.DRIVER_NAME = self.driver_name

        # Update path for file scanning, as it depends on the driver_location
        self.documents_path = os.path.expanduser(server.main_backup_folder())

        if os.path.exists(server.backup_folder_name()):
            self.search_entry.set_sensitive(bool(has_driver_connection()))

        GLib.idle_add(self._refresh_left_sidebar_summary_and_usage) # Refresh on device change
        GLib.idle_add(self._populate_suggested_files) # Refresh suggested files
        GLib.idle_add(self._populate_starred_files)   # Refresh starred files
        GLib.idle_add(self._set_initial_daemon_state_and_update_icon) # Refresh daemon state icon
        GLib.idle_add(self.populate_latest_backups) # Refresh latest backups
        GLib.idle_add(self._check_for_critical_log_errors) # Check for critical errors
        
        # Reset and restart file scanning for search functionality
        self.files_loaded = False
        self.files = []
        self.file_names_lower = []
        self.file_search_display_paths_lower = []
        self.search_results = [] # Clear previous search results
        GLib.idle_add(self.populate_results, []) # Clear the listbox UI of old results
        if has_driver_connection(): # Only scan if a device is connected and selected
            self.scan_files_folder_threaded()

        # Update daemon state based on new connection status
        self._set_initial_daemon_state_and_update_icon()
        
    def _set_initial_daemon_state_and_update_icon(self):
        if not has_driver_connection():
            self.current_daemon_state = "disconnected"
        elif os.path.exists(server.get_interrupted_main_file()):
            self.current_daemon_state = "interrupted"
        else:
            self.current_daemon_state = "idle"
        GLib.idle_add(self._update_status_icon_display)

    def _update_status_icon_display(self):
        icon_name = "dialog-information-symbolic" # Default: idle
        tooltip = "Daemon is idle. Monitoring for file changes and waiting for next backup cycle."
        daemon_is_actually_running = server.is_daemon_running()

        if self.current_daemon_state == "disconnected":
            # Check if at least the daemon is running
            if server.is_daemon_running():
                icon_name = "network-wired-acquiring-symbolic"
                tooltip = "Backup device not connected. but daemon is running."
            else:
                icon_name = "network-offline-symbolic"
                tooltip = "Backup device not connected."
        elif self.current_daemon_state == "interrupted":
            if daemon_is_actually_running:
                icon_name = "dialog-warning-symbolic"
                tooltip = "Interrupted backup pending. Daemon is running and will attempt to resume."
            else:
                icon_name = "error-symbolic" # Or a different icon indicating daemon is not running
                tooltip = "Interrupted backup pending, but the daemon is NOT running. Please start it manually or check settings."
        elif self.current_daemon_state == "scanning":
            icon_name = "view-refresh-symbolic" # Or "system-search-symbolic"
            tooltip = "Scanning files for backup..."
        elif self.current_daemon_state == "copying":
            icon_name = "emblem-synchronizing-symbolic" # Or "media-floppy-symbolic"
            tooltip = "Backing up files..."
        elif self.current_daemon_state == "restoring":
            icon_name = "document-revert-symbolic" # Icon for restoring
            tooltip = "Restoring files..."
        elif self.current_daemon_state == "idle":
            if daemon_is_actually_running:
                icon_name = "media-playback-start-symbolic" # Or "emblem-ok-symbolic" or "security-high-symbolic"
                tooltip = "Daemon is active and monitoring for file changes. Waiting for next backup cycle."
            else:
                icon_name = "media-playback-stop-symbolic" # Or "dialog-error-symbolic"
                tooltip = "Daemon is NOT running. Automatic backups are off or an error occurred."
        # "idle" uses the default icon_name and tooltip

        self.status_icon.set_from_icon_name(icon_name)
        self.status_icon.set_tooltip_text(tooltip)
        self.status_icon.set_visible(True)

    def on_listbox_selection_changed(self, listbox, row):
        if row:
            path: str = getattr(row, "device_path", None)
            self.selected_file_path = path
            self.selected_item_size = server.get_item_size(path, True)
        else:
            self.selected_file_path = None

    def populate_latest_backups(self):
        self.top_center_label.set_text("Backups Files")
        GLib.idle_add(self._hide_center_spinner) # Ensure spinner is hidden when populating this

        # Show latest backup files on startup
        latest_files = self.get_latest_backup_files()
        if latest_files:
            # If files were not loaded yet (e.g. initial state before scan completes)
            # this ensures the spinner is hidden and content page is shown.
            GLib.idle_add(self._hide_center_spinner)
            # Optionally, populate your listbox or UI with these files
            self.populate_results([{"name": os.path.basename(f), "path": f, "date": os.path.getmtime(f)} for f in latest_files])

    ##########################################################################
    # Socket reciever
    ##########################################################################
    def remove_socket(self):
        print("Removing socket file")
        # Remove old socket if it exists
        if os.path.exists(server.SOCKET_PATH):
            os.remove(server.SOCKET_PATH)

    def create_connect_socket(self):
        # Make sure the directory for the socket exists
        os.makedirs(os.path.dirname(server.SOCKET_PATH), exist_ok=True)

        # Remove socket file
        # self.remove_socket()

        # Create and bind the socket once
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.bind(server.SOCKET_PATH)
        server_socket.listen(5)
        print(f"Listening on UNIX socket {server.SOCKET_PATH}...")

        while True:
            conn, _ = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    # Handle multiple JSON objects in a single recv
                    # This is a simple implementation; a more robust one would buffer incomplete messages
                    messages = data.decode("utf-8").strip().split('\n')
                    for msg_str in messages:
                        if not msg_str: continue
                        self.process_daemon_message(msg_str)
                except Exception as e:
                    logging.error(f"Socket error processing message: {e}\nData: {data.decode('utf-8', errors='ignore')}")

    def process_daemon_message(self, message_string: str):
        """Processes a single JSON message string from the daemon."""
        try:
            msg = json.loads(message_string)
            file_id = msg.get("id")
            filename = msg.get("filename", "unknown")
            size = msg.get("size", "0 KB")
            eta = msg.get("eta", "n/a")
            progress = msg.get("progress", 0.0)
            
            current_state_before_message = self.current_daemon_state
            msg_type = msg.get("type")

            if msg_type == "scanning":
                folder_being_scanned = msg.get("folder")
                if folder_being_scanned:
                    self.current_daemon_state = "scanning"
                else:
                    if not self.transfer_rows:
                        self.current_daemon_state = "interrupted" if os.path.exists(server.get_interrupted_main_file()) else "idle"
                GLib.idle_add(self.update_scanning_folder_display, folder_being_scanned)
            elif msg_type == "transfer_progress":
                self.current_daemon_state = "copying"
                GLib.idle_add(self.update_or_create_transfer, file_id, filename, size, eta, progress, msg.get("error"))
                GLib.idle_add(self.update_scanning_folder_display, None)
            elif msg_type == "summary_updated":
                GLib.idle_add(self._refresh_left_sidebar_summary_and_usage)
                GLib.idle_add(self.update_scanning_folder_display, None)
                if not self.transfer_rows:
                    self.current_daemon_state = "interrupted" if os.path.exists(server.get_interrupted_main_file()) else "idle"
            elif msg_type == "daemon_stopping":
                self.current_daemon_state = "idle" # Visually, it's idle/stopped
            elif msg_type == "daemon_suspended":
                self.current_daemon_state = "suspended" # A new state
            elif msg_type == "daemon_resumed":
                self.current_daemon_state = "idle" # Or whatever state it should be in

            if current_state_before_message != self.current_daemon_state:
                GLib.idle_add(self._update_status_icon_display)

            GLib.idle_add(self._update_left_panel_visibility)
        except json.JSONDecodeError:
            logging.warning(f"Received non-JSON message from daemon: {message_string}")
        except Exception as e:
            logging.error(f"Error in process_daemon_message: {e}")

    def handle_client_old(self, conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    msg = json.loads(data.decode("utf-8").strip())
                    file_id = msg.get("id")  # must be unique per file (e.g., hash or relative path)
                    filename = msg.get("filename", "unknown")
                    size = msg.get("size", "0 KB")
                    eta = msg.get("eta", "n/a")
                    progress = msg.get("progress", 0.0)
                    
                    current_state_before_message = self.current_daemon_state
                    msg_type = msg.get("type")

                    if msg_type == "scanning":
                        folder_being_scanned = msg.get("folder") # Can be None
                        if folder_being_scanned:
                            self.current_daemon_state = "scanning"
                        else: # Scanning phase ended for this top-level folder or all
                            if not self.transfer_rows: # Check if any transfers are ongoing
                                if os.path.exists(server.get_interrupted_main_file()):
                                    self.current_daemon_state = "interrupted"
                                else:
                                    self.current_daemon_state = "idle"
                            # If transfers are active, state will become "copying" from transfer messages
                        GLib.idle_add(self.update_scanning_folder_display, folder_being_scanned)
                    elif msg_type == "transfer_progress": # Explicitly handle transfer progress
                        self.current_daemon_state = "copying"
                        GLib.idle_add(self.update_or_create_transfer, file_id, filename, size, eta, progress)
                        GLib.idle_add(self.update_or_create_transfer, file_id, filename, size, eta, progress, msg.get("error"))
                        # When transfers start, scanning of current top-level folder is done or all scans are done.
                        GLib.idle_add(self.update_scanning_folder_display, None) # Hide scanning card
                    elif msg_type == "summary_updated":
                        GLib.idle_add(self._refresh_left_sidebar_summary_and_usage)
                        GLib.idle_add(self.update_scanning_folder_display, None) # Ensure scanning display is cleared
                        # If no transfers are active, transition to idle or interrupted
                        if not self.transfer_rows:
                            if os.path.exists(server.get_interrupted_main_file()):
                                self.current_daemon_state = "interrupted" #NOSONAR
                            else:
                                self.current_daemon_state = "idle"
                    elif msg_type == "restoring_file":
                        # This message type is no longer handled here for UI-initiated restores
                        pass

                    if current_state_before_message != self.current_daemon_state:
                        GLib.idle_add(self._update_status_icon_display)

                    GLib.idle_add(self._update_left_panel_visibility)
                except Exception as e:
                    print("Socket error:", e)
                    
    def update_scanning_folder_display(self, folder_path_from_daemon): # Renaming parameter to match usage
        """Updates the folder scanning status display in the center panel."""
        if folder_path_from_daemon:
            # Extract the top-level folder name from the path
            parts = folder_path_from_daemon.split(os.sep)
            top_level_folder_name = parts[0] if parts else folder_path_from_daemon
            self.current_scan_status_label.set_text(f"Scanning: {top_level_folder_name}")
            self.scan_status_revealer.set_reveal_child(True)
            self.currently_scanning_top_level_folder_name = top_level_folder_name
        else:
            self.currently_scanning_top_level_folder_name = None
            self.scan_status_revealer.set_reveal_child(False)
        
        self._update_left_panel_visibility()


    def _populate_folder_status_list(self):
        """
        This method is now largely obsolete as the folder status listbox
        has been replaced by a single card showing the current scanning folder.
        It's kept for now in case some initial "waiting" state is desired,
        but for the current request, it does nothing.
        """
        if not has_driver_connection():
            # self.scan_status_revealer.set_reveal_child(False) # Or true with a message
            return
        # If no specific folder is scanning yet, the card remains hidden by default.
        self._update_left_panel_visibility()
    
    def update_or_create_transfer(self, file_id, filename, size, eta, progress):
        if file_id not in self.transfer_rows:
            content_widget = BackupProgressRow(file_id, filename, size, eta)
            
            revealer = Gtk.Revealer()
            revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
            revealer.set_transition_duration(250)
            revealer.set_child(content_widget)
            
            listbox_row = Gtk.ListBoxRow()
            listbox_row.set_child(revealer) # Add revealer to row
            
            self.transfer_rows[file_id] = listbox_row # Store the Gtk.ListBoxRow
            self.queue_listbox.append(listbox_row) # Add the Gtk.ListBoxRow
            revealer.set_reveal_child(True) # Animate in

        # Retrieve the Gtk.ListBoxRow
        listbox_row_to_update = self.transfer_rows.get(file_id)
        if not listbox_row_to_update:
            # This can happen if the row was removed due to progress >= 1.0
            # in a previous call, but a new update message arrives.
            return

        # Get revealer and then the content_widget (BackupProgressRow)
        revealer_to_update = listbox_row_to_update.get_child()
        if isinstance(revealer_to_update, Gtk.Revealer):
            content_widget_to_update = revealer_to_update.get_child()
            if isinstance(content_widget_to_update, BackupProgressRow): # Type check for safety
                content_widget_to_update.update(size, eta, progress)
 
        if progress >= 1.0: # If this item just completed
            if isinstance(revealer_to_update, Gtk.Revealer):
                revealer_to_update.set_reveal_child(False)
                duration = revealer_to_update.get_transition_duration()
                GLib.timeout_add(duration, self._remove_transfer_row_after_animation, listbox_row_to_update, file_id)

        self._update_left_panel_visibility()

        if progress >= 1.0 and not self.transfer_rows: # If this was the last transfer
            # Check if there are any pending removals due to animation
            pending_removal = False
            for row_id, lbox_row in self.transfer_rows.items():
                revealer = lbox_row.get_child()
                if isinstance(revealer, Gtk.Revealer) and revealer.get_reveal_child():
                    # This means a row is still visible or animating in, so not all transfers are "done" from UI perspective
                    pending_removal = True
                    break
            if pending_removal: return # Don't change state yet

            new_final_state = "idle"
            if os.path.exists(server.get_interrupted_main_file()):
                new_final_state = "interrupted"
            if self.current_daemon_state != new_final_state:
                self.current_daemon_state = new_final_state
                GLib.idle_add(self._update_status_icon_display) # Update icon
                GLib.idle_add(self.update_scanning_folder_display, None) # Also hide scanning card

    def _remove_transfer_row_after_animation(self, row, file_id):
        if row and row.get_parent() == self.queue_listbox:
            self.queue_listbox.remove(row)
        if file_id in self.transfer_rows:
            del self.transfer_rows[file_id]
        # Check if this was the last one for real now
        self._update_left_panel_visibility() # Update visibility based on remaining items
        return GLib.SOURCE_REMOVE

    def _refresh_left_sidebar_summary_and_usage(self):
        """Refreshes the backup summary details and device usage in the left sidebar."""
        # 1. Refresh Backup Summary Details (self.details_list)
        # Clear existing items from self.details_list
        child = self.details_list.get_first_child()
        while child:
            self.details_list.remove(child)
            child = self.details_list.get_first_child()

        # Define mappings for icons and colors (can be moved to a shared place or class constants if used elsewhere)
        category_icons = {
            "Image": "image-x-generic-symbolic", "Video": "video-x-generic-symbolic",
            "Document": "x-office-document-symbolic", "Others": "application-x-addon-symbolic",
        }
        default_icon = "dialog-question-symbolic"
        category_colors = {
            "Image": "#EA4335", "Video": "#4285F4", "Document": "#34A853", "Others": "#FBBC04",
        }
        default_color = "#9E9E9E"

        items_from_summary = []
        summary_file_path = server.get_summary_filename()
        if self.driver_location and os.path.exists(self.driver_location) and os.path.exists(summary_file_path):
            try:
                with open(summary_file_path, 'r') as f:
                    summary_data = json.load(f)
                if "categories" in summary_data:
                    for category_info in summary_data["categories"]:
                        name = category_info.get("name", "Unknown")
                        items_from_summary.append({
                            "name": name,
                            "icon_name": category_icons.get(name, default_icon),
                            "color_hex": category_colors.get(name, default_color),
                            "count": f"{category_info.get('count', 0)} files",
                            "size": category_info.get("size_str", "0 B")
                        })
            except Exception as e:
                print(f"Error loading or parsing summary file {summary_file_path} for refresh: {e}")

        # Re-use the _create_detail_row helper method
        if not items_from_summary:
            self.details_list.append(self._create_detail_row("No summary data", default_icon, default_color, "0 files", "0 B"))
        else:
            for item_data in items_from_summary:
                self.details_list.append(self._create_detail_row(item_data["name"], item_data["icon_name"], item_data["color_hex"], item_data["count"], item_data["size"]))

        # 2. Refresh Device Usage (within self.usage_box)
        self.device_name_label.set_text(self.driver_name if self.driver_name else "N/A")

        new_total_size_str = "N/A"
        new_used_size_str = "N/A"
        new_fraction = 0.0
        if self.driver_location and os.path.exists(self.driver_location):
            try:
                total_bytes, used_bytes, _ = shutil.disk_usage(self.driver_location)
                if total_bytes > 0:
                    new_fraction = used_bytes / total_bytes
                new_total_size_str = server.get_user_device_size(self.driver_location, True)
                new_used_size_str = server.get_user_device_size(self.driver_location, False)
            except Exception as e:
                print(f"Error getting disk usage for refresh: {e}")

        self.usage_progress_bar.set_fraction(new_fraction)
        self.combined_usage_label.set_text(f"{new_used_size_str} of {new_total_size_str}")
        # The status icon is updated by _update_status_icon_display based on self.current_daemon_state
                
    ##########################################################################
    # STARRED FILES - LOAD/SAVE
    ##########################################################################
    def _load_starred_files_from_json(self):
        starred_file_json_path = server.get_starred_files_location()
        if os.path.exists(starred_file_json_path):
            try:
                with open(starred_file_json_path, 'r') as f:
                    loaded_list = json.load(f)
                    if isinstance(loaded_list, list):
                        # If more than MAX_STARRED_FILES, keep only the most recent ones
                        self.starred_files = loaded_list[-self.MAX_STARRED_FILES:]
                    else:
                        print(f"Warning: Starred files JSON content is not a list. Initializing as empty.")
                        self.starred_files = []
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error loading starred files from {starred_file_json_path}: {e}. Initializing as empty set.")
                self.starred_files = []
            except Exception as e:
                print(f"Unexpected error loading starred files from {starred_file_json_path}: {e}. Initializing as empty list.")
                self.starred_files = []
        else:
            self.starred_files = []

    def _on_clear_starred_files_clicked(self, button):
        """Clears all starred files and updates the UI."""
        if not self.starred_files: # Nothing to clear
            return

        self.starred_files.clear()
        starred_file_json_path = server.get_starred_files_location()
        if os.path.exists(starred_file_json_path):
            try:
                os.remove(starred_file_json_path)
                print("Cleared starred files JSON.")
            except OSError as e:
                print(f"Error removing starred files JSON {starred_file_json_path}: {e}")
        GLib.idle_add(self._populate_starred_files)

        # Also, reset star icons in the current search results list
        current_row = self.listbox.get_first_child()
        while current_row:
            # The Gtk.ListBoxRow's child is the Gtk.Revealer, whose child is the Gtk.Grid
            revealer = current_row.get_child()
            if isinstance(revealer, Gtk.Revealer):
                grid = revealer.get_child()
                if isinstance(grid, Gtk.Grid):
                    star_button = grid.get_child_at(3, 0) # Assuming star button is at col 3, row 0
                    if isinstance(star_button, Gtk.Button) and hasattr(star_button, "file_path"):
                        star_button.set_icon_name("non-starred-symbolic")
                        star_button.set_tooltip_text("Star this item")
            current_row = current_row.get_next_sibling()

    def _get_main_backup_equivalent_path(self, file_path_clicked):
        """
        Returns the path equivalent in the .main_backup folder.
        Based on current UI logic, file_path_clicked should already be
        a path within server.main_backup_folder() when this is called
        because the star button is only enabled for such files.
        This method includes fallback logic for robustness if that precondition changes.
        """
        main_backup_abs = os.path.abspath(server.main_backup_folder())
        file_path_abs = os.path.abspath(file_path_clicked)

        if file_path_abs.startswith(main_backup_abs):
            return file_path_clicked # Already the main backup path

        # Fallback: Attempt to convert if it's an incremental backup path
        logging.debug(
            f"_get_main_backup_equivalent_path called with an unexpected path: {file_path_clicked}. "
            f"Attempting to convert to main backup equivalent."
        )
        backup_root_abs = os.path.abspath(server.backup_folder_name())
        if file_path_abs.startswith(backup_root_abs):
            # Path is like /path/to/driver/timemachine/backups/DATE/TIME/rel/path/to/file
            relative_to_backup_root = os.path.relpath(file_path_abs, backup_root_abs)
            parts = relative_to_backup_root.split(os.sep)
            if len(parts) > 2: # Must have DATE, TIME, and then the actual relative path
                actual_relative_path = os.path.join(*parts[2:])
                return os.path.join(main_backup_abs, actual_relative_path)
            else:
                logging.error(f"  Path {file_path_clicked} looks incremental but structure is unexpected. Returning original.")
        return file_path_clicked # Fallback if conversion is not possible
    
    ##########################################################################
    # POPULATE SUMMARY DATA
    ##########################################################################
    def _populate_summary_data(self):
        """
        Loads the summary data from the JSON file and updates the UI.
        This is called on startup to ensure the latest summary is displayed.
        """
        items_from_summary = []
        summary_file_path = server.get_summary_filename()
        # Define mappings for icons and colors
        category_icons = {
            "Image": "image-x-generic-symbolic",
            "Video": "video-x-generic-symbolic",
            "Document": "x-office-document-symbolic",
            "Others": "application-x-addon-symbolic",
            # Add more categories and their icons as needed
        }
        default_icon = "dialog-question-symbolic"

        category_colors = {
            "Image": "#EA4335",
            "Video": "#4285F4",
            "Document": "#34A853",
            "Others": "#FBBC04",
            # Add more categories and their colors as needed
        }
        default_color = "#9E9E9E"

        if os.path.exists(summary_file_path):
            try:
                with open(summary_file_path, 'r') as f:
                    summary_data = json.load(f)
                if "categories" in summary_data:
                    for category_info in summary_data["categories"]:
                        name = category_info.get("name", "Unknown")
                        items_from_summary.append({
                            "name": name,
                            "icon_name": category_icons.get(name, default_icon),
                            "color_hex": category_colors.get(name, default_color),
                            "count": f"{category_info.get('count', 0)} files",
                            "size": category_info.get("size_str", "0 B")
                        })
            except Exception as e:
                print(f"Error loading or parsing summary file {summary_file_path}: {e}")

        if not items_from_summary: # Fallback or empty state
            self.details_list.append(self._create_detail_row("No summary data", default_icon, default_color, "0 files", "0 B"))
        else:
            for item_data in items_from_summary:
                self.details_list.append(self._create_detail_row(item_data["name"], item_data["icon_name"], item_data["color_hex"], item_data["count"], item_data["size"]))

    ##########################################################################
    # SUGGESTED FILES
    ##########################################################################
    def _populate_suggested_files(self):
        # Clear previous suggestions from the flowbox
        child = self.suggested_files_flowbox.get_child_at_index(0)
        while child:
            self.suggested_files_flowbox.remove(child)
            child = self.suggested_files_flowbox.get_child_at_index(0)

        summary_file_path = server.get_summary_filename()
        added_basenames = set()
        suggested_items_to_display = [] # Store dicts: {"basename": str, "thumbnail_path": str, "original_path": str}
        MAX_SUGGESTIONS_PER_SOURCE = 5

        # 1. Populate from "most_frequent_backups" (if connection and summary exist)
        # Order of preference for suggestions:
        # a) Most frequent in last 5 days
        # b) Overall most frequent
        # c) System recent files

        if has_driver_connection() and os.path.exists(summary_file_path):
            try:
                with open(summary_file_path, 'r') as f:
                    summary_data = json.load(f)

                # a) Most frequent in last 5 days
                most_frequent_recent = summary_data.get("most_frequent_recent_backups", [])
                for item in most_frequent_recent[:MAX_SUGGESTIONS_PER_SOURCE]:
                    rel_path = item.get("path")
                    if not rel_path:
                        continue
                    basename = os.path.basename(rel_path)
                    if basename not in added_basenames:
                        thumbnail_path = os.path.join(server.main_backup_folder(), rel_path)
                        original_path = os.path.join(server.USER_HOME, rel_path)
                        suggested_items_to_display.append({"basename": basename, "thumbnail_path": thumbnail_path, "original_path": original_path, "source": "freq_recent"})
                        added_basenames.add(basename)
                        
                # b) Overall most frequent (if still need more suggestions)
                most_frequent_overall = summary_data.get("most_frequent_backups", [])
                overall_freq_added_count = 0
                for item in most_frequent_overall:
                    if len(suggested_items_to_display) >= MAX_SUGGESTIONS_PER_SOURCE * 2: break # Overall limit
                    if overall_freq_added_count >= MAX_SUGGESTIONS_PER_SOURCE: break

                    rel_path = item.get("path")
                    if not rel_path:
                        continue
                    basename = os.path.basename(rel_path)
                    if basename not in added_basenames:
                        thumbnail_path = os.path.join(server.main_backup_folder(), rel_path)
                        original_path = os.path.join(server.USER_HOME, rel_path) # Path in user's system
                        suggested_items_to_display.append({
                            "basename": basename,
                            "thumbnail_path": thumbnail_path,
                            "original_path": original_path,
                            "source": "freq_overall"
                        })
                        added_basenames.add(basename)
                        overall_freq_added_count +=1
            except Exception as e:
                print(f"Error loading or parsing summary file {summary_file_path}: {e}")

        # 3. Populate FlowBox
        if not suggested_items_to_display:
            self.suggested_files_flowbox.set_visible(False)
            return

        self.suggested_files_flowbox.set_visible(True)

        for item_data in suggested_items_to_display:
            basename = item_data["basename"]
            thumbnail_path = item_data["thumbnail_path"]
            original_path = item_data["original_path"]

            button_content = Adw.ButtonContent()
            # pixbuf = self._generate_thumbnail_pixbuf(thumbnail_path, size_px=48)
            # if pixbuf:
            #     try:
            #         button_content.set_paintable(Gdk.Texture.new_for_pixbuf(pixbuf))
            #     except Exception as e:
            #         pass
            # else:
            
            button_content.set_icon_name("text-x-generic-symbolic") # Fallback icon
            button_content.set_label(basename)

            btn = Gtk.Button(child=button_content, has_frame=True)
            btn.add_css_class("suggested-file-card") # For custom styling
            # Pass basename for search and original_path for potential future context
            btn.connect("clicked", self.on_suggested_file_clicked, basename, original_path)
            self.suggested_files_flowbox.append(btn)

    def on_suggested_file_clicked(self, button, basename_to_search, original_file_path):
        # original_file_path is the absolute path to the file on the user's system.
        # It can be used for context, e.g., if you wanted to add an "Open Original" option.
        # print(f"Suggested file clicked: {basename_to_search} (Original: {original_file_path})")

        # Determine the search term to use.
        # If the original_file_path is within the user's home directory,
        # use the path relative to home. Otherwise, fall back to the basename.
        if original_file_path and original_file_path.startswith(server.USER_HOME):
            search_term = os.path.relpath(original_file_path, server.USER_HOME)
        else:
            search_term = basename_to_search # Fallback to basename if path is unexpected

        self.search_entry.set_text(search_term)

        # Trigger the search logic directly.
        # The on_search_changed method has a timer, so calling perform_search directly is better here.
        query = search_term.strip().lower()
        threading.Thread(target=self.perform_search, args=(query,), daemon=True).start()

    def _populate_starred_files(self):
        button_content = Adw.ButtonContent()

        # Clear previous starred items from the flowbox
        child = self.starred_files_flowbox.get_child_at_index(0)
        while child:
            self.starred_files_flowbox.remove(child)
            child = self.starred_files_flowbox.get_child_at_index(0)

        if not self.starred_files:
            self.starred_files_flowbox.set_visible(False)
            # Optionally hide the "Starred Items" title label if you have a reference to it
            return

        self.starred_files_flowbox.set_visible(True)

        for starred_file_path in self.starred_files:
            if not os.path.exists(starred_file_path): # Check if file still exists in backup
                print(f"Starred file {starred_file_path} no longer exists in backup. Skipping.")
                # Optionally, you might want to remove it from self.starred_files here
                # self.starred_files.remove(starred_file_path) # Be careful with modifying during iteration
                continue

            basename = os.path.basename(starred_file_path)
            # For starred items, the "thumbnail_path" is the starred_file_path itself
            # The "original_path" for search context:
            original_path_for_search = ""
            if starred_file_path.startswith(server.main_backup_folder()):
                rel_path = os.path.relpath(starred_file_path, server.main_backup_folder())
                original_path_for_search = os.path.join(server.USER_HOME, rel_path)
            else: # For incremental, it's harder to map back to a simple original_path for search.
                  # We can use the basename or the full backup path for search context.
                original_path_for_search = starred_file_path # Or just basename

            # placeholder icon first
            pixbuf = self._generate_thumbnail_pixbuf(starred_file_path, size_px=48)
            ext = os.path.splitext(starred_file_path)[1].lower()
            if pixbuf:
                try:
                    button_content.set_paintable(Gdk.Texture.new_for_pixbuf(pixbuf))
                except AttributeError:
                    button_content.set_icon_name("image-x-generic-symbolic") # Fallback icon
            else:
                button_content.set_icon_name("text-x-generic-symbolic") # Fallback icon

            # if pixbuf:
            #     button_content.set_paintable(Gdk.Texture.new_for_pixbuf(pixbuf))
            # else:
            #     if ext in server.VIDEO_EXTENSIONS:
            #         button_content.set_icon_name("video-x-generic-symbolic")
            #     elif ext in server.IMAGE_EXTENSIONS:
            #         button_content.set_icon_name("image-x-generic-symbolic")
            #     else:
            #         button_content.set_icon_name("text-x-generic-symbolic")

            button_content.set_label(basename)

            btn = Gtk.Button(child=button_content, has_frame=True)
            btn.add_css_class("suggested-file-card") # Reuse styling
            btn.connect("clicked", self.on_suggested_file_clicked, basename, original_path_for_search)
            self.starred_files_flowbox.append(btn)

    ##########################################################################
    # Backup
    ##########################################################################
    def get_latest_backup_files(self):
        base_backup_folder = server.main_backup_folder()
        backup_root = server.backup_folder_name()

        if not os.path.exists(backup_root):
            return []
        
        # List all date folders
        date_folders = [folder for folder in os.listdir(backup_root)
                            if os.path.isdir(os.path.join(backup_root, folder))]
        base_folder_name = os.path.basename(base_backup_folder)
        if base_folder_name in date_folders:
            date_folders.remove(base_folder_name)
            date_folders.sort(
                key=lambda folder: datetime.strptime(folder, "%d-%m-%Y"),
                reverse=True
            )
        if not date_folders:
            return []

        # Get latest date folder
        latest_date = date_folders[0]  # e.g.: 01-01-20
        latest_date_path = os.path.join(backup_root, latest_date)

        # Find the latest time folder inside the latest date
        time_folders = [
            t for t in os.listdir(latest_date_path)
            if os.path.isdir(os.path.join(latest_date_path, t))
        ]

        if not time_folders:
            return []

        try:
            time_folders.sort(key=lambda t: datetime.strptime(t, "%H-%M"), reverse=True)
        except Exception:
            time_folders.sort(reverse=True)

        # Get latest time folder
        latest_time = time_folders[0]
        latest_backup_path = os.path.join(latest_date_path, latest_time)

        # List all files in the latest backup folder
        backup_files = []
        for root, dirs, files in os.walk(latest_backup_path):
            for file in files:
                backup_files.append(os.path.join(root, file))
        return backup_files

    def open_modal_preview_window(self, filepath):
        if not filepath or not os.path.exists(filepath):
            dialog = Adw.MessageDialog(transient_for=self, modal=True,
                                       title="Preview Error",
                                       body="File not found or path is invalid.")
            dialog.add_response("ok", "OK")
            dialog.connect("response", lambda d, r: d.close())
            dialog.present()
            return

        preview_widget = None
        ext = os.path.splitext(filepath)[1].lower()
        mime, _ = mimetypes.guess_type(filepath)
        if mime is None: mime = ""

        if (ext in server.TEXT_EXTENSIONS or mime.startswith("text")): #NOSONAR
            preview_widget = self._create_text_preview_widget(filepath)
        elif (ext in server.IMAGE_EXTENSIONS or mime.startswith("image")):
            preview_widget = self._create_image_preview_widget(filepath)

        # Create Modal Window
        modal_preview_win = Adw.Window(transient_for=self, modal=True)
        modal_preview_win.set_title(f"Preview: {os.path.basename(filepath)}")
        modal_preview_win.set_default_size(700, 600)
        modal_preview_win.set_destroy_with_parent(True)

        # Create a main vertical box for the modal window's content
        modal_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        header = Adw.HeaderBar()
        modal_main_box.append(header) # Add header to the main box

        # Scrolled window for the preview content
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        modal_main_box.append(scrolled_window) # Add scrolled_window to the main box

        if preview_widget:
            scrolled_window.set_child(preview_widget)
        else:
            label = Gtk.Label(label="No preview available for this file type or an error occurred.")
            label.set_wrap(True)
            label.set_xalign(0.5)
            label.set_valign(Gtk.Align.CENTER)
            scrolled_window.set_child(label)

        modal_preview_win.set_content(modal_main_box) # Set the main box as the window's content
        modal_preview_win.present()

    def _create_text_preview_widget(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read(16384) # Read up to 16KB for preview
            textview = Gtk.TextView()
            textview.set_editable(False)
            textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            textview.get_buffer().set_text(text)
            textview.set_vexpand(True) 
            textview.set_hexpand(True)
            return textview
        except Exception as e:
            print(f"Failed to create text preview widget for {filepath}: {e}")
            return None

    def _create_image_preview_widget(self, filepath):
        try:
            picture = Gtk.Picture.new_for_filename(filepath)
            picture.set_content_fit(Gtk.ContentFit.CONTAIN) 
            picture.set_vexpand(True) 
            picture.set_hexpand(True)
            return picture
        except Exception as e:
            print(f"Failed to create image preview widget for {filepath}: {e}")
            return None

            ##########################################################################
            # SEARCH ENTRY
            ##########################################################################
            # Scale to fit preview area (e.g., max width 200px, adjust as needed)
            # This is a simple scaling, more sophisticated logic might be needed
            preview_width = self.preview_scrolled_window.get_allocated_width() - 20 # Account for padding
            if preview_width <= 0: preview_width = 300 # Fallback

            scale = preview_width / width if width > 0 else 1.0
            surf_width = int(width * scale)
            surf_height = int(height * scale)
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf_width, surf_height)
            cr = cairo.Context(surface)
            cr.save() # Save context
            cr.set_source_rgb(1, 1, 1)  # White background
            cr.paint()
            cr.restore() # Restore context
            cr.scale(scale, scale)
            page.render(cr)
            surface.flush()
            pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, surf_width, surf_height)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            image.set_vexpand(False) # Don't let image itself expand beyond its size
            image.set_hexpand(False)
            self.preview_scrolled_window.set_child(image)
            self.current_preview_widget = image
            return True # Indicate success
        except Exception as e:
            print(f"Failed to load PDF preview for {filepath}: {e}")
            self.show_no_preview(f"Error loading PDF: {e}")
            return False # Indicate failure

    def show_text_preview(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read(8192) # Read up to 8KB for preview
            textview = Gtk.TextView()
            textview.set_editable(False)
            textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            textview.get_buffer().set_text(text)
            textview.set_vexpand(True) # TextView should expand
            textview.set_hexpand(True)
            self.preview_scrolled_window.set_child(textview)
            self.current_preview_widget = textview
            return True # Indicate success
        except Exception as e:
            print(f"Failed to load text preview for {filepath}: {e}")
            self.show_no_preview(f"Error loading text: {e}")
            return False # Indicate failure

    def show_image_preview(self, filepath):
        try:
            picture = Gtk.Picture.new_for_filename(filepath)
            picture.set_content_fit(Gtk.ContentFit.CONTAIN) # Scale down to fit, preserve aspect ratio
            picture.set_vexpand(True) # Picture should expand within scrolled window
            picture.set_hexpand(True)
            self.preview_scrolled_window.set_child(picture)
            self.current_preview_widget = picture
            return True # Indicate success
        except Exception as e:
            print(f"Failed to load image preview for {filepath}: {e}")
            self.show_no_preview(f"Error loading image: {e}")
            return False # Indicate failure

    def show_no_preview(self, message="No preview available."):
        self.clear_preview()
        label = Gtk.Label(label=message)
        label.set_wrap(True)
        label.set_xalign(0.5)
        label.set_valign(Gtk.Align.CENTER)
        # label.set_vexpand(True) # The label itself doesn't need to vexpand
        self.preview_scrolled_window.set_child(label)
        self.current_preview_widget = label
        self.preview_scrolled_window.set_vexpand(False) # Collapse
        self.preview_scrolled_window.set_visible(False) # Hide
        if self.close_preview_button:
            self.close_preview_button.set_visible(False) # Hide close button
        if self.info_box.get_parent() == self.main_content: # If info_box is currently shown
            self.main_content.remove(self.info_box) # Remove it
    
    ##########################################################################
    # SEARCH ENTRY
    ##########################################################################
    def scan_files_folder_threaded(self):
        # Show spinner *before* starting the thread if files are not loaded
        if not self.files_loaded:
            GLib.idle_add(self._show_center_spinner)

        def scan():
            try:
                self.files = self.scan_files_folder()
                # These attributes must be set *before* files_loaded is True
                self.file_names_lower = [f["name"].lower() for f in self.files]
                self.file_search_display_paths_lower = [f["search_display_path"].lower().replace(os.sep, "/") for f in self.files]
                self.files_loaded = True  # Mark files as loaded only after successful initialization
            except Exception as e:
                print(f"Error during background file scanning: {e}")
                # Ensure a clean state on error
                self.files = []
                self.file_names_lower = []
                self.file_search_display_paths_lower = []
                self.files_loaded = False # Crucial: mark as not loaded
                GLib.idle_add(self._hide_center_spinner) # Hide spinner on error
                return # Stop further processing in this thread if scanning failed

            # If scan was successful and files are loaded, process any pending/last search
            hide_spinner_after_scan = True
            if self.pending_search_query is not None:
                GLib.idle_add(self.perform_search, self.pending_search_query)
                self.pending_search_query = None
                hide_spinner_after_scan = False # perform_search will hide it
            elif self.last_query:
                GLib.idle_add(self.perform_search, self.last_query)
                hide_spinner_after_scan = False # perform_search will hide it
            else: # No search query, populate with latest backups as default
                GLib.idle_add(self.populate_latest_backups)
                # populate_latest_backups itself calls _hide_center_spinner if it populates results
                # but to be safe, ensure it's hidden if it doesn't populate anything.
                # However, populate_latest_backups calls populate_results which will hide it.

            if hide_spinner_after_scan: # If no search took over, hide the initial scanning spinner
                GLib.idle_add(self._hide_center_spinner)

        threading.Thread(target=scan, daemon=True).start()
        
    def scan_files_folder(self):
        """Scan files and return a list of file dictionaries."""
        if not os.path.exists(self.documents_path):
            # print(f"Documents path for scanning does not exist: {self.documents_path}")
            return []

        file_list = []
        # base_for_rel_path is the folder *containing* .main_backup, i.e., server.backup_folder_name()
        base_for_search_display_path = os.path.dirname(self.documents_path) 

        for root, dirs, files in os.walk(self.documents_path):
            # Optionally, add logic here to exclude hidden directories or specific directories
            # dirs[:] = [d for d in dirs if not d.startswith('.')] # Example: exclude hidden dirs
            for file_name in files:
                # Optionally, add logic here to exclude hidden files
                # if file_name.startswith('.'): continue # Example: exclude hidden files
                file_path = os.path.join(root, file_name)
                file_date = os.path.getmtime(file_path)
                search_display_path = os.path.relpath(file_path, base_for_search_display_path)
                file_list.append({"name": file_name, "path": file_path, "date": file_date, "search_display_path": search_display_path})
        return file_list

    def on_search_changed(self, entry):
        if self.search_timer:
            self.search_timer.cancel()

        query = entry.get_text().strip().lower()
        self.last_query = query  # Store the last query

        if not self.files_loaded:
            self.pending_search_query = query
            if query: # Only show spinner if there's a query and files are not loaded
                GLib.idle_add(self._show_center_spinner)
            else: # Query cleared, files not loaded, hide spinner
                GLib.idle_add(self._hide_center_spinner)
            return

        if query:
            GLib.idle_add(self._show_center_spinner) # Show spinner before starting search thread
            self.search_timer = Timer(0.5, 
                lambda: threading.Thread(target=self.perform_search, args=(query,), 
                                        daemon=True).start())
            self.search_timer.start()
        else:
            GLib.idle_add(self._hide_center_spinner) # Hide spinner if query is cleared
            # Show latest backup files from latest backup date
            self.populate_latest_backups()

    def perform_search(self, query):
        """Perform the search and update the results."""
        # Spinner is typically shown by on_search_changed or if files were not loaded initially.
        # If perform_search is called directly (e.g. after scan), ensure spinner is shown.
        GLib.idle_add(self._show_center_spinner)

        if not self.files_loaded:
            self.pending_search_query = query
            # Spinner is already shown by the caller or initial scan.
            return

        try:
            results = self.search_backup_sources(query)
            self.top_center_label.set_text("Backups Files")
        except AttributeError as e:
            # This is a fallback. Ideally, the `if not self.files_loaded` check prevents this.
            # If this happens, it indicates a deeper issue with state management during file loading.
            print(f"Critical Search Error (AttributeError): {e}. File attributes might be missing.")
            print("Attempting to re-initialize file scan and deferring search.")
            self.files_loaded = False  # Mark as not loaded to ensure re-check/re-scan
            self.pending_search_query = query # Re-queue the current search
            self.scan_files_folder_threaded() # Re-trigger the scan
            results = []
        except Exception as e:
            print(f"Error during search: {e}")
            results = []
        # Hide spinner after results are processed by populate_results
        GLib.idle_add(self.populate_results, results)
    
    def on_diff_button_clicked_from_row(self, button, backup_file_path_from_button):
        """Handles the Diff button click from a row in the main search results."""
        backup_file_path = backup_file_path_from_button

        original_file_path = self._get_original_path_from_backup(backup_file_path)
        if not original_file_path or not os.path.exists(original_file_path):
            dialog = Adw.MessageDialog(transient_for=self, modal=True,
                                       title="Diff Error",
                                       body="Original file not found in your home directory to compare against.")
            dialog.add_response("ok", "OK")
            dialog.connect("response", lambda d, r: d.close())
            dialog.present()
            return

        backup_label_extra = ""
        # Since files in populate_results are from .main_backup, they are the "current" backup version
        if server.main_backup_folder() in backup_file_path:
            backup_label_extra = " (Current Backup)"
        # Fallback for other cases, though not strictly expected for populate_results items
        else:
            path_parts = backup_file_path.replace(server.backup_folder_name(), "").lstrip(os.sep).split(os.sep)
            if len(path_parts) > 2 and path_parts[0] != server.MAIN_BACKUP_LOCATION: # Incremental
                try:
                    date_str, time_str = path_parts[0], path_parts[1]
                    backup_label_extra = f" (Backup: {date_str} {time_str.replace('-', ':')})"
                except Exception: pass

        diff_win = DiffViewWindow(
            transient_for=self, # self is BackupWindow
            file1_path=backup_file_path, file2_path=original_file_path,
            file1_label=f"{os.path.basename(backup_file_path)}{backup_label_extra}",
            file2_label=f"{os.path.basename(original_file_path)} (Current in Home)")
        diff_win.present()

    def search_backup_sources(self, query):
        query = query.strip().lower()
        if not query:
            return []

        # With index
        matches = []
        for idx, name in enumerate(self.file_names_lower):
            # Check against basename or the searchable display path
            if query in name or query in self.file_search_display_paths_lower[idx]:
                matches.append(self.files[idx])
        #matches.sort(key=lambda x: x["date"], reverse=True)
        return matches[:self.page_size]
    
    def _generate_thumbnail_pixbuf(self, file_path, size_px=32):
        """
        Generates a GdkPixbuf.Pixbuf thumbnail for a given file.
        Supports images and videos (using ffmpeg for videos).
        """
        if not os.path.exists(file_path):
            return None

        if file_path in self.thumbnail_cache:
            return self.thumbnail_cache[file_path]

        pixbuf = None
        ext = os.path.splitext(file_path)[1].lower()
        mime, _ = mimetypes.guess_type(file_path)
        if mime is None: mime = ""

        try:
            if ext in server.IMAGE_EXTENSIONS or mime.startswith("image"):
                temp_pixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)
                img_width = temp_pixbuf.get_width()
                img_height = temp_pixbuf.get_height()
                scale = min(size_px / img_width, size_px / img_height)
                pixbuf = temp_pixbuf.scale_simple(int(img_width * scale), int(img_height * scale), GdkPixbuf.InterpType.BILINEAR)
            elif ext in server.VIDEO_EXTENSIONS or mime.startswith("video"):
                # Generate thumbnail using ffmpeg (first frame)
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_thumb:
                    thumb_path = tmp_thumb.name
                try:
                    # Extract first frame as PNG
                    sub.run([
                        "ffmpeg", "-y", "-i", file_path, "-vf", f"thumbnail,scale={size_px}:{size_px}",
                        "-frames:v", "1", thumb_path
                    ], stdout=sub.DEVNULL, stderr=sub.DEVNULL)
                    if os.path.exists(thumb_path):
                        temp_pixbuf = GdkPixbuf.Pixbuf.new_from_file(thumb_path)
                        pixbuf = temp_pixbuf
                finally:
                    if os.path.exists(thumb_path):
                        os.remove(thumb_path)
        except Exception as e:
            print(f"Error generating thumbnail for {file_path}: {e}")
            pixbuf = None

        if pixbuf:
            self.thumbnail_cache[file_path] = pixbuf
        return pixbuf

    def populate_results(self, results):
        """Populate the results listbox with up to 'self.page_size' search results, aligned in columns."""
        # Ensure the content page is visible and spinner is hidden
        GLib.idle_add(self._hide_center_spinner)

        if hasattr(self, "loading_label"):
            pass
            
        # Clear existing results from the listbox
        while True:
            first_child_row = self.listbox.get_first_child() # This returns a Gtk.ListBoxRow
            if not first_child_row: # No fade out for simplicity, instant clear
                break
            self.listbox.remove(first_child_row)
 
        limited_results = results[:self.page_size]

        for file_info in limited_results:
            grid = Gtk.Grid()
            grid.set_column_spacing(12) # Reduced spacing
            grid.set_row_spacing(0)
            grid.set_hexpand(True)
            grid.set_vexpand(False)

            # Thumbnail or Icon
            thumbnail_pixbuf = self._generate_thumbnail_pixbuf(file_info["path"], 32) # 32px thumbnail
            if thumbnail_pixbuf:
                texture = Gdk.Texture.new_for_pixbuf(thumbnail_pixbuf)
                thumbnail_widget = Gtk.Image.new_from_paintable(texture)
            else:
                # Fallback icon
                ext = os.path.splitext(file_info["name"])[1].lower()
                if ext == ".pdf":
                    icon_name = "application-pdf"
                elif ext in server.TEXT_EXTENSIONS: # Use your server.TEXT_EXTENSIONS
                    icon_name = "text-x-generic"
                elif ext in server.IMAGE_EXTENSIONS: # Use your server.IMAGE_EXTENSIONS
                    icon_name = "image-x-generic"
                else:
                    icon_name = "text-x-generic" # Default
                thumbnail_widget = Gtk.Image.new_from_icon_name(icon_name)
                
            thumbnail_widget.set_pixel_size(32) # Ensure consistent size for icons too
            grid.attach(thumbnail_widget, 0, 0, 1, 1)

            # Name and Size Box (Vertical)
            name_and_size_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            name_and_size_box.set_hexpand(True) # This box should expand

            # Name Label
            shorted_file_path = file_info["path"].replace(server.backup_folder_name(), "").lstrip(os.sep)
            name_label = Gtk.Label(label=shorted_file_path, xalign=0)
            name_label.set_hexpand(True) # Name label expands within its parent (name_and_size_box)
            name_label.set_halign(Gtk.Align.START)
            name_label.set_ellipsize(Pango.EllipsizeMode.END)  # Enable ellipsizing
            name_and_size_box.append(name_label)

            # Size Label
            size_label_text = server.get_item_size(file_info["path"], True)
            if size_label_text == "None": # server.get_item_size returns string "None"
                size_label_text = "N/A"
            size_label = Gtk.Label(label=size_label_text, xalign=0)
            size_label.add_css_class("caption") # Style as caption
            name_and_size_box.append(size_label)
            
            grid.attach(name_and_size_box, 1, 0, 1, 1) # Col 1: Name/Size Box
            
            # Date Label
            backup_date_str = ""
            path_for_date_extraction = file_info["path"].replace(server.backup_folder_name(), "").lstrip(os.sep)
            path_parts = path_for_date_extraction.split(os.sep)

            if len(path_parts) > 1 and path_parts[0] != server.MAIN_BACKUP_LOCATION:
                try:
                    date_str_from_path = path_parts[0]
                    time_str_from_path = path_parts[1]
                    
                    parsed_date_obj = datetime.strptime(date_str_from_path, "%d-%m-%Y")
                    formatted_time_str = time_str_from_path.replace('-', ':')
                    backup_date_str = f"{parsed_date_obj.strftime('%b %d')} {formatted_time_str}"
                except (ValueError, IndexError):
                    backup_date_str = datetime.fromtimestamp(file_info["date"]).strftime("%b %d %H:%M")
            else:
                backup_date_str = datetime.fromtimestamp(file_info["date"]).strftime("%b %d %H:%M")
            date_label = Gtk.Label(label=backup_date_str, xalign=0)
            date_label.set_hexpand(False)
            date_label.set_halign(Gtk.Align.START)
            date_label.add_css_class("caption")
            grid.attach(date_label, 2, 0, 1, 1)

            # Star button for each row
            star_button_row = Gtk.Button()
            star_button_row.add_css_class("flat")
            setattr(star_button_row, "file_path", file_info["path"])

            star_button_row.set_sensitive(True)
            path_for_star_check = self._get_main_backup_equivalent_path(file_info["path"])

            if path_for_star_check in self.starred_files:
                star_button_row.set_icon_name("starred-symbolic")
                star_button_row.set_tooltip_text("Unstar this item")
            else:
                star_button_row.set_icon_name("non-starred-symbolic")
                star_button_row.set_tooltip_text("Star this item")
            star_button_row.connect("clicked", self.on_star_button_clicked, file_info["path"], star_button_row)
            grid.attach(star_button_row, 3, 0, 1, 1)
            
            # --- Actions MenuButton ---
            actions_button = Gtk.MenuButton(icon_name="view-more-symbolic", label="Actions")
            actions_button.set_direction(Gtk.ArrowType.DOWN)
            actions_button.set_tooltip_text("More actions for this file")

            menu = Gio.Menu()
            # Restore
            menu.append("Restore File", "item.restore")
            # Open
            menu.append("Open File", "item.open")
            # Open Location
            menu.append("Open Location", "item.open_location")
            # Diff
            menu.append("Compare (Diff)", "item.diff")
            # Versions
            menu.append("Find All Versions", "item.versions")

            popover = Gtk.PopoverMenu()
            popover.set_menu_model(menu)
            actions_button.set_popover(popover)
            
            grid.attach(actions_button, 4, 0, 1, 1) # Add the menu button to the grid

            # --- Row setup and actions ---
            row_revealer = Gtk.Revealer()
            row_revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
            row_revealer.set_transition_duration(250)
            row_revealer.set_child(grid)

            listbox_row = Gtk.ListBoxRow()
            listbox_row.set_margin_top(6)
            listbox_row.set_margin_bottom(3)
            listbox_row.set_margin_start(12)
            listbox_row.set_margin_end(12)
            listbox_row.set_child(row_revealer)
            listbox_row.add_css_class("file-list-row-card")
            listbox_row.device_path = file_info["path"]

            # Create an action group for this specific row
            action_group = Gio.SimpleActionGroup()
            listbox_row.insert_action_group("item", action_group)

            # Helper function to create and add actions
            def add_row_action(name, callback):
                action = Gio.SimpleAction.new(name, None)
                action.connect("activate", callback)
                action_group.add_action(action)
                return action

            # Add actions to the row's action group
            path = file_info["path"]
            add_row_action("restore", lambda a, p, current_path=path: self.perform_restore_action(current_path))
            add_row_action("open", lambda a, p, current_path=path: self.on_open_file_clicked(current_path))
            add_row_action("open_location", lambda a, p, current_path=path: self.on_open_location_clicked(current_path))
            # The 'find_update' method expects a 'button_stack' which we don't have. Pass None.
            add_row_action("versions", lambda a, p, current_path=path: self.find_update(current_path, None))
            
            # Special handling for Diff action to enable/disable it
            diff_action = add_row_action("diff", lambda a, p, current_path=path: self.on_diff_button_clicked_from_row(None, current_path))
            can_diff = False
            original_path_for_diff = self._get_original_path_from_backup(path)
            if original_path_for_diff and os.path.exists(original_path_for_diff):
                ext_check = os.path.splitext(path)[1].lower()
                if ext_check in server.TEXT_EXTENSIONS:
                    can_diff = True
            diff_action.set_enabled(can_diff)

            self.listbox.append(listbox_row)
            row_revealer.set_reveal_child(True)
            
    def on_star_button_clicked(self, button_widget, file_path_clicked, star_button_itself):
        # Determine the path to actually store in self.starred_files (always the .main_backup equivalent)
        path_to_star_or_unstar = self._get_main_backup_equivalent_path(file_path_clicked)

        if path_to_star_or_unstar in self.starred_files:
            # Item is currently starred, so unstar it
            self.starred_files.remove(path_to_star_or_unstar)
            star_button_itself.set_icon_name("non-starred-symbolic")
            star_button_itself.set_tooltip_text("Star this item")
            print(f"Unstarred (actual stored path): {path_to_star_or_unstar} (clicked: {file_path_clicked})")
        else:
            # Item is not starred, so star it
            # Add to the end (most recent)
            self.starred_files.append(path_to_star_or_unstar)
            # If limit exceeded, remove the oldest (first item)
            if len(self.starred_files) > self.MAX_STARRED_FILES:
                removed_oldest = self.starred_files.pop(0)
                print(f"Starred files limit ({self.MAX_STARRED_FILES}) reached. Removed oldest starred: {removed_oldest}")
            star_button_itself.set_icon_name("starred-symbolic")
            star_button_itself.set_tooltip_text("Unstar this item")
            print(f"Starred (actual stored path): {path_to_star_or_unstar} (clicked: {file_path_clicked})")
        
        # Save to JSON
        starred_file_json_path = server.get_starred_files_location()
        try:
            os.makedirs(os.path.dirname(starred_file_json_path), exist_ok=True)
            with open(starred_file_json_path, 'w') as f:
                json.dump(self.starred_files, f) # self.starred_files is already a list
        except Exception as e:
            print(f"Error saving starred files to {starred_file_json_path}: {e}")
        GLib.idle_add(self._populate_starred_files) # Refresh the starred items section
    
    def on_open_file_clicked(self, file_path_from_button):
        if file_path_from_button:
            if not os.path.isfile(file_path_from_button):
                print(f"Error: The file does not exist or is not accessible: {file_path_from_button}")
                dialog = Adw.MessageDialog(transient_for=self, modal=True,
                                           title="Cannot Open File",
                                           body=f"The file '{os.path.basename(file_path_from_button)}' could not be found or accessed at the backup location.")
                dialog.add_response("ok", "OK")
                dialog.connect("response", lambda d, r: d.close())
                dialog.present()
                return

            try:
                file_uri = GLib.filename_to_uri(file_path_from_button, None)
                Gio.AppInfo.launch_default_for_uri_async(file_uri, None, None,
                                                         self._on_open_file_callback, file_path_from_button)
                print(f"Attempting to open file: {file_path_from_button}")
            except GLib.Error as e:
                print(f"GLib error preparing to open file {file_path_from_button}: {e}. Falling back to xdg-open.")
                self._fallback_open_file(file_path_from_button)
            except Exception as e:
                print(f"Unexpected error opening file {file_path_from_button}: {e}. Falling back to xdg-open.")
                self._fallback_open_file(file_path_from_button)
        else:
            print("No file path provided to open.")

    def _on_open_file_callback(self, source_object, res, user_data):
        file_path = user_data
        try:
            success = Gio.AppInfo.launch_default_for_uri_finish(res)
            if success:
                print(f"Successfully launched default application for: {file_path}")
            else:
                print(f"Failed to launch default application for: {file_path} (launch_default_for_uri_finish returned false). Falling back.")
                self._fallback_open_file(file_path) # Fallback if Gio launch fails
        except GLib.Error as e:
            print(f"Error launching default application for {file_path}: {e}. Falling back.")
            self._fallback_open_file(file_path)

    # Open location button
    # def on_open_location_clicked(self, button):
    #     if self.selected_file_path:
    #         folder = os.path.dirname(self.selected_file_path)
            
    #         try:
    #             sub.Popen(["xdg-open", folder])
    #         except Exception as e:
    #             print("Failed to open folder:", e)

    def on_open_location_clicked(self, file_path_from_button):
        if file_path_from_button:
            folder_path = os.path.dirname(file_path_from_button)
            
            if not os.path.isdir(folder_path):
                print(f"Error: The parent directory does not exist or is not accessible: {folder_path}")
                dialog = Adw.MessageDialog(transient_for=self, modal=True,
                                           title="Cannot Open Location",
                                           body=f"The folder '{folder_path}' could not be found or accessed.")
                dialog.add_response("ok", "OK")
                dialog.connect("response", lambda d, r: d.close())
                dialog.present()
                return

            try:
                folder_uri = GLib.filename_to_uri(folder_path, None)
                # Asynchronously launch the default application for the folder URI
                Gio.AppInfo.launch_default_for_uri_async(folder_uri, None, None, 
                                                         self._on_open_location_callback, folder_path)
                print(f"Attempting to open folder: {folder_path}")
            except GLib.Error as e:
                print(f"GLib error preparing to open folder {folder_path}: {e}. Falling back to xdg-open.")
                self._fallback_open_location(folder_path)
            except Exception as e: # Catch any other unexpected errors
                print(f"Unexpected error opening folder {folder_path}: {e}. Falling back to xdg-open.")
                self._fallback_open_location(folder_path)
        else:
            print("No file path provided to open location.")
            
    def _fallback_open_file(self, file_path):
        """Fallback to xdg-open if Gio methods fail for opening a file."""
        try:
            sub.Popen(["xdg-open", file_path])
            print(f"Opened file: {file_path} using xdg-open as fallback.")
        except Exception as e_xdg:
            print(f"Failed to open file {file_path} with xdg-open: {e_xdg}")
            dialog = Adw.MessageDialog(transient_for=self, modal=True,
                                       title="Error Opening File",
                                       body=f"Could not open file: {os.path.basename(file_path)}\nDetails: {e_xdg}")
            dialog.add_response("ok", "OK")
            dialog.connect("response", lambda d, r: d.close())
            dialog.present()

    def _fallback_open_location(self, folder_path):
        """Fallback to xdg-open if Gio methods fail."""
        try:
            sub.Popen(["xdg-open", folder_path])
            print(f"Opened folder: {folder_path} using xdg-open as fallback.")
        except Exception as e_xdg:
            print(f"Failed to open folder {folder_path} with xdg-open: {e_xdg}")
            dialog = Adw.MessageDialog(transient_for=self, modal=True,
                                       title="Error Opening Location",
                                       body=f"Could not open folder: {folder_path}\nDetails: {e_xdg}")
            dialog.add_response("ok", "OK")
            dialog.connect("response", lambda d, r: d.close())
            dialog.present()

    def _on_open_location_callback(self, source_object, res, user_data):
        folder_path = user_data
        try:
            success = Gio.AppInfo.launch_default_for_uri_finish(res)
            if success:
                print(f"Successfully launched file manager for: {folder_path}")
            else:
                print(f"Failed to launch file manager for: {folder_path}. Falling back.")
                self._fallback_open_location(folder_path)
        except GLib.Error as e:
            print(f"Error launching file manager for {folder_path}: {e}. Falling back.")
            self._fallback_open_location(folder_path)

    # def on_listbox_key_press(self, controller, keyval, keycode, state):
    #     if keyval == Gdk.KEY_space:
    #         row = self.listbox.get_selected_row()
    #         if row:
    #             path = getattr(row, "device_path", None)
    #             if path:
    #                 self.open_preview_window(path)
    #         return True
    #     return False
    
    def open_preview_window_popup(self, filepath): # Renamed to avoid conflict with inline show_preview
        # If a preview window is already open, close it and return (toggle behavior)
        if getattr(self, "preview_window", None) is not None:
            self.preview_window.close()
            self.preview_window = None
            return

        ext = os.path.splitext(filepath)[1].lower()
        mime, _ = mimetypes.guess_type(filepath)
        if mime is None:
            mime = ""
        # Only allow preview for supported types - PDF preview removed #NOSONAR
        previewable = False
        IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"}
        TEXT_EXTENSIONS = {".txt", ".py", ".md", ".csv", ".json", ".xml", ".ini", ".log", ".gd", ".js", ".html", ".css", ".sh", ".c", ".cpp", ".h", ".hpp", ".java", ".rs", ".go", ".toml", ".yml", ".yaml"}
        if (ext in TEXT_EXTENSIONS or mime.startswith("text")) and os.path.exists(filepath): #NOSONAR #NOSONAR
            previewable = True
        elif (ext in IMAGE_EXTENSIONS or mime.startswith("image")) and os.path.exists(filepath):
            previewable = True

        if not previewable:
            print("No preview available for this file.")
            return

        preview_win = Gtk.Window(title="File Preview")
        self.preview_window = preview_win  # Track the window

        preview_win.set_default_size(600, 400)
        preview_win.set_resizable(True)
        preview_win.set_deletable(True)
        preview_win.set_size_request(400, 600)

        # Set a maximum size (e.g., 90% of the screen)
        display = Gdk.Display.get_default()
        if not display:
            max_width = 800
            max_height = 600
        else:
            monitor_to_use = display.get_primary_monitor()
            if not monitor_to_use:
                monitors = display.get_monitors()
                if monitors.get_n_items() > 0:
                    monitor_to_use = monitors.get_item(0)
                else:
                    max_width = 800
                    max_height = 600
                    monitor_to_use = None
            if monitor_to_use:
                geometry = monitor_to_use.get_geometry()
                max_width = int(geometry.width * 0.9)
                max_height = int(geometry.height * 0.9)
            else:
                max_width = 800
                max_height = 600

        preview_win.set_default_size(min(600, max_width), min(400, max_height))
        preview_win.set_size_request(400, 600)

        # Add a scrolled window for the content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        preview_win.set_child(scrolled)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        scrolled.set_child(box)

        # PDF Preview removed
        if (ext in TEXT_EXTENSIONS or mime.startswith("text")) and os.path.exists(filepath): #NOSONAR #NOSONAR
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read(4096)
            textview = Gtk.TextView()
            textview.set_editable(False)
            textview.set_vexpand(True)
            textview.set_hexpand(True)
            textview.set_wrap_mode(Gtk.WrapMode.WORD)
            textview.get_buffer().set_text(text)
            textview.set_size_request(-1, 350)
            box.append(textview)
        elif (ext in IMAGE_EXTENSIONS or mime.startswith("image")) and os.path.exists(filepath):
            picture = Gtk.Picture.new_for_filename(filepath)
            picture.set_content_fit(Gtk.ContentFit.CONTAIN)
            picture.set_vexpand(True)
            picture.set_hexpand(True)
            box.append(picture)

        # # Add key controller to the preview window for Spacebar close
        # key_controller = Gtk.EventControllerKey()
        # def preview_key_press(controller, keyval, keycode, state):
        #     if keyval == Gdk.KEY_space:
        #         preview_win.close()
        #         return True
        #     return False
        # key_controller.connect("key-pressed", preview_key_press)
        # preview_win.add_controller(key_controller)

        # When the preview window is closed, clear the reference
        def on_close(win, *args):
            self.preview_window = None

        preview_win.connect("close-request", on_close)
        preview_win.present()

    def on_settings_clicked(self, action, parameter=None):
        # Only create one settings window at a time
        if getattr(self, "settings_window", None) is not None:
            self.settings_window.present()
            return
        self.settings_window = SettingsWindow(application=self.get_application())
        self.settings_window.set_modal(True)  # Make modal
        self.settings_window.set_transient_for(self)  # Set parent
        def on_close(win, *args):
            self.settings_window = None
        self.settings_window.connect("close-request", on_close)
        self.settings_window.present()
        
    def on_about_clicked(self, action, parameter):
        """Shows the About window."""
        print(server.ID + ".png")
        about_window = Adw.AboutWindow(
            transient_for=self,
            application_name=server.APP_NAME,
            application_icon=server.ID,    
            version=server.APP_VERSION,
            developer_name=server.DEV_NAME,
            website=server.GITHUB_PAGE,
            issue_url=server.GITHUB__ISSUES,
            copyright=server.COPYRIGHT,        
            release_notes=server.APP_RELEASE_NOTES,
            comments="timemachine is a simple and efficient backup solution for your personal files.",
        )
        about_window.present()
        
    def _get_original_path_from_backup(self, backup_file_path: str) -> str | None:
        """
        Determines the original path in the user's home directory for a given backup file path.
        """
        abs_backup_file_path = os.path.abspath(backup_file_path)
        # main_backup_abs_path = os.path.abspath(server.main_backup_folder()) # Not expected from versions window
        incremental_backups_abs_path = os.path.abspath(server.backup_folder_name())
        
        rel_path = None
        if abs_backup_file_path.startswith(incremental_backups_abs_path):
            # Path is like /path/to/driver/timemachine/backups/DATE/TIME/rel/path/to/file
            temp_rel_path = os.path.relpath(abs_backup_file_path, incremental_backups_abs_path)
            parts = temp_rel_path.split(os.sep)
            if len(parts) > 2: # Must have DATE, TIME, and then the actual relative path
                # The first two parts are DATE and TIME, the rest is the relative path to home
                rel_path = os.path.join(*parts[2:])
            else:
                logging.error(f"Could not determine relative path for incremental backup: {backup_file_path} - unexpected structure: {parts}")
                return None
        else:
            # This case should ideally not be hit if called from the versions window,
            # as it filters out main_backup_folder items.
            # If it's a direct path from .main_backup (e.g. if this func is reused elsewhere):
            main_backup_abs_path_check = os.path.abspath(server.main_backup_folder())
            if abs_backup_file_path.startswith(main_backup_abs_path_check):
                 rel_path = os.path.relpath(abs_backup_file_path, main_backup_abs_path_check)
            else:
                logging.error(f"File path '{backup_file_path}' is not within a known backup structure (incremental or main).")
                return None
            
        if rel_path is not None:
            return os.path.join(server.USER_HOME, rel_path)
        return None

    ########################################################################################
    # Find updates for a file
    ########################################################################################
    def find_update(self, file_path, button_stack=None):
        # Extract the file name to search for all its backup versions
        
        # Show spinner on the button that was clicked, if it exists
        if button_stack:
            button_stack.set_visible_child_name("spinner")
            spinner = button_stack.get_child_by_name("spinner")
            spinner.start()

        def do_search():
            file_name = os.path.basename(file_path)
            results = []
            for root, dirs, files in os.walk(server.backup_folder_name()):
                for fname in files:
                    if fname == file_name:
                        fpath = os.path.join(root, fname)
                        fdate = os.path.getmtime(fpath)
                        results.append({
                            "name": fname,
                            "path": fpath,
                            "date": fdate
                        })
            results.sort(key=lambda x: x["date"], reverse=True)

            def on_search_done():
                if button_stack:
                    spinner.stop()
                    button_stack.set_visible_child_name("button")
                self.show_update_window(file_name, results)

            GLib.idle_add(on_search_done)

        threading.Thread(target=do_search, daemon=True).start()    
    def show_update_window(self, file_name, results):
        """
        Show a window with all previous backups for the selected file.
        Reminder:
                - This will only show backups that are not in the main backup folder, e.g.: 01.01.2025/12-05/...
        """
        # Create a small window (no minimize/maximize)
        win = Gtk.Window(
            title=f'All previous backups for "{file_name}"',
            modal=True,
            transient_for=self,
            default_width=850, # Slightly wider for more info
            default_height=650
        )
        self.update_window = win

        def on_close(win, *args):
            self.update_window = None

        win.connect("close-request", on_close)

        # Header bar with Close and Restore buttons
        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label=f"Versions for \"{file_name}\"")) # Adwaita style title
        win.set_titlebar(header) # Set header for the Gtk.Window

        # Open button
        open_button = Gtk.Button(label="Open File")
        open_button.set_tooltip_text("Open this version of the file.")
        open_button.set_sensitive(False)
        header.pack_start(open_button)

        # Open Location button
        open_location_button = Gtk.Button(label="Open Location")
        open_location_button.set_tooltip_text("Open the folder containing this backup version.")
        open_location_button.set_sensitive(False)
        header.pack_start(open_location_button)

        # Diff button
        diff_button = Gtk.Button(label="Diff")
        diff_button.set_tooltip_text("Compare this version with the current file in your home directory.")
        diff_button.set_sensitive(False) # Initially insensitive
        header.pack_start(diff_button)

        # Restore button (moved to header)
        restore_button = Gtk.Button(label="Restore File")
        restore_button.set_css_classes(["suggested-action"])
        restore_button.set_sensitive(False)
        header.pack_end(restore_button)

        # Main content: List of updates
        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
            margin_top=6,
            margin_bottom=6,
            margin_start=6,
            margin_end=6
        )
        win.set_child(vbox)

        # ListBox for updates inside a scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        vbox.append(scrolled)

        listbox = Gtk.ListBox() #NOSONAR
        listbox.set_vexpand(True)
        listbox.set_hexpand(True)
        listbox.add_css_class("overview-card") # Consistent styling with main listbox
        scrolled.set_child(listbox)
        listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        # For status messages
        status_label = Gtk.Label()
        vbox.append(status_label)

        progressbar = Gtk.ProgressBar()
        progressbar.set_hexpand(True)
        progressbar.set_visible(False)
        vbox.append(progressbar)

        # Populate the listbox with backup versions
        for result in results:
            # Skip backups that are from the main backup folder
            if server.MAIN_BACKUP_LOCATION in result["path"]:
                continue

            row = Gtk.ListBoxRow()
            row.set_margin_top(8)
            row.set_margin_bottom(8)
            row.add_css_class("file-list-row-card") # Consistent styling

            grid = Gtk.Grid()
            grid.set_column_spacing(12)
            grid.set_hexpand(True)
            row.set_child(grid)

            # Icon
            ext = os.path.splitext(result["name"])[1].lower()
            icon_name = "text-x-generic" # Default
            if ext == ".pdf": icon_name = "application-pdf"
            elif ext in server.TEXT_EXTENSIONS: icon_name = "text-x-generic"
            elif ext in server.IMAGE_EXTENSIONS: icon_name = "image-x-generic"
            # Add more specific icons as needed

            icon_widget = Gtk.Image.new_from_icon_name(icon_name)
            icon_widget.set_pixel_size(24) # Slightly smaller icon for version list
            icon_widget.set_valign(Gtk.Align.CENTER)
            grid.attach(icon_widget, 0, 0, 1, 2) # Span 2 rows if using two labels

            # Path Label (Primary Text)
            path_label_text = os.path.relpath(result["path"], server.backup_folder_name())
            path_label = Gtk.Label(label=path_label_text, xalign=0)
            path_label.set_hexpand(True)
            path_label.set_ellipsize(Pango.EllipsizeMode.END)
            grid.attach(path_label, 1, 0, 1, 1)

            # Date Label (Secondary Text - mtime of this version)
            # date_str = datetime.fromtimestamp(result["date"]).strftime("%Y-%m-%d %H:%M:%S")
            date_str = result["path"]
            date_label = Gtk.Label(label=date_str, xalign=0)
            date_label.add_css_class("caption")
            grid.attach(date_label, 1, 1, 1, 1)

            # Size Label (in its own column)
            size_str = server.get_item_size(result["path"], True)
            if size_str == "None": size_str = "N/A"
            size_label_widget = Gtk.Label(label=size_str, xalign=1) # Align to the right
            size_label_widget.add_css_class("caption")
            size_label_widget.set_valign(Gtk.Align.CENTER)
            size_label_widget.set_hexpand(False) # Don't let size expand too much
            size_label_widget.set_width_chars(10) # Give it some minimum width
            grid.attach(size_label_widget, 2, 0, 1, 2) # Span 2 rows, attach to col 2

            # Attach file path to row for later use
            row.file_path = result["path"]
            listbox.append(row)
        # Enable restore button only when a row is selected
        def on_row_selected(lb, row):
            is_selected = row is not None
            restore_button.set_sensitive(is_selected)
            open_button.set_sensitive(is_selected)
            open_location_button.set_sensitive(is_selected)
            
            can_diff = False
            if row:
                selected_backup_path = getattr(row, "file_path", None)
                win.selected_backup_version_path = selected_backup_path # Store on the versions window
                self.selected_file_path = selected_backup_path # Keep this for open/restore if needed

                if selected_backup_path:
                    original_path = self._get_original_path_from_backup(selected_backup_path)
                    ext = os.path.splitext(selected_backup_path)[1].lower()
                    if ext in server.TEXT_EXTENSIONS and original_path and os.path.exists(original_path):
                        can_diff = True
            else:
                win.selected_backup_version_path = None
                self.selected_file_path = None
            
            diff_button.set_sensitive(can_diff)

        def on_open_clicked(btn):
            if self.selected_file_path:
                self.on_open_file_clicked(self.selected_file_path)

        def on_open_location_clicked_header(btn): # Renamed to avoid conflict
            if self.selected_file_path:
                self.on_open_location_clicked(self.selected_file_path)

        def on_diff_btn_clicked(btn_widget): # Renamed to avoid conflict
            # 'win' here is the versions_window
            self.on_show_diff_clicked(btn_widget, win) 

        listbox.connect("row-selected", on_row_selected)
        diff_button.connect("clicked", on_diff_btn_clicked)
        
        # Restore logic
        def on_restore_clicked(btn):
            # btn.set_sensitive(False) # Sensitivity handled by perform_restore_action
            row = listbox.get_selected_row()
            if not row or not hasattr(row, "file_path"):
                return
            file_to_restore = getattr(row, "file_path")
            self.perform_restore_action(file_to_restore, btn) # Pass the button itself
        restore_button.connect("clicked", on_restore_clicked)
        open_button.connect("clicked", on_open_clicked)
        open_location_button.connect("clicked", on_open_location_clicked_header)

        # # Add key controller for Spacebar preview
        # key_controller = Gtk.EventControllerKey()
        # def on_key_press(controller, keyval, keycode, state):
        #     if keyval == Gdk.KEY_space:
        #         row = listbox.get_selected_row()
        #         if row and hasattr(row, "file_path"):
        #             self.open_preview_window(row.file_path)
        #         return True
        #     return False
        # key_controller.connect("key-pressed", on_key_press)
        # listbox.add_controller(key_controller)

        win.connect("close-request", on_close)
        win.present()

    def on_show_diff_clicked(self, button, versions_window):
        backup_file_path = getattr(versions_window, "selected_backup_version_path", None)
        if not backup_file_path:
            return

        original_file_path = self._get_original_path_from_backup(backup_file_path)
        if not original_file_path or not os.path.exists(original_file_path):
            dialog = Adw.MessageDialog(transient_for=versions_window, modal=True,
                                       title="Diff Error",
                                       body="Original file not found in your home directory to compare against.")
            dialog.add_response("ok", "OK")
            dialog.connect("response", lambda d, r: d.close())
            dialog.present()
            return

        backup_label_extra = ""
        try:
            path_parts = backup_file_path.split(os.sep)
            if len(path_parts) >= 3 and path_parts[-3].count('-') == 2 and path_parts[-2].count('-') == 1:
                date_str, time_str = path_parts[-3], path_parts[-2]
                backup_label_extra = f" (Backup: {date_str} {time_str.replace('-', ':')})"
        except Exception: pass

        diff_win = DiffViewWindow(
            transient_for=versions_window,
            file1_path=backup_file_path, file2_path=original_file_path,
            file1_label=f"{os.path.basename(backup_file_path)}{backup_label_extra}",
            file2_label=f"{os.path.basename(original_file_path)} (Current in Home)")
        diff_win.present()
    
    # def update_overview_cards_from_summary(self):
    #     summary_file_path = server.get_summary_filename()
    #     if not os.path.exists(summary_file_path):
    #         print(f"Summary file not found: {summary_file_path}")
    #         # Optionally, clear or show default/empty state for cards
    #         return

    #     try:
    #         with open(summary_file_path, 'r') as f:
    #             summary_data = json.load(f)
    #     except Exception as e:
    #         print(f"Error loading or parsing summary file {summary_file_path}: {e}")
    #         return

    #     if "categories" not in summary_data:
    #         print("Summary file does not contain 'categories' key.")
    #         return

    #     # Assuming overview_cards_grid is accessible and its children are the cards in order
    #     # This part needs to be robust. It's better to store references to the cards or their labels.
    #     # For now, let's assume a direct mapping based on the order in overview_data in __init__
    #     # This is a simplified example; a more robust solution would involve updating specific cards by ID or title.
    #     # For this example, we'll just print, as direct update is complex without card references.
    #     print("Summary data found!")
    #     # TODO: Implement logic to find and update each card in self.overview_cards_grid

    def on_restore_button_clicked_from_row(self, button):
        file_to_restore = getattr(button, "file_path", None)
        if file_to_restore:
            self.perform_restore_action(file_to_restore, button)
        else:
            print("No file_path associated with this restore button.")

    # Centralized restore logic
    def perform_restore_action(self, file_to_restore_path, clicked_button_widget=None):
        if clicked_button_widget:
            clicked_button_widget.set_sensitive(False)

        if not file_to_restore_path:
            print("No file path provided for restore.")
            if clicked_button_widget: GLib.idle_add(clicked_button_widget.set_sensitive, True)
            return

        abs_file_to_restore_path = os.path.abspath(file_to_restore_path)
        main_backup_abs_path = os.path.abspath(server.main_backup_folder())
        incremental_backups_abs_path = os.path.abspath(server.backup_folder_name())

        rel_path = None
        if abs_file_to_restore_path.startswith(main_backup_abs_path):
            rel_path = os.path.relpath(abs_file_to_restore_path, main_backup_abs_path)
        elif abs_file_to_restore_path.startswith(incremental_backups_abs_path):
            temp_rel_path = os.path.relpath(abs_file_to_restore_path, incremental_backups_abs_path)
            # Expected structure: DATE/TIME/actual/path/to/file
            parts = temp_rel_path.split(os.sep)
            if len(parts) > 2: # Ensure there's at least DATE/TIME and then the actual relative path
                rel_path = os.path.join(*parts[2:])
            else:
                print(f"Error: Could not determine relative path for incremental backup: {file_to_restore_path}")
                if clicked_button_widget: GLib.idle_add(clicked_button_widget.set_sensitive, True)
                return
        else:
            print(f"Error: File path '{file_to_restore_path}' is not within known backup locations: '{main_backup_abs_path}' or '{incremental_backups_abs_path}'")
            if clicked_button_widget: GLib.idle_add(clicked_button_widget.set_sensitive, True)
            return

        destination_path = os.path.join(server.USER_HOME, rel_path)

        # Set daemon state to restoring
        self.current_daemon_state = "restoring"
        GLib.idle_add(self._update_status_icon_display)

        def do_restore():
            try:
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                src = file_to_restore_path # Use the passed file_to_restore_path
                dst = destination_path
                file_id_restore = f"restore_{dst}" # Unique ID for the transfer row
                filename_restore = os.path.basename(dst)
                total_size = os.path.getsize(src)
                copied = 0
                chunk_size = 1024 * 1024  # 1MB

                with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                    while True:
                        chunk = fsrc.read(chunk_size)
                        if not chunk: break
                        fdst.write(chunk)
                        copied += len(chunk)
                        progress = copied / total_size if total_size > 0 else 1.0
                        size_restore_str = server.get_item_size(src, True)
                        eta_restore_str = "Restoring..." if progress < 1.0 else "Done"
                        GLib.idle_add(self.update_or_create_transfer, file_id_restore, filename_restore, size_restore_str, eta_restore_str, progress)
                print(f"Restored {src} to {dst}")
                shutil.copystat(src, dst)

                if clicked_button_widget:
                    GLib.idle_add(clicked_button_widget.set_sensitive, True)

                # Close the update window if the restore was triggered from there
                if hasattr(self, "update_window") and self.update_window is not None and self.update_window.get_visible():
                    if clicked_button_widget and clicked_button_widget.get_ancestor(Gtk.Window) == self.update_window:
                        GLib.idle_add(self.update_window.close)
            except Exception as e:
                print(f"Error restoring file: {e}")
                if clicked_button_widget: GLib.idle_add(clicked_button_widget.set_sensitive, True)
            # The 'finally' block for hiding progressbar is removed as the row handles its own lifecycle.
        threading.Thread(target=do_restore, daemon=True).start()

    def on_main_window_close(self, *args):
        self.get_application().quit()
        return False  # Propagate event
    
    def on_window_map(self, *args):
        self.search_entry.grab_focus()
        # self.add_found_devices_to_devices_popover_box() # This is now handled by the modal
        return False
    
    #########################################################################
    # LOGS
    ##########################################################################
    def show_backup_logs_dialog(self, action, parameter=None):
        """Display backup logs dialog."""
        logs_dialog = Adw.Window(
            transient_for=self,
            title="Backup Logs",
            modal=True,
            default_width=600,
            default_height=400,
        )

        # Read logs file from the server location
        log_file_path = server.get_log_file_path()
        try:
            with open(log_file_path, "r") as log_file:
                log_content = log_file.read()
        except FileNotFoundError:
            log_content = "Error: Log file not found."
        except Exception as e:
            log_content = f"Error reading log file: {e}"

        # Header bar with buttons
        header_bar = Gtk.HeaderBar()

        # Main content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=10)
        main_box.set_halign(Gtk.Align.FILL)
        logs_dialog.set_content(main_box)

        # Terminal-like Logs section
        log_view = Gtk.TextView(editable=False, cursor_visible=False, monospace=True)
        log_buffer = log_view.get_buffer()
        log_view.set_wrap_mode(Gtk.WrapMode.NONE)

        # Insert the log content into the buffer
        log_buffer.set_text(log_content)

        # Create a Scrolled Window for the logs
        logs_scrolled = Gtk.ScrolledWindow()
        logs_scrolled.set_child(log_view)
        logs_scrolled.set_vexpand(True)

        # Pack widgets into the main box
        main_box.append(header_bar)
        main_box.append(logs_scrolled)

        # Show the dialog
        logs_dialog.present()

    def on_restore_system_button_clicked(self, action, parameter=None):
        # Modal window
        win = Gtk.Window(
            title="System Restore",
            modal=True,
            transient_for=self,
            default_width=600,
            default_height=500
        )

        # HeaderBar with Restore button
        header = Gtk.HeaderBar()
        restore_btn = Gtk.Button(label="Restore")
        restore_btn.set_css_classes(["suggested-action"])
        restore_btn.set_halign(Gtk.Align.START)
        header.pack_end(restore_btn)
        win.set_titlebar(header)

        # Stack for pages
        stack = Gtk.Stack()
        win.set_child(stack)

        # --- PAGE 1: Selection ---
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16, margin_top=16, margin_bottom=16, margin_start=16, margin_end=16)

        # Applications (Deb/RPM)
        self.apps_checkbox = Gtk.CheckButton(label="Applications (Deb/RPM)")
        vbox.append(self.apps_checkbox)

        # Applications dropdown area (hidden by default), with a scrolled window
        self.apps_dropdown_scrolled = Gtk.ScrolledWindow()
        self.apps_dropdown_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.apps_dropdown_scrolled.set_vexpand(True)
        self.apps_dropdown_scrolled.set_hexpand(True)
        self.apps_dropdown_scrolled.set_visible(False)
        self.apps_dropdown_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, margin_start=24)
        self.apps_dropdown_scrolled.set_child(self.apps_dropdown_box)
        vbox.append(self.apps_dropdown_scrolled)

        def on_apps_toggled(check, pspec=None):
            self.apps_dropdown_scrolled.set_visible(check.get_active())
            if check.get_active() and not hasattr(self, "_apps_checkboxes_loaded"):
                self._apps_checkboxes_loaded = True
                # Add RPM packages
                rpm_folder = server.rpm_main_folder()
                if os.path.exists(rpm_folder):
                    for pkg in os.listdir(rpm_folder):
                        if pkg.endswith('.rpm'):
                            cb = Gtk.CheckButton(label=f"RPM: {pkg}")
                            cb.package_path = os.path.join(rpm_folder, pkg)
                            self.apps_dropdown_box.append(cb)
                # Add DEB packages
                deb_folder = server.deb_main_folder()
                if os.path.exists(deb_folder):
                    for pkg in os.listdir(deb_folder):
                        if pkg.endswith('.deb'):
                            cb = Gtk.CheckButton(label=f"DEB: {pkg}")
                            cb.package_path = os.path.join(deb_folder, pkg)
                            self.apps_dropdown_box.append(cb)
                if not any(isinstance(child, Gtk.CheckButton) for child in self.apps_dropdown_box):
                    self.apps_dropdown_box.append(Gtk.Label(label="No packages found."))

        self.apps_checkbox.connect("toggled", on_apps_toggled)

        # Files/Folders
        self.files_checkbox = Gtk.CheckButton(label="Files/Folders")
        vbox.append(self.files_checkbox)

        # Files/Folders dropdown area (hidden by default), with a scrolled window
        self.files_dropdown_scrolled = Gtk.ScrolledWindow()
        self.files_dropdown_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.files_dropdown_scrolled.set_vexpand(True)
        self.files_dropdown_scrolled.set_hexpand(True)
        self.files_dropdown_scrolled.set_visible(False)
        self.files_dropdown_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, margin_start=24)
        self.files_dropdown_scrolled.set_child(self.files_dropdown_box)
        vbox.append(self.files_dropdown_scrolled)

        def on_files_toggled(check, pspec=None):
            self.files_dropdown_scrolled.set_visible(check.get_active())
            if check.get_active() and not hasattr(self, "_files_checkboxes_loaded"):
                self._files_checkboxes_loaded = True
                # List all files and folders in main_backup_folder
                main_folder = server.main_backup_folder()
                if os.path.exists(main_folder):
                    items = sorted(os.listdir(main_folder), key=lambda x: x.lower())
                    for item in items:
                        item_path = os.path.join(main_folder, item)
                        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                        if os.path.isdir(item_path):
                            icon = Gtk.Image.new_from_icon_name("folder")
                        else:
                            # Use a generic file icon or guess by extension
                            ext = os.path.splitext(item)[1].lower()
                            if ext in [".jpg", ".jpeg", ".png", ".gif"]:
                                icon_name = "image-x-generic"
                            elif ext in [".pdf"]:
                                icon_name = "application-pdf"
                            elif ext in [".txt", ".md", ".log"]:
                                icon_name = "text-x-generic"
                            else:
                                icon_name = "text-x-generic"
                            icon = Gtk.Image.new_from_icon_name(icon_name)
                        icon.set_pixel_size(16)
                        hbox.append(icon)
                        hbox.append(Gtk.Label(label=item))
                        cb = Gtk.CheckButton()
                        cb.set_child(hbox)
                        cb.restore_path = item_path
                        cb.is_folder = os.path.isdir(item_path)
                        self.files_dropdown_box.append(cb)
                else:
                    self.files_dropdown_box.append(Gtk.Label(label="No files or folders found."))

        self.files_checkbox.connect("toggled", on_files_toggled)

        # Flatpaks
        flatpak_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.flatpak_checkbox = Gtk.CheckButton(label="Flatpaks")
        flatpak_box.append(self.flatpak_checkbox)
        vbox.append(flatpak_box)

        # Flatpak dropdown area (hidden by default), now with a scrolled window
        self.flatpak_dropdown_scrolled = Gtk.ScrolledWindow()
        self.flatpak_dropdown_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.flatpak_dropdown_scrolled.set_vexpand(True)
        self.flatpak_dropdown_scrolled.set_hexpand(True)
        self.flatpak_dropdown_scrolled.set_visible(False)
        self.flatpak_dropdown_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, margin_start=24)
        self.flatpak_dropdown_scrolled.set_child(self.flatpak_dropdown_box)
        flatpak_box.append(self.flatpak_dropdown_scrolled)

        def on_flatpak_toggled(check, pspec=None):
            self.flatpak_dropdown_scrolled.set_visible(check.get_active())
            if check.get_active() and not hasattr(self, "_flatpak_checkboxes_loaded"):
                self._flatpak_checkboxes_loaded = True
                # Load flatpak apps from file
                flatpak_txt = server.flatpak_txt_location()
                if os.path.exists(flatpak_txt):
                    with open(flatpak_txt, "r") as f:
                        for line in f:
                            app = line.strip()
                            if app:
                                cb = Gtk.CheckButton(label=app)
                                self.flatpak_dropdown_box.append(cb)
                else:
                    self.flatpak_dropdown_box.append(Gtk.Label(label="No Flatpak list found."))

        self.flatpak_checkbox.connect("toggled", on_flatpak_toggled)

        stack.add_named(vbox, "select")

        # --- PAGE 2: Progress ---
        progress_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=32,
            margin_bottom=32,
            margin_start=32, 
            margin_end=32)
        progress_label = Gtk.Label(label="Restoring...")
        progress_label.set_halign(Gtk.Align.CENTER)
        progress_bar = Gtk.ProgressBar()
        progress_bar.set_hexpand(True)
        progress_bar.set_valign(Gtk.Align.CENTER)
        progress_box.append(progress_label)
        progress_box.append(progress_bar)

        # Terminal/log area
        terminal_scrolled = Gtk.ScrolledWindow()
        terminal_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        terminal_scrolled.set_vexpand(True)
        terminal_scrolled.set_hexpand(True)
        progress_box.append(terminal_scrolled)

        terminal_view = Gtk.TextView(editable=False, cursor_visible=False, monospace=True)
        terminal_buffer = terminal_view.get_buffer()
        terminal_scrolled.set_child(terminal_view)

        stack.add_named(progress_box, "progress")

        # --- Restore button handler ---
        def on_restore_clicked(btn):
            restore_btn.set_sensitive(False)
            stack.set_visible_child_name("progress")
            progress_bar.set_fraction(0)
            progress_label.set_text("Restoring...")

            terminal_buffer.set_text("")  # Clear terminal

            # Gather selected items
            restore_tasks = []

            # Applications (DEB/RPM)
            if self.apps_checkbox.get_active():
                child = self.apps_dropdown_box.get_first_child()
                while child:
                    if isinstance(child, Gtk.CheckButton) and child.get_active():
                        label = child.get_label()
                        pkg_path = getattr(child, "package_path", None)
                        if pkg_path and os.path.exists(pkg_path):
                            restore_tasks.append(("app", label, pkg_path))
                    child = child.get_next_sibling()

            # Files/Folders
            if self.files_checkbox.get_active():
                child = self.files_dropdown_box.get_first_child()
                while child:
                    if isinstance(child, Gtk.CheckButton) and child.get_active():
                        # Extract label from the hbox child
                        label = None
                        hbox = child.get_child()
                        if isinstance(hbox, Gtk.Box):
                            for subchild in hbox:
                                if isinstance(subchild, Gtk.Label):
                                    label = subchild.get_text()
                                    break
                        if label is None:
                            label = "Unknown"
                        restore_path = getattr(child, "restore_path", None)
                        is_folder = getattr(child, "is_folder", False)
                        if restore_path and os.path.exists(restore_path):
                            restore_tasks.append(("file", label, restore_path, is_folder))
                    child = child.get_next_sibling()

            # Flatpaks
            if self.flatpak_checkbox.get_active():
                child = self.flatpak_dropdown_box.get_first_child()
                while child:
                    if isinstance(child, Gtk.CheckButton) and child.get_active():
                        label = child.get_label()
                        restore_tasks.append(("flatpak", label, None))
                    child = child.get_next_sibling()

            if not restore_tasks:
                restore_tasks = [("info", "Nothing selected", None)]

            def append_terminal(text):
                end_iter = terminal_buffer.get_end_iter()
                terminal_buffer.insert(end_iter, text + "\n")
                # Scroll to end
                mark = terminal_buffer.create_mark(None, terminal_buffer.get_end_iter(), False)
                terminal_view.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
            
            # Files and Folders restoration
            def restore_folder_with_incrementals():
                """
                Applies incremental updates by copying, for each file, the latest updated version
                from the update folders (sorted in descending order) to dest_root.

                For each file in the update folders:
                - Compute the file's path relative to the update folder.
                - Remove the first path element if necessary (for example, if the update folder's name
                    is part of the relative path and should not be).
                - If the file has already been updated by a later (newer) update, skip it.
                - Otherwise, copy the file to the destination, ensuring that the directory structure is preserved.
                """
                base_backup_folder = server.main_backup_folder()
                
                # 2. Apply incremental updates (if any)
                updates_root = server.backup_folder_name()
                if os.path.exists(updates_root):
                    incremental_folders = [folder for folder in os.listdir(updates_root)
                                        if os.path.isdir(os.path.join(updates_root, folder))]
                    base_folder_name = os.path.basename(base_backup_folder)
                    if base_folder_name in incremental_folders:
                        incremental_folders.remove(base_folder_name)
                    try:
                        incremental_folders.sort(
                            key=lambda folder: datetime.strptime(folder, "%d-%m-%Y"),
                            reverse=True
                        )
                    except Exception as e:
                        GLib.idle_add(append_terminal, f"Error parsing update folder names: {e}")
                        return

                    updated_files = set()
                    file_count = 0
                    for _, date in enumerate(incremental_folders):
                        update_path = os.path.join(updates_root, str(date))
                        for root, dirs, files in os.walk(update_path):
                            for file in files:
                                rel_path = os.path.relpath(os.path.join(root, file), update_path)
                                rel_path = "/".join(rel_path.split('/')[1:])
                                if rel_path in updated_files:
                                    continue
                                dest_item = os.path.join(server.HOME_USER, rel_path)
                                try:
                                    #os.makedirs(os.path.dirname(dest_item), exist_ok=True)
                                    #shutil.copy2(os.path.join(root, file), dest_item)
                                    updated_files.add(rel_path)
                                    file_count += 1
                                    # Only update UI every 20 files
                                    if file_count % 20 == 0:
                                        GLib.idle_add(progress_label.set_text, f"Restoring: {rel_path}")
                                        GLib.idle_add(append_terminal, f"Incremental: {os.path.join(root, file)} → {dest_item}")
                                        time.sleep(0.01)  # Yield to avoid UI freeze
                                except Exception as e:
                                    GLib.idle_add(append_terminal, f"Error updating {rel_path}: {e}")
                    # Final update for the last file
                    GLib.idle_add(progress_label.set_text, f"Restoring: {rel_path}")
                    GLib.idle_add(append_terminal, f"Incremental: {os.path.join(root, file)} → {dest_item}")

            def restore_folder(src_root: str, dest_root: str):
                count = 0
                for root, dirs, files in os.walk(src_root):
                    for file in files:
                        src_item = os.path.join(root, file)
                        relative_path = os.path.relpath(src_item, src_root)
                        dest_item = os.path.join(dest_root, relative_path)
                        try:
                            os.makedirs(os.path.dirname(dest_item), exist_ok=True)
                            shutil.copy2(src_item, dest_item)
                            count += 1
                            # Only update UI every 20 files
                            if count % 20 == 0:
                                GLib.idle_add(progress_label.set_text, f"Restoring: {relative_path}")
                                GLib.idle_add(append_terminal, f"Restored: {src_item} → {dest_item}")
                                time.sleep(0.01)  # Yield to avoid UI freeze
                        except Exception as e:
                            GLib.idle_add(append_terminal, f"Error copying {src_item}: {e}")
                # Final update for the last file
                GLib.idle_add(progress_label.set_text, f"Restoring: {relative_path}")
                GLib.idle_add(append_terminal, f"Restored: {src_item} → {dest_item}")

            def run_restore():
                total = len(restore_tasks)
                folders_restored = False
                for idx, task in enumerate(restore_tasks):
                    kind = task[0]
                    label = task[1]
                    GLib.idle_add(progress_label.set_text, f"Restoring: {label}")
                    GLib.idle_add(append_terminal, f"Restoring: {label}")

                    if kind == "app":
                        package_manager = check_package_manager()
                        TEST_MODE = True  # Set to True to simulate, False for real install
                        if package_manager == 'deb':
                            cmd = ["dpkg", "-i", pkg_path]
                        elif package_manager == 'rpm':
                            cmd = ["rpm", "-ivh", "--replacepkgs", pkg_path]
                        else:
                            cmd = None

                        if cmd:
                            try:
                                if TEST_MODE:
                                    # Simulate with echo for testing
                                    proc = sub.Popen(
                                        ["echo", f"Simulating install of {label} ({' '.join(cmd)})"],
                                        stdout=sub.PIPE, stderr=sub.PIPE, text=True
                                    )
                                else:
                                    proc = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, text=True)
                                for line in proc.stdout:
                                    GLib.idle_add(append_terminal, line.rstrip())
                                for line in proc.stderr:
                                    GLib.idle_add(append_terminal, line.rstrip())
                                proc.wait()
                                if proc.returncode == 0:
                                    GLib.idle_add(append_terminal, f"Installed: {label}")
                                else:
                                    GLib.idle_add(append_terminal, f"Error installing {label}")
                            except Exception as e:
                                GLib.idle_add(append_terminal, f"Error: {e}")
                    elif kind == "file":
                        restore_path = task[2]
                        is_folder = task[3]
                        TEST_MODE = True  # Set to True to simulate, False for real restore
                        try:
                            if is_folder:
                                if TEST_MODE:
                                    GLib.idle_add(append_terminal, f"\n[TEST MODE] Would restore folder: {label}")
                                else:
                                    restore_folder(restore_path, server.HOME_USER)
                                    GLib.idle_add(append_terminal, f"Restored folder: {label}")
                            else:
                                dest_item = os.path.join(server.HOME_USER, os.path.basename(restore_path))
                                if TEST_MODE:
                                    GLib.idle_add(progress_label.set_text, f"\n[TEST MODE] Restoring: {os.path.basename(restore_path)}")
                                    GLib.idle_add(append_terminal, f"\n[TEST MODE] Would restore file: {restore_path} → {dest_item}")
                                else:
                                    shutil.copy2(restore_path, dest_item)
                                    GLib.idle_add(progress_label.set_text, f"Restoring: {os.path.basename(restore_path)}")
                                    GLib.idle_add(append_terminal, f"Restored file: {restore_path} → {dest_item}")
                        except Exception as e:
                            GLib.idle_add(append_terminal, f"Error restoring {label}: {e}")
                    elif kind == "flatpak":
                        flatpak_ref = label
                        try:
                            GLib.idle_add(progress_label.set_text, f"\nInstalling Flatpak: {flatpak_ref}")
                            GLib.idle_add(append_terminal, f"\nInstalling Flatpak: {flatpak_ref}")
                            # --- TEST MODE: set to True to simulate, False to really install ---
                            TEST_MODE = True

                            if TEST_MODE:
                                # Simulate with echo for testing
                                proc = sub.Popen(
                                    ["echo", f"Simulating install of {flatpak_ref}"],
                                    stdout=sub.PIPE, stderr=sub.PIPE, text=True
                                )
                            else:
                                # Real Flatpak install
                                proc = sub.Popen(
                                    ["flatpak", "install", "--system", "--noninteractive", "--assumeyes", flatpak_ref],
                                    stdout=sub.PIPE, stderr=sub.PIPE, text=True
                                )
                            for line in proc.stdout:
                                GLib.idle_add(append_terminal, line.rstrip())
                            for line in proc.stderr:
                                GLib.idle_add(append_terminal, line.rstrip())
                            proc.wait()
                            if proc.returncode == 0:
                                GLib.idle_add(append_terminal, f"Successfully installed Flatpak: {flatpak_ref}")
                            else:
                                GLib.idle_add(append_terminal, f"Failed to install Flatpak '{flatpak_ref}'")
                        except Exception as e:
                            GLib.idle_add(append_terminal, f"Error installing Flatpak {flatpak_ref}: {e}")
                    elif kind == "info":
                        GLib.idle_add(append_terminal, label)

                    GLib.idle_add(progress_bar.set_fraction, (idx + 1) / total)
                    time.sleep(0.2)

                # After all restores, do incrementals if any folder was restored
                if folders_restored:
                    restore_folder_with_incrementals()

                GLib.idle_add(progress_bar.set_fraction, 1.0)
                GLib.idle_add(progress_label.set_text, "Restore Complete!")
                GLib.idle_add(append_terminal, "Restore Complete!")
                GLib.idle_add(restore_btn.set_sensitive, True)

            threading.Thread(target=run_restore, daemon=True).start()

        restore_btn.connect("clicked", on_restore_clicked)
        win.present()


class SettingsWindow(Adw.PreferencesWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Settings")
        self.set_default_size(600, 600)

        self.ignored_folders = []
        self.ignored_folders = server.load_ignored_folders_from_config()
        self.programmatic_change = False  
        self.switch_cooldown_active = False  # To track the cooldown state
        
        # Get exclude hidden items setting from the server 
        # Get exclude hidden items setting from the server
        self.exclude_hidden_itens: bool = server.get_database_value(
            section='EXCLUDE',
            option='exclude_hidden_itens')
        
        # --- Backups Tab ---
        backups_page = Adw.PreferencesPage(title="Backups")
        backups_page.set_icon_name("backups-app-symbolic")
        backups_group = Adw.PreferencesGroup(title="Back Up Automatically")
        
        auto_backup_row = Adw.ActionRow(title="Enable Automatic Backups")
        self.auto_backup_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.auto_backup_switch.connect("notify::active", self.on_auto_backup_switch_toggled)
        auto_backup_row.add_suffix(self.auto_backup_switch)
        backups_group.add(auto_backup_row)

        # Use a horizontal box for label + switch
        auto_backup_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        backups_group.add(auto_backup_box)
        backups_page.add(backups_group)
        self.add(backups_page)

        # --- Create a new ActionRow for "Exclude Hidden Files" ---
        self.exclude_hidden_switch = Gtk.Switch(valign=Gtk.Align.CENTER) # Already defined
        exclude_hidden_files_row = Adw.ActionRow(title="Ignore hidden files")
        exclude_hidden_files_row.add_suffix(self.exclude_hidden_switch)
        exclude_hidden_files_row.set_activatable_widget(self.exclude_hidden_switch)
        exclude_hidden_files_row.set_selectable(False)
        self.exclude_hidden_switch.connect("notify::active", self.on_exclude_hidden_switch_toggled)
        
        # --- Folders to Ignore Tab ---
        folders_to_ignore_page = Adw.PreferencesPage(title="Folders")
        folders_to_ignore_page.set_icon_name("folder")

        # Bold title for the "ignore hidden files"
        self.ignore_hidden_files_group = Adw.PreferencesGroup(title="Ignore Hidden Files")
        # Bold title for the folders group
        self.folders_to_ignore_group = Adw.PreferencesGroup(title="Folders To Ignore")
        
        # Create a vertical box to hold the header and the folder list
        folders_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Horizontal box for label and add button (header)
        folders_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        folders_header.set_halign(Gtk.Align.CENTER)

        add_folder_button = Gtk.Button(icon_name="list-add-symbolic", halign=Gtk.Align.CENTER)
        add_folder_button.add_css_class("flat")
        add_folder_button.connect("clicked", self.on_add_folder_clicked)
        folders_header.append(add_folder_button)

        folders_vbox.append(folders_header)

        # Box for the folder rows
        self.ignore_folders_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        folders_vbox.append(self.ignore_folders_box)
        
        self.ignore_hidden_files_group.add(exclude_hidden_files_row)
        self.folders_to_ignore_group.add(folders_vbox)

        folders_to_ignore_page.add(self.ignore_hidden_files_group)
        folders_to_ignore_page.add(self.folders_to_ignore_group)
        self.add(folders_to_ignore_page)

        ##########################################################################
        # STARTUP
        ##########################################################################
        self.auto_backup_checkbox()
        self.auto_select_hidden_itens()  # Exclude hidden files
        self.load_folders_from_config()
        self.display_excluded_folders()  
        self.display_excluded_folders()
    
    def display_excluded_folders(self):
        """Display loaded excluded folders."""
        for folder in self.ignored_folders:
            # logging.info("Adding folder: %s", folder)
            self.add_folder_to_list(folder)
    
    def load_folders_from_config(self):
        """Loads folders from the config file."""
        config = configparser.ConfigParser()

        if os.path.exists(server.CONF_LOCATION):  # Ensure the config file exists
            config.read(server.CONF_LOCATION)
            if 'EXCLUDE_FOLDER' in config:  # Check if the section exists
                self.ignored_folders = config.get('EXCLUDE_FOLDER', 'folders').split(',')
                # Remove empty strings in case of trailing commas
                self.ignored_folders = [folder.strip() for folder in self.ignored_folders if folder.strip()]
    
    ######################################################################################
    # Automatic Backup Switch
    ######################################################################################
    def auto_backup_checkbox(self):
        # Get stored driver_location and driver_name
        automatically_backup = server.get_database_value(
            section='BACKUP',
            option='automatically_backup')

        self.programmatic_change = True  # Set the flag to indicate programmatic change

        if automatically_backup:
            self.auto_backup_switch.set_active(True)
        else:
            self.auto_backup_switch.set_active(False)
        
        self.programmatic_change = False  # Reset the flag after programmatic change
    
    def enable_switch(self, switch):
        """Re-enable the switch after the cooldown period."""
        self.switch_cooldown_active = False
        self.auto_backup_switch.set_sensitive(True)  # Re-enable the switch
    
    def disable_switch_for_cooldown(self, switch):
        """Disables the switch and re-enables it after the cooldown period."""
        self.switch_cooldown_active = True
        switch.set_sensitive(False)  # Disable the switch to prevent user interaction

        def enable_switch_after_cooldown():
            time.sleep(5)  # Cooldown delay
            GLib.idle_add(self.enable_switch, switch)  # Re-enable in the main thread

        # Start the cooldown in a new thread to avoid blocking the UI
        threading.Thread(target=enable_switch_after_cooldown, daemon=True).start()
    
    def on_auto_backup_switch_toggled(self, switch, pspec):
        """Handle the 'Back Up Automatically' switch toggle."""
        if self.programmatic_change or self.switch_cooldown_active:
            return  # Exit the function if it's a programmatic change or cooldown active

        if switch.get_active(): # Trying to enable
            # Check for persistent critical error state by reading the log
            log_file_path = server.get_log_file_path()
            has_critical_in_log = False
            if os.path.exists(log_file_path):
                try:
                    with open(log_file_path, 'r') as f:
                        for line_log in f: # Scan efficiently
                            if "[CRITICAL]" in line_log:
                                has_critical_in_log = True
                                break
                except Exception as e:
                    print(f"Could not check log for critical errors: {e}")

            if has_critical_in_log:
                self.programmatic_change = True
                switch.set_active(False) # Prevent enabling
                self.programmatic_change = False
                
                error_dialog = Adw.MessageDialog(
                    transient_for=self.get_root(),
                    modal=True, title="Cannot Enable Automatic Backup",
                    body="A critical error was previously logged. Automatic backup has been disabled.\n\nPlease resolve the issue (check application logs) and restart Time Machine to attempt re-enabling automatic backups."
                )
                error_dialog.add_response("ok", "OK")
                error_dialog.connect("response", lambda d, r: d.close())
                error_dialog.present()
                return # Stop further processing for enabling

        # Check if the switch is being enabled
        if switch.get_active():
            # Disable the switch immediately and start the cooldown
            self.disable_switch_for_cooldown(switch)

            # Wait for user's confirmation to proceed
            def handle_confirmation(confirmed):
                self._handle_auto_backup_enable_confirmation(confirmed, switch)

            # Show the confirmation dialog
            self.confirm_backup_device(handle_confirmation)
        else:
            # If the switch is being disabled, proceed without showing the dialog
            self._handle_auto_backup_disable(switch)

    # Helper for enabling logic after confirmation
    def _handle_auto_backup_enable_confirmation(self, confirmed, switch):
        if not confirmed:
            self.programmatic_change = True
            switch.set_active(False)
            self.programmatic_change = False
            if self.switch_cooldown_active:
                 GLib.idle_add(self.enable_switch, switch)
            return

        if not server.is_daemon_running():
            self.start_daemon()
        
        self.create_autostart_entry_if_not_exists()
        server.set_database_value('BACKUP', 'automatically_backup', 'true')

    # Helper for disabling logic
    def _handle_auto_backup_disable(self, switch):
        self.stop_daemon()
        self.remove_autostart_entry()
        server.set_database_value('BACKUP', 'automatically_backup', 'false')

    # New helper for creating autostart (to avoid code duplication)
    def create_autostart_entry_if_not_exists(self):
        autostart_dir = os.path.expanduser("~/.config/autostart/")
        autostart_file_path = os.path.join(autostart_dir, f"{server.APP_NAME_CLOSE_LOWER}_autostart.desktop")

        if not os.path.exists(autostart_file_path):
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_file_content = f"""
                [Desktop Entry]
                Type=Application
                Exec=flatpak run --command=python3 {server.ID} /app/share/{server.APP_NAME_CLOSE_LOWER}/src/at_boot.py
                Icon={server.ID}
                X-GNOME-Autostart-enabled=true
                Name={server.APP_NAME}
                Comment[en_US]=Automatically start {server.APP_NAME}
                Comment=Automatically start {server.APP_NAME}
                """
            with open(autostart_file_path, 'w') as f:
                f.write(desktop_file_content)
            logging.info("Autostart entry created.")
        else:
            logging.info("Autostart entry already exists.")

    def confirm_backup_device(self, callback):
        """Show a confirmation dialog to confirm the backup device."""
        device_name = server.get_database_value(
            section='DRIVER',
            option='driver_name'
        )

        # Create the Adw.MessageDialog
        dialog = Adw.MessageDialog(
            transient_for=self.get_root(), # Use self.get_root() for Adw.Window
            modal=True,
            title="Enable Automatic Backup",
            body=f"Do you want to back up to this device: '{device_name}'?"
        )

        # Add responses to the dialog
        dialog.add_response("yes", "Yes")
        dialog.set_response_appearance("yes", Adw.ResponseAppearance.SUGGESTED)
        dialog.add_response("no", "No")
        dialog.set_default_response("no")
        dialog.set_close_response("no")

        # Connect to the response signal
        def on_response(dialog_widget, response_id): # Matched signal signature
            dialog_widget.close()
            if response_id == "yes":
                print(f"User confirmed backup to device: {device_name}")
                callback(True)  # Call the callback with True
            else:
                print("User declined automatic backup.")
                callback(False)  # Call the callback with False

        dialog.connect("response", on_response)

        # Show the dialog
        dialog.present()

    def start_daemon(self):
        """Start the daemon and store its PID, ensuring only one instance runs."""
        def _do_start_daemon():
            process = None # Initialize process to None
            try:
                # Start a new daemon process
                daemon_cmd = ['python3', server.DAEMON_PY_LOCATION]
                logging.info(f"UI: Attempting to start daemon with command: {' '.join(daemon_cmd)}")
                
                if server.is_daemon_running():
                    logging.info("UI: Daemon is already running.")
                    return

                process = sub.Popen(
                    daemon_cmd,
                    start_new_session=True,
                    close_fds=True,
                    stdout=sub.PIPE,  # Capture standard output
                    stderr=sub.PIPE   # Capture standard error
                )
            except Exception:
                pass
                
        try:
            daemon_cmd = ['python3', server.DAEMON_PY_LOCATION]
            logging.info(f"UI: Attempting to start daemon with command: {' '.join(daemon_cmd)}")
            # Use Popen to start the daemon in the background without waiting for it
            sub.Popen(daemon_cmd, start_new_session=True, close_fds=True)
            logging.info("UI: Daemon process launched.")
        except Exception as e:
            error_msg = f"UI: Failed to start daemon: {e}"
            logging.error(error_msg, exc_info=True)

        # Create a start socket file
        threading.Thread(target=BackupWindow().create_connect_socket, daemon=True).start()  # Start the socket server in a separate thread
        threading.Thread(target=_do_start_daemon, daemon=True).start()

    def stop_daemon(self):
        """Stop daemon by removing the socket file"""
        BackupWindow().remove_socket()
        try:
            if os.path.exists(server.SOCKET_PATH):
                os.remove(server.SOCKET_PATH)
                logging.info(f"UI: Removed socket file {server.SOCKET_PATH} to signal daemon to stop.")
        except Exception as e:
            logging.error(f"UI: Error removing socket file to stop daemon: {e}")

    def remove_autostart_entry(self):
        autostart_file_path = os.path.expanduser(f"~/.config/autostart/{server.APP_NAME_CLOSE_LOWER}_autostart.desktop")
        if os.path.exists(autostart_file_path):
            os.remove(autostart_file_path)
            logging.info("Autostart entry removed.")

            # Update the conf file
            server.set_database_value(
                section='BACKUP',
                option='automatically_backup',
                value='false'
            )
    
    def create_folder_row(self, folder_name):
        """Create a row for folders with a trash icon."""
        row = Adw.ActionRow(title=folder_name)
        trash_button = Gtk.Button(icon_name="user-trash-symbolic", valign=Gtk.Align.CENTER)
        trash_button.add_css_class("flat")
        trash_button.connect("clicked", self.on_remove_folder_clicked, row, folder_name)
        row.add_suffix(trash_button)
        return row

    def on_remove_folder_clicked(self, button, row, folder_name):
        """Remove a folder row from the group."""
        parent = row.get_parent()
        parent.remove(row)

        # Remove the folder from the internal list
        if folder_name in self.ignored_folders:
            self.ignored_folders.remove(folder_name)

        # Save the updated list of folders to the config file
        self.save_folders_to_config()

        # Debugging: print the current ignored folders
        logging.info(f"Removed folder: {folder_name}")
        logging.info(f"Remaining ignored folders: {self.ignored_folders}")
        print(f"Removed folder: {folder_name}")
        print(f"Remaining ignored folders: {self.ignored_folders}")

    def on_add_folder_clicked(self, button):
        """Open a folder chooser dialog to add a folder to Ignore group."""
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Select a Folder To Ignore")
        dialog.set_modal(True)
        dialog.set_accept_label("_Select")

        def on_select_folder(dialog, result):
            try:
                folder = dialog.select_folder_finish(result)
                if folder:
                    folder_path = folder.get_path()
                    if folder_path not in self.ignored_folders:
                        self.ignored_folders.append(folder_path)
                        print(f"Selected folder: {folder_path}")
                        self.add_folder_to_list(folder_path)
                        self.save_folders_to_config()
            except Exception as e:
                print("Error selecting folder:", e)

        dialog.select_folder(self.get_application().get_active_window(), None, on_select_folder)
    
    def add_folder_to_list(self, folder):
        ignore_row = self.create_folder_row(folder)
        self.folders_to_ignore_group.add(ignore_row)

    def save_folders_to_config(self):
        """Saves the current list of ignored folders to the config file."""
        config = configparser.ConfigParser()
        config['EXCLUDE_FOLDER'] = {'folders': ','.join(self.ignored_folders)}
        
        server.set_database_value(
            section='EXCLUDE_FOLDER', 
            option='folders', 
            value=','.join(self.ignored_folders))
        
    def on_exclude_hidden_switch_toggled(self, switch, pspec):
        """Handle the 'Ignore Hidden Files' switch toggle."""
        true_false: str = 'false'

        # Handle the toggle state of the ignore hidden switch
        if switch.get_active():
            true_false = 'true'

        # Update the conf file
        server.set_database_value(
            section='EXCLUDE',
            option='exclude_hidden_itens',
            value=true_false)
    
    def auto_select_hidden_itens(self):
        if self.exclude_hidden_itens:
            self.exclude_hidden_switch.set_active(True)
        else:
            self.exclude_hidden_switch.set_active(False)

class BackupApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=server.ID,
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
    def do_activate(self):
        # Ensure dynamic CSS provider is set up early if BackupWindow uses it in __init__
        # This is a common pattern if dynamic styles are applied during window construction.
        # If BackupWindow._add_dynamic_css_rule is called in its __init__, this needs to be here.
        # However, based on current BackupWindow structure, it seems dynamic_css_provider
        # is initialized within BackupWindow.__init__ itself, which is fine.

        win = BackupWindow(application=self)
        win.present()

class DiffViewWindow(Adw.Window):
    def __init__(self, transient_for, file1_path, file2_path, file1_label, file2_label, **kwargs):
        super().__init__(modal=True, transient_for=transient_for, **kwargs)
        self.set_title(f"View Differences: {os.path.basename(file1_path)}")
        self.set_default_size(850, 700)

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(main_vbox)

        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label=f"Comparing Versions of {os.path.basename(file1_path)}"))
        main_vbox.append(header)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        main_vbox.append(scrolled_window)

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_monospace(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
        scrolled_window.set_child(self.textview)

        buffer = self.textview.get_buffer()

        # Tag for added lines
        added_tag = buffer.create_tag("added")
        added_color = Gdk.RGBA()
        added_color.red = 0.0  # Standard Green
        added_color.green = 0.5
        added_color.blue = 0.0
        added_color.alpha = 1.0
        added_tag.set_property("foreground_rgba", added_color)

        # Tag for removed lines
        removed_tag = buffer.create_tag("removed")
        removed_color = Gdk.RGBA()
        removed_color.red = 0.8 # Standard Red
        removed_color.green = 0.0
        removed_color.blue = 0.0
        removed_color.alpha = 1.0
        removed_tag.set_property("foreground_rgba", removed_color)

        # Tag for header lines
        header_tag = buffer.create_tag("header")
        # No specific color, will use default text color (black/white based on theme)
        # header_color = Gdk.RGBA() # Example if a color was desired
        # header_color.parse("grey")
        # header_tag.set_property("foreground_rgba", header_color)
        header_tag.set_property("weight", Pango.Weight.BOLD)

        self._generate_and_display_diff(file1_path, file2_path, file1_label, file2_label)

        
    def _generate_and_display_diff(self, file1_path, file2_path, file1_label, file2_label):
        buffer = self.textview.get_buffer()
        try:
            with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f1:
                file1_lines = [l.rstrip('\r\n') for l in f1.readlines()]
                file1_lines = f1.readlines()
            with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
                file2_lines = [l.rstrip('\r\n') for l in f2.readlines()]
        except Exception as e:
            buffer.insert(buffer.get_end_iter(), f"Error reading files: {e}\n")
            return

        diff_lines = list(difflib.unified_diff(file1_lines, file2_lines, fromfile=file1_label, tofile=file2_label, lineterm=''))
        if not diff_lines:
            buffer.insert(buffer.get_end_iter(), "Files are identical or no differences found.\n")
            return

        for line in diff_lines:
            end_iter = buffer.get_end_iter()
            line_to_insert = line + '\n'
            if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
                buffer.insert_with_tags_by_name(end_iter, line_to_insert, "header")
            elif line.startswith('+'):
                buffer.insert_with_tags_by_name(end_iter, line_to_insert, "added")
            elif line.startswith('-'):
                buffer.insert_with_tags_by_name(end_iter, line_to_insert, "removed")
            else:
                buffer.insert(end_iter, line_to_insert)

class BackupProgressRow(Gtk.Box):
    def __init__(self, file_id, filename, size, eta):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    def __init__(self, file_id, filename, size, eta, error_msg=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.file_id = file_id
        self.set_margin_top(6)
        self.set_margin_bottom(6)
        self.set_margin_start(8)
        self.set_margin_end(8)
        self.set_hexpand(True)
        self.add_css_class("backup-progress-row")

        # Top row: icon + filename + spacer + close button
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        top_row.set_hexpand(True)
        top_row.set_vexpand(True)
        self.append(top_row)

        # File icon
        icon = Gtk.Image.new_from_icon_name("document-send-symbolic") # Or a more specific icon based on file type if available
        # icon.set_pixel_size(24)
        top_row.append(icon)
        self.icon = Gtk.Image.new_from_icon_name("document-send-symbolic")
        self.append(self.icon)

        # Info column
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_box.set_hexpand(True)
        self.append(info_box)

        self.filename_label = Gtk.Label(label=filename)
        self.filename_label.set_xalign(0)
        self.filename_label.set_max_width_chars(32)
        self.filename_label.set_max_width_chars(25)
        self.filename_label.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(self.filename_label)

        self.size_eta_label = Gtk.Label(label=f"{size} • {eta}")
        self.size_eta_label.set_xalign(0)
        self.size_eta_label.add_css_class("dim-label")

        info_box.append(self.filename_label)
        info_box.append(self.size_eta_label)
        top_row.append(info_box)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        top_row.append(spacer)

        # Progress bar
        self.progress = Gtk.ProgressBar()
        self.progress.set_hexpand(True)
        self.progress.set_hexpand(False)
        self.progress.set_size_request(80, -1) # Give progress bar a fixed width
        self.progress.set_fraction(0.0)
        self.progress.set_margin_top(4)
        self.append(self.progress)

    def update(self, size, eta, progress):
        self.progress.set_fraction(progress)
        if progress >= 1.0:
            self.size_eta_label.set_text(f"{size} • success")
        else:
            self.size_eta_label.set_text(f"{size} • {eta}")

class ScanningStatusRow(Gtk.Box):
    def __init__(self, filename):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.set_margin_top(6)
        self.set_margin_bottom(6)
        self.set_margin_start(8)
        self.set_margin_end(8)
        self.set_hexpand(True)
        # self.add_css_class("backup-progress-row")

        # Top row: icon + scanning label
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        top_row.set_hexpand(True)
        top_row.set_vexpand(True)
        self.append(top_row)

        # File icon
        icon = Gtk.Image.new_from_icon_name("system-search") # Icon for scanning
        icon.set_pixel_size(24)
        top_row.append(icon)

        # Info column for the status label
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0) # spacing=0 or 2
        info_box.set_hexpand(True)
        self.status_label = Gtk.Label(label="Scanning...")
        self.status_label.set_xalign(0)
        self.status_label.set_max_width_chars(40) # Adjust as needed, similar to filename
        info_box.append(self.status_label)
        top_row.append(info_box)

        info_box.append(self.status_label)
        top_row.append(info_box)

    def update(self, text):
        if text:
            self.status_label.set_text(text)
            self.set_visible(True)
        else:
            self.set_visible(False)

def main():
    # server.setup_logging()
    app = BackupApp()
    return app.run(None)


if __name__ == "__main__":
    log_file_path = server.get_log_file_path()
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    main()
