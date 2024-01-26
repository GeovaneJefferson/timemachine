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

# Define a function to convert the date string to a datetime object
def convert_to_datetime(date_str):
    return datetime.strptime(date_str, '%y-%m-%d')

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
        add_to_backup_dict(
            item_name, 
            item_path, 
            'NEW')
            
    # Work with date/time backup folder
    if all_dates_list:
        # Check if custom dst exists
        if os.path.exists(dst_full_location):
            # Dir has been updated at size
            if get_item_diff(
                item_path,
                dst_full_location):

                # Search in date/time folder(s)
                search_in_all_date_time_file(
                    item_name, 
                    item_path,
                    main_custom_full_location)

    else:
        # Is a dir
        if os.path.isdir(item_path):
            # Check if custom dst exists
            if os.path.exists(dst_full_location):
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
            # Check if custom dst exists
            if os.path.exists(dst_full_location):
                    
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
        # TODO
        # RE_CODE THIS!!!
        if files:
            for item_name in files:
                file_full_location = os.path.join(root, item_name)

                short_dst_loc = os.path.dirname(file_full_location)
                short_dst_loc = str(short_dst_loc).replace(HOME_USER, '')
                short_dst_loc = short_dst_loc.split('/')[3:]
                short_dst_loc = ('/').join(short_dst_loc) + '/'

                # Compare sizes
                if get_item_diff(
                    file_full_location,
                    main_custom_full_location + '/' + short_dst_loc + item_name):
                    
                    # Item has been updated
                    add_to_backup_dict(
                        item_name, 
                        os.path.join(item_path, short_dst_loc), 
                        'UPDATED')

                # Exclude invalid location, like: '/car.fbx'
                if short_dst_loc != '/':
                    # Backup destination full location
                    dst_backup_full_location = os.path.join(
                        main_custom_full_location, short_dst_loc, item_name)
                    
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
    
    # Reverse all dates list, so the latest appears first
    # all_dates_list.reverse()

    # Sort the dates in descending order using the converted datetime objects
    sorted_date = sorted(all_dates_list,
                key=convert_to_datetime,
                reverse=True)

    # Loop through each date folder
    for i in range(len(sorted_date)):
        # Get date path
        date_path = (MAIN_INI_FILE.backup_dates_location() 
            + '/' 
            + sorted_date[i])

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

                        relative_path = os.path.relpath(
                            dst_date_time_path, time_path)
                
                        y = os.path.join(HOME_USER, dst_date_time_path).split('/')[:-1]
                        check_path = '/'.join(y)

                        # Is a dir
                        if os.path.isdir(check_path):
                            # Search in dir
                            search_in_dir(
                                check_path, 
                                dst_date_time_path, 
                                item_name,
                                item_path)

                        else:
                            # Match found in date/time folder
                            if item_name == file:
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
                                # Search in man in backup folder
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

def search_in_dir(
        dir_path, 
        dst_date_time_path, 
        dir_name,
        item_path):
    
    # search in dir
    for root, _, files in os.walk(item_path):
        # Has files inside
        if files:   
            for file in files:
                # Find match
                dst_date_time_file_name = str(dst_date_time_path).split('/')[-1]
                if dst_date_time_file_name == file:
                    print('Dir:', dir_name)
                    print('filename:', file)
                    print('Root, Filename:', os.path.join(root, file))
                    print()
                    
                    # Add to found list
                    if (file not in 
                        list_of_found_in_date_time):

                        list_of_found_in_date_time.append(
                            file)
                        
                        file_full_home_location = os.path.join(root, file)

                        extracted_last_dir = os.path.dirname(file_full_home_location)
                        extracted_last_dir = str(extracted_last_dir).replace(HOME_USER, '')
                        extracted_last_dir = extracted_last_dir.split('/')[3:]
                        extracted_last_dir = ('/').join(extracted_last_dir) + '/'

                        # # Compare sizes
                        # if get_item_diff(
                        #     file_full_home_location,
                        #     dst_date_time_file_name + '/' + extracted_last_dir + file):
                        
                        # DATES

                        # HOME
                        # Compare itens sizes
                        if get_item_diff(
                            # item_path,
                            file_full_home_location,
                            dst_date_time_path):
                            
                            # Get file dir location
                            extracted_file_dir = str(file_full_home_location).split('/')[:-1]
                            extracted_file_dir = '/'.join(extracted_file_dir)

                            # Item has been updated
                            add_to_backup_dict(
                                file, 
                                # Send only the files dir
                                extracted_file_dir,
                                # os.path.join(item_path, extracted_last_dir), 
                                'UPDATED')

