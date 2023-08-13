from setup import *
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def get_packages_size():
    try:
        if package_manager() == RPM_FOLDER_NAME:
            application_Size=os.popen(f"du -hs {MAIN_INI_FILE.rpm_main_folder()}/")
            application_Size=application_Size.read().strip("\t").strip("\n")
            application_Size=application_Size.replace(f"{MAIN_INI_FILE.rpm_main_folder()}", "").replace("\t", "").replace("/", "")
        elif package_manager() == DEB_FOLDER_NAME:
            application_Size=os.popen(f"du -hs {MAIN_INI_FILE.deb_main_folder()}/")
            application_Size=application_Size.read().strip("\t").strip("\n")
            application_Size=application_Size.replace(f"{MAIN_INI_FILE.deb_main_folder()}", "").replace("\t", "").replace("/", "")
        
        if "M" in application_Size:
            return application_Size + "B"
        else:
            return application_Size
    except:
        return "None"


if __name__=='__main__':
    pass