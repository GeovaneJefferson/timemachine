import glob
import subprocess as sub
import os
import shutil
import subprocess as sub
import configparser
import datetime
from pathlib import Path

#----Get user home----#
user = str(Path.home())
#GET HOUR, MINUTE
date_time = datetime.datetime.now()
day_name = (date_time.strftime("%a"))
date_day = (date_time.strftime("%d"))
date_month = (date_time.strftime("%m"))
date_year = (date_time.strftime("%y"))
hour = date_time.strftime("%H")
hour = str(hour)
minute = date_time.strftime("%M")
minute = str(minute)
#CONFIGPARSER
src_user_config = "src/user.ini"

config = configparser.ConfigParser()
config.read(src_user_config)
#CREATE TMB FOLDER
read_hd_hd = config['EXTERNAL']['hd']
create_tmb = read_hd_hd+"/TMB"
date_folder = (create_tmb+"/"+date_day+"-"+date_month+"-"+date_year)

#---Location to ---#
#path_desktop = (date_folder+"/Desktop")

path_flat_folder = date_folder+"/Flatpak"
path_flat = date_folder+"/Flatpak/Flatlist.txt"


def set_wallpaper():
    #----Set the current wallpaper----#
    # try:
    #     for filename in glob.iglob(path_wall + '**/*.jpg', recursive=True):
    #         sub.Popen("gsettings set org.gnome.desktop.background picture-uri "+filename,shell=True)
    # except:
    #     pass
    # try:
    #     for filename in glob.iglob(path_wall + '**/*.jpeg', recursive=True):
    #         sub.Popen("gsettings set org.gnome.desktop.background picture-uri "+filename,shell=True)
    # except:
    #     pass
    # try:
    #     for filename in glob.iglob(path_wall + '**/*.png', recursive=True):
    #         sub.Popen("gsettings set org.gnome.desktop.background picture-uri "+filename,shell=True)
    # except:
    #     pass
    # print("\nWallpaper was restored!")

    #----Install flatpak list----#
    with open(path_flat, "r") as reader:
        for apps in reader:
            Read_The_File = reader.readline()
            sub.call("flatpak install flathub -y --noninteractive  " + Read_The_File, shell=True)
            
    print("flatpaks apps was restored successfully!")
    exit()

set_wallpaper()

