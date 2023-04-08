from setup import *
from get_user_icon import users_icon_name
from users_cursor_name import users_cursor_name
from get_user_theme import users_theme_name
from get_kde_color_scheme import get_kde_color_scheme
from read_ini_file import UPDATEINIFILE

def delete_old_settings(x):
    mainIniFile = UPDATEINIFILE()
    if x == "Icon":
        if os.listdir(f"{str(mainIniFile.icon_main_folder())}/"):
            for icon in os.listdir(f"{str(mainIniFile.icon_main_folder())}/"):
                # If is not the same name, remove it, and backup the new one
                if icon != users_icon_name():
                    print(f"Deleting {str(mainIniFile.icon_main_folder())}/{icon}...")
                    sub.run(f"rm -rf {str(mainIniFile.icon_main_folder())}/{icon}",shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'icon', f"{users_icon_name()}")
            config.write(configfile)

    elif x == "Cursor":
        if os.listdir(f"{str(mainIniFile.cursor_main_folder())}/"):
            for cursor in os.listdir(f"{str(mainIniFile.cursor_main_folder())}/"):
                # If is not the same name, remove it, and backup the new one
                if cursor != users_cursor_name():
                    print(f"Deleting {str(mainIniFile.cursor_main_folder())}/{cursor}...")
                    sub.run(f"rm -rf {str(mainIniFile.cursor_main_folder())}/{cursor}",shell=True)
        
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'cursor', f"{users_cursor_name()}")
            config.write(configfile)

    elif x == "Theme":
        if os.listdir(f"{str(mainIniFile.gtk_theme_main_folder())}/"):
            for theme in os.listdir(f"{str(mainIniFile.gtk_theme_main_folder())}/"):
                # If is not the same name, remove it, and backup the new one
                if theme != users_theme_name():
                    print(f"Deleting {mainIniFile.gtk_theme_main_folder()}/{theme}...")
                    sub.run(f"rm -rf {mainIniFile.gtk_theme_main_folder()}/{theme}",shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'theme', f"{users_theme_name()}")
            config.write(configfile)

    elif x == "Color-Scheme":
        if os.listdir(f"{str(mainIniFile.color_scheme_main_folder())}/"):
            for colortheme in os.listdir(f"{str(mainIniFile.color_scheme_main_folder())}/"):
                # If is not the same name, remove it, and backup the new one
                if colortheme != get_kde_color_scheme():
                    print(f"Deleting {mainIniFile.color_scheme_main_folder()}/{colortheme}...")
                    sub.run(f"rm -rf {mainIniFile.color_scheme_main_folder()}/{colortheme}",shell=True)

        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'colortheme', f"{get_kde_color_scheme()}")
            config.write(configfile)
    else:
        pass