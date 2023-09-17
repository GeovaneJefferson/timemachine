from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()


def calculate_time_left_to_backup():
    # Current time
    current_time = datetime.now()

    # Next hour
    next_hour = int(MAIN_INI_FILE.current_hour()) + 1

    # Time of the next backup
    next_backup_time = current_time.replace(
        hour=next_hour, minute=0, second=0)

    # Calculate the time left
    time_left = next_backup_time - current_time

    # Extract hours and minutes from the time left
    # hours_left = time_left.seconds // 3600
    minutes_left = (time_left.seconds // 60) % 60

    # Return calculation
    return calculation(minutes_left)

def calculation(time_left):
    return f"In Approx. {time_left} minutes..."
            

if __name__ == '__main__':
    pass