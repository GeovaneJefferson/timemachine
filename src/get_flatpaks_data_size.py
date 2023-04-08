from setup import *
from read_ini_file import UPDATEINIFILE


def restore_backup_flatpaks_data():
    mainIniFile = UPDATEINIFILE()
    try:
        print("Checking size of flatpak (var)...")
        # Get folders size
        self.flatpakVarSizeList=[]
        self.flatpakLocalSizeList=[]
        self.flatpakVarToBeRestore=[]
        self.flatpakLocaloBeRestore=[]
        
        for output in os.listdir(src_flatpak_var_folder_location): 
            getSize = os.popen(f"du -s {src_flatpak_var_folder_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_var_folder_location}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            ################################################################################
            # Add to list
            # If current folder (output inside var/app) is not higher than X MB
            # Add to list to be backup
            ################################################################################
            # Add to self.flatpakVarSizeList KBytes size of the current output (folder inside var/app)
            # inside external device
            self.flatpakVarSizeList.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            self.flatpakVarToBeRestore.append(f"{src_flatpak_var_folder_location}/{output}")
        
        ################################################################################
        # Get flatpak (.local/share/flatpak) folders size
        ################################################################################
        for output in os.listdir(src_flatpak_local_folder_location):  # Get .local/share/flatpak size before back up to external
            # Get size of flatpak folder inside var/app/
            getSize = os.popen(f"du -s {src_flatpak_local_folder_location}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{src_flatpak_local_folder_location}/{output}", "").replace("\t", "")
            getSize = int(getSize)

            # Add to list to be backup
            self.flatpakVarSizeList.append(getSize)
            # Add current output (folder inside var/app) to be backup later
            self.flatpakLocaloBeRestore.append(f"{src_flatpak_local_folder_location}/{output}")
            self.flatpakLocaloBeRestore=[]
    except:
        pass
if __name__ == '__main__':
    pass