from setup import *


flatpak_var_size_list = []
flatpak_var_to_be_restore = []
flatpak_local_to_be_restore = []

def restore_backup_flatpaks_data():
    try:
        print("Checking size of flatpak (var)...")
        for output in os.listdir(src_flatpak_var_folder_location): 
            getSize = os.popen(f"du -s {src_flatpak_var_folder_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_var_folder_location}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            ################################################################################
            # Add to list
            # If current folder (output inside var/app) is not higher than X MB
            # Add to list to be backup
            ################################################################################
            # Add to flatpak_var_size_list KBytes size of the current output (folder inside var/app)
            # inside external device
            flatpak_var_size_list.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            flatpak_var_to_be_restore.append(f"{src_flatpak_var_folder_location}/{output}")
        
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        for output in os.listdir(src_flatpak_local_folder_location):  # Get .local/share/flatpak size before back up to external
            # Get size of flatpak folder inside var/app/
            getSize = os.popen(f"du -s {src_flatpak_local_folder_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_local_folder_location}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            # Add to list to be backup
            flatpak_var_size_list.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            flatpak_local_to_be_restore.append(f"{src_flatpak_local_folder_location}/{output}")
    except Exception as e:
        print(e)
        pass

    
if __name__ == '__main__':
    pass