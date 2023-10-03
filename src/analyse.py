from setup import *
from get_folders_to_be_backup import get_folders
from handle_spaces import handle_spaces
from get_sizes import number_of_item_to_backup, get_item_size
from get_users_de import get_user_de
from prepare_backup import PREPAREBACKUP
from notification_massage import notification_message
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()
MAIN_PREPARE = PREPAREBACKUP()

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

# List of all not found item in date/time
list_of_not_found_in_date_time = []

# List of all not found item in date/time
list_of_found_in_date_time = []

pass_dir_list = []

# List of all dates
all_dates_list = []

# List of all times
all_times_list = []

def get_all_dates():
    # Add all dates to the list
    for date in os.listdir(MAIN_INI_FILE.backup_dates_location()):
        # Eclude hidden files/folders
        if not date.startswith('.'):
            all_dates_list.append(date)

def loop_through_home():
    try:                    
        # Source from .main backup folder
        for item_name, info in backup_home_dict.items():
            # Handle spaces
            item_name = handle_spaces(item_name)

            # Home item path
            item_path = info['location']

            # Remove home username location
            home_item_without_user_dir = str(item_path).replace(f'{HOME_USER}/', ' ').strip()
            
            # Only item dirname. Fx. Desktop
            home_item_dirname = os.path.dirname(home_item_without_user_dir)
            
            # Destination/Source full location
            main_custom_full_location = (
                MAIN_INI_FILE.main_backup_folder() + 
                '/' + 
                str(item_path).replace(HOME_USER + '/', ' ').strip()) 
        
            # Destination dirname 
            main_item_full_location_dirname = main_custom_full_location.split(
                '/')[1:-1]
            main_item_full_location_dirname = '/' + ','.join(
                main_item_full_location_dirname).replace(',', '/')
            
            # Item main dir
            item_home_dirname = HOME_USER + '/' + home_item_dirname

            short_dst_loc = os.path.dirname(item_path)
            short_dst_loc = str(short_dst_loc).replace(HOME_USER, '')
            short_dst_loc = short_dst_loc.split('/')[3:]
            short_dst_loc = ('/').join(short_dst_loc) + '/'
       
            # # .directory
            # print('Item name         :', item_name)  
            # # /home/xxx/Dekstop/directory
            # print('Item path         :', item_path)  
            # # Desktop/directory
            # print('Item no dir loc.  :', home_item_without_user_dir)  
            # # /run/media/xxx/Backups/TMB/backups/.main_backups/Desktop/.directory
            # print('Custom dst, src.  :', main_custom_full_location)  
            # # /run/media/xxx/Backups/TMB/backups/.main_backups/Desktop/
            # print('Destination dir. n:', main_item_full_location_dirname)  
            # # Desktop
            # print('Item dirname      :', home_item_dirname)
            # print('Item home dirname :', item_home_dirname)
            # print('Short dst         :', short_dst_loc)
            # print()

            # Has date/time folder(s)
            if all_dates_list:
                check_this_item(
                    item_name,
                    item_path,
                    item_home_dirname,    
                    main_custom_full_location,  # Look inside date/time folder(s)
                    main_custom_full_location)  
            
            else:
                check_this_item(
                    item_name,
                    item_path,
                    item_home_dirname,    
                    main_custom_full_location,  # Look inside main folder
                    main_custom_full_location)  
                
    except FileNotFoundError:
        pass

def check_this_item(
        item_name,
        item_path,
        item_home_dirname,    
        dst_full_location,  # Can be to main or date/time folder
        main_custom_full_location):  
    
    # Is a new item
    if is_new_item(main_custom_full_location):
        # Add to backup to main
        add_to_backup_dict(item_name, item_path, 'NEW')
    
    # Work with date/time backup folder
    if all_dates_list:
        # Search in date/time folder(s)
        search_in_all_date_time_file(
            item_name, 
            item_path,
            main_custom_full_location)

    else:
        # Is a dir
        if os.path.isdir(item_path):
            # Dir has been updated at size
            if get_item_diff(
                item_path,
                dst_full_location):
            
                # Search in the current dir
                search_in_main_dir(
                    item_name, 
                    item_path,
                    dst_full_location)
        
        else:
            # File has been updated at size
            if get_item_diff(
                item_path,
                dst_full_location):
            
                # Item has been updated
                add_to_backup_dict(
                    item_name, item_path, 'UPDATED')
  
