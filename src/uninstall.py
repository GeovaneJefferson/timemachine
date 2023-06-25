import subprocess as sub
import sys
sys.path.insert(1, 'src/')
from setup import *

try:
    sub.run(f"rm -rf {homeUser}/.local/share/{appNameClose}/", shell=True)
    sub.run(f"rm -f {dst_timemachine_desktop}", shell=True)
    sub.run(f"rm -f {dst_migration_assistant_desktop}", shell=True)
    sub.run(f"rm -f {dst_backup_check_desktop}", shell=True)

except Exception as error:
    print(error)
    exit()

print("App was successfully removed.")
exit()
