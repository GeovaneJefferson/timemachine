from setup import *


class CHECKER:
    def __init__(self):
        self.downloadLoc = f"{homeUser}/Downloads"
        self.savedStaticNumber = []
        self.savedContinueNumber = []

        self.staticOutput = False
        self.continueOutput = False

        self.read_ini_files()

    def read_ini_files(self):
        self.detectedPackagesDebList = []
        ################################################################################
        # Read file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        
        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
        self.debMainFolder = f"{self.iniExternalLocation}/{baseFolderName}/{applicationFolderName}/{debFolderName}"        

    def search_downloads(self):
        # Read Downloads folder
        for i in os.listdir(self.debMainFolder):
            self.detectedPackagesDebList.append(i)
    
        print(self.detectedPackagesDebList)
        for output in os.listdir(self.downloadLoc):
            if output.endswith(".deb"):
                # Check if has not been already back up
                if output not in self.detectedPackagesDebList:
                    # Back up DEB
                    sub.run(f"{copyRsyncCMD} {self.downloadLoc}/{output} {self.debMainFolder}", shell=True)
                else:
                    print(f"{output} is already back up.")
            else:
                print("No package to be backup...")

        # Clean list
        self.detectedPackagesDebList.clear()

app = CHECKER()

while True:
    if app.iniAutomaticallyBackup == "true":
        app.search_downloads()
        time.sleep(10)
    else:
        break
print("Auto backup is off...")
exit()