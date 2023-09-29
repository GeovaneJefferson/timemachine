from setup import *
from read_ini_file import UPDATEINIFILE
from device_location import device_location


MAIN_INI_FILE = UPDATEINIFILE()


flatpak_var_size_list = []
flatpak_var_to_be_backup = []
flatpak_local_to_be_backup = []
flatpak_local_size_list = []

def flatpak_var_size():
    ################################################################################
    # Get flatpak (var/app) folders size
    ################################################################################
    for output in os.listdir(SRC_FLATPAK_VAR_FOLDER_LOCATION):  # Get folders size before back up to external
        get_size = os.popen(f"du -s {SRC_FLATPAK_VAR_FOLDER_LOCATION}/{output}").read().strip("\t").strip("\n").replace(
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
        flatpak_var_to_be_backup.append(f"{SRC_FLATPAK_VAR_FOLDER_LOCATION}/{output}")
    
    # Return sum of all var sizes
    return sum(flatpak_var_size_list)
    
def flatpak_var_list():
    # Get flapatk var size
    flatpak_var_size()

    return flatpak_var_to_be_backup

def flatpak_local_size():
    try:
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        for output in os.listdir(SRC_FLATPAK_LOCAL_FOLDER_LOCATION):  # Get .local/share/flatpak size before back up to external
            # Get size of flatpak folder inside var/app/
            get_size = os.popen(f"du -s {SRC_FLATPAK_LOCAL_FOLDER_LOCATION}/{output}")
            get_size = get_size.read().strip("\t").strip("\n").replace(
                f"{SRC_FLATPAK_LOCAL_FOLDER_LOCATION}/{output}", "").replace("\t", "")

            # Add to list to be backup
            flatpak_local_size_list.append(int(get_size))
            # Add current output (folder inside var/app) to be backup later
            flatpak_local_to_be_backup.append(f"{SRC_FLATPAK_LOCAL_FOLDER_LOCATION}/{output}")
        
        # Return sum of all local sizes
        return sum(flatpak_local_size_list)
    except:
        pass

def flatpak_local_list():
    flatpak_local_size()

    return flatpak_local_to_be_backup


if __name__ == '__main__':
    pass