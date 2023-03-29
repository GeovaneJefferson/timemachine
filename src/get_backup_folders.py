from setup import *
from read_ini_file import UPDATEINIFILE

homeFolderToBeBackup=[]
homeFolderToBackupSizeList=[]
flatpakVarSizeList=[]
flatpakVarToBeBackup=[]
flatpakLocaloBeBackup=[]
flatpakLocalSizeList=[]

def get_folders():
    mainIniFile = UPDATEINIFILE()
    try:
        ################################################################################
        # Get Backup Folders
        ################################################################################
        for output in mainIniFile.ini_folders():  # Get folders size before back up to external
            # Capitalize first letter
            output = output.capitalize()
            # Can output be found inside Users Home?
            try:
                os.listdir(f"{homeUser}/{output}")
            except:
                # Lower output first letter
                output = output.lower() # Lower output first letter

            # Add output inside homeFolderToBeBackup
            homeFolderToBeBackup.append(output)
            # Sort them
            homeFolderToBeBackup.sort()
        
        return homeFolderToBeBackup 
    except:
        pass

def home_folders_size():
    try:
        for output in homeFolderToBeBackup:
            # Get folder size
            getSize = os.popen(f"du -s {homeUser}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{homeUser}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            # Add to list
            homeFolderToBackupSizeList.append(getSize)

        return homeFolderToBackupSizeList
    except:
        pass

def flatpak_var_size():
    try:
        ################################################################################
        # Get flatpak (var/app) folders size
        ################################################################################
        for output in os.listdir(src_flatpak_var_location):  # Get folders size before back up to external
            getSize = os.popen(f"du -s {src_flatpak_var_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_var_location}/{output}", "").replace("\t", "")
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
            flatpakVarToBeBackup.append(f"{src_flatpak_var_location}/{output}")
        
        return flatpakVarSizeList
    except:
        pass


def flatpak_var_list():
    try:
        return flatpakVarToBeBackup
    except:
        pass

def flatpak_local_size():
    try:
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        for output in os.listdir(src_flatpak_local_location):  # Get .local/share/flatpak size before back up to external
            # Get size of flatpak folder inside var/app/
            getSize = os.popen(f"du -s {src_flatpak_local_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_local_location}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            # Add to list to be backup
            flatpakLocalSizeList.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            flatpakLocaloBeBackup.append(f"{src_flatpak_local_location}/{output}")

        return flatpakLocalSizeList
    except:
        pass

def flatpak_local_list():
    try:
        return flatpakLocaloBeBackup
    except:
        pass

def total_home_folders_to_backup():
    mainIniFile = UPDATEINIFILE()
    global freeSpace

    print("Calculating Home folders...")
    ################################################################################
    # Get external maximum size
    ################################################################################
    externalMaxSize = os.popen(f"df --output=size {str(mainIniFile.ini_external_location())}")
    externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace("Size", "").replace(
        "\n", "").replace(" ", "")
    externalMaxSize = int(externalMaxSize)

    ################################################################################
    # Get external used space
    ################################################################################
    usedSpace = os.popen(f"df --output=used {str(mainIniFile.ini_external_location())}")
    usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace("Used", "").replace(
        "\n", "").replace(" ", "")
    usedSpace = int(usedSpace)

    ################################################################################
    # Calculattions
    ################################################################################
    # Sum of all folders (from INI file) to be backup
    totalHomeFoldersToBackupSize = sum(homeFolderToBackupSizeList)
    # Calculate free space
    freeSpace = int(externalMaxSize - usedSpace)

    return totalHomeFoldersToBackupSize

def free_space_home_folders():
    return freeSpace
