from setup import *


flatpak_var_size_list = []
flatpak_var_to_be_restore = []
flatpak_local_to_be_restore = []

def restore_backup_flatpaks_data():
    print("Checking size of flatpak (var)...")

    try:
        for output in os.listdir(SRC_FLATPAK_VAR_FOLDER_LOCATION): 
            get_size = os.popen(f"du -s {SRC_FLATPAK_VAR_FOLDER_LOCATION}/{output}")
            get_size = get_size.read().strip("\t").strip("\n").replace(
                f"{SRC_FLATPAK_VAR_FOLDER_LOCATION}/{output}", "").replace("\t", "")

            ################################################################################
            # Add to list
            # If current folder (output inside var/app) is not higher than X MB
            # Add to list to be backup
            ################################################################################
            # Add to flatpak_var_size_list KBytes size of the current output (folder inside var/app)
            # inside external device
            flatpak_var_size_list.append(int(get_size))
            # Add current output (folder inside var/app) to be backup later
            flatpak_var_to_be_restore.append(f"{SRC_FLATPAK_VAR_FOLDER_LOCATION}/{output}")
        
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        # Get .local/share/flatpak size before back up to external
        for output in os.listdir(SRC_FLATPAK_LOCAL_FOLDER_LOCATION):  
            # Get size of flatpak folder inside var/app/
            get_size = os.popen(f"du -s {SRC_FLATPAK_LOCAL_FOLDER_LOCATION}/{output}")
            get_size = get_size.read().strip("\t").strip("\n").replace(
                f"{SRC_FLATPAK_LOCAL_FOLDER_LOCATION}/{output}", "").replace("\t", "")

            # Add to list to be backup
            flatpak_var_size_list.append(int(get_size))
            # Add current output (folder inside var/app) to be backup later
            flatpak_local_to_be_restore.append(f"{SRC_FLATPAK_LOCAL_FOLDER_LOCATION}/{output}")
    except Exception:
        pass

    
if __name__ == '__main__':
    pass