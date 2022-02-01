import os
import pathlib
import shutil
from pathlib import Path


class CLI:
    def __init__(self):
        # Folders
        self.home_user = str(Path.home())
        self.get_current_location = pathlib.Path().resolve()  # Current folder

        # Terminal commands
        self.create_cmd = 'mkdir '

        # Default
        # Current folder
        self.src_backup_check = "src/backup_check.desktop"
        self.src_timemachine_desktop = "src/timemachine.desktop"

        # Destination folder
        self.dst_env_loc = self.home_user + "/.local/share/timemachine/env/"
        self.dst_folder_timemachine = self.home_user + "/.local/share/timemachine"
        self.dst_timemachine_desktop = self.home_user + "/.local/share/applications/timemachine.desktop"
        self.restore_icon = self.home_user + "/.local/share/timemachine/src/icons/restore_48.png"
        self.create_autostart_folder = self.home_user + "/.config/autostart"

        self.begin_install()

    def begin_install(self):
        # Create file if file do not exist
        if os.path.exists(self.create_autostart_folder):
            pass
        else:
            os.system(self.create_cmd + self.create_autostart_folder)

        # Create and modify .desktop and timemachine.desktop to get username
        with open(self.src_backup_check, "w") as writer:
            writer.write(
                "[Desktop Entry]\n Type=Application\n Exec=/bin/python3 " + self.home_user + "/.local/share/timemachine/src/backup_check.py\n Hidden=false\n NoDisplay=false\n Name=Time Machine\n Comment=Backup your files\n Icon=" + self.restore_icon)

        # .Desktop
        with open(self.src_timemachine_desktop, "w") as writer:
            writer.write(
                "[Desktop Entry]\n Version=1.0\n Type=Application\n Name=Time Machine\n Comment=Backup your files\n Icon=" + self.home_user + '/.local/share/timemachine/src/icons/restore.png\n Exec=python3 ' + self.home_user + '/.local/share/timemachine/src/gui.py\n Path=' + self.home_user + "/.local/share/timemachine/\n Categories=Settings\n StartupWMClass=Gui.py\n Terminal=false")

        # Copy current Time Machine folder to user
        shutil.copytree(self.get_current_location, self.dst_folder_timemachine)     # Copy current folder to destination folder
        shutil.copy(self.src_timemachine_desktop, self.dst_timemachine_desktop)     # Copy .desktop and .timemachine.desktop to destination folder

        # Remove env folder from user
        os.system("rm -rf " + self.dst_env_loc)

        print("Program was installed!")
        # Install libnotify to get notification
        print("Libnotify-bin needs to be installed, so you can receive notifications from Time Machine.")

        exit()


app = CLI()
app.__init__()
