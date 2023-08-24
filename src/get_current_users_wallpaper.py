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
    for counter in range(len(SUPPORT_OS)):
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
            # Go in loop one more time, and exit
            one_more_loop = False
            
            # Search wallaper inside plasma-org.kde.plasma.desktop-appletsrc
            with open(f"{HOME_USER}/.config/plasma-org.kde.plasma.desktop-appletsrc", "r") as file:
                # Strips the newline character
                for wallpaper in file.readlines():
                    wallpaper = wallpaper.strip()

                    if one_more_loop:
                        wallpaper = wallpaper.replace("Image=", "").replace("file://", "")

                        # Handle spaces
                        wallpaper = handle_spaces(wallpaper)
                        # Return wallpapers full location
                        return wallpaper

                    if wallpaper == "[Containments][1][Wallpaper][org.kde.image][General]" and not one_more_loop:
                        one_more_loop = True

    # No compatibility found, return None
    return None


if __name__ == '__main__':
    pass