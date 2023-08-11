from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()


def calculate_time_left_to_backup():
    global time_left

    # Backup hour
    backup_hour = MAIN_INI_FILE.get_database_value('SCHEDULE', 'hours')
    # Current hour
    current_hour = MAIN_INI_FILE.current_hour()
    # Backup minute
    backup_minute = MAIN_INI_FILE.get_database_value('SCHEDULE', 'minutes')
    # Current minute
    current_minute = MAIN_INI_FILE.current_minute()

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
    MAIN_INI_FILE.get_database_value('SCHEDULE', 'time_left', f'In Approx. {time_left} minutes...')


if __name__ == '__main__':
    pass
