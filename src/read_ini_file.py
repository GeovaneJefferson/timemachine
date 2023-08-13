from setup import *


class UPDATEINIFILE:
    def variables(self):
        self.NOW = datetime.now()

    def get_database_value(self, table, key):
        # Connect to the SQLite database
        conn = sqlite3.connect(SRC_USER_CONFIG_DB)
        cursor = conn.cursor()

        # Query the value from the specified table and key
        cursor.execute(f"SELECT value FROM {table} WHERE key = ?", (f'{key}',))
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        if result:
            if result[0] == 'True' or result[0] == 'Yes':
                return True
            elif result[0] == 'False' or result[0] == 'No':
                return False
            else:
                return result[0]  # The value is the first element in the result tuple
        else:
            return None  # Return None if the key doesn't exist

    def set_database_value(self, table, key, value):
        # Connect to the SQLite database
        conn = sqlite3.connect(SRC_USER_CONFIG_DB)
        cursor = conn.cursor()
            
        cursor.execute(f'''
            INSERT OR REPLACE INTO {table} (key, value)
            VALUES (?, ?)
        ''', (f'{key}', f'{value}'))

        conn.commit()
        conn.close()

    def get_value_from_table_key(self, table, key):
        # Connect to the SQLite database
        conn = sqlite3.connect(SRC_USER_CONFIG_DB)
        cursor = conn.cursor()

        # Query the value from the specified table and key
        cursor.execute(f"SELECT value FROM {table} WHERE key = ?", (key,))
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        if result:
            if result[0] == 'True':
                return True
            elif result[0] == 'False':
                return False
            else:
                return result[0]  # The value is the first element in the result tuple
        else:
            return None  # Return None if the key doesn't exist

    def ini_info_wallpaper(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['wallpaper']

    def ini_info_icon(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['icon']

    def ini_info_cursor(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['cursor']

    def ini_info_font(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['font']

    def ini_info_colortheme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['colortheme']

    def ini_info_gtktheme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['gtktheme']

    def ini_info_theme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['theme']

    ####################################################################
    # Date/time
    ####################################################################
    def day_name(self):
        NOW = datetime.now()
        return str(NOW.strftime("%a"))

    def current_date(self):
        NOW = datetime.now()
        return NOW.strftime("%d")

    def current_month(self):
        NOW = datetime.now()
        return NOW.strftime("%m")

    def current_year(self):
        NOW = datetime.now()
        return NOW.strftime("%y")

    def current_hour(self):
        # With 'now', current time will update by each hour
        NOW = datetime.now()
        return NOW.strftime("%H")

    def current_minute(self):
        # With 'now', current time will update by each minute
        NOW = datetime.now()
        return NOW.strftime("%M")

    def current_second(self):
        NOW = datetime.now()
        return int(NOW.strftime("%S"))

    def date_folder_format(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}"

    def time_folder_format(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{str(self.backup_date())}-{str(self.backup_month())}-{str(self.backup_year())}/{str(self.backup_hour())}-{str(self.backup_minute())}"

    def current_time(self):
        return int(f"{self.current_hour()}{self.current_minute()}")

    def backup_year(self):
        return self.NOW.strftime("%y")

    def backup_month(self):
        return self.NOW.strftime("%m")

    def backup_date(self):
        return self.NOW.strftime("%d")

    def backup_hour(self):
        return self.NOW.strftime("%H")

    def backup_minute(self):
        return self.NOW.strftime("%M")

    def backup_time_military(self):
        return int(f"{self.get_database_value('SCHEDULE', 'hours')}{self.get_database_value('SCHEDULE', 'minutes')}")

    ####################################################################
    # Folder creation
    ####################################################################
    def create_base_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}"

    def backup_folder_name(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}"

    # Wallpaper
    def wallpaper_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{WALLPAPER_FOLDER_NAME}"

    def application_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}"

    ####################################################################
    # System settings
    ####################################################################
    def icon_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{ICONS_FOLDER_NAME}"

    def cursor_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{CURSORS_FOLDER_NAME}"

    def fonts_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FONTS_FOLDER_NAME}"

    def gtk_theme_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GTK_THEME_FOLDER_NAME}"

    def theme_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{THEMES_FOLDER_NAME}"

    ####################################################################
    # KDE
    ####################################################################
    # Create kde folder
    def kde_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}"

    # KDE configurration folder
    def kde_configurations_folder_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}"

    # KDE CONFIG folder
    def kde_config_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{CONFIG_FOLDER_NAME}"

    # KDE .local/share
    def kde_local_share_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_FOLDER_NAME}"

    def kde_share_config_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_CONFIG_FOLDER_NAME}"

    ####################################################################
    # GNOME
    ####################################################################
    # Create gnome folder
    def gnome_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}"

    def gnome_configurations_folder_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}"

    # GNOME CONFIG folder
    def gnome_config_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{CONFIG_FOLDER_NAME}"

    # GNOME share folder
    def gnome_local_share_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_FOLDER_NAME}"

    ####################################################################
    # Packages managers
    ####################################################################
    # .rpm
    def rpm_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{RPM_FOLDER_NAME}"

    # .deb
    def deb_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{DEB_FOLDER_NAME}"

    ####################################################################
    # Flatpak
    ####################################################################
    def flatpak_txt_location(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{FLATPAK_TXT}"
    
    def flatpak_var_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{VAR_FOLDER_NAME}"

    def flatpak_local_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{LOCAL_FOLDER_NAME}"
    
    def create_flatpak_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}"

    ####################################################################
    # Exclude
    ####################################################################
    def exclude_apps_location(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{SRC_EXCLUDE_APPLICATIONS}"

    def exclude_applications_location(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{SRC_EXCLUDE_APPLICATIONS}"

    def restore_settings_location(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}"

    def get_backup_home_folders(self):
        from get_latest_backup_date import latest_backup_date
        return f"{self.backup_folder_name()}/{latest_backup_date()}"


if __name__ == '__main__':
    # MAIN_INI_FILE = UPDATEINIFILE()
    pass
