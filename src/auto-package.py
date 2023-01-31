from setup import *


class CHECKER:
    def __init__(self):
        self.downloadLoc = f"{homeUser}/Downloads"
        self.read_ini_files()

    def read_ini_files(self):
        self.detectedPackagesDebList = []
        self.detectedPackagesRPMList = []
        ################################################################################
        # Read file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        
        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
        self.debMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{debFolderName}"        
        self.rpmMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{rpmFolderName}"        
   
    def search_downloads(self):
        try:
            # Read Downloads folder for .deb
            for debs in os.listdir(self.debMainFolder):
                self.detectedPackagesDebList.append(debs)
        except:
            pass
        try:
            # Read Downloads folder for .rpm
            for rpms in os.listdir(self.rpmMainFolder):
                self.detectedPackagesRPMList.append(rpms)
        except:
            pass

        for output in os.listdir(self.downloadLoc):
            if output.endswith(".deb"):
                # Check if has not been already back up
                if output not in self.detectedPackagesDebList:
                    # Back up DEB
                    sub.run(f"{copyRsyncCMD} {self.downloadLoc}/{output} {self.debMainFolder}", shell=True)
                else:
                    print(f"{output} is already back up.")

            elif output.endswith(".rpm"):
                # Check if has not been already back up
                if output not in self.detectedPackagesRPMList:
                    # Back up DEB
                    sub.run(f"{copyRsyncCMD} {self.downloadLoc}/{output} {self.rpmMainFolder}", shell=True)
                else:
                    print(f"{output} is already back up.")
            else:
                print("No package to be backup...")

        # Clean list
        self.detectedPackagesDebList.clear()
        self.detectedPackagesRPMList.clear()

app = CHECKER()

while True:
    app.read_ini_files()
    if app.iniAutomaticallyBackup == "true":
        app.search_downloads()
        time.sleep(1)
    else:
        break

print("Auto backup is off...")
exit()