def add_to_home_dict(item_name, item_path):
    # Store item information in the dictionary, to check they size
    backup_home_dict[item_name] = {
        "size": get_item_size(item_path),
        "location": item_path
        }

def get_item_diff(home_item_size, dst_item_size):
    # Compare item from home -> item from .main bakckup
    if (get_item_size(home_item_size) != get_item_size(dst_item_size)): 
        # print()
        # print(home_item_size)
        # print(dst_item_size)
        # print(get_item_size(home_item_size))
        # print(get_item_size(dst_item_size))
        return True
    
    else:
        return False

def add_to_backup_dict(item_name, item_path, status):
    destination = item_path.replace(HOME_USER, '')
    
    # Analysing right now
    notification_message(
        f'Analysing: {item_name}' )

    if os.path.isdir(item_path):
        # Ignore if dir is empty
        if any(os.scandir(item_path)):
            # Add item to dict
            items_to_backup_dict[item_name] = {
                "size": get_item_size(item_path),
                "location": item_path,
                "destination": destination,
                "status": status
                }
            
            print('Added:')
            print(f"        -Filename : {item_name}")
            print(f"        -Location : {item_path}")
            print(f"        -Destinat.: {destination}")
            print(f"        -Status   : {status}")
            print()

        else:
            # Dir is empty
            print(item_path, "is empty. So it won't be back up.")

    else:
        # Add item to dict
        items_to_backup_dict[item_name] = {
            "size": get_item_size(item_path),
            "location": item_path,
            "destination": destination,
            "status": status
            }
        
        print('Added:')
        print(f"        -Filename : {item_name}")
        print(f"        -Location : {item_path}")
        print(f"        -Destinat.: {destination}")
        print(f"        -Status   : {status}")
        print()
    

    # Write to file
    write_to_file()

def write_to_file():
    # Write file and folder information to the output file
    with open(MAIN_INI_FILE.include_to_backup(), "w") as f:
        for item_name, info in items_to_backup_dict.items():
            item_path = info['location']
            destination = info['destination']
            status = info['status']

            f.write(f"Filename: {item_name}\n")
            f.write(f"Size: {info['size']} bytes\n")
            f.write(f"Location: {item_path}\n")
            f.write(f"Destination: {destination}\n")
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
    # Create main backup folder
    if not os.path.exists(MAIN_INI_FILE.main_backup_folder()):
        sub.run(
            ['mkdir', MAIN_INI_FILE.main_backup_folder()], 
            stdout=sub.PIPE, 
            stderr=sub.PIPE)
    
    # First backup to main backup folder
    if os.path.exists(MAIN_INI_FILE.main_backup_folder()):
        # Get all backup dates
        get_all_dates()

        get_select_backup_home() 
        
        loop_through_home()
        
        # If number of item > 0
        if number_of_item_to_backup() == 0:
            # notification_message(' ')

            print(YELLOW + 'ANALYSE: No need to backup.' + RESET)
            return False

    # Write to file
    write_to_file()

    # Needs to backup
    print(GREEN + 'ANALYSE: Need to backup.' + RESET)
    print('Calling backup now...')
    return True 
    

if __name__ == '__main__':
    # Update notification
    print('Analysing backup...')

    notification_message('Analysing backup...')

    # # Set backing up now to True
    # MAIN_INI_FILE.set_database_value(
    #     'STATUS', 'backing_up_now', 'True') 

    # need_to_backup_analyse()

    # Need to backup
    if need_to_backup_analyse():
        # Prepare backup
        if MAIN_PREPARE.prepare_the_backup():
            print('Calling backup now...')

            # Backup now
            sub.Popen(
                ['python3', SRC_BACKUP_NOW_PY], 
                    stdout=sub.PIPE, 
                    stderr=sub.PIPE).wait()  

    else:
        # Backing up to False
        MAIN_INI_FILE.set_database_value(
            'STATUS', 'backing_up_now', 'False')   

        # Re.open backup checker
        sub.Popen(
            ['python3', SRC_BACKUP_CHECKER_PY], 
            stdout=sub.PIPE, 
            stderr=sub.PIPE).wait()