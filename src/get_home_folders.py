from setup import *


def get_home_folders():
    ################################################################################
    # Get Home Folders and Sort them alphabetically
    ################################################################################
    # 
    homeFoldersList = []
    for folder in getHomeFolders:
        if not "." in folder:    
            homeFoldersList.append(folder)
            homeFoldersList.sort()
    
    return homeFoldersList
