import glob
import subprocess as sub
from pathlib import Path

#----Get user home----#
user = str(Path.home())
path_wall = user+"/Applications/timemachine/wallpaper"
path = user+"/Applications/timemachine/src/Flatlist.txt"

def set_wallpaper():
    #----Set the current wallpaper----#
    try:
        for filename in glob.iglob(path_wall + '**/*.jpg', recursive=True):
            sub.Popen("gsettings set org.gnome.desktop.background picture-uri "+filename,shell=True)
    except:
        pass
    try:
        for filename in glob.iglob(path_wall + '**/*.jpeg', recursive=True):
            sub.Popen("gsettings set org.gnome.desktop.background picture-uri "+filename,shell=True)
    except:
        pass
    try:
        for filename in glob.iglob(path_wall + '**/*.png', recursive=True):
            sub.Popen("gsettings set org.gnome.desktop.background picture-uri "+filename,shell=True)
    except:
        pass
    print("\nWallpaper was restored!")

    #----Install flatpak list----#
    with open(path, "r") as reader:
        for apps in reader:
            Read_The_File = reader.readline()
            sub.call("flatpak install flathub -y --noninteractive  "+Read_The_File,shell=True)
            
    print("flatpaks apps was restored successfully!")
    exit()

set_wallpaper()

