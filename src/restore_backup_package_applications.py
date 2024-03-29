from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_backup_package_applications():
    print("Installing applications packages...")
    
    try:             
        with open(MAIN_INI_FILE.exclude_applications_location(), 'r') as read_exclude:
            read_exclude = read_exclude.read().split("\n")
    except:
        pass

    try:    
        package_manager = MAIN_INI_FILE.get_database_value('INFO', 'packagermanager') 

        if package_manager == DEB_FOLDER_NAME:
            ################################################################################
            # Restore DEBS
            ################################################################################
            for package in os.listdir(MAIN_INI_FILE.deb_main_folder()):
                print(f"Installing {MAIN_INI_FILE.deb_main_folder()}/{package}")

                # Install only if package if not in the exclude app list
                if package not in read_exclude:
                    # Install it
                    command = MAIN_INI_FILE.deb_main_folder() + "/" + package
                    
                    sub.run(
                        ["sudo", "dpkg", "-i", command],
                        stdout=sub.PIPE,
                        stderr=sub.PIPE)

                    # Update notification
                    notification_message_current_backing_up(
                        f'Installing: {package}...')

            # Fix packages installation
            sub.run(
                ["sudo", "apt", "install", "-f"],
                stdout=sub.PIPE,
                stderr=sub.PIPE)

        elif package_manager == RPM_FOLDER_NAME:
            ################################################################################
            # Restore RPMS
            ################################################################################
            for package in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
                print(f"Installing {MAIN_INI_FILE.rpm_main_folder()}/{package}")

                # Install only if package if not in the exclude app list
                if package not in read_exclude:
                    # Install rpms applications
                    command = f"{MAIN_INI_FILE.rpm_main_folder()}/{package}"
                    
                    sub.run(
                        ["sudo", "rpm", "-ivh", "--replacepkgs", command],
                        stdout=sub.PIPE,
                        stderr=sub.PIPE)

                    # Update notification
                    notification_message_current_backing_up(
                        f'Restoring: {package}...')
    
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    pass