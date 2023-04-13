from setup import *
from read_ini_file import UPDATEINIFILE

def backup_kde_kglobal_shortcuts_src():
    mainIniFile = UPDATEINIFILE()

    try:
        os.listdir(f"{homeUser}/.config/")
        sub.run(f"{copyRsyncCMD} {homeUser}/.config/kglobalshortcutsrc {str(mainIniFile.kglobal_shortcut_src_main_folder())}",shell=True)
    except FileNotFoundError as error:
        print(error)
        pass