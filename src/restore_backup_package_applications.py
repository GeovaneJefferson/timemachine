from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()


async def restore_backup_package_applications():
    print("Installing applications packages...")
    
    with open(f"{MAIN_INI_FILE.exclude_applications_location()}", 'r') as read_exclude:
        read_exclude = read_exclude.read().split("\n")

    try:             
        if MAIN_INI_FILE.get_database_value('INFO', 'packagermanager') == f"{DEB_FOLDER_NAME}":
            ################################################################################
            # Restore DEBS
            ################################################################################
            for package in os.listdir(f"{MAIN_INI_FILE.deb_main_folder()}"):
                print(f"{INSTALL_DEB} {MAIN_INI_FILE.deb_main_folder()}")

                # Install only if package if not in the exclude app list
                if package not in read_exclude:
                    # Install it
                    sub.run(f"{INSTALL_DEB} {MAIN_INI_FILE.deb_main_folder()}/{package}",shell=True)
                    # Update notification
                    notification_message_current_backing_up(f'Installing: {package}...')

            # Fix packages installation
            sub.run("sudo apt install -y -f", shell=True)

        elif MAIN_INI_FILE.get_database_value('INFO', 'packagermanager') == f"{RPM_FOLDER_NAME}":
            ################################################################################
            # Restore RPMS
            ################################################################################
            for package in os.listdir(f"{MAIN_INI_FILE.rpm_main_folder()}"):
                print(f"{INSTALL_RPM} {MAIN_INI_FILE.rpm_main_folder()}")

                # Install only if package if not in the exclude app list
                if package not in read_exclude:
                    # Install rpms applications
                    sub.run(f"{INSTALL_RPM} {MAIN_INI_FILE.rpm_main_folder()}/{package}",shell=True)
                    # Update notification
                    notification_message_current_backing_up(f'Restoring: {package}...')

        
        return "Task completed: Wallpaper"
    
    except Exception:
        pass


if __name__ == '__main__':
    pass