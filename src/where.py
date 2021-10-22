import subprocess as sub
import configparser
import getpass
import os
import sys

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

home_user = str(Path.home())
user_name = getpass.getuser()
get_hd_name = os.listdir("/media/"+user_name+"/")

#PLACE TO SET HD NAME
hd_list = {"1":[],"2":[],"3":[],"4":[]};

#SRC LOCATION
src_where_py = "src/where.py"
src_user_config = "src/user.ini"
src_ui_where = "src/where.ui"
src_restore_small_icon = "src/icons/restore_small.png"
#DST LOCATION
# dst_where_py = home_user+"/.local/share/timemachine/src/where.py"
# dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"
#dst_ui_where = home_user+"/.local/share/timemachine/src/gui.ui"
#dst_restore_small_icon = home_user+"/.local/share/timemachine/src/icons/restore_small.png"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

class TimeMachine(QMainWindow):
    def __init__(self):
        super(TimeMachine, self).__init__()
        loadUi(src_ui_where,self)
        self.button_where_cancel.clicked.connect(self.on_button_where_cancel_clicked)
        self.button_where_refresh.clicked.connect(self.on_button_where_refresh_clicked)
                
        #GET HD
        turn = 0
        for storage in get_hd_name:
            turn = turn + 1
            if turn == 1:
                hd_list["1"].append(storage)
                self.option1 = (hd_list["1"])
                self.option1 = print(', '.join(self.option1))

            if turn == 2:
                hd_list["2"].append(storage)
                self.option2 = (hd_list["2"])
                self.option2 = print(', '.join(self.option2))

            if turn == 3:
                hd_list["3"].append(storage)
                self.option3 = (hd_list["3"])
                self.option3 = print(', '.join(self.option3))

            if turn == 4:
                hd_list["4"].append(storage)
                self.option4 = (hd_list["4"])
                self.option4 = print(', '.join(self.option4))

        self.option1 = (hd_list["1"])
        self.option2 = (hd_list["2"])
        self.option3 = (hd_list["3"])
        self.option4 = (hd_list["4"])

        #---Clean---#
        self.option1 = str(self.option1)
        self.option1 = self.option1.replace("'","").replace("[","").replace("]","")            
        self.option2 = str(self.option2)
        self.option2 = self.option2.replace("'","").replace("[","").replace("]","")
        self.option3 = str(self.option3)
        self.option3 = self.option3.replace("'","").replace("[","").replace("]","")
        self.option4 = str(self.option4)
        self.option4 = self.option4.replace("'","").replace("[","").replace("]","")

        #---Set buttons---#
        if  (bool(self.option1)) == True:
            label1_image = QLabel(self)
            pixmap = QPixmap(src_restore_small_icon)
            label1_image.setPixmap(pixmap)
            label1_image.setFixedSize(48, 48)
            label1_image.move(30, 35)
    
            button1 = QPushButton(self.option1, self.where_frame)
            button1.setFixedSize(280, 30)
            button1.move(60, 20)
            button1.clicked.connect(self.on_button1_clicked)
            button1.show()

            if (bool(self.option2)) == True:
                label2_image = QLabel(self)
                pixmap = QPixmap(src_restore_small_icon)
                label2_image.setPixmap(pixmap)
                label2_image.setFixedSize(48, 48)
                label2_image.move(30, 30*3)
        
                button2 = QPushButton(self.option2, self.where_frame)
                button2.setFixedSize(280, 30)
                button2.move(60, 75)
                button2.clicked.connect(self.on_button2_clicked)
                button2.show()                   
                
                if (bool(self.option3)) == True:
                    label3_image = QLabel(self)
                    pixmap = QPixmap(src_restore_small_icon)
                    label3_image.setPixmap(pixmap)
                    label3_image.setFixedSize(48, 48)
                    label3_image.move(50, 30*4)
            
                    button3 = QPushButton(self.option3, self.where_frame)
                    button3.setFixedSize(280, 30)
                    button3.move(100, 130)
                    button3.clicked.connect(self.on_button3_clicked)
                    button3.show()          

                    if (bool(self.option4)) == True:
                        label4_image = QLabel(self)
                        pixmap = QPixmap(src_restore_small_icon)
                        label4_image.setPixmap(pixmap)
                        label4_image.setFixedSize(48, 48)
                        label4_image.move(50, 30*5)
                
                        button4 = QPushButton(self.option4, self.where_frame)
                        button4.setFixedSize(280, 30)
                        button4.move(100, 185)
                        button4.clicked.connect(self.on_button4_clicked)
                        button4.show()      

    def on_button1_clicked(self, button):
        #----Read/Load user.config (backup automatically)----#
        cfgfile = open(src_user_config, 'w')
        config.set('EXTERNAL', 'hd', '/media/'+user_name+'/'+self.option1)
        config.set('EXTERNAL', 'name', self.option1)
        config.write(cfgfile)
        cfgfile.close()
        exit()

    def on_button2_clicked(self, button):
        #----Read/Load user.config (backup automatically)----#
        cfgfile = open(src_user_config, 'w')
        config.set('EXTERNAL', 'hd', '/media/'+user_name+'/'+self.option2)
        config.set('EXTERNAL', 'name', self.option2)
        config.write(cfgfile)
        cfgfile.close()
        exit()

    def on_button3_clicked(self, button):
        #----Read/Load user.config (backup automatically)----#
        cfgfile = open(src_user_config, 'w')
        config.set('EXTERNAL', 'hd', '/media/'+user_name+'/'+self.option3)
        config.set('EXTERNAL', 'name', self.option3)
        config.write(cfgfile)
        cfgfile.close()
        exit()

    def on_button4_clicked(self, button):
        #----Read/Load user.config (backup automatically)----#
        cfgfile = open(src_user_config, 'w')
        config.set('EXTERNAL', 'hd', '/media/'+user_name+'/'+self.option4)
        config.set('EXTERNAL', 'name', self.option4)
        config.write(cfgfile)
        cfgfile.close()
        exit()

    def on_button_where_cancel_clicked(self, button):
        exit()

    def on_button_where_refresh_clicked(self, button):
        sub.Popen("python3 "+src_where_py,shell=True)
        exit()

# main
app = QApplication(sys.argv)
main_screen = TimeMachine()
widget = QtWidgets.QStackedWidget()
appIcon = QIcon("src/icons/restore.png")
widget.setWindowIcon(appIcon)
widget.addWidget(main_screen)
widget.setFixedHeight(325)
widget.setFixedWidth(400)
widget.setWindowTitle("External HD")
widget.show()
sys.exit(app.exec_())