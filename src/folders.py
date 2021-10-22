import configparser
import sys
import os

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize    
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *

home_user = str(Path.home())
get_home_folders = os.listdir(home_user)
#src_user_config = "src/user.ini"

dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(dst_user_config)

class Options(QMainWindow):
    def __init__(self):
        super(Options, self).__init__()
        loadUi("src/options.ui",self)
        self.button_folders_cancel.clicked.connect(self.on_button_folders_cancel_clicked)
        self.button_folders_done.clicked.connect(self.on_button_folders_done_clicked)

        #---get user other folder---#
        folder_list = []
        for files in get_home_folders:
            if not files.startswith('.'):
                folder_list.append(files)

        #---remove default folders---#
        folder_list.remove("Desktop")
        folder_list.remove("Documents")
        folder_list.remove("Downloads")
        folder_list.remove("Pictures")
        folder_list.remove("Videos")
        folder_list.remove("Music")

        one_list = (folder_list[1])
        two_list = (folder_list[2])
        three_list = (folder_list[3])
        four_list = (folder_list[4])
        five_list = (folder_list[5])
        six_list = (folder_list[6])

        #---Clean---#
        one_list = str(one_list)
        one_list = one_list.replace("'","").replace("[","").replace("]","")            
        two_list = str(two_list)
        two_list = two_list.replace("'","").replace("[","").replace("]","")
        three_list = str(three_list)
        three_list = three_list.replace("'","").replace("[","").replace("]","")
        four_list = str(four_list)
        four_list = four_list.replace("'","").replace("[","").replace("]","")
        five_list = str(five_list)
        five_list = five_list.replace("'","").replace("[","").replace("]","")
        six_list = str(six_list)
        six_list = six_list.replace("'","").replace("[","").replace("]","")
        
        print(one_list, two_list, three_list, four_list, five_list, six_list)
        
        #---Set names to checkbox---#
        if  (bool(one_list)) == True:
            self.one_checkbox.setText(one_list)
            
            # cfgfile = open(dst_user_config, 'a')
            # config.set('FOLDER', one_list, '')
            # config.write(cfgfile)
            # cfgfile.close() 
            #self.c1.clicked.connect(self.on_desktop_checkbox_clicked)

            if  (bool(two_list)) == True:
                self.two_checkbox.setText(two_list)
                #self.c1.clicked.connect(self.on_desktop_checkbox_clicked)

                if  (bool(three_list)) == True:
                    self.three_checkbox.setText(three_list)
                    #self.c1.clicked.connect(self.on_desktop_checkbox_clicked)

                    if  (bool(four_list)) == True:
                        self.four_checkbox.setText(four_list)
                        #self.c1.clicked.connect(self.on_desktop_checkbox_clicked)                        

                        if  (bool(five_list)) == True:
                            self.five_checkbox.setText(five_list)
                            #self.c1.clicked.connect(self.on_desktop_checkbox_clicked)        
        
                            if  (bool(six_list)) == True:
                                self.six_checkbox.setText(six_list)
                                #self.c1.clicked.connect(self.on_desktop_checkbox_clicked)

        #----Read user.config(backup folders choose)----#
        reader_desktop_folder = config['FOLDER']['desktop']        
        if reader_desktop_folder == "true":
            self.desktop_checkbox.setChecked(True)
        else:
            pass

        reader_documents_folder = config['FOLDER']['documents']        
        if reader_documents_folder == "true":
            self.documents_checkbox.setChecked(True)
        else:
            pass

        reader_downloads_folder = config['FOLDER']['downloads']        
        if reader_downloads_folder == "true":
            self.downloads_checkbox.setChecked(True)
        else:
            pass

        reader_music_folder = config['FOLDER']['music']        
        if reader_music_folder == "true":
            self.music_checkbox.setChecked(True)
        else:
            pass

        reader_pictures_folder = config['FOLDER']['pictures']        
        if reader_pictures_folder == "true":
            self.pictures_checkbox.setChecked(True)
        else:
            pass

        reader_videos_folder = config['FOLDER']['videos']        
        if reader_videos_folder == "true":
            self.videos_checkbox.setChecked(True)
        else:
            pass

    def on_desktop_checkbox_clicked(self):
        if self.desktop_checkbox.isChecked():
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'desktop', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Desktop")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'desktop', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_documents_checkbox_clicked(self):
        if self.documents_checkbox.isChecked():
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'documents', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Documents")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'documents', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_downloads_checkbox_clicked(self):
        if self.downloads_checkbox.isChecked():
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'downloads', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Downloads")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'downloads', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_music_checkbox_clicked(self):
        if self.music_checkbox.isChecked():
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'music', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Music")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'music', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_pictures_checkbox_clicked(self):
        if self.pictures_checkbox.isChecked():
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'pictures', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Picture")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'pictures', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_videos_checkbox_clicked(self):
        if self.videos_checkbox.isChecked():
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'videos', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Videos")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(dst_user_config, 'w')
            config.set('FOLDER', 'videos', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_button_folders_cancel_clicked(self, button):
        exit()

    def on_button_folders_done_clicked(self, button):
        exit()

# main
app = QApplication(sys.argv)
main_screen = Options()
widget = QtWidgets.QStackedWidget()
appIcon = QIcon("src/icons/restore.png")
widget.setWindowIcon(appIcon)
widget.addWidget(main_screen)
widget.setFixedHeight(350)
widget.setFixedWidth(400)
widget.setWindowTitle("Folders")
widget.show()
sys.exit(app.exec_())


