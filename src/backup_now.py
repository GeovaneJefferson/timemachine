from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de
from get_folders_to_be_backup import get_folders
# from get_flatpaks_folders_size import flatpak_var_list, flatpak_local_list
from notification_massage import notification_message
from handle_spaces import handle_spaces
from get_backup_date import get_backup_date
from get_time import today_date
from backup_status import backup_status
from get_sizes import get_item_size
from get_sizes import number_of_item_to_backup
from backup_hidden import start_backup_hidden_home


# Handle signal
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)
    
#########################################################
# KDE
#########################################################
# KDE cursor
def get_kde_users_cursor_name():
    with open(f"{HOME_USER}/.config/xsettingsd/xsettingsd.conf", "r") as read:
        read = read.readlines()

        for counter in range(len(read)):
            if read[counter].split()[0] == "Gtk/CursorThemeName":
                # Return users cursor name
                return read[counter].split()[1].replace('"','')

# KDE font
def get_kde_users_font_name():
    with open(f"{HOME_USER}/.config/kdeglobals", "r") as read:
        read = read.readlines()

        for counter in range(len(read)):
            if read[counter].startswith("font="):
                # Return users kde font name
                return (read[counter]).strip().split(",")[0].replace("font=","")

# KDE font size
def get_kde_users_font_size():
    with open(f"{HOME_USER}/.config/kdeglobals", "r") as read:
        read = read.readlines()

        for counter in range(len(read)):
            if read[counter].startswith("font="):
                # Return users kde font size
                return (read[counter]).strip().split(",")[1]

# KDE icon
def get_kde_users_icon_name():
    with open(f"{HOME_USER}/.config/xsettingsd/xsettingsd.conf", "r") as read:
        read = read.readlines()
        for counter in range(len(read)):
            if read[counter].split()[0] == "Net/IconThemeName":
                # Return users icon name
                return read[counter].split()[1].replace('"','')

#########################################################
# GNOME
#########################################################
# GTK theme
def get_gtk_users_theme_name():
    user_theme_name = os.popen(GET_USER_THEME_CMD).read().strip().replace("'", "")
    return user_theme_name

# GTK font
def get_gtk_user_font_name():
    user_font_name = os.popen(GET_USER_FONT_CMD).read().replace("'", "")
    user_font_name = " ".join(user_font_name.split())
    return user_font_name

    # def get_user_font():
    #     if get_user_de() == 'kde':
    #         mainFont=FONT()
    #         return  f"{mainFont.get_kde_font()}, {mainFont.get_kde_font_size()}"

    #     else:
    #         userFontName=os.popen(getUserFontCMD)
    #         userFontName=userFontName.read().replace("'", "")
    #         userFontName=" ".join(userFontName.split())
    #         return userFontName

# GTK icon
def get_gtk_users_icon_name():
    userIconName = os.popen(GET_USER_ICON_CMD).read().strip().replace("'", "")
    return userIconName

# def users_icon_size():
#     try:
#         userIconSize=os.popen(f"du -s {homeUser}/.icons/{users_icon_name()}")
#         userIconSize=userIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.icons/{users_icon_name()}", "").replace("\t", "")
#         userIconSize=int(userIconSize)

#     except ValueError:
#         try:
#             userIconSize=os.popen(f"du -s {homeUser}/.local/share/icons/{users_icon_name()}")
#             userIconSize=userIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.local/share/icons/{users_icon_name()}", "").replace("\t", "")
#             userIconSize=int(userIconSize)

#         except ValueError:
#             try:
#                 userIconSize=os.popen(f"du -s /usr/share/icons/{users_icon_name()}")
#                 userIconSize=userIconSize.read().strip("\t").strip("\n").replace(f"/usr/share/icons/{users_icon_name()}", "").replace("\t", "")
#                 userIconSize=int(userIconSize)

#             except ValueError:
#                 return None

#     return userIconSize

# GTK cursor
def get_gtk_users_cursor_name():
    user_cursor_name = os.popen(
        GET_USER_CURSOR_CMD).read().strip().replace("'", "")
    return user_cursor_name
    

