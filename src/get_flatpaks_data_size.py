from setup import *


flatpak_var_size_list = []
flatpak_var_to_be_restore = []
flatpak_local_to_be_restore = []

def restore_backup_flatpaks_data():
    print("Checking size of flatpak (var)...")

    try:
        for output in os.listdir(src_flatpak_var_folder_location): 
            get_size = os.popen(f"du -s {src_flatpak_var_folder_location}/{output}")
            get_size = get_size.read().strip("\t").strip("\n").replace(
                f"{src_flatpak_var_folder_location}/{output}", "").replace("\t", "")

            ################################################################################
            # Add to list
            # If current folder (output inside var/app) is not higher than X MB
            # Add to list to be backup
            ################################################################################
            # Add to flatpak_var_size_list KBytes size of the current output (folder inside var/app)
            # inside external device
            flatpak_var_size_list.append(int(get_size))
            # Add current output (folder inside var/app) to be backup later
            flatpak_var_to_be_restore.append(f"{src_flatpak_var_folder_location}/{output}")
        
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        # Get .local/share/flatpak size before back up to external
        for output in os.listdir(src_flatpak_local_folder_location):  
            # Get size of flatpak folder inside var/app/
            get_size = os.popen(f"du -s {src_flatpak_local_folder_location}/{output}")
            get_size = get_size.read().strip("\t").strip("\n").replace(
                f"{src_flatpak_local_folder_location}/{output}", "").replace("\t", "")

            # Add to list to be backup
            flatpak_var_size_list.append(int(get_size))
            # Add current output (folder inside var/app) to be backup later
            flatpak_local_to_be_restore.append(f"{src_flatpak_local_folder_location}/{output}")
    except Exception:
        pass

    
if __name__ == '__main__':
    pass