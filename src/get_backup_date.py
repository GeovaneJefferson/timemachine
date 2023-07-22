from setup import *
from read_ini_file import UPDATEINIFILE


DATA_FOLDERS=[]


def get_backup_date():
    MAININIFILE=UPDATEINIFILE()
    try:
        DATA_FOLDERS.clear()
        for output in os.listdir(f"{str(MAININIFILE.backup_folder_name())}"):
            # Hide hidden outputs
            if "." not in output:
                DATA_FOLDERS.append(output)
                DATA_FOLDERS.sort(
                    reverse=True, 
                    key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        return DATA_FOLDERS

    except Exception as error:
        print(error)
        print("Error trying to get backup dates!")
        pass
    

if __name__ == '__main__':
    print(get_backup_date())
    pass