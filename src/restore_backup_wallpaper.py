from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de

someImageInsideList = []

def restore_backup_wallpaper():
    mainIniFile = UPDATEINIFILE()

    print("Restoring users wallpaper...")
    try:
        # Check if a wallpaper can be found
        for wallpaper in os.listdir(f"{mainIniFile.wallpaper_main_folder()}/"):
            someImageInsideList.append(wallpaper)
        
        # If has a wallpaper to restore and restoreSystemSettings:
        if someImageInsideList: 
            # Create wallpapers folders
            if not os.path.exists(str(mainIniFile.create_base_folder())):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/wallpapers/",shell=True)

            # Copy to wallpapers folders
            for image in os.listdir(f"{mainIniFile.wallpaper_main_folder()}/"):
                sub.run(f"{copyRsyncCMD} {mainIniFile.wallpaper_main_folder()}/{image} {homeUser}/.local/share/wallpapers/", shell=True)

            # Check if user DE is in the supported list to Automatically apply
            ################################################################
            for count in range(len(supportedOS)):
                # Activate wallpaper option
                if supportedOS[count] in str(get_user_de()):
                    # Detect color scheme
                    getColorScheme = os.popen(detectThemeMode)
                    getColorScheme = getColorScheme.read().strip().replace("'", "")
                    
                    # Remove spaces if exist
                    if "," in image:
                        image = str(image.replace(", ", "\, "))
                        
                    # Add \ if it has space
                    if " " in image:
                        image = str(image.replace(" ", "\ "))

                    # Light or Dark wallpaper
                    if getColorScheme == "prefer-light" or getColorScheme == "default":
                        print()
                        print(getColorScheme)
                        print()
                        
                        # Light theme o default
                        print(f"{setGnomeWallpaper} {homeUser}/.local/share/wallpapers/{image}")
                        sub.run(f"{setGnomeWallpaper} {homeUser}/.local/share/wallpapers/{image}", shell=True)
                    else:
                        # Dark theme
                        print(f"{setGnomeWallpaperDark} {homeUser}/.local/share/wallpapers/{image}")
                        sub.run(f"{setGnomeWallpaperDark} {homeUser}/.local/share/wallpapers/{image}", shell=True)

                    # Set wallpaper to Zoom
                    sub.run(f"{zoomGnomeWallpaper}", shell=True)
                    ################################################################

                elif get_user_de() == "kde":
                    print("Restoring users wallpaper (KDE)...")
                    # Apply to KDE desktop
                    os.popen("""
                            dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
                        var Desktops = desktops();
                        for (i=0;i<Desktops.length;i++) {
                                d = Desktops[i];
                                d.wallpaperPlugin = "org.kde.image";
                                d.currentConfigGroup = Array("Wallpaper",
                                                            "org.kde.image",
                                                            "General");
                                d.writeConfig("Image", "file://%s/.local/share/wallpapers/%s");
                        }'
                            """ % (homeUser, image))
    except:
        pass