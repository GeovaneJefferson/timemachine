from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()
DATA_FOLDERS = []

def get_backup_date():
    DATA_FOLDERS.clear()

    try:
        for folder in os.listdir(f"{str(MAIN_INI_FILE.backup_folder_name())}"):
            # No hidden outputs
            if "." not in folder:
                DATA_FOLDERS.append(folder)
                DATA_FOLDERS.sort(
                    reverse = True, 
                    key = lambda date: datetime.strptime(date, "%d-%m-%y"))
                
        return DATA_FOLDERS
    except Exception :
        pass
    

if __name__ == '__main__':
    pass