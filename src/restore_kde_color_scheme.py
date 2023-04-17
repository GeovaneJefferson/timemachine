from setup import *
from read_ini_file import UPDATEINIFILE

somethingInside = []

def restore_kde_color_scheme():
    mainIniFile = UPDATEINIFILE()

    print("Restoring KDE Color Scheme...")
    try:
        for colorScheme in os.listdir(f"{mainIniFile.color_scheme_main_folder()}/"):
            somethingInside.append(colorScheme)
       
        if somethingInside:
            if not os.path.exists(f"{homeUser}/.local/share/color-schemes/"):
                sub.run(f"{createCMDFolder} {homeUser}/.local/share/color-schemes/", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.color_scheme_main_folder()}/ {homeUser}/.local/share/color-schemes/", shell=True)
    except:         
        pass

if __name__ == '__main__':
    pass