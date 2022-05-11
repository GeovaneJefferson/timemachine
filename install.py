import subprocess as sub
import os
import pathlib
import shutil
from pathlib import Path


class CLI:
    def __init__(self):
        # Folders
        self.home_user = str(Path.home())
        self.getCurrentLocation = pathlib.Path().resolve()  # Current folder

        # Compatible system
        self.ubuntu = False
        self.debian = False
        self.opensuse = False
        self.fedora = False
        self.arch = False

        # Terminal commands
        self.createCmd = "mkdir"

        # Default
        # Current folder
        self.src_backup_check = "src/desktop/backup_check.desktop"
        self.src_timemachine_desktop = "src/desktop/timemachine.desktop"

        # Destination folder
        self.dst_venv_loc = f"{self.home_user}/.local/share/timemachine/venv"
        self.dst_folder_timemachine = f"{self.home_user}/.local/share/timemachine"
        self.dst_timemachine_desktop = f"{self.home_user}/.local/share/applications/timemachine.desktop"
        self.dst_kde_service = f"{self.home_user}/.local/share/kservices5/ServiceMenus"
        self.restore_icon = f"{self.home_user}/.local/share/timemachine/src/icons/restore_48.png"
        self.create_autostart_folder = f"{self.home_user}/.config/autostart"

        self.check_system()

    def check_system(self):
        ################################################################################
        ## Check system (Ubuntu, Opensuse etc.)
        ################################################################################
        # sub.run("pkexec sudo", shell=True)
        output = os.popen("cat /etc/os-release") # uname -v
        output = output.read()

        if "ubuntu" in output:
            self.ubuntu = True

        elif "debian" in output:
            self.debian = True

        elif "opensuse" in output:
            self.opensuse = True

        elif "fedora" in output:
            self.fedora = True

        elif "arch" in output:
            self.arch = True

        self.requeriments()

    def requeriments(self):
        ################################################################################
        ## Install pip (Ubuntu)
        ################################################################################
        print("Python3 pip need to be installed.")

        if self.ubuntu or self.debian:
            try:
                print("")
                sub.run("sudo apt install python3-pip libnotify-bin", shell=True)
                print("Python3-pip was installed.")

            except :
                print("Error trying to install python3-pip!")
                exit()

        ################################################################################
        ## Install pip (Opensuse)
        ################################################################################
        elif self.opensuse:
            try:
                print("")
                sub.run("sudo zypper install python3-pip", shell=True)
                print("Python3-pip was installed.")

            except:
                print("Error trying to install python3-pip!")
                exit()

        ################################################################################
        ## Install pip (Fedora)
        ################################################################################
        elif self.fedora:
            try:
                print("")
                sub.run("sudo dnf install python3-pip", shell=True)
                print("Python3-pip was installed.")

            except:
                print("Error trying to install python3-pip!")
                exit()

        elif self.arch:
            try:
                print("")
                sub.run("sudo pacman -Sy python-pip", shell=True)
                print("Python3-pip was installed.")

            except:
                print("Error trying to install python3-pip!")
                exit()

        ################################################################################
        ## Install PySide6
        ################################################################################
        if self.ubuntu or self.opensuse or self.fedora or self.arch or self.debian:
            try:
                print("")
                print("PySide6 pip need to be installed.")
                sub.run("pip install pyside6", shell=True)

            except :
                print("Error trying to install PySide6!")
                exit()

        else:
            print("None compatible system found.")
            print("Could not install python3-pip and PySide6.")
            print("You have to install manually..")

        self.begin_to_install()

    def begin_to_install(self):
        ################################################################################
        ## Create autostart folder
        ################################################################################
        try:
            if os.path.exists(self.create_autostart_folder):
                pass
            else:
                sub.run(f"{self.createCmd} {self.create_autostart_folder}", shell=True)

        except FileNotFoundError:
            print("Error trying to create autostart folders insise users home!")

        ################################################################################
        ## Create applications folder
        ################################################################################
        try:
            if os.path.exists(f"{self.home_user}/.local/share/applications/"):
                pass
            else:
                sub.run(f"{self.createCmd} {self.home_user}/.local/share/applications/", shell=True)
                
        except FileNotFoundError:
            print("Error trying to create applications folder inside users home!")
            pass

        ################################################################################
        ## Copy all .desktop 
        ################################################################################
        ################################################################################
        ## Backup cheker .desktop
        ################################################################################
        with open(self.src_backup_check, "w") as writer:    # Modify backup_check.desktop and add username to it
            writer.write(
                f"[Desktop Entry]\n "
                f"Type=Application\n "
                f"Exec=/bin/python3 {self.home_user}/.local/share/timemachine/src/at_boot.py\n"
                f"Hidden=false\n "
                f"NoDisplay=false\n "
                f"Name=Time Machine\n "
                f"Comment=Backup your files\n "
                f"Icon={self.restore_icon}")

        ################################################################################
        ## Time Machine entry .desktop
        ################################################################################
        with open(self.src_timemachine_desktop, "w") as writer:     # Modify timemachine.desktop and add username to it
            writer.write(
                f"[Desktop Entry]\n "
                f"Version=1.0\n "
                f"Type=Application\n "
                f"Name=Time Machine\n "
                f"Comment=Backup your files\n "
                f"Icon={self.home_user}/.local/share/timemachine/src/icons/restore.png\n "
                f"Exec=python3 {self.home_user}/.local/share/timemachine/src/gui.py\n "
                f"Path={self.home_user}/.local/share/timemachine/\n "
                f"Categories=System\n "
                f"StartupWMClass=Gui.py\n "
                f"Terminal=false")
        
        try:
            # Copy current Time Machine folder to user
            shutil.copytree(self.getCurrentLocation, self.dst_folder_timemachine)       # Copy current folder to destination folder
            shutil.copy(self.src_timemachine_desktop, self.dst_timemachine_desktop)     # Copy .desktop and .timemachine.desktop to destination folder

            sub.run(f"rm -rf {self.dst_venv_loc}", shell=True)        # Remove venv folder from user

            print("Program was installed!")
 
        except FileExistsError:
            print("Program is already installed!")

        exit()


app = CLI()
