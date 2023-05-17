from setup import *
from read_ini_file import UPDATEINIFILE

homeFolderToBeBackup=[]
homeFolderToBackupSizeList=[]


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

if __name__ == '__main__':
    pass