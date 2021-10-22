import gi
import os
import getpass
import configparser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from pathlib import Path

home_user = str(Path.home())
user_name = getpass.getuser()
get_hd_name = os.listdir("/media/"+user_name+"/")
dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"

#----Read/Load user.config (backup automatically)----#
config = configparser.ConfigParser()
config.read(dst_user_config)
  
class StackWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title ="Time Machine")
        self.set_border_width(10)
  
        # Creating a box vertically oriented with a space of 100 pixel.
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 100)
        self.add(vbox)

        for storage in get_hd_name:
            storage = storage

        
        # Creating stack, transition type and transition duration.
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
  
        # # Creating the check button.
        # checkbutton = Gtk.CheckButton("Yes")
        # stack.add_titled(checkbutton, "check", "Check Button")
        
        read_user_config_where = config['SEARCH']['where']    
        read_user_config_type = config['SEARCH']['type']        
        for r, d, f in os.walk("/media/"+user_name+"/"+storage+"/14-10-21/"+read_user_config_where):
            for file_last in f:
                if file_last.lower().endswith(read_user_config_type):
                    file_last = file_last
                    print(file_last)

        label = Gtk.Label(label=file_last)
        stack.add_titled(label, "label", "14-10-21")

        label = Gtk.Label(label=file_last)
        stack.add_titled(label, "label", "13-10-21")

        # # Creating label .
        # label = Gtk.Label()
        # label.set_markup("<big>Hello World</big>")
        # stack.add_titled(label, "label", "Label")
  
        # Implementation of stack switcher.
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)
  
  
win = StackWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()