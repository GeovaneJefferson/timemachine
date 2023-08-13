from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE=UPDATEINIFILE()
DATA_FOLDERS=[]

def get_backup_date():
    try:
        DATA_FOLDERS.clear()
        for output in os.listdir(f"{str(MAIN_INI_FILE.backup_folder_name())}"):
            # Hide hidden outputs
            if "." not in output:
                DATA_FOLDERS.append(output)
                DATA_FOLDERS.sort(
                    reverse = True, 
                    key = lambda date: datetime.strptime(date, "%d-%m-%y"))

        return DATA_FOLDERS

    except Exception as e:
        print(e)
        pass
    

if __name__ == '__main__':
    pass