class BACKUP:
    async def backup_hidden_home(self):
        # Start backing up hidden files/folder by getting users DE name
        await start_backup_hidden_home(get_user_de())
 
    async def backup_home(self):
        item_minus = 0
        item_sum_size = 0 

        # Check for something inside main folder
        list_of_main_item = []
        for i in os.listdir(MAIN_INI_FILE.main_backup_folder()):
            # Exclude hidden files/folders
            if '.' not in i:
                list_of_main_item.append(i)
                break

        # Main folder is empty
        if not list_of_main_item:
            # Backup home to the main backup folder
            for folder in get_folders():
                folder = handle_spaces(folder)

                # Backup Home folder
                src = HOME_USER + "/" + folder
                dst = MAIN_INI_FILE.main_backup_folder() + '/'
                
                print(f'Backing up: {HOME_USER}/{folder}')
                
                # Add to counters
                item_sum_size += get_item_size(f'{HOME_USER}/{folder}')
                item_minus += 1 

                # Send backup current status to the notification DB
                notification_message(
                    backup_status(
                        item_minus, 
                        item_sum_size, 
                        len(get_folders())))

                sub.run(
                    ['cp', '-rvf', src, dst], 
                        stdout=sub.PIPE, stderr=sub.PIPE)
                
        else:
            # Read the include file and process each item's information
            with open(MAIN_INI_FILE.include_to_backup(), "r") as f:
                lines = f.readlines()
                
                for i in range(0, len(lines), 5):
                    try:
                        # filename = lines[i + 0].split(':')[-1].strip()
                        size_string = lines[i + 1].split(':')[-1].strip()
                        size = int(size_string.split()[0])
                        location = lines[i + 2].split(':')[-1].strip()
                        status = lines[i + 3].split(':')[-1].strip()
                        
                        # Remove home username
                        remove_username = os.path.relpath(location, os.curdir)
                        
                        # Extract location's folder name
                        extracted_folder_name = (
                            os.path.basename(os.path.dirname(remove_username)))

                        ##########################################################
                        # .MAIN BACKUP
                        ##########################################################
                        # Copy to .main backup
                        if status == 'NEW':
                            # Sent to main backup folder
                            destination_location = (
                                f'{MAIN_INI_FILE.main_backup_folder()}/{extracted_folder_name}')
                        
                        ##########################################################
                        # LATEST DATE/TIME
                        ##########################################################
                        elif status == 'UPDATED':
                            # Sent to a new date/time backup folder
                            destination_location = (
                                f'{MAIN_INI_FILE.time_folder_format()}/{extracted_folder_name}')
                        
                        # Create current directory in backup device
                        if not os.path.exists(destination_location):
                            # Create folder
                            os.makedirs(destination_location, exist_ok=True)

                        # Backup file
                        if os.path.isfile(location):
                            print(
                                'Backing up file:', location, 'to', destination_location)
                            
                            # Add to counters
                            item_sum_size += size   # Bytes
                            item_minus += 1 

                            # Send backup current status to the notification DB
                            notification_message(
                                backup_status(
                                    item_minus, 
                                    item_sum_size, 
                                    number_of_item_to_backup()))

                            # Copy files
                            sub.run(
                                ['cp', '-rvf', location, destination_location],
                                stdout=sub.PIPE, 
                                stderr=sub.PIPE)

                        # Backup folder
                        elif os.path.isdir(location):
                            print(
                                'Backing up folder:', location, 'to', destination_location)
                            
                            # Add to counters
                            item_sum_size += size   # Bytes
                            item_minus += 1 

                            # Send backup current status to the notification DB
                            notification_message(
                                backup_status(
                                    item_minus, 
                                    item_sum_size, 
                                    number_of_item_to_backup()))

                            # Backup directories using shutil.copytree()
                            sub.run(
                                ['cp', '-rvf', location, destination_location],
                                stdout=sub.PIPE, 
                                stderr=sub.PIPE)

                        # If only new file/folder was backup, save the backup
                        # date to main folder
                        if MAIN_INI_FILE.oldest_backup_date() is None:
                            # Oldest backup to main
                            MAIN_INI_FILE.set_database_value(
                                'INFO', 'oldest_backup_to_main', today_date())
                        
                            # Latest backup to main
                            MAIN_INI_FILE.set_database_value(
                                'INFO', 'latest_backup_to_main', today_date())
                        
                        else:
                            # Latest backup to main
                            MAIN_INI_FILE.set_database_value(
                                'INFO', 'latest_backup_to_main', today_date())
                            
                    except IndexError:
                        pass

    async def end_backup(self):
        print('Ending backup')

        notification_message('')

        # Write to restore ini file 
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{MAIN_INI_FILE.restore_settings_location()}")
        with open(f"{MAIN_INI_FILE.restore_settings_location()}", 'w') as configfile:
            if not CONFIG.has_section('INFO'):
                CONFIG.add_section('INFO')

            # KDE
            if get_user_de() == 'kde':
                CONFIG.set('INFO', 'icon', f'{get_kde_users_icon_name()}')
                CONFIG.set('INFO', 'cursor', f'{get_kde_users_cursor_name()}')
                CONFIG.set('INFO', 'font', f'{get_kde_users_font_name()}, {get_kde_users_font_size()}')
                CONFIG.set('INFO', 'gtktheme', f'{get_gtk_users_theme_name()}')
                CONFIG.set('INFO', 'theme', f'None')
            
            # GNOME
            else:
                CONFIG.set('INFO', 'icon', f'{get_gtk_users_icon_name()}')
                CONFIG.set('INFO', 'cursor', f'{get_gtk_users_cursor_name()}')
                CONFIG.set('INFO', 'font', f'{get_gtk_user_font_name()}')
                CONFIG.set('INFO', 'gtktheme', f'{get_gtk_users_theme_name()}')
                CONFIG.set('INFO', 'theme', f'None')
                CONFIG.set('INFO', 'colortheme', f'None')

            CONFIG.write(configfile)

        print("Backup is done!")
        print("Sleeping for 60 seconds")
        # Wait x, so if it finish fast, won't repeat the backup
        time.sleep(60)

        # Update DB
        MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
        MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'No')

        # Exit
        exit()

    async def main(self):
        await self.backup_hidden_home()
        await self.backup_home()
        await self.end_backup()


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    main = BACKUP()
    asyncio.run(main.main())