from setup import *
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de
from notification_massage import notification_message_current_backing_up
from handle_spaces import handle_spaces


MAIN_INI_FILE = UPDATEINIFILE()


has_wallpaper_to_restore = []

async def restore_backup_wallpaper():
    print("Applying users wallpaper...")

    notification_message_current_backing_up("Applying: Wallpaper...")

    # Check for at least a wallpaper
    for wallpaper in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
        has_wallpaper_to_restore.append(wallpaper)
    
    # If has a wallpaper to restore and restoreSystemSettings:
    if has_wallpaper_to_restore: 
        # Create .local/share/wallpapers/
        if not os.path.exists(str(MAIN_INI_FILE.create_base_folder())):
            command = f"{HOME_USER}/.local/share/wallpapers/"
            sub.run(["mkdir", command])

        # Copy backed up wallpaper to .local/share/wallpapers/
        for wallpaper in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
            # Handle spaces
            wallpaper = handle_spaces(wallpaper)
            
            # Restore
            src = MAIN_INI_FILE.wallpaper_main_folder() + "/" + wallpaper
            dst = HOME_USER + "/.local/share/wallpapers/"
            sub.run(["rsync", "-avr", src, dst])
            
        # Apply wallpaper
        apply_wallpaper(wallpaper)

        return "Task completed: Wallpaper"

def apply_wallpaper(wallpaper):
    print("Applying", wallpaper)

    # Activate wallpaper option
    if  get_user_de() == "gnome":
        # Detect color scheme
        get_color_scheme = os.popen(DETECT_THEME_MODE)
        get_color_scheme = get_color_scheme.read().strip().replace("'", "")

        # Light or Dark wallpaper
        if get_color_scheme == "prefer-light" or get_color_scheme == "default":
            command = f"{HOME_USER}/.local/share/wallpapers/{wallpaper}"
            action = "gsettings", "set", "org.gnome.desktop.background", "picture-uri"
            sub.run([action, command])
        else:
            command = f"{HOME_USER}/.local/share/wallpapers/{wallpaper}"
            action = "gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark"
            sub.run([action, command])

        # Set wallpaper to Zoom
        action = "gsettings", "set", "org.gnome.desktop.background", "picture-options", "zoom"
        sub.run([action])
        ################################################################

    elif get_user_de() == "kde":
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
                """ % (HOME_USER, wallpaper))
    else:
        return None


if __name__ == '__main__':
    pass