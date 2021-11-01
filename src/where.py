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

user_name = getpass.getuser()
home_user = str(Path.home())
show_all_hd = os.listdir("/media/"+user_name+"/")

#SRC LOCATION
src_where_py = "src/where.py"
src_user_config = "src/user.ini"
src_ui_where = "src/where.ui"
src_restore_small_icon = "src/icons/restore_small.png"

#DST LOCATION
# src_where_py = home_user+"/.local/share/timemachine/src/where.py"
# src_user_config = home_user+"/.local/share/timemachine/src/user.ini"
# src_ui_where = home_user+"/.local/share/timemachine/src/where.ui"
# src_restore_small_icon = home_user+"/.local/share/timemachine/src/icons/restore_small.png"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

class TimeMachine(QMainWindow):
    def __init__(self):
        super(TimeMachine, self).__init__()
        loadUi(src_ui_where,self)
        self.button_where_cancel.clicked.connect(self.on_button_where_cancel_clicked)
        self.button_where_refresh.clicked.connect(self.on_button_where_refresh_clicked)

        #ADD BUTTONS AND IMAGES FOR EACH HD
        vertical = 20
        vertical_img = 32
        for self.storage in show_all_hd:
            print(self.storage)
            label_image = QLabel(self)
            pixmap = QPixmap(src_restore_small_icon)
            label_image.setPixmap(pixmap)
            label_image.setFixedSize(48, 48)
            label_image.move(30, vertical_img)
            vertical_img = vertical_img + 50
    
            button = QPushButton(self.storage, self.where_frame)
            button.setFixedSize(280, 30)
            button.move(60, vertical)
            vertical = vertical + 50
            text = button.text()
            button.show()
            button.clicked.connect(lambda ch, text=text : self.on_button_clicked(text))

    def on_button_clicked(self, choose):
        #----Read/Load user.config (backup automatically)----#
        cfgfile = open(src_user_config, 'w')
        config.set('EXTERNAL', 'hd', '/media/'+user_name+'/'+choose)
        config.set('EXTERNAL', 'name', choose)
        config.write(cfgfile)
        cfgfile.close()
        exit()

    def on_button_where_cancel_clicked(self):
        exit()

    def on_button_where_refresh_clicked(self):
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