from setup import *
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE

dummySystemSettingsSizeList = []
dummy = []

def get_system_settings_size():
    mainIniFile = UPDATEINIFILE()
    
    try:
        # Icons size
        systemSettingsIcon = os.popen(f"du -hs {mainIniFile.icon_main_folder()} 2>/dev/null")
        systemSettingsIcon = systemSettingsIcon.read().strip("\t")
        systemSettingsIcon = systemSettingsIcon.strip("\n")
        systemSettingsIcon = systemSettingsIcon.replace(f"{mainIniFile.icon_main_folder()}", "")
        
        if systemSettingsIcon != "":
            for string in systemSettingsIcon:
                if string.isdigit():
                    dummy.append(string)

            systemSettingsIcon = ''.join(dummy)
            dummy.clear()
            systemSettingsIcon = int(systemSettingsIcon)
            dummySystemSettingsSizeList.append(systemSettingsIcon)

        # Theme size
        systemSettingsTheme = os.popen(f"du -hs {gtkThemeFolderName} 2>/dev/null")
        systemSettingsTheme = systemSettingsTheme.read().strip("\t")
        systemSettingsTheme = systemSettingsTheme.strip("\n")
        systemSettingsTheme = systemSettingsTheme.replace(f"{gtkThemeFolderName}", "")

        if systemSettingsTheme != "":
            for string in systemSettingsTheme:
                if string.isdigit():
                    dummy.append(string)

            systemSettingsTheme = ''.join(dummy)
            dummy.clear()
            systemSettingsTheme = int(systemSettingsTheme)
            dummySystemSettingsSizeList.append(systemSettingsTheme)
        
        if len(dummySystemSettingsSizeList) > 1:
            return sum(dummySystemSettingsSizeList)
        else:
            if sum(dummySystemSettingsSizeList) < 1000:
                return str(dummySystemSettingsSizeList[0]) + "MB"
            else:
                return str(dummySystemSettingsSizeList[0])

    
    except Exception as error:
        print(error)
        return "None"

if __name__ == '__main__':
    pass