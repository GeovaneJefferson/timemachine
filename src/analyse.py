from setup import *
from get_folders_to_be_backup import get_folders
from handle_spaces import handle_spaces
from get_sizes import number_of_item_to_backup, get_item_size
from get_users_de import get_user_de
from prepare_backup import may_continue_to_backup
from get_time import today_date


backup_home_dict = {}
items_to_backup_dict = {}

# Gnome list
list_gnome_include = [
    "gnome-shell",
    "dconf"
    ]

# Kde list
list_kde_include = [
        "kwin",
        "plasma_notes",
        "plasma",
        "aurorae",
        "color-schemes",
        "fonts",
        "kate",
        "kxmlgui5",
        "icons",
        "themes",

        "gtk-3.0",
        "gtk-4.0",
        "kdedefaults",
        "dconf",
        "fontconfig",
        "xsettingsd",
        "dolphinrc",
        "gtkrc",
        "gtkrc-2.0",
        "kdeglobals",
        "kwinrc",
        "plasmarc",
        "plasmarshellrc",
        "kglobalshortcutsrc",
        "khotkeysrc",
        "kwinrulesrc"
        "dolphinrc",
        "ksmserverrc",
        "konsolerc",
        "kscreenlockerrc",
        "plasmashellr",
        "plasma-org.kde.plasma.desktop-appletsrc",
        "plasmarc",
        "kdeglobals",
        
        "gtk-3.0",
        "gtk-4.0",
        "kdedefaults",
        "dconf",
        "fontconfig",
        "xsettingsd",
        "dolphinrc",
        "gtkrc",
        "gtkrc-2.0",
        "kdeglobals",
        "kwinrc",
        "plasmarc",
        "plasmarshellrc",
        "kglobalshortcutsrc",
        "khotkeysrc"
    ]

# Color
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Dates
has_date_folders = None

# Check if if there date/time folders
dates_list = []
for date_path in os.listdir(MAIN_INI_FILE.backup_dates_location()):
    if not date_path.startswith('.'):
        dates_list.append(date_path)

if dates_list:
    has_date_folders = True

else:
    has_date_folders = False

async def run_algo():
    try:                    
        # Source from .main backup folder
        for home_item_name, info in backup_home_dict.items():
            # Handle spaces
            home_item_name = handle_spaces(home_item_name)

            # Home item path
            home_item_path = info['location']

            # Remove home username location
            home_item_without_user_dir = str(home_item_path).replace(f'{HOME_USER}/', ' ').strip()
            
            # Only item dirname. Fx. Desktop
            home_item_dirname = os.path.dirname(home_item_without_user_dir)
            
            # Destination/Source full location
            main_custom_full_location = (
                MAIN_INI_FILE.main_backup_folder() + 
                '/' + 
                str(home_item_path).replace(HOME_USER + '/', ' ').strip()) 
           
            # Destination dirname 
            main_item_full_location_dirname = main_custom_full_location.split(
                '/')[1:-1]
            main_item_full_location_dirname = '/' + ','.join(
                main_item_full_location_dirname).replace(',', '/')
            

            # # .directory
            # print('Item name         :', home_item_name)  
            # # /home/xxx/Dekstop/directory
            # print('Item home path    :', home_item_path)  
            # # Desktop/directory
            # print('Item no dir loc.  :', home_item_without_user_dir)  
            # # /run/media/xxx/Backups/TMB/backups/.main_backups/Desktop/.directory
            # print('Custom dst, src.  :', main_custom_full_location)  
            # # /run/media/xxx/Backups/TMB/backups/.main_backups/Desktop/
            # print('Destination dir. n:', main_item_full_location_dirname)  
            # # Desktop
            # print('Item dirname      :', home_item_dirname)
            # print()

            # Check item 
            check_this_item(
                home_item_without_user_dir, 
                main_custom_full_location,
                main_item_full_location_dirname,
                home_item_name, 
                home_item_path)    
            
    except FileNotFoundError:
        pass

def check_this_item(
    home_item_without_user_dir,
    main_custom_full_location,
    main_item_full_location_dirname,
    home_item_name, 
    home_item_path):
    
    # New item 
    is_a_new_item(
        home_item_without_user_dir,
        main_custom_full_location,
        main_item_full_location_dirname,
        home_item_name, 
        home_item_path)
                
    # Only search inside if destination exist
    if os.path.exists(main_item_full_location_dirname):
        # Has date/time folders
        if has_date_folders:
            search_in_all_date_time_file(
                main_item_full_location_dirname,
                home_item_name, 
                home_item_path)
        
        else:
            search_in_main_file(    
                main_item_full_location_dirname,
                home_item_name, 
                home_item_path)

