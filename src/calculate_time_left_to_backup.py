from setup import *
from read_ini_file import UPDATEINIFILE

def calculate_time_left_to_backup():
    mainIniFile = UPDATEINIFILE()

    backupHour = mainIniFile.ini_next_hour() 
    currentBackupHour = mainIniFile.current_hour() 
    
    backupMinute = mainIniFile.ini_next_minute() 
    currentBackupMinute = mainIniFile.current_minute() 

    # Different Hour
    if int(backupHour) - int(currentBackupHour) == 1:
        timeLeft = 59 - int(currentBackupMinute) + int(backupMinute) 
        if not timeLeft < 0:
            if not timeLeft > 59:
                # Write time left, so main window can get it
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('SCHEDULE', 'time_left', f'in {timeLeft} minutes...')
                    config.write(configfile)
                    
                return f"In Approx. {timeLeft} minutes..."
            
    # Same Hour
    elif  int(backupHour) - int(currentBackupHour) == 0:
        timeLeft = int(backupMinute) - int(currentBackupMinute) 
        if not timeLeft < 0:
            if not timeLeft > 59:
                # Write time left, so main window can get it
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:
                    config.set('SCHEDULE', 'time_left', f'in {timeLeft} minutes...')
                    config.write(configfile)
                    
                return f"In Approx. {timeLeft} minutes..."
            

    return None


if __name__ == '__main__':
    pass