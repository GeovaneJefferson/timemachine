from setup import *
from read_ini_file import UPDATEINIFILE
from get_size import flatpak_var_list,flatpak_local_list



def backup_user_flatpak_data():
    mainIniFile = UPDATEINIFILE()
    foundVarFolder = []
    
    print("Backing up Flatpak folders...")

    try:
        # FOUND
        # Check first if folders inside backup device can be found, if so, use Rsync, if not, Just Copy to speed the process
        for var in os.listdir(f"{str(mainIniFile.application_var_folder())}"):
            print(var)

        ################################################################################
        # Start Flatpak (var/app) backup
        ################################################################################
        count = 0
        for _ in flatpak_var_list():
            # Copy the Flatpak var/app folders
            sub.run(f"{copyRsyncCMD} {flatpak_var_list()[count]} {str(mainIniFile.application_var_folder())}", shell=True)
            count += 1

        ################################################################################
        # Start Flatpak (.local/share/flatpak) backup
        ################################################################################
        count = 0
        for _ in flatpak_local_list():
            # Copy the Flatpak var/app folders
            sub.run(f"{copyRsyncCMD} {flatpak_local_list()[count]} {str(mainIniFile.application_local_folder())}", shell=True)
            count += 1

    except:
        # NOT FOUND
        ################################################################################
        # Start Flatpak (var/app) backup
        ################################################################################
        count = 0
        for _ in flatpak_var_list():
            # Copy the Flatpak var/app folders
            sub.run(f"{copyCPCMD} {flatpak_var_list()[count]} {str(mainIniFile.application_var_folder())}", shell=True)
            count += 1

        ################################################################################
        # Start Flatpak (.local/share/flatpak) backup
        ################################################################################
        count = 0
        for _ in flatpak_local_list():
            # Copy the Flatpak var/app folders
            sub.run(f"{copyCPCMD} {flatpak_local_list()[count]} {str(mainIniFile.application_local_folder())}", shell=True)
            count += 1
    
    else:
        pass

if __name__ == '__main__':
    pass