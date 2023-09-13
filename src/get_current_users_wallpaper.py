from setup import *
from read_ini_file import UPDATEINIFILE
from handle_spaces import handle_spaces


MAIN_INI_FILE = UPDATEINIFILE()


def get_wallpaper_full_location():
    # Detect color scheme
    get_color_scheme = os.popen(DETECT_THEME_MODE).read().strip().replace("'", "")

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
            wallpaper = os.popen(GET_GNOME_WALLPAPER).read().strip().replace("file://", "").replace("'", "")
        else:
            # Get current wallpaper (Dark)
            wallpaper = os.popen(GET_GNOME_WALLPAPER_DARK).read().strip().replace("file://", "").replace("'", "")

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

                    # Handle spaces
                    # line = handle_spaces(line)

                    # Return lines full location
                    return line

    # No compatibility found, return None
    return None


if __name__ == '__main__':
    pass