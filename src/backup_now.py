import os
import subprocess as sub
import configparser
from pathlib import Path
from datetime import datetime

home_user = str(Path.home())

# GET HOUR, MINUTE
date_time = datetime.now()
day_name = (date_time.strftime("%a"))
date_day = (date_time.strftime("%d"))
date_month = (date_time.strftime("%m"))
date_year = (date_time.strftime("%y"))

current_hour = date_time.strftime("%H")
current_minute = date_time.strftime("%M")

# SRC LOCATION
# src_user_config = "src/user.ini"

# DST LOCATION
src_user_config = home_user + "/.local/share/timemachine/src/user.ini"

# CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)


class Main:
    def backup_now_pressed(self):
        read_hd_name = config['EXTERNAL']['hd']

        # CREATE TMB FOLDER
        create_tmb = read_hd_name + "/TMB"
        date_folder = (create_tmb + "/" + date_day + "-" + date_month + "-" + date_year)

        # ---Location to ---#
        dst_desktop = date_folder + "/Desktop"
        dst_downloads = date_folder + "/Downloads"
        dst_documents = date_folder + "/Documents"
        dst_music = date_folder + "/Music"
        dst_pictures = date_folder + "/Pictures"
        dst_videos = date_folder + "/Videos"

        # READ INI FOLDERS:
        read_desktop = config['FOLDER']['desktop']
        read_downloads = config['FOLDER']['downloads']
        read_documents = config['FOLDER']['documents']
        read_music = config['FOLDER']['music']
        read_pictures = config['FOLDER']['pictures']
        read_videos = config['FOLDER']['videos']

        # BACKUP NOW TRUE
        backup_now_checker = config['DEFAULT']['backup_now']
        if backup_now_checker:
            try:
                # TMB FOLDERS
                if os.path.exists(create_tmb):
                    pass
                else:
                    os.system("mkdir " + create_tmb)
                # DATE FOLDER
                if os.path.exists(date_folder):
                    pass
                else:
                    os.system("mkdir " + date_folder)

                try:
                    # DESKTOP
                    if read_desktop:
                        os.system("rsync -avzh " + home_user + '/Desktop/' + " " + dst_desktop)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_downloads:
                        os.system("rsync -avzh " + home_user + '/Download/' + " " + dst_downloads)
                    else:
                        pass
                except FileExistsError:
                    pass
                try:
                    if read_documents:
                        os.system("rsync -avzh " + home_user + '/Documents/' + " " + dst_documents)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_music:
                        os.system("rsync -avzh " + home_user + '/Music/' + " " + dst_music)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_pictures:
                        os.system("rsync -avzh " + home_user + '/Pictures/' + " " + dst_pictures)
                    else:
                        pass
                except FileExistsError:
                    pass

                try:
                    if read_videos:
                        os.system("rsync -avzh " + home_user + '/Videos/' + " " + dst_videos)
                    else:
                        pass
                except FileExistsError:
                    pass

                    # After backup is done
                    sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Time Machine is done backing up your files!' 5", shell=True)
                    with open(src_user_config, 'w') as configfile:
                        config.set('DEFAULT', 'backup_now', 'false')
                        config.set('INFO', 'latest', day_name + ', ' + current_hour + ':' + current_minute)
                        config.write(configfile)
                    exit()

            except FileNotFoundError:
                # ---If external HD is not available ---#
                sub.Popen("kdialog --title 'Time Machine' --passivepopup 'Your external HD could not be found!' 5", shell=True)
                exit()


Object = Main()
Object.backup_now_pressed()
