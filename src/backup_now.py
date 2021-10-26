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

#dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

#GET FLATPAK
r = os.popen('flatpak --app list --columns=application')
flatpak_list = r.readlines()

class Main():
    def backup_now_pressed(self):
        read_hd_hd = config['EXTERNAL']['hd']
        print(read_hd_hd)

        #CREATE TMB FOLDER
        create_tmb = read_hd_hd+"/TMB"
        date_folder = (create_tmb+"/"+date_day+"-"+date_month+"-"+date_year)

        #---Location to ---#
        path_desktop = (date_folder+"/Desktop")
        path_documents = (date_folder+"/Documents")
        path_downloads = (date_folder+"/Downloads")
        path_music = (date_folder+"/Music")
        path_pictures = (date_folder+"/Pictures")
        path_videos = (date_folder+"/Videos")
        self.path_flat_folder = date_folder+"/Flatpak"
        self.path_flat = date_folder+"/Flatpak/Flatlist.txt"

        #---start by look into home_user.config for backup now---#
        backup_now_checker = config['DEFAULT']['backup_now']
        if backup_now_checker == "true":
            try:
                if os.path.exists(create_tmb):
                    pass
                else:
                    os.system("mkdir "+create_tmb)
                
                if os.path.exists(date_folder):
                    pass
                else:
                    os.system("mkdir "+date_folder)

                #---Create Flatpak Folder inside External HD if do no exist---#
                if os.path.exists(self.path_flat_folder):
                    pass
                else:
                    os.system("mkdir "+date_folder+"/Flatpak")
                    print("Flatpak folder created!")
                    f = open(self.path_flat, "w")    
                    f.close()

                #---Backup Desktop---#
                desktop_checker = config['FOLDER']['desktop']
                if desktop_checker == "true":
                    if os.path.exists(path_desktop):
                        pass
                    else:
                        from_desk = home_user+"/Desktop"
                        shutil.copytree(from_desk, path_desktop)
                        print("Desktop folder created!")
                
                #---Backup Documents---#
                documents_checker = config['FOLDER']['documents']
                if documents_checker == "true":
                    if os.path.exists(path_documents):
                        pass
                    else:
                        from_docu = home_user+"/Documents"
                        shutil.copytree(from_docu,path_documents)
                        print("Documents folder created!")
    
                #---Backup Downloads---#
                downloads_checker = config['FOLDER']['downloads']
                if downloads_checker == "true":
                    if os.path.exists(path_downloads):
                        pass
                    else:
                        from_downloads = home_user+"/Downloads"
                        shutil.copytree(from_downloads,path_downloads)
                        print("Downloads folder created!")

                #---Backup Music---#
                downloads_checker = config['FOLDER']['music']
                if downloads_checker == "true":
                    if os.path.exists(path_music):
                        pass
                    else:
                        from_music = home_user+"/Music"
                        shutil.copytree(from_music,path_music)
                        print("Music folder created!")


                #---Backup Pictures---#
                pictures_checker = config['FOLDER']['pictures']
                if pictures_checker == "true":
                    if os.path.exists(path_pictures):
                        pass
                    else:
                        from_pict = home_user+"/Pictures"
                        shutil.copytree(from_pict,path_pictures)
                        print("Pictures folder created!")
    
                videos_checker = config['FOLDER']['videos']
                if videos_checker == "true":
                    #---Backup Videos---#
                    if os.path.exists(path_videos):
                        pass
                    else:
                        from_video = home_user+"/Videos"
                        shutil.copytree(from_video,path_videos)
                        print("Videos folder created!")

                #----Flatpak----#
                with open(self.path_flat, "w") as reader:
                    for item in flatpak_list:
                        reader.write("app/")
                        reader.write(item.lower())

                    #---After backup is done ---# 
                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Time Machine is done backing up your files!' 5",shell=True)
                    config.read(src_user_config)
                    cfgfile = open(src_user_config, 'w')
                    config.set('DEFAULT', 'backup_now', 'false')
                    config.set('INFO', 'latest', day_name+', '+hour+':'+minute)
                    config.write(cfgfile)
                    cfgfile.close()
                    exit()

            except FileNotFoundError:
                #---If external HD is not available ---# 
                sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your external HD could not be found!' 5",shell=True)
                exit()
            
Object = Main()
Object.backup_now_pressed()