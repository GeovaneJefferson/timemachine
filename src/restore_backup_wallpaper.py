from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()
some_image_inside_list = []

async def restore_backup_wallpaper():
    print("Restoring users wallpaper...")
    notification_message_current_backing_up("Restoring: Wallpaper...")

    try:
        # Check if a wallpaper can be found
        for wallpaper in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
            some_image_inside_list.append(wallpaper)
        
        # If has a wallpaper to restore and restoreSystemSettings:
        if some_image_inside_list: 
            # Create wallpapers folders
            if not os.path.exists(str(MAIN_INI_FILE.create_base_folder())):
                sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/wallpapers/",shell=True)

            # Copy to wallpapers folders
            for image in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
                sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.wallpaper_main_folder()}/{image} {HOME_USER}/.local/share/wallpapers/", shell=True)

            # Check if user DE is in the supported list to Automatically apply
            ################################################################
            for count in range(len(SUPPORT_OS)):
                # Activate wallpaper option
                if SUPPORT_OS[count] in str(get_user_de()):
                    # Detect color scheme
                    getColorScheme=os.popen(DETECT_THEME_MODE)
                    getColorScheme=getColorScheme.read().strip().replace("'", "")
                    
                    # Remove spaces if exist
                    if "," in image:
                        image=str(image.replace(", ", "\, "))
                        
                    # Add \ if it has space
                    if " " in image:
                        image=str(image.replace(" ", "\ "))

                    # Light or Dark wallpaper
                    if getColorScheme == "prefer-light" or getColorScheme == "default":
                        # Light theme o default
                        print(f"{SET_GNOME_WALLPAPER} {HOME_USER}/.local/share/wallpapers/{image}")
                        sub.run(f"{SET_GNOME_WALLPAPER} {HOME_USER}/.local/share/wallpapers/{image}", shell=True)
                    else:
                        # Dark theme
                        print(f"{SET_GNOME_WALLPAPER_DARK} {HOME_USER}/.local/share/wallpapers/{image}")
                        sub.run(f"{SET_GNOME_WALLPAPER_DARK} {HOME_USER}/.local/share/wallpapers/{image}", shell=True)

                    # Set wallpaper to Zoom
                    sub.run(f"{ZOOM_GNOME_WALLPAPER}", shell=True)
                    break
                    ################################################################

                elif get_user_de() == "kde":
                    print("Restoring users wallpaper (KDE)...")
                    # Apply to KDE desktop
                    os.popen("""
                            dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
                        var Desktops=desktops();
                        for (i=0;i<Desktops.length;i++) {
                                d=Desktops[i];
                                d.wallpaperPlugin="org.kde.image";
                                d.currentConfigGroup=Array("Wallpaper",
                                                            "org.kde.image",
                                                            "General");
                                d.writeConfig("Image", "file://%s/.local/share/wallpapers/%s");
                        }'
                            """ % (HOME_USER, image))
                    break
        
        return "Task completed: Wallpaper"
    
    except:
        pass

if __name__ == '__main__':
    pass