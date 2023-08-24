from setup import *


home_folders_list = []

def get_home_folders():
    for folder in GET_HOME_FOLDERS:
        if not "." in folder:    
            home_folders_list.append(folder)
    
    # Sort list
    home_folders_list.sort()
    # Return list
    return home_folders_list


if __name__ == '__main__':
    pass