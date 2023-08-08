import subprocess as sub
import os
import shutil
import pathlib
from pathlib import Path


# Remember to change setup too!
HOME_USER = str(Path.home())
GET_CURRENT_LOCATION = pathlib.Path().resolve()

APP_NAME_CLOSE = "timemachine"
APP_NAME = "Time Machine"
APP_VERSION = "v1.1.7.03 dev"

CREATE_CMD_FOLDER = "mkdir"

DST_FOLDER_INSTALL = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}"
DST_APPLICATIONS_LOCATION = f"{HOME_USER}/.local/share/applications"
DST_FILE_EXE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
SRC_AUTOSTARTFOLDER_LOCATION=f"{HOME_USER}/.config/autostart"

SRC_MAIN_WINDOW_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/mainwindow.py"
SRC_CALL_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/call_migration_assistant.py"
SRC_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/migration_assistant.py"
SRC_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/migration_assistant.py"

SRC_MIGRATION_ASSISTANT_ICON_212PX = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/migration_assistant_212px.png"

DST_BACKUP_CHECK_DESKTOP = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"
SRC_TIMEMACHINE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP = f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"

SRC_RESTORE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/restore_64px.svg"
SRC_BACKUP_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/backup_128px.png"


# # DEB
# # ARCH
# # INSTALLDEPENDECIESArch="python3-pip flatpak"
# # PIP
# INSTALL_PIP3="python3-pip"
# # User distro name
# USERS_DISTRO_NAME=os.popen("cat /etc/os-release").read()  # "ubuntu" in USERDISTRONAME:

class CLI:
    def __init__(self):
        pass

    def install_dependencies(self):
        # Depedencies
        try:
            sub.run(f"pip install -r {GET_CURRENT_LOCATION}/requirements.txt", shell=True)

        except FileNotFoundError as e:
            print(e)
            exit()

    def copy_files(self):
        try:
            # Copy current folder to the destination folder
            shutil.copytree(GET_CURRENT_LOCATION, DST_FOLDER_INSTALL)

        except FileExistsError as e:
            pass

    def create_application_files(self):
        # Create .local/share/applications
        if not os.path.exists(DST_APPLICATIONS_LOCATION):
            sub.run(f"{CREATE_CMD_FOLDER} {DST_APPLICATIONS_LOCATION}", shell=True)

        # Send to DST_FILE_EXE_DESKTOP
        with open(SRC_TIMEMACHINE_DESKTOP, "w") as writer:
            writer.write(
                f"[Desktop Entry]\n "
                f"Version={APP_VERSION}\n "
                f"Type=Application\n "
                f"Name={APP_NAME}\n "
                f"Comment=Backup your files with {APP_NAME}\n "
                f"Icon={SRC_BACKUP_ICON}\n "
                f"Exec=python3 {SRC_MAIN_WINDOW_PY}\n "
                f"Path={HOME_USER}/.local/share/{APP_NAME_CLOSE}/\n "
                f"Categories=System\n "
                f"StartupWMClass={SRC_MAIN_WINDOW_PY.split('/')[-1]}\n "
                f"Terminal=false")

        # Migration_assistant .desktop
        with open(DST_MIGRATION_ASSISTANT_DESKTOP, "w") as writer:
            writer.write(
                f"[Desktop Entry]\n "
                f"Version={APP_VERSION}\n "
                f"Type=Application\n "
                f"Name=Migration Assistant\n "
                f"Comment=Restore files/folders etc. from a {APP_NAME}'s backup\n "
                f"Icon={SRC_MIGRATION_ASSISTANT_ICON_212PX}\n "
                f"Exec=python3 {SRC_CALL_MIGRATION_ASSISTANT_PY}\n "
                f"Path={HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/\n "
                f"Categories=System\n "
                f"StartupWMClass={(SRC_MIGRATION_ASSISTANT_PY).split('/')[-1]}\n "
                f"Terminal=true")

    def create_backup_checker_desktop(self):
        # Create autostart folder if necessary
        if not os.path.exists(SRC_AUTOSTARTFOLDER_LOCATION):
            sub.run(f"{CREATE_CMD_FOLDER} {SRC_AUTOSTARTFOLDER_LOCATION}", shell=True)

        # Edit file startup with system
        with open(DST_BACKUP_CHECK_DESKTOP, "w") as writer:
            writer.write(
                f"[Desktop Entry]\n "
                f"Type=Application\n "
                f"Exec=/bin/python3 {HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/at_boot.py\n "
                f"Hidden=false\n "
                f"NoDisplay=false\n "
                f"Name={APP_NAME}\n "
                f"Comment={APP_NAME}'s manager before boot.\n "
                f"Icon={SRC_RESTORE_ICON}")
            
            
if __name__ == '__main__':
    MAIN=CLI()

    try:
        # Install dependencies
        MAIN.install_dependencies()
        # Begin installation
        MAIN.copy_files()
        # Create exe files
        MAIN.create_application_files()
        # Create backup checker.dekstop
        MAIN.create_backup_checker_desktop()
    except Exception as e:
        print(f"Error:", e)
    
    print("Program was successfully installed!")

    # Quit
    exit()
