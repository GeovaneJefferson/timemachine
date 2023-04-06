from setup import *
from read_ini_file import UPDATEINIFILE
from get_latest_backup_date import latest_backup_date
from get_backup_time import get_latest_backup_time

homeFolderToBeRestore=[]
homeFolderToRestoreSizeList=[]

def get_backup_home_folders_name():
    mainIniFile = UPDATEINIFILE()

    try:
        print("Getting folders name...")
        for output in os.listdir(f"{mainIniFile.get_backup_home_folders()}"):
            output = output.capitalize() 

            try:
                os.listdir(f"{homeUser}/{output}")
            except:
                # Lower output first letter
                output = output.lower() 

            homeFolderToBeRestore.append(output)
    
            try:
                getSize = os.popen(f"du -s {mainIniFile.backup_folder_name()}/{latest_backup_date()}/{get_latest_backup_time()}/")
                getSize = getSize.read().strip("\t").strip("\n").replace(f"{mainIniFile.backup_folder_name()}/"
                        f"{latest_backup_date()}/{get_latest_backup_time()}/", "").replace("\t", "")
                getSize = int(getSize)
                
                homeFolderToRestoreSizeList.append(getSize)
            except:
                pass
    
        return homeFolderToBeRestore
    
    except:
        pass

def get_backup_folders_size():
    return homeFolderToRestoreSizeList

if __name__ == '__main__':
    pass