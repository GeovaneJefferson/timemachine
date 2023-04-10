from setup import *
from read_ini_file import UPDATEINIFILE

def calculate_time_left_to_backup():
    mainIniFile = UPDATEINIFILE()

    backupTime = mainIniFile.backup_time_military() 
    currentTime = f"{mainIniFile.current_hour()}{mainIniFile.current_minute()}" 
    timeLeft = int(backupTime) - int(currentTime)

    # print("backupTime:",backupTime)
    # print("currentTime:",currentTime)
    # print(timeLeft)

    # Fix timer
    if timeLeft > 59:
        x = timeLeft-59
        timeLeft = int(timeLeft-59) + x

    if 0 < timeLeft < 59:
        # Write time left, so main window can get it
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'time_left', f'in {timeLeft} minutes...')
            config.write(configfile)
            
        return f"Approx. in {timeLeft} minutes..."
    
    else:
        return None

if __name__ == '__main__':
    print(calculate_time_left_to_backup())
    pass