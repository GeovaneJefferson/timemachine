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
        for output in get_folders():
            # Get folder size
            getSize = os.popen(f"du -s {homeUser}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{homeUser}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            # Add to list
            homeFolderToBackupSizeList.append(getSize)

        return sum(homeFolderToBackupSizeList)
    except:
        pass

# def flatpak_var_size():
#     try:
#         ################################################################################
#         # Get flatpak (var/app) folders size
#         ################################################################################
#         for output in os.listdir(src_flatpak_var_folder_location):  # Get folders size before back up to external
#             getSize = os.popen(f"du -s {src_flatpak_var_folder_location}/{output}")
#             getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_var_folder_location}/{output}", "").replace("\t", "")
#             getSize = int(getSize)
#             ################################################################################
#             # Add to list
#             # If current folder (output inside var/app) is not higher than X MB
#             # Add to list to be backup
#             ################################################################################
#             # Add to flatpakVarSizeList KBytes size of the current output (folder inside var/app)
#             # inside external device
#             flatpakVarSizeList.append(getSize)
#             # Add current output (folder inside var/app) to be backup later
#             flatpakVarToBeBackup.append(f"{src_flatpak_var_folder_location}/{output}")
        
#         return sum(flatpakVarSizeList)
#     except:
#         pass


# def flatpak_var_list():
#     try:
#         flatpak_var_size()
#         return flatpakVarToBeBackup
#     except:
#         pass

# def flatpak_local_size():
#     try:
#         ################################################################################
#         # Get flatpak (.local/share/flatpak) folders size
#         ################################################################################
#         for output in os.listdir(src_flatpak_local_folder_location):  # Get .local/share/flatpak size before back up to external
#             # Get size of flatpak folder inside var/app/
#             getSize = os.popen(f"du -s {src_flatpak_local_folder_location}/{output}")
#             getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_local_folder_location}/{output}", "").replace("\t", "")
#             getSize = int(getSize)

#             # Add to list to be backup
#             flatpakLocalSizeList.append(getSize)
#             # Add current output (folder inside var/app) to be backup later
#             flatpakLocaloBeBackup.append(f"{src_flatpak_local_folder_location}/{output}")

#         return sum(flatpakLocalSizeList)
#     except:
#         pass

# def flatpak_local_list():
#     try:
#         flatpak_local_size()
#         return flatpakLocaloBeBackup
#     except:
#         pass

# def external_device_size_information():
#     mainIniFile = UPDATEINIFILE()
#     global freeSpace

#     ################################################################################
#     # Get external maximum size
#     ################################################################################
#     externalMaxSize = os.popen(f"df --output=size {str(mainIniFile.ini_external_location())}")
#     externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace("Size", "").replace(
#         "\n", "").replace(" ", "")
#     externalMaxSize = int(externalMaxSize)

#     ################################################################################
#     # Get external used space
#     ################################################################################
#     usedSpace = os.popen(f"df --output=used {str(mainIniFile.ini_external_location())}")
#     usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace("Used", "").replace(
#         "\n", "").replace(" ", "")
#     usedSpace = int(usedSpace)

#     # Calculate free space
#     freeSpace = int(externalMaxSize - usedSpace)

#     return sum(homeFolderToBackupSizeList)

# def external_device_free_space():
#     external_device_size_information()
#     return freeSpace

if __name__ == '__main__':
    pass