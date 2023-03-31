from setup import *
from get_user_icon import users_icon_name

def delete_old_settings_settings(x):
    if x == "Icon":
        if os.listdir(f"{str(mainIniFile.icon_main_folder())}/"):
            for icon in os.listdir(f"{str(mainIniFile.icon_main_folder())}/"):
                # If is not the same name, remove it, and backup the new one
                if icon != users_icon_name():
                    print(f"Deleting {str(mainIniFile.icon_main_folder())}/{icon}...")
                    sub.run(f"rm -rf {str(mainIniFile.icon_main_folder())}/{icon}", shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'icon', f"{users_icon_name()}")
            config.write(configfile)

    elif x == "Cursor":
        if os.listdir(f"{str(mainIniFile.cursor_main_folder())}/"):
            for cursor in os.listdir(f"{str(mainIniFile.cursor_main_folder())}/"):
                # If is not the same name, remove it, and backup the new one
                if cursor != userCurrentcursor:
                    print(f"Deleting {str(mainIniFile.cursor_main_folder())}/{cursor}...")
                    sub.run(f"rm -rf {str(mainIniFile.cursor_main_folder())}/{cursor}", shell=True)
        
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'cursor', f"{users_cursor_name()}")
            config.write(configfile)

    elif x == "Theme":
        if os.listdir(f"{str(mainIniFile.theme_main_folder())}/"):
            for theme in os.listdir(f"{str(mainIniFile.theme_main_folder())}/"):
                # If is not the same name, remove it, and backup the new one
                if theme != users_theme_name():
                    print(f"Deleting {mainIniFile.theme_main_folder()}/{theme}...")
                    sub.run(f"rm -rf {mainIniFile.theme_main_folder()}/{theme}", shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'theme', f"{users_theme_name()}")
            config.write(configfile)
    else:
        pass