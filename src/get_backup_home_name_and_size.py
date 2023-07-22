from setup import *
from read_ini_file import UPDATEINIFILE
from get_latest_backup_date import latest_backup_date
from get_backup_time import get_latest_backup_time

homeFolderToBeRestore=[]
homeFolderToRestoreSizeList=[]
homeFolderToRestoreSizeListPretty=[]

def get_backup_home_folders_name():
    MAININIFILE=UPDATEINIFILE()

    try:
        print("Getting folders name...")
        for output in os.listdir(f"{MAININIFILE.get_backup_home_folders()}"):
            output=output.capitalize() 

            try:
                os.listdir(f"{HOME_USER}/{output}")
            except:
                # Lower output first letter
                output=output.lower() 

            homeFolderToBeRestore.append(output)
    
            try:
                getSize=os.popen(f"du -s {MAININIFILE.backup_folder_name()}/{latest_backup_date()}/{(get_latest_backup_time()[0])}/")
                getSize=getSize.read().strip("\t").strip("\n").replace(f"{MAININIFILE.backup_folder_name()}/"
                        f"{latest_backup_date()}/{(get_latest_backup_time()[0])}/", "").replace("\t", "")
                getSize=int(getSize)
                
                homeFolderToRestoreSizeList.append(getSize)
            except:
                pass
           
            try:
                getSize=os.popen(f"du -hs {MAININIFILE.backup_folder_name()}/{latest_backup_date()}/{(get_latest_backup_time()[0])}/")
                getSize=getSize.read().strip("\t").strip("\n").replace(f"{MAININIFILE.backup_folder_name()}/"
                        f"{latest_backup_date()}/{(get_latest_backup_time()[0])}/", "").replace("\t", "")
                
                homeFolderToRestoreSizeListPretty.append(getSize)
            except:
                pass

        return homeFolderToBeRestore
    
    except:
        pass

def get_backup_folders_size():
    get_backup_home_folders_name()
    
    return homeFolderToRestoreSizeList[0]

def get_backup_folders_size_pretty():
    get_backup_home_folders_name()

    try:
        return homeFolderToRestoreSizeListPretty[0]
    except IndexError:
        print("No backup's folder found.")
        return None
    
if __name__ == '__main__':
    pass