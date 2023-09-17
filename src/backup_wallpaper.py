from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message
from handle_spaces import handle_spaces


MAIN_INI_FILE = UPDATEINIFILE()

def get_wallpaper_full_location():
    # Detect color scheme
    get_color_scheme = os.popen(
        DETECT_THEME_MODE).read().strip().replace("'", "")

    ##################################
    # Compatibility
    ##################################
    ##################################
    # Gnome
    ###################################
    # If users os name is found in DB
    if MAIN_INI_FILE.get_database_value('INFO', 'os') == "gnome":
        # Light theme
        if get_color_scheme == "prefer-light":
            # Get current wallpaper
            wallpaper = os.popen(
                GET_GNOME_WALLPAPER).read().strip().replace(
                    "file://", "").replace("'", "")
            
        else:
            # Get current wallpaper (Dark)
            wallpaper = os.popen(
                GET_GNOME_WALLPAPER_DARK).read().strip().replace(
                    "file://", "").replace("'", "")

        # If exist, remove "/" at the end
        if wallpaper.endswith("/"):
            wallpaper = wallpaper.rsplit("/", 1)
            wallpaper = "".join(wallpaper)
            wallpaper = wallpaper.strip().replace("[", "").replace("'", "")
            wallpaper = wallpaper.replace("]", "").replace(",", "")

        # Handle spaces
        wallpaper = handle_spaces(wallpaper)
        
        # Return wallpapers full location
        return wallpaper
    
    ##################################
    # Kde
    ###################################
    elif MAIN_INI_FILE.get_database_value('INFO', 'os') == "kde":
        
        # Search wallaper inside plasma-org.kde.plasma.desktop-appletsrc
        with open(f"{HOME_USER}/.config/plasma-org.kde.plasma.desktop-appletsrc", "r") as file:
            # Strips the newline character
            for line in file.readlines():
                line = line.strip()

                # Search for
                if line.startswith('Image='):
                    # Replace line
                    line = line.replace('Image=', '')

                    # Remove file://
                    line = line.replace('file://', '')

                    # Handle spaces
                    # line = handle_spaces(line)

                    # Return lines full location
                    return line

async def backup_wallpaper():
    print("Backing up: Wallpaper")

    # GNOME/KDE
    notification_message("Backing up: Wallpaper")

    # Check for at least a wallpaper
    if os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
        for wallpaper in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
            # Delete all wallpapers
            command = f"{MAIN_INI_FILE.wallpaper_main_folder()}/{wallpaper}"
            sub.run(
                ["rm", "-rf", command], 
                stdout=sub.PIPE, 
                stderr=sub.PIPE)

    # Backup wallpaper
    if get_wallpaper_full_location() is not None:
        src = get_wallpaper_full_location()
        dst = MAIN_INI_FILE.wallpaper_main_folder() + "/"
        sub.run(["cp", "-rvf", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)

    # Write to file
    await update_db()

async def update_db():
    CONFIG = configparser.ConfigParser()
    CONFIG.read(MAIN_INI_FILE.restore_settings_location())
    with open(MAIN_INI_FILE.restore_settings_location(), 'w') as configfile:
        if not CONFIG.has_section('INFO'):
            CONFIG.add_section('INFO')

        if get_wallpaper_full_location() is not None:
            CONFIG.set(
                'INFO', 'wallpaper', f'{get_wallpaper_full_location().split("/")[-1]}')
            
            # Write to file
            CONFIG.write(configfile)


if __name__ == '__main__':
    pass
