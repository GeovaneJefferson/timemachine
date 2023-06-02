from setup import *
from read_ini_file import UPDATEINIFILE

def calculate_time_left_to_backup():
    mainIniFile = UPDATEINIFILE()
    global timeLeft

    backupHour = mainIniFile.ini_next_hour() 
    currentBackupHour = mainIniFile.current_hour() 
    
    backupMinute = mainIniFile.ini_next_minute() 
    currentBackupMinute = mainIniFile.current_minute() 

    if int(backupHour) - int(currentBackupHour) == 1:
        timeLeft = (int(backupMinute) - int(currentBackupMinute) + 59)
    
        if timeLeft < 59:
            write_to_ini_file()
            return f"In Approx. {timeLeft} minutes..."
    
    elif int(backupHour) - int(currentBackupHour) == 0:
        timeLeft = int(backupMinute) - int(currentBackupMinute)
        write_to_ini_file()
        return f"In Approx. {timeLeft} minutes..."
 
def write_to_ini_file():
    print(f"In Approx. {timeLeft} minutes...")
    
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('SCHEDULE', 'time_left', f'In Approx. {timeLeft} minutes...')
        config.write(configfile)
    

if __name__ == '__main__':
    pass