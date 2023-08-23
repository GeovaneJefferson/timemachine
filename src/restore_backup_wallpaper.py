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
            sub.run(f"{CREATE_CMD_FOLDER} {HOME_USER}/.local/share/wallpapers/",shell=True)

        # Copy backed up wallpaper to .local/share/wallpapers/
        for wallpaper in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
            # Handle spaces
            wallpaper = handle_spaces(wallpaper)
            
            sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.wallpaper_main_folder()}/{wallpaper} "\
                    f"{HOME_USER}/.local/share/wallpapers/", shell=True)

        # Apply wallpaper
        apply_wallpaper(wallpaper)

        return "Task completed: Wallpaper"

def apply_wallpaper(wallpaper):
    print("Applying", wallpaper)

    # Try to automatically apply the restored wallpaper
    for count in range(len(SUPPORT_OS)):
        # Activate wallpaper option
        if SUPPORT_OS[count] in get_user_de():
            # Detect color scheme
            get_color_scheme = os.popen(DETECT_THEME_MODE)
            get_color_scheme = get_color_scheme.read().strip().replace("'", "")

            # Light or Dark wallpaper
            if get_color_scheme == "prefer-light" or get_color_scheme == "default":
                sub.run(
                    f"{SET_GNOME_WALLPAPER} {HOME_USER}/.local/share/wallpapers/{wallpaper}", shell=True)
            else:
                sub.run(
                    f"{SET_GNOME_WALLPAPER_DARK} {HOME_USER}/.local/share/wallpapers/{wallpaper}", shell=True)

            # Set wallpaper to Zoom
            sub.run(f"{ZOOM_GNOME_WALLPAPER}", shell=True)
            break
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
            break

        else:
            return None


if __name__ == '__main__':
    pass