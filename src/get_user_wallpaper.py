from setup import *
from read_ini_file import UPDATEINIFILE

def user_wallpaper():
    mainIniFile = UPDATEINIFILE()

    ################################################################################
    # Detect color scheme
    ################################################################################
    getColorScheme = os.popen(detectThemeMode)
    getColorScheme = getColorScheme.read().strip().replace("'", "")
        
    # Check if user DE is in the supported list
    count = 0
    for _ in supportedOS:
        if supportedOS[count] == str(mainIniFile.ini_user_os()):
            # Light theme
            if getColorScheme == "prefer-light":
                # Get current wallpaper
                getWallpaper = os.popen(getGnomeWallpaper)
                getWallpaper = getWallpaper.read().strip().replace("file://", "").replace("'", "")
            
            else:
                # Get current wallpaper (Dark)
                getWallpaper = os.popen(getGnomeWallpaperDark)
                getWallpaper = getWallpaper.read().strip().replace("file://", "").replace("'", "")
        
            # If it has comma
            if "," in getWallpaper:
                getWallpaper = str(getWallpaper.replace(",", "\, "))
            
            # Remove spaces if exist
            if " " in getWallpaper:
                getWallpaper = str(getWallpaper.replace(" ", "\ "))
            
            # Remove / at the end if exist
            if getWallpaper.endswith("/"):
                getWallpaper = str(getWallpaper.rsplit("/", 1))
                getWallpaper = "".join(str(getWallpaper))
                getWallpaper = str(getWallpaper.strip().replace("[", "").replace("'", ""))
                getWallpaper = str(getWallpaper.replace("]", "").replace(",", ""))
            
            # After one supported item was found, go to backup_user_wallpaper()
            return getWallpaper

        elif str(mainIniFile.ini_user_os()) == "kde":
            oneMore = False
            with open(f"{homeUser}/.config/plasma-org.kde.plasma.desktop-appletsrc", "r") as file:
                file = file.readlines()
                # Strips the newline character
                for line in file:
                    line = line.strip()
                    if oneMore:
                        line = line.replace("Image=", "").replace("file://", "")
                        getWallpaper = str(line)
                        # After one supported item was found, go to backup_user_wallpaper()
                        return getWallpaper

                    if line == "[Containments][1][Wallpaper][org.kde.image][General]" and not oneMore:
                        oneMore = True

        else:
            count += 1

