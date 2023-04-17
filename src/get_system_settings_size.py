from setup import *
from package_manager import package_manager
from read_ini_file import UPDATEINIFILE

dummySystemSettingsSizeList = []
dummy = []
result = []

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

        ####################################
        # Plasma
        ####################################
        systemSettingsTheme = os.popen(f"du -hs {mainIniFile.plasma_main_folder()} 2>/dev/null")
        systemSettingsTheme = systemSettingsTheme.read().strip("\t")
        systemSettingsTheme = systemSettingsTheme.strip("\n")
        systemSettingsTheme = systemSettingsTheme.replace(f"{plasmaFolderName}", "")

        if systemSettingsTheme != "":
            for string in systemSettingsTheme:
                if string.isdigit():
                    dummy.append(string)

            systemSettingsTheme = ''.join(dummy)
            dummy.clear()
            systemSettingsTheme = int(systemSettingsTheme)
            dummySystemSettingsSizeList.append(systemSettingsTheme)
        
        ####################################
        # GTK Theme
        ####################################
        systemSettingsTheme = os.popen(f"du -hs {mainIniFile.gtk_theme_main_folder()} 2>/dev/null")
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
        
        ####################################
        # Aurorae
        ####################################
        systemSettingsTheme = os.popen(f"du -hs {mainIniFile.aurorae_main_folder()} 2>/dev/null")
        systemSettingsTheme = systemSettingsTheme.read().strip("\t")
        systemSettingsTheme = systemSettingsTheme.strip("\n")
        systemSettingsTheme = systemSettingsTheme.replace(f"{auroraeFolderName}", "")

        if systemSettingsTheme != "":
            for string in systemSettingsTheme:
                if string.isdigit():
                    dummy.append(string)

            systemSettingsTheme = ''.join(dummy)
            dummy.clear()
            systemSettingsTheme = int(systemSettingsTheme)
            dummySystemSettingsSizeList.append(systemSettingsTheme)
        
        if len(dummySystemSettingsSizeList) > 1:
            if sum(dummySystemSettingsSizeList) < 1000:
                return f"{sum(dummySystemSettingsSizeList)} MB" 
            else:
                if len(dummySystemSettingsSizeList) == 4:
                    x = sum(dummySystemSettingsSizeList)

                    value = 0
                    for count in range(len(str(x))):
                        #print(str(x)[count])
                        result.append(str(x)[count])
                        if value == 0:
                            result.append(".")
                            value += 1
                        else:
                            value += 1

                y = " ".join(result).replace(" ","")
                if int(y[3]) > 1:
                    return f"{y[0]}G"
                else:
                    return f"{y[:3]}G"
    
    except Exception as error:
        print(error)
        return "None"

if __name__ == '__main__':
    pass