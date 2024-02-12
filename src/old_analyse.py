from setup import *
from get_folders_to_be_backup import get_folders
from handle_spaces import handle_spaces
from get_sizes import number_of_item_to_backup, get_item_size
from get_users_de import get_user_de
from prepare_backup import PREPAREBACKUP
from prepare_backup import create_base_folders
from notification_massage import notification_message
from read_ini_file import UPDATEINIFILE
from backup_flatpak import backup_flatpak
from backup_pip_packages import backup_pip_packages
from backup_wallpaper import backup_wallpaper
from backup_now import list_include_kde, list_gnome_include

MAIN_INI_FILE = UPDATEINIFILE()
MAIN_PREPARE = PREPAREBACKUP()

backup_home_dict = {}
items_to_backup_dict = {}

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
has_date_time_to_compare = []

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
            has_date_time_to_compare.append(date)

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

            extracted_item_dirname = os.path.dirname(item_path)
            extracted_item_dirname = str(extracted_item_dirname).replace(HOME_USER, '')
            extracted_item_dirname = extracted_item_dirname.split('/')[3:]
            extracted_item_dirname = ('/').join(extracted_item_dirname) + '/'
            
            # Has date/time folder(s)
            if has_date_time_to_compare:
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
        file_full_home_location,
        item_home_dirname,    
        dst_full_location,  # Can be to main or date/time folder
        combined_home_with_backup_location):  
    
    # Process
    '''
    1 - Check the item
        - Is a new file/folder?
            True:
                - Send to Main backup folder
            False:
                - Has at least a backup date/time to compare to?
                    True:
                        - Compare file/folder sizes (Home <-> Latest backup folder (date/time))
                        - Has changed?
                            True:
                                - Search inside for the updates
                                    Compare with Main Backup Folder
                                    - Is a new file/folder?
                                        True:
                                            - Send to Main backup folder
                                        False:
                                            - Compare file/folder sizes (Home <-> Latest backup folder (date/time))
                                    
                                    Compare with Latest Backup date/time
                                    - Has changed?
                                        - True: Send to a new date/time backup folder

    '''
    # Check for a new dir or file
    # This will not check inside a dir for update
    # if is_new_item(combined_home_with_backup_location):
    #     # Add to backup to main
    #     add_to_backup_dict(
    #         item_name, 
    #         file_full_home_location, 
    #         'NEW')

    # Has a backup to compare to (With date/time folder)
    if has_date_time_to_compare:
        # Combined Home + Main backup location exist
        if os.path.exists(combined_home_with_backup_location):
            # Check file size diff
            if get_item_diff(
                file_full_home_location,
                combined_home_with_backup_location):

                # Search in main backup dir
                search_in_main_dir(
                    item_name, 
                    file_full_home_location,
                    dst_full_location)
                
                # Check this diff file with a previous date/time backup
                search_in_all_date_time_file(
                    item_name, 
                    file_full_home_location,
                    combined_home_with_backup_location)
    else:
        # Is a dir
        if os.path.isdir(file_full_home_location):
            # Check if custom dst exists
            # if os.path.exists(dst_full_location):
            # Dir has been updated at size
            if get_item_diff(
                file_full_home_location,
                dst_full_location):
            
                # Search in the current dir
                search_in_main_dir(
                    item_name, 
                    file_full_home_location,
                    dst_full_location)
        
        else:
            # Check if custom dst exists
            # if os.path.exists(dst_full_location):
                
            # File has been updated at size
            if get_item_diff(
                file_full_home_location,
                dst_full_location):
            
                # Item has been updated
                add_to_backup_dict(
                    item_name, file_full_home_location, 'UPDATED')
      
def is_new_item(item_full_location):
    # Check if item location in backup exist
    if not os.path.exists(item_full_location):
        return True
    else:
        return False

def search_in_main_dir(
        item_name, 
        item_path,
        main_custom_full_location):

    # Loop through the files to find updates
    for root, _, files in os.walk(item_path):
        if files:
            for item_name in files:
                home_item_full_location = os.path.join(root, item_name)

                extracted_item_dirname = os.path.dirname(home_item_full_location)
                extracted_item_dirname = str(extracted_item_dirname).replace(HOME_USER, '')
                extracted_item_dirname = extracted_item_dirname.split('/')[3:]
                extracted_item_dirname = ('/').join(extracted_item_dirname) + '/'
                
                # Exclude invalid location, like: '/car.fbx'
                if extracted_item_dirname != '/':
                    # Backup destination full location
                    combined_home_with_backup_location = os.path.join(
                        main_custom_full_location, extracted_item_dirname, item_name)
                    
                    # Is a new item
                    if is_new_item(combined_home_with_backup_location):
                        add_to_backup_dict(
                            item_name, 
                            os.path.dirname(home_item_full_location), 
                            'NEW')
                    else:
                        # Compare sizes: Backup file with the Home file
                        if get_item_diff(
                            home_item_full_location,
                            main_custom_full_location + '/' + extracted_item_dirname + item_name):
                            
                            # Item has been updated
                            add_to_backup_dict(
                                item_name, 
                                os.path.join(item_path, extracted_item_dirname), 
                                'UPDATED')

