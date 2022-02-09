import os
from pathlib import Path

home_user = str(Path.home())

os.system("rm -rf " + home_user + "/.local/share/timemachine/")
os.system("rm " + home_user + "/.local/share/applications/timemachine.desktop")
os.system("rm " + home_user + "/.config/autostart/backup_check.desktop")

print("Time Machine was removed!")
exit()
