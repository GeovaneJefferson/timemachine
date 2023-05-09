from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_wallpaper import user_wallpaper


def backup_user_wallpaper():
    mainIniFile = UPDATEINIFILE()
    
    # Replace wallpaper inside the folder, only allow 1
    if os.listdir(f"{str(mainIniFile.wallpaper_main_folder())}"):
        # Delete all image inside wallpaper folder
        for image in os.listdir(f"{str(mainIniFile.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}/"):
            print(f"Deleting {str(mainIniFile.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}/{image}...")
            sub.run(f"rm -rf {str(mainIniFile.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}/{image}", shell=True)

    print(f"{copyCPCMD} {user_wallpaper()} {str(mainIniFile.wallpaper_main_folder())}/")
    sub.run(f"{copyCPCMD} {user_wallpaper()} {str(mainIniFile.wallpaper_main_folder())}/", shell=True) 


if __name__ == '__main__':
    pass
