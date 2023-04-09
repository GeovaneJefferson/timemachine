from setup import *

now = datetime.now()
config = configparser.ConfigParser()
config.read(src_user_config)


class UPDATEINIFILE:
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
        self.iniExternalLocation = config['EXTERNAL']['hd']
        return self.iniExternalLocation

    def ini_backup_now(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniBackupNow = config['BACKUP']['backup_now']
        return self.iniBackupNow

    def ini_automatically_backup(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            return config['BACKUP']['auto_backup']
        except:
            pass

    def ini_system_tray(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SYSTEMTRAY']['system_tray']
   
    def exclude_appsications_location(self):
        return f"{self.ini_external_location()}/{baseFolderName}/{applicationFolderName}/{src_exclude_applications}"
   
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
        self.oneTimeMode = config['MODE']['one_time_mode']
        return self.oneTimeMode
    
    def ini_multiple_time_mode(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniMultipleTimePerDay = config['MODE']['more_time_mode']
        return self.iniMultipleTimePerDay
    
    # def ini_dark_mode(self):
    #     config = configparser.ConfigParser()
    #     config.read(src_user_config)
    #     self.darkMode = config['MODE']['dark_mode']
    #     return self.darkMode
     
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
        self.iniNextBackupSun = config['SCHEDULE']['sun']
        return self.iniNextBackupSun

    def ini_next_backup_mon(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextBackupMon = config['SCHEDULE']['mon']
        return self.iniNextBackupMon
    
    def ini_next_backup_tue(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        return config['SCHEDULE']['tue']

    def ini_next_backup_wed(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextBackupWed = config['SCHEDULE']['wed']
        return self.iniNextBackupWed

    def ini_next_backup_thu(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextBackupThu = config['SCHEDULE']['thu']
        return self.iniNextBackupThu
    
    def ini_next_backup_fri(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextBackupFri = config['SCHEDULE']['fri']
        return self.iniNextBackupFri

    def ini_next_backup_sat(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextBackupSat = config['SCHEDULE']['sat']
        return self.iniNextBackupSat

    def ini_everytime(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.everytime = config['SCHEDULE']['everytime']
        return self.everytime
    
    def ini_time_left(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniTimeLeft = config['SCHEDULE']['time_left']
        return self.iniTimeLeft
                                                     
    def ini_extra_information(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniExtraInformation = config['INFO']['notification_add_info']
        return self.iniExtraInformation

    def ini_current_backup_information(self):
        try:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            self.iniCurrentBackupInfo = config['INFO']['feedback_status']
            return self.iniCurrentBackupInfo
        except:
            pass
        
    def ini_allow_flatpak_names(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniAllowFlatpakNames = config['BACKUP']['allow_flatpak_names']
        return self.iniAllowFlatpakNames
    
    def ini_allow_flatpak_data(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniAllowFlatpakData = config['BACKUP']['allow_flatpak_data']
        return self.iniAllowFlatpakData
    
    def ini_files_and_folders(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniFilesAndsFolders = config['RESTORE']['files_and_folders']
        return self.iniFilesAndsFolders
    
    def ini_system_settings(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniSystemSettings = config['RESTORE']['system_settings']
        return self.iniSystemSettings
    
    def ini_user_os(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniUserOS = config['INFO']['os']
        return self.iniUserOS

    def ini_folders(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniFolders = config.options('FOLDER')
        return self.iniFolders
    
    def day_name(self):
        self.dayName = now.strftime("%a")
        return self.dayName

    def current_date(self):
        self.dateDay = now.strftime("%d")
        return self.dateDay

    def current_month(self):
        self.dateMonth = now.strftime("%m")
        return self.dateMonth

    def current_year(self):
        self.dateYear = now.strftime("%y")
        return self.dateYear

    def current_hour(self):
        self.currentHour = now.strftime("%H")
        return self.currentHour

    def current_minute(self):
        self.currentMinute = now.strftime("%M")
        return self.currentMinute

    def current_time(self):
        return f"{self.current_hour()}{self.current_minute()}" 

    def backup_time_military(self):
        backupTime = f"{str(self.ini_next_hour())}{str(self.ini_next_minute())}"
        return backupTime
    
    def create_base_folder(self):
        createBackupFolder = f"{str(self.ini_external_location())}/{baseFolderName}"
        return createBackupFolder

    def backup_folder_name(self):
        createBackupFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{backupFolderName}"
        return createBackupFolder

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

    def icon_main_folder(self):
        iconsMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{iconFolderName}"
        return iconsMainFolder

    def cursor_main_folder(self):
        cursorMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{cursorFolderName}"
        return cursorMainFolder

    def gtk_theme_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{gtkThemeFolderName}"
    
    def theme_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{themeFolderName}"
    
    def color_scheme_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{colorSchemeName}"
    
    def plasma_style_main_folder(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{desktopThemeName}"

    def gnomeshell_main_folder(self):
        gnomeShellMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{gtkThemeFolderName}/{gnomeShellFolder}"
        return gnomeShellMainFolder

    def rpm_main_folder(self):
        rpmMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{rpmFolderName}"
        return rpmMainFolder

    def deb_main_folder(self):
        debMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{debFolderName}"
        return debMainFolder

    def date_folder_format(self):
        dateFolder = f"{str(self.backup_folder_name())}/{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}"
        return dateFolder

    def time_folder_format(self):
        timeFolder = f"{str(self.backup_folder_name())}/{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}/{str(self.current_hour())}-{str(self.current_minute())}"
        return timeFolder

    def flatpak_txt_location(self):
        flatpakTxtFile = f"{str(self.ini_external_location())}/{baseFolderName}/{flatpakTxt}"
        return flatpakTxtFile
    
    def exclude_apps_location(self):
        excludeAppsLoc = f"{str(self.ini_external_location())}/{baseFolderName}/{applicationFolderName}/{src_exclude_applications}"
        return excludeAppsLoc

    def restore_settings_location(self):
        return f"{str(self.ini_external_location())}/{baseFolderName}/{restoreSettingsIni}"
    
    def ini_package_manager(self):
        self.packageManager = config['INFO']['packageManager']
        return self.packageManager
    
    def ini_automatically_reboot(self):
        self.iniAutoReboot = config['INFO']['auto_reboot']
        return self.iniAutoReboot
    
    def ini_applications_packages(self):
        self.iniApplicationsPackages = config['RESTORE']['applications_packages']
        return self.iniApplicationsPackages
    
    def get_backup_home_folders(self):
        from get_latest_backup_date import latest_backup_date

        getbackupHomeFolders = f"{self.backup_folder_name()}/{latest_backup_date()}"
        return getbackupHomeFolders
    
    def ini_restoring_is_running(self):
        iniIsRestoreRunning = config['RESTORE']['is_restore_running']
        return iniIsRestoreRunning
    
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


if __name__ == '__main__':
    pass