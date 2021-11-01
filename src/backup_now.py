import os
import shutil
import subprocess as sub
import configparser
import datetime
from pathlib import Path

home_user = str(Path.home())

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

src_user_config = "src/user.ini"

#DST LOCATION
# src_user_config = home_user+"/.local/share/timemachine/src/user.ini"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

#GET FLATPAK
r = os.popen('flatpak --app list --columns=application')
flatpak_list = r.readlines()

class Main():
    def backup_now_pressed(self):
        read_hd_hd = config['EXTERNAL']['hd']

        #CREATE TMB FOLDER
        create_tmb = read_hd_hd+"/TMB"
        date_folder = (create_tmb+"/"+date_day+"-"+date_month+"-"+date_year)

        #---Location to ---#
        self.dst_desktop = date_folder+"/Desktop"
        self.dst_downloads = date_folder+"/Downloads"
        self.dst_documents = date_folder+"/Documents"
        self.dst_music = date_folder+"/Music"
        self.dst_pictures = date_folder+"/Pictures"
        self.dst_videos = date_folder+"/Videos"
        self.dst_flatpak_folder = date_folder+"/Flatpak"
        self.dst_flatpak_txt = date_folder+"/Flatpak/Flatlist.txt"
        
        #READ INI FOLDERS:
        read_desktop = config['FOLDER']['desktop']
        read_downloads = config['FOLDER']['downloads']
        read_documents = config['FOLDER']['documents']
        read_music = config['FOLDER']['music']
        read_pictures = config['FOLDER']['pictures']
        read_videos = config['FOLDER']['videos']

        #BACKUP NOW TRUE
        backup_now_checker = config['DEFAULT']['backup_now']
        if backup_now_checker == "true":
            try:
                #TMB FOLDERS
                if os.path.exists(create_tmb):
                    pass
                else:
                    os.system("mkdir "+create_tmb)
                #DATE FOLDER
                if os.path.exists(date_folder):
                    pass
                else:
                    os.system("mkdir "+date_folder)

                try:
                    #DESKTOP
                    if read_desktop == "true":
                        shutil.copytree(home_user+'/Desktop',self.dst_desktop)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_downloads == "true":
                        shutil.copytree(home_user+'/Downloads',self.dst_downloads)
                    else:
                        pass
                except FileExistsError:
                        pass
                try:
                    if read_documents == "true":
                        shutil.copytree(home_user+'/Documents',self.dst_documents)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_music == "true":
                        shutil.copytree(home_user+'/Music',self.dst_music)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_pictures == "true":
                        shutil.copytree(home_user+'/Pictures',self.dst_pictures)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_videos == "true":
                        shutil.copytree(home_user+'/Videos',self.dst_videos)
                    else:
                        pass
                except FileExistsError:
                    pass

                #FLATPAK FOLDER
                if os.path.exists(self.dst_flatpak_folder):
                    pass
                else:
                    #FLATPAK TXT
                    os.system("mkdir "+date_folder+"/Flatpak")
                    f = open(self.dst_flatpak_txt, "w")    
                    f.close()
                        
                #FLATPAK
                with open(self.dst_flatpak_txt, "w") as reader:
                    for item in flatpak_list:
                        reader.write("app/")
                        reader.write(item.lower())

                    #---After backup is done ---# 
                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Time Machine is done backing up your files!' 5",shell=True)
                    with open(src_user_config, 'w') as configfile:
                        config.set('DEFAULT', 'backup_now', 'false')
                        config.set('INFO', 'latest', day_name+', '+hour+':'+minute)
                        config.write(configfile) 
                    exit()

            except FileNotFoundError:
                #---If external HD is not available ---# 
                sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your external HD could not be found!' 5",shell=True)
                exit()

Object = Main()
Object.backup_now_pressed()