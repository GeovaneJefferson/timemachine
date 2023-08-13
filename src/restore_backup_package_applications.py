from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()
exclude_apps_list = []

async def restore_backup_package_applications():
    print("Installing applications packages...")
    with open(f"{MAIN_INI_FILE.exclude_apps_location()}", 'r') as read_exclude:
        read_exclude = read_exclude.read().split("\n")
        exclude_apps_list.append(f"{(read_exclude)}")

    try:             
        if MAIN_INI_FILE.get_database_value('INFO', 'packagermanager') == f"{RPM_FOLDER_NAME}":
            ################################################################################
            # Restore RPMS
            ################################################################################
            for output in os.listdir(f"{MAIN_INI_FILE.rpm_main_folder()}"):
                print(f"{INSTALL_RPM} {MAIN_INI_FILE.rpm_main_folder()}")

                # Install only if output if not in the exclude app list
                if output not in str(exclude_apps_list):
                    # Install rpms applications
                    sub.run(f"{INSTALL_RPM} {MAIN_INI_FILE.rpm_main_folder()}/{output}",shell=True)
        
        elif MAIN_INI_FILE.get_database_value('INFO', 'packagermanager') == f"{DEB_FOLDER_NAME}":
            ################################################################################
            # Restore DEBS
            ################################################################################
            for output in os.listdir(f"{MAIN_INI_FILE.deb_main_folder()}"):
                print(f"{INSTALL_DEB} {MAIN_INI_FILE.deb_main_folder()}")

                # Install only if output if not in the exclude app list
                if output not in str(exclude_apps_list):
                    # Install deb applications
                    sub.run(f"{INSTALL_DEB} {MAIN_INI_FILE.deb_main_folder()}/{output}",shell=True)

            # Fix packages installation
            sub.run("sudo apt install -y -f", shell=True)

        return "Task completed: Wallpaper"
    
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    pass