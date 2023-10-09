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
APP_VERSION = "v1.1.6.094 dev"

CREATE_CMD_FOLDER = "mkdir"

DST_FOLDER_INSTALL = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}"
DST_APPLICATIONS_LOCATION = f"{HOME_USER}/.local/share/applications"
DST_FILE_EXE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
SRC_AUTOSTARTFOLDER_LOCATION=f"{HOME_USER}/.config/autostart"

SRC_MAIN_WINDOW_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/main_window.py"
SRC_CALL_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/call_migration_assistant.py"
SRC_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/migration_assistant.py"

SRC_MIGRATION_ASSISTANT_ICON_212PX = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/migration_assistant_212px.png"

DST_BACKUP_CHECK_DESKTOP = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"
SRC_TIMEMACHINE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP = f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"

SRC_RESTORE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/restore_64px.svg"
SRC_BACKUP_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/backup_128px.png"


USERS_DISTRO_NAME = os.popen("cat /etc/os-release").read()  # "ubuntu" in USERDISTRONAME:

def install_dependencies():
    # Depedencies
    try:
        command = f"{GET_CURRENT_LOCATION}/requirements.txt"
        sub.run(["pip", "install", "-r", command])

        # Arch
        if 'arch' in USERS_DISTRO_NAME:
            command = "qt6-wayland"
            
            # Check if the package is already installed
            try:
                sub.run(["pacman", "-Qq", command], check=True)
                print(f"{command} is already installed.")
                
            except sub.CalledProcessError:
                # If not installed, install the package
                sub.run(["sudo", "pacman", "-S", command], check=True)

    except FileNotFoundError as e:
        print(e)
        exit()

def copy_files():
    try:
        # Copy current folder to the destination folder
        shutil.copytree(GET_CURRENT_LOCATION, DST_FOLDER_INSTALL)
        
    except FileExistsError:
        pass

def create_application_files():
    # Create .local/share/applications
    if not os.path.exists(DST_APPLICATIONS_LOCATION):
        command = DST_APPLICATIONS_LOCATION
        sub.run(["mkdir", command])

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

def create_backup_checker_desktop():
    # Create autostart folder if necessary
    if not os.path.exists(SRC_AUTOSTARTFOLDER_LOCATION):
        command = SRC_AUTOSTARTFOLDER_LOCATION
        sub.run(["mkdir", command])

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
    try:
        # Install dependencies
        print("Installing dependencies...")
        install_dependencies()
        
        # Begin installation
        print()
        print(f"Copyng files to {HOME_USER}/.local/share/{APP_NAME_CLOSE}/...")
        copy_files()

        # Create exe files
        print(f"Creating {APP_NAME_CLOSE}.desktop...")
        create_application_files()
        
        # Create backup checker.dekstop
        print(f"Creating backup_checker.desktop...")
        create_backup_checker_desktop()

    except Exception as e:
        print(e)
    
    print()
    print("Program was successfully installed!")
    exit()
