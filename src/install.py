from setup import *
from create_backup_checker_desktop import create_backup_checker_desktop


class CLI:
    def __init__(self):
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

    def check_system(self):
        usersDistro = os.popen("cat /etc/os-release").read()

        if "ubuntu" in usersDistro:
            return "ubuntu"

        elif "debian" in usersDistro:
            return "debian"

        elif "opensuse" in usersDistro:
            return "opensuse"

        elif "fedora" in usersDistro:
            return "fedora"

        elif "arch" in usersDistro:
            return "arch"

        else:
            print("No support OS found!")
            print("Please, Contact the developer :D")
            exit()

    def requirements(self,user_os):
        print("Users OS:",user_os.capitalize())

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
            
        except:
            return "Error trying to install depedencies."

        # Depedencies
        try:
            print("Installing PySide6...")
            sub.run(f"pip install {self.installPipPackages}", shell=True)

        except:
            print("Error trying to install dependencies!")
            print("Yóu need to manually install all dependencies:\n",
                "* python3-pip or python-pip\n",
                "* PySide6.")
            
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

    def copy_files(self):
        try:
            # Copy current Time Machine folder to user
            shutil.copytree(getCurrentLocation,
                            dst_folder_timemachine)
            
        except FileNotFoundError as e:
            print(e)
            print(f"Error trying install {appName}!")
            exit()

    def create_files(self):
        create_backup_checker_desktop()

        # Create applications folder inside .local/share
        if not os.path.exists(dst_applications_location):
            sub.run(f"{createCMDFolder} {dst_applications_location}", shell=True)

        # Edit appNameClose.desktop 
        print(f"Editing {dst_timemachine_desktop}")
        with open(dst_timemachine_desktop, "w") as writer: 
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

        # Edit migration_assistant.desktop 
        with open(dst_migration_assistant_desktop, "w") as writer:
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
            

if __name__ == '__main__':
    main = CLI()
    main.requirements(str(main.check_system()))
    
    # Begin installation
    main.copy_files()
    
    # Edit files
    main.create_files()

    print("Program was successfully installed!")
