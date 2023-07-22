from setup import *
from read_ini_file import UPDATEINIFILE

# Auto Packages
downloads_folder_loccation=f"{HOME_USER}/Downloads"


def search_download_for_packages():
    MAININIFILE=UPDATEINIFILE()
    
    # Auto Packages List
    detectedPackagesDebList=[]
    detectedPackagesRPMList=[]
    

    try:
        # Read Downloads folder for .deb
        for debs in os.listdir(MAININIFILE.deb_main_folder()):
            detectedPackagesDebList.append(debs)
    except:
        pass
    
    try:
        # Read Downloads folder for .rpm
        for rpms in os.listdir(MAININIFILE.rpm_main_folder()):
            detectedPackagesRPMList.append(rpms)
    except:
        pass

    for output in os.listdir(downloads_folder_loccation):
        if output.endswith(".deb"):
            if output.split("_")[0] in (f"{MAININIFILE.deb_main_folder()}/{(output).split('_')[0]}"):
                # Delete the old version before back up
                for deleteOutput in os.listdir(MAININIFILE.deb_main_folder()):
                    if deleteOutput.startswith(f"{output.split('_')[0]}"):
                        sub.run(f"rm -f {MAININIFILE.deb_main_folder()}/{deleteOutput}",shell=True)
                
                # Now back up
                sub.run(f"{COPY_RSYNC_CMD} {downloads_folder_loccation}/{output} {MAININIFILE.deb_main_folder()}", shell=True)

        elif output.endswith(".rpm"):
            if output.split("_")[0] in (f"{MAININIFILE.rpm_main_folder()}/{(output).split('_')[0]}"):
                # Delete the old version before back up
                for deleteOutput in os.listdir(MAININIFILE.rpm_main_folder()):
                    if deleteOutput.startswith(f"{output.split('_')[0]}"):
                        sub.run(f"rm -f {MAININIFILE.rpm_main_folder()}/{deleteOutput}",shell=True)
                
                # Now back up
                sub.run(f"{COPY_RSYNC_CMD} {downloads_folder_loccation}/{output} {MAININIFILE.rpm_main_folder()}", shell=True)


if __name__ == '__main__':
    pass