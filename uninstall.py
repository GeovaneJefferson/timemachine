import subprocess as sub
import pathlib
from pathlib import Path

# Remember to change setup too!
HOME_USER = str(Path.home())
GET_CURRENT_LOCATION = pathlib.Path().resolve()

APP_NAME_CLOSE = "timemachine"
DST_FILE_EXE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP = f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"
DST_BACKUP_CHECK_DESKTOP = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"


try:
    command = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/"
    sub.run(["rm", "-rf", command])

    command = DST_FILE_EXE_DESKTOP
    sub.run(["rm", "-rf", command])

    command = DST_MIGRATION_ASSISTANT_DESKTOP
    sub.run(["rm", "-rf", command])

    command = DST_BACKUP_CHECK_DESKTOP
    sub.run(["rm", "-rf", command])

except Exception as error:
    print(error)
    exit()

print("App was successfully removed.")
exit()
