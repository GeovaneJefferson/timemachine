from setup import *

now = datetime.now()

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
            self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
            return self.iniAutomaticallyBackup
        except:
            pass

    def ini_system_tray(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
        return self.iniSystemTray
    
    def ini_oldest_backup(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniOldestBackup = config['INFO']['oldest']
        return self.iniOldestBackup
    
    def ini_lastest_backup(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniLastBackup = config['INFO']['latest']
        return self.iniLastBackup
    
    def ini_next_backup(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextBackup = config['INFO']['next']
        return self.iniNextBackup
    
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
    
    def ini_dark_mode(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.darkMode = config['MODE']['dark_mode']
        return self.darkMode
     
    def ini_next_hour(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextHour = config['SCHEDULE']['hours']
        return self.iniNextHour
     
    def ini_next_minute(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniNextMinute = config['SCHEDULE']['minutes']
        return self.iniNextMinute
    
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
        self.iniNextBackupTue = config['SCHEDULE']['tue']
        return self.iniNextBackupTue

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
        currentTime = int(self.current_hour()) + int(self.current_minute())
        return currentTime

    def backup_time(self):
        backupTime = int(self.ini_next_hour()) + int(self.ini_next_minute())
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

    def theme_main_folder(self):
        themeMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{themeFolderName}"
        return themeMainFolder

    def gnomeshell_main_folder(self):
        gnomeShellMainFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{themeFolderName}/{gnomeShellFolder}"
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
        timeFolder = f"{str(self.backup_folder_name())}/{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}/{str(self.current_hour())}-{str(self.current_hour())}"
        return timeFolder

    def flatpak_txt_location(self):
        flatpakTxtFile = f"{str(self.ini_external_location())}/{baseFolderName}/{flatpakTxt}"
        return flatpakTxtFile

if __name__ == '__main__':
    pass