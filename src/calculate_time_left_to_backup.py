from setup import *
from read_ini_file import UPDATEINIFILE

def calculate_time_left_to_backup():
    MAININIFILE=UPDATEINIFILE()
    global time_left

    # Backup hour
    backup_hour=MAININIFILE.ini_next_hour()
    # Current hour
    current_hour=MAININIFILE.current_hour()
    # Backup minute
    backup_minute=MAININIFILE.ini_next_minute()
    # Current minute
    current_minute=MAININIFILE.current_minute()

    # If backup hour - current hour == 1, ex. backup hour=10, current hour=9
    if int(backup_hour) - int(current_hour) == 1:
        time_left=(int(backup_minute) - int(current_minute) + 59)

        if time_left < 59 and time_left >= 0:
            # Write time left to ini file
            write_to_ini_file()

            return f"In Approx. {time_left} minutes..."
        else:
            return None

    # If backup hour - current hour == 0, ex. backup hour=10, current hour=10
    elif int(backup_hour) - int(current_hour) == 0:
        time_left=int(backup_minute) - int(current_minute)

        if time_left >= 0:
            # Write time left to ini file
            write_to_ini_file()

            return f"In Approx. {time_left} minutes..."
        else:
            return None

def write_to_ini_file():
    print(f"In Approx. {time_left} minutes...")

    config=configparser.ConfigParser()
    config.read(SRC_USER_CONFIG)
    with open(SRC_USER_CONFIG, 'w') as configfile:
        config.set('SCHEDULE', 'time_left', f'In Approx. {time_left} minutes...')
        config.write(configfile)


if __name__ == '__main__':
    pass
