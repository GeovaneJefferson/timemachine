from setup import *
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE

mainIniFile = UPDATEINIFILE()

def get_packages_size():
    try:
        if package_manager() == rpmFolderName:
            applicationSize = os.popen(f"du -hs {mainIniFile.rpm_main_folder()}/")
            applicationSize = applicationSize.read().strip("\t")
            applicationSize = applicationSize.strip("\n")
            applicationSize = applicationSize.replace(f"{mainIniFile.deb_main_folder()}", "").replace("\t", "").replace("/", "")

        elif package_manager() == debFolderName:
            applicationSize = os.popen(f"du -hs {mainIniFile.deb_main_folder()}/")
            applicationSize = applicationSize.read().strip("\t")
            applicationSize = applicationSize.strip("\n")
            applicationSize = applicationSize.replace(f"{mainIniFile.deb_main_folder()}", "").replace("\t", "").replace("/", "")
        
        if "M" in applicationSize:
            return applicationSize + "B"
        else:
            return applicationSize
    
    except:
        return "None"

if __name__ == '__main__':
    pass