from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def get_wallpaper_full_location():
    # Detect color scheme
    get_color_scheme = os.popen(DETECT_THEME_MODE).read().strip().replace("'", "")
        
    # Check if user DE is in the supported list
    counter = 0
    # TODO
    # Maybe re-code this
    for _ in SUPPORT_OS:
        if SUPPORT_OS[counter] == MAIN_INI_FILE.get_database_value('INFO', 'os'):
            # Light theme
            if get_color_scheme == "prefer-light":
                # Get current wallpaper
                wallpaper = os.popen(GET_GNOME_WALLPAPER).read().strip().replace("file://", "").replace("'", "")
            else:
                # Get current wallpaper (Dark)
                wallpaper = os.popen(GET_GNOME_WALLPAPER_DARK).read().strip().replace("file://", "").replace("'", "")
            
            # If it has comma
            if "," in wallpaper:
                wallpaper = str(wallpaper.replace(",", "\, "))
            # Remove spaces if exist
            elif " " in wallpaper:
                wallpaper = str(wallpaper.replace(" ", "\ "))
                
            # Remove / at the end if exist
            if wallpaper.endswith("/"):
                wallpaper = str(wallpaper.rsplit("/", 1))
                wallpaper = "".join(str(wallpaper))
                wallpaper = str(wallpaper.strip().replace("[", "").replace("'", ""))
                wallpaper = str(wallpaper.replace("]", "").replace(",", ""))
            
            # Return wallpaper full location
            return wallpaper

        elif MAIN_INI_FILE.get_database_value('INFO', 'os') == "kde":
            one_more_loop = False
            
            with open(f"{HOME_USER}/.config/plasma-org.kde.plasma.desktop-appletsrc", "r") as file:
                # Strips the newline character
                for wallpaper in file.readlines():
                    wallpaper = wallpaper.strip()

                    if one_more_loop:
                        wallpaper = wallpaper.replace("Image=", "").replace("file://", "")

                        if " " in wallpaper:
                            # Return wallpaper full location
                            return wallpaper.replace(' ', '\ ')
                        else:
                            return wallpaper

                    if wallpaper == "[Containments][1][Wallpaper][org.kde.image][General]" and not one_more_loop:
                        one_more_loop=True
        else:
            counter +=1

    return None

if __name__ == '__main__':
    pass