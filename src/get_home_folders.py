from setup import *

homeFoldersList=[]

def get_home_folders():
    for folder in GET_HOME_FOLDERS:
        if not "." in folder:    
            homeFoldersList.append(folder)
            homeFoldersList.sort()
    
    return homeFoldersList
if __name__ == '__main__':
    pass