def search_inside_directory(
    home_item_without_user_dir,
    searh_in_dirname,
    home_item_name, 
    home_item_path):

    # Search in destination dirname
    for root, dirs, files in os.walk(searh_in_dirname):
        # Ignore empty list
        if files:
            # Found a match with names from backup folder and home 
            if files[0] in home_item_path:
                file_full_location = searh_in_dirname + '/' + files[0]
                # Check home item path with backup item path
                if (get_item_size(home_item_path) > get_item_size(file_full_location) 
                    or
                    get_item_size(home_item_path) < get_item_size(file_full_location)):
                    
                    # File size has changed
                    add_to_backup_dict(
                        home_item_without_user_dir,
                        home_item_name,
                        home_item_path,
                        'UPDATED')
     
def is_a_new_item(
    home_item_without_user_dir,
    main_custom_full_location,
    main_item_full_location_dirname,
    home_item_name, 
    home_item_path):

    # Backup to Main
    if not os.path.exists(main_custom_full_location):
        # Add the new item
        backup_to_main(home_item_name, home_item_path)

def backup_to_main(home_item_name, home_item_path):
    # New item
    add_to_backup_dict(home_item_name, home_item_path, 'NEW')

async def write_to_file():
    # Write file and folder information to the output file
    with open(MAIN_INI_FILE.include_to_backup(), "w") as f:
        for home_item_name, info in items_to_backup_dict.items():
            home_item_path = info['location']
            status = info['status']

            f.write(f"Filename: {home_item_name}\n")
            f.write(f"Size: {info['size']} bytes\n")
            f.write(f"Location: {home_item_path}\n")
            f.write(f"Status: {status}\n")
            f.write("\n")

def search_in_all_date_time_file(
    main_item_full_location_dirname,
    home_item_name, 
    home_item_path):

    # List of all not found item in date/time
    list_of_not_found_in_date_time = []
    
    # List of all not found item in date/time
    list_of_found_in_date_time = []

    # Loop through each date folder
    for date_path in os.listdir(MAIN_INI_FILE.backup_dates_location()):
        if not date_path.startswith('.'):
            date_path = os.path.join(MAIN_INI_FILE.backup_dates_location(), date_path)

            # Loop through each time folder in the current date folder
            for time_folder in os.listdir(date_path):
                time_path = os.path.join(date_path, time_folder)

                # if os.path.exists(main_item_full_location_dirname):

                # Loop through the files in the current time folder
                for root, _, files in os.walk(time_path):
                    # Has files inside
                    if files:
                        for file in files:
                            dst_date_time_path = os.path.join(root, file)
                            relative_path = os.path.relpath(
                                dst_date_time_path, time_path)
                            
                            # print(files)
                            # print(home_item_name)
                            # print(home_item_path)
                            # print(dst_date_time_path)
                            # print(time_path)
                            # print(relative_path)
                            # print()

                            # Match found in date/time folder
                            if home_item_name == file:
                                # Add to found list
                                list_of_found_in_date_time.append(
                                    home_item_name)
                                
                                # Compare itens sizes
                                get_item_diff(    
                                    dst_date_time_path,
                                    home_item_name,
                                    home_item_path)
                            
                            else:
                                # Filter item
                                if (
                                    home_item_path 
                                    not in 
                                    list_of_not_found_in_date_time
                                    and 
                                    home_item_name
                                    not in 
                                    list_of_found_in_date_time):
                                    list_of_not_found_in_date_time.append(
                                        home_item_path)
    
    # print(list_of_not_found_in_date_time)
    # Search not found files in main folder
    if list_of_not_found_in_date_time:
        search_in_main_file(    
            main_item_full_location_dirname,
            home_item_name, 
            home_item_path)

def search_in_main_file(
    main_item_full_location_dirname,
    home_item_name, 
    home_item_path):

    # Loop through the files in the main folder
    for root, _, files in os.walk(
        main_item_full_location_dirname):
        
        # Has files inside
        if files:
            for main_file in files:
                dst_main_path = os.path.join(root, main_file)

                # Match found in main folder
                if home_item_name == main_file:
                    # Compare itens sizes
                    get_item_diff(    
                        dst_main_path,
                        home_item_name,
                        home_item_path)
                        
def get_item_diff(
    dst_path,
    home_item_name,
    home_item_path):
    
    # Destination exist
    if os.path.exists(dst_path):
        # Compare item from home -> item from .main bakckup
        if (get_item_size(home_item_path) != get_item_size(dst_path)): 
            # Backup to date/time
            add_to_backup_dict(
                home_item_name,
                home_item_path,
                'UPDATED')

