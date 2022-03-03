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

        # Terminal commands
        self.createCmd = 'mkdir '

        # Default
        # Current folder
        self.src_backup_check = "src/desktop/backup_check.desktop"
        self.src_timemachine_desktop = "src/desktop/timemachine.desktop"
        self.src_service = "src/desktop/service.desktop"

        # Destination folder
        self.dst_venv_loc = f"{self.home_user}/.local/share/timemachine/venv"
        self.dst_folder_timemachine = f"{self.home_user}/.local/share/timemachine"
        self.dst_timemachine_desktop = f"{self.home_user}/.local/share/applications/timemachine.desktop"
        self.dst_kde_service = f"{self.home_user}/.local/share/kservices5/ServiceMenus/"
        self.restore_icon = f"{self.home_user}/.local/share/timemachine/src/icons/restore_48.png"
        self.create_autostart_folder = f"{self.home_user}/.config/autostart"

        self.begin_to_install()

    def begin_to_install(self):
        # Create file if file do not exist
        if os.path.exists(self.create_autostart_folder):
            pass
        else:
            sub.run(self.createCmd + self.create_autostart_folder, shell=True)

        with open(self.src_backup_check, "w") as writer:    # Modify backup_check.desktop and add username to it
            writer.write(
                f"[Desktop Entry]\n "
                f"Type=Application\n "
                f"Exec=/bin/python3 {self.home_user}/.local/share/timemachine/src/backup_check.py\n "
                f"Hidden=false\n "
                f"NoDisplay=false\n "
                f"Name=Time Machine\n "
                f"Comment=Backup your files\n "
                f"Icon={self.restore_icon}")

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
        
        with open(self.src_service, "w") as writer:     # Modify service.desktop and add username to it
            writer.write(
                f"[Desktop Entry]\n "
                f"Version=1.0\n "
                f"Type=Service\n "
                f"ServiceTypes=KonqPopupMenu/Plugin\n "
                f"MimeType=application/octet-stream;\n "
                f"Actions=EnterTimeMachine;\n "
                f"X-KDE-Priority=TopLevel\n "
                f"X-KDE-StartupNotify=false\n "
                f"Icon={self.home_user}/.local/share/timemachine/src/icons/restore.png\n\n "
                
                f"[Desktop Action "
                f"EnterTimeMachine]\n "
                f"Icon={self.home_user}/.local/share/timemachine/src/icons/restore.png\n "
                f"Name=Enter Time Machine\n "
                f"Exec=sh {self.home_user}/.local/share/timemachine/src/scripts/getDir.sh")

        try:
            # Copy current Time Machine folder to user
            shutil.copytree(self.getCurrentLocation, self.dst_folder_timemachine)       # Copy current folder to destination folder
            shutil.copy(self.src_timemachine_desktop, self.dst_timemachine_desktop)     # Copy .desktop and .timemachine.desktop to destination folder
            shutil.copy(self.src_service, self.dst_kde_service)     # Copy service.desktop

            sub.run(f"rm -rf {self.dst_venv_loc}", shell=True)        # Remove venv folder from user

            print("Program was installed!")
            # Install libnotify to get notification
            print("Libnotify-bin needs to be installed, so you can receive notifications from Time Machine.")
        
        except FileExistsError:
            print("Program is already installed!")

        exit()


app = CLI()
