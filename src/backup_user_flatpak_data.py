from setup import *
from read_ini_file import UPDATEINIFILE
from get_size import flatpak_var_list,flatpak_local_list

def backup_user_flatpak_data():
    mainIniFile = UPDATEINIFILE()
    
    print("Backing up Flatpak folders...")
    try:
        ################################################################################
        # Start Flatpak (var/app) backup
        ################################################################################
        count = 0
        for output in flatpak_var_list():
            # Copy the Flatpak var/app folders
            print(f"{copyCPCMD} {flatpak_var_list()[count]} {str(mainIniFile.application_var_folder())}")
            sub.run(f"{copyCPCMD} {flatpak_var_list()[count]} {str(mainIniFile.application_var_folder())}", shell=True)
            count += 1

        ################################################################################
        # Start Flatpak (.local/share/flatpak) backup
        ################################################################################
        count = 0
        for output in flatpak_local_list():
            # Copy the Flatpak var/app folders
            print(f"{copyRsyncCMD} {flatpak_local_list()[count]} {str(mainIniFile.application_local_folder())}")
            sub.run(f"{copyRsyncCMD} {flatpak_local_list()[count]} {str(mainIniFile.application_local_folder())}", shell=True)
            count += 1

    except FileNotFoundError as error:
        error_trying_to_backup(error)

if __name__ == '__main__':
    pass