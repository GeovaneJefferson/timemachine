import shutil
import os
import pathlib
from pathlib import Path

home_user = str(Path.home())
#CURRENT FOLDER
src_current_location = pathlib.Path().resolve()

src_timemachine_desktop = "src/timemachine.desktop"
dst_folder_timemachine = home_user+"/.local/share/timemachine"

src_backup_check = "src/backup_check.desktop"
dst_timemachine_desktop = home_user+"/.local/share/applications/timemachine.desktop"
dst_restore_icon = home_user+"/.local/share/timemachine/src/icons/restore_48.png"
create_autostart_folder = home_user+"/.config/autostart"

#----Create file if do not exist----#
if os.path.exists(create_autostart_folder):
    pass
else:
    os.system("mkdir "+create_autostart_folder)

#----Create/modify .desktop and timemachine.desktop to get username----#
with open(src_backup_check, "w") as writer:
    writer.write("[Desktop Entry]\nType=Application\nExec=/bin/python3 "+home_user+"/.local/share/timemachine/src/backup_check.py\nHidden=false\nNoDisplay=false\nName=Time Machine\nComment=Backup your files\nIcon="+dst_restore_icon)

#.DESKTOP
with open(src_timemachine_desktop, "w") as writer:
    writer.write("[Desktop Entry]\nVersion=1.0\nType=Application\nName=Time Machine\nIcon="+home_user+"/.local/share/timemachine/src/icons/restore.png\nExec=python3 "+home_user+"/.local/share/timemachine/gui.py\nPath="+home_user+"/.local/share/timemachine/\nCategories=Settings\nStartupWMClass=Gui.py\nTerminal=false")

#---Set current folder location and copy to file---#
shutil.copytree(src_current_location, dst_folder_timemachine)
#---copy app from folder to the system
shutil.copy(src_timemachine_desktop,dst_timemachine_desktop)
print("Program was installed!")
exit()