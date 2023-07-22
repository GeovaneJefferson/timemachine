from setup import *
from read_ini_file import UPDATEINIFILE

dummyExcludeAppsList=[]

async def restore_backup_package_applications():
    MAININIFILE=UPDATEINIFILE()
    print("Installing applications packages...")

    config=configparser.ConfigParser()
    config.read(SRC_USER_CONFIG)
    with open(f"{MAININIFILE.exclude_apps_location()}", 'r') as readExclude:
        readExclude=readExclude.read().split("\n")
        dummyExcludeAppsList.append(f"{readExclude}")

    try:             
        if MAININIFILE.ini_package_manager() == f"{RPM_FOLDER_NAME}":
            ################################################################################
            # Restore RPMS
            ################################################################################
            for output in os.listdir(f"{MAININIFILE.rpm_main_folder()}"):
                print(f"{INSTALL_RPM} {MAININIFILE.rpm_main_folder()}")

                # Install only if output if not in the exclude app list
                if output not in str(dummyExcludeAppsList):
                    # Install rpms applications
                    sub.run(f"{INSTALL_RPM} {MAININIFILE.rpm_main_folder()}/{output}",shell=True)
        
        elif MAININIFILE.ini_package_manager() == f"{DEB_FOLDER_NAME}":
            ################################################################################
            # Restore DEBS
            ################################################################################
            for output in os.listdir(f"{MAININIFILE.deb_main_folder()}"):
                print(f"{INSTALL_DEB} {MAININIFILE.deb_main_folder()}")

                # Install only if output if not in the exclude app list
                if output not in str(dummyExcludeAppsList):
                    # Install deb applications
                    sub.run(f"{INSTALL_DEB} {MAININIFILE.deb_main_folder()}/{output}",shell=True)
                    

            # Fix packages installation
            sub.run("sudo apt install -y -f", shell=True)

        # Add flathub repository
        sub.run("sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo", shell=True)
        
        return "Task completed: Wallpaper"
    
    except:
        print("Error trying to install packages...")
        pass


if __name__ == '__main__':
    pass