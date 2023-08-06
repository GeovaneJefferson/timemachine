import subprocess as sub
import pathlib
from pathlib import Path

# Remember to change setup too!
HOME_USER=str(Path.home())
GET_CURRENT_LOCATION=pathlib.Path().resolve()

APP_NAME_CLOSE="timemachine"
DST_FILE_EXE_DESKTOP=f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP=f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"
DST_BACKUP_CHECK_DESKTOP=f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"


try:
    sub.run(f"rm -rf {HOME_USER}/.local/share/{APP_NAME_CLOSE}/", shell=True)
    sub.run(f"rm -f {DST_FILE_EXE_DESKTOP}", shell=True)
    sub.run(f"rm -f {DST_MIGRATION_ASSISTANT_DESKTOP}", shell=True)
    sub.run(f"rm -f {DST_BACKUP_CHECK_DESKTOP}", shell=True)

except Exception as error:
    print(error)
    exit()

print("App was successfully removed.")
exit()
