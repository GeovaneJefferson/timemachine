import gi
import getpass
import subprocess as sub
import configparser

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path

home_user = str(Path.home())
user_name = getpass.getuser()
restore_show_file = home_user+"/.local/share/timemachine/src/restore_show_file.py"
dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"
dst_restore_icon = home_user+"/.local/share/timemachine/src/icons/restore.png"
dst_desktop_icon = home_user+"/.local/share/timemachine/src/icons/desktop.png"
dst_documents_icon = home_user+"/.local/share/timemachine/src/icons/documents.png"
dst_music_icon = home_user+"/.local/share/timemachine/src/icons/music.png"
dst_pictures_icon = home_user+"/.local/share/timemachine/src/icons/pictures.png"
dst_videos_icon = home_user+"/.local/share/timemachine/src/icons/videos.png"

#----Read/Load user.config (backup automatically)----#
config = configparser.ConfigParser()
config.read(dst_user_config)

class LabelWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Type of the file(s):")
        self.set_default_size(-1, -1)
        self.set_border_width(45)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_resizable(False)
        self.set_icon_from_file(dst_restore_icon)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        image_desktop = Gtk.Image()
        image_desktop.set_from_file(dst_desktop_icon)

        image_documents = Gtk.Image()
        image_documents.set_from_file(dst_documents_icon)

        image_music = Gtk.Image()
        image_music.set_from_file(dst_music_icon)

        image_pictures = Gtk.Image()
        image_pictures.set_from_file(dst_pictures_icon)

        image_videos = Gtk.Image()
        image_videos.set_from_file(dst_videos_icon)

        button_desktop = Gtk.Button(label="Text")
        button_desktop.connect("clicked", self.on_text_button_clicked)

        button_documents = Gtk.Button(label="Image")
        button_documents.connect("clicked", self.on_text_button_clicked)

        button_music = Gtk.Button(label="Audio")
        button_music.connect("clicked", self.on_text_button_clicked)

        button_pictures = Gtk.Button(label="Video")
        button_pictures.connect("clicked", self.on_text_button_clicked)

        button_videos = Gtk.Button(label="Else")
        button_videos.connect("clicked", self.on_text_button_clicked)

        grid.attach(image_desktop, 0, 0, 1, 1)
        grid.attach(button_desktop, 0, 1, 1, 1)
        grid.attach(image_documents, 1, 0, 1, 1)
        grid.attach(button_documents, 1, 1, 1, 1)
        grid.attach(image_music, 2, 0, 1, 1)
        grid.attach(button_music, 2, 1, 1, 1)
        grid.attach(image_pictures, 3, 0, 1, 1)
        grid.attach(button_pictures, 3, 1, 1, 1)
        grid.attach(image_videos, 4, 0, 1, 1)
        grid.attach(button_videos, 4, 1, 1, 1)

    def on_text_button_clicked(self, button):
        #----Update User.conf settings (User settings)----#
        cfgfile = open(dst_user_config, 'w')
        config.set('SEARCH', 'type', '.txt')
        config.write(cfgfile)
        cfgfile.close()
        sub.Popen("python3 "+restore_show_file,shell=True)
        exit()

window = LabelWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()