def add_to_backup_dict(
    home_item_name,
    home_item_path,
    status):
    print('Added:')
    print(f"        -Filename : {home_item_name}")
    print(f"        -Location : {home_item_path}")
    print(f"        -Status   : {status}")
    print()
    
    # Add item to dict
    items_to_backup_dict[home_item_name] = {
        "size": get_item_size(home_item_path),
        "location": home_item_path,
        "status": status
    }

def add_to_home_dict(home_item_name, home_item_path):
    # Store item information in the dictionary, to check they size
    backup_home_dict[home_item_name] = {
        "size": get_item_size(home_item_path),
        "location": home_item_path
    }


class Analyse:
    def get_source_dir(self):
        source_folders = [] 
        
        # HOME folders selected by user
        for item in get_folders():
            # Handle spaces
            item = handle_spaces(item)

            source_folders.append(f'{HOME_USER}/{item}')
        
        # For GNOME
        if get_user_de() == 'gnome':
            # Hidden folder .local/share/
            for item in os.listdir(f"{HOME_USER}/.local/share/"):
                # Handle spaces
                item = handle_spaces(item)
                
                if item in list_gnome_include:
                    try:
                        source_folders.append(f'{HOME_USER}/.local/share/{item}')
                    except:
                        pass
                
            # Hidden folder .config/
            for item in os.listdir(f"{HOME_USER}/.config/"):
                # Handle spaces
                item = handle_spaces(item)

                if item in list_gnome_include:
                    try:
                        source_folders.append(f'{HOME_USER}/.config/{item}')
                    except:
                        pass
                    
        # For KDE
        elif get_user_de() == 'kde':
            # Hidden folder .local/share/
            for item in os.listdir(f"{HOME_USER}/.local/share/"):
                # Handle spaces
                item = handle_spaces(item)
                
                if item in list_kde_include:
                    source_folders.append(f'{HOME_USER}/.local/share/')
            
            # Hidden folder .config/
            for item in os.listdir(f"{HOME_USER}/.config/"):
                # Handle spaces
                item = handle_spaces(item)

                if item in list_kde_include:
                    source_folders.append(f'{HOME_USER}/.config/')
        
        return source_folders

    async def get_select_backup_home(self):
        counter = 0
        counter_limit = 0

        try:
            # Loop through items in the source directory
            for counter_limit in range(len(self.get_source_dir())):
                counter_limit = counter_limit

            try:
                # Run loop through list
                for _ in range(counter_limit):
                    for home_item_name in os.listdir(self.get_source_dir()[counter]):

                        #  Item path
                        home_item_path = os.path.join(
                            self.get_source_dir()[counter], home_item_name)
                        
                        # Detect home hidden files
                        detect_home_hidden_files = str(home_item_path).replace(
                            f'{HOME_USER}/', ' ').strip()

                        # For hidden HOME files
                        if str(detect_home_hidden_files).startswith('.'):
                            # For Gnome
                            if get_user_de() == 'gnome':    
                                if detect_home_hidden_files in list_gnome_include:
                                    add_to_home_dict(home_item_name, home_item_path)
                            # For gnome
                            elif get_user_de() == 'kde':
                                if detect_home_hidden_files in list_kde_include:
                                    add_to_home_dict(home_item_name, home_item_path)

                        else:
                            add_to_home_dict(home_item_name, home_item_path)

                    counter += 1

            except IndexError:
                pass

        except FileNotFoundError:
            pass

    async def need_to_backup_analyse(self):
        await self.get_select_backup_home() 
        await run_algo()
        await write_to_file()

        # # Set todays date to DB to the 'Checked date for backup'
        # latest_checked_date = MAIN_INI_FILE.set_database_value(
        #     'INFO', 'checked_backup_date', today_date())

        # print('Latest checked date:', today_date())

        # If number of item > 0
        if number_of_item_to_backup() > 0:
            print(GREEN + 'ANALYSE: Need to backup.' + RESET)
            return True 
        
        else:
            print(YELLOW + 'ANALYSE: No need to backup.' + RESET)
            return False


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    MAIN = Analyse()

    # print(asyncio.run(MAIN.need_to_backup_analyse()))

    # Start analyses
    if asyncio.run(MAIN.need_to_backup_analyse()):
        # Prepare backup
        if may_continue_to_backup():
            # Backup now
            sub.Popen(
                ["python3", SRC_BACKUP_NOW_PY], 
                    stdout=sub.PIPE, stderr=sub.PIPE)

            # Exit
            exit()
