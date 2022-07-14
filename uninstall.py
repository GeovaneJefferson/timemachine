import subprocess as sub
from pathlib import Path

homeUser = str(Path.home())

try:
    sub.run(f"rm -rf {homeUser}/.local/share/timemachine/", shell=True)
    sub.run(f"rm {homeUser}/.local/share/applications/timemachine.desktop", shell=True)
    sub.run(f"rm {homeUser}/.config/autostart/backup_check.desktop", shell=True)

except Exception as error:
    print(error)
    exit()

print("App was successfully removed.")
exit()
