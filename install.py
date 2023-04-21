import subprocess as sub
import os
import sys
import pathlib
import shutil
from pathlib import Path
sys.path.insert(1, 'src/')
from setup import *


class CLI:
    def __init__(self):
        # Install command
        # DEB 
        self.installDependencies = "flatpak '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev" 
        # ARCH
        # self.installDependenciesArch = "python3-pip flatpak"   
        # PIP
        self.installPip = "python3-pip"
        # PYSIDE6
        self.installPipPackages = "pyside6"
        # Extra: Flathub
        self.installFlathub = "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"

        self.getCurrentLocation = pathlib.Path().resolve() 
        self.src_backup_check = "src/desktop/backup_check.desktop"
        self.src_timemachine_desktop = f"src/desktop/{appNameClose}.desktop"
        self.src_migration_assistant = "src/desktop/migration_assistant.desktop"

        self.check_system()

    def check_system(self):
        usersDistro = os.popen("cat /etc/os-release").read()

        if "ubuntu" in usersDistro:
            self.requirements("ubuntu")

        elif "debian" in usersDistro:
            self.requirements("debian")

        elif "opensuse" in usersDistro:
            self.requirements("opensuse")

        elif "fedora" in usersDistro:
            self.requirements("fedora")

        elif "arch" in usersDistro:
            self.requirements("arch")

        else:
            print("No support OS found!")
            print("Please, Contact the developer :D")
            exit()

    def requirements(self,user_os):
        print("Users OS: " + user_os.capitalize())
        ################################################################################
        # Install pip (Ubuntu)
        ################################################################################
        try:
            print("Installing all the dependencies...")
            if user_os == "ubuntu":
                print("")
                sub.run(f"sudo apt -y update", shell=True)
                sub.run(f"sudo apt -y install {self.installPip}", shell=True)
                sub.run(f"sudo apt -y install {self.installDependencies}", shell=True)
            
            elif user_os == "debian":
                print("")
                sub.run(f"sudo apt -y update", shell=True)
                sub.run(f"sudo apt -y install {self.installPip}", shell=True)
                sub.run(f"sudo apt -y install {self.installDependencies}", shell=True)

            elif user_os == "opensuse":
                print("")
                sub.run(f"sudo zypper -y update", shell=True)
                sub.run(f"sudo zypper -y install {self.installPip}", shell=True)
                sub.run(f"sudo zypper -y install {self.installDependencies}", shell=True)

            elif user_os == "fedora":
                print("")
                sub.run(f"sudo dnf -y update", shell=True)
                sub.run(f"sudo dnf -y install {self.installPip}", shell=True)
                sub.run(f"sudo dnf -y install {self.installDependencies}", shell=True)

            elif user_os == "arch":
                print("")
                # sub.run(f"sudo pacman -S {self.installDependenciesArch}", shell=True)
                sub.run(f"sudo pacman -S python-pip", shell=True)
                sub.run(f"sudo pacman -S {self.installDependencies}", shell=True)

            ################################################################################
            # Install PySide6
            ################################################################################
            print("")
            print("Installing PySide6...")
            sub.run(f"pip install {self.installPipPackages}", shell=True)

        except:
            print("")
            print("Error trying to install dependencies!")
            print("Yóu need to manually install all dependencies:\n",
                "* python3-pip or python-pip\n",
                "* PySide6.")
            print("")
            pass

        # Install flathub
        try:
            print("Installing flathub...")
            sub.run(f"sudo {self.installFlathub}", shell=True)

        except:
            print("")
            print("Error trying to install Flathub!")
            print("Yóu need to manually install Flathub.")
            print("")
            pass

        self.begin_to_install()

    def begin_to_install(self):
        try:
            # Create autostart folder if necessary
            if not os.path.exists(src_autostart_folder_location):
                sub.run(f"{createCMDFolder} {src_autostart_folder_location}", shell=True)

            # Create applications folder
            if not os.path.exists(src_applications_location):
                sub.run(f"{createCMDFolder} {src_applications_location}", shell=True)

            print("Creating backup_check,desktop ...")
            with open(self.src_backup_check, "w") as writer: 
                writer.write(
                    f"[Desktop Entry]\n "
                    f"Type=Application\n "
                    f"Exec=/bin/python3 {homeUser}/.local/share/{appNameClose}/src/at_boot.py\n "
                    f"Hidden=false\n "
                    f"NoDisplay=false\n "
                    f"Name={appName}\n "
                    f"Comment={appName}'s manager before boot.\n "
                    f"Icon={src_restore_icon}")

            print(f"Creating {appNameClose}.desktop...")
            with open(self.src_timemachine_desktop, "w") as writer: 
                writer.write(
                    f"[Desktop Entry]\n "
                    f"Version=1.0\n "
                    f"Type=Application\n "
                    f"Name={appName}\n "
                    f"Comment=Backup your files with {appName}\n "
                    f"Icon={src_backup_icon}\n "
                    f"Exec=python3 {src_main_window_py}\n "
                    f"Path={homeUser}/.local/share/{appNameClose}/\n "
                    f"Categories=System\n "
                    f"StartupWMClass={(src_main_window_py).split('/')[-1]}\n "
                    f"Terminal=false")

            print(f"Creating Migration Assistant.desktop...")
            with open(self.src_migration_assistant, "w") as writer:
                writer.write(
                    f"[Desktop Entry]\n "
                    f"Version=1.0\n "
                    f"Type=Application\n "
                    f"Name=Migration Assistant\n "
                    f"Comment=Restore files/folders etc. from a {appName}'s backup\n "
                    f"Icon={src_migration_assistant_icon_212px}\n "
                    f"Exec=python3 {src_call_migration_assistant_py}\n "
                    f"Path={homeUser}/.local/share/{appNameClose}/src/\n "
                    f"Categories=System\n "
                    f"StartupWMClass={(src_migration_assistant_py).split('/')[-1]}\n "
                    f"Terminal=true")

            ################################################################################
            # Copy current Time Machine folder to user
            # Copy current folder to destination folder
            ################################################################################
            try:
                shutil.copytree(self.getCurrentLocation,
                                src_folder_timemachine)
            except FileExistsError:
                pass
            ################################################################################
            # Copy .desktop and .timemachine.desktop to destination folder
            ################################################################################
            try:
                shutil.copy(self.src_timemachine_desktop,
                            src_timemachine_desktop)
            except FileExistsError:
                pass
            ################################################################################
            # Copy migration_assistant.desktop to destination folder
            ################################################################################
            try:
                shutil.copy(self.src_migration_assistant,
                            src_migration_assistant_desktop)
            except FileExistsError:
                pass

            print("Program was successfully installed!")

        except FileNotFoundError:
            print(f"Error trying install {appName}!")
            exit()


main = CLI()
