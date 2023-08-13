from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def user_wallpaper():
    # Detect color scheme
    get_color_scheme = os.popen(DETECT_THEME_MODE).read().strip().replace("'", "")
        
    # Check if user DE is in the supported list
    counter = 0
    for _ in SUPPORT_OS:
        if SUPPORT_OS[counter] == MAIN_INI_FILE.get_database_value('INFO', 'os'):
            # Light theme
            if get_color_scheme == "prefer-light":
                # Get current wallpaper
                get_wallpaper = os.popen(GET_GNOME_WALLPAPER).read().strip().replace("file://", "").replace("'", "")
            
            else:
                # Get current wallpaper (Dark)
                get_wallpaper = os.popen(GET_GNOME_WALLPAPER_DARK).read().strip().replace("file://", "").replace("'", "")
        
            # If it has comma
            if "," in get_wallpaper:
                get_wallpaper = str(get_wallpaper.replace(",", "\, "))
            
            # Remove spaces if exist
            if " " in get_wallpaper:
                get_wallpaper = str(get_wallpaper.replace(" ", "\ "))
            
            # Remove / at the end if exist
            if get_wallpaper.endswith("/"):
                get_wallpaper = str(get_wallpaper.rsplit("/", 1))
                get_wallpaper = "".join(str(get_wallpaper))
                get_wallpaper = str(get_wallpaper.strip().replace("[", "").replace("'", ""))
                get_wallpaper = str(get_wallpaper.replace("]", "").replace(",", ""))
            
            # After one supported item was found, go to backup_user_wallpaper()
            return get_wallpaper

        elif MAIN_INI_FILE.get_database_value('INFO', 'os') == "kde":
            one_more = False
            with open(f"{HOME_USER}/.config/plasma-org.kde.plasma.desktop-appletsrc", "r") as file:
                # Strips the newline character
                for line in file.readlines():
                    line = line.strip()
                    if one_more:
                        line = line.replace("Image=", "").replace("file://", "")
                        get_wallpaper=str(line)

                        # Return the found location wallpaper
                        return get_wallpaper

                    if line == "[Containments][1][Wallpaper][org.kde.image][General]" and not one_more:
                        one_more=True
        else:
            counter += 1


if __name__ == '__main__':
    pass