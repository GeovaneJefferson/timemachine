from setup import *
from read_ini_file import UPDATEINIFILE

# Auto Packages
downloadLoc = f"{homeUser}/Downloads"

# Auto Packages List
detectedPackagesDebList = []
detectedPackagesRPMList = []

def search_download_for_packages():
    mainIniFile = UPDATEINIFILE()

    print("Searching new packages to be backup...")
    try:
        # Read Downloads folder for .deb
        for debs in os.listdir(mainIniFile.deb_main_folder()):
            detectedPackagesDebList.append(debs)
    except:
        pass
    
    try:
        # Read Downloads folder for .rpm
        for rpms in os.listdir(mainIniFile.rpm_main_folder()):
            detectedPackagesRPMList.append(rpms)
    except:
        pass

    for output in os.listdir(downloadLoc):
        if output.endswith(".deb"):
            if output.split("_")[0] in (f"{mainIniFile.deb_main_folder()}/{(output).split('_')[0]}"):
                # Delete the old version before back up
                for deleteOutput in os.listdir(mainIniFile.deb_main_folder()):
                    if deleteOutput.startswith(f"{output.split('_')[0]}"):
                        sub.run(f"rm -f {mainIniFile.deb_main_folder()}/{deleteOutput}",shell=True)
                
                # Now back up
                sub.run(f"{copyRsyncCMD} {downloadLoc}/{output} {mainIniFile.deb_main_folder()}", shell=True)

        elif output.endswith(".rpm"):
            if output.split("_")[0] in (f"{mainIniFile.rpm_main_folder()}/{(output).split('_')[0]}"):
                # Delete the old version before back up
                for deleteOutput in os.listdir(mainIniFile.rpm_main_folder()):
                    if deleteOutput.startswith(f"{output.split('_')[0]}"):
                        sub.run(f"rm -f {mainIniFile.rpm_main_folder()}/{deleteOutput}",shell=True)
                
                # Now back up
                sub.run(f"{copyRsyncCMD} {downloadLoc}/{output} {mainIniFile.rpm_main_folder()}", shell=True)

    # Clean list
    detectedPackagesDebList.clear()
    detectedPackagesRPMList.clear()

if __name__ == '__main__':
    pass