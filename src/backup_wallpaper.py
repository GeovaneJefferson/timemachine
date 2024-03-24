from setup import *
from read_ini_file import UPDATEINIFILE
from handle_spaces import handle_spaces
from get_users_de import get_user_de


MAIN_INI_FILE = UPDATEINIFILE()

def get_wallpaper_full_location():
    # Detect color scheme
    get_color_scheme = os.popen(
        DETECT_THEME_MODE).read().replace("'", "").strip()
    ## Set XDG_CURRENT_DESKTOP environment variable
    #os.environ['XDG_CURRENT_DESKTOP']

    ## Execute the command and print the output
    #output = os.popen('echo $XDG_CURRENT_DESKTOP').read().strip().lower()

    ##################################
    # Compatibility
    ##################################
    ##################################
    # Gnome
    ###################################
    # If users os name is found in DB
    if 'gnome' in get_user_de() or 'unity' in get_user_de():
        # Light theme
        if get_color_scheme == "prefer-light":
            # Get current wallpaper
            wallpaper = os.popen(
                GET_GNOME_WALLPAPER).read().replace(
                    "file://", "").replace("'", "").strip()
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
    elif 'kde' in get_user_de():
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

def backup_wallpaper():
    wallpaper_folder = MAIN_INI_FILE.wallpaper_main_folder()

    # Get a list of wallpapers in the specified folder
    wallpapers = os.listdir(wallpaper_folder)

    # Check if there are any wallpapers to delete
    if wallpapers:
        # Iterate over each wallpaper and delete it
        for wallpaper in wallpapers:
            wallpaper_path = os.path.join(wallpaper_folder, wallpaper)
            print('Deleting', wallpaper_path)

            # Execute the command to delete the wallpaper
            os.remove(wallpaper_path)

    # Backup wallpaper
    if get_wallpaper_full_location() is not None:
        src = get_wallpaper_full_location()
        dst = MAIN_INI_FILE.wallpaper_main_folder()

        print('Copying', src, dst)
        shutil.copy2(src, dst)

    # Write to file
    update_db()

def update_db():
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
