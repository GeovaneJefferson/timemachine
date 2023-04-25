from setup import *
from read_ini_file import UPDATEINIFILE

dummyExcludeAppsList = []

async def restore_backup_package_applications():
    mainIniFile = UPDATEINIFILE()
    print("Installing applications packages...")

    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(f"{mainIniFile.exclude_apps_location()}", 'r') as readExclude:
        readExclude = readExclude.read().split("\n")
        dummyExcludeAppsList.append(f"{readExclude}")

    try:             
        if mainIniFile.ini_package_manager() == f"{rpmFolderName}":
            ################################################################################
            # Restore RPMS
            ################################################################################
            for output in os.listdir(f"{mainIniFile.rpm_main_folder()}"):
                print(f"{installRPM} {mainIniFile.rpm_main_folder()}")

                # Install only if output if not in the exclude app list
                if output not in str(dummyExcludeAppsList):
                    # Install rpms applications
                    sub.run(f"{installRPM} {mainIniFile.rpm_main_folder()}/{output}",shell=True)
        
        elif mainIniFile.ini_package_manager() == f"{debFolderName}":
            ################################################################################
            # Restore DEBS
            ################################################################################
            for output in os.listdir(f"{mainIniFile.deb_main_folder()}"):
                print(f"{installDEB} {mainIniFile.deb_main_folder()}")

                # Install only if output if not in the exclude app list
                if output not in str(dummyExcludeAppsList):
                    # Install deb applications
                    sub.run(f"{installDEB} {mainIniFile.deb_main_folder()}/{output}",shell=True)
                    

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