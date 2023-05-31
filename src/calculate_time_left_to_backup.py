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
    
        if timeLeft < 60:
            write_to_ini_file()
    
    elif int(backupHour) - int(currentBackupHour) == 0:
        timeLeft = int(backupMinute) - int(currentBackupMinute)
        write_to_ini_file()
 
def write_to_ini_file():
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('SCHEDULE', 'time_left', f'in {timeLeft} minutes...')
        config.write(configfile)
    
    print(f"In Approx. {timeLeft} minutes...")
    # return f"In Approx. {timeLeft} minutes..."

    # # Begin calculatiin if backup is 1 hour away
    # # Ex: current time: 09:00, backup time: 10:00
    # if int(backupHour) - int(currentBackupHour) == 1:
    #     timeLeft = 59 - int(currentBackupMinute) + int(backupMinute) 

    #     if not 0 < timeLeft > 59:
    #         config = configparser.ConfigParser()
    #         config.read(src_user_config)
    #         with open(src_user_config, 'w') as configfile:
    #             config.set('SCHEDULE', 'time_left', f'in {timeLeft} minutes...')
    #             config.write(configfile)
                
    #         return f"In Approx. {timeLeft} minutes..."
            
    # # Same Hour
    # elif  int(backupHour) - int(currentBackupHour) == 0:
    #     timeLeft = int(backupMinute) - int(currentBackupMinute) 

    #     if not 0 < timeLeft > 59:
    #         config = configparser.ConfigParser()
    #         config.read(src_user_config)
    #         with open(src_user_config, 'w') as configfile:
    #             config.set('SCHEDULE', 'time_left', f'in {timeLeft} minutes...')
    #             config.write(configfile)

    #         return f"In Approx. {timeLeft} minutes..."

if __name__ == '__main__':
    print(calculate_time_left_to_backup())
    pass