def search_in_all_date_time_file(
        item_name, 
        item_path, 
        main_custom_full_location):

    # Sort the dates in descending order using the converted datetime objects
    sorted_date = sorted(has_date_time_to_compare,
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
                                # Compare itens sizes
                                if get_item_diff(
                                    item_path,
                                    dst_date_time_path):
                                    
                                    # Item has been updated
                                    add_to_backup_dict(
                                        item_name, 
                                        item_path, 
                                        'UPDATED')
                        
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
                    # Add to found list
                    file_full_home_location = os.path.join(root, file)

                    extracted_last_dir = os.path.dirname(file_full_home_location)
                    extracted_last_dir = str(extracted_last_dir).replace(HOME_USER, '')
                    extracted_last_dir = extracted_last_dir.split('/')[3:]
                    extracted_last_dir = ('/').join(extracted_last_dir) + '/'

                    # HOME
                    # Compare itens sizes
                    if get_item_diff(
                        # item_path,
                        file_full_home_location,
                        dst_date_time_path):
                        
                        # # Get file dir location
                        # extracted_file_dir = str(file_full_home_location).split('/')[:-1]
                        # extracted_file_dir = '/'.join(extracted_file_dir)

                        # Get file dir location
                        extracted_file_dir = os.path.dirname(file_full_home_location)

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
            
            # print('Added:')
            # print(f"        -Filename : {item_name}")
            # print(f"        -Location : {item_path}")
            # print(f"        -Destinat.: {destination}")
            # print(f"        -Status   : {status}")
            # print()
    else:
        # Add item to dict
        items_to_backup_dict[item_name] = {
            "size": get_item_size(item_path),
            "location": item_path,
            "destination": destination,
            "status": status
            }
        
        # print('Added:')
        # print(f"        -Filename : {item_name}")
        # print(f"        -Location : {item_path}")
        # print(f"        -Destinat.: {destination}")
        # print(f"        -Status   : {status}")
        # print()

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
            
            if item in list_include_kde:
                source_folders.append(f'{HOME_USER}/.local/share/')
        
        # Hidden folder .config/
        for item in os.listdir(f"{HOME_USER}/.config/"):
            # Handle spaces
            item = handle_spaces(item)

            if item in list_include_kde:
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

                    # # Detect home hidden files
                    # detect_home_hidden_files = str(item_path).replace(
                    #     f'{HOME_USER}/', ' ').strip()

                    # # For hidden HOME files
                    # if str(detect_home_hidden_files).startswith('.'):
                    #     # For Gnome
                    #     if get_user_de() == 'gnome' or get_user_de() == 'kde' or get_user_de() == 'unity':    
                    #         if detect_home_hidden_files in list_gnome_include or \
                    #             detect_home_hidden_files in list_include_kde:
                    #             add_to_home_dict(
                    #                 item_name, 
                    #                 item_path)

                    # else:
                    #     add_to_home_dict(
                    #         item_name, 
                    #         item_path)
                    
                    add_to_home_dict(
                            item_name, 
                            item_path)
                
                counter += 1

        except IndexError:
            pass

    except FileNotFoundError:
        pass

def need_to_backup_analyse():
    # Not the first backup with Time Machine
    if os.path.exists(MAIN_INI_FILE.main_backup_folder()):        
        get_all_dates()
        get_select_backup_home() 
        loop_through_home()
        
        # If number of item > 0
        if number_of_item_to_backup() == 0:
            # notification_message(' ')

            print(YELLOW + 'ANALYSE: No need to backup.' + RESET)
            return False
        else:
            # Write to file
            write_to_file()

            # Needs to backup
            print(GREEN + 'ANALYSE: Need to backup.' + RESET)
            print('Calling backup now...')
            return True 
    
    else:
        # Make first backup
        print(GREEN + 'ANALYSE: Making first backup.' + RESET)
        print('Calling backup now...')
        return True

def is_process_running(process_title):
    try:
        result = sub.run(
            ['pgrep', '-f', process_title],
            check=True,
            stdout=sub.PIPE)
        return bool(result.stdout.strip())
    except sub.CalledProcessError:
        return False

# Update notification
print('Analysing backup...')

notification_message('Analysing backup...')

need_to_backup_analyse()

# try:
#     # Backup flatpak
#     print("Backing up: flatpak applications")
#     backup_flatpak()
    
#     # Backup pip packages
#     print("Backing up: pip packages")
#     backup_pip_packages()
    
#     # Backup wallpaper
#     print("Backing up: Wallpaper")
#     backup_wallpaper()
    
#     # Need to backup
#     if need_to_backup_analyse():
#         # Prepare backup
#         if MAIN_PREPARE.prepare_the_backup():
#             print('Calling backup now...')

#             # Backup now
#             sub.Popen(
#                 ['python3', SRC_BACKUP_NOW_PY], 
#                     stdout=sub.PIPE, 
#                     stderr=sub.PIPE)  
#     else:
#         print('No need to back up.')

#         # Backing up to False
#         MAIN_INI_FILE.set_database_value(
#             'STATUS', 'backing_up_now', 'False')  
        
#         # Check if backup checker is not already running  
#         process_title = "Time Machine - Backup Checker"
#         if not is_process_running(process_title):
#             print(f"No process with the title '{process_title}' is currently running.")
#             # Re.open backup checker
#             sub.Popen(
#                 ['python3', SRC_BACKUP_CHECKER_PY], 
#                 stdout=sub.PIPE, 
#                 stderr=sub.PIPE)
# except Exception as e:
#     # Save error log
#     MAIN_INI_FILE.report_error(e)