from setup import *


def next_backup_label():
    int_list = []
    
    # Current hour + 1
    next_backup_time = MAIN_INI_FILE.current_hour() + 1 

    # Under 10:00
    for i in str(next_backup_time):
        int_list.append(i)

    # Add 0 at the begin
    if len(int_list) == 1:
        int_list.insert(0, '0') 
        # Join
        next_backup_time = ''.join(int_list)

    return f'Today, {str(next_backup_time)}:00'


if __name__ == '__main__':
    pass