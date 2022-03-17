import subprocess as sub
from pathlib import Path

home_user = str(Path.home())

try:
    sub.run(f"rm -rf {home_user}/.local/share/timemachine/", shell=True)
    sub.run(f"rm {home_user}/.local/share/applications/desktop/timemachine.desktop", shell=True)
    sub.run(f"rm {home_user}/.config/autostart/backup_check.desktop", shell=True)
    sub.run(f"rm {home_user}/.local/share/kservices5/ServiceMenus/service.desktop", shell=True)

except:
    print("Error trying to remove Time Machine!")

print("Time Machine was removed!")
exit()
