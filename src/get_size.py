from setup import *
from read_ini_file import UPDATEINIFILE

flatpakVarSizeList=[]
flatpakVarToBeBackup=[]
flatpakLocaloBeBackup=[]
flatpakLocalSizeList=[]

def flatpak_var_size():
    try:
        ################################################################################
        # Get flatpak (var/app) folders size
        ################################################################################
        for output in os.listdir(src_flatpak_var_folder_location):  # Get folders size before back up to external
            getSize = os.popen(f"du -s {src_flatpak_var_folder_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_var_folder_location}/{output}", "").replace("\t", "")
            getSize = int(getSize)
            ################################################################################
            # Add to list
            # If current folder (output inside var/app) is not higher than X MB
            # Add to list to be backup
            ################################################################################
            # Add to flatpakVarSizeList KBytes size of the current output (folder inside var/app)
            # inside external device
            flatpakVarSizeList.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            flatpakVarToBeBackup.append(f"{src_flatpak_var_folder_location}/{output}")
        
        return sum(flatpakVarSizeList)
    except:
        pass

def flatpak_var_list():
    try:
        flatpak_var_size()
        return flatpakVarToBeBackup
    except:
        pass

def flatpak_local_size():
    try:
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        for output in os.listdir(src_flatpak_local_folder_location):  # Get .local/share/flatpak size before back up to external
            # Get size of flatpak folder inside var/app/
            getSize = os.popen(f"du -s {src_flatpak_local_folder_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_local_folder_location}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            # Add to list to be backup
            flatpakLocalSizeList.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            flatpakLocaloBeBackup.append(f"{src_flatpak_local_folder_location}/{output}")

        return sum(flatpakLocalSizeList)
    except:
        pass

def flatpak_local_list():
    try:
        flatpak_local_size()
        return flatpakLocaloBeBackup
    except:
        pass

def get_external_device_max_size():
    mainIniFile = UPDATEINIFILE()

    # Get external max size
    externalMaxSize = os.popen(f"df --output=size -h {str(mainIniFile.ini_external_location())}")
    externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace(
        "Size", "").replace("\n", "").replace(" ", "")
    return str(externalMaxSize)

def get_external_device_used_size():
    mainIniFile = UPDATEINIFILE()

    # Get external usded size
    usedSpace = os.popen(f"df --output=used -h {str(mainIniFile.ini_external_location())}")
    usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace(
        "Used", "").replace("\n", "").replace(" ", "")

    return str(usedSpace)

def get_external_device_free_size():
    mainIniFile = UPDATEINIFILE()

    try:
        availDeviceSpace = os.popen(f"df --output=avail {str(mainIniFile.ini_external_location())}")
        availDeviceSpace = availDeviceSpace.read().strip().replace("1K-blocks", "").replace("Avail", "").replace(
            "\n", "").replace(" ", "")
        availDeviceSpace = int(availDeviceSpace)

        return int(availDeviceSpace)
    
    except ValueError:
        print("Device is probably not connected.")
        exit()

def get_external_device_string_size(device):
    # Get external max size
    externalMaxSize = os.popen(f"df --output=size -h {device}")
    externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace(
        "Size", "").replace("\n", "").replace(" ", "")

    # Get external usded size
    usedSpace = os.popen(f"df --output=used -h {device}")
    usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace(
        "Used", "").replace("\n", "").replace(" ", "")

    return usedSpace+"/"+externalMaxSize

if __name__ == '__main__':
    pass