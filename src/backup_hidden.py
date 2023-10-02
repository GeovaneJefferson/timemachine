from setup import *
from read_ini_file import UPDATEINIFILE
from handle_spaces import handle_spaces
from notification_massage import notification_message

MAIN_INI_FILE = UPDATEINIFILE()

local_share_loc = f'{HOME_USER}/.local/share/'
config_loc = f'{HOME_USER}/.config/'
kde_share_loc = f'{HOME_USER}/.kde/share/'

list_gnome_include = [
    'gnome-shell',
    'dconf'
    ]

# Backup .local/share/ selected folder for KDE
list_include_kde = [
    'kwin',
    'plasma_notes',
    'plasma',
    'aurorae',
    'color-schemes',
    'fonts',
    'kate',
    'kxmlgui5',
    'icons',
    'themes',

    'gtk-3.0',
    'gtk-4.0',
    'kdedefaults',
    'dconf',
    'fontconfig',
    'xsettingsd',
    'dolphinrc',
    'gtkrc',
    'gtkrc-2.0',
    'kdeglobals',
    'kwinrc',
    'plasmarc',
    'plasmarshellrc',
    'kglobalshortcutsrc',
    'khotkeysrc',
    'kwinrulesrc'
    'dolphinrc',
    'ksmserverrc',
    'konsolerc',
    'kscreenlockerrc',
    'plasmashellr',
    'plasma-org.kde.plasma.desktop-appletsrc',
    'plasmarc',
    'kdeglobals',
    
    'gtk-3.0',
    'gtk-4.0',
    'kdedefaults',
    'dconf',
    'fontconfig',
    'xsettingsd',
    'dolphinrc',
    'gtkrc',
    'gtkrc-2.0',
    'kdeglobals',
    'kwinrc',
    'plasmarc',
    'plasmarshellrc',
    'kglobalshortcutsrc',
    'khotkeysrc'
    ]

async def start_backup_hidden_home(user_de):
    # Gnome and KDE
    if user_de == 'gnome' or user_de == 'kde': 
        await backup_hidden_local_share(user_de)
        await backup_hidden_config(user_de)

        # Extra step for kde
        if user_de == 'kde':
            await backup_hidden_kde_share() 

async def backup_hidden_local_share(user_de):
    # Local share
    for folder in os.listdir(local_share_loc):
        # Handle spaces
        folder = handle_spaces(folder)
        
        # Gnome or KDE
        if user_de == 'gnome':
            compare_list = list_gnome_include
            
            # Destination
            dst = MAIN_INI_FILE.gnome_local_share_main_folder() + '/' + folder

        elif user_de == 'kde':
            compare_list = list_include_kde

            # Destination
            dst = MAIN_INI_FILE.kde_local_share_main_folder() + '/' + folder

        # Find match in list
        if folder in compare_list:
            src = local_share_loc + folder
            # dst = MAIN_INI_FILE.main_backup_folder() + '/.local/share/' + folder
            
            # Create current directory in backup device
            dst_moded = dst.split('/')[:-1]  # Remove the last component (file name)
            dst_moded = '/'.join(dst_moded)    # Join components with forward slashes

            if not os.path.exists(dst_moded):
                os.makedirs(dst_moded, exist_ok=True)

            print(f'Backing up: {local_share_loc}{folder}')

            notification_message(f'Backing up: .local/share/{folder}')
            
            sub.run(
                ['cp', '-rvf', src, dst],
                stdout=sub.PIPE,
                stderr=sub.PIPE)

async def backup_hidden_config(user_de):
    # Config
    for folder in os.listdir(config_loc):
        # Handle spaces
        folder = handle_spaces(folder)

        # Adapt for users DE
        if user_de == 'gnome':
            compare_list = list_gnome_include
       
            # Destination
            dst = MAIN_INI_FILE.gnome_config_main_folder() + '/' + folder

        elif user_de == 'kde':
            compare_list = list_include_kde

            # Destination
            dst = MAIN_INI_FILE.kde_config_main_folder() + '/' + folder

        if folder in compare_list:
            src = config_loc + folder
            # dst = MAIN_INI_FILE.main_backup_folder() + '/.config/' + folder
            
            # Create current directory in backup device
            dst_moded = dst.split('/')[:-1]  # Remove the last component (file name)
            dst_moded = '/'.join(dst_moded)    # Join components with forward slashes

            if not os.path.exists(dst_moded):
                os.makedirs(dst_moded, exist_ok=True)

            print(f'Backing up: {config_loc}{folder}')
            
            notification_message(f'Backing up: .config/{folder}')
            
            sub.run(
                ['cp', '-rvf', src, dst],
                stdout=sub.PIPE,
                stderr=sub.PIPE)
            
async def backup_hidden_kde_share():
    try:
        # .kde/share/
        for folder in os.listdir(kde_share_loc):
            # Handle spaces
            folder = handle_spaces(folder)
        
            src = kde_share_loc + folder
            # dst = MAIN_INI_FILE.main_backup_folder() + '/.kde/share/' + folder
            
            # Destination
            dst = MAIN_INI_FILE.kde_share_config_main_folder() + '/' + folder

            # Create current directory in backup device
            dst_moded = dst.split('/')[:-1]  # Remove the last component (file name)
            dst_moded = '/'.join(dst_moded)    # Join components with forward slashes
            
            if not os.path.exists(dst_moded):
                os.makedirs(dst_moded, exist_ok=True)

            print(f'Backing up: {kde_share_loc}{folder}')
            
            notification_message(f'Backing up: .kde/share/{folder}')
            
            sub.run(
                ['cp', '-rvf', src, dst],
                stdout=sub.PIPE,
                stderr=sub.PIPE)
                
    except FileNotFoundError as e:
        print(e)
        pass


if __name__ == '__main__':
    pass