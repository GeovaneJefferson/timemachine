from setup import *

now = datetime.now()
config = configparser.ConfigParser()
config.read(src_user_config)


class UPDATEINIFILE:
    ####################################################################
    # INI
    ####################################################################
    def ini_hd_name(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            self.iniHDName = config['EXTERNAL']['name']
            return self.iniHDName
        
        except:
            pass

    def ini_external_location(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['EXTERNAL']['hd']

    def ini_backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        try:
            return config['BACKUP']['backup_now']
        
        except:
            return "None"
        
    def ini_automatically_backup(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            return config['BACKUP']['auto_backup']
        
        except:
            return "false"

    def ini_system_tray(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SYSTEMTRAY']['system_tray']
   
    # def ini_oldest_backup(self):
    #     config = configparser.ConfigParser()
    #     config.read(src_user_config)
    #     return config['INFO']['oldest']   

    # def ini_lastest_backup(self):
    #     config = configparser.ConfigParser()
    #     config.read(src_user_config)
    #     return config['INFO']['latest']
    
    # def ini_next_backup(self):
    #     config = configparser.ConfigParser()
    #     config.read(src_user_config)
    #     self.iniNextBackup = config['INFO']['next']
    #     return self.iniNextBackup
    
    def ini_one_time_mode(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['MODE']['one_time_mode']
    
    def ini_multiple_time_mode(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['MODE']['more_time_mode']
    
    def ini_next_hour(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['hours']
     
    def ini_next_minute(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['minutes']
    
    def ini_next_backup_sun(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['sun']

    def ini_next_backup_mon(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['mon']
    
    def ini_next_backup_tue(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['tue']

    def ini_next_backup_wed(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['wed']

    def ini_next_backup_thu(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['thu']
    
    def ini_next_backup_fri(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['fri']

    def ini_next_backup_sat(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['sat']

    def ini_everytime(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['everytime']
    
    def ini_time_left(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['time_left']
                                                     
    def ini_extra_information(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        try:
            return config['INFO']['notification_add_info']
        except KeyError:
            return "None"

    def ini_current_backup_information(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            return config['INFO']['current_backing_up']
        except:
            pass
        
    def ini_allow_flatpak_names(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['BACKUP']['allow_flatpak_names']
    
    def ini_allow_flatpak_data(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['BACKUP']['allow_flatpak_data']
    
    def ini_files_and_folders(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['RESTORE']['files_and_folders']
    
    def ini_system_settings(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['RESTORE']['system_settings']
    
    def ini_user_os(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['INFO']['os']

    def ini_folders(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config.options('FOLDER')

    def ini_package_manager(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['INFO']['packageManager']
    
    def ini_automatically_reboot(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['INFO']['auto_reboot']
    
    def ini_applications_packages(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['RESTORE']['applications_packages']
    
    def ini_restoring_is_running(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['RESTORE']['is_restore_running']
    
    def ini_info_wallpaper(self):
        config = configparser.ConfigParser()
        config.read(f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}")
        return config['INFO']['wallpaper']

    def ini_info_icon(self):
        config = configparser.ConfigParser()
        config.read(f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}")
        return config['INFO']['icon']

    def ini_info_cursor(self):
        config = configparser.ConfigParser()
        config.read(f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}")
        return config['INFO']['cursor']
    
    def ini_info_font(self):
        config = configparser.ConfigParser()
        config.read(f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}")
        return config['INFO']['font']

    def ini_info_colortheme(self):
        config = configparser.ConfigParser()
        config.read(f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}")
        return config['INFO']['colortheme']

    def ini_info_gtktheme(self):
        config = configparser.ConfigParser()
        config.read(f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}")
        return config['INFO']['gtktheme']

    def ini_info_theme(self):
        config = configparser.ConfigParser()
        config.read(f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}")
        return config['INFO']['theme']
    
    ####################################################################
    # Date/time
    ####################################################################
    def day_name(self):
        now = datetime.now()
        self.dayName = now.strftime("%a")
        return self.dayName

    def current_date(self):
        now = datetime.now()
        self.dateDay = now.strftime("%d")
        return self.dateDay

    def current_month(self):
        now = datetime.now()
        self.dateMonth = now.strftime("%m")
        return self.dateMonth

    def current_year(self):
        now = datetime.now()
        self.dateYear = now.strftime("%y")
        return self.dateYear

    def current_hour(self):
        # With 'now', current time will update by each hour 
        now = datetime.now()
        return now.strftime("%H")

    def current_minute(self):
        # With 'now', current time will update by each minute 
        now = datetime.now()
        return now.strftime("%M")

    def current_second(self):
        now = datetime.now()
        return int(now.strftime("%S"))
    
    def date_folder_format(self):
        dateFolder = f"{str(self.backup_folder_name())}/{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}"
        return dateFolder

    def time_folder_format(self):
        timeFolder = f"{str(self.backup_folder_name())}/{str(self.backup_date())}-{str(self.backup_month())}-{str(self.backup_year())}/{str(self.backup_hour())}-{str(self.backup_minute())}"
        return timeFolder

    def current_time(self):
        return f"{self.current_hour()}{self.current_minute()}" 
    
    def backup_year(self):
        return now.strftime("%y") 

    def backup_month(self):
        return now.strftime("%m")
    
    def backup_date(self):
        return now.strftime("%d")

    def backup_hour(self):
        return now.strftime("%H") 

    def backup_minute(self):
        return now.strftime("%M") 

    def backup_time_military(self):
        backupTime = f"{str(self.ini_next_hour())}{str(self.ini_next_minute())}"
        return backupTime
    
    ####################################################################
    # Folder creation 
    ####################################################################
    def create_base_folder(self):
        createBackupFolder = f"{str(self.ini_external_location())}/{baseFolderName}"
        return createBackupFolder

    def backup_folder_name(self):
        createBackupFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{backupFolderName}"
        return createBackupFolder

    # Wallpaper
    def wallpaper_main_folder(self):
        wallpaperMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{wallpaperFolderName}"
        return wallpaperMainFolder
    
    def application_main_folder(self):
        applicationMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}"
        return applicationMainFolder

    def application_var_folder(self):
        applicationVarFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{varFolderName}"
        return applicationVarFolder

    def application_local_folder(self):
        applicationLocalFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{localFolderName}"
        return applicationLocalFolder

    ####################################################################
    # System settings
    ####################################################################
    def icon_main_folder(self):
        iconsMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{iconFolderName}"
        return iconsMainFolder

    def cursor_main_folder(self):
        cursorMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{cursorFolderName}"
        return cursorMainFolder

    def fonts_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{fontsFolderName}"

    def gtk_theme_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{gtkThemeFolderName}"
    
    def theme_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{themeFolderName}"
    
    def configurations_folder_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{configurationFolderName}"
    
    def gnome_local_share_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{gnomeFolderName}/{configurationFolderName}/{shareFolderName}"
    
    ####################################################################
    # KDE
    ####################################################################
    # KDE config folder
    def kde_config_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{kdeFolderName}/{configurationFolderName}/{configFolderName}"
   
    # KDE .local/share 
    def kde_local_share_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{kdeFolderName}/{configurationFolderName}/{shareFolderName}"
    
    ####################################################################
    # GNOME
    ####################################################################
    # GNOME config folder
    def gnome_config_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{gnomeFolderName}/{configurationFolderName}/{configFolderName}"
    
    def gnomeshell_main_folder(self):
        gnomeShellMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{gtkThemeFolderName}/{gnomeShellFolder}"
        return gnomeShellMainFolder

    def share_config_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{configurationFolderName}/{shareConfigFolderName}"

    ####################################################################
    # Packages managers
    ####################################################################
    # .rpm
    def rpm_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{rpmFolderName}"

    # .deb
    def deb_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{debFolderName}"

    ####################################################################
    # Flatpak
    ####################################################################
    def flatpak_txt_location(self):
        flatpakTxtFile = f"{str(self.ini_external_location())}/{baseFolderName}/{flatpakTxt}"
        return flatpakTxtFile
    
    ####################################################################
    # Exclude
    ####################################################################
    def exclude_apps_location(self):
        excludeAppsLoc = f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{src_exclude_applications}"
        return excludeAppsLoc
   
    def exclude_appsications_location(self):
        return f"{self.ini_external_location()}/{baseFolderName}/{applicationFolderName}/{src_exclude_applications}"
   
    def restore_settings_location(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}"
    
    def get_backup_home_folders(self):
        from get_latest_backup_date import latest_backup_date

        getbackupHomeFolders = f"{self.backup_folder_name()}/{latest_backup_date()}"
        return getbackupHomeFolders


if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    pass