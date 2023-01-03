import subprocess as sub
import os
import pathlib
import shutil
from pathlib import Path


class CLI:
    def __init__(self):
        # Install command
        # DEB 
        self.installDependencies = "python3-pip flatpak '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev" 
        # ARCH
        self.installDependenciesArch = "python3-pip flatpak"   
        # PIP
        self.installPipPackages = "pyside6"
        # Extra: Flathub
        self.installFlathub = "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"

        # Folders
        self.home_user = str(Path.home())
        self.getCurrentLocation = pathlib.Path().resolve()  # Current folder

        # Terminal commands
        self.createCmd = "mkdir"

        # Default
        # Current folder
        self.src_backup_check = "src/desktop/backup_check.desktop"
        self.src_timemachine_desktop = "src/desktop/timemachine.desktop"
        self.src_migration_assistant = "src/desktop/migration_assistant.desktop"

        # Destination folder
        self.dst_folder_timemachine = f"{self.home_user}/.local/share/timemachine"
        self.dst_timemachine_desktop = f"{self.home_user}/.local/share/applications/timemachine.desktop"
        self.dst_migration_assistant = f"{self.home_user}/.local/share/applications/migration_assistant.desktop"
        self.restore_icon = f"{self.home_user}/.local/share/timemachine/src/icons/restore_48.png"
        self.create_autostart_folder = f"{self.home_user}/.config/autostart"

        self.check_system()

    def check_system(self):
        # Check User system (Ubuntu, Opensuse etc.)
        output = os.popen("cat /etc/os-release")  # uname -v
        output = output.read()

        # Types of systems
        if "ubuntu" in output:
            self.requirements("ubuntu")

        elif "debian" in output:
            self.requirements("debian")

        elif "opensuse" in output:
            self.requirements("opensuse")

        elif "fedora" in output:
            self.requirements("fedora")

        elif "arch" in output:
            self.requirements("arch")

        else:
            print("No support OS found!")
            print("Please, Contact the developer :D")
            exit()

    def requirements(self, user_os):
        print(f"Users OS: {(user_os.capitalize())}")
        ################################################################################
        # Install pip (Ubuntu)
        ################################################################################
        try:
            print("Installing all the dependencies...")
            # Ubuntu
            if user_os == "ubuntu":
                print("")
                sub.run(f"sudo apt -y update", shell=True)
                sub.run(f"sudo apt -y install {self.installDependencies}", shell=True)
            
            # Debian
            elif user_os == "debian":
                print("")
                sub.run(f"sudo apt -y update", shell=True)
                sub.run(f"sudo apt -y install {self.installDependencies}", shell=True)

            # Opensuse
            elif user_os == "opensuse":
                print("")
                sub.run(f"sudo zypper -y update", shell=True)
                sub.run(f"sudo zypper -y install {self.installDependencies}", shell=True)

            # Fedora
            elif user_os == "fedora":
                print("")
                sub.run(f"sudo dnf -y update", shell=True)
                sub.run(f"sudo dnf -y install {self.installDependencies} qt5-qtbase-devel", shell=True)

            # Arch
            elif user_os == "arch":
                print("")
                sub.run(f"sudo pacman -S {self.installDependenciesArch}", shell=True)

            ################################################################################
            # Install PySide6
            ################################################################################
            print("")
            print("Installing PySide6 and pip...")
            sub.run(f"pip install {self.installPipPackages}", shell=True)

        except:
            print("Error trying to install dependencies!")
            exit()

        # Install flathub
        try:
            print("Installing flathub...")
            sub.run(f"sudo {self.installFlathub}", shell=True)

        except:
            pass

        self.begin_to_install()

    def begin_to_install(self):
        try:
            # Create autostart folder if necessary
            if not os.path.exists(self.create_autostart_folder):
                sub.run(f"{self.createCmd} {self.create_autostart_folder}", shell=True)

            # Create applications folder
            if not os.path.exists(f"{self.home_user}/.local/share/applications/"):
                sub.run(f"{self.createCmd} {self.home_user}/.local/share/applications/", shell=True)

            ################################################################################
            # Copy all .desktop
            # Backup checker .desktop
            ################################################################################
            with open(self.src_backup_check, "w") as writer:  # Modify backup_check.desktop and add username to it
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
            # Time Machine entry .desktop
            ################################################################################
            with open(self.src_timemachine_desktop, "w") as writer:  # Modify timemachine.desktop and add username to it
                writer.write(
                    f"[Desktop Entry]\n "
                    f"Version=1.0\n "
                    f"Type=Application\n "
                    f"Name=Time Machine\n "
                    f"Comment=Backup your files\n "
                    f"Icon={self.home_user}/.local/share/timemachine/src/icons/backup_128px.png\n "
                    f"Exec=python3 {self.home_user}/.local/share/timemachine/src/mainwindow.py\n "
                    f"Path={self.home_user}/.local/share/timemachine/\n "
                    f"Categories=System\n "
                    f"StartupWMClass=mainwindow.py\n "
                    f"Terminal=false")

            ################################################################################
            # Call Migration Assistant entry .desktop
            ################################################################################
            with open(self.src_migration_assistant, "w") as writer:
                writer.write(
                    f"[Desktop Entry]\n "
                    f"Version=1.0\n "
                    f"Type=Application\n "
                    f"Name=Migration Assistant\n "
                    f"Comment=Restore settings from a Time Machine backup\n "
                    f"Icon={self.home_user}/.local/share/timemachine/src/icons/migration_assistant_96px.png\n "
                    f"Exec=python3 {self.home_user}/.local/share/timemachine/src/call_migration_assistant.py\n "
                    f"Path={self.home_user}/.local/share/timemachine/src/\n "
                    f"Categories=System\n "
                    f"StartupWMClass=migration_assistant.py\n "
                    f"Terminal=true")

            ################################################################################
            # Copy current Time Machine folder to user
            # Copy current folder to destination folder
            ################################################################################
            shutil.copytree(self.getCurrentLocation,
                            self.dst_folder_timemachine)

            ################################################################################
            # Copy .desktop and .timemachine.desktop to destination folder
            ################################################################################
            shutil.copy(self.src_timemachine_desktop,
                        self.dst_timemachine_desktop)

            ################################################################################
            # Copy migration_assistant.desktop to destination folder
            ################################################################################
            shutil.copy(self.src_migration_assistant,
                        self.dst_migration_assistant)

            print("Program was installed!")

        except FileNotFoundError:
            print("Error trying install Time Machine")
            exit()


app = CLI()
