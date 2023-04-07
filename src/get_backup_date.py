from setup import *
from read_ini_file import UPDATEINIFILE


dateFolders = []
def get_backup_date():
    mainIniFile = UPDATEINIFILE()
    try:
        dateFolders.clear()
        for output in os.listdir(f"{str(mainIniFile.backup_folder_name())}"):
            # Hide hidden outputs
            if "." not in output:
                dateFolders.append(output)
                dateFolders.sort(
                    reverse=True, 
                    key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        return dateFolders

    except Exception as error:
        print(error)
        print("Error trying to get backup dates!")
        pass
    
if __name__ == '__main__':
    pass