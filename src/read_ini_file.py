from setup import *


NOW = datetime.now()
CONFIG = configparser.ConfigParser()
CONFIG.read(SRC_USER_CONFIG)


class UPDATEINIFILE:
    ####################################################################
    # INI
    ####################################################################
    def ini_hd_name(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return str(CONFIG['EXTERNAL']['name'])

    def ini_external_location(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return CONFIG['EXTERNAL']['hd']

    def ini_backing_up_now(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        # Not backing up
        if str(CONFIG['STATUS']['backing_up_now']) == 'False':
            return False

        # Current backing up
        else:
            return True

    def ini_unfinished_backup(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['STATUS']['unfinished_backup']) == 'No':
            return False

        else:
            return True

    def ini_automatically_backup(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        if CONFIG['STATUS']['automatically_backup'] == 'False':
            return False
        else:
            return True

    def ini_system_tray(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if CONFIG['SYSTEMTRAY']['system_tray'] == 'False':
            return False
        else:
            return True

    def ini_one_time_mode(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['MODE']['one_time_mode']) == 'False':
            return False
        else:
            return True

    def ini_multiple_time_mode(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['MODE']['more_time_mode']) == 'False':
            return False
        else:
            return True

    def ini_backup_hour(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return CONFIG['SCHEDULE']['hours']

    def ini_backup_minute(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return CONFIG['SCHEDULE']['minutes']

    def ini_next_backup_sun(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['DAYS']['sun']) == 'False':
            return False

        else:
            return True

    def ini_next_backup_mon(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['DAYS']['mon']) == 'False':
            return False
        else:
            return True

    def ini_next_backup_tue(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['DAYS']['tue']) == 'False':
            return False
        else:
            return True

    def ini_next_backup_wed(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['DAYS']['wed']) == 'False':
            return False

        else:
            return True

    def ini_next_backup_thu(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['DAYS']['thu']) == 'False':
            return False

        else:
            return True

    def ini_next_backup_fri(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['DAYS']['fri']) == 'False':
            return False
        else:
            return True

    def ini_next_backup_sat(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['DAYS']['sat']) == 'False':
            return False

        else:
            return True

    def ini_everytime(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return str(CONFIG['SCHEDULE']['everytime'])

    def ini_time_left(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if CONFIG['SCHEDULE']['time_left'] == 'None':
            return None

    def ini_extra_information(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        try:
            return CONFIG['INFO']['notification_add_info']
        except KeyError:
            return "None"

    def ini_current_backup_information(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return str(CONFIG['INFO']['current_backing_up'])
    
    def ini_restore_flatpaks_name(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['RESTORE']['applications_flatpak_names']) == 'False':
            return False
        else:
            return True
    
    def ini_restore_flatpaks_data(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        if str(CONFIG['RESTORE']['applications_flatpak_data']) == 'False':
            return False
        else:
            return True
        
    def ini_allow_flatpak_data(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if str(CONFIG['STATUS']['allow_flatpak_data']) == 'False':
            return False
        else:
            return True

    def ini_files_and_folders(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        if str(CONFIG['RESTORE']['files_and_folders']) == 'False':
            return False
        else:
            return True

    def ini_system_settings(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        if str(CONFIG['RESTORE']['system_settings']) == 'False':
            return False
        else:
            return True

    def ini_user_os(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return CONFIG['INFO']['os']

    def ini_folders(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return CONFIG.options('FOLDER')

    def ini_package_manager(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        return CONFIG['INFO']['packageManager']

    def ini_automatically_reboot(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if CONFIG['INFO']['auto_reboot'] == 'False':
            return False
        else:
            return True 

    def ini_applications_packages(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)

        if CONFIG['RESTORE']['applications_packages'] == 'False':
            return False
        elif CONFIG['RESTORE']['applications_packages'] == 'True':
            return True
        else:
            return None

    def ini_restoring_is_running(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        if str(CONFIG['RESTORE']['is_restore_running']) == 'False':
            return False
        else:
            return True

    def ini_info_wallpaper(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['wallpaper']

    def ini_info_icon(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['icon']

    def ini_info_cursor(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['cursor']

    def ini_info_font(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['font']

    def ini_info_colortheme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['colortheme']

    def ini_info_gtktheme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['gtktheme']

    def ini_info_theme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['theme']

    ####################################################################
    # Date/time
    ####################################################################
    def day_name(self):
        NOW = datetime.now()
        return str(NOW.strftime("%a"))

    def current_date(self):
        NOW=datetime.now()
        self.dateDay= NOW.strftime("%d")
        return self.dateDay

    def current_month(self):
        NOW=datetime.now()
        self.dateMonth=   NOW.strftime("%m")
        return self.dateMonth

    def current_year(self):
        NOW=datetime.now()
        self.dateYear=NOW.strftime("%y")
        return self.dateYear

    def current_hour(self):
        # With 'now', current time will update by each hour
        NOW = datetime.now()
        return  NOW.strftime("%H")

    def current_minute(self):
        # With 'now', current time will update by each minute
        NOW=datetime.now()
        return  NOW.strftime("%M")

    def current_second(self):
        NOW=datetime.now()
        return int(NOW.strftime("%S"))

    def date_folder_format(self):
        dateFolder=f"{str(self.backup_folder_name())}/{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}"
        return dateFolder

    def time_folder_format(self):
        value=f"{str(self.backup_folder_name())}/{str(self.backup_date())}-{str(self.backup_month())}-{str(self.backup_year())}/{str(self.backup_hour())}-{str(self.backup_minute())}"
        return value

    def current_time(self):
        value=f"{self.current_hour()}{self.current_minute()}"
        return int(value)

    def backup_year(self):
        return  NOW.strftime("%y")

    def backup_month(self):
        return  NOW.strftime("%m")

    def backup_date(self):
        return  NOW.strftime("%d")

    def backup_hour(self):
        return  NOW.strftime("%H")

    def backup_minute(self):
        return  NOW.strftime("%M")

    def backup_time_military(self):
        value=f"{str(self.ini_backup_hour())}{str(self.ini_backup_minute())}"
        return int(value)

    ####################################################################
    # Folder creation
    ####################################################################
    def create_base_folder(self):
        createBackupFolder=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}"
        return createBackupFolder

    def backup_folder_name(self):
        createBackupFolder=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}"
        return createBackupFolder

    # Wallpaper
    def wallpaper_main_folder(self):
        wallpaperMainFolder=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{WALLPAPER_FOLDER_NAME}"
        return wallpaperMainFolder

    def application_main_folder(self):
        applicationMainFolder=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}"
        return applicationMainFolder

    ####################################################################
    # System settings
    ####################################################################
    def icon_main_folder(self):
        iconsMainFolder=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{ICONS_FOLDER_NAME}"
        return iconsMainFolder

    def cursor_main_folder(self):
        cursorMainFolder=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{CURSORS_FOLDER_NAME}"
        return cursorMainFolder

    def fonts_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{FONTS_FOLDER_NAME}"

    def gtk_theme_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{GTK_THEME_FOLDER_NAME}"

    def theme_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{THEMES_FOLDER_NAME}"

    ####################################################################
    # KDE
    ####################################################################
    # Create kde folder
    def kde_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}"

    # KDE configurration folder
    def kde_configurations_folder_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}"

    # KDE CONFIG folder
    def kde_config_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{CONFIG_FOLDER_NAME}"

    # KDE .local/share
    def kde_local_share_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_FOLDER_NAME}"

    def kde_share_config_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_CONFIG_FOLDER_NAME}"

    ####################################################################
    # GNOME
    ####################################################################
    # Create gnome folder
    def gnome_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}"

    def gnome_configurations_folder_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}"

    # GNOME CONFIG folder
    def gnome_config_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{CONFIG_FOLDER_NAME}"

    # GNOME share folder
    def gnome_local_share_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_FOLDER_NAME}"

    ####################################################################
    # Packages managers
    ####################################################################
    # .rpm
    def rpm_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{RPM_FOLDER_NAME}"

    # .deb
    def deb_main_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{DEB_FOLDER_NAME}"

    ####################################################################
    # Flatpak
    ####################################################################
    def flatpak_txt_location(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{FLATPAK_TXT}"
    
    def flatpak_var_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{VAR_FOLDER_NAME}"

    def flatpak_local_folder(self):
        applicationLocalFolder=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{LOCAL_FOLDER_NAME}"
        return applicationLocalFolder
    
    def create_flatpak_folder(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}"

    ####################################################################
    # Exclude
    ####################################################################
    def exclude_apps_location(self):
        excludeAppsLoc=f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{SRC_EXCLUDE_APPLICATIONS}"
        return excludeAppsLoc

    def exclude_applications_location(self):
        return f"{self.ini_external_location()}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{SRC_EXCLUDE_APPLICATIONS}"

    def restore_settings_location(self):
        return f"{str(self.ini_external_location())}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}"

    def get_backup_home_folders(self):
        from get_latest_backup_date import latest_backup_date

        getbackupHomeFolders=f"{self.backup_folder_name()}/{latest_backup_date()}"
        return getbackupHomeFolders


if __name__ == '__main__':
    MAIN_INI_FILE=UPDATEINIFILE()
    pass
