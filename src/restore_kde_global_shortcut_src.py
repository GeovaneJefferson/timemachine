from setup import *
from read_ini_file import UPDATEINIFILE
from get_user_de import get_user_de
'''
This changes:
- Color Scheme
- Fonts
- Icons
- Single Click 
- Other small folders configurations

Missing:
- Plasma Style
- Window Decoration
- Cursor

'''
somethingToRestoreInKGlobalShortcutSrc = []

async def restore_kde_global_shortcut_src():
    mainIniFile = UPDATEINIFILE()

    print("Restoring Kde Globals Shortcuts Src...")
    try:
        for kGlobalShortcutSrc in os.listdir(f"{mainIniFile.kglobal_shortcut_src_main_folder()}/"):
            somethingToRestoreInKGlobalShortcutSrc.append(kGlobalShortcutSrc)
       
        # # If has something to restore
        if somethingToRestoreInKGlobalShortcutSrc:
            ################################################################################
            # Create .config inside home user
            ################################################################################
            if not os.path.exists(f"{homeUser}/.config"):
                sub.run(f"{createCMDFolder} {homeUser}/.config", shell=True)   

            sub.run(f"{copyRsyncCMD} {mainIniFile.kglobal_shortcut_src_main_folder()}/ {homeUser}/.config", shell=True)
    except:         
        pass

    return "Task completed: Wallpaper"

if __name__ == '__main__':
    pass