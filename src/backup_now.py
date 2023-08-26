from setup import *
from get_current_users_wallpaper import get_wallpaper_full_location
from read_ini_file import UPDATEINIFILE
from get_users_de import get_user_de
from get_folders_to_be_backup import get_folders
from get_flatpaks_folders_size import flatpak_var_list, flatpak_local_list
from notification_massage import notification_message
from handle_spaces import handle_spaces


# Handle signal
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class BACKUP:
    async def backup_wallpaper(self):
        print("Backing up: Wallpaper...")

        # GNOME/KDE
        notification_message("Backing up: Wallpaper...")

        # Check for at least a wallpaper
        if os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
            for wallpaper in os.listdir(f"{MAIN_INI_FILE.wallpaper_main_folder()}/"):
                # Handle spaces
                wallpaper = handle_spaces(wallpaper)
                # Delete all wallpapers
                command = f"{MAIN_INI_FILE.wallpaper_main_folder()}/{wallpaper}"
                sub.run(["rm", "-rf", command], stdout=sub.PIPE, stderr=sub.PIPE)

        # Backup wallpaper
        if get_wallpaper_full_location() is not None:
            src = get_wallpaper_full_location()
            dst = MAIN_INI_FILE.wallpaper_main_folder() + "/"
            sub.run(["cp", "-rv", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)

    async def backup_home(self):
        for folder in get_folders():
            # Handle spaces
            folder = handle_spaces(folder)

            # Backup Home folder
            src = HOME_USER + "/" + folder
            dst = MAIN_INI_FILE.time_folder_format()
            sub.run(["cp", "-rv", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
            
            print(f'Backing up: {HOME_USER}/{folder}...')
            notification_message(f'Backing up: {folder}...')

    async def backup_home_hidden_files(self):
        # For GNOME
        if get_user_de() == 'gnome':
            # .local/share/
            list_gnome_include = [
                "gnome-shell",
                "dconf"
                ]
        
            for folder in os.listdir(f"{HOME_USER}/.local/share/"):
                # Handle spaces
                folder = handle_spaces(folder)
                
                if folder in list_gnome_include:
                    try:
                        src = HOME_USER + "/.local/share/" + folder
                        dst = MAIN_INI_FILE.gnome_local_share_main_folder()
                        sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
                    
                        print(f'Backing up: {HOME_USER}/.local/share/{folder}...')
                        notification_message(f'Backing up: .local/share/{folder}...')
                    except:
                        pass

            # .config/
            for folder in os.listdir(f"{HOME_USER}/.config/"):
                # Handle spaces
                folder = handle_spaces(folder)

                if folder in list_gnome_include:
                    src = HOME_USER + "/.config/" + folder
                    dst = MAIN_INI_FILE.gnome_config_main_folder()
                    sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
                    
                    print(f'Backing up: {HOME_USER}/.config/{folder}...')
                    notification_message(f'Backing up: .config/{folder}...')

        # For KDE
        elif get_user_de() == 'kde':
            # Backup .local/share/ selected folder for KDE
            list_include_kde = [
                # "icons",
                "kwin",
                "plasma_notes",
                "plasma",
                "aurorae",
                "color-schemes",
                "fonts",
                "kate",
                "kxmlgui5",
                "icons",
                "themes",

                "gtk-3.0",
                "gtk-4.0",
                "kdedefaults",
                "dconf",
                "fontconfig",
                "xsettingsd",
                "dolphinrc",
                "gtkrc",
                "gtkrc-2.0",
                "kdeglobals",
                "kwinrc",
                "plasmarc",
                "plasmarshellrc",
                "kglobalshortcutsrc",
                "khotkeysrc",
                "kwinrulesrc"
                "dolphinrc",
                "ksmserverrc",
                "konsolerc",
                "kscreenlockerrc",
                "plasmashellr",
                "plasma-org.kde.plasma.desktop-appletsrc",
                "plasmarc",
                "kdeglobals",
                
                "gtk-3.0",
                "gtk-4.0",
                "kdedefaults",
                "dconf",
                "fontconfig",
                "xsettingsd",
                "dolphinrc",
                "gtkrc",
                "gtkrc-2.0",
                "kdeglobals",
                "kwinrc",
                "plasmarc",
                "plasmarshellrc",
                "kglobalshortcutsrc",
                "khotkeysrc"
                ]

            for folder in os.listdir(f"{HOME_USER}/.local/share/"):
                # Handle spaces
                folder = handle_spaces(folder)

                # .local/share
                if folder in list_include_kde:
                    try:
                        src = HOME_USER + "/.local/share/" + folder
                        dst = MAIN_INI_FILE.kde_local_share_main_folder()
                        sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
                    
                        print(f'Backing up: {HOME_USER}/.local/share/{folder}...')
                        notification_message(f'Backing up: .local/share/{folder}...')
                    except:
                        pass

            # .config/
            try:
                for folder in os.listdir(f"{HOME_USER}/.config/"):
                    # Handle spaces
                    folder = handle_spaces(folder)

                    if folder in list_include_kde:
                        src = HOME_USER + "/.config/" + folder
                        dst = MAIN_INI_FILE.kde_config_main_folder()
                        sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
                    
                        print(f'Backing up: {HOME_USER}/.config/{folder}...')
                        notification_message(f'Backing up: .config/{folder}...')
            except:
                pass

            # .kde/share/
            try:
                for folders in os.listdir(f"{HOME_USER}/.kde/share/"):
                    # Handle spaces
                    folder = handle_spaces(folder)
                
                    if folder in list_include_kde:
                        src = HOME_USER + "}/.kde/share/" + folder
                        dst = MAIN_INI_FILE.kde_share_config_main_folder()
                        sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
                    
                        print(f'Backing up: {HOME_USER}/.kde/share/{folders}...')
                        notification_message(f'Backing up: .kde/share/{folders}...')
            except:
                pass
        else:
            pass

    async def backup_flatpak(self):
        try:
            counter = 0
            flatpak_list = []

            # Write to flatpak.txt
            with open(MAIN_INI_FILE.flatpak_txt_location(), 'w') as configfile:
                for flatpak in os.popen(GET_FLATPAKS_APPLICATIONS_NAME):
                    flatpak_list.append(flatpak)
                    # Write all installed flatpak apps by the name
                    configfile.write(flatpak_list[counter])
                    notification_message(f'Backing up: {flatpak_list[counter]}...')
                    counter += 1
        except Exception:
            pass

        # Backup flatpak data
        if MAIN_INI_FILE.get_database_value('STATUS', 'allow_flatpak_data'):
            # Backup flatpak data folder
            try:
                # .var/app
                for counter in range(len(flatpak_var_list())):
                    # Copy the Flatpak var/app folders
                    src = flatpak_var_list()[counter]
                    dst = MAIN_INI_FILE.flatpak_var_folder()
                    sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
                    
                    print(f'Backing up: {flatpak_var_list()[counter]}...')
                    notification_message(f'Backing up: {flatpak_var_list()[counter]}...')

                # Start Flatpak (.local/share/flatpak) backup
                for counter in range(len(flatpak_local_list())):
                    # Copy the Flatpak var/app folders
                    src = flatpak_local_list()[counter]
                    dst = MAIN_INI_FILE.flatpak_local_folder()
                    sub.run(["rsync", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
                    
                    print(f'Backing up: {flatpak_local_list()[counter]}...')
                    notification_message(f'Backing up: {flatpak_local_list()[counter]}...')
            except:
                pass

    async def end_backup(self):
        print("Ending backup...")

        notification_message("")

        MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
        MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'No')
        MAIN_INI_FILE.set_database_value('SCHEDULE', 'time_left', 'None')

        # Write to restore ini file 
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{MAIN_INI_FILE.restore_settings_location()}")
        with open(f"{MAIN_INI_FILE.restore_settings_location()}", 'w') as configfile:
            if not CONFIG.has_section('INFO'):
                CONFIG.add_section('INFO')

            CONFIG.set('INFO', 'wallpaper', f'{get_wallpaper_full_location().split("/")[-1]}')

            # KDE
            if get_user_de() == 'kde':
                CONFIG.set('INFO', 'icon', f'{self.get_kde_users_icon_name()}')
                CONFIG.set('INFO', 'cursor', f'{self.get_kde_users_cursor_name()}')
                CONFIG.set('INFO', 'font', f'{self.get_kde_users_font_name()}, {self.get_kde_users_font_size()}')
                CONFIG.set('INFO', 'gtktheme', f'{self.get_gtk_users_theme_name()}')
                CONFIG.set('INFO', 'theme', f'None')
            # GNOME
            else:
                CONFIG.set('INFO', 'icon', f'{self.get_gtk_users_icon_name()}')
                CONFIG.set('INFO', 'cursor', f'{self.get_gtk_users_cursor_name()}')
                CONFIG.set('INFO', 'font', f'{self.get_gtk_user_font_name()}')
                CONFIG.set('INFO', 'gtktheme', f'{self.get_gtk_users_theme_name()}')
                CONFIG.set('INFO', 'theme', f'None')
                CONFIG.set('INFO', 'colortheme', f'None')

            CONFIG.write(configfile)

        print("Backup is done!")
        print("Sleeping for 60 seconds...")

        # Wait x, so if it finish fast, won't repeat the backup
        time.sleep(60)
        exit()

    #########################################################
    # KDE
    #########################################################
    # KDE cursor
    def get_kde_users_cursor_name(self):
        with open(f"{HOME_USER}/.config/xsettingsd/xsettingsd.conf", "r") as read:
            read = read.readlines()

            for counter in range(len(read)):
                if read[counter].split()[0] == "Gtk/CursorThemeName":
                    # Return users cursor name
                    return read[counter].split()[1].replace('"','')

    # KDE font
    def get_kde_users_font_name(self):
        with open(f"{HOME_USER}/.config/kdeglobals", "r") as read:
            read = read.readlines()

            for counter in range(len(read)):
                if read[counter].startswith("font="):
                    # Return users kde font name
                    return (read[counter]).strip().split(",")[0].replace("font=","")

    # KDE font size
    def get_kde_users_font_size(self):
        with open(f"{HOME_USER}/.config/kdeglobals", "r") as read:
            read = read.readlines()

            for counter in range(len(read)):
                if read[counter].startswith("font="):
                    # Return users kde font size
                    return (read[counter]).strip().split(",")[1]

    # KDE icon
    def get_kde_users_icon_name(self):
        with open(f"{HOME_USER}/.config/xsettingsd/xsettingsd.conf", "r") as read:
            read = read.readlines()
            for counter in range(len(read)):
                if read[counter].split()[0] == "Net/IconThemeName":
                    # Return users icon name
                    return read[counter].split()[1].replace('"','')

    #########################################################
    # GNOME
    #########################################################
    # GTK theme
    def get_gtk_users_theme_name(self):
        user_theme_name = os.popen(GET_USER_THEME_CMD).read().strip().replace("'", "")
        return user_theme_name

        # def users_theme_size():
        #     try:
        #         userThemeSize=os.popen(f"du -s {homeUser}/.themes/{users_theme_name()}")
        #         userThemeSize=userThemeSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.themes/{users_theme_name()}", "").replace("\t", "")
        #         userThemeSize=int(userThemeSize)
        #     except ValueError:
        #         try:
        #             userThemeSize=os.popen(f"du -s {homeUser}/.local/share/themes/{users_theme_name()}")
        #             userThemeSize=userThemeSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.local/share/themes/{users_theme_name()}", "").replace("\t", "")
        #             userThemeSize=int(userThemeSize)
        #         except ValueError:
        #             try:
        #                 userThemeSize=os.popen(f"du -s /usr/share/themes/{users_theme_name()}")
        #                 userThemeSize=userThemeSize.read().strip("\t").strip("\n").replace(f"/usr/share/themes/{users_theme_name()}", "").replace("\t", "")
        #                 userThemeSize=int(userThemeSize)
        #             except ValueError:
        #                 return None

        #     return userThemeSize

    # GTK font
    def get_gtk_user_font_name(self):
        user_font_name = os.popen(GET_USER_FONT_CMD).read().replace("'", "")
        user_font_name = " ".join(user_font_name.split())
        return user_font_name

        # def get_user_font():
        #     if get_user_de() == 'kde':
        #         mainFont=FONT()
        #         return  f"{mainFont.get_kde_font()}, {mainFont.get_kde_font_size()}"

        #     else:
        #         userFontName=os.popen(getUserFontCMD)
        #         userFontName=userFontName.read().replace("'", "")
        #         userFontName=" ".join(userFontName.split())
        #         return userFontName

    # GTK icon
    def get_gtk_users_icon_name(self):
        userIconName = os.popen(GET_USER_ICON_CMD).read().strip().replace("'", "")
        return userIconName

        # def users_icon_size():
        # try:
        #     userIconSize=os.popen(f"du -s {homeUser}/.icons/{users_icon_name()}")
        #     userIconSize=userIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.icons/{users_icon_name()}", "").replace("\t", "")
        #     userIconSize=int(userIconSize)

        # except ValueError:
        #     try:
        #         userIconSize=os.popen(f"du -s {homeUser}/.local/share/icons/{users_icon_name()}")
        #         userIconSize=userIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.local/share/icons/{users_icon_name()}", "").replace("\t", "")
        #         userIconSize=int(userIconSize)

        #     except ValueError:
        #         try:
        #             userIconSize=os.popen(f"du -s /usr/share/icons/{users_icon_name()}")
        #             userIconSize=userIconSize.read().strip("\t").strip("\n").replace(f"/usr/share/icons/{users_icon_name()}", "").replace("\t", "")
        #             userIconSize=int(userIconSize)

        #         except ValueError:
        #             return None

        # return userIconSize

    # GTK cursor
    def get_gtk_users_cursor_name(self):
        user_cursor_name = os.popen(GET_USER_CURSOR_CMD).read().strip().replace("'", "")
        return user_cursor_name
    
    async def main(self):
        await self.backup_wallpaper()
        await self.backup_home()
        await self.backup_home_hidden_files()
        await self.backup_flatpak()
        await self.end_backup()


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    main = BACKUP()
    asyncio.run(main.main())