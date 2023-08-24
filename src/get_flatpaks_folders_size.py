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
    for output in os.listdir(src_flatpak_var_folder_location):  # Get folders size before back up to external
        get_size = os.popen(f"du -s {src_flatpak_var_folder_location}/{output}").read().strip("\t").strip("\n").replace(
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
        flatpak_var_to_be_backup.append(f"{src_flatpak_var_folder_location}/{output}")
    
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
        for output in os.listdir(src_flatpak_local_folder_location):  # Get .local/share/flatpak size before back up to external
            # Get size of flatpak folder inside var/app/
            get_size = os.popen(f"du -s {src_flatpak_local_folder_location}/{output}")
            get_size = get_size.read().strip("\t").strip("\n").replace(
                f"{src_flatpak_local_folder_location}/{output}", "").replace("\t", "")

            # Add to list to be backup
            flatpak_local_size_list.append(int(get_size))
            # Add current output (folder inside var/app) to be backup later
            flatpak_local_to_be_backup.append(f"{src_flatpak_local_folder_location}/{output}")
        
        # Return sum of all local sizes
        return sum(flatpak_local_size_list)
    except:
        pass

def flatpak_local_list():
    flatpak_local_size()

    return flatpak_local_to_be_backup

def get_external_device_max_size():
    # Get external max size
    external_max_size = os.popen(
        f"df --output=size -h {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}")
    external_max_size = external_max_size.read().strip()\
                            .replace("1K-blocks", "")\
                            .replace("Size", "")\
                            .replace("\n", "")\
                            .replace(" ", "")
    
    return str(external_max_size)

def get_external_device_used_size():
    used_space = os.popen(
        f"df --output=avail -h {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}").read().strip()\
                            .replace("1K-blocks", "")\
                            .replace("Avail", "")\
                            .replace("\n", "")\
                            .replace(" ", "")

    return str(used_space)

def get_external_device_free_size():
    try:
        available_device_space = os.popen(
            f"df --output=avail {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}")
        available_device_space = available_device_space.read().strip()\
            .replace("1K-blocks", "")\
            .replace("Avail", "")\
            .replace("\n", "")\
            .replace(" ", "")
        
        return int(available_device_space)
    
    except ValueError:
        print("Device is probably not connected.")
        exit()

def get_external_device_string_size(device):
    # Get external max size
    external_max_size=os.popen(
        f"df --output=size -h {device}").read().strip().replace(
        "1K-blocks", "").replace(
        "Size", "").replace(
        "\n", "").replace(
        " ", "")

    # Get external usded size
    used_space = os.popen(f"df --output=used -h {device}")
    used_space = used_space.read().strip().replace("1K-blocks", "").replace(
        "Used", "").replace("\n", "").replace(" ", "")

    return used_space + "/" + external_max_size

def get_all_used_backup_device_space(device):
    # If inside /Media
    if device_location():
        used_space = os.popen(
            f"df --output=avail -h {MEDIA}/{USERNAME}/{device}").read().\
            strip().replace(
            "1K-blocks", "").replace(
            "Avail", "").replace(
            "\n", "").replace(
            " ", "")

    # If inside /Run
    else:
        used_space = os.popen(f"df --output=avail -h {RUN}/{USERNAME}/{device}").read().\
            strip().replace(
            "1K-blocks", "").replace(
            "Avail", "").replace(
            "\n", "").replace(
            " ", "")

    return str(used_space)

def get_all_max_backup_device_space(device):
    # If inside /Media
    if device_location():
        external_max_size=os.popen(f"df --output=size -h {MEDIA}/{USERNAME}/{device}").read().strip().replace(
            "1K-blocks", "").replace(
            "Size", "").replace(
            "\n", "").replace(
            " ", "")
    
    # If inside /Run
    else:
        external_max_size=os.popen(f"df --output=size -h {RUN}/{USERNAME}/{device}").read().strip().replace(
            "1K-blocks", "").replace(
            "Size", "").replace(
            "\n", "").replace(
            " ", "")
    
    return str(external_max_size)


if __name__ == '__main__':
    pass