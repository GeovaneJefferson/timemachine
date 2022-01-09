import shutil
import os
import pathlib
from pathlib import Path

home_user = str(Path.home())
# CURRENT FOLDER
src_current_location = pathlib.Path().resolve()
src_timemachine_desktop = "src/timemachine.desktop"
src_backup_check = "src/backup_check.desktop"

dst_folder_timemachine = home_user + "/.local/share/timemachine"
dst_timemachine_desktop = home_user + "/.local/share/applications/timemachine.desktop"
dst_restore_icon = home_user + "/.local/share/timemachine/src/icons/restore_48.png"
create_autostart_folder = home_user + "/.config/autostart"

# INSTALL LIBNOTIFY TO GET NOTIFICATION
print("Please, enter your password. Libnotify needs to be installed.")
os.system("sudo zypper install libnotify-bin -y")

# ----Create file if do not exist----#
if os.path.exists(create_autostart_folder):
    pass
else:
    os.system("mkdir " + create_autostart_folder)

# ----Create/modify .desktop and timemachine.desktop to get username----#
with open(src_backup_check, "w") as writer:
    writer.write("[Desktop Entry]\n Type=Application\n Exec=/bin/python3 " + home_user+ "/.local/share/timemachine/src/backup_check.py\n Hidden=false\n NoDisplay=false\n Name=Time Machine\n Comment=Backup your files\n Icon="+ dst_restore_icon)

# .DESKTOP
with open(src_timemachine_desktop, "w") as writer:
    writer.write("[Desktop Entry]\n Version=1.0\n Type=Application\n Name=Time Machine\n Comment=Backup your files\n Icon="+ home_user + '/.local/share/timemachine/src/icons/restore.png\n Exec=python3 '+ home_user + '/.local/share/timemachine/src/gui.py\n Path='+ home_user + "/.local/share/timemachine/\n Categories=Settings\n StartupWMClass=Gui.py\n Terminal=false")

# ---Set current folder location and copy to file---#
shutil.copytree(src_current_location, dst_folder_timemachine)
# ---copy app from folder to the system
shutil.copy(src_timemachine_desktop, dst_timemachine_desktop)
print("Program was installed!")
exit()
