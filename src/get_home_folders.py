from setup import *


def get_home_folders():
    homeFoldersList = []
    for folder in getHomeFolders:
        if not "." in folder:    
            homeFoldersList.append(folder)
            homeFoldersList.sort()
    
    return homeFoldersList