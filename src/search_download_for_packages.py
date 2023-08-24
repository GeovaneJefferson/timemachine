from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()
# Auto Packages
downloads_folder_location=f"{HOME_USER}/Downloads"

def search_download_for_packages():
    # Auto Packages List
    detectedPackagesDebList = []
    detectedPackagesRPMList = []

    try:
        # Read Downloads folder for .deb
        for debs in os.listdir(MAIN_INI_FILE.deb_main_folder()):
            detectedPackagesDebList.append(debs)
    except Exception:
        pass
    
    try:
        # Read Downloads folder for .rpm
        for rpms in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
            detectedPackagesRPMList.append(rpms)
    except Exception:
        pass

    for output in os.listdir(downloads_folder_location):
        if output.endswith(".deb"):
            if output.split("_")[0] in (f"{MAIN_INI_FILE.deb_main_folder()}/{(output).split('_')[0]}"):
                # Delete the old version before back up
                for deleteOutput in os.listdir(MAIN_INI_FILE.deb_main_folder()):
                    if deleteOutput.startswith(f"{output.split('_')[0]}"):
                        action = MAIN_INI_FILE.deb_main_folder() + "/" + deleteOutput
                        sub.run(["rm", "-rf", action])

                # Now back up
                src = downloads_folder_location + "/" + output
                dst = MAIN_INI_FILE.deb_main_folder()
                sub.run(["rsync", "-avr", src, dst])
            
        elif output.endswith(".rpm"):
            if output.split("_")[0] in (f"{MAIN_INI_FILE.rpm_main_folder()}/{(output).split('_')[0]}"):
                # Delete the old version before back up
                for deleteOutput in os.listdir(MAIN_INI_FILE.rpm_main_folder()):
                    if deleteOutput.startswith(f"{output.split('_')[0]}"):
                        action = MAIN_INI_FILE.rpm_main_folder() + "/" + deleteOutput
                        sub.run(["rm", "-rf", action])

                # Now back up
                src = downloads_folder_location + "/" + output
                dst = MAIN_INI_FILE.rpm_main_folder()
                sub.run(["rsync", "-avr", src, dst])
            

if __name__ == '__main__':
    pass