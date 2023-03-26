from setup import *

class UPDATEINIFILE:
    def __init__(self):
        self.now = datetime.now()

    def day_name(self):
        self.dayName = self.now.strftime("%a")
        return self.dayName

    def current_hour(self):
        self.currentHour = self.now.strftime("%H")
        return self.currentHour

    def current_minute(self):
        self.currentMinute = self.now.strftime("%M")
        return self.currentMinute

    def ini_hd_name(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniHDName = config['EXTERNAL']['name']
        return self.iniHDName
    
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
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
        return self.iniAutomaticallyBackup

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
                                                     
    def current_time(self):
        self.currentTime = int(self.current_hour()) + int(self.current_minute())
        return self.currentTime

    def backup_time(self):
        self.backupTime = int(self.ini_next_hour()) + int(self.ini_next_minute())
        return self.backupTime
    
    def ini_extra_information(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniExtraInformation = config['INFO']['notification_add_info']
        return self.iniExtraInformation

    def ini_current_backup_information(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniCurrentBackupInfo = config['INFO']['feedback_status']
        return self.iniCurrentBackupInfo
    
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

    def create_backup_folder(self):
        self.createBackupFolder = f"{str(self.ini_external_location())}/{baseFolderName}/{backupFolderName}"
        return self.createBackupFolder