def is_new_item(main_custom_full_location):
    # Check if item location in backup exist
    if not os.path.exists(main_custom_full_location):
        return True
    
    else:
        return False

def search_in_main_dir(
    item_name, 
    item_path,
    main_custom_full_location):
    # Loop through the files to find updates
    for root, _, files in os.walk(item_path):
        # Has files inside
        if files:
            for item_name in files:
                file_full_location = os.path.join(root, item_name)

                short_dst_loc = os.path.dirname(file_full_location)
                short_dst_loc = str(short_dst_loc).replace(HOME_USER, '')
                short_dst_loc = short_dst_loc.split('/')[3:]
                short_dst_loc = ('/').join(short_dst_loc) + '/'
       
                # Exclude invalid location, like: '/car.fbx'
                if short_dst_loc != '/':
                    # Backup destination full location
                    dst_backup_full_location = os.path.join(
                        main_custom_full_location, short_dst_loc, item_name)
                    
                    # print(short_dst_loc)
                    # print(item_name)
                    # print(dst_backup_full_location)
                    # print()

                    # Is a new item
                    if is_new_item(dst_backup_full_location):
                        add_to_backup_dict(
                            item_name, 
                            os.path.dirname(file_full_location), 
                            'NEW')

def search_in_all_date_time_file(
    item_name, 
    item_path, 
    main_custom_full_location):
    # Loop through each date folder
    for i in range(len(all_dates_list)):
        # Get date path
        date_path = (MAIN_INI_FILE.backup_dates_location() 
            + '/' 
            + all_dates_list[i])

        # Loop through each time folder in the current date folder
        for time_path in reversed(os.listdir(date_path)):  # Start from the latest time_path folder
            # Get data path + time path, join it
            time_path = os.path.join(date_path + '/' + time_path)
    
            # Loop through the files in the current time folder
            for root, _, files in os.walk(time_path):
                # Has files inside
                if files:
                    for file in files:
                        dst_date_time_path = os.path.join(root, file)

                        # relative_path = os.path.relpath(
                        #     dst_date_time_path, time_path)

                        # Match found in date/time folder
                        if item_name == file:
                            # print('DATE/TIME')
                            # print('Compare   :', file, '->', item_name )
                            # print('Item path :', item_path)
                            # print('D/T path  :', dst_date_time_path)
                            # print('Compare to:', time_path)
                            # print('Rel. path :', relative_path)
                            # print()

                            # Add to found list
                            if (item_name not in 
                                list_of_found_in_date_time):

                                list_of_found_in_date_time.append(
                                    item_name)
                            
                                # Compare itens sizes
                                if get_item_diff(
                                    item_path,
                                    dst_date_time_path):
                                    
                                    # Item has been updated
                                    add_to_backup_dict(
                                        item_name, 
                                        item_path, 
                                        'UPDATED')
                      
                        else:
                            # Search in manin backup folder
                            if (item_path not in 
                                list_of_not_found_in_date_time and 
                                item_name not in 
                                list_of_found_in_date_time):

                                list_of_not_found_in_date_time.append(
                                    item_path)
    
    # Search not found files in main folder
    if list_of_not_found_in_date_time:
        search_in_main_dir(
            item_name, 
            item_path,
            main_custom_full_location)
    
def add_to_home_dict(item_name, item_path):
    # Store item information in the dictionary, to check they size
    backup_home_dict[item_name] = {
        "size": get_item_size(item_path),
        "location": item_path
        }

def get_item_diff(
        item_path,
        dst):
    
    # Compare item from home -> item from .main bakckup
    if (get_item_size(item_path) != get_item_size(dst)): 
        return True
    
    else:
        return False

