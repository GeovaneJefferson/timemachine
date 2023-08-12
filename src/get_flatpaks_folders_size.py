from setup import *
from read_ini_file import UPDATEINIFILE
from device_location import device_location

flatpakVarSizeList=[]
flatpakVarToBeBackup=[]
flatpakLocaloBeBackup=[]
flatpakLocalSizeList=[]
MAIN_INI_FILE = UPDATEINIFILE()

def flatpak_var_size():
    ################################################################################
    # Get flatpak (var/app) folders size
    ################################################################################
    for output in os.listdir(src_flatpak_var_folder_location):  # Get folders size before back up to external
        getSize=os.popen(f"du -s {src_flatpak_var_folder_location}/{output}").read().strip("\t").strip("\n").replace(
            f"{src_flatpak_var_folder_location}/{output}", "").replace("\t", "")

        ################################################################################
        # Add to list
        # If current folder (output inside var/app) is not higher than X MB
        # Add to list to be backup
        ################################################################################
        # Add to flatpakVarSizeList KBytes size of the current output (folder inside var/app)
        # inside external device
        flatpakVarSizeList.append(int(getSize))
        # Add current output (folder inside var/app) to be backup later
        flatpakVarToBeBackup.append(f"{src_flatpak_var_folder_location}/{output}")
    
    return sum(flatpakVarSizeList)
    
def flatpak_var_list():
    # Get flapatk var/ size
    flatpak_var_size()

    return flatpakVarToBeBackup

def flatpak_local_size():
    try:
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        for output in os.listdir(src_flatpak_local_folder_location):  # Get .local/share/flatpak size before back up to external
            # Get size of flatpak folder inside var/app/
            getSize=os.popen(f"du -s {src_flatpak_local_folder_location}/{output}")
            getSize=getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_local_folder_location}/{output}", "").replace("\t", "")
            getSize=int(getSize)

            # Add to list to be backup
            flatpakLocalSizeList.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            flatpakLocaloBeBackup.append(f"{src_flatpak_local_folder_location}/{output}")

        return sum(flatpakLocalSizeList)
    except:
        pass

def flatpak_local_list():
    flatpak_local_size()
    return flatpakLocaloBeBackup

def get_external_device_max_size():
    # Get external max size
    external_max_size = os.popen(f"df --output=size -h {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}")
    external_max_size = external_max_size.read().strip()\
                            .replace("1K-blocks", "")\
                            .replace("Size", "")\
                            .replace("\n", "")\
                            .replace(" ", "")
    
    return str(external_max_size)

def get_external_device_used_size():
    used_space = os.popen(f"df --output=avail -h \
                          {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}").read().strip()\
                            .replace("1K-blocks", "")\
                            .replace("Avail", "")\
                            .replace("\n", "")\
                            .replace(" ", "")

    return str(used_space)

def get_external_device_free_size():
    try:
        availDeviceSpace = os.popen(f"df --output=avail {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}")
        availDeviceSpace = availDeviceSpace.read().strip()\
            .replace("1K-blocks", "")\
            .replace("Avail", "")\
            .replace("\n", "")\
            .replace(" ", "")

        return int(availDeviceSpace)
    
    except ValueError:
        print("Device is probably not connected.")
        exit()

def get_external_device_string_size(device):
    # Get external max size
    external_max_size=os.popen(f"df --output=size -h {device}").read().strip().replace(
        "1K-blocks", "").replace(
        "Size", "").replace(
        "\n", "").replace(
        " ", "")

    # Get external usded size
    used_space=os.popen(f"df --output=used -h {device}")
    used_space=used_space.read().strip().replace("1K-blocks", "").replace(
        "Used", "").replace("\n", "").replace(" ", "")

    return used_space+"/"+external_max_size

def get_all_used_backup_device_space(device):
    # If inside /Media
    if device_location():
        used_space=os.popen(f"df --output=avail -h {MEDIA}/{USERNAME}/{device}").read().\
            strip().replace("1K-blocks", "").replace("Avail", "").replace("\n", "").replace(" ", "")

    # If inside /Run
    else:
        used_space=os.popen(f"df --output=avail -h {RUN}/{USERNAME}/{device}").read().\
            strip().replace("1K-blocks", "").replace("Avail", "").replace("\n", "").replace(" ", "")

    return str(used_space)

def get_all_max_backup_device_space(device):
    # If inside /Media
    if device_location():
        external_max_size=os.popen(f"df --output=size -h {MEDIA}/{USERNAME}/{device}").read().strip().replace(
            "1K-blocks", "").replace("Size", "").replace("\n", "").replace(" ", "")
    
    # If inside /Run
    else:
        external_max_size=os.popen(f"df --output=size -h {RUN}/{USERNAME}/{device}").read().strip().replace(
            "1K-blocks", "").replace("Size", "").replace("\n", "").replace(" ", "")
    
    return str(external_max_size)


if __name__ == '__main__':
    pass