import subprocess as sub
import pathlib
from pathlib import Path
import sqlite3
import shutil


# Remember to change setup too!
HOME_USER = str(Path.home())
GET_CURRENT_LOCATION = pathlib.Path().resolve()

APP_NAME_CLOSE = "timemachine"
DST_FILE_EXE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP = f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"
DST_BACKUP_CHECK_DESKTOP = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"
SRC_USER_CONFIG_DB = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/ini/config.db"


try:
    # Disable system tray

    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()
        
    cursor.execute(f'''
        INSERT OR REPLACE INTO SYSTEMTRAY (key, value)
        VALUES (?, ?)
    ''', ('system_tray', 'False'))

    conn.commit()
    conn.close()

    command = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/"
    # Remove dir
    # sub.run(["rm", "-rf", command])
    shutil.rmtree(command)

    command = DST_FILE_EXE_DESKTOP
    sub.run(["rm", "-rf", command])
    # Remove dir
    shutil.rmtree(command)

    command = DST_MIGRATION_ASSISTANT_DESKTOP
    # sub.run(["rm", "-rf", command])
    # Remove dir
    shutil.rmtree(command)

    command = DST_BACKUP_CHECK_DESKTOP
    # sub.run(["rm", "-rf", command])
    # Remove dir
    shutil.rmtree(command)
except Exception as error:
    print(error)
    exit()

print("App was successfully removed.")
exit()