def add_to_backup_dict(item_name, item_path, status):
    # print('Added:')
    # print(f"        -Filename : {item_name}")
    # print(f"        -Location : {item_path}")
    # print(f"        -Status   : {status}")
    # print()

    # if os.path.isdir(item_path):
    #     # Add item to dict
    #     items_to_backup_dict[item_name] = {
    #         "size": get_item_size(item_path),
    #         "location": item_path + '/' + item_name,
    #         "status": status
    #         }
    
    if os.path.isdir(item_path):
        # Add item to dict
        items_to_backup_dict[item_name] = {
            "size": get_item_size(item_path),
            "location": item_path,
            "status": status
            }
    
    else:
        # Add item to dict
        items_to_backup_dict[item_name] = {
            "size": get_item_size(item_path),
            "location": item_path,
            "status": status
            }
        
    write_to_file()

def write_to_file():
    # Write file and folder information to the output file
    with open(MAIN_INI_FILE.include_to_backup(), "w") as f:
        for item_name, info in items_to_backup_dict.items():
            item_path = info['location']
            status = info['status']

            f.write(f"Filename: {item_name}\n")
            f.write(f"Size: {info['size']} bytes\n")
            f.write(f"Location: {item_path}\n")
            f.write(f"Status: {status}\n")
            f.write("\n")

def get_source_dir():
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

def get_select_backup_home():
    counter = 0
    counter_limit = 0

    try:
        # Loop through items in the source directory
        for counter_limit in range(len(get_source_dir())):
            counter_limit = counter_limit

        try:
            # Run loop through list
            for _ in range(counter_limit):
                for item_name in os.listdir(get_source_dir()[counter]):

                    #  Item path
                    item_path = os.path.join(
                        get_source_dir()[counter], item_name)
                    
                    # Detect home hidden files
                    detect_home_hidden_files = str(item_path).replace(
                        f'{HOME_USER}/', ' ').strip()

                    # For hidden HOME files
                    if str(detect_home_hidden_files).startswith('.'):
                        # For Gnome
                        if get_user_de() == 'gnome':    
                            if detect_home_hidden_files in list_gnome_include:
                                add_to_home_dict(
                                    item_name, 
                                    item_path)

                        # For gnome
                        elif get_user_de() == 'kde':
                            if detect_home_hidden_files in list_kde_include:
                                add_to_home_dict(
                                    item_name, 
                                    item_path)
                                    
                    else:
                        add_to_home_dict(
                            item_name, 
                            item_path)

                counter += 1

        except IndexError:
            pass

    except FileNotFoundError:
        pass

def need_to_backup_analyse():
    # First backup to main backup folder
    if any(os.scandir(MAIN_INI_FILE.main_backup_folder())):
        # Get all backup dates
        get_all_dates()

        get_select_backup_home() 
        
        loop_through_home()
        
        write_to_file()

        # If number of item > 0
        if number_of_item_to_backup() == 0:
            notification_message(' ')

            print(YELLOW + 'ANALYSE: No need to backup.' + RESET)
            return False
    
    # Needs to backup
    print(GREEN + 'ANALYSE: Need to backup.' + RESET)
    print()
    print('Calling backup now...')
    return True 
        

if __name__ == '__main__':
    # Update notification
    print('Analysing backup...')
    notification_message('Analysing backup...')

    # need_to_backup_analyse()

    # Need to backup
    if need_to_backup_analyse():
        # Prepare backup
        if MAIN_PREPARE.prepare_the_backup():
            # Backing up to True
            MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'True') 
            
            print('Calling backup now...')

            # Backup now
            sub.Popen(
                ['python3', SRC_BACKUP_NOW_PY], 
                    stdout=sub.PIPE, 
                    stderr=sub.PIPE)

    else:
        # Backing up to False
        MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')   

        # Re.open backup checker
        sub.Popen(
            ['python3', SRC_BACKUP_CHECKER_PY], 
            stdout=sub.PIPE, 
            stderr=sub.PIPE)