from setup import *
# from package_manager import package_manager
from read_ini_file import UPDATEINIFILE

MAIN_INI_FILE = UPDATEINIFILE()
system_settings_size_list=[]
dummy_list = []
result_list = []


# TODO
def get_system_settings_size():
    try:
        # Icons size
        systemSettingsIcon = os.popen(f"du -hs {MAIN_INI_FILE.icon_main_folder()} 2>/dev/null")
        systemSettingsIcon = systemSettingsIcon.read().strip("\t")
        systemSettingsIcon = systemSettingsIcon.strip("\n")
        systemSettingsIcon = systemSettingsIcon.replace(f"{MAIN_INI_FILE.icon_main_folder()}", "")
        
        if systemSettingsIcon != "":
            for string in systemSettingsIcon:
                if string.isdigit():
                    dummy_list.append(string)

            systemSettingsIcon = ''.join(dummy_list)
            dummy_list.clear()
            systemSettingsIcon = int(systemSettingsIcon)
            system_settings_size_list.append(systemSettingsIcon)

        ####################################
        # Plasma
        ####################################
        # systemSettingsTheme=os.popen(f"du -hs {MAIN_INI_FILE.plasma_main_folder()} 2>/dev/null")
        # systemSettingsTheme=systemSettingsTheme.read().strip("\t")
        # systemSettingsTheme=systemSettingsTheme.strip("\n")
        # systemSettingsTheme=systemSettingsTheme.replace(f"{PLASMA_FOLDER_NAME}", "")

        # if systemSettingsTheme != "":
        #     for string in systemSettingsTheme:
        #         if string.isdigit():
        #             dummy_list.append(string)

        #     systemSettingsTheme=''.join(dummy_list)
        #     dummy_list.clear()
        #     systemSettingsTheme=int(systemSettingsTheme)
        #     system_settings_size_list.append(systemSettingsTheme)
        
        ####################################
        # GTK Theme
        ####################################
        systemSettingsTheme = os.popen(f"du -hs {MAIN_INI_FILE.gtk_theme_main_folder()} 2>/dev/null")
        systemSettingsTheme = systemSettingsTheme.read().strip("\t")
        systemSettingsTheme = systemSettingsTheme.strip("\n")
        systemSettingsTheme = systemSettingsTheme.replace(f"{GTK_THEME_FOLDER_NAME}", "")

        if systemSettingsTheme != "":
            for string in systemSettingsTheme:
                if string.isdigit():
                    dummy_list.append(string)

            systemSettingsTheme = ''.join(dummy_list)
            dummy_list.clear()
            systemSettingsTheme=int(systemSettingsTheme)
            system_settings_size_list.append(systemSettingsTheme)
        
        ####################################
        # Aurorae
        ####################################
        # systemSettingsTheme=os.popen(f"du -hs {MAIN_INI_FILE.aurorae_main_folder()} 2>/dev/null")
        # systemSettingsTheme=systemSettingsTheme.read().strip("\t")
        # systemSettingsTheme=systemSettingsTheme.strip("\n")
        # systemSettingsTheme=systemSettingsTheme.replace(f"{AURORAEFOLDERNAME}", "")

        # if systemSettingsTheme != "":
        #     for string in systemSettingsTheme:
        #         if string.isdigit():
        #             dummy_list.append(string)

        #     systemSettingsTheme=''.join(dummy_list)
        #     dummy_list.clear()
        #     systemSettingsTheme=int(systemSettingsTheme)
        #     system_settings_size_list.append(systemSettingsTheme)
        
        if len(system_settings_size_list) > 1:
            if sum(system_settings_size_list) < 1000:
                return f"{sum(system_settings_size_list)} MB" 
            else:
                if len(system_settings_size_list) == 4:
                    x=sum(system_settings_size_list)

                    value=0
                    for count in range(len(str(x))):
                        #print(str(x)[count])
                        result_list.append(str(x)[count])
                        if value == 0:
                            result_list.append(".")
                            value += 1
                        else:
                            value += 1

                y=" ".join(result_list).replace(" ","")
                if int(y[3]) > 1:
                    return f"{y[0]}G"
                else:
                    return f"{y[:3]}G"
    
    except Exception as e:
        print(e)
        return "None"


if __name__ == '__main